"""Uzbekistan Trek logo options as SVG strings (text converted to outlines, so the files need no fonts).

Options:
  A  Khatam star   8-point tile star from Uzbek girih tilework, with a horizontal wordmark
  B  Registan      three madrasa portals, a dome and four minarets, the Registan in one line
  C  Stamp         round passport stamp: UZBEKISTAN TREK / SINCE 2025 around a madrasa portal
  D  Monogram      UT in a glazed tile, for avatars and favicons
  E  Ikat          wordmark over an ikat diamond band
Run this file to write every option as .svg files into ../logos/ (or a folder given as argv[1]).
"""
import math, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_FONTS = {}


def _font(name):
    if name not in _FONTS:
        _FONTS[name] = TTFont(os.path.join(FONT_DIR, name + ".ttf"))
    return _FONTS[name]


def _glyph(fontname, ch):
    f = _font(fontname)
    gs = f.getGlyphSet()
    g = f.getBestCmap().get(ord(ch))
    return (gs[g] if g else None), gs, f["head"].unitsPerEm


def text_outline(text, fontname="archivo-latin-900-normal", size=40.0, tracking=0.0, x0=0.0, baseline=0.0):
    """Return (svg path d, width, (xmin, ymin, xmax, ymax)) for text set on a baseline (y grows downward)."""
    x = x0
    parts = []
    bp = None
    for ch in text:
        g, gs, upm = _glyph(fontname, ch)
        s = size / upm
        if g is None:
            x += size * 0.28 + tracking
            continue
        pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        parts.append(pen.getCommands())
        b = BoundsPen(gs)
        g.draw(TransformPen(b, (s, 0, 0, -s, x, baseline)))
        if b.bounds:
            bp = b.bounds if bp is None else (min(bp[0], b.bounds[0]), min(bp[1], b.bounds[1]), max(bp[2], b.bounds[2]), max(bp[3], b.bounds[3]))
        x += g.width * s + tracking
    return " ".join(parts), x - tracking - x0, bp


def cap_height(fontname, size):
    g, gs, upm = _glyph(fontname, "H")
    b = BoundsPen(gs)
    g.draw(b)
    return (b.bounds[3] - b.bounds[1]) * size / upm


def arc_text(text, fontname, size, cx, cy, r, center_deg, bottom=False, tracking=0.0):
    """Glyphs set along a circle. center_deg: -90 is the top of the circle (SVG y down), 90 the bottom."""
    widths = []
    for ch in text:
        g, gs, upm = _glyph(fontname, ch)
        widths.append((g.width * size / upm if g else size * 0.28) + tracking)
    total = sum(widths) - tracking
    span = total / r  # radians
    ch_h = cap_height(fontname, size)
    out = []
    if not bottom:
        theta = math.radians(center_deg) - span / 2
        step_sign = 1
    else:
        theta = math.radians(center_deg) + span / 2
        step_sign = -1
    for ch, w in zip(text, widths):
        g, gs, upm = _glyph(fontname, ch)
        mid = theta + step_sign * (w - tracking) / 2 / r
        px, py = cx + r * math.cos(mid), cy + r * math.sin(mid)
        rot = math.degrees(mid) + (90 if not bottom else -90)
        if g is not None:
            s = size / upm
            gw = g.width * s
            pen = SVGPathPen(gs)
            g.draw(TransformPen(pen, (s, 0, 0, -s, -gw / 2, ch_h / 2)))
            out.append(f'<path transform="translate({px:.2f} {py:.2f}) rotate({rot:.2f})" d="{pen.getCommands()}"/>')
        theta += step_sign * w / r
    return "".join(out)


def _arch(xa, xb, yt, yb):
    """Pointed (Timurid) arch from x=xa to xb, apex at yt, open to the bottom yb."""
    w = xb - xa
    xm = (xa + xb) / 2
    ys = yt + w * 0.62
    return (f"M{xa:.2f} {yb:.2f} V{ys:.2f} C{xa:.2f} {ys - w*0.42:.2f} {xm - w*0.18:.2f} {yt + w*0.12:.2f} {xm:.2f} {yt:.2f} "
            f"C{xm + w*0.18:.2f} {yt + w*0.12:.2f} {xb:.2f} {ys - w*0.42:.2f} {xb:.2f} {ys:.2f} V{yb:.2f} Z")


