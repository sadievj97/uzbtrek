"""Builds the five pages of the Uzbekistan Trek site. Run from the repository root:

    python3 shared/build.py                    writes index.html, big-group.html, small-group.html, founder.html, contact.html
    python3 shared/build.py --preview DIR      also writes claude.ai preview copies to DIR (index.html without html/head/body)

Text comes from shared/content.py, photo captions from shared/photos.json. The pages are generated: edit the sources, not the HTML.
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))     # shared/: text, photo catalog and the code that builds the pages
SITE_ROOT = os.path.abspath(os.path.join(HERE, ".."))  # the repository root, which GitHub Pages serves
sys.path.insert(0, HERE)
from content import *          # noqa: F401,F403
from forms_html import big_group_form, small_group_form, ambassador_form
import logos
import motion_parts as MP

PH_BASE = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8"))
PH = PH_BASE
import content as CONTENT_EN
import content_uz as CONTENT_UZ
# language: (content module, folder for its pages). The Uzbek pages live in uz/ and use the same img/, assets/ and files/.
LANGS = {"en": (CONTENT_EN, ""), "uz": (CONTENT_UZ, "uz")}
SITE_URL = "https://uzbekistantrek.com/"
CURRENT_PAGE = "index.html"   # set by main() for the page being built


def set_lang(lang):
    """Points every text constant (SITE, NAV, UI, FORMS, ...) at the language's content module, and the photo captions at its PHOTO_TEXT."""
    global ROOT, PH
    mod, folder = LANGS[lang]
    g = globals()
    for k, v in vars(mod).items():
        if k.isupper():
            g[k] = v
    ROOT = "../" if folder else ""
    PH = {k: (dict(v, caption=PHOTO_TEXT[k][0], alt=PHOTO_TEXT[k][1]) if k in PHOTO_TEXT else v) for k, v in PH_BASE.items()}

NAVY, NAVY_DEEP, YELLOW = "#1C3166", "#13234B", "#FBB617"
ROOT = ""   # img/ and assets/ sit next to the pages in both outputs

