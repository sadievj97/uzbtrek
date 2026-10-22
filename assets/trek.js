/* Uzbekistan Trek: shared page script (forms to Telegram, mobile menu, departure picker).
   Reads window.TREK_CONFIG from assets/config.js:
     endpoint     URL of the Telegram relay (Cloudflare Worker), e.g. "https://uzbtrek-relay.example.workers.dev/submit".
                  Forms send requests straight to the bot through it. If it is empty or unreachable, the visitor
                  sees a red message pointing to Telegram and email. Visit alerts go to the same relay at /visit.
     telegramBot  bot username without @, e.g. "uzbtrek_bot".
     email        address offered as a second way to send the request when the relay is not set up.
     analyticsToken  Cloudflare Web Analytics site token. When set, every page loads Cloudflare's visitor counter;
                  the numbers are visible only in the owner's Cloudflare dashboard. Leave empty to turn it off.
   Never put a Telegram bot token in this file or anywhere in the website: the site is public. */
(function () {
  "use strict";
  var CFG = window.TREK_CONFIG || {};
  var BOT = CFG.telegramBot || "uzbtrek_bot";
  var BOT_URL = "https://t.me/" + BOT;
  var EMAIL = CFG.email || "";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- every page opens at its top, showing the banner ----------
     Normal browsers already open a new page at the top. Some previews and app views keep the old scroll position,
     so the page also goes to its top when it loads (until the visitor scrolls), when it is left, after Back or a
     reload, and, inside a preview frame, the moment a link to another page is clicked.
     Links to a section (like #faq) keep their target. */
  var root = document.documentElement;
  function toTop(frames) {
    var was = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);
    if (frames && window.self !== window.top) {
      /* shown inside a taller frame: also scroll the outer page up to this page's first pixel */
      var pad = root.style.scrollPaddingTop;
      root.style.scrollPaddingTop = "0px";
      try { root.scrollIntoView({ block: "start" }); } catch (e) { /* ignore */ }
      root.style.scrollPaddingTop = pad;
    }
    root.style.scrollBehavior = was;
  }
  function wantsSection() {
    var id = "";
    try { id = location.hash ? decodeURIComponent(location.hash.slice(1)) : ""; } catch (e) { /* ignore */ }
    return !!(id && document.getElementById(id));
  }
  try { if ("scrollRestoration" in history) history.scrollRestoration = "manual"; } catch (e) { /* ignore */ }
  var touched = false;
  ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (t) {
    window.addEventListener(t, function () { touched = true; }, { passive: true, capture: true });
  });
  function startAtTop() { if (!touched && !wantsSection()) toTop(false); }
  startAtTop();
  document.addEventListener("DOMContentLoaded", startAtTop);
  window.addEventListener("load", function () { startAtTop(); setTimeout(startAtTop, 150); setTimeout(startAtTop, 450); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) { touched = false; startAtTop(); } });
  window.addEventListener("pagehide", function () { toTop(false); });
  /* inside a preview frame, the frame may keep its scroll position or swap the page in place:
     jump to the top as the link is followed (a normal browser tab already opens the next page at its top) */
  window.addEventListener("click", function (e) {
    if (window.self === window.top) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a || (a.target && a.target !== "_self") || a.hasAttribute("download")) return;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    if (!/^https?:$/.test(url.protocol) || url.origin !== location.origin || url.hash) return;   /* other sites, mail, and links to a section */
    toTop(true);
  }, true);

  /* ---------- visitor statistics and visit alerts: only the owner sees them; visitors see nothing ----------
     1. Counter: when assets/config.js has an analyticsToken, every page loads Cloudflare Web Analytics. The numbers
        appear only in the owner's Cloudflare dashboard; that token can send visits but cannot read them.
     2. Visit alerts: when someone arrives at the site (not when they move between its pages, reload or go back),
        the page tells the relay (the endpoint, with /visit instead of /submit) and @uzbtrek_bot sends the owner a note.
     Neither sets cookies. Opening any page with ?count=off stops both for that browser (for the owner's own visits);
     ?count=on turns them back on. */
  (function () {
    var token = String(CFG.analyticsToken || "").trim();
    var endpoint = String(CFG.endpoint || "").trim();
    var visitUrl = /\/submit\/?$/.test(endpoint) ? endpoint.replace(/\/submit\/?$/, "/visit") : "";
    var KEY = "uztrek-count";
    var m = /[?&]count=(on|off)(?:&|$)/.exec(location.search);
    if (!token && !visitUrl && !m) return;

    function sendVisit() {
      var nav = null;
      try { nav = performance.getEntriesByType("navigation")[0]; } catch (e) { /* ignore */ }
      if (nav && (nav.type === "reload" || nav.type === "back_forward")) return;   /* not a new arrival */
      var ref = "";
      try { ref = document.referrer ? new URL(document.referrer).hostname : ""; } catch (e) { /* ignore */ }
      if (ref === location.hostname) return;   /* moving between the site's own pages */
      if (navigator.webdriver) return;   /* automated browsers */
      var tag = "";
      try { tag = new URLSearchParams(location.search).get("utm_source") || ""; } catch (e) { /* ignore */ }
      var data = JSON.stringify({ page: location.pathname, ref: ref, src: tag.slice(0, 40) });
      function send() {
        try { if (navigator.sendBeacon && navigator.sendBeacon(visitUrl, data)) return; } catch (e) { /* use fetch */ }
        try { fetch(visitUrl, { method: "POST", body: data, mode: "no-cors", keepalive: true }).catch(function () {}); } catch (e) { /* ignore */ }
      }
      if (document.prerendering) document.addEventListener("prerenderingchange", send, { once: true });   /* only once actually shown */
      else send();
    }

    function note(text) {
      function show() {
        var n = document.createElement("div");
        n.setAttribute("role", "status");
        n.setAttribute("data-count-note", "");
        n.textContent = text;
        n.style.cssText = "position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:9999;" +
          "width:max-content;max-width:calc(100% - 32px);box-sizing:border-box;padding:12px 18px;border-radius:999px;" +
          "background:#13234B;color:#fff;font-weight:600;font-size:15px;line-height:1.35;text-align:center;" +
          "box-shadow:0 6px 24px rgba(19,35,75,.35)";
        document.body.appendChild(n);
        setTimeout(function () { if (n.parentNode) n.parentNode.removeChild(n); }, 5000);
      }
      if (document.body) show(); else document.addEventListener("DOMContentLoaded", show);
    }

    var off = !!(m && m[1] === "off"), saved = false;
    try {
      if (m) { if (m[1] === "off") localStorage.setItem(KEY, "off"); else localStorage.removeItem(KEY); }
      saved = true;
      if (localStorage.getItem(KEY) === "off") off = true;
    } catch (e) { /* this browser blocks site storage */ }
    if (m) {
      try {   /* take ?count=... out of the address, so a copied link does not carry it */
        var q = new URLSearchParams(location.search);
        q.delete("count");
        q = q.toString();
        history.replaceState(history.state, "", location.pathname + (q ? "?" + q : "") + location.hash);
      } catch (e) { /* ignore */ }
      note(!saved ? "This browser does not let the site save this setting."
        : m[1] === "off" ? "Visits from this browser are no longer counted." : "Visits from this browser are counted again.");
    }
    if (off) return;
    if (token) {
      var s = document.createElement("script");
      s.defer = true;
      s.src = "https://static.cloudflareinsights.com/beacon.min.js";
      s.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
      document.head.appendChild(s);
    }
    if (visitUrl && !m) sendVisit();   /* no note for the visit that only switches ?count on or off */
  })();

  /* ---------- mobile menu: a button with [data-menu-btn] toggles the element with [data-menu] ---------- */
  document.querySelectorAll("[data-menu-btn]").forEach(function (btn) {
    var menu = document.getElementById(btn.getAttribute("aria-controls")) || document.querySelector("[data-menu]");
    if (!menu) return;
    btn.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.textContent = open ? "Close" : "Menu";
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a") && menu.classList.contains("open")) {
        menu.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.textContent = "Menu";
      }
    });
  });

  /* ---------- planned departure buttons: [data-pick] fills the small-group form ---------- */
  document.querySelectorAll("[data-pick]").forEach(function (b) {
    b.addEventListener("click", function () {
      var form = document.querySelector('form.tform[data-form="small-group"]');
      if (!form) return;
      var sel = form.querySelector('select[name="departure"]');
      if (sel) sel.value = b.getAttribute("data-pick");
      var join = form.querySelector('input[name="option"][value="Join a departure"]');
      if (join) join.checked = true;
      form.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      var first = form.querySelector('input[name="name"]');
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, reduce ? 0 : 450);
    });
  });

  /* ---------- sample texts (home page guide): links to a sample open it; copy buttons copy its text ---------- */
  function openSample(id) {
    var el = id ? document.getElementById(id) : null;
    var d = el ? (el.tagName === "DETAILS" ? el : el.querySelector("details")) : null;
    if (d) d.open = true;
  }
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href^="#sample-"]') : null;
    if (a) openSample(a.getAttribute("href").slice(1));
  });
  if (/^#sample-/.test(location.hash)) openSample(location.hash.slice(1));
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var status = btn.parentNode.querySelector(".copy-status");
    var timer = null;
    function say(text) {
      if (!status) return;
      status.textContent = text;
      clearTimeout(timer);
      timer = setTimeout(function () { status.textContent = ""; }, 5000);
    }
    btn.addEventListener("click", function () {
      var src = document.getElementById(btn.getAttribute("data-copy"));
      if (!src) return;
      function selectIt() {   /* when the browser refuses the clipboard: open the text and select it */
        var box = src.closest(".sample");
        if (box) openSample(box.id);
        try {
          var range = document.createRange();
          range.selectNodeContents(src);
          var sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
          say("Text selected: press Ctrl+C (or Cmd+C) to copy.");
        } catch (err) { say("Open the text and copy it by hand."); }
      }
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(src.textContent).then(function () { say("Copied."); }, selectIt);
        } else { selectIt(); }
      } catch (err) { selectIt(); }
    });
  });

  /* ---------- forms ---------- */
  function fieldsOf(form) {
    var out = [], seen = {};
    form.querySelectorAll("input, select, textarea").forEach(function (el) {
      if (!el.name || el.name === "website") return;
      if ((el.type === "checkbox" || el.type === "radio") && !el.checked) return;
      var v = String(el.value || "").trim();
      if (!v) return;
      var label = el.getAttribute("data-label") || el.name;
      if (Object.prototype.hasOwnProperty.call(seen, label)) { out[seen[label]].value += ", " + v; return; }
      seen[label] = out.length;
      out.push({ label: label, value: v });
    });
    return out;
  }

  function validate(form) {
    var bad = null, names = [];
    form.querySelectorAll("[data-req]").forEach(function (el) {
      var v = String(el.value || "").trim();
      var ok = el.type === "email" ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) : v.length > 0;
      if (ok && el.type === "number") {
        var n = Number(v);
        if (!isFinite(n) || (el.min !== "" && n < Number(el.min)) || (el.max !== "" && n > Number(el.max))) ok = false;
      }
      el.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok) { names.push(el.getAttribute("data-req")); if (!bad) bad = el; }
    });
    return { bad: bad, names: names };
  }

  function setMsg(msg, kind) { msg.className = "tform-msg " + kind; msg.hidden = false; msg.textContent = ""; }

  function line(parent, text, tag) {
    var p = document.createElement(tag || "p");
    p.textContent = text;
    parent.appendChild(p);
    return p;
  }

  /* green line under the button when the request has reached the bot */
  function showSent(msg) {
    setMsg(msg, "sent");
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 20 20"); svg.setAttribute("aria-hidden", "true"); svg.setAttribute("focusable", "false");
    var path = document.createElementNS(ns, "path");
    path.setAttribute("d", "M5 10.5 8.5 14 15 6.5");
    svg.appendChild(path);
    msg.appendChild(svg);
    msg.appendChild(document.createTextNode("Your message has been successfully sent!"));
  }

  /* red message when the request could not be sent; the form keeps what the visitor typed */
  function showFailed(msg) {
    setMsg(msg, "err");
    line(msg, "Sorry, your message could not be sent. Please try again in a minute.");
    var p = line(msg, "You can also write to us on Telegram at ");
    var a = document.createElement("a");
    a.href = BOT_URL; a.target = "_blank"; a.rel = "noopener"; a.textContent = "@" + BOT;
    p.appendChild(a);
    if (EMAIL) {
      p.appendChild(document.createTextNode(" or by email at "));
      var m = document.createElement("a");
      m.href = "mailto:" + EMAIL; m.textContent = EMAIL;
      p.appendChild(m);
    }
    p.appendChild(document.createTextNode("."));
  }

  document.querySelectorAll("form.tform").forEach(function (form) {
    var msg = form.querySelector(".tform-msg");
    var submit = form.querySelector('[type="submit"]');
    if (!msg || !submit) return;
    var label = submit.textContent;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = validate(form);
      if (v.bad) {
        setMsg(msg, "err");
        msg.textContent = "Please add " + v.names.join(", ") + ".";
        v.bad.focus();
        return;
      }
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) { form.reset(); setMsg(msg, "ok"); msg.textContent = "Thank you."; return; }

      var fields = fieldsOf(form);

      if (!CFG.endpoint) {   /* the relay address is missing in assets/config.js */
        showFailed(msg);
        return;
      }

      submit.disabled = true;
      submit.textContent = "Sending";
      var payload = {
        form: form.getAttribute("data-form") || "",
        title: form.getAttribute("data-form-title") || "",
        page: location.href,
        fields: fields,
        website: ""
      };
      fetch(CFG.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) {
          if (!r.ok) throw new Error("status " + r.status);
          form.reset();
          showSent(msg);
        })
        .catch(function () { showFailed(msg); })
        .then(function () { submit.disabled = false; submit.textContent = label; });
    });
  });
})();
