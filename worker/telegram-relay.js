/**
 * Uzbekistan Trek: Telegram relay (Cloudflare Worker, free plan is enough).
 *
 * What it does
 *   POST /submit    receives website form requests and sends them to you through your bot (@uzbtrek_bot).
 *   POST /telegram  Telegram webhook: makes @uzbtrek_bot a two-way chat. Anything a visitor writes to the bot
 *                   is forwarded to you; when you REPLY to a forwarded message in your chat with the bot,
 *                   the bot sends your reply back to that visitor.
 *   POST /visit     someone arrived at the website: the bot sends you a short note (page, where they came from,
 *                   approximate place, device). The site sends it once per arrival, not for every page.
 *
 * Settings (Cloudflare dashboard > your Worker > Settings > Variables and Secrets)
 *   BOT_TOKEN        secret: the token BotFather gave you for @uzbtrek_bot. Never put it in the website.
 *   ADMIN_CHAT_ID    your Telegram user id (open @uzbtrek_bot and press Start first, so the bot may write to you).
 *   WEBHOOK_SECRET   secret: any long random string; the same value goes into setWebhook (see README).
 *   ALLOWED_ORIGINS  your site address(es), comma separated, e.g. https://yourname.github.io,https://uzbekistantrek.com
 *   WELCOME_TEXT     optional: the message visitors see after /start.
 *   VISIT_ALERTS     optional: "on" (default: visit notes arrive without a sound), "loud" (with a sound) or "off".
 */

const MAX_BODY = 12000;
const RATE = new Map(); // best-effort, per worker instance: ip -> [timestamps]

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS || "*").split(",").map((s) => s.trim()).filter(Boolean);
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes("*") ? "*" : (allowed.includes(origin) ? origin : allowed[0] || ""),
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
      "Vary": "Origin",
    };

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (url.pathname === "/submit" && request.method === "POST") return handleSubmit(request, env, cors, origin, allowed);
    if (url.pathname === "/telegram" && request.method === "POST") return handleTelegram(request, env);
    if (url.pathname === "/visit" && request.method === "POST") return handleVisit(request, env, ctx, cors, origin, allowed);
    return new Response("Uzbekistan Trek relay is running.", { status: 200, headers: { "Content-Type": "text/plain" } });
  },
};

function json(data, status, headers) {
  return new Response(JSON.stringify(data), { status, headers: { ...headers, "Content-Type": "application/json" } });
}

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function tg(env, method, payload) {
  const r = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  let data = {};
  try { data = await r.json(); } catch (e) { /* ignore */ }
  return data;
}

function rateLimited(ip) {
  const now = Date.now();
  const list = (RATE.get(ip) || []).filter((t) => now - t < 10 * 60 * 1000);
  list.push(now);
  RATE.set(ip, list);
  return list.length > 8; // more than 8 requests in 10 minutes from one address
}

async function handleSubmit(request, env, cors, origin, allowed) {
  if (!allowed.includes("*") && !allowed.includes(origin)) return json({ ok: false, error: "origin" }, 403, cors);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (rateLimited(ip)) return json({ ok: false, error: "rate" }, 429, cors);

  const raw = await request.text();
  if (raw.length > MAX_BODY) return json({ ok: false, error: "size" }, 413, cors);
  let body;
  try { body = JSON.parse(raw); } catch (e) { return json({ ok: false, error: "json" }, 400, cors); }
  if (body.website) return json({ ok: true }, 200, cors); // honeypot filled: quietly ignore bots

  const fields = Array.isArray(body.fields) ? body.fields.slice(0, 30) : [];
  if (!fields.length) return json({ ok: false, error: "empty" }, 400, cors);

  const lines = [
    `🧭 <b>${esc(body.title || "New request")}</b>`,
    "",
    ...fields.map((f) => {
      const label = String(f.label || "").slice(0, 60);
      return `<b>${esc(label)}${/[?:]$/.test(label) ? "" : ":"}</b> ${esc(String(f.value || "").slice(0, 1500))}`;
    }),
    "",
    `<i>${esc(String(body.page || "").slice(0, 200))}</i>`,
  ];
  let text = lines.join("\n");
  if (text.length > 4000) text = text.slice(0, 3990) + "…";

  const res = await tg(env, "sendMessage", { chat_id: env.ADMIN_CHAT_ID, text, parse_mode: "HTML", link_preview_options: { is_disabled: true } });
  if (!res.ok) return json({ ok: false, error: "telegram" }, 502, cors);
  return json({ ok: true }, 200, cors);
}

