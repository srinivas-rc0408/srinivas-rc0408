"""Generates every SVG for the srinivas-rc0408 profile README. Monochrome. Run: python3 build.py"""
import math, random
from xml.sax.saxutils import escape as esc

BK, W = "#000000", "#FFFFFF"
G1, G2, G3, G4 = "#A3A3A3", "#5C5C5C", "#262626", "#141414"
MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono','Cascadia Mono','DejaVu Sans Mono',Menlo,Consolas,'Liberation Mono',monospace"
OUT = "assets/"

BASE_CSS = f"""
text{{font-family:{MONO};fill:{W}}}
.g1{{fill:{G1}}} .g2{{fill:{G2}}} .b{{font-weight:700}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes march{{to{{stroke-dashoffset:-16}}}}
"""
RM = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

def svg(w, h, title, desc, css, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<style>{BASE_CSS}{css}{RM}</style>{body}</svg>')

def crop_marks(x, y, w, h, L=14, col=W):
    p = []
    for (cx, cy, dx, dy) in [(x, y, 1, 1), (x+w, y, -1, 1), (x, y+h, 1, -1), (x+w, y+h, -1, -1)]:
        p.append(f'<path d="M{cx} {cy+dy*L}V{cy}H{cx+dx*L}" fill="none" stroke="{col}" stroke-width="1.5"/>')
    return "".join(p)

def write(name, s):
    open(OUT + name, "w").write(s)
    print(f"{name:26s} {len(s)/1024:6.1f} KB")

GLYPHS = {
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "1": ["..#..", ".##..", "#.#..", "..#..", "..#..", "..#..", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
}

# ------------------------------------------------------------------ HERO
def hero():
    Wd, H = 960, 470
    rnd = random.Random(10)
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>']
    # faint dot field
    b.append('<g>')
    for x in range(24, Wd, 24):
        for y in range(24, H - 70, 24):
            b.append(f'<circle cx="{x}" cy="{y}" r="1" fill="{G4}"/>')
    b.append('</g>')
    # a few twinkling field dots
    for i in range(10):
        x = 24 * rnd.randint(1, 39); y = 24 * rnd.randint(1, 16)
        b.append(f'<circle class="tw" cx="{x}" cy="{y}" r="1.4" fill="{G2}" style="animation-delay:{rnd.uniform(0, 6):.2f}s"/>')
    b.append(crop_marks(16, 16, Wd - 32, H - 32))
    # top meta
    b.append(f'<text x="40" y="48" class="g2" font-size="12">srinivas-rc0408 / readme</text>')
    b.append(f'<text x="{Wd-40}" y="48" class="g2" font-size="12" text-anchor="end">12.97&#176; N  77.59&#176; E</text>')

    # S10 dot matrix, assembling from scattered positions
    pitch, r = 24, 8.2
    gx, gy = 52, 98
    col0 = 0
    dots = []
    for g in "S10":
        for ri, row in enumerate(GLYPHS[g]):
            for ci, v in enumerate(row):
                if v == "#":
                    dots.append((gx + (col0 + ci) * pitch + pitch / 2, gy + ri * pitch + pitch / 2))
        col0 += 6
    b.append('<g>')
    for i, (x, y) in enumerate(dots):
        dx, dy = rnd.uniform(-260, 380), rnd.uniform(-160, 220)
        d = 0.25 + rnd.uniform(0, 0.9)
        b.append(f'<circle class="ab" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{W}" '
                 f'style="--dx:{dx:.0f}px;--dy:{dy:.0f}px;animation-delay:{d:.2f}s"/>')
    b.append('</g>')
    # ghost grid of the unlit matrix cells
    b.append('<g>')
    for c in range(17):
        for ri in range(7):
            x, y = gx + c * pitch + pitch / 2, gy + ri * pitch + pitch / 2
            if not any(abs(x - px) < 1 and abs(y - py) < 1 for px, py in dots):
                b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{G3}"/>')
    b.append('</g>')
    # looping scan line across the matrix
    mw = 17 * pitch
    b.append(f'<g class="scanwrap"><rect class="scan" x="{gx}" y="{gy-6}" width="2" height="{7*pitch+12}" fill="{W}"/></g>')

    # name
    b.append(f'<g class="in" style="animation-delay:1.35s"><text x="{gx+4}" y="{gy+7*pitch+58}" font-size="34" class="b" letter-spacing="1">Srinivas R C</text>'
             f'<text x="{gx+4}" y="{gy+7*pitch+84}" font-size="14" class="g1">AI/ML engineer, Bengaluru</text></g>')

    # right column: scrambled tagline
    RX = 520
    lines = ["I build AI that runs", "where the cloud can't."]
    fs, cw = 22, 22 * 0.6
    charset = "01#$%&*+<>/\\=?ABCDEFGHJKLMNPQRSTUVWXYZ"
    t = 1.0
    for li, line in enumerate(lines):
        y = 118 + li * 34
        for i, ch in enumerate(line):
            if ch == " ":
                continue
            x = RX + i * cw
            start = t + i * 0.035
            for k in range(3):
                g = rnd.choice(charset)
                b.append(f'<text class="sc g1" x="{x:.1f}" y="{y}" font-size="{fs}" style="animation-delay:{start + k*0.07:.2f}s">{esc(g)}</text>')
            b.append(f'<text class="in b" x="{x:.1f}" y="{y}" font-size="{fs}" style="animation-delay:{start + 0.21:.2f}s">{esc(ch)}</text>')
        t += 0.35

    rows = [
        ("focus", "offline agentic AI systems"),
        ("building", "AEGIS, air-gapped workbench, SIH 2026"),
        ("interning", "codebase migration agent, REVA"),
        ("stack", "python / langgraph / ollama / faiss"),
        ("machine", "rtx 3050 ti, 4 GB of VRAM, arch linux"),
    ]
    y = 214
    for i, (k, v) in enumerate(rows):
        d = 2.05 + i * 0.09
        b.append(f'<g class="in" style="animation-delay:{d:.2f}s"><text x="{RX}" y="{y}" font-size="13" class="g2">{k}</text>'
                 f'<text x="{RX+92}" y="{y}" font-size="13">{esc(v)}</text></g>')
        y += 24
    d = 2.05 + len(rows) * 0.09
    b.append(f'<g class="in" style="animation-delay:{d:.2f}s"><text x="{RX}" y="{y}" font-size="13" class="g2">status</text>'
             f'<circle class="pl" cx="{RX+97}" cy="{y-4.5}" r="4" fill="{W}"/>'
             f'<text x="{RX+110}" y="{y}" font-size="13">open to AI/ML internships</text></g>')

    # ticker
    ty = H - 58
    b.append(f'<line x1="16" x2="{Wd-16}" y1="{ty}" y2="{ty}" stroke="{G3}"/>')
    items = ["AEGIS", "codebase migration agent", "AquaSentinel", "ArchAgent", "health-risk-mlops", "Debug.ext", "SIH 2026", "B.Tech AI & ML, REVA '27"]
    tick = "   +   ".join(items) + "   +   "
    L = round(len(tick) * 13 * 0.6)
    b.append(f'<clipPath id="tc"><rect x="16" y="{ty}" width="{Wd-32}" height="42"/></clipPath>')
    b.append(f'<g clip-path="url(#tc)"><g class="tk">')
    for k in range(3):
        b.append(f'<text x="{16 + k*L}" y="{ty+26}" font-size="13" class="g1" textLength="{L}" lengthAdjust="spacing">{esc(tick)}</text>')
    b.append('</g></g>')

    css = f"""
.ab{{animation:ab 1.1s cubic-bezier(.16,1,.3,1) both}}
@keyframes ab{{from{{opacity:0;transform:translate(var(--dx),var(--dy))}}to{{opacity:1;transform:none}}}}
.sc{{opacity:0;animation:fl .07s linear}}
@keyframes fl{{0%,100%{{opacity:1}}}}
.in{{animation:show 0s step-end both}}
.scanwrap{{animation:show 0s step-end 2.6s both}}
.scan{{opacity:.55;animation:scan 7s cubic-bezier(.45,0,.55,1) 2.6s infinite}}
@keyframes scan{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:.55}}44%{{opacity:.55}}50%{{transform:translateX({mw}px);opacity:0}}100%{{transform:translateX({mw}px);opacity:0}}}}
.pl{{animation:pulse 1.6s ease-in-out infinite}}
.tw{{animation:pulse 3.2s ease-in-out infinite}}
.tk{{animation:tk 38s linear infinite}}
@keyframes tk{{to{{transform:translateX(-{L}px)}}}}
@media (prefers-reduced-motion:reduce){{.sc{{display:none}}}}
"""
    write("hero.svg", svg(Wd, H, "Srinivas R C (S10)",
        "S10 assembled from white dots. Srinivas R C, AI/ML engineer in Bengaluru. I build AI that runs where the cloud can't. "
        "Focus: offline agentic AI systems. Building AEGIS, an air-gapped workbench for SIH 2026. Interning on a codebase migration agent at REVA. "
        "Stack: Python, LangGraph, Ollama, FAISS. Status: open to AI/ML internships.", css, "".join(b)))

# ------------------------------------------------------------------ SECTION HEADERS
def header(slug, note):
    Wd, H = 960, 64
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>']
    b.append(f'<text x="24" y="41" font-size="22" class="b">~/{slug}</text>')
    cx = 24 + (2 + len(slug)) * 13.2 + 6
    b.append(f'<rect class="cu" x="{cx:.1f}" y="24" width="11" height="20" fill="{W}"/>')
    b.append(f'<line x1="{cx+28:.1f}" x2="{Wd-24-len(note)*7.8-20:.1f}" y1="34" y2="34" stroke="{G3}"/>')
    b.append(f'<text x="{Wd-24}" y="39" font-size="13" class="g2" text-anchor="end">{esc(note)}</text>')
    css = ".cu{animation:blink 1.06s step-end infinite}"
    write(f"h-{slug}.svg", svg(Wd, H, f"~/{slug}", note, css, "".join(b)))

# ------------------------------------------------------------------ PROJECT CARDS
CW_, CH_ = 470, 262

def chips(tags, x, y):
    out, cx = [], x
    for t in tags:
        w = len(t) * 6.3 + 16
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="none" stroke="{G2}"/>'
                   f'<text x="{cx + w/2:.1f}" y="{y+15}" font-size="10.5" class="g1" text-anchor="middle">{esc(t)}</text>')
        cx += w + 6
    assert cx - x < 640, (tags, cx - x)
    return "".join(out)

def card(fname, status, live, title, desc, tags, art, art_css, alt):
    b = [f'<rect width="{CW_}" height="{CH_}" fill="{BK}"/>',
         f'<rect x=".5" y=".5" width="{CW_-1}" height="{CH_-1}" fill="none" stroke="{G3}"/>',
         crop_marks(8, 8, CW_ - 16, CH_ - 16, 10, G1)]
    if live:
        b.append(f'<circle class="pl" cx="30" cy="38" r="4" fill="{W}"/>')
    else:
        b.append(f'<circle cx="30" cy="38" r="3.5" fill="none" stroke="{G1}"/>')
    b.append(f'<text x="42" y="42" font-size="12" class="g1">{esc(status)}</text>')
    b.append(f'<text x="24" y="84" font-size="22" class="b">{esc(title)}</text>')
    for i, line in enumerate(desc):
        assert len(line) <= 34, line
        b.append(f'<text x="24" y="{114 + i*20}" font-size="12.5" class="g1">{esc(line)}</text>')
    b.append(chips(tags, 24, CH_ - 50))
    b.append(art)
    write(fname, svg(CW_, CH_, title, alt, ".pl{animation:pulse 1.6s ease-in-out infinite}" + art_css, "".join(b)))

AX, AY = CW_ - 24 - 78, 118   # art centre

def art_aegis():
    cx, cy = AX, AY
    p = [f'<rect class="mar" x="{cx-66}" y="{cy-66}" width="132" height="132" fill="none" stroke="{G2}" stroke-dasharray="4 4"/>',
         f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{G3}"/>']
    for i in range(5):
        a = math.radians(-90 + i * 72)
        x, y = cx + 40 * math.cos(a), cy + 40 * math.sin(a)
        p.append(f'<circle class="nd" cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{BK}" stroke="{W}" stroke-width="1.5" style="animation-delay:{i:.0f}s"/>')
    p.append(f'<g class="orb" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy-40}" r="3" fill="{W}"/></g>')
    p.append(f'<text x="{cx}" y="{cy+4}" font-size="10" class="g2" text-anchor="middle">7B</text>')
    # packets from the outside world, stopped at the air gap
    for i, (sx, sy, ex) in enumerate([(cx+110, cy-30, cx+70), (cx+110, cy+22, cx+70), (cx-110, cy+40, cx-70)]):
        dx = ex - sx
        p.append(f'<circle class="pk" cx="{sx}" cy="{sy}" r="2.5" fill="{G1}" style="--dx:{dx}px;animation-delay:{i*0.9:.1f}s"/>')
    css = f"""
.mar{{animation:march 1.2s linear infinite}}
.orb{{animation:spin 5s linear infinite}}
.nd{{animation:nd 5s linear infinite}}
@keyframes nd{{0%,6%{{fill:{W}}}12%,100%{{fill:{BK}}}}}
.pk{{animation:pk 2.7s ease-in infinite}}
@keyframes pk{{0%{{transform:translateX(0);opacity:0}}15%{{opacity:1}}70%{{transform:translateX(var(--dx));opacity:1}}85%,100%{{transform:translateX(var(--dx));opacity:0}}}}
"""
    return "".join(p), css

def art_migrate():
    cx, cy = AX, AY
    p = [f'<text x="{cx-52}" y="{cy-58}" font-size="11" class="g2" text-anchor="middle">v1</text>',
         f'<text x="{cx+42}" y="{cy-58}" font-size="11" class="g2" text-anchor="middle">v2</text>',
         f'<path d="M{cx-9} {cy-6}l7 6-7 6" fill="none" stroke="{G1}" stroke-width="1.5"/>']
    widths = [44, 30, 52, 24, 40, 34]
    css = []
    period = 6.0
    for i, w in enumerate(widths):
        y = cy - 46 + i * 16
        p.append(f'<rect x="{cx-74}" y="{y}" width="{w}" height="6" rx="3" fill="{G2}"/>')
        s = (0.10 + i * 0.1) * 100
        e = s + 4
        css.append(f'@keyframes m{i}{{0%,{s:.0f}%{{fill:{G3}}}{e:.0f}%,88%{{fill:{W}}}96%,100%{{fill:{G3}}}}}'
                   f'.m{i}{{animation:m{i} {period}s linear infinite}}')
        p.append(f'<rect class="m{i}" x="{cx+20}" y="{y}" width="{w}" height="6" rx="3" fill="{G3}"/>')
    # scanner sweeping v1 while rewriting v2
    p.append(f'<rect class="scn" x="{cx-80}" y="{cy-50}" width="62" height="1.5" fill="{W}"/>')
    p.append(f'<g class="ok"><circle cx="{cx+40}" cy="{cy+62}" r="9" fill="none" stroke="{W}" stroke-width="1.5"/>'
             f'<path d="M{cx+35} {cy+62}l3.5 3.5 6-7" fill="none" stroke="{W}" stroke-width="1.5"/></g>')
    p.append(f'<text x="{cx-42}" y="{cy+66}" font-size="10" class="g2" text-anchor="middle">tests</text>')
    css.append(f"""
.scn{{animation:scn {period}s linear infinite}}
@keyframes scn{{0%,8%{{transform:translateY(0);opacity:0}}10%{{opacity:1}}70%{{transform:translateY(96px);opacity:1}}72%,100%{{transform:translateY(96px);opacity:0}}}}
.ok{{animation:ok {period}s linear infinite}}
@keyframes ok{{0%,74%{{opacity:0}}76%,90%{{opacity:1}}96%,100%{{opacity:0}}}}
""")
    return "".join(p), "".join(css)

def art_sonar():
    cx, cy = AX, AY
    p = []
    for r in (22, 44, 66):
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{G3}"/>')
    p.append(f'<path d="M{cx-72} {cy}H{cx+72}M{cx} {cy-72}V{cy+72}" stroke="{G3}"/>')
    wedge = []
    for k, op in enumerate([.30, .18, .10, .05]):
        a0 = math.radians(-90 - k * 10); a1 = math.radians(-90 - (k + 1) * 10)
        x0, y0 = cx + 66 * math.cos(a0), cy + 66 * math.sin(a0)
        x1, y1 = cx + 66 * math.cos(a1), cy + 66 * math.sin(a1)
        wedge.append(f'<path d="M{cx} {cy}L{x0:.1f} {y0:.1f}A66 66 0 0 0 {x1:.1f} {y1:.1f}Z" fill="{W}" fill-opacity="{op}"/>')
    p.append(f'<g class="sw" style="transform-origin:{cx}px {cy}px">{"".join(wedge)}<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-66}" stroke="{W}" stroke-width="1.5"/></g>')
    css = [".sw{animation:spin 4s linear infinite}"]
    for i, (ang, rad) in enumerate([(40, 50), (130, 30), (250, 58), (320, 36)]):
        a = math.radians(ang - 90)
        x, y = cx + rad * math.cos(a), cy + rad * math.sin(a)
        p.append(f'<circle class="bl" cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{W}" style="animation-delay:{ang/360*4:.2f}s"/>')
    css.append("@keyframes bl{0%{opacity:1}70%,100%{opacity:0}}.bl{opacity:0;animation:bl 4s linear infinite}")
    p.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{W}"/>')
    return "".join(p), "".join(css)

def art_arch():
    cx, cy = AX, AY + 18
    a = (30, 17); bb = (-30, 17); up = (0, -40)
    def P(i, j, k):  # i along a, j along b, k along up
        return (cx + i*a[0] + j*bb[0] + k*up[0], cy - 34 + i*a[1] + j*bb[1] + k*up[1] + 40)
    def pt(q): return f"{q[0]:.1f} {q[1]:.1f}"
    base = [P(0,0,0), P(1.6,0,0), P(1.6,1.4,0), P(0,1.4,0)]
    top = [P(0,0,1), P(1.6,0,1), P(1.6,1.4,1), P(0,1.4,1)]
    r1 = (P(0,0.7,1)[0], P(0,0.7,1)[1] - 30); r2 = (P(1.6,0.7,1)[0], P(1.6,0.7,1)[1] - 30)
    paths = [
        "M" + "L".join(pt(q) for q in base) + "Z",
        "".join(f"M{pt(base[i])}L{pt(top[i])}" for i in range(4)),
        "M" + "L".join(pt(q) for q in top) + "Z",
        f"M{pt(r1)}L{pt(r2)}M{pt(top[0])}L{pt(r1)}L{pt(top[3])}M{pt(top[1])}L{pt(r2)}L{pt(top[2])}",
        f"M{pt(P(0.5,1.4,0))}L{pt(P(0.5,1.4,0.55))}L{pt(P(0.9,1.4,0.55))}L{pt(P(0.9,1.4,0))}",
    ]
    p = []
    for i, d in enumerate(paths):
        p.append(f'<path class="dr" d="{d}" pathLength="1" fill="none" stroke="{W}" stroke-width="1.4" stroke-linejoin="round" style="animation-delay:{i*0.35:.2f}s"/>')
    # dimension line + cost tag
    y = cy + 62
    p.append(f'<g class="tag"><path d="M{cx-48} {y}H{cx+48}M{cx-48} {y-4}v8M{cx+48} {y-4}v8" stroke="{G1}"/>'
             f'<text x="{cx}" y="{y+16}" font-size="10.5" class="g1" text-anchor="middle">&#8377; itemised</text></g>')
    css = """
.dr{stroke-dasharray:1;stroke-dashoffset:1;animation:dr 7s cubic-bezier(.6,0,.3,1) infinite}
@keyframes dr{0%{stroke-dashoffset:1;opacity:1}25%,78%{stroke-dashoffset:0;opacity:1}90%,100%{stroke-dashoffset:0;opacity:0}}
.tag{animation:tg 7s linear infinite}
@keyframes tg{0%,40%{opacity:0}46%,78%{opacity:1}88%,100%{opacity:0}}
"""
    return "".join(p), css

def art_mlops():
    cx, cy = AX - 20, AY
    stages = ["data", "train", "track", "serve"]
    p = [f'<line x1="{cx}" y1="{cy-60}" x2="{cx}" y2="{cy+60}" stroke="{G3}" stroke-width="1.5"/>']
    for i, s in enumerate(stages):
        y = cy - 60 + i * 40
        p.append(f'<rect class="st" x="{cx-9}" y="{y-9}" width="18" height="18" fill="{BK}" stroke="{W}" stroke-width="1.5" style="animation-delay:{i*0.75:.2f}s"/>')
        p.append(f'<text x="{cx+22}" y="{y+4}" font-size="11" class="g1">{s}</text>')
    for i in range(2):
        p.append(f'<circle class="fw" cx="{cx}" cy="{cy-60}" r="3" fill="{W}" style="animation-delay:{i*1.5:.1f}s"/>')
    css = """
.fw{animation:fw 3s linear infinite}
@keyframes fw{0%{transform:translateY(0);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateY(120px);opacity:0}}
.st{animation:stp 3s linear infinite}
@keyframes stp{0%,10%{fill:#FFFFFF}22%,100%{fill:#000000}}
"""
    return "".join(p), css

def art_debug():
    cx, cy = AX, AY
    x0 = cx - 70
    widths = [96, 70, 118, 88, 60, 104, 76]
    p = []
    for i, w in enumerate(widths):
        y = cy - 54 + i * 16
        cls = "er" if i == 3 else ""
        p.append(f'<rect class="{cls}" x="{x0}" y="{y}" width="{w}" height="6" rx="3" fill="{G2 if i != 3 else G2}"/>')
    y3 = cy - 54 + 3 * 16
    p.append(f'<g class="pz"><rect x="{x0+96}" y="{y3-5}" width="30" height="16" rx="3" fill="{W}"/>'
             f'<text x="{x0+111}" y="{y3+7}" font-size="10.5" text-anchor="middle" style="fill:{BK}" class="b">P0</text></g>')
    p.append(f'<g class="fx"><path d="M{x0+100} {y3+3}l4 4 7-8" fill="none" stroke="{W}" stroke-width="1.8"/>'
             f'<text x="{x0+116}" y="{y3+7}" font-size="10.5" class="g1">fixed</text></g>')
    p.append(f'<rect class="cu" x="{x0}" y="{cy+62}" width="8" height="12" fill="{W}"/>')
    css = """
.er{animation:er 4s linear infinite}
@keyframes er{0%,15%{fill:#5C5C5C}18%,55%{fill:#FFFFFF}62%,100%{fill:#5C5C5C}}
.pz{animation:pz 4s linear infinite}
@keyframes pz{0%,18%{opacity:0}20%,55%{opacity:1}58%,100%{opacity:0}}
.fx{animation:fx 4s linear infinite}
@keyframes fx{0%,60%{opacity:0}63%,92%{opacity:1}97%,100%{opacity:0}}
.cu{animation:blink 1.06s step-end infinite}
"""
    return "".join(p), css

# ------------------------------------------------------------------ STACK
def stack():
    Wd = 960
    rows = [
        ("llm systems", ["LangGraph", "Ollama", "FAISS", "ChromaDB", "sentence-transformers", "Gemini API"]),
        ("ml + mlops", ["Python", "NumPy", "MLflow", "Docker", "GitHub Actions"]),
        ("backend", ["FastAPI", "Express", "PostgreSQL", "SQLite"]),
        ("frontend", ["TypeScript", "React", "Next.js", "Vite", "Streamlit"]),
        ("systems", ["Arch Linux", "Bash", "fish", "Git", "C++"]),
    ]
    H = 40 + len(rows) * 44 + 12
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>', crop_marks(8, 8, Wd - 16, H - 16, 10, G1)]
    period = len(rows) * 2.4
    css = [f".hl{{fill:{G2}}}.mk{{opacity:0}}", f".hl{{animation:hl {period}s linear infinite}}",
           f"@keyframes hl{{0%{{fill:{G2}}}3%,17%{{fill:{W}}}20%,100%{{fill:{G2}}}}}",
           f".mk{{animation:mk {period}s linear infinite}}",
           f"@keyframes mk{{0%{{opacity:0}}3%,17%{{opacity:1}}20%,100%{{opacity:0}}}}"]
    for i, (label, items) in enumerate(rows):
        y = 50 + i * 44
        d = i * 2.4
        b.append(f'<text class="mk" x="28" y="{y}" font-size="14" style="animation-delay:{d}s">&gt;</text>')
        b.append(f'<text class="hl" x="46" y="{y}" font-size="14" style="animation-delay:{d}s">{label}</text>')
        x = 250
        parts = []
        for j, it in enumerate(items):
            if j:
                parts.append(f'<tspan class="g2">  /  </tspan>')
            parts.append(f'<tspan>{esc(it)}</tspan>')
        b.append(f'<text x="{x}" y="{y}" font-size="14">{"".join(parts)}</text>')
        if i < len(rows) - 1:
            b.append(f'<line x1="28" x2="{Wd-28}" y1="{y+18}" y2="{y+18}" stroke="{G4}"/>')
    alt = "; ".join(f"{l}: {', '.join(it)}" for l, it in rows)
    write("stack.svg", svg(Wd, H, "Stack", alt, "".join(css), "".join(b)))

# ------------------------------------------------------------------ CONTACT BUTTONS
def button(fname, label, value, icon, delay):
    Wd, H = 232, 64
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>',
         f'<rect x=".5" y=".5" width="{Wd-1}" height="{H-1}" fill="none" stroke="{G2}"/>',
         f'<g transform="translate(18 22)" fill="none" stroke="{W}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{icon}</g>',
         f'<text x="54" y="27" font-size="11" class="g2">{label}</text>',
         f'<text x="54" y="45" font-size="{12 if len(value) <= 20 else 11}">{esc(value)}</text>',
         f'<clipPath id="c"><rect width="{Wd}" height="{H}"/></clipPath>',
         f'<g clip-path="url(#c)"><rect class="gl" x="-60" y="-10" width="26" height="{H+20}" fill="{W}" fill-opacity=".14" transform="skewX(-20)" style="animation-delay:{delay}s"/></g>']
    css = ".gl{animation:gl 7s ease-in-out infinite}@keyframes gl{0%{transform:skewX(-20deg) translateX(0)}18%,100%{transform:skewX(-20deg) translateX(340px)}}"
    write(fname, svg(Wd, H, f"{label}: {value}", f"{label}: {value}", css, "".join(b)))

ICONS = {
    "globe": '<circle cx="10" cy="10" r="9"/><ellipse cx="10" cy="10" rx="4" ry="9"/><path d="M1 10h18"/>',
    "in": '<rect x="1" y="1" width="18" height="18" rx="3"/><path d="M6 9v6M6 5.5v.1M10 15v-6M10 11.5c0-1.5 1-2.5 2.3-2.5S14.5 10 14.5 11.5V15"/>',
    "mail": '<rect x="1" y="3" width="18" height="14" rx="2"/><path d="M1.5 4l8.5 7 8.5-7"/>',
    "pad": '<rect x="1" y="5" width="18" height="11" rx="5"/><path d="M6 8.5v4M4 10.5h4"/><circle cx="13.5" cy="9.5" r=".6"/><circle cx="15.5" cy="11.8" r=".6"/>',
}

# ------------------------------------------------------------------ FOOTER
def footer():
    Wd, H = 960, 96
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>',
         f'<text x="24" y="40" font-size="15"><tspan class="b">srinivas@s10</tspan><tspan class="g1"> ~&gt; </tspan>exit</text>',
         f'<text x="24" y="66" font-size="13" class="g2">[process completed]</text>',
         f'<rect class="cu" x="{24 + 20*9:.0f}" y="54" width="9" height="15" fill="{W}"/>',
         f'<text x="{Wd-24}" y="66" font-size="12" class="g2" text-anchor="end">made in Bengaluru on Arch Linux</text>']
    write("footer.svg", svg(Wd, H, "exit", "srinivas@s10 exit. Process completed. Made in Bengaluru on Arch Linux.",
                            ".cu{animation:blink 1.06s step-end infinite}", "".join(b)))

