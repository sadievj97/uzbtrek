/* Uzbekistan Trek: shared page script (forms to Telegram, mobile menu, departure picker).
   Reads window.TREK_CONFIG from assets/config.js:
     endpoint     URL of the Telegram relay (Cloudflare Worker), e.g. "https://uzbtrek-relay.example.workers.dev/submit".
                  Leave it empty and the form falls back to "copy the request and open Telegram".
     telegramBot  bot username without @, e.g. "uzbtrek_bot".
     email        address offered as a second way to send the request when the relay is not set up.
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

  function asText(form, fields) {
    var title = form.getAttribute("data-form-title") || "Trek request";
    return ["Uzbekistan Trek: " + title].concat(fields.map(function (f) { return f.label + (/[?:]$/.test(f.label) ? " " : ": ") + f.value; })).join("\n");
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

  function copyText(text, onDone) {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { onDone(true); }, function () { onDone(false); });
        return;
      }
    } catch (e) { /* fall through */ }
    onDone(false);
  }

  function telegramFallback(msg, text, intro, title) {
    setMsg(msg, "ok tg");
    line(msg, intro);
    var status = line(msg, "", "p");
    status.className = "tform-copied";
    var ta = document.createElement("textarea");
    ta.className = "tform-copy";
    ta.readOnly = true;
    ta.value = text;
    ta.rows = Math.min(10, text.split("\n").length + 1);
    ta.setAttribute("aria-label", "Your request");
    msg.appendChild(ta);
    var row = document.createElement("div");
    row.className = "tform-actions";
    var copy = document.createElement("button");
    copy.type = "button";
    copy.className = "tform-copybtn";
    copy.textContent = "Copy request";
    var open = document.createElement("a");
    open.className = "tform-tg";
    open.href = BOT_URL;
    open.target = "_blank";
    open.rel = "noopener";
    open.textContent = "Open Telegram: @" + BOT;
    row.appendChild(copy);
    row.appendChild(open);
    if (EMAIL) {
      var mail = document.createElement("a");
      mail.className = "tform-mail";
      mail.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Uzbekistan Trek: " + (title || "Trek request")) +
        "&body=" + encodeURIComponent(text);
      mail.textContent = "Or send it by email";
      row.appendChild(mail);
    }
    msg.appendChild(row);
    function done(ok) {
      status.textContent = ok ? "Copied. Paste it into the chat with @" + BOT + " and send, or use the email link." :
        "Copy the request below, then paste it into the chat with @" + BOT + ", or use the email link.";
      if (!ok) { ta.focus(); ta.select(); }
    }
    copy.addEventListener("click", function () { copyText(text, done); });
    copyText(text, done);
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
      var text = asText(form, fields);

      if (!CFG.endpoint) {
        telegramFallback(msg, text, "Last step: send this request to us on Telegram or by email.", form.getAttribute("data-form-title"));
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
          setMsg(msg, "ok");
          line(msg, "Request sent. We usually reply within three working days.");
          var p = line(msg, "For a faster answer, message us on Telegram: ");
          var a = document.createElement("a");
          a.href = BOT_URL; a.target = "_blank"; a.rel = "noopener"; a.textContent = "@" + BOT;
          p.appendChild(a);
        })
        .catch(function () {
          telegramFallback(msg, text, "We could not send your request automatically. Please send it to us on Telegram or by email instead.", form.getAttribute("data-form-title"));
        })
        .then(function () { submit.disabled = false; submit.textContent = label; });
    });
  });
})();