CSS = r"""
/* Layout: the trek decks on the web. Yellow and navy bands, white polaroids, a dark tiled itinerary. */
:root{
  --navy:#1C3166; --navy-deep:#13234B; --yellow:#FBB617; --yellow-soft:#FFF3CF; --sky:#BFE0E8; --red:#C2272D;
  --white:#FFFFFF; --paper:#F6F7FA; --muted:#4E5A7B; --line:#E3E0D5;
  --sans:"Archivo","Tahoma","Verdana",system-ui,-apple-system,sans-serif;
  --script:"Kaushan Script","Brush Script MT","Segoe Script",cursive;
  color-scheme:light;
}
*,*::before,*::after{ box-sizing:border-box; }
/* Moving between pages, or between EN and UZ, cross-fades instead of jumping. Browsers without cross-document view
   transitions (Firefox for now) switch pages as before. Off for visitors who ask for reduced motion. */
@media (prefers-reduced-motion: no-preference){
  @view-transition{ navigation:auto; }
  ::view-transition-old(root), ::view-transition-new(root){ animation-duration:.38s; animation-timing-function:cubic-bezier(.4,0,.2,1); }
  ::view-transition-group(site-head){ animation-duration:.38s; }
  .head{ view-transition-name:site-head; }   /* the header stays in place while the page under it changes */
}
html{ background:var(--white); scroll-behavior:smooth; scroll-padding-top:84px; }
body{ margin:0; background:var(--white); color:var(--navy); font-family:var(--sans); font-size:17px; line-height:1.6; -webkit-font-smoothing:antialiased; }
body::before{ content:""; position:fixed; inset:0 0 auto; height:env(safe-area-inset-top,0px); z-index:40; background:var(--white); }
img{ max-width:100%; display:block; }
a{ color:var(--navy); text-underline-offset:3px; }
:focus-visible{ outline:3px solid var(--red); outline-offset:3px; border-radius:4px; }
h1,h2,h3{ font-family:var(--sans); margin:0; line-height:1.08; text-wrap:balance; }
h1,h2{ font-weight:850; font-stretch:108%; text-transform:uppercase; letter-spacing:.005em; }
h2{ font-size:clamp(30px, 4.4vw, 48px); }
h3{ font-weight:750; font-size:20px; }
p{ margin:0; }
.wrap{ position:relative; max-width:1180px; margin:0 auto; padding-left:max(16px, env(safe-area-inset-left,0px)); padding-right:max(16px, env(safe-area-inset-right,0px)); }
.sec{ position:relative; padding-block:clamp(60px, 8vw, 104px); }
.lede{ font-size:clamp(17px, 1.6vw, 19px); max-width:62ch; margin-top:16px; }
.muted{ color:var(--muted); }

.btn{ display:inline-flex; align-items:center; justify-content:center; min-height:50px; padding:12px 24px; border-radius:999px; font-family:var(--sans); font-weight:750; font-size:16px; text-decoration:none; border:2px solid transparent; cursor:pointer; text-align:center; }
.btn-navy{ background-color:var(--navy); color:var(--white); border-color:var(--navy); }
.btn-yellow{ background-color:var(--yellow); color:var(--navy-deep); --sw:var(--white); }
.btn-line{ border-color:var(--navy); color:var(--navy); background-color:transparent; --sw:var(--navy); --swf:var(--white); }
.btn-row{ display:flex; flex-wrap:wrap; gap:12px; margin-top:28px; }

/* Header */
.head{ position:sticky; top:env(safe-area-inset-top,0px); z-index:30; background:var(--white); border-bottom:3px solid var(--yellow); }
.head .wrap{ display:flex; align-items:center; justify-content:space-between; gap:16px; min-height:72px; }
.logo{ display:flex; align-items:center; text-decoration:none; flex:none; }
.logo svg{ height:40px; width:auto; display:block; }
.nav{ display:flex; align-items:center; gap:22px; }
.nav > a{ text-decoration:none; font-weight:650; font-size:15px; color:var(--navy); padding:6px 0; border-bottom:3px solid transparent; }
.nav > a:hover, .nav > a[aria-current]{ border-bottom-color:var(--yellow); }
.nav .btn{ border-bottom:0; padding:10px 18px; min-height:44px; font-size:15px; color:var(--white); }
/* EN / UZ: the current language on navy, the other one a link to the same page in it */
.nav .lang{ display:inline-flex; align-items:stretch; border:2px solid var(--navy); border-radius:999px; overflow:hidden; font-size:13px; font-weight:800; letter-spacing:.06em; line-height:1.2; }
.nav .lang a, .nav .lang .on{ padding:6px 10px; text-decoration:none; }
.nav .lang .on{ background-color:var(--navy); color:var(--white); }
.nav .lang a{ color:var(--navy); }
.nav .lang a:hover, .nav .lang a:focus-visible{ background-color:var(--yellow-soft); }
.menu-btn{ display:none; appearance:none; border:2px solid var(--navy); background-color:var(--white); color:var(--navy); --sw:var(--navy); --swf:var(--white); border-radius:999px; min-height:44px; padding:0 16px; font:inherit; font-weight:700; cursor:pointer; }

/* Vertical side label, as on the decks */
.side{ position:absolute; top:44px; bottom:44px; right:max(14px, env(safe-area-inset-right,0px)); display:flex; flex-direction:column; align-items:center; gap:16px; writing-mode:vertical-rl; font-size:11.5px; letter-spacing:.42em; font-weight:600; pointer-events:none; }
.side::before, .side::after{ content:""; flex:1; width:1px; background:currentColor; opacity:.7; }
.side.light{ color:var(--white); }

/* Home hero: the ambassador program. A yellow band with the khatam watermark (MOTION_CSS), text left, three polaroids right */
.home-hero .split{ grid-template-columns:minmax(0,1.12fr) minmax(0,.88fr); }
.home-hero .wrap{ padding-block:clamp(44px, 6vw, 88px); }
.page-hero.home-hero h1{ font-size:clamp(36px, 5.6vw, 72px); line-height:.95; }   /* the longest word must fit the text column */
/* "Uzbekistan Trek" in the title: white letters, navy outline and a hard navy shadow. paint-order keeps the outline
   outside the letters, so the white stays full width (Chrome 123+, Safari 11+, Firefox 60+). */
.home-hero h1 .sticker{ color:var(--white); -webkit-text-stroke:.07em var(--navy); paint-order:stroke fill; text-shadow:.06em .06em 0 var(--navy); }
.home-hero .lede{ max-width:54ch; margin-top:22px; }
.hero-pols.h{ min-height:530px; }
.hero-pols.h .pol{ width:min(268px, 48%); }
.hero-pols.h .pol:nth-child(1){ left:0; top:0; --r:-4deg; }
.hero-pols.h .pol:nth-child(2){ left:auto; right:0; top:30px; --r:3.5deg; }
.hero-pols.h .pol:nth-child(3){ left:25%; top:auto; bottom:0; --r:-1.5deg; }
.choices{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:22px; max-width:1000px; margin:0 auto; }
.choice{ display:grid; grid-template-columns:auto 1fr; grid-template-rows:auto auto 1fr auto; column-gap:22px; row-gap:6px; padding:26px 28px; border-radius:20px; background:var(--yellow); color:var(--navy-deep); text-decoration:none; box-shadow:0 14px 34px rgba(10,20,50,.38); transition:transform .18s ease, box-shadow .18s ease; min-height:230px; }
.choice.on-white{ background:var(--white); box-shadow:0 12px 30px rgba(19,35,75,.16); }
.choice:hover{ transform:translateY(-4px); box-shadow:0 20px 40px rgba(10,20,50,.45); }
.choice:focus-visible{ outline:4px solid var(--white); outline-offset:4px; }
.choice.on-white:focus-visible{ outline-color:var(--navy); }
.choice .num{ grid-row:1 / span 3; font-weight:900; font-stretch:112%; font-size:clamp(52px, 6vw, 72px); line-height:.9; letter-spacing:-.02em; }
.choice .num small{ display:block; font-size:15px; font-weight:700; letter-spacing:.04em; margin-top:8px; text-transform:uppercase; }
.choice .people{ height:34px; width:auto; margin-bottom:2px; }
.choice strong{ font-weight:850; font-stretch:108%; font-size:clamp(22px, 2.4vw, 28px); text-transform:uppercase; line-height:1.05; }
.choice span.d{ font-size:16px; line-height:1.45; }
.choice .go{ grid-column:1 / -1; margin-top:16px; display:flex; align-items:center; justify-content:space-between; gap:12px; background-color:var(--navy-deep); color:var(--white); border:2px solid var(--navy-deep); border-radius:999px; padding:10px 18px; font-weight:750; font-size:16px; --sw:var(--white); --swf:var(--navy-deep); }
.choice.on-white .go{ --sw:var(--yellow); }
.choice .go i{ font-style:normal; font-size:20px; line-height:1; display:inline-block; transition:transform .55s cubic-bezier(.4,0,.2,1); }
.choice:hover .go i, .choice:focus-visible .go i{ transform:translateX(6px); }
.choices.small .choice{ min-height:0; }

/* Bands */
.band-yellow{ background:var(--yellow); }
.band-navy{ background:var(--navy-deep); color:var(--white); }
.band-navy h2, .band-navy h3{ color:var(--white); }
.band-sky{ background:var(--sky); }
.band-paper{ background:var(--paper); }

/* Text + polaroids */
.split{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.05fr); gap:clamp(28px, 5vw, 64px); align-items:center; }
.diam{ list-style:none; padding:0; margin:22px 0 0; display:grid; gap:12px; }
.diam li{ position:relative; padding-left:28px; font-size:18px; line-height:1.5; }
.diam li::before{ content:""; position:absolute; left:3px; top:.42em; width:12px; height:12px; background:var(--navy); transform:rotate(45deg); }
.band-navy .diam li::before, .itin .diam li::before{ background:var(--yellow); }
.diam.x li::before{ background:transparent; border:2px solid var(--red); width:11px; height:11px; }
.red-script{ font-family:var(--script); color:var(--red); font-size:clamp(24px, 3vw, 32px); margin-top:26px; display:block; }

.pol{ margin:0; background:var(--white); padding:10px 10px 0; box-shadow:0 12px 26px rgba(19,35,75,.22); transform:rotate(var(--r,0deg)); max-width:100%; }
.pol .ph{ aspect-ratio:var(--ar, 4/3); overflow:hidden; background:#DCE2EE; max-width:100%; }
.pol img{ width:100%; height:100%; object-fit:cover; }
.pol figcaption{ padding:12px 8px 16px; text-align:center; font-weight:800; font-size:13.5px; line-height:1.35; text-transform:uppercase; letter-spacing:.03em; color:var(--navy); }
.pol figcaption small{ display:block; margin-top:4px; font-weight:600; font-size:12px; color:var(--muted); letter-spacing:.06em; }
.pols{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:26px 22px; align-items:start; }
.pol.q figcaption{ text-transform:none; font-weight:700; font-size:14.5px; letter-spacing:0; line-height:1.4; }
.pol.q figcaption small{ text-transform:uppercase; }
.pols .pol:nth-child(odd){ --r:-2.5deg; }
.pols .pol:nth-child(even){ --r:2deg; margin-top:24px; }
.collage{ display:grid; grid-template-columns:repeat(5, minmax(0,1fr)); gap:28px 22px; margin-top:40px; align-items:start; }
.collage .pol:nth-child(3n+1){ --r:-3deg; }
.collage .pol:nth-child(3n+2){ --r:2.5deg; margin-top:18px; }
.collage .pol:nth-child(3n){ --r:-1deg; }
.moments-title{ font-family:var(--script); color:var(--yellow); text-shadow:2px 2px 0 var(--navy), -1px -1px 0 var(--navy), 1px -1px 0 var(--navy), -1px 1px 0 var(--navy); font-size:clamp(40px, 6vw, 72px); line-height:1.1; text-align:center; transform:rotate(-2deg); font-weight:400; text-transform:none; }

/* Itinerary (route scene styles are in MOTION_CSS) */
.tailor{ margin-top:44px; background:var(--yellow); color:var(--navy-deep); border-radius:18px; padding:clamp(22px, 3vw, 32px); display:grid; grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr); gap:20px 36px; align-items:center; }
.tailor h3{ font-size:clamp(24px, 2.8vw, 32px); font-weight:850; font-stretch:108%; text-transform:uppercase; }
.tailor .diam{ margin:0; grid-template-columns:repeat(2, minmax(0,1fr)); gap:10px 22px; }
.tailor .diam li{ font-size:17px; font-weight:600; }
.tailor .diam li::before{ background:var(--navy); }
.tent{ margin-top:22px; font-style:italic; color:var(--yellow); font-size:15.5px; max-width:80ch; }

/* Included and not included */
.inc-grid{ display:grid; grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr); align-items:stretch; }
.inc-photo{ position:relative; min-height:460px; background-color:var(--navy-deep); background-position:center; background-size:cover; display:flex; align-items:center; justify-content:center; padding:40px; }
.inc-photo .pol{ width:min(340px, 100%); --r:-2deg; }
.inc-text{ background:var(--yellow); padding:clamp(40px, 6vw, 72px) clamp(24px, 5vw, 64px); position:relative; display:grid; gap:34px; }
.inc-text h2{ font-size:clamp(26px, 3.4vw, 38px); }
.inc-cols{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:28px; }
.inc-cols .diam{ margin-top:14px; }
.inc-cols .diam li{ font-size:16.5px; }

/* Payment */
.tranches{ list-style:none; margin:46px 0 0; padding:0; display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:22px; counter-reset:t; }
.tranches li{ position:relative; background:var(--white); border:2px solid var(--navy); border-radius:16px; padding:34px 14px 18px; text-align:center;
  box-shadow:4px 5px 0 0 rgba(19,35,75,.16); display:grid; gap:6px; align-content:start; }
.tranches li:last-child{ background:var(--yellow-soft); }
.tranches .tn{ position:absolute; top:-26px; left:50%; width:50px; height:50px; margin-left:-25px; display:grid; place-items:center; isolation:isolate;
  font-weight:900; font-stretch:110%; font-size:20px; color:var(--navy-deep); }
.tranches .tn svg{ position:absolute; inset:0; width:100%; height:100%; z-index:-1; overflow:visible; }
.tranches .tn path{ fill:var(--yellow); stroke:var(--navy); stroke-width:2.2; stroke-linejoin:round; }
.tranches .tn i{ font-style:normal; }
.tranches li:not(:last-child)::after{ content:""; position:absolute; right:-17px; top:50%; width:10px; height:10px; margin-top:-5px;
  border-top:3px solid var(--navy); border-right:3px solid var(--navy); transform:rotate(45deg); }
.tranches b{ display:block; font-size:18px; font-weight:850; line-height:1.2; }
.tranches span.d{ font-size:14.5px; color:var(--muted); line-height:1.4; }
.pay-note{ margin-top:14px; font-size:15.5px; color:var(--muted); }

/* Founder teaser */
.letter{ background:var(--white); color:var(--navy); padding:clamp(24px, 3vw, 36px); border-radius:6px; box-shadow:0 18px 40px rgba(0,0,0,.28); position:relative; }
.letter p{ font-size:clamp(17px, 1.6vw, 19px); line-height:1.65; }
.sig{ display:block; margin-top:18px; font-family:var(--script); font-size:clamp(30px, 3.4vw, 40px); color:var(--navy); line-height:1.1; }
.sig small{ display:block; font-family:var(--sans); font-size:13px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-top:14px; }

/* FAQ */
.faq-sec{ background-color:var(--navy-deep); background-position:center; background-size:cover; }
.faq-box{ background:var(--white); border:8px solid var(--yellow); padding:clamp(22px, 4vw, 40px); max-width:920px; margin:0 auto; }
.faq-box h2{ font-size:clamp(26px, 3.4vw, 36px); margin-bottom:10px; }
.faq-box details{ border-bottom:1px solid var(--line); }
.faq-box details:last-of-type{ border-bottom:0; }
.faq-box summary{ cursor:pointer; list-style:none; padding:18px 44px 18px 0; position:relative; font-weight:800; font-size:18px; }
.faq-box summary::-webkit-details-marker{ display:none; }
.faq-box summary::after{ content:"+"; position:absolute; right:4px; top:50%; transform:translateY(-50%); width:30px; height:30px; display:grid; place-items:center; border-radius:50%; background:var(--yellow); font-weight:900; font-size:20px; line-height:1; }
.faq-box details[open] summary::after{ content:"\2212"; }
.faq-box summary::after{ transition:transform .5s cubic-bezier(.4,0,.2,1); }
.faq-box details[open]:not(.closing) summary::after{ transform:translateY(-50%) rotate(180deg); }
.faq-box details.closing summary::after{ content:"+"; }
.faq-box .a{ padding:0 0 20px; max-width:68ch; color:var(--muted); font-size:17px; }
.faq-box .a p + p{ margin-top:10px; }
.faq-box .a a{ color:var(--navy); font-weight:700; }

/* Inner page hero */
.page-hero{ background:var(--yellow); position:relative; overflow:hidden; }
.page-hero .wrap{ padding-block:clamp(48px, 7vw, 88px); }
.kicker{ display:inline-block; background:var(--navy); color:var(--white); font-weight:800; font-size:14px; letter-spacing:.06em; text-transform:uppercase; padding:6px 14px; border-radius:999px; margin-bottom:18px; }
.page-hero h1{ font-size:clamp(40px, 6.4vw, 76px); line-height:.98; }
.hero-pols{ position:relative; min-height:540px; }
.hero-pols .pol{ position:absolute; width:min(260px, 50%); }
.hero-pols .pol:nth-child(1){ left:0; top:6px; --r:-5deg; }
.hero-pols .pol:nth-child(2){ right:0; top:22px; --r:4deg; }
.hero-pols .pol:nth-child(3){ left:26%; bottom:0; --r:-1deg; z-index:1; }
.hero-pols.f .pol:nth-child(1){ width:min(300px, 56%); left:2%; top:0; --r:-3deg; }
.hero-pols.f .pol:nth-child(2){ top:auto; bottom:0; right:0; width:min(250px, 46%); --r:4deg; }

.cards3{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:22px; margin-top:34px; }
.card{ background:var(--white); border:2px solid var(--navy); border-top:10px solid var(--yellow); border-radius:14px; padding:24px; }
.card h3{ margin-bottom:8px; }
.card p{ color:var(--muted); font-size:16px; }
.who-grid{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:22px; margin-top:34px; }
.who{ background:var(--white); border-radius:16px; padding:26px 28px; color:var(--navy); }
.who h3{ text-transform:uppercase; font-stretch:108%; font-weight:850; margin-bottom:12px; }
.who.us{ background:var(--yellow); }
.who ul{ margin:0; padding-left:20px; display:grid; gap:8px; }
.timeline{ list-style:none; padding:0; margin:40px 0 0; display:grid; grid-template-columns:repeat(7, minmax(0,1fr)); gap:14px; position:relative; }
.timeline::before{ content:""; position:absolute; left:20px; right:20px; top:19px; height:4px; background:var(--navy); }
.timeline li{ position:relative; min-width:0; counter-increment:tl; }
.timeline{ counter-reset:tl; }
.timeline li::before{ content:counter(tl); position:relative; display:grid; place-items:center; width:40px; height:40px; font-weight:900; color:var(--navy-deep); background:var(--yellow); clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%); margin-bottom:12px; }
.timeline b{ display:block; font-size:14px; letter-spacing:.04em; text-transform:uppercase; color:var(--muted); font-weight:750; }
.timeline span{ display:block; font-weight:750; font-size:16px; line-height:1.35; margin-top:2px; }
.tl-note{ margin-top:22px; color:var(--muted); font-size:16px; }
.table-wrap{ position:relative; overflow-x:auto; margin-top:30px; border:2px solid var(--navy); border-radius:16px; background:var(--white); }
table{ border-collapse:collapse; width:100%; min-width:680px; }
th, td{ text-align:left; padding:16px 18px; border-bottom:1px solid var(--line); vertical-align:top; font-size:16px; }
th{ background:var(--navy); color:var(--white); font-weight:750; font-size:14.5px; letter-spacing:.03em; text-transform:uppercase; }
tr:last-child td{ border-bottom:0; }
td b{ display:block; font-weight:850; }
.pill{ display:inline-block; background:var(--yellow-soft); border:1px solid var(--yellow); color:#6E4E00; font-weight:700; font-size:13px; padding:3px 10px; border-radius:999px; white-space:nowrap; }
.mini{ appearance:none; border:2px solid var(--navy); background-color:var(--white); color:var(--navy); --sw:var(--navy); --swf:var(--white); border-radius:999px; padding:7px 14px; font:inherit; font-weight:700; font-size:14px; cursor:pointer; white-space:nowrap; }
.nw{ white-space:nowrap; }

/* Start a trek at your university (home): five steps on a dashed route, where to look, tips, sample texts */
.steps{ list-style:none; margin:52px 0 0; padding:0; display:grid; grid-template-columns:repeat(5, minmax(0,1fr)); gap:26px; position:relative; }
.steps::before{ content:""; position:absolute; left:28px; right:calc((100% - 104px) / 5 - 28px); top:27px; border-top:3px dashed var(--navy); opacity:.5; }
.steps li{ position:relative; min-width:0; display:grid; gap:8px; align-content:start; }
.steps .sn{ position:relative; width:56px; height:56px; display:grid; place-items:center; isolation:isolate; margin-bottom:6px;
  font-weight:900; font-stretch:110%; font-size:22px; color:var(--navy-deep); }
.steps .sn::before{ content:""; position:absolute; inset:4px; border-radius:50%; background:var(--white); z-index:-2; }
.steps .sn svg{ position:absolute; inset:0; width:100%; height:100%; z-index:-1; overflow:visible; }
.steps .sn path{ fill:var(--yellow); stroke:var(--navy); stroke-width:2.2; stroke-linejoin:round; }
.steps .sn i{ font-style:normal; }
.steps li:last-child .sn{ color:var(--yellow); }
.steps li:last-child .sn path{ fill:var(--navy); }
.steps b{ font-size:18px; font-weight:850; font-stretch:106%; text-transform:uppercase; line-height:1.15; }
.steps p{ font-size:15.5px; line-height:1.5; color:var(--muted); }
.go-link{ justify-self:start; font-weight:750; font-size:15px; text-decoration:none; border-bottom:2px solid var(--yellow); line-height:1.3; }
.go-link::after{ content:" \203A"; }
.go-link:hover{ border-bottom-color:var(--navy); }
.start-grid{ display:grid; grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr); gap:22px; margin-top:52px; }
.start-box{ border-radius:16px; padding:24px 26px; }
.start-box h3{ text-transform:uppercase; font-stretch:108%; font-weight:850; margin-bottom:14px; }
.start-box.where{ background:var(--paper); }
.start-box.tips{ background:var(--yellow); color:var(--navy-deep); }
.start-box.tips .diam{ margin:0; gap:10px; }
.start-box.tips .diam li{ font-size:16px; }
.chips{ display:flex; flex-wrap:wrap; gap:10px; list-style:none; margin:0; padding:0; }
.chips li{ background:var(--white); border:2px solid var(--navy); border-radius:999px; padding:7px 14px; font-weight:700; font-size:15px; line-height:1.3; }
.samples-title{ margin-top:52px; font-size:clamp(22px, 2.6vw, 28px); font-weight:850; font-stretch:108%; text-transform:uppercase; }
.samples{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:22px; margin-top:18px; align-items:start; }
.sample{ background:var(--white); border:2px solid var(--navy); border-top:10px solid var(--yellow); border-radius:14px; padding:20px 22px; scroll-margin-top:100px; min-width:0; }
/* Where subgrid works, each block spans three rows of the grid (title, button, bottom line), so two blocks side by side
   are the same height with their buttons and bottom lines at the same level. Elsewhere the blocks simply stack. */
@supports (grid-template-rows:subgrid){
  .samples{ row-gap:0; align-items:stretch; }
  .sample{ display:grid; grid-row:span 3; grid-template-rows:subgrid; row-gap:0; align-content:start; margin-bottom:22px; }
}
.sample .copy-row{ margin-top:14px; }
a.mini{ display:inline-block; text-decoration:none; }
.sample-more{ margin-top:14px; border-top:1px solid var(--line); }
.sample-dl{ display:flex; align-items:center; gap:10px; padding:12px 0 2px; font-weight:750; font-size:15.5px; text-decoration:none; color:var(--navy); }
.sample-dl::before{ content:"\2193"; display:grid; place-items:center; width:24px; height:24px; flex:none; border-radius:50%; background:var(--yellow); font-weight:900; }
.sample-dl:hover{ text-decoration:underline; }
.sample h4{ margin:8px 0 0; font-size:19px; font-weight:800; line-height:1.25; }
.sample .when{ color:var(--muted); font-size:15px; margin-top:2px; }
.copy-row{ display:flex; flex-wrap:wrap; align-items:center; gap:6px 12px; }
.copy-status{ font-size:14px; font-weight:700; color:#157A3A; }
.copy-status:empty{ display:none; }
.sample details{ margin-top:14px; border-top:1px solid var(--line); }
.sample summary{ cursor:pointer; list-style:none; padding:12px 0 2px; font-weight:750; font-size:15.5px; display:flex; align-items:center; gap:10px; }
.sample summary::-webkit-details-marker{ display:none; }
.sample summary::before{ content:"+"; display:grid; place-items:center; width:24px; height:24px; flex:none; border-radius:50%; background:var(--yellow); font-weight:900; }
.sample details[open] summary::before{ content:"\2212"; }
.sample summary::before{ transition:transform .5s cubic-bezier(.4,0,.2,1); }
.sample details[open]:not(.closing) summary::before{ transform:rotate(180deg); }
.sample details.closing summary::before{ content:"+"; }
.sample-text{ white-space:pre-line; overflow-wrap:anywhere; margin-top:10px; padding:16px 18px; border-radius:10px; background:var(--paper); font-size:15.5px; line-height:1.55; color:var(--navy); }
.sr{ position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
.opt-grid{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:26px; margin-top:36px; }
.opt{ background:var(--white); border-radius:20px; overflow:hidden; box-shadow:0 12px 30px rgba(19,35,75,.14); display:flex; flex-direction:column; }
.opt .ph{ aspect-ratio:16/9; overflow:hidden; }
.opt .ph img{ width:100%; height:100%; object-fit:cover; }
.opt .body{ padding:26px 28px 28px; display:flex; flex-direction:column; gap:12px; flex:1; }
.opt h3{ text-transform:uppercase; font-stretch:108%; font-weight:850; font-size:24px; }
.opt .tag{ align-self:flex-start; background:var(--yellow); font-weight:800; font-size:13.5px; padding:4px 12px; border-radius:999px; letter-spacing:.03em; text-transform:uppercase; }
.opt .btn{ align-self:flex-start; margin-top:auto; }
.opt .diam{ margin-top:4px; }
.opt .diam li{ font-size:16.5px; }

/* Forms */
.form-wrap{ display:grid; grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr); gap:clamp(28px, 5vw, 56px); align-items:start; }
.tform{ background:var(--white); color:var(--navy); border-radius:20px; padding:clamp(22px, 3vw, 32px); display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:16px 18px; box-shadow:0 16px 40px rgba(10,20,50,.25); }
.tf{ display:grid; gap:6px; min-width:0; }
.tf.full, fieldset.tf{ grid-column:1 / -1; }
.tf label, .tf legend{ font-weight:750; font-size:15px; }
.tf input, .tf select, .tf textarea{ font:inherit; font-size:16px; color:var(--navy); background:var(--white); border:2px solid #C9CFDD; border-radius:10px; padding:10px 12px; min-height:48px; width:100%; }
.tf textarea{ min-height:110px; resize:vertical; }
.tf input:focus, .tf select:focus, .tf textarea:focus{ outline:none; border-color:var(--navy); box-shadow:0 0 0 4px rgba(251,182,23,.55); }
.tf [aria-invalid="true"]{ border-color:var(--red); }
fieldset.tf{ border:0; margin:0; padding:0; display:grid; gap:8px; }
.tchips{ display:flex; flex-wrap:wrap; gap:10px; }
.tchip{ display:flex; align-items:center; gap:8px; border:2px solid #C9CFDD; border-radius:999px; padding:8px 14px; cursor:pointer; font-size:15px; font-weight:600; }
.tchip input{ width:18px; height:18px; min-height:0; margin:0; accent-color:var(--navy); }
.tchip:has(input:checked){ border-color:var(--navy); background:var(--yellow-soft); }
.tform-hp{ position:absolute; left:-9999px; width:1px; height:1px; overflow:hidden; }
.tform-foot{ grid-column:1 / -1; display:flex; flex-wrap:wrap; gap:14px; align-items:center; justify-content:space-between; }
.tform-foot small{ color:var(--muted); font-size:14px; max-width:42ch; }
.tform-msg[hidden]{ display:none; }
.tform-msg{ grid-column:1 / -1; padding:14px 16px; border-radius:12px; font-size:15.5px; font-weight:600; display:grid; gap:10px; }
.tform-msg.ok{ background:#E2F2EF; color:#0F5550; }
.tform-msg.err{ background:#F8E1E3; color:#842129; }
.tform-msg.sent{ display:flex; align-items:center; gap:10px; background:#E7F6EC; color:#157A3A; font-weight:750; font-size:16.5px; }
.tform-msg.sent svg{ width:22px; height:22px; flex:none; border-radius:50%; background:#1E9E4A; padding:3px; }
.tform-msg.sent svg path{ fill:none; stroke:#FFFFFF; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round; }
.tform-msg a{ color:inherit; }
.tform-copy{ width:100%; font:inherit; font-size:14px; font-weight:500; border:1px solid #9CC9C3; border-radius:8px; padding:10px; background:var(--white); color:var(--navy); resize:vertical; }
.tform-actions{ display:flex; flex-wrap:wrap; gap:10px; }
.tform-copybtn, .tform-tg{ display:inline-flex; align-items:center; min-height:44px; padding:8px 16px; border-radius:999px; font:inherit; font-weight:750; font-size:15px; cursor:pointer; text-decoration:none; }
.tform-copybtn{ border:2px solid #0F5550; background-color:transparent; color:#0F5550; --sw:#0F5550; --swf:var(--white); }
.tform-tg{ background-color:#229ED9; color:var(--white) !important; border:2px solid #229ED9; --sw:var(--navy-deep); --swf:var(--white); }
.tform-copied{ font-weight:600; font-size:14.5px; }
.tform-mail{ display:inline-flex; align-items:center; min-height:44px; padding:0 6px; font-weight:750; font-size:15px; text-decoration:underline; text-underline-offset:3px; }
.tform-alt{ grid-column:1 / -1; font-size:14.5px; color:var(--muted); margin:0; }
.tform-alt a{ font-weight:700; }

/* Founder page */
.portrait-big{ --ar:3/4; }
.facts{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:14px 22px; margin-top:26px; max-width:640px; }
.facts div{ border-left:4px solid var(--navy); padding-left:12px; font-size:16px; line-height:1.4; }
.facts b{ display:block; font-weight:850; }
.story{ max-width:760px; }
.story h2{ font-size:clamp(22px, 2.8vw, 30px); margin-top:46px; }
.story h2:first-child{ margin-top:0; }
.story p{ margin-top:14px; font-size:18.5px; line-height:1.7; }
.story .sig{ margin-top:30px; }
.story-grid{ display:grid; grid-template-columns:minmax(0,1fr) 340px; gap:clamp(28px, 5vw, 64px); align-items:start; }
.story-side{ position:sticky; top:96px; display:grid; gap:30px; }
.story-side .pol:nth-child(odd){ --r:-2deg; }
.story-side .pol:nth-child(even){ --r:2.5deg; }
.tl{ list-style:none; padding:0; margin:36px 0 0; display:grid; grid-template-columns:repeat(6, minmax(0,1fr)); gap:18px; position:relative; }
.tl::before{ content:""; position:absolute; left:12px; right:calc((100% - 90px) / 6 - 12px); top:9px; height:3px; background:var(--yellow); }
.tl li{ position:relative; padding-top:34px; min-width:0; }
.tl li::before{ content:""; position:absolute; left:2px; top:0; width:20px; height:20px; background:var(--yellow); transform:rotate(45deg); }
.tl b{ display:block; color:var(--yellow); font-weight:850; font-size:15px; letter-spacing:.04em; text-transform:uppercase; }
.tl span{ display:block; margin-top:4px; font-size:16px; line-height:1.4; }
.tl strong{ display:block; font-weight:900; font-stretch:110%; font-size:34px; line-height:1.05; color:var(--white); margin-top:6px; }
.quotes2{ display:grid; gap:34px; }
.quote-note{ margin-top:10px; font-size:14.5px; font-style:italic; color:var(--navy-deep); }
.quotes2 + .quote-note{ margin-top:22px; }
.bigquote{ margin:0; font-weight:650; font-size:clamp(19px, 2.1vw, 23px); line-height:1.5; max-width:62ch; }
.bigquote::before{ content:"\201C"; display:block; font-family:var(--script); font-size:84px; line-height:.6; color:var(--navy); margin-bottom:4px; }
.cite{ margin-top:14px; font-weight:800; text-transform:uppercase; letter-spacing:.04em; font-size:14.5px; }
.areas-grid{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:26px; margin-top:30px; }
.areas-col{ background:var(--paper); border-radius:16px; padding:24px 26px; }
.areas-col h3{ text-transform:uppercase; font-stretch:108%; font-weight:850; margin-bottom:14px; }
.areas-col ul{ list-style:none; margin:0; padding:0; display:grid; gap:10px; }
/* In the news (home page) */
.press-head{ display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.3fr); gap:12px 48px; align-items:end; }
.press-head .lede{ margin-top:0; }
.press-note{ display:block; margin-top:6px; font-size:15px; color:rgba(255,255,255,.72); }
.ticker{ position:relative; overflow:hidden; margin-top:38px; padding:16px 0; border-block:1px solid rgba(255,255,255,.2);
  -webkit-mask-image:linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent); mask-image:linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent); }
.ticker-track{ display:flex; width:max-content; animation:tick 52s linear infinite; }
.ticker:hover .ticker-track{ animation-play-state:paused; }
.ticker .tk{ display:flex; }
.ticker .tk span{ display:inline-flex; align-items:center; gap:22px; padding-right:22px; white-space:nowrap; font-weight:850; font-stretch:110%;
  text-transform:uppercase; letter-spacing:.03em; font-size:clamp(17px, 2vw, 24px); color:var(--white); }
.ticker svg{ width:16px; height:16px; flex:none; }
.ticker svg path{ fill:var(--yellow); }
@keyframes tick{ to{ transform:translateX(-50%); } }
.press-years{ display:grid; gap:46px; margin-top:46px; }
.press-year{ display:grid; grid-template-columns:220px minmax(0,1fr); gap:18px 36px; align-items:start; }
.py-label{ position:sticky; top:96px; }
.py-label b{ display:block; font-weight:900; font-stretch:115%; font-size:clamp(48px, 5.4vw, 72px); line-height:.9; letter-spacing:-.02em; color:var(--yellow); }
.py-label span{ display:block; margin-top:10px; font-weight:700; font-size:13.5px; letter-spacing:.06em; text-transform:uppercase; color:rgba(255,255,255,.75); }
.press-grid{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:16px; }
.press-card{ position:relative; display:flex; flex-direction:column; gap:8px; min-height:172px; padding:18px 18px 16px; border-radius:16px;
  background-color:var(--white); color:var(--navy-deep); text-decoration:none; box-shadow:0 10px 24px rgba(0,0,0,.2);
  background-image:linear-gradient(var(--yellow), var(--yellow)); background-repeat:no-repeat; background-position:left center; background-size:0% 100%;
  transition:background-size .6s cubic-bezier(.4,0,.2,1), transform .45s cubic-bezier(.2,.9,.25,1), box-shadow .45s cubic-bezier(.2,.9,.25,1); }
.press-card:hover, .press-card:focus-visible{ background-size:100% 100%; transform:translateY(-4px); box-shadow:0 18px 32px rgba(0,0,0,.28); }
.pc-kind{ align-self:flex-start; display:inline-flex; align-items:center; gap:6px; padding:4px 10px 4px 8px; border-radius:999px; background:var(--yellow-soft);
  color:var(--navy-deep); font-weight:800; font-size:12px; letter-spacing:.06em; text-transform:uppercase; transition:background-color .4s ease; }
.pc-kind svg{ width:15px; height:15px; flex:none; }
.press-card:hover .pc-kind, .press-card:focus-visible .pc-kind{ background:var(--white); }
.pc-src{ font-weight:850; font-stretch:105%; font-size:19px; line-height:1.2; margin-top:4px; }
.pc-line{ font-size:15px; line-height:1.4; color:var(--muted); transition:color .4s ease; }
.press-card:hover .pc-line, .press-card:focus-visible .pc-line{ color:var(--navy-deep); }
.pc-go{ margin-top:auto; padding-top:6px; display:inline-flex; align-items:center; gap:6px; font-weight:800; font-size:13.5px; letter-spacing:.06em; text-transform:uppercase; color:var(--navy); }
.pc-go svg{ width:12px; height:12px; transition:transform .45s cubic-bezier(.2,.9,.25,1); }
.press-card:hover .pc-go svg, .press-card:focus-visible .pc-go svg{ transform:translate(3px, -3px); }
.areas-col li{ background:var(--white); border:2px solid var(--navy); border-radius:12px; padding:10px 14px; font-weight:650; font-size:16px; }

/* Who we are (home) */
.team-grid{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:22px; margin-top:34px; }
.member{ display:grid; grid-template-columns:auto minmax(0,1fr); gap:18px 24px; align-items:center; background:var(--white); border:2px solid var(--navy); border-radius:16px; padding:24px 26px; }
.avatar{ width:96px; height:96px; border-radius:50%; border:3px solid var(--navy); overflow:hidden; background:var(--yellow); display:grid; place-items:center;
  font-weight:900; font-stretch:110%; font-size:30px; letter-spacing:.02em; color:var(--navy-deep); }
.avatar img{ width:100%; height:100%; object-fit:cover; }
.role{ display:inline-block; background:var(--yellow); color:var(--navy-deep); font-weight:800; font-size:12.5px; letter-spacing:.08em; text-transform:uppercase; padding:4px 12px; border-radius:999px; }
.member h3{ font-size:24px; font-weight:800; margin-top:10px; }
.member p{ font-size:16.5px; line-height:1.5; margin-top:6px; }
.member .go-link{ display:inline-block; margin-top:12px; }
/* Contact page */
.contact-grid{ margin-top:0; }
.contact-grid .member.tg{ grid-column:1 / -1; }
.contact-grid .avatar svg{ width:42px; height:42px; fill:var(--navy-deep); }
.contact-mail{ display:flex; flex-wrap:wrap; align-items:center; gap:6px 12px; margin-top:12px; }
.contact-mail .addr{ font-weight:750; font-size:17px; overflow-wrap:anywhere; }
.tg-btn{ margin-top:14px; }
.contact-next{ display:flex; flex-wrap:wrap; gap:14px 30px; margin-top:18px; }

/* What you get (home) */
.gets{ list-style:none; margin:40px 0 0; padding:0; display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:18px; }
.get{ background:var(--navy); border:1px solid rgba(255,255,255,.14); border-radius:18px; padding:24px 22px 26px; display:grid; gap:10px; align-content:start; box-shadow:0 18px 36px rgba(0,0,0,.25); }
.get .ic{ width:54px; height:54px; border-radius:16px; background:var(--yellow); color:var(--navy-deep); display:grid; place-items:center; margin-bottom:6px; }
.get .ic svg{ width:28px; height:28px; fill:none; stroke:currentColor; stroke-width:1.9; stroke-linecap:round; stroke-linejoin:round; }
.get b{ font-size:19px; font-weight:850; font-stretch:106%; text-transform:uppercase; line-height:1.15; color:var(--white); }
.get p{ font-size:15.5px; line-height:1.5; color:#D5DCEC; }

/* Home FAQ groups and the application */
.faq-box .fq{ margin:28px 0 2px; font-size:14px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }
.faq-box h2 + .fq{ margin-top:12px; }
.apply h3{ margin-top:32px; text-transform:uppercase; font-stretch:108%; font-weight:850; }
.apply .diam{ margin-top:14px; }
.apply .diam li{ font-size:17px; }
.apply .tform{ box-shadow:0 18px 40px rgba(19,35,75,.22); }
.groups-note{ text-align:center; margin-top:22px; font-size:16px; }

/* Footer */
.foot{ background:var(--navy-deep); color:#CBD3E6; font-size:15px; }
.foot .wrap{ padding-block:44px 48px; display:grid; grid-template-columns:minmax(0,1.3fr) minmax(0,1fr); gap:28px 48px; }
.foot .logo svg{ height:38px; }
.foot nav{ display:grid; gap:8px; align-content:start; }
.foot nav a{ color:var(--white); text-decoration:none; font-weight:650; }
.foot nav a:hover{ text-decoration:underline; }
.foot p + p{ margin-top:10px; }
.contact{ margin-top:18px; display:grid; gap:6px; }
.contact b{ color:var(--white); font-weight:700; }
.contact a{ color:var(--yellow); font-weight:700; }
.contact .mail{ color:var(--white); user-select:all; font-weight:600; }

/* Buttons: on hover a fill runs across from left to right.
   Plain CSS draws the fill as a background and fades the text color. Where motion.js has added a copy of the label (.sw),
   the copy rides on the fill instead, so the text color changes exactly at the fill's edge. */
.btn, .mini, .menu-btn, .choice .go, .tform-copybtn, .tform-tg{
  background-image:linear-gradient(var(--sw, var(--yellow)), var(--sw, var(--yellow)));
  background-repeat:no-repeat; background-position:left center; background-size:0% 100%; background-origin:border-box;
  transition:background-size .6s cubic-bezier(.4,0,.2,1), color .3s ease .15s; }
.btn:not(.has-sw):hover, .btn:not(.has-sw):focus-visible, .mini:not(.has-sw):hover, .mini:not(.has-sw):focus-visible,
.menu-btn:hover, .menu-btn:focus-visible, .tform-copybtn:hover, .tform-copybtn:focus-visible, .tform-tg:hover, .tform-tg:focus-visible,
.choice:hover .go:not(.has-sw), .choice:focus-visible .go:not(.has-sw){ background-size:100% 100%; color:var(--swf, var(--navy-deep)); }
.btn.has-sw, .mini.has-sw, .choice .go.has-sw{ background-image:none; }
.mini, .choice .go{ position:relative; isolation:isolate; }
.sw{ position:absolute; inset:0; z-index:1; display:flex; align-items:center; justify-content:center; gap:inherit; padding:inherit; border-radius:inherit;
  background-color:var(--sw, var(--yellow)); color:var(--swf, var(--navy-deep)); pointer-events:none; user-select:none;
  clip-path:inset(0 100% 0 0); transition:clip-path .6s cubic-bezier(.4,0,.2,1); }
.choice .go .sw{ justify-content:space-between; }
.has-sw:hover .sw, .has-sw:focus-visible .sw, .choice:hover .has-sw .sw, .choice:focus-visible .has-sw .sw{ clip-path:inset(0); }

@media (max-width: 1100px){ .side{ display:none; } .press-grid, .gets{ grid-template-columns:repeat(2, minmax(0,1fr)); } }
@media (max-width: 980px){
  .split, .form-wrap, .story-grid, .home-hero .split{ grid-template-columns:1fr; }
  .hero-pols.h{ width:100%; max-width:600px; margin:6px auto 0; }
  .page-hero.home-hero h1{ font-size:clamp(32px, 10.2vw, 72px); }
  .story-side{ position:static; grid-template-columns:repeat(2, minmax(0,1fr)); }
  .collage{ grid-template-columns:repeat(3, minmax(0,1fr)); }
  .inc-grid{ grid-template-columns:1fr; }
  .inc-photo{ min-height:380px; }
  .cards3{ grid-template-columns:1fr; }
  .tailor{ grid-template-columns:1fr; }
  .timeline{ grid-template-columns:1fr; gap:16px; }
  .timeline::before{ left:18px; right:auto; top:20px; bottom:20px; width:4px; height:auto; }
  .timeline li{ display:grid; grid-template-columns:40px 1fr; column-gap:16px; align-items:center; }
  .timeline li::before{ margin:0; grid-row:span 2; }
  .tl{ grid-template-columns:repeat(3, minmax(0,1fr)); row-gap:30px; }
  .tl::before{ display:none; }
  .steps{ grid-template-columns:1fr; gap:22px; margin-top:40px; }
  .steps::before{ left:27px; right:auto; top:28px; bottom:28px; border-top:0; border-left:3px dashed var(--navy); }
  .steps li{ grid-template-columns:56px minmax(0,1fr); column-gap:18px; row-gap:6px; }
  .steps .sn{ grid-row:1 / span 3; margin:0; }
  .steps li > :not(.sn){ grid-column:2; }
}
/* Below these widths the header links fold into the Menu button: 1010px in English, 1080px in Uzbek (longer words). */
@media (max-width: 1010px){
  .nav{ display:none; position:absolute; top:100%; left:0; right:0; flex-direction:column; align-items:stretch; gap:0; background:var(--white); border-bottom:3px solid var(--yellow); padding:8px max(16px, env(safe-area-inset-right,0px)) 18px max(16px, env(safe-area-inset-left,0px)); }
  .nav.open{ display:flex; }
  .nav > a{ padding:12px 0; border-bottom:1px solid var(--line); }
  .nav .btn{ margin-top:14px; }
  .nav .lang{ align-self:flex-start; margin-top:12px; }
  .nav .lang a, .nav .lang .on{ padding:9px 18px; }
  .menu-btn{ display:inline-flex; align-items:center; }
}
@media (max-width: 1080px){
  :root[lang="uz"] .nav{ display:none; position:absolute; top:100%; left:0; right:0; flex-direction:column; align-items:stretch; gap:0; background:var(--white); border-bottom:3px solid var(--yellow); padding:8px max(16px, env(safe-area-inset-right,0px)) 18px max(16px, env(safe-area-inset-left,0px)); }
  :root[lang="uz"] .nav.open{ display:flex; }
  :root[lang="uz"] .nav > a{ padding:12px 0; border-bottom:1px solid var(--line); }
  :root[lang="uz"] .nav .btn{ margin-top:14px; }
  :root[lang="uz"] .nav .lang{ align-self:flex-start; margin-top:12px; }
  :root[lang="uz"] .nav .lang a, :root[lang="uz"] .nav .lang .on{ padding:9px 18px; }
  :root[lang="uz"] .menu-btn{ display:inline-flex; align-items:center; }
}
@media (max-width: 860px){
  .choices{ grid-template-columns:1fr; }
  .opt-grid, .who-grid, .areas-grid, .inc-cols, .team-grid{ grid-template-columns:1fr; }
  .start-grid, .samples{ grid-template-columns:1fr; }
}
@media (max-width: 640px){
  .logo svg{ height:32px; }
  .collage{ grid-template-columns:repeat(2, minmax(0,1fr)); gap:22px 16px; }
  .press-head{ grid-template-columns:1fr; }
  .press-year{ grid-template-columns:1fr; }
  /* on phones the month and travelers sit next to the year, centered on it (two short lines) */
  .py-label{ position:static; display:flex; align-items:center; gap:16px; }
  .py-label b{ font-size:52px; flex:none; }
  .py-label span{ margin-top:0; line-height:1.35; }
  .press-grid{ grid-template-columns:none; grid-auto-flow:column; grid-auto-columns:78%; overflow-x:auto; scroll-snap-type:x mandatory;
    margin-inline:-16px; padding:4px 16px 14px; scroll-padding-inline:16px; }
  .press-card{ scroll-snap-align:start; }
  .collage .pol:last-child:nth-child(odd){ grid-column:1 / -1; justify-self:center; width:calc(50% - 8px); }
  .tailor .diam{ grid-template-columns:1fr; }
  .tranches{ grid-template-columns:1fr; gap:40px; }
  .tranches li{ padding:32px 18px 16px; }
  .tranches li:not(:last-child)::after{ right:auto; left:50%; top:auto; bottom:-27px; margin:0 0 0 -6px; transform:rotate(135deg); }
  .tform{ grid-template-columns:1fr; }
  .hero-pols, .hero-pols.f, .hero-pols.h{ min-height:0; display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:18px; align-items:start; }
  .hero-pols .pol, .hero-pols.f .pol, .hero-pols.h .pol{ position:static; width:auto !important; }
  .hero-pols .pol:nth-child(3){ display:none; }
  .facts{ grid-template-columns:1fr; }
  .tl{ grid-template-columns:repeat(2, minmax(0,1fr)); }
  .foot .wrap{ grid-template-columns:1fr; }
  .choice{ padding:22px; min-height:0; }
  .choice .num{ font-size:52px; }
}
@media (max-width: 560px){ .gets{ grid-template-columns:1fr; } }
@media (max-width: 420px){
  .story-side{ grid-template-columns:1fr; }
  .member{ padding:20px; gap:14px 18px; }
  .avatar{ width:76px; height:76px; font-size:24px; }
  .member h3{ font-size:21px; }
}
@media (max-width: 560px){
  .pols.quotes{ grid-template-columns:1fr; gap:22px; }
  .pols.quotes .pol{ width:84%; margin-top:0; }
  .pols.quotes .pol:nth-child(even){ justify-self:end; }
}
@media (prefers-reduced-motion: reduce){ html{ scroll-behavior:auto; } *{ transition:none !important; }
  .ticker-track{ animation:none; width:auto; } .ticker .tk{ flex-wrap:wrap; justify-content:center; row-gap:10px; } .ticker .dup{ display:none; }
  .ticker{ -webkit-mask-image:none; mask-image:none; } }
"""