// ------------------------------------------------------------------ visit alerts
const VISIT_IP = new Map();                       // best-effort, per worker instance: ip -> [timestamps]
const VISIT_MINUTE = { minute: 0, count: 0 };
const BOT_UA = /bot|crawl|spider|slurp|preview|headless|lighthouse|pagespeed|inspectiontool|facebookexternalhit|embedly|monitor|uptime/i;
const PAGES = new Map([["", "Home page"], ["index.html", "Home page"], ["big-group.html", "Big group page"],
  ["small-group.html", "Small group page"], ["founder.html", "Founder page"]]);
const SOURCES = [
  [/(^|\.)google\.[a-z.]+$/, "Google"], [/(^|\.)bing\.com$/, "Bing"], [/(^|\.)duckduckgo\.com$/, "DuckDuckGo"],
  [/(^|\.)yandex\.[a-z.]+$/, "Yandex"], [/(^|\.)instagram\.com$/, "Instagram"], [/(^|\.)(facebook|fb)\.com$/, "Facebook"],
  [/(^|\.)linkedin\.com$|^lnkd\.in$/, "LinkedIn"], [/^t\.me$|(^|\.)telegram\.org$/, "Telegram"],
  [/^t\.co$|(^|\.)(x|twitter)\.com$/, "X (Twitter)"], [/(^|\.)youtube\.com$|^youtu\.be$/, "YouTube"],
  [/(^|\.)whatsapp\.(com|net)$/, "WhatsApp"], [/(^|\.)chatgpt\.com$/, "ChatGPT"], [/(^|\.)perplexity\.ai$/, "Perplexity"],
];

async function handleVisit(request, env, ctx, cors, origin, allowed) {
  const done = () => new Response(null, { status: 204, headers: cors });
  const mode = String(env.VISIT_ALERTS || "on").trim().toLowerCase();
  if (mode === "off") return done();
  if (!allowed.includes("*") && !allowed.includes(origin)) return new Response(null, { status: 403, headers: cors });
  const ua = request.headers.get("User-Agent") || "";
  if (!ua || BOT_UA.test(ua)) return done();   // search engines, link previews, monitors

  // flood guard: one note per address every 10 seconds and at most 20 an hour; at most 30 a minute in total
  const now = Date.now();
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const seen = (VISIT_IP.get(ip) || []).filter((t) => now - t < 60 * 60 * 1000);
  if ((seen.length && now - seen[seen.length - 1] < 10 * 1000) || seen.length >= 20) return done();
  seen.push(now);
  if (VISIT_IP.size > 5000) VISIT_IP.clear();
  VISIT_IP.set(ip, seen);
  const minute = Math.floor(now / 60000);
  if (VISIT_MINUTE.minute !== minute) { VISIT_MINUTE.minute = minute; VISIT_MINUTE.count = 0; }
  if (++VISIT_MINUTE.count > 30) return done();

  let body = {};
  try { body = JSON.parse((await request.text()).slice(0, 2000)) || {}; } catch (e) { /* keep it empty */ }
  const tag = String(body.src || "").slice(0, 40);
  const where = placeName(request.cf || {});
  const lines = [
    `👀 <b>New visitor</b>: ${esc(pageName(body.page))}`,
    `From: ${esc(sourceName(body.ref))}${tag ? ` (link tag: ${esc(tag)})` : ""}`,
    where ? `Where: ${esc(where)} (approximate)` : "",
    `Device: ${esc(deviceName(ua))}`,
  ].filter(Boolean);
  const send = tg(env, "sendMessage", {
    chat_id: env.ADMIN_CHAT_ID, text: lines.join("\n"), parse_mode: "HTML",
    disable_notification: mode !== "loud", link_preview_options: { is_disabled: true },
  }).catch(() => {});
  if (ctx && ctx.waitUntil) ctx.waitUntil(send); else await send;
  return done();
}