if __name__ == "__main__":
    hero()
    for s, n in [("now", "in progress"), ("shipped", "finished and public"), ("stack", "tools I can defend in an interview"),
                 ("activity", "the last twelve months"), ("contact", "fastest reply: email")]:
        header(s, n)
    card("card-aegis.svg", "building / SIH 2026", True, "AEGIS",
         ["Air-gapped agentic AI workbench", "for Mangalore Refinery. Runs a", "7B model on a 4 GB laptop GPU."],
         ["LangGraph", "Ollama", "FAISS", "Docker"], *art_aegis(),
         "AEGIS: air-gapped agentic AI workbench for Mangalore Refinery, Smart India Hackathon 2026. Runs a 7B model on a 4 GB laptop GPU. LangGraph, Ollama, FAISS, Docker.")
    card("card-migration.svg", "building / REVA CAIML", True, "Migration Agent",
         ["An LLM agent that upgrades whole", "codebases across breaking version", "changes, then tests its own edits."],
         ["Python", "AST", "LLM agents", "Docker"], *art_migrate(),
         "Codebase migration agent: an LLM agent that upgrades whole codebases across breaking version changes and tests its own edits. Python, AST, Docker.")
    card("card-aquasentinel.svg", "shipped / live demo", False, "AquaSentinel",
         ["Mission control for an underwater", "inspection robot: telemetry, route", "planning, AI defect detection."],
         ["React 19", "TypeScript", "Express", "Postgres"], *art_sonar(),
         "AquaSentinel: mission control for an underwater inspection robot with telemetry, route planning and AI defect detection. Live demo at aqua-wheat.vercel.app.")
    card("card-archagent.svg", "shipped", False, "ArchAgent",
         ["A plain-language brief becomes 3D", "renders and an itemised INR cost", "estimate in under 60 seconds."],
         ["React", "TypeScript", "Gemini API"], *art_arch(),
         "ArchAgent: a plain-language building brief becomes 3D renders and an itemised INR cost estimate in under 60 seconds. React, TypeScript, Gemini.")
    card("card-mlops.svg", "shipped", False, "health-risk-mlops",
         ["A risk model taken to production", "shape: served, containerised,", "tracked, tested on every push."],
         ["FastAPI", "Docker", "MLflow", "Actions"], *art_mlops(),
         "health-risk-mlops: a health-risk model served by FastAPI, containerised with Docker, tracked in MLflow, tested by GitHub Actions.")
    card("card-debugext.svg", "shipped", False, "Debug.ext",
         ["Chrome extension that catches", "runtime errors, ranks them P0-P3,", "and drafts the fix."],
         ["Chrome MV3", "FastAPI", "Streamlit"], *art_debug(),
         "Debug.ext: Chrome extension that catches runtime errors, ranks them P0 to P3, and drafts the fix. FastAPI and Streamlit.")
    stack()
    button("btn-portfolio.svg", "portfolio", "srinivas-rc.is-a.dev", ICONS["globe"], 0)
    button("btn-linkedin.svg", "linkedin", "Srinivas R C", ICONS["in"], 0.5)
    button("btn-email.svg", "email", "srinivasrc0408@gmail.com", ICONS["mail"], 1.0)
    button("btn-steam.svg", "steam", "off the clock", ICONS["pad"], 1.5)
    footer()