# ------------------------------------------------------------------ marks
def star_mark(c1="#FBB617", c2="#1C3166", size=48):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="{size}" height="{size}" role="img" aria-label="Uzbekistan Trek">'
            f'<g fill="{c1}"><rect x="8" y="8" width="32" height="32" rx="1.5"/><rect x="8" y="8" width="32" height="32" rx="1.5" transform="rotate(45 24 24)"/></g>'
            f'<g fill="{c2}"><rect x="15" y="15" width="18" height="18"/><rect x="15" y="15" width="18" height="18" transform="rotate(45 24 24)"/></g>'
            f'<circle cx="24" cy="24" r="4.2" fill="{c1}"/></svg>')


def star_shapes(c1, c2, x=0, y=0, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><g fill="{c1}"><rect x="8" y="8" width="32" height="32" rx="1.5"/>'
            f'<rect x="8" y="8" width="32" height="32" rx="1.5" transform="rotate(45 24 24)"/></g>'
            f'<g fill="{c2}"><rect x="15" y="15" width="18" height="18"/><rect x="15" y="15" width="18" height="18" transform="rotate(45 24 24)"/></g>'
            f'<circle cx="24" cy="24" r="4.2" fill="{c1}"/></g>')


def registan_shapes(c, uid="rg"):
    """Skyline in a 120 x 48 box. Returns (defs, body)."""
    holes = " ".join([_arch(16.5, 25.5, 17, 44.5), _arch(56, 64, 19, 44.5), _arch(94.5, 103.5, 17, 44.5),
                      _arch(9, 13, 27, 44.5), _arch(29, 33, 27, 44.5), _arch(46, 50, 29, 44.5), _arch(70, 74, 29, 44.5),
                      _arch(87, 91, 27, 44.5), _arch(107, 111, 27, 44.5)])
    defs = (f'<mask id="{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="120" height="48">'
            f'<rect width="120" height="48" fill="#fff"/><path d="{holes}" fill="#000"/></mask>')
    body = (f'<g fill="{c}" mask="url(#{uid})">'
            '<rect x="0" y="44.5" width="120" height="3.5"/>'
            '<rect x="6" y="22" width="30" height="23"/><rect x="12" y="11" width="18" height="34"/>'
            '<rect x="42" y="24" width="36" height="21"/><rect x="51.5" y="15" width="17" height="30"/>'
            '<path d="M51 16.5 C51 9 55.5 5.2 60 1 C64.5 5.2 69 9 69 16.5 Z"/>'
            '<rect x="84" y="22" width="30" height="23"/><rect x="90" y="11" width="18" height="34"/>'
            '<path d="M84.5 22.5 C84.5 18 86.5 16.2 88 14.2 C89.5 16.2 91.5 18 91.5 22.5 Z"/>'
            '<path d="M106.5 22.5 C106.5 18 108.5 16.2 110 14.2 C111.5 16.2 113.5 18 113.5 22.5 Z"/>'
            '<path d="M1.6 45 L2.4 9 H5.6 L6.4 45 Z"/><rect x="1.2" y="6.6" width="5.6" height="2.6" rx=".6"/>'
            '<path d="M36.6 45 L37.3 11 H40.2 L40.9 45 Z"/><rect x="36.3" y="8.7" width="4.9" height="2.4" rx=".6"/>'
            '<path d="M79.1 45 L79.8 11 H82.7 L83.4 45 Z"/><rect x="78.8" y="8.7" width="4.9" height="2.4" rx=".6"/>'
            '<path d="M113.6 45 L114.4 9 H117.6 L118.4 45 Z"/><rect x="113.2" y="6.6" width="5.6" height="2.6" rx=".6"/>'
            '</g>')
    return defs, body


def registan_mark(c="#C9A04A", size=120, uid="rgm"):
    defs, body = registan_shapes(c, uid)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 48" width="{size}" height="{size*0.4:.0f}" role="img" aria-label="Uzbekistan Trek">'
            f'<defs>{defs}</defs>{body}</svg>')


