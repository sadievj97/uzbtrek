"""Motion pieces for the main (yellow and navy) site: the hero stars, the train route map, and their CSS.

Used by styles/deck/build.py. The behaviour lives in shared/assets/motion.js.
"""
import math

# ------------------------------------------------------------------ small path helpers
def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------ khatam stars
def star_outline_path(cx=24, cy=24, R=22.6, r=17.3):
    pts = []
    for i in range(16):
        rad = R if i % 2 == 0 else r
        a = math.radians(-90 + i * 22.5)
        pts.append(f"{f(cx + rad * math.cos(a))} {f(cy + rad * math.sin(a))}")
    return "M" + "L".join(pts) + "Z"


STAR_OUTLINE = star_outline_path()

# (left %, top %, width px, depth 0..1, opacity, kind, desktop only)
HERO_STARS = [
    (-5, 4, 280, 0.18, 0.20, "line", False),
    (84, 10, 72, 0.85, 0.95, "logo", False),
    (11, 60, 28, 0.95, 0.9, "fill", False),
    (70, 50, 130, 0.42, 0.28, "line", True),
    (29, 16, 18, 1.0, 0.75, "fill", True),
    (63, 7, 22, 0.7, 0.6, "fill", True),
    (88, 44, 320, 0.12, 0.13, "line", True),
    (5, 33, 46, 0.6, 0.45, "line", True),
    (93, 72, 24, 0.95, 0.85, "fill", False),
    (46, 3, 36, 0.55, 0.35, "line", True),
]


def hero_stars(yellow="#FBB617", navy="#13234B"):
    out = []
    for i, (x, y, w, d, o, kind, dsk) in enumerate(HERO_STARS):
        if kind == "line":
            inner = f'<path d="{STAR_OUTLINE}" fill="none" stroke="{yellow}" stroke-width="{1.4 if w > 100 else 2}" vector-effect="non-scaling-stroke"/>'
        elif kind == "fill":
            inner = f'<path d="{STAR_OUTLINE}" fill="{yellow}"/>'
        else:
            inner = (f'<g fill="{yellow}"><rect x="8" y="8" width="32" height="32" rx="1.5"/><rect x="8" y="8" width="32" height="32" rx="1.5" transform="rotate(45 24 24)"/></g>'
                     f'<g fill="{navy}"><rect x="15" y="15" width="18" height="18"/><rect x="15" y="15" width="18" height="18" transform="rotate(45 24 24)"/></g>'
                     f'<circle cx="24" cy="24" r="4.2" fill="{yellow}"/>')
        spin = 70 + (i * 17) % 60
        out.append(f'<span class="hs{" dsk" if dsk else ""}" style="left:{x}%;top:{y}%;width:{w}px;--d:{d};--o:{o};--spin:{spin}s;--i:{i}">'
                   f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false">{inner}</svg></span>')
    return "".join(out)


# ------------------------------------------------------------------ watermark tile for yellow bands
def watermark_uri(color="#1C3166", opacity=0.07):
    star = star_outline_path(80, 80, 30, 22.9)
    small = star_outline_path(0, 0, 9, 6.9)
    small2 = star_outline_path(160, 160, 9, 6.9)
    small3 = star_outline_path(160, 0, 9, 6.9)
    small4 = star_outline_path(0, 160, 9, 6.9)
    diamonds = "M80 4l5 5-5 5-5-5Z M80 146l5 5-5 5-5-5Z M4 80l5-5 5 5-5 5Z M146 80l5-5 5 5-5 5Z"
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160' viewBox='0 0 160 160'>"
           f"<g fill='none' stroke='{color}' stroke-opacity='{opacity}' stroke-width='1.6'>"
           f"<path d='{star}'/><path d='{small}{small2}{small3}{small4}'/><path d='{diamonds}'/>"
           f"<path d='M80 50V110M50 80H110' stroke-opacity='{opacity * 0.6:.3f}'/></g></svg>")
    return "data:image/svg+xml," + svg.replace("#", "%23").replace("<", "%3C").replace(">", "%3E").replace('"', "'")