# ------------------------------------------------------------------ helpers
def img(key):
    return f"{ROOT}img/{PH[key]['file']}"


def pol(key, cap=None, sub=None, ar="4/3", extra_style="", cls="pol", lazy=True, drift=None):
    p = PH[key]
    if cap is None:
        # keep hyphenated names such as Tilla-Kari or Shah-i-Zinda on one line
        cap = re.sub(r"(?<![&#\w])(\w+(?:-\w+)+)", r'<span class="nw">\1</span>', p["caption"])
    if sub is None:
        sub = p["year"]
    subh = f"<small>{sub}</small>" if sub else ""
    ld = ' loading="lazy"' if lazy else ""
    fl = f' data-float="{drift}"' if drift else ""
    return (f'<figure class="{cls}" style="--ar:{ar}{extra_style}"{fl}><div class="ph"><img src="{img(key)}" alt="{p["alt"]}"{ld}></div>'
            f'<figcaption>{cap}{subh}</figcaption></figure>')


def quote_note():
    """On the Uzbek pages, a line under the quotes says they are translated from English (the owner, Nov 2026)."""
    return f'<p class="quote-note">{UI["quotes_note"]}</p>' if UI.get("quotes_note") else ""


def en_attr():
    """The sample texts stay in English on the Uzbek pages; they are marked as English for screen readers and translators."""
    return "" if LANG == "en" else ' lang="en"'


