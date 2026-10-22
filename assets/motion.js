/* Uzbekistan Trek: motion for the main site.
   - Home banner: only the khatam stars move, at different depths, on scroll and with the mouse. The photo stays still.
   - Sample itinerary: the fast train runs the route while the section is pinned (a bus for the mountain day);
     city cards swap at each stop.
   - Buttons: on hover a fill runs across from left to right, with a copy of the label riding on it;
     pills are magnetic, their label and shadow move at different depths; button rows drift gently on scroll.
   - Yellow bands: the khatam watermark drifts slowly on scroll.
   Photos do not move.
   Respects "reduce motion": with it on, nothing moves and the itinerary shows every stop as a list.
   If anything fails, the page stays fully usable (the "mo" class is removed). */
(function () {
  "use strict";
  var doc = document.documentElement;
  var mm = function (q) { return !!(window.matchMedia && window.matchMedia(q).matches); };
  if (mm("(prefers-reduced-motion: reduce)")) return;
  var fine = mm("(hover: hover) and (pointer: fine)");
  doc.classList.add("mo");
  try { init(); } catch (err) {
    doc.classList.remove("mo");
    if (window.console && console.warn) console.warn("Uzbekistan Trek: motion is off.", err);
  }

  function init() {
    var $ = function (s, r) { return (r || document).querySelector(s); };
    var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
    var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
    var raf = window.requestAnimationFrame || function (f) { return setTimeout(f, 16); };

    /* ---------- hero ---------- */
    var hero = $(".hero[data-parallax]");
    var tx = 0, ty = 0, mx = 0, my = 0, heroH = 0, heroLoop = false;
    function heroTick() {
      mx += (tx - mx) * 0.08; my += (ty - my) * 0.08;
      if (Math.abs(tx - mx) < 0.001 && Math.abs(ty - my) < 0.001) { mx = tx; my = ty; heroLoop = false; }
      hero.style.setProperty("--mx", mx.toFixed(4));
      hero.style.setProperty("--my", my.toFixed(4));
      if (heroLoop) raf(heroTick);
    }
    function heroKick() { if (!heroLoop) { heroLoop = true; raf(heroTick); } }
    if (hero && fine) {
      hero.addEventListener("pointermove", function (e) {
        if (e.pointerType && e.pointerType !== "mouse") return;
        var r = hero.getBoundingClientRect();
        tx = clamp(((e.clientX - r.left) / r.width - 0.5) * 2, -1, 1);
        ty = clamp(((e.clientY - r.top) / r.height - 0.5) * 2, -1, 1);
        heroKick();
      });
      hero.addEventListener("pointerleave", function () { tx = 0; ty = 0; heroKick(); });
    }

    /* ---------- itinerary route ---------- */
    var routeSec = $(".route-pin"), routePath = $("#routePath"), routeDone = $("#routeDone"), train = $("#train"), bus = $("#bus");
    var routeMap = $(".map"), hint = $(".map-hint"), busFrom = -1, busBack = -1, lastBus = null;
    var dots = $$(".map .stop-dot"), cityLabels = $$(".map .city"), cards = $$(".stop-card");
    var stopCity = cards.map(function (c) { return c.getAttribute("data-city"); });
    var routeLen = 0, stopLens = [], routeTop = 0, routeH = 0;
    if (routePath && routePath.getTotalLength) {
      routeLen = routePath.getTotalLength();
      stopLens = routePath.getAttribute("data-stops").split(",").map(function (v) { return +v * routeLen; });
      var bi = parseInt(routePath.getAttribute("data-bus-from"), 10);
      if (!isNaN(bi) && stopLens[bi] != null) { busFrom = stopLens[bi]; if (stopLens[bi + 1] != null) busBack = stopLens[bi + 1]; }
      if (routeDone) { routeDone.style.strokeDasharray = routeLen + " " + routeLen; routeDone.style.strokeDashoffset = String(routeLen); }
    }
    var lastIdx = -1;
    function setActive(idx) {
      if (idx === lastIdx) return;
      lastIdx = idx;
      cards.forEach(function (c, i) { c.classList.toggle("on", i === idx); });
      var seen = {};
      for (var i = 0; i <= idx; i++) seen[stopCity[i]] = true;
      dots.forEach(function (d) { var c = d.getAttribute("data-city"); d.classList.toggle("on", !!seen[c]); d.classList.toggle("now", c === stopCity[idx]); });
      cityLabels.forEach(function (l) { l.classList.toggle("now", l.getAttribute("data-city") === stopCity[idx]); });
    }
    var DWELL = 0.7, TRAVEL = 1;
    function routeAt(p) {
      var n = stopLens.length, u = p * (n * DWELL + (n - 1) * TRAVEL);
      for (var i = 0; i < n; i++) {
        if (u <= DWELL) return { l: stopLens[i], idx: i };
        u -= DWELL;
        if (i < n - 1) {
          if (u <= TRAVEL) {
            var e = u / TRAVEL;
            e = e < 0.5 ? 2 * e * e : 1 - Math.pow(-2 * e + 2, 2) / 2;
            return { l: stopLens[i] + (stopLens[i + 1] - stopLens[i]) * e, idx: e < 0.5 ? i : i + 1 };
          }
          u -= TRAVEL;
        }
      }
      return { l: stopLens[n - 1], idx: n - 1 };
    }
    function setRoute(p) {
      if (!routeLen || !train || !stopLens.length) return;
      var r = routeAt(p), l = clamp(r.l, 0, routeLen);
      var a = routePath.getPointAtLength(clamp(l - 1.5, 0, routeLen)), b = routePath.getPointAtLength(clamp(l + 1.5, 0, routeLen));
      var pt = routePath.getPointAtLength(l), ang = Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI;
      var onBus = !!bus && busFrom >= 0 && l > busFrom + 0.5;
      var back = onBus && busBack >= 0 && l > busBack + 0.5;
      var phase = onBus ? (back ? 2 : 1) : 0;
      if (phase !== lastBus) {
        lastBus = phase;
        if (routeMap) routeMap.classList.toggle("by-bus", onBus);
        if (hint) hint.textContent = ["Scroll to ride the fast train", "To the mountains by bus", "Back to Tashkent by bus"][phase];
      }
      var pos = "translate(" + pt.x.toFixed(1) + " " + pt.y.toFixed(1) + ")";
      train.setAttribute("transform", pos + " rotate(" + ang.toFixed(1) + ")");
      if (bus) {
        /* keep the bus wheels down: mirror it instead of turning it upside down */
        var left = Math.abs(ang) > 90, bang = left ? ang - (ang > 0 ? 180 : -180) : ang;
        bus.setAttribute("transform", pos + " rotate(" + bang.toFixed(1) + ")" + (left ? " scale(-1 1)" : ""));
      }
      if (routeDone) routeDone.style.strokeDashoffset = String(Math.max(0, routeLen - l));
      setActive(r.idx);
    }
    if (cards.length) setActive(0);

    /* ---------- buttons: wrap the label so it can move on its own layer ---------- */
    $$(".btn").forEach(function (b) {
      if (b.querySelector(".bt") || !b.firstChild) return;
      var s = document.createElement("span");
      s.className = "bt";
      while (b.firstChild) s.appendChild(b.firstChild);
      b.appendChild(s);
    });

    /* ---------- buttons: a copy of the label rides on the hover fill, so the text color changes exactly at its edge ---------- */
    $$(".btn:not([type=submit]), .mini, .choice .go").forEach(function (b) {
      if (b.querySelector(".sw")) return;
      var s = document.createElement("span");
      s.className = "sw";
      s.setAttribute("aria-hidden", "true");
      Array.prototype.forEach.call(b.childNodes, function (n) { s.appendChild(n.cloneNode(true)); });
      b.appendChild(s);
      b.classList.add("has-sw");
    });

    if (fine) {
      /* magnetic pill buttons */
      $$(".btn").forEach(function (b) {
        b.addEventListener("pointermove", function (e) {
          if (e.pointerType && e.pointerType !== "mouse") return;
          var r = b.getBoundingClientRect();
          var dx = clamp((e.clientX - (r.left + r.width / 2)) / (r.width / 2), -1, 1);
          var dy = clamp((e.clientY - (r.top + r.height / 2)) / (r.height / 2), -1, 1);
          b.classList.add("mag");
          b.style.setProperty("--bx", (dx * 7).toFixed(2) + "px");
          b.style.setProperty("--by", (dy * 5).toFixed(2) + "px");
          b.style.setProperty("--lx", (dx * 5).toFixed(2) + "px");
          b.style.setProperty("--ly", (dy * 3).toFixed(2) + "px");
        });
        b.addEventListener("pointerleave", function () {
          b.classList.remove("mag");
          ["--bx", "--by", "--lx", "--ly"].forEach(function (p) { b.style.removeProperty(p); });
        });
      });

    }

    /* ---------- scroll-driven pieces ---------- */
    var floats = $$("[data-float]");
    var marks = $$(".band-yellow, .page-hero, .inc-text");
    var vh = 0, wide = false;
    function docTop(el) { return el.getBoundingClientRect().top + window.pageYOffset; }

    function measure() {
      vh = window.innerHeight; wide = window.innerWidth >= 860;
      heroH = hero ? hero.offsetHeight : 0;
      if (routeSec) { routeTop = docTop(routeSec); routeH = routeSec.offsetHeight; }
      floats.forEach(function (el) { el.style.translate = ""; el._top = docTop(el); el._h = el.offsetHeight; });
      marks.forEach(function (el) { el._top = docTop(el); el._h = el.offsetHeight; });
      update();
    }
    var measureT = 0;
    function measureSoon() { clearTimeout(measureT); measureT = setTimeout(measure, 120); }

    var ticking = false;
    function onScroll() { if (!ticking) { ticking = true; raf(update); } }

    function update() {
      ticking = false;
      var y = window.pageYOffset;
      if (hero && y < heroH + 80) hero.style.setProperty("--y", Math.max(0, y).toFixed(1));
      if (routeSec && routeLen && routeH > vh) setRoute(clamp((y - routeTop) / Math.max(1, routeH - vh), 0, 1));
      var mid = y + vh / 2, k = wide ? 1 : 0.45;
      floats.forEach(function (el) {
        if (el._top + el._h < y - 300 || el._top > y + vh + 300) return;
        var d = (el._top + el._h / 2 - mid) * (+el.getAttribute("data-float") || 0) * k;
        el.style.translate = "0 " + clamp(d, -60, 60).toFixed(1) + "px";
      });
      marks.forEach(function (el) {
        if (el._top + el._h < y || el._top > y + vh) return;
        el.style.setProperty("--wy", ((y - el._top) * 0.18).toFixed(1));
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", measureSoon);
    window.addEventListener("load", measure);
    if ("ResizeObserver" in window) new ResizeObserver(measureSoon).observe(document.body);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measureSoon);
    measure();
  }
})();