# ------------------------------------------------------------------ route map (sample itinerary)
CITIES = {
    "tas": {"name": "Tashkent", "card": "Tashkent", "xy": (760, 170), "sub": "Days 1, 6 and 8", "lab": (746, 126, "end")},
    "buk": {"name": "Bukhara", "card": "Bukhara", "xy": (170, 345), "sub": "Days 2 and 3", "lab": (148, 336, "end")},
    "sam": {"name": "Samarkand", "card": "Samarkand", "xy": (480, 352), "sub": "Days 4 and 5", "lab": (470, 292, "middle")},
    "mtn": {"name": "Mountains", "card": "Tashkent mountains", "xy": (858, 112), "sub": "Day 7, by bus", "lab": (888, 60, "end")},
}
ROUTE = ["tas", "buk", "sam", "tas", "mtn", "tas"]
ROUTE_CTRL = [
    ((700, 380), (420, 520)),   # day 2: fast train to Bukhara
    ((250, 290), (390, 290)),   # day 4: fast train to Samarkand
    ((560, 300), (650, 150)),   # day 5: Samarkand to Tashkent
    ((780, 120), (815, 88)),    # day 7: into the Tashkent mountains
    ((884, 150), (826, 204)),   # day 8: back to Tashkent for departures
]
STOPS = [
    {"city": "tas", "days": [1], "photo": "tashkent_minor_mosque", "cap": "A tiled portal, Tashkent"},
    {"city": "buk", "days": [2, 3], "photo": "hero_mir_i_arab", "cap": None},
    {"city": "sam", "days": [4, 5], "photo": "samarkand_registan_night", "cap": None},
    {"city": "tas", "days": [6], "photo": "a006", "cap": "Blue domes, Tashkent"},
    {"city": "mtn", "days": [7], "photo": "mountains_snow", "cap": None},
    {"city": "tas", "days": [8], "photo": "a030", "cap": None},
]


def bezier_len(p0, c1, c2, p1, steps=600):
    length, prev = 0.0, p0
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1 - t
        x = mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * p1[0]
        y = mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * p1[1]
        length += math.hypot(x - prev[0], y - prev[1])
        prev = (x, y)
    return length


MAP_TITLE = ("Route of the sample itinerary: arrival in Tashkent, fast train to Bukhara, fast train to Samarkand, back to Tashkent, "
             "a day in the Tashkent mountains by bus, departures from Tashkent. Khiva can be added as an option.")
BUS_FROM = 3   # stop index where the bus takes over: Tashkent (day 6) to the mountains and back


def route_geometry():
    pts = [CITIES[c]["xy"] for c in ROUTE]
    d = f"M{pts[0][0]} {pts[0][1]}"
    curves, lens = [], [0.0]
    for (c1, c2), p0, p1 in zip(ROUTE_CTRL, pts[:-1], pts[1:]):
        c = f"C{c1[0]} {c1[1]} {c2[0]} {c2[1]} {p1[0]} {p1[1]}"
        curves.append(c)
        d += c
        lens.append(lens[-1] + bezier_len(p0, c1, c2, p1))
    rail = f"M{pts[0][0]} {pts[0][1]}" + "".join(curves[:BUS_FROM])
    road = f"M{pts[BUS_FROM][0]} {pts[BUS_FROM][1]}" + "".join(curves[BUS_FROM:])
    return d, [round(v / lens[-1], 5) for v in lens], rail, road