def rich(text):
    """A sample text as HTML: **bold**, __italic__ and !!bold red!! (within one line) become <strong>, <em> and a red <strong>;
    everything else is escaped. The red is an inline style, so it stays red when the copied text is pasted into an email."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"!!(.+?)!!", r'<strong style="color:#C2272D">\1</strong>', t)
    return re.sub(r"__(.+?)__", r"<em>\1</em>", t)


def faq_bg(key):
    return f"background-image:linear-gradient(rgba(19,35,75,.62), rgba(19,35,75,.82)), url('{img(key)}')"


def people(n, rows=1):
    per = -(-n // rows)
    w = per * 13 + 6
    h = rows * 18 + 16
    out = []
    k = 0
    for r in range(rows):
        for c in range(per):
            if k >= n:
                break
            x = 8 + c * 13 + (6 if r % 2 else 0)
            y = 2 + r * 16
            out.append(f'<circle cx="{x}" cy="{y+5}" r="4.4"/><path d="M{x-6} {y+21}c0-4.2 2.7-7.6 6-7.6s6 3.4 6 7.6z"/>')
            k += 1
    return f'<svg class="people" viewBox="0 0 {w+6} {h}" fill="currentColor" aria-hidden="true">{"".join(out)}</svg>'


def side(light=False):
    return f'<span class="side{" light" if light else ""}" aria-hidden="true">{SITE["side_label"]}</span>'


def diam(items, cls="diam"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def faq_block(title, items, hid):
    """items: [(question, [paragraphs])], or in groups: [(group title, [(question, [paragraphs])])]."""
    def rows(its):
        return "".join(f'<details><summary>{q}</summary><div class="a">{"".join(f"<p>{p}</p>" for p in ps)}</div></details>' for q, ps in its)
    grouped = bool(items) and bool(items[0][1]) and isinstance(items[0][1][0], tuple)
    body = "".join(f'<h3 class="fq">{g}</h3>{rows(its)}' for g, its in items) if grouped else rows(items)
    return f'<div class="faq-box"><h2 id="{hid}">{title}</h2>{body}</div>'


def choices(white=False, cid="choose"):
    cls = "choice on-white" if white else "choice"
    out = []
    for key, n, rows in (("big", 10, 2), ("small", 3, 1)):
        c = CHOICES[key]
        d = c["short"] if white else c["desc"]
        out.append(f'<a class="{cls}" href="{c["href"]}"><span class="num">{c["count"]}<small>{c["unit"]}</small></span>{people(n, rows)}'
                   f'<strong>{c["title"]}</strong><span class="d">{d}</span><span class="s">{c["short"]}</span>'
                   f'<span class="go">{c["cta"]} <i aria-hidden="true">&#8250;</i></span></a>')
    return f'<div class="choices{" small" if white else ""}" id="{cid}">' + "".join(out) + "</div>"


def header(active):
    """active: "home", or the NAV key to mark ("groups" on the group pages, "team" on the founder page)."""
    home = active == "home"

    def here(href):
        # on the home page, links to its own sections scroll instead of reloading the page
        return href[len("index.html"):] if home and href.startswith("index.html#") else href

    links = []
    for href, label, key in NAV:
        cur = ' aria-current="true"' if key == active else ""
        links.append(f'<a href="{here(href)}"{cur}>{label}</a>')
    cta_href, cta_label = NAV_CTA
    cta_href = here(cta_href)   # "Apply now" goes to the application form from every page
    lk = logos.lockup_star(YELLOW, NAVY, NAVY, height=40)
    page = "" if CURRENT_PAGE == "index.html" else CURRENT_PAGE
    to = {"en": ("../" if LANG == "uz" else "") + page, "uz": ("" if LANG == "uz" else "uz/") + page}   # the same page
    parts = "".join(f'<span class="on" aria-current="true">{label}</span>' if code == LANG else
                    f'<a href="{to[code] or "./"}" hreflang="{code}" lang="{code}" title="{hint}">{label}</a>'
                    for code, label, hint in UI["langs"])
    lang_link = f'<span class="lang" role="group" aria-label="{UI["lang_label"]}">{parts}</span>'
    return f"""<header class="head">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="{UI["logo_label"]}">{lk}</a>
    <button class="menu-btn" id="menu-btn" data-menu-btn aria-expanded="false" aria-controls="nav">{UI["menu"]}</button>
    <nav class="nav" id="nav" aria-label="{UI["nav_label"]}">
      {"".join(links)}
      {lang_link}
      <a class="btn btn-navy" href="{cta_href}">{cta_label}</a>
    </nav>
  </div>