def portal_shapes(c, uid, cx=60, cy=62, s=1.0):
    """Single madrasa portal with two minarets, centred on (cx, cy), about 44 wide, 40 tall at s=1."""
    hole = _arch(-6, 6, -9, 18.5)
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<defs><mask id="{uid}" maskUnits="userSpaceOnUse" x="-30" y="-30" width="60" height="60"><rect x="-30" y="-30" width="60" height="60" fill="#fff"/>'
            f'<path d="{hole}" fill="#000"/></mask></defs>'
            f'<g fill="{c}" mask="url(#{uid})"><rect x="-13" y="-16" width="26" height="35"/>'
            f'<path d="M-10 -16 C-10 -24 -4.5 -27.5 0 -32 C4.5 -27.5 10 -24 10 -16 Z"/>'
            f'<path d="M-22.5 19 L-21.6 -18 H-18.4 L-17.5 19 Z"/><rect x="-23" y="-20.6" width="6" height="2.8" rx=".6"/>'
            f'<path d="M17.5 19 L18.4 -18 H21.6 L22.5 19 Z"/><rect x="17" y="-20.6" width="6" height="2.8" rx=".6"/>'
            f'<rect x="-26" y="19" width="52" height="3"/></g></g>')


def stamp_mark(c="#1C3166", size=120, uid="stp", bg=None):
    f = "archivo-latin-800-normal"
    top = arc_text("UZBEKISTAN TREK", f, 10.4, 60, 60, 46.5, -90, bottom=False, tracking=1.35)
    bot = arc_text("SINCE 2025", f, 10.4, 60, 60, 46.5, 90, bottom=True, tracking=1.8)
    dots = "".join(f'<rect x="{60 + 46.5*math.cos(math.radians(a)) - 2.4:.2f}" y="{60 + 46.5*math.sin(math.radians(a)) - 2.4:.2f}" width="4.8" height="4.8" '
                   f'transform="rotate(45 {60 + 46.5*math.cos(math.radians(a)):.2f} {60 + 46.5*math.sin(math.radians(a)):.2f})"/>' for a in (0, 180))
    bgc = f'<circle cx="60" cy="60" r="59" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="{size}" height="{size}" role="img" aria-label="Uzbekistan Trek, since 2025">'
            f'{bgc}<g fill="none" stroke="{c}"><circle cx="60" cy="60" r="57.5" stroke-width="3"/><circle cx="60" cy="60" r="36" stroke-width="1.6"/></g>'
            f'<g fill="{c}">{top}{bot}{dots}</g>{portal_shapes(c, uid, 60, 62, 0.92)}</svg>')


def monogram_mark(bg="#A51C30", fg="#FFFFFF", size=48, fontname="source-serif-4-latin-700-normal"):
    d, w, b = text_outline("UT", fontname, 26, tracking=-0.6)
    tw = b[2] - b[0]
    th = b[3] - b[1]
    tx = 24 - (b[0] + tw / 2)
    ty = 24.6 - (b[1] + th / 2)
    corners = "".join(f'<rect x="{x-1.6}" y="{y-1.6}" width="3.2" height="3.2" transform="rotate(45 {x} {y})"/>' for x, y in ((8, 8), (40, 8), (8, 40), (40, 40)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="{size}" height="{size}" role="img" aria-label="Uzbekistan Trek">'
            f'<rect width="48" height="48" rx="9" fill="{bg}"/><rect x="4.5" y="4.5" width="39" height="39" rx="5.5" fill="none" stroke="{fg}" stroke-opacity=".55" stroke-width="1"/>'
            f'<g fill="{fg}" fill-opacity=".85">{corners}</g><path fill="{fg}" transform="translate({tx:.2f} {ty:.2f})" d="{d}"/></svg>')


IKAT = ["#C2272D", "#FBB617", "#1E9BB0", "#1C3166"]


def ikat_band(x, y, width, h=9, colors=IKAT):
    n = max(4, int(round(width / (h * 1.5))))
    step = width / n
    out = []
    for i in range(n):
        cx = x + step * (i + 0.5)
        col = colors[i % len(colors)]
        out.append(f'<path d="M{cx - step/2:.2f} {y + h/2:.2f} L{cx:.2f} {y:.2f} L{cx + step/2:.2f} {y + h/2:.2f} L{cx:.2f} {y + h:.2f} Z" fill="{col}"/>')
    return "".join(out)


# ------------------------------------------------------------------ lockups
def lockup_star(c1="#FBB617", c2="#1C3166", text_color="#1C3166", height=44):
    f = "archivo-latin-900-normal"
    d, w, b = text_outline("UZBEKISTAN TREK", f, 21, tracking=1.1)
    ch = cap_height(f, 21)
    base = 24 + ch / 2
    d, w, b = text_outline("UZBEKISTAN TREK", f, 21, tracking=1.1, x0=60, baseline=base)
    W = 60 + w + 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} 48" height="{height}" width="{height*W/48:.1f}" role="img" aria-label="Uzbekistan Trek">'
            f'{star_shapes(c1, c2)}<path fill="{text_color}" d="{d}"/></svg>')