def route_svg(text=None):
    """text (optional) gives the map's words in another language: {"cities": {city id: (name, sub)}, "khiva": (name, sub),
    "title": the description read by screen readers}. Without it the words come from CITIES and the English defaults below."""
    text = text or {}
    names = text.get("cities", {})
    khiva_name, khiva_sub = text.get("khiva", ("Khiva", "Optional add-on"))
    d, fracs, rail, road = route_geometry()
    dots, labels = "", ""
    for cid, c in CITIES.items():
        x, y = c["xy"]
        lx, ly, anchor = c["lab"]
        dots += (f'<g class="stop-dot" data-city="{cid}"><circle class="halo" cx="{x}" cy="{y}" r="22"/>'
                 f'<circle class="ring" cx="{x}" cy="{y}" r="11"/><circle class="core" cx="{x}" cy="{y}" r="5"/></g>')
        name, csub = names.get(cid, (c["name"], c["sub"]))
        labels += (f'<g class="city" data-city="{cid}"><text x="{lx}" y="{ly}" text-anchor="{anchor}">{name}</text>'
                   f'<text class="sub" x="{lx}" y="{ly + 22}" text-anchor="{anchor}">{csub}</text></g>')
    peaks = "M866 178l15-30 15 30Z M878 178l11-21 11 21Z M856 178l10-17 10 17Z"
    dunes = ("M40 470C90 455 130 455 180 468C230 481 260 480 300 468"
             "M90 500C140 488 180 488 230 498C270 506 300 505 340 496")
    train = ('<g id="train" transform="translate(760 170)"><g transform="translate(-36 0)">'
             '<rect x="0" y="-6.5" width="21" height="13" rx="3.5"/><rect x="23" y="-6.5" width="21" height="13" rx="3.5"/>'
             '<path d="M46 -6.5H60Q72 0 60 6.5H46Z"/><rect class="stripe" x="1" y="-1.3" width="66" height="2.6"/></g></g>')
    bus = ('<g id="bus" transform="translate(760 170)"><rect x="-21" y="-11" width="42" height="18" rx="4.5"/>'
           '<rect class="win" x="-17" y="-8" width="26" height="6" rx="1.5"/><rect class="win" x="12" y="-8" width="6" height="8" rx="1.5"/>'
           '<rect class="stripe" x="-21" y="1.5" width="42" height="2.4"/>'
           '<circle class="wheel" cx="-11" cy="8" r="3.8"/><circle class="wheel" cx="11" cy="8" r="3.8"/></g>')
    khiva = ('<g class="extra" data-city="khi"><path class="opt-link" d="M170 345C176 268 92 214 60 120"/>'
             '<circle class="opt-ring" cx="60" cy="120" r="11"/><path class="opt-plus" d="M60 114.5v11M54.5 120h11"/>'
             f'<text x="84" y="113">{khiva_name}</text><text class="sub" x="84" y="137">{khiva_sub}</text></g>')
    return f"""<svg class="map" viewBox="0 0 900 520" role="img" aria-labelledby="mapTitle" focusable="false">
  <title id="mapTitle">{text.get("title", MAP_TITLE)}</title>
  <defs><pattern id="dotgrid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#FFFFFF" fill-opacity=".11"/></pattern></defs>
  <rect width="900" height="520" fill="url(#dotgrid)"/>
  <path d="{dunes}" fill="none" stroke="#FBB617" stroke-opacity=".32" stroke-width="2" stroke-linecap="round"/>
  <path d="{peaks}" fill="#3A5294"/>
  {khiva}
  <path class="rail" d="{rail}"/>
  <path class="road" d="{road}"/>
  <path class="rail-done" id="routeDone" d="{d}"/>
  <path id="routePath" d="{d}" fill="none" stroke="none" data-stops="{','.join(str(v) for v in fracs)}" data-bus-from="{BUS_FROM}"/>
  {dots}
  {labels}
  {train}
  {bus}
</svg>"""