</header>"""


def footer():
    lk = logos.lockup_star(YELLOW, NAVY_DEEP, "#FFFFFF", height=38)
    return f"""<footer class="foot">
  <div class="wrap">
    <div>
      <a class="logo" href="index.html" aria-label="{UI["logo_label"]}">{lk}</a>
      <p style="margin-top:16px">{FOOTER_BLURB}</p>
      <p>{DISCLAIMER}</p>
      <div class="contact">
        <span><b>{UI["email"]}</b> {", ".join(f'<span class="mail">{e}</span>' for e in SITE["emails"])}</span>
        <span><b>{UI["telegram"]}</b> <a href="{SITE["telegram_url"]}" target="_blank" rel="noopener">@{SITE["telegram_bot"]}</a></span>
      </div>
    </div>
    <nav aria-label="{UI["footer_label"]}">
      {"".join(f'<a href="{h}">{t}</a>' for h, t in UI["footer_links"])}
      <span style="margin-top:14px">{COPYRIGHT}</span>
    </nav>
  </div>
</footer>
<script src="{ROOT}assets/config.js"></script>
<script src="{ROOT}assets/trek.js"></script>
<script src="{ROOT}assets/motion.js"></script>"""


def head(title=None, desc=None):
    """The page's <head> part: title and description from META, and links to the same page in each language."""
    title, desc = (title, desc) if title else META[CURRENT_PAGE]
    page = "" if CURRENT_PAGE == "index.html" else CURRENT_PAGE
    alts = "".join(f'<link rel="alternate" hreflang="{h}" href="{SITE_URL}{f}{page}">\n'
                   for h, f in (("en", ""), ("uz", "uz/"), ("x-default", "")))
    return f"""<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
{alts}
<link rel="icon" href="data:image/svg+xml,{logos.star_mark(YELLOW, NAVY).replace('"', "'").replace('#', '%23').replace('<', '%3C').replace('>', '%3E')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Kaushan+Script&display=swap" rel="stylesheet">
<style>{CSS}{MP.MOTION_CSS.replace("__WM__", MP.watermark_uri())}</style>"""