def lockup_registan(c="#C9A04A", text_color="#C9A04A", height=64, uid="rgl"):
    f = "el-messiri-latin-700-normal"
    d, w, b = text_outline("Uzbekistan Trek", f, 24, tracking=0.4)
    tw = b[2] - b[0]
    W = max(120, tw) + 4
    x0 = (W - tw) / 2 - b[0]
    d, w, b2 = text_outline("Uzbekistan Trek", f, 24, tracking=0.4, x0=x0, baseline=72)
    H = b2[3] + 3
    defs, body = registan_shapes(c, uid)
    sx = (W - 120) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" height="{height}" width="{height*W/H:.1f}" role="img" aria-label="Uzbekistan Trek">'
            f'<defs>{defs}</defs><g transform="translate({sx:.2f} 0)">{body}</g><path fill="{text_color}" d="{d}"/></svg>')


def lockup_registan_h(c="#C9A04A", text_color="#C9A04A", height=40, uid="rgh"):
    f = "el-messiri-latin-700-normal"
    defs, body = registan_shapes(c, uid)
    ch = cap_height(f, 26)
    d, w, b = text_outline("Uzbekistan Trek", f, 26, tracking=0.4, x0=132, baseline=24 + ch / 2 + 2)
    W = 132 + w + 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} 48" height="{height}" width="{height*W/48:.1f}" role="img" aria-label="Uzbekistan Trek">'
            f'<defs>{defs}</defs>{body}<path fill="{text_color}" d="{d}"/></svg>')


def lockup_monogram(bg="#A51C30", fg="#FFFFFF", text_color="#1E1E1E", height=44):
    f = "source-serif-4-latin-700-normal"
    mono = monogram_mark(bg, fg, 48).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" role="img" aria-label="Uzbekistan Trek">', '<g>').replace('</svg>', '</g>')
    ch = cap_height(f, 24)
    d, w, b = text_outline("Uzbekistan Trek", f, 24, tracking=0.2, x0=60, baseline=24 + ch / 2)
    W = 60 + w + 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} 48" height="{height}" width="{height*W/48:.1f}" role="img" aria-label="Uzbekistan Trek">'
            f'{mono}<path fill="{text_color}" d="{d}"/></svg>')


def lockup_ikat(text_color="#1C3166", height=48, colors=IKAT):
    f = "archivo-latin-900-normal"
    d, w, b = text_outline("Uzbekistan Trek", f, 30, tracking=0.2, x0=0, baseline=26)
    W = b[2] + 1
    band = ikat_band(b[0], 33, b[2] - b[0], 9, colors)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} 44" height="{height}" width="{height*W/44:.1f}" role="img" aria-label="Uzbekistan Trek">'
            f'<path fill="{text_color}" d="{d}"/>{band}</svg>')


def write_all(folder):
    os.makedirs(folder, exist_ok=True)
    files = {
        "logo-a-star-mark.svg": star_mark(),
        "logo-a-star-lockup.svg": lockup_star(),
        "logo-a-star-lockup-white.svg": lockup_star(text_color="#FFFFFF"),
        "logo-b-registan-mark.svg": registan_mark(),
        "logo-b-registan-lockup.svg": lockup_registan(),
        "logo-b-registan-lockup-h.svg": lockup_registan_h(),
        "logo-c-stamp-navy.svg": stamp_mark("#1C3166"),
        "logo-c-stamp-gold-on-navy.svg": stamp_mark("#FBB617", bg="#13234B", uid="stp2"),
        "logo-d-monogram-crimson.svg": monogram_mark(),
        "logo-d-monogram-lockup.svg": lockup_monogram(),
        "logo-e-ikat-wordmark.svg": lockup_ikat(),
    }
    for name, svg in files.items():
        with open(os.path.join(folder, name), "w", encoding="utf-8") as fh:
            fh.write(svg)
    return files


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos")
    print("wrote", list(write_all(out)))