# ------------------------------------------------------------------ CSS for all of the above (appended to the site CSS)
MOTION_CSS = r"""
/* ---------- home hero: still photo; only the khatam stars move (scroll and mouse) ---------- */
.hero{ position:relative; overflow:hidden; overflow:clip; isolation:isolate; background:var(--navy-deep); color:var(--white);
  --y:0; --mx:0; --my:0; }
.hero > .hl{ position:absolute; pointer-events:none; }
.hero-photo{ inset:0; z-index:0; }
.hero-photo img{ width:100%; height:100%; object-fit:cover; object-position:center 42%; }
.hero-shade{ inset:0; z-index:1; background:
  radial-gradient(120% 70% at 50% 30%, rgba(19,35,75,.18), rgba(19,35,75,.55) 70%),
  linear-gradient(180deg, rgba(19,35,75,.45) 0%, rgba(19,35,75,.28) 38%, rgba(19,35,75,.82) 100%); }
.hero-stars{ inset:0; z-index:2; }
.hs{ position:absolute; display:block; opacity:var(--o);
  transform:translate3d(calc(var(--mx) * var(--d) * 34px), calc(var(--y) * (.32 - var(--d) * .62) * 1px + var(--my) * var(--d) * 22px), 0) rotate(calc(var(--y) * var(--d) * .09deg));
  animation:hsIn 1.1s cubic-bezier(.2,.8,.2,1) both; animation-delay:calc(var(--i) * 70ms); }
.hs svg{ display:block; width:100%; height:auto; overflow:visible; animation:hsSpin var(--spin) linear infinite; }
@keyframes hsIn{ from{ opacity:0; scale:.55; } }
@keyframes hsSpin{ to{ rotate:360deg; } }
.hero > .side{ z-index:5; }
.hero > .wrap{ position:relative; z-index:5; padding-block:clamp(40px, 5.5vw, 76px); }
.choice .s{ display:none; }

/* ---------- group boxes: no parallax, a small lift on hover ---------- */
.choice{ transition:transform .45s cubic-bezier(.2,.9,.25,1), box-shadow .45s cubic-bezier(.2,.9,.25,1); }

/* ---------- pill buttons: magnetic, with the label and a hard shadow at different depths ---------- */
.btn{ --bx:0px; --by:0px; --lx:0px; --ly:0px; position:relative;
  transform:translate3d(var(--bx), var(--by), 0);
  box-shadow:calc(4px - var(--bx) * .7) calc(5px - var(--by) * .7) 0 0 var(--btn-sh, rgba(19,35,75,.28));
  transition:transform .55s cubic-bezier(.2,.9,.25,1), box-shadow .55s cubic-bezier(.2,.9,.25,1), background-size .55s cubic-bezier(.4,0,.2,1), color .3s ease .12s; }
.btn .bt{ display:inline-block; transform:translate3d(var(--lx), var(--ly), 0); transition:transform .55s cubic-bezier(.2,.9,.25,1); }
.btn.mag{ transition-duration:.35s, .35s, .55s, .3s; }
.btn.mag .bt{ transition-duration:.35s; }
.btn-yellow{ --btn-sh:rgba(0,0,0,.32); }
.band-navy .btn-navy, .itin .btn-navy{ --btn-sh:rgba(0,0,0,.35); }
.nav .btn{ --btn-sh:rgba(19,35,75,.18); }
.btn:active{ --bx:1px; --by:2px; }

/* ---------- yellow bands: a light khatam watermark that drifts on scroll ---------- */
.band-yellow, .page-hero, .inc-text{ --wy:0; background-color:var(--yellow);
  background-image:radial-gradient(ellipse 62% 78% at 50% 50%, var(--yellow) 30%, rgba(251,182,23,.55) 62%, rgba(251,182,23,0) 100%), url("__WM__");
  background-size:100% 100%, 160px 160px; background-repeat:no-repeat, repeat;
  background-position:center, calc(50% + 80px) calc(var(--wy) * 1px); }

/* ---------- itinerary: the train runs the route ---------- */
.itin{ --navh:75px; background:var(--navy-deep); color:var(--white); position:relative; }
.itin-head{ position:relative; background-color:var(--navy-deep); background-position:center; background-size:cover; padding-block:clamp(60px, 8vw, 100px) 10px; }
.itin-head .lede{ color:#E6EBF7; }
.itin h2{ color:var(--white); }
.route-stage{ display:grid; grid-template-columns:minmax(0,1.12fr) minmax(0,.88fr); gap:clamp(20px, 3.5vw, 48px); align-items:start; padding-block:30px; }
.map-wrap{ position:sticky; top:calc(var(--navh) + 20px); }
.map{ width:100%; height:auto; display:block; overflow:visible; }
.map .rail{ fill:none; stroke:#FFFFFF; stroke-opacity:.38; stroke-width:3; stroke-dasharray:2 9; stroke-linecap:round; }
.map .rail-done{ fill:none; stroke:var(--yellow); stroke-width:4.5; stroke-linecap:round; }
.map .ring{ fill:var(--navy-deep); stroke:#FFFFFF; stroke-width:3; }
.map .core{ fill:var(--yellow); }
.map .halo{ fill:var(--yellow); opacity:0; transform-box:fill-box; transform-origin:center; }
.mo .map .core{ fill:#FFFFFF; opacity:.35; transition:fill .3s ease, opacity .3s ease; }
.mo .map .stop-dot.on .core{ fill:var(--yellow); opacity:1; }
.mo .map .stop-dot.now .halo{ animation:halo 1.8s ease-out infinite; }
@keyframes halo{ from{ opacity:.6; transform:scale(.4); } to{ opacity:0; transform:scale(1.25); } }
.map .city text{ font-family:var(--sans); font-weight:850; font-stretch:110%; font-size:27px; fill:#FFFFFF; letter-spacing:.03em; text-transform:uppercase; }
.map .city text.sub{ font-weight:500; font-stretch:100%; font-size:15px; fill:#C8D0E6; text-transform:none; letter-spacing:0; }
.mo .map .city.now text:not(.sub){ fill:var(--yellow); }
#train{ fill:#FFFFFF; transition:opacity .25s ease; }
#train .stripe{ fill:var(--yellow); }
#bus{ fill:#FFFFFF; opacity:0; transition:opacity .25s ease; }
#bus .win, #bus .wheel{ fill:var(--navy-deep); }
#bus .wheel{ stroke:#FFFFFF; stroke-width:1.6; }
#bus .stripe{ fill:var(--yellow); }
.map.by-bus #bus{ opacity:1; }
.map.by-bus #train{ opacity:0; }
.map .road{ fill:none; stroke:#FFFFFF; stroke-opacity:.38; stroke-width:3; stroke-dasharray:10 7; stroke-linecap:round; }
.map .opt-link{ fill:none; stroke:var(--yellow); stroke-opacity:.6; stroke-width:2.5; stroke-dasharray:2 8; stroke-linecap:round; }
.map .opt-ring{ fill:var(--navy-deep); stroke:var(--yellow); stroke-width:2.5; stroke-dasharray:4 3; }
.map .opt-plus{ fill:none; stroke:var(--yellow); stroke-width:2.4; stroke-linecap:round; }
.map .extra text{ font-family:var(--sans); font-weight:850; font-stretch:110%; font-size:24px; fill:#C8D0E6; letter-spacing:.03em; text-transform:uppercase; }
.map .extra text.sub{ font-weight:600; font-stretch:100%; font-size:15px; fill:var(--yellow); text-transform:none; letter-spacing:0; }
.map-hint{ display:none; margin-top:8px; font-size:14px; color:#C8D0E6; text-align:center; }
.stops{ display:grid; gap:20px; }
.stop-card{ background:var(--navy); border:1px solid rgba(255,255,255,.14); border-radius:20px; overflow:hidden; box-shadow:0 22px 44px rgba(0,0,0,.35); }
.stop-photo{ position:relative; overflow:hidden; background:#24396F; }
.stop-photo img{ width:100%; aspect-ratio:16/9; object-fit:cover; }
.stop-photo .cap{ position:absolute; left:12px; bottom:12px; background:rgba(19,35,75,.86); color:#FFFFFF; font-size:13px; font-weight:650; padding:4px 11px; border-radius:999px; }
.stop-text{ padding:18px 22px 22px; }
.stop-n{ font-size:13.5px; color:var(--yellow); font-weight:750; letter-spacing:.04em; text-transform:uppercase; }
.stop-text h3{ margin-top:4px; font-size:clamp(28px, 3vw, 40px); font-weight:850; font-stretch:110%; text-transform:uppercase; color:#FFFFFF; }
.sday{ margin-top:12px; }
.sday b{ font-weight:900; font-stretch:110%; color:var(--yellow); font-size:20px; letter-spacing:.02em; text-transform:uppercase; }
.sday .where{ display:block; font-size:16px; color:#FFFFFF; }
.sday ul{ list-style:none; margin:6px 0 0; padding:0; display:flex; flex-wrap:wrap; gap:6px; }
.sday li{ font-size:14px; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.18); border-radius:999px; padding:3px 11px; color:#FFFFFF; }
.tailor-row{ display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr); gap:clamp(24px, 4vw, 56px); align-items:center; padding-block:clamp(30px, 5vw, 60px) clamp(64px, 8vw, 104px); }
.tailor-row .tailor{ margin-top:0; grid-template-columns:1fr; }
.tailor-row .pol{ --r:3deg; width:min(300px, 100%); justify-self:center; }

/* pinned route (motion only) */
.mo .route-pin{ height:500vh; height:500svh; }
.mo .route-stage{ position:sticky; top:0; height:100vh; height:100svh; align-items:center; padding-top:calc(var(--navh) + 14px); padding-bottom:20px; }
.mo .map-wrap{ position:relative; top:auto; }
.mo .stops{ position:relative; height:min(600px, calc(100svh - var(--navh) - 60px)); }
.mo .stop-card{ position:absolute; inset:0; display:flex; flex-direction:column; opacity:0; transform:translateY(26px) scale(.98); transition:opacity .45s ease, transform .45s ease; pointer-events:none; }
.mo .stop-card.on{ opacity:1; transform:none; pointer-events:auto; }
.mo .stop-photo{ flex:1 1 auto; min-height:0; }
.mo .stop-photo img{ height:100%; aspect-ratio:auto; }
.mo .stop-text{ flex:none; }
.mo .map-hint{ display:block; }

@media (max-width: 980px){
  .route-stage{ grid-template-columns:minmax(0,1fr); }
  .map-wrap{ position:static; }
  .mo .route-pin{ height:440vh; height:440svh; }
  .mo .route-stage{ display:flex; flex-direction:column; gap:10px; align-items:stretch; }
  .mo .map-wrap{ flex:none; }
  .mo .map{ max-height:30svh; width:auto; max-width:100%; margin:0 auto; }
  .mo .map-hint{ margin-top:2px; }
  .mo .stops{ height:auto; flex:1 1 auto; min-height:0; }
  .tailor-row{ grid-template-columns:minmax(0,1fr); }
}
@media (max-width: 640px){
  .hs.dsk{ display:none; }
  .hero .ask small{ display:none; }
  .hero .ask{ margin:22px auto 12px; }
  .choices{ gap:12px; }
  .choice{ grid-template-rows:auto auto auto; padding:16px 18px 16px; column-gap:16px; row-gap:2px; }
  .choice .num{ font-size:44px; grid-row:1 / span 2; }
  .choice .num small{ font-size:11.5px; margin-top:6px; }
  .choice .people{ display:none; }
  .choice strong{ font-size:21px; }
  .choice .d{ display:none; }
  .choice .s{ display:block; font-size:15px; line-height:1.35; }
  .choice .go{ margin-top:12px; padding:10px 16px; font-size:15px; }
  .map .city text{ font-size:28px; }
  .map .city[data-city="buk"]{ transform:translate(20px, 56px); }
  .map .extra text{ font-size:26px; }
  .map .extra text.sub{ font-size:22px; }
  .map .city text.sub{ display:none; }
  .mo .route-pin{ height:420vh; height:420svh; }
  .mo .stop-text{ padding:12px 16px 16px; }
  .mo .stop-text h3{ font-size:26px; }
  .mo .sday{ margin-top:6px; }
  .mo .sday b{ font-size:17px; }
  .mo .sday .where{ font-size:14.5px; }
  .mo .sday li{ font-size:12.5px; padding:2px 9px; }
}
@media (max-height: 700px) and (max-width: 980px){ .mo .map{ max-height:26svh; } }
@media (prefers-reduced-motion: reduce){
  .hs, .hs svg{ animation:none !important; }
}
"""