# ------------------------------------------------------------------ pages
PRESS_ICON = {
    "tv": '<rect x="2" y="3" width="12" height="8.5" rx="1.6"/><path d="M6 14h4M8 11.5V14"/>',
    "article": '<rect x="2.5" y="2.5" width="11" height="11" rx="1.6"/><path d="M5 6h6M5 8.5h6M5 11h3.5"/>',
    "news": '<rect x="2.5" y="2.5" width="11" height="11" rx="1.6"/><path d="M5 6h6M5 8.5h6M5 11h3.5"/>',
    "telegram": '<path d="M3.2 3h9.6A1.2 1.2 0 0 1 14 4.2v6A1.2 1.2 0 0 1 12.8 11.4H7.2L4.2 14v-2.6h-1A1.2 1.2 0 0 1 2 10.2v-6A1.2 1.2 0 0 1 3.2 3z"/>',
    "instagram": '<rect x="2.5" y="2.5" width="11" height="11" rx="2"/><path d="M4.5 11.2 7 8.4l1.8 1.8L10.4 8.8l1.4 2.4"/><circle cx="10.4" cy="5.6" r="1"/>',
    "video": '<circle cx="8" cy="8" r="6"/><path d="M6.9 5.7v4.6L10.6 8z" fill="currentColor" stroke="none"/>',
}