function pageName(path) {
  const last = String(path || "").split(/[?#]/)[0].split("/").pop().slice(0, 80);
  return PAGES.get(last) || last;
}

function sourceName(host) {
  const h = String(host || "").toLowerCase().replace(/[^a-z0-9.-]/g, "").slice(0, 100);
  if (!h) return "direct (typed address, bookmark or an app)";
  for (const [re, name] of SOURCES) if (re.test(h)) return name;
  return h;
}

function placeName(cf) {
  let country = String(cf.country || "");
  if (country === "XX") country = "";              // unknown
  else if (country === "T1") country = "Tor network";
  try { if (/^[A-Z]{2}$/.test(country)) country = new Intl.DisplayNames(["en"], { type: "region" }).of(country) || country; } catch (e) { /* keep the code */ }
  const parts = [cf.city, cf.region, country].map((s) => String(s || "").slice(0, 60)).filter(Boolean);
  return parts.filter((p, i) => parts.indexOf(p) === i).join(", ");
}

function deviceName(ua) {
  const os = /iPhone/.test(ua) ? "iPhone" : /iPad/.test(ua) ? "iPad"
    : /Android/.test(ua) ? (/Mobile/.test(ua) ? "Android phone" : "Android tablet")
    : /Macintosh|Mac OS X/.test(ua) ? "Mac" : /Windows/.test(ua) ? "Windows" : /CrOS/.test(ua) ? "Chromebook" : /Linux/.test(ua) ? "Linux" : "";
  const app = /Instagram/.test(ua) ? "Instagram app" : /FBAN|FBAV|FB_IAB/.test(ua) ? "Facebook app" : /LinkedInApp/.test(ua) ? "LinkedIn app"
    : /Telegram/i.test(ua) ? "Telegram app" : /Edg(?:e|A|iOS)?\//.test(ua) ? "Edge" : /OPR\/|Opera/.test(ua) ? "Opera"
    : /Firefox|FxiOS/.test(ua) ? "Firefox" : /CriOS|Chrome\//.test(ua) ? "Chrome" : /Safari\//.test(ua) ? "Safari" : "";
  return [os, app].filter(Boolean).join(", ") || "unknown device";
}

async function handleTelegram(request, env) {
  if (env.WEBHOOK_SECRET && request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.WEBHOOK_SECRET) {
    return new Response("forbidden", { status: 403 });
  }
  let update;
  try { update = await request.json(); } catch (e) { return new Response("ok"); }
  const msg = update.message;
  if (!msg || !msg.chat) return new Response("ok");

  const admin = String(env.ADMIN_CHAT_ID);
  const fromId = String(msg.chat.id);

  // 1) You reply to a forwarded visitor message: send your reply to that visitor.
  if (fromId === admin) {
    const replied = msg.reply_to_message;
    const tagText = replied ? (replied.text || replied.caption || "") : "";
    const m = tagText.match(/#u(\d+)/);
    if (m) {
      const res = await tg(env, "copyMessage", { chat_id: m[1], from_chat_id: admin, message_id: msg.message_id });
      await tg(env, "sendMessage", {
        chat_id: admin,
        text: res.ok ? "✅ Sent." : `⚠️ Not delivered: ${res.description || "unknown error"}`,
        reply_parameters: { message_id: msg.message_id, allow_sending_without_reply: true },
      });
    } else if (msg.text === "/start" || msg.text === "/help") {
      await tg(env, "sendMessage", {
        chat_id: admin,
        text: "You are the admin of this bot. Website requests and visitor messages arrive here. To answer a visitor, reply to their message.",
      });
    }
    return new Response("ok");
  }

  // 2) A visitor writes to the bot.
  const who = [msg.from && msg.from.first_name, msg.from && msg.from.last_name].filter(Boolean).join(" ") || "Visitor";
  const handle = msg.from && msg.from.username ? ` (@${msg.from.username})` : "";
  if (msg.text === "/start") {
    await tg(env, "sendMessage", {
      chat_id: fromId,
      text: env.WELCOME_TEXT ||
        "Salom! Welcome to Uzbekistan Trek 🇺🇿\n\nTell us about your trip: how many people, which university, and when you would like to travel. We usually reply within three working days, often sooner.",
    });
    await tg(env, "sendMessage", { chat_id: admin, text: `👋 ${esc(who)}${esc(handle)} started the bot. #u${fromId}`, parse_mode: "HTML" });
    return new Response("ok");
  }

  const header = `💬 <b>${esc(who)}</b>${esc(handle)} #u${fromId}`;
  if (msg.text) {
    await tg(env, "sendMessage", { chat_id: admin, text: `${header}\n\n${esc(msg.text).slice(0, 3800)}`, parse_mode: "HTML" });
  } else {
    await tg(env, "sendMessage", { chat_id: admin, text: `${header}\n(attachment below; reply to this message to answer)`, parse_mode: "HTML" });
    await tg(env, "copyMessage", { chat_id: admin, from_chat_id: fromId, message_id: msg.message_id });
  }
  return new Response("ok");
}