def press_block():
    P = PRESS
    star = f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="{MP.STAR_OUTLINE}"/></svg>'
    names = "".join(f"<span>{n}{star}</span>" for n in P["ticker"])
    arrow = ('<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M3.5 8.5 8.5 3.5M4.5 3.5h4v4" fill="none" '
             'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

    def card(kind, src, line, act, url):
        icon = (f'<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.5" '
                f'stroke-linecap="round" stroke-linejoin="round">{PRESS_ICON[kind]}</svg>')
        return (f'<a class="press-card" href="{url}" target="_blank" rel="noopener">'
                f'<span class="pc-kind">{icon}{UI["press_kind"][kind]}</span><b class="pc-src">{src}</b><span class="pc-line">{line}</span>'
                f'<span class="pc-go">{act}{arrow}</span><span class="sr">{UI["new_tab"]}</span></a>')

    years = "".join(
        f'<div class="press-year"><div class="py-label"><b>{yr}</b><span>{sub}</span></div>'
        f'<div class="press-grid">{"".join(card(*it) for it in items)}</div></div>'
        for yr, sub, items in P["years"])
    return f"""
  <section class="sec band-navy press" aria-labelledby="press-title">
    {side(light=True)}
    <div class="wrap">
      <div class="press-head">
        <h2 id="press-title">{P["title"]}</h2>
        <p class="lede">{P["lede"]} <span class="press-note">{P["note"]}</span></p>
      </div>
      <div class="ticker" aria-hidden="true"><div class="ticker-track"><span class="tk">{names}</span><span class="tk dup">{names}</span></div></div>
      <div class="press-years">{years}</div>
    </div>
  </section>
"""


def start_block():
    """Home page "How it works": the steps for an ambassador, where to find a group, tips and the sample texts."""
    S = START
    star = f'<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="{MP.STAR_OUTLINE}"/></svg>'
    steps = ""
    for i, (title, text, link) in enumerate(S["steps"], 1):
        go = f'<a class="go-link" href="{link[0]}">{link[1]}</a>' if link else ""
        steps += f'<li><span class="sn" aria-hidden="true">{star}<i>{i}</i></span><b>{title}</b><p>{text}</p>{go}</li>'
    chips = "".join(f"<li>{w}</li>" for w in S["where"])
    samples = ""
    # every block has the same three rows (title, button, bottom line), so blocks side by side line up (see .sample in CSS)
    for s in SAMPLES:
        tid = s["id"] + "-text"
        top = (f'<div class="sample-top"><span class="pill">{s["step"]}</span><h4 id="{s["id"]}-title">{s["title"]}</h4>'
               f'<p class="when">{s["when"]}</p></div>')
        if "text" in s:
            wa = ' data-copy-as="whatsapp"' if s.get("copy_as") == "whatsapp" else ""
            act = (f'<div class="copy-row"><button class="mini" type="button" data-copy="{tid}">{UI["copy_text"]}</button>'
                   f'<span class="copy-status" role="status" aria-live="polite"></span></div>')
            more = (f'<details><summary>{UI["read_text"]}</summary>'
                    f'<div class="sample-text" id="{tid}"{wa}{en_attr()}>{rich(s["text"])}</div></details>')
        else:
            href, open_label, dl_label = s["file"]
            href = ROOT + href
            act = f'<div class="copy-row"><a class="mini" href="{href}" target="_blank" rel="noopener">{open_label}</a></div>'
            more = f'<div class="sample-more"><a class="sample-dl" href="{href}" download>{dl_label}</a></div>'
        samples += f'<article class="sample" id="{s["id"]}" aria-labelledby="{s["id"]}-title">{top}{act}{more}</article>'
    return f"""
  <section class="sec start" id="how" aria-labelledby="start-title">
    <span id="start" aria-hidden="true"></span>
    {side()}
    <div class="wrap">
      <h2 id="start-title">{S["title"]}</h2>
      <p class="lede">{S["lede"]}</p>
      <ol class="steps">{steps}</ol>
      <div class="start-grid">
        <div class="start-box where"><h3>{S["where_title"]}</h3><ul class="chips">{chips}</ul></div>
        <div class="start-box tips"><h3>{S["tips_title"]}</h3>{diam(S["tips"])}</div>
      </div>
      <h3 class="samples-title">{S["samples_title"]}</h3>
      <div class="samples">{samples}</div>
    </div>
  </section>
"""


def route_block():
    days = {d["n"]: d for d in ITINERARY["days"]}

    def sday(n):
        d = days[n]
        return (f'<div class="sday"><b>{UI["day"].format(n=n)}</b><span class="where">{d["where"]}</span>'
                f'<ul>{"".join(f"<li>{i}</li>" for i in d["items"])}</ul></div>')

    cards = ""
    total = len(MP.STOPS)
    for i, st in enumerate(MP.STOPS):
        p = PH[st["photo"]]
        cap = STOP_CAPS.get(st["photo"]) or st["cap"] or p["caption"]
        card = (MAP or {}).get("cards", {}).get(st["city"]) or MP.CITIES[st["city"]]["card"]
        cards += (f'<article class="stop-card{" on" if i == 0 else ""}" data-city="{st["city"]}">'
                  f'<div class="stop-photo"><img src="{img(st["photo"])}" alt="{p["alt"]}" loading="lazy" decoding="async"><span class="cap">{cap}</span></div>'
                  f'<div class="stop-text"><p class="stop-n">{UI["stop_of"].format(i=i + 1, total=total)}</p><h3>{card}</h3>'
                  f'{"".join(sday(n) for n in st["days"])}</div></article>')
    return f"""
  <section class="itin" id="itinerary" aria-labelledby="itin-title">
    <div class="itin-head" style="background-image:linear-gradient(180deg, rgba(19,35,75,.84), rgba(19,35,75,.97)), url('{img("bukhara_palace_ceiling")}')">
      {side(light=True)}
      <div class="wrap">
        <h2 id="itin-title">{ITINERARY["title"]}</h2>
        <p class="lede">{ITINERARY["intro"]}</p>
      </div>
    </div>
    <div class="route-pin">
      <div class="route-stage wrap">
        <div class="map-wrap">{MP.route_svg(MAP)}<p class="map-hint" aria-hidden="true" data-hints="{"|".join(UI["map_hints"])}">{UI["map_hints"][0]}</p></div>
        <div class="stops">{cards}</div>
      </div>
    </div>
    <div class="wrap tailor-row">
      <div>
        <div class="tailor">
          <h3>{ITINERARY["tailor_title"]}</h3>
          {diam(ITINERARY["tailor"])}
        </div>
        <p class="tent">{ITINERARY["footnote"]}</p>
      </div>
      {pol("train_afrosiyob", None, None, "3/4")}
    </div>
  </section>"""


GET_ICON = {   # 24x24 line icons for "What you get"
    "slides": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M12 16v4M8.5 20h7M7 8.5h6M7 11.5h9"/>',
    "megaphone": '<path d="M4 10v4a1 1 0 0 0 1 1h2.2L12 19V5L7.2 9H5a1 1 0 0 0-1 1z"/><path d="M15.5 9a4 4 0 0 1 0 6M18.2 6.3a8 8 0 0 1 0 11.4"/>',
    "chat": '<path d="M20 12a8 8 0 0 1-11.7 7.1L4 20l1.1-4.1A8 8 0 1 1 20 12z"/><path d="M8.6 12.1l2.3 2.3 4.5-4.6"/>',
    "plane": ('<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4'
              'l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>'),
}


def page_home():
    q = QUOTES
    H, T, G, A = HERO, TEAM, GETS, APPLY
    collage = [("y2025_registan", None, "4/3.4"), ("food_plov", None, "3/4"), ("y2025_suzani", None, "4/3"), ("samarkand_circle", None, "3/4"),
               ("workshop_cooking", None, "3/4"), ("mountains_amirsoy_group", None, "4/3"), ("y2025_workshop", None, "4/3"), ("bukhara_golf_cart", None, "4/3"),
               ("a822", None, "4/3"), ("mountains_charvak", None, "4/3")]
    star = f'<svg viewBox="0 0 48 48" focusable="false"><path d="{MP.STAR_OUTLINE}"/></svg>'
    tranches = "".join(f'<li><span class="tn" aria-hidden="true">{star}<i>{i}</i></span><b>{t}</b><span class="d">{d}</span></li>'
                       for i, (t, d) in enumerate(PAYMENT["tranches"], 1))
    hero_pols = "".join(pol(k, None, "" if PH[k]["year"] and PH[k]["caption"].endswith(PH[k]["year"]) else None, lazy=False)
                        for k in H["photos"])
    assert H["title_sticker"] in H["title"], "HERO title_sticker must be part of the title"
    hero_title = H["title"].replace(H["title_sticker"], f'<span class="sticker">{H["title_sticker"]}</span>', 1)
    members = ""
    for m in T["members"]:
        av = f'<img src="{img(m["photo"])}" alt="" loading="lazy">' if m["photo"] else m["initials"]
        link = f'<a class="go-link" href="{m["link"][0]}">{m["link"][1]}</a>' if m["link"] else ""
        members += (f'<article class="member"><div class="avatar" aria-hidden="true">{av}</div><div>'
                    f'<span class="role">{m["role"]}</span><h3>{m["name"]}</h3><p>{m["text"]}</p>{link}</div></article>')
    gets = "".join(f'<li class="get"><span class="ic" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false">{GET_ICON[ic]}</svg></span>'
                   f'<b>{t}</b><p>{d}</p></li>' for ic, t, d in G["items"])
    body = f"""
<main>
  <section class="page-hero home-hero" aria-labelledby="home-title">
    {side()}
    <div class="wrap split">
      <div>
        <span class="kicker">{H["kicker"]}</span>
        <h1 id="home-title">{hero_title}</h1>
        <p class="lede">{H["lede"]}</p>
        <div class="btn-row">
          <a class="btn btn-navy" href="{H["cta_primary"][0]}">{H["cta_primary"][1]}</a>
          <a class="btn btn-line" href="{H["cta_secondary"][0]}">{H["cta_secondary"][1]}</a>
        </div>
      </div>
      <div class="hero-pols h">{hero_pols}</div>
    </div>
  </section>

  <section class="sec band-paper" id="team" aria-labelledby="team-title">
    <div class="wrap">
      <h2 id="team-title">{T["title"]}</h2>
      <p class="lede">{T["lede"]}</p>
      <div class="team-grid">{members}</div>
    </div>
  </section>

  <section class="sec band-navy" id="get" aria-labelledby="get-title">
    {side(light=True)}
    <div class="wrap">
      <h2 id="get-title">{G["title"]}</h2>
      <p class="lede">{G["lede"]}</p>
      <ul class="gets">{gets}</ul>
    </div>
  </section>
{start_block()}
  <section class="sec band-yellow" aria-labelledby="prev-title">
    {side()}
    <div class="wrap split">
      <div>
        <h2 id="prev-title">{PREVIOUS["title"]}</h2>
        {diam(PREVIOUS["bullets"])}
        <span class="red-script">{PREVIOUS["script"]}</span>{quote_note()}
        <div class="btn-row" data-float="0.07"><a class="btn btn-navy" href="founder.html">{UI["how_started"]}</a></div>
      </div>
      <div class="pols quotes">
        {pol("senate_handshake", "&ldquo;" + q["best"]["text"] + "&rdquo;", q["best"]["cite"], cls="pol q")}
        {pol("train_group", "&ldquo;" + q["guided"]["text"] + "&rdquo;", q["guided"]["cite"].split(",")[0], cls="pol q")}
        {pol("y2025_dancer", "&ldquo;" + q["dancing"]["text"] + "&rdquo;", q["dancing"]["cite"], cls="pol q")}
        {pol("cohort_registan", None, UI["cohort_sub"])}
      </div>
    </div>
  </section>
{press_block()}
  <section class="sec band-sky" aria-labelledby="mom-title">
    <div class="wrap">
      <h2 id="mom-title" class="moments-title">{UI["moments"]}</h2>
      <div class="collage">{"".join(pol(k, c, ar=a) for k, c, a in collage)}</div>
    </div>
  </section>

{route_block()}

  <section aria-labelledby="inc-title">
    <div class="inc-grid">
      <div class="inc-photo" style="background-image:url('{img("samarkand_shahizinda")}')">{pol("samarkand_tillakari_dome", None, None, "3/4")}</div>
      <div class="inc-text">
        <h2 id="inc-title">{UI["includes_title"]}</h2>
        <div class="inc-cols">
          <div><h3>{UI["included"]}</h3>{diam(INCLUDED)}</div>
          <div><h3>{UI["not_included"]}</h3>{diam(NOT_INCLUDED, "diam x")}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="pay-title">
    {side()}
    <div class="wrap split">
      <div>
        <h2 id="pay-title">{PAYMENT["title"]}</h2>
        <p class="lede">{PAYMENT["lede"]}</p>
        <h3 style="margin-top:30px">{PAYMENT["tranches_title"]}</h3>
        <ol class="tranches">{tranches}</ol>
        <p class="pay-note">{PAYMENT["note"]}</p>
      </div>
      <div class="pols">
        {pol("a626")}
        {pol("food_tandir", None, None, "3/4")}
      </div>
    </div>
  </section>

  <section class="sec faq-sec" id="faq" aria-labelledby="faq-title" style="{faq_bg("tashkent_civilization_dome")}">
    <div class="wrap">{faq_block(UI["faq"], FAQ_HOME, "faq-title")}</div>
  </section>

  <section class="sec band-yellow apply" id="apply" aria-labelledby="apply-title">
    {side()}
    <div class="wrap form-wrap">
      <div>
        <h2 id="apply-title">{A["title"]}</h2>
        <p class="lede">{A["lede"]}</p>
        <h3>{A["who_title"]}</h3>
        {diam(A["who"])}
      </div>
      {ambassador_form("btn btn-navy", "a", FORMS, FORM_COMMON)}
    </div>
  </section>

  <section class="sec band-paper" id="groups" aria-labelledby="groups-title">
    <div class="wrap">
      <h2 id="groups-title" style="text-align:center">{GROUPS["title"]}</h2>
      <p class="lede" style="margin:12px auto 32px; text-align:center">{GROUPS["lede"]}</p>
      {choices(white=True, cid="choose")}
    </div>
  </section>
</main>
"""
    return head() + header("home") + body + footer()


def page_big():
    B = BIG
    cards = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in B["for"])
    tl = "".join(f"<li><b>{w}</b><span>{s}</span></li>" for w, s in B["timeline"])
    body = f"""
<main>
  <section class="page-hero" aria-labelledby="big-title">
    {side()}
    <div class="wrap split">
      <div>
        <span class="kicker">{B["kicker"]}</span>
        <h1 id="big-title">{B["title"]}</h1>
        <p class="lede">{B["lede"]}</p>
        <div class="btn-row">
          <a class="btn btn-navy" href="{B["cta_primary"][0]}">{B["cta_primary"][1]}</a>
          <a class="btn btn-line" href="{B["cta_secondary"][0]}">{B["cta_secondary"][1]}</a>
        </div>
      </div>
      <div class="hero-pols">
        {pol("a070", None, None, lazy=False)}
        {pol("a474", None, None, "4/3", lazy=False)}
        {pol("a634", None, None, lazy=False)}
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="for-title">
    <div class="wrap">
      <h2 id="for-title">{B["for_title"]}</h2>
      <div class="cards3">{cards}</div>
    </div>
  </section>

  <section class="sec band-navy" aria-labelledby="get-title">
    {side(light=True)}
    <div class="wrap split">
      <div>
        <h2 id="get-title">{B["gets_title"]}</h2>
        {diam(B["gets"])}
      </div>
      <div class="pols">
        {pol("a060")}
        {pol("nowruz_trees", None, None, "3/4")}
      </div>
    </div>
  </section>

  <section class="sec band-paper" aria-labelledby="split-title">
    <div class="wrap">
      <h2 id="split-title">{B["split_title"]}</h2>
      <div class="who-grid">
        <div class="who"><h3>{UI["you"]}</h3><ul>{"".join(f"<li>{i}</li>" for i in B["you"])}</ul></div>
        <div class="who us"><h3>{UI["we"]}</h3><ul>{"".join(f"<li>{i}</li>" for i in B["we"])}</ul></div>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="time-title">
    <div class="wrap">
      <h2 id="time-title">{B["timeline_title"]}</h2>
      <ol class="timeline">{tl}</ol>
      <p class="tl-note">{B["timeline_note"]}</p>
    </div>
  </section>

  <section class="sec band-navy" id="quote" aria-labelledby="quote-title">
    <div class="wrap form-wrap">
      <div>
        <h2 id="quote-title">{B["form_title"]}</h2>
        <p class="lede">{B["form_lede"]}</p>
      </div>
      {big_group_form("btn btn-yellow", "b", FORMS, FORM_COMMON, INTERESTS)}
    </div>
  </section>

  <section class="sec faq-sec" aria-labelledby="bfaq-title" style="{faq_bg("a693")}">
    <div class="wrap">{faq_block(B["faq_title"], B["faq"], "bfaq-title")}</div>
  </section>
</main>
"""
    return head() + header("groups") + body + footer()


def page_small():
    S = SMALL

    def opt(o, key, alt_ar="16/9"):
        p = PH[key]
        return (f'<article class="opt"><div class="ph"><img src="{img(key)}" alt="{p["alt"]}" loading="lazy"></div><div class="body">'
                f'<span class="tag">{o["tag"]}</span><h3>{o["title"]}</h3>{diam(o["items"])}'
                f'<a class="btn btn-navy" href="{o["cta"][0]}">{o["cta"][1]}</a></div></article>')

    rows = "".join(f'<tr><td><b>{d["name"]}</b>{d["len"]}</td><td>{d["dates"]}</td><td>{d["why"]}</td><td><span class="pill">{d["status"]}</span></td>'
                   f'<td><button class="mini" type="button" data-pick="{d["pick"]}">{UI["register_interest"]}</button></td></tr>' for d in S["departures"])
    cmp_head = "".join(f"<th>{h}</th>" for h in S["cmp_head"])
    cmp_rows = "".join("<tr>" + f"<td><b>{r[0]}</b></td>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in S["cmp_rows"])
    body = f"""
<main>
  <section class="page-hero" aria-labelledby="small-title">
    {side()}
    <div class="wrap split">
      <div>
        <span class="kicker">{S["kicker"]}</span>
        <h1 id="small-title">{S["title"]}</h1>
        <p class="lede">{S["lede"]}</p>
        <div class="btn-row">
          <a class="btn btn-navy" href="{S["cta_primary"][0]}">{S["cta_primary"][1]}</a>
          <a class="btn btn-line" href="{S["cta_secondary"][0]}">{S["cta_secondary"][1]}</a>
        </div>
      </div>
      <div class="hero-pols">
        {pol("a916", None, None, lazy=False)}
        {pol("a315", None, None, "4/3", lazy=False)}
        {pol("mountains_horse", None, None, "4/3", lazy=False)}
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="ways-title">
    <div class="wrap">
      <h2 id="ways-title">{S["ways_title"]}</h2>
      <div class="opt-grid">{opt(S["join"], "a947")}{opt(S["private"], "a365")}</div>
    </div>
  </section>

  <section class="sec band-yellow" id="departures" aria-labelledby="dep-title">
    {side()}
    <div class="wrap">
      <h2 id="dep-title">{S["dep_title"]}</h2>
      <p class="lede">{S["dep_lede"]}</p>
      <div class="table-wrap">
        <table>
          <thead><tr>{"".join(f"<th>{h}</th>" for h in UI["dep_head"][:4])}<th><span class="sr">{UI["dep_head"][4]}</span></th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="cmp-title">
    <div class="wrap">
      <h2 id="cmp-title">{S["cmp_title"]}</h2>
      <div class="table-wrap"><table><thead><tr>{cmp_head}</tr></thead><tbody>{cmp_rows}</tbody></table></div>
      <p class="muted" style="margin-top:16px">{S["cmp_note"]}</p>
    </div>
  </section>

  <section class="sec band-navy" id="interest" aria-labelledby="int-title">
    <div class="wrap form-wrap">
      <div>
        <h2 id="int-title">{S["form_title"]}</h2>
        <p class="lede">{S["form_lede"]}</p>
      </div>
      {small_group_form("btn btn-yellow", "s", S["departures"], FORMS, FORM_COMMON)}
    </div>
  </section>

  <section class="sec faq-sec" aria-labelledby="sfaq-title" style="{faq_bg("a489")}">
    <div class="wrap">{faq_block(S["faq_title"], S["faq"], "sfaq-title")}</div>
  </section>
</main>
"""
    return head() + header("groups") + body + footer()


def page_founder():
    F = FOUNDER
    facts = "".join(f"<div><b>{a}</b>{b}</div>" for a, b in F["facts"])
    story = "".join(f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for h, ps in F["story"])
    tl = "".join(f'<li><b>{a}</b>{f"<strong>{n}</strong>" if n else ""}<span>{t}</span></li>' for a, n, t in F["timeline"])
    quotes = "".join(f'<div><blockquote class="bigquote">{QUOTES[k]["text"]}</blockquote><p class="cite">{QUOTES[k]["cite"]}</p></div>' for k in F["quotes"])
    areas = "".join(f'<div class="areas-col"><h3>{grp}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>' for grp, items in F["areas"].items())
    moments = "".join(pol(k, None, "", ar=a) for k, a in F["moments"])
    body = f"""
<main>
  <section class="page-hero" aria-labelledby="f-title">
    {side()}
    <div class="wrap split">
      <div class="hero-pols f">
        {pol("founder_portrait", F["name"], UI["cofounder"], "3/4", lazy=False)}
        {pol("y2025_hazrati_imam", None, "", lazy=False)}
      </div>
      <div>
        <span class="kicker">{F["kicker"]}</span>
        <h1 id="f-title">{F["name"]}</h1>
        <p class="lede">{F["lede"]}</p>
        <div class="facts">{facts}</div>
      </div>
    </div>
  </section>

  <section class="sec" aria-label="{UI["story_label"]}">
    <div class="wrap story-grid">
      <article class="story">
        {story}
        <span class="sig">{F["signature"]}<small>{UI["signature_role"]}</small></span>
      </article>
      <aside class="story-side">
        {pol("senate_group", None, "", "3/2")}
        {pol("with_shakhnoza", None, "", "3/4")}
        {pol("a573", None, "")}
      </aside>
    </div>
  </section>

  <section class="sec band-sky" aria-labelledby="fm-title">
    <div class="wrap">
      <h2 id="fm-title" class="moments-title">{F["moments_title"]}</h2>
      <div class="collage">{moments}</div>
    </div>
  </section>

  <section class="sec band-navy" aria-labelledby="tl-title">
    {side(light=True)}
    <div class="wrap">
      <h2 id="tl-title">{F["timeline_title"]}</h2>
      <ol class="tl">{tl}</ol>
    </div>
  </section>

  <section class="sec band-yellow" aria-labelledby="q-title">
    {side()}
    <div class="wrap split">
      <div>
        <h2 id="q-title" style="margin-bottom:26px">{F["quotes_title"]}</h2>
        <div class="quotes2">{quotes}</div>{quote_note()}
      </div>
      <div class="pols">
        {pol("y2025_nowruz", None, None, "3/4")}
        {pol("y2025_kalyan", None, None, "3/4")}
      </div>
    </div>
  </section>

  <section class="sec" aria-labelledby="areas-title">
    <div class="wrap">
      <h2 id="areas-title">{F["areas_title"]}</h2>
      <div class="areas-grid">{areas}</div>
      <p class="muted" style="margin-top:20px; max-width:72ch">{F["areas_note"]}</p>
    </div>
  </section>

  <section class="sec band-yellow" aria-labelledby="fcta-title">
    <div class="wrap" style="text-align:center">
      <h2 id="fcta-title">{F["cta_title"]}</h2>
      <p class="lede" style="margin:12px auto 0">{F["cta_lede"]}</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn-navy" href="{NAV_CTA[0]}">{NAV_CTA[1]}</a>
        <a class="btn btn-line" href="index.html#how">{UI["how_it_works"]}</a>
      </div>
      <p class="groups-note">{F["cta_groups"]}</p>
    </div>
  </section>
</main>
"""
    return head() + header("team") + body + footer()


def page_contact():
    C = CONTACT
    cards = ""
    for p in C["people"]:
        mid = "mail-" + p["initials"].lower()
        cards += (f'<article class="member"><div class="avatar" aria-hidden="true">{p["initials"]}</div><div>'
                  f'<span class="role">{p["role"]}</span><h3>{p["name"]}</h3><p>{p["school"]}</p>'
                  f'<div class="contact-mail"><a class="addr" id="{mid}" href="mailto:{p["email"]}">{p["email"]}</a>'
                  f'<button class="mini" type="button" data-copy="{mid}">{UI["copy"]}</button>'
                  f'<span class="copy-status" role="status" aria-live="polite"></span></div></div></article>')
    plane = '<svg viewBox="0 0 24 24" focusable="false"><path d="M2.5 11.3 21.6 3.2l-3.4 17.4-5.9-4.4-3.1 3 .4-4.8 8.3-7.6-10.2 6.3z"/></svg>'
    cards += (f'<article class="member tg"><div class="avatar" aria-hidden="true">{plane}</div><div>'
              f'<span class="role">{C["telegram_role"]}</span><h3>{C["telegram_title"]}</h3><p>{C["telegram_text"]}</p>'
              f'<a class="btn btn-navy tg-btn" href="{SITE["telegram_url"]}" target="_blank" rel="noopener">{C["telegram_cta"]}</a></div></article>')
    nxt = "".join(f'<a class="go-link" href="{h}">{t}</a>' for h, t in C["next"])
    body = f"""
<main>
  <section class="page-hero contact-hero" aria-labelledby="c-title">
    {side()}
    <div class="wrap">
      <span class="kicker">{C["kicker"]}</span>
      <h1 id="c-title">{C["title"]}</h1>
      <p class="lede">{C["lede"]}</p>
    </div>
  </section>

  <section class="sec" aria-label="{UI["reach_label"]}">
    <div class="wrap">
      <div class="team-grid contact-grid">{cards}</div>
      <h2 class="samples-title">{C["next_title"]}</h2>
      <div class="contact-next">{nxt}</div>
    </div>
  </section>
</main>
"""
    return head() + header("contact") + body + footer()


PAGES = {"index.html": page_home, "big-group.html": page_big, "small-group.html": page_small, "founder.html": page_founder,
         "contact.html": page_contact}


def full_doc(inner):
    head_part, rest = inner.split('<header class="head">', 1)
    return (f'<!doctype html>\n<html lang="{LANG}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head_part + '</head>\n<body>\n<header class="head">' + rest + '\n</body>\n</html>\n')


def fix_links(html):
    return html.replace('href="index.html#', 'href="./#').replace('href="index.html"', 'href="./"')


def main():
    """Writes the pages in PAGES to the site root (English) and to uz/ (Uzbek).
    With --preview DIR it also writes claude.ai preview copies of the English pages there."""
    global CURRENT_PAGE
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    if preview:
        os.makedirs(preview, exist_ok=True)
    for lang, (mod, folder) in LANGS.items():
        set_lang(lang)
        out_dir = os.path.join(SITE_ROOT, folder)
        os.makedirs(out_dir, exist_ok=True)
        for name, fn in PAGES.items():
            CURRENT_PAGE = name
            inner = fix_links(fn())
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
                fh.write(full_doc(inner))
            if preview and lang == "en":
                with open(os.path.join(preview, name), "w", encoding="utf-8") as fh:
                    fh.write(inner if name == "index.html" else full_doc(inner))
        print(f"built ({lang}):", ", ".join((folder + "/" if folder else "") + n for n in PAGES))
    set_lang("en")


if __name__ == "__main__":
    main()
