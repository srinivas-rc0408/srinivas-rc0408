"""S10 profile README generator: frosted-glass, monochrome, dark + light themes.
Run: python3 build.py   ->  assets/dark/*.svg, assets/light/*.svg, README.md"""
import math, random, os
from xml.sax.saxutils import escape as esc

MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono','Cascadia Mono','DejaVu Sans Mono',Menlo,Consolas,'Liberation Mono',monospace"

def rgba(hex_, a):
    h = hex_.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{a})"

THEMES = {
    "dark": dict(fg="#F0F3F6", fg2="#9198A1", fg3="#656C76", ink="#FFFFFF", solid="#12161D", inv="#0D1117",
                 glass=.035, line=.11, dim1=.30, dim2=.12, orb=.10, sheen=.06, sq=[.07, .28, .55, .82, 1.0]),
    "light": dict(fg="#1F2328", fg2="#59636E", fg3="#818B98", ink="#1F2328", solid="#F3F5F7", inv="#FFFFFF",
                  glass=.025, line=.13, dim1=.30, dim2=.11, orb=.035, sheen=.35, sq=[.07, .22, .45, .72, .92]),
}

class T:  # active theme accessor
    pass

def use(name):
    t = THEMES[name]
    for k, v in t.items(): setattr(T, k, v)
    T.name = name
    T.d1 = rgba(T.ink, T.dim1); T.d2 = rgba(T.ink, T.dim2)
    T.ln = rgba(T.ink, T.line)
    T.sqc = [rgba(T.ink, a) for a in T.sq]

def base_css():
    return f"""
text{{font-family:{MONO};fill:{T.fg}}}
.f2{{fill:{T.fg2}}} .f3{{fill:{T.fg3}}} .b{{font-weight:700}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes march{{to{{stroke-dashoffset:-16}}}}
@keyframes ring{{0%{{transform:scale(.6);opacity:.7}}100%{{transform:scale(2.4);opacity:0}}}}
"""
RM = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

def svg(w, h, title, desc, css, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<style>{base_css()}{css}{RM}</style>{body}</svg>')

def write(name, s):
    os.makedirs("assets", exist_ok=True)
    open(f"assets/{name}", "w").write(s)

def glass(w, h, r=16, orbs=(), drift=False, sheen=False):
    """Frosted panel: blurred light blobs behind a translucent pane, hairline border, top highlight."""
    o = [f'<defs><clipPath id="gc"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}"/></clipPath>'
         f'<filter id="bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="42"/></filter>'
         f'<linearGradient id="gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T.ink}" stop-opacity="{T.glass*2.2}"/>'
         f'<stop offset=".45" stop-color="{T.ink}" stop-opacity="{T.glass}"/><stop offset="1" stop-color="{T.ink}" stop-opacity="{T.glass*.6}"/></linearGradient>'
         f'<linearGradient id="gt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T.ink}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{T.ink}" stop-opacity="{.45 if T.name=="dark" else .25}"/><stop offset="1" stop-color="{T.ink}" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="#fff" stop-opacity="{T.sheen}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>',
         f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="#0D1117"/>',
         '<g clip-path="url(#gc)">']
    for i, (cx, cy, rr) in enumerate(orbs):
        cls = f' class="od{i%3}"' if drift else ""
        o.append(f'<circle{cls} cx="{cx}" cy="{cy}" r="{rr}" fill="{T.ink}" fill-opacity="{T.orb}" filter="url(#bl)"/>')
    o.append(f'<rect width="{w}" height="{h}" fill="url(#gv)"/>')
    if sheen:
        o.append(f'<rect class="sheen" x="-300" y="-40" width="220" height="{h+80}" fill="url(#sh)" transform="skewX(-18)"/>')
    o.append('</g>')
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{T.ln}"/>')
    o.append(f'<path d="M{r} .75H{w-r}" stroke="url(#gt)" stroke-width="1.2"/>')
    css = ""
    if drift:
        css += """
.od0{animation:d0 26s ease-in-out infinite}.od1{animation:d1 32s ease-in-out infinite}.od2{animation:d2 29s ease-in-out infinite}
@keyframes d0{50%{transform:translate(120px,40px)}}@keyframes d1{50%{transform:translate(-140px,-30px)}}@keyframes d2{50%{transform:translate(60px,-60px)}}
"""
    if sheen:
        css += f".sheen{{animation:sh 11s ease-in-out 3s infinite}}@keyframes sh{{0%{{transform:skewX(-18deg) translateX(0)}}22%,100%{{transform:skewX(-18deg) translateX({w+600}px)}}}}"
    return "".join(o), css

GLYPHS = {
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "1": ["..#..", ".##..", "#.#..", "..#..", "..#..", "..#..", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
}

# =================================================================== HERO
def hero():
    Wd, H = 960, 610
    FS, CW, LH = 15, 9.0, 23
    rnd = random.Random(1008)
    g, gcss = glass(Wd, H, 20, orbs=[(170, 220, 170), (820, 120, 150), (600, 560, 190)], drift=True, sheen=True)
    b = [g]
    # title bar
    b.append(f'<text x="{Wd/2}" y="27" font-size="12" class="f3" text-anchor="middle">fish  /  srinivas@s10  /  ~</text>')
    b.append(f'<path d="M1 42H{Wd-1}" stroke="{T.ln}"/>')
    tl = [("#FF8A80", "#E5372E", "#9E1B14"), ("#7BEA8E", "#25B347", "#14712B"), ("#8CC8FF", "#2D86E8", "#1752A3")]
    defs = "".join(f'<radialGradient id="tl{i}" cx=".38" cy=".3" r=".75"><stop offset="0" stop-color="{a}"/>'
                   f'<stop offset=".55" stop-color="{m}"/><stop offset="1" stop-color="{d}"/></radialGradient>' for i, (a, m, d) in enumerate(tl))
    b.append(f'<defs>{defs}</defs>')
    for i in range(3):
        cx = 30 + i * 26
        b.append(f'<circle cx="{cx}" cy="22" r="8" fill="url(#tl{i})"/>'
                 f'<circle cx="{cx}" cy="22" r="7.5" fill="none" stroke="#000" stroke-opacity=".35"/>'
                 f'<ellipse cx="{cx-1}" cy="18.6" rx="4.2" ry="2.2" fill="#fff" fill-opacity=".45"/>')
    b.append(f'<text x="{Wd-24}" y="27" font-size="11.5" class="f3" text-anchor="end">12.97&#176; N  77.59&#176; E</text>')
    PX = 44
    prompt = f'<tspan class="b">srinivas@s10</tspan><tspan class="f2"> ~&gt; </tspan>'
    PC = len("srinivas@s10 ~> ")
    y1 = 82
    b.append(f'<text x="{PX}" y="{y1}" font-size="{FS}">{prompt}</text>')
    cx0 = PX + PC * CW
    for i, ch in enumerate("fastfetch"):
        b.append(f'<text class="in" x="{cx0+i*CW:.1f}" y="{y1}" font-size="{FS}" style="animation-delay:{0.35+(i+1)*0.07:.2f}s">{ch}</text>')
    b.append(f'<rect class="cur1" x="{cx0:.1f}" y="{y1-13}" width="{CW}" height="17" rx="1.5" fill="{T.fg}"/>')

    cell, gap = 13, 4; pitch = cell + gap
    cols, rows = 19, 9
    gx, gy = PX, 132
    lit, c0 = set(), 1
    for gl in "S10":
        for r, row in enumerate(GLYPHS[gl]):
            for c, v in enumerate(row):
                if v == "#": lit.add((c0 + c, 1 + r))
        c0 += 6
    for c in range(cols):
        for r in range(rows):
            x, y = gx + c*pitch, gy + r*pitch
            d = 1.10 + c*0.034 + r*0.011
            if (c, r) in lit:
                col = rnd.choices(T.sqc[2:], [2, 3, 5])[0]
                b.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3.5" fill="{col}" style="animation-delay:{d:.3f}s"/>')
            else:
                near = any((c+dx, r+dy) in lit for dx in (-1,0,1) for dy in (-1,0,1))
                col = T.sqc[1] if (rnd.random() < 0.10 and not near) else T.sqc[0]
                cls = ' class="cell"' if col != T.sqc[0] else ""
                b.append(f'<rect{cls} x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3.5" fill="{col}" style="animation-delay:{d:.3f}s"/>')
    gw, gh = cols*pitch - gap, rows*pitch - gap
    ly = gy + gh + 26
    lx = gx + gw - 5*14 - 30
    b.append(f'<g class="in" style="animation-delay:1.95s"><text x="{lx-36}" y="{ly}" font-size="12" class="f3">Less</text>')
    for i, col in enumerate(T.sqc):
        b.append(f'<rect x="{lx+i*14}" y="{ly-10}" width="10" height="10" rx="2.5" fill="{col}"/>')
    b.append(f'<text x="{lx+5*14+4}" y="{ly}" font-size="12" class="f3">More</text></g>')
    b.append(f'<g class="in" style="animation-delay:2.05s">'
             f'<text x="{gx}" y="{ly+52}" font-size="28" class="b" letter-spacing=".5">Srinivas R C</text>'
             f'<text x="{gx}" y="{ly+78}" font-size="13" class="f2">AI engineer, Bengaluru</text>'
             f'<text x="{gx}" y="{ly+100}" font-size="13" class="f3">github.com/srinivas-rc0408</text></g>')

    RX, KW = 400, 10 * CW
    who = [("Role", "AI engineer intern, IIT Ropar (remote)"),
           ("Project", "Ajrasakha, multilingual farm assistant"),
           ("Building", "AEGIS, air-gapped AI workbench (SIH '26)"),
           ("Agent", "Codebase migration agent, REVA CAIML"),
           ("Degree", "B.Tech AI &amp; ML, REVA University '27")]
    rig = [("Focus", "RAG, LLM agents, offline inference"),
           ("Stack", "Python, TypeScript, LangGraph, FastAPI"),
           ("Models", "Qwen2.5, DeepSeek-R1, moondream2 (Ollama)"),
           ("Certs", "NPTEL Deep Learning, IIT Ropar"),
           ("Learning", "NPTEL AI Foundations, IIT Delhi"),
           ("Lead", "Head of Media, Yantra IoT Club"),
           ("Env", "Arch Linux, niri, fish + bash")]
    t0, st = 1.18, 0.07
    n = [0]
    def line(inner):
        b.append(f'<g class="in" style="animation-delay:{t0+n[0]*st:.3f}s">{inner}</g>'); n[0] += 1
    y = 132
    line(f'<text x="{RX}" y="{y}" font-size="{FS}" class="b">srinivas<tspan class="f3" style="font-weight:400">@</tspan>s10</text>')
    y += LH; line(f'<text x="{RX}" y="{y}" font-size="{FS}" class="f3">{"-"*12}</text>')
    def kv(y, k, v):
        line(f'<text x="{RX}" y="{y}" font-size="{FS}" class="f3">{k}</text><text x="{RX+KW:.0f}" y="{y}" font-size="{FS}">{v}</text>')
    for k, v in who:
        y += LH; kv(y, k, v)
    y += LH
    sx = RX + KW + 5
    line(f'<text x="{RX}" y="{y}" font-size="{FS}" class="f3">Status</text>'
         f'<circle class="rg" cx="{sx:.0f}" cy="{y-5}" r="4.5" fill="none" stroke="{T.fg}" style="transform-origin:{sx:.0f}px {y-5}px"/>'
         f'<circle cx="{sx:.0f}" cy="{y-5}" r="4" fill="{T.fg}"/>'
         f'<text x="{RX+KW+18:.0f}" y="{y}" font-size="{FS}">open to 2027 AI/ML roles</text>')
    y += LH * 0.9
    line(f'<path d="M{RX} {y-5:.0f}H{RX+KW+396:.0f}" stroke="{T.ln}"/>')
    y += LH * 0.3
    for k, v in rig:
        y += LH; kv(y, k, v)
    y += LH + 8
    line("".join(f'<rect x="{RX+i*30}" y="{y-12:.0f}" width="28" height="14" rx="3" fill="{rgba(T.ink, a)}"/>'
                 for i, a in enumerate([.06, .14, .24, .36, .5, .66, .82, 1])))
    tend = t0 + n[0] * st
    yb = H - 36
    b.append(f'<g class="in" style="animation-delay:{tend+0.15:.2f}s"><text x="{PX}" y="{yb}" font-size="{FS}">{prompt}</text></g>')
    cmd = "open srinivas-rc.is-a.dev"
    ts = tend + 0.45
    for i, ch in enumerate(cmd):
        b.append(f'<text class="in" x="{cx0+i*CW:.1f}" y="{yb}" font-size="{FS}" style="animation-delay:{ts+i*0.03:.2f}s">{esc(ch)}</text>')
    tdone = ts + len(cmd) * 0.03
    b.append(f'<g class="in" style="animation-delay:{tdone:.2f}s"><rect class="bl2" x="{cx0+len(cmd)*CW:.1f}" y="{yb-13}" width="{CW}" height="17" rx="1.5" fill="{T.fg}"/></g>')
    pw, ph = 252, 36
    px, py = Wd - 40 - pw, yb - 24
    bx, by = px + pw - 70, py + ph / 2          # click point on the button
    b.append(f'<defs><linearGradient id="btn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/>'
             f'<stop offset="1" stop-color="#fff" stop-opacity=".05"/></linearGradient>'
             f'<linearGradient id="bsh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="bc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="{ph/2}"/></clipPath></defs>')
    b.append(f'<g class="in" style="animation-delay:{tdone+0.1:.2f}s">'
             f'<g class="press" style="transform-origin:{px+pw/2}px {py+ph/2}px">'
             f'<rect x="{px}" y="{py+2}" width="{pw}" height="{ph}" rx="{ph/2}" fill="#000" fill-opacity=".35"/>'
             f'<rect class="cta" x="{px}" y="{py}" width="{pw}" height="{ph}" rx="{ph/2}" fill="url(#btn)" stroke="#fff" stroke-opacity=".32"/>'
             f'<path d="M{px+ph/2} {py+.8}H{px+pw-ph/2}" stroke="#fff" stroke-opacity=".45"/>'
             f'<g clip-path="url(#bc)"><rect class="bshine" x="{px-80}" y="{py-4}" width="50" height="{ph+8}" fill="url(#bsh)" style="transform-origin:{px-55}px {py+ph/2}px"/>'
             f'<circle class="rip" cx="{bx}" cy="{by}" r="40" fill="#fff" style="transform-origin:{bx}px {by}px"/></g>'
             f'<circle class="rg" cx="{px+20}" cy="{py+ph/2}" r="4" fill="none" stroke="{T.fg}" style="transform-origin:{px+20}px {py+ph/2}px"/>'
             f'<circle cx="{px+20}" cy="{py+ph/2}" r="3.4" fill="{T.fg}"/>'
             f'<text x="{px+34}" y="{py+ph/2+4.5}" font-size="12.5" class="b">click to open portfolio</text>'
             f'<path d="M{px+pw-28} {py+ph/2+4}l7-7M{px+pw-26} {py+ph/2-3}h5v5" fill="none" stroke="{T.fg}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
             f'</g></g>')
    # mouse pointer (classic arrow) that glides in and clicks
    arrow = "M0 0L0 17L4.6 12.8L7.6 19.4L10.4 18.2L7.5 11.8L13.4 11.6Z"
    b.append(f'<g class="ptr" style="--sx:{70}px;--sy:{60}px">'
             f'<g transform="translate({bx-2} {by-3})"><g class="ptrc"><path d="{arrow}" fill="#fff" stroke="#0D1117" stroke-width="1.3" stroke-linejoin="round"/></g></g></g>')
    T_CTA = tdone + 0.8
    css = gcss + f"""
.in{{animation:show 0s step-end both}}
.cell{{animation:lit .4s cubic-bezier(.2,.7,.2,1) both}}
@keyframes lit{{from{{fill:{T.sqc[0]}}}}}
.cur1{{animation:type .63s steps(9,end) .35s both, hide 0s step-end 1.02s both}}
@keyframes type{{from{{transform:translateX(0)}}to{{transform:translateX({9*CW}px)}}}}
@keyframes hide{{from{{opacity:1}}to{{opacity:0}}}}
.bl2{{animation:blink 1.06s step-end infinite}}
.cta{{animation:cta 7s ease-in-out {T_CTA:.2f}s infinite}}
@keyframes cta{{0%,40%,70%,100%{{stroke-opacity:.32}}46%,56%{{stroke-opacity:.85}}}}
.press{{animation:press 7s cubic-bezier(.3,0,.3,1) {T_CTA:.2f}s infinite}}
@keyframes press{{0%,44%{{transform:scale(1)}}47%{{transform:scale(.955)}}53%,100%{{transform:scale(1)}}}}
.bshine{{animation:bsh 7s ease-in-out {T_CTA:.2f}s infinite}}
@keyframes bsh{{0%,8%{{transform:skewX(-20deg) translateX(0)}}26%,100%{{transform:skewX(-20deg) translateX({pw+160}px)}}}}
.rip{{opacity:0;animation:rip 7s ease-out {T_CTA:.2f}s infinite}}
@keyframes rip{{0%,46%{{transform:scale(0);opacity:0}}47%{{transform:scale(.05);opacity:.35}}66%{{transform:scale(1.6);opacity:0}}100%{{opacity:0}}}}
.ptr{{opacity:0;animation:ptr 7s cubic-bezier(.45,0,.2,1) {T_CTA:.2f}s infinite}}
@keyframes ptr{{0%,10%{{transform:translate(var(--sx),var(--sy));opacity:0}}16%{{opacity:1}}40%,58%{{transform:translate(0,0);opacity:1}}74%,100%{{transform:translate(-14px,22px);opacity:0}}}}
.ptrc{{animation:ptrc 7s ease-in-out {T_CTA:.2f}s infinite}}
@keyframes ptrc{{0%,44%{{transform:scale(1)}}47%{{transform:scale(.82)}}53%,100%{{transform:scale(1)}}}}
.rg{{animation:ring 2.2s cubic-bezier(.2,.6,.3,1) infinite}}
@media (prefers-reduced-motion:reduce){{.cur1,.ptr{{display:none}}}}
"""
    alt = ("Terminal running fastfetch. S10 drawn in contribution squares. Srinivas R C, AI engineer intern at IIT Ropar (remote) "
           "working on Ajrasakha. Building AEGIS for SIH 2026 and a codebase migration agent at REVA CAIML. "
           "B.Tech AI and ML, REVA University 2027. Open to 2027 AI/ML roles. Click to open the portfolio at srinivas-rc.is-a.dev.")
    write("hero.svg", svg(Wd, H, "srinivas@s10 fastfetch", alt, css, "".join(b)))
    return alt

# =================================================================== HEADERS (no box)
def header(slug, note):
    Wd, H = 960, 60
    tw = (2 + len(slug)) * 13.2
    b = [f'<rect width="{Wd}" height="{H}" rx="10" fill="#0D1117"/>', f'<text x="16" y="38" font-size="22" class="b">~/{slug}</text>',
         f'<rect class="cu" x="{16+tw+6:.1f}" y="21" width="11" height="20" rx="1.5" fill="{T.fg}"/>',
         f'<path d="M{16+tw+32:.1f} 31H{Wd-16-len(note)*7.8-18:.1f}" stroke="{T.ln}"/>',
         f'<text x="{Wd-16}" y="36" font-size="13" class="f3" text-anchor="end">{esc(note)}</text>']
    write(f"h-{slug}.svg", svg(Wd, H, f"~/{slug}", note, ".cu{animation:blink 1.06s step-end infinite}", "".join(b)))

# =================================================================== CARDS
def chips(tags, x, y):
    out, cx = [], x
    for t in tags:
        w = len(t) * 6.3 + 18
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" fill="{rgba(T.ink, .04)}" stroke="{T.ln}"/>'
                   f'<text x="{cx + w/2:.1f}" y="{y+15}" font-size="10.5" class="f2" text-anchor="middle">{esc(t)}</text>')
        cx += w + 6
    return "".join(out)

def status(label, live):
    if live:
        return (f'<circle class="rg" cx="30" cy="36" r="4" fill="none" stroke="{T.fg}" style="transform-origin:30px 36px"/>'
                f'<circle cx="30" cy="36" r="3.6" fill="{T.fg}"/><text x="42" y="40" font-size="12" class="f2">{esc(label)}</text>')
    return f'<circle cx="30" cy="36" r="3.4" fill="none" stroke="{T.fg2}"/><text x="42" y="40" font-size="12" class="f2">{esc(label)}</text>'

def card(fname, stat, live, title, desc, tags, artfn, alt, Wd=470, H=262, maxc=34):
    g, gcss = glass(Wd, H, 16, orbs=[(Wd - 90, 60, 110)])
    b = [g, status(stat, live), f'<text x="24" y="82" font-size="22" class="b">{esc(title)}</text>']
    for i, line in enumerate(desc):
        assert len(line) <= maxc, line
        b.append(f'<text x="24" y="{112 + i*20}" font-size="12.5" class="f2">{esc(line)}</text>')
    b.append(chips(tags, 24, H - 48))
    art, acss = artfn()
    b.append(art)
    write(fname, svg(Wd, H, title, alt, gcss + ".rg{animation:ring 2.2s cubic-bezier(.2,.6,.3,1) infinite}" + acss, "".join(b)))

AX, AY = 470 - 24 - 78, 116

def art_aegis():
    cx, cy = AX, AY
    p = [f'<rect class="mar" x="{cx-66}" y="{cy-66}" width="132" height="132" rx="10" fill="none" stroke="{T.d1}" stroke-dasharray="4 4"/>',
         f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{T.d2}"/>']
    for i in range(5):
        a = math.radians(-90 + i * 72)
        x, y = cx + 40 * math.cos(a), cy + 40 * math.sin(a)
        p.append(f'<circle class="nd" cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{T.solid}" stroke="{T.fg}" stroke-width="1.5" style="animation-delay:{i}s"/>')
    p.append(f'<g class="orb" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy-40}" r="3" fill="{T.fg}"/></g>')
    p.append(f'<text x="{cx}" y="{cy+4}" font-size="10" class="f3" text-anchor="middle">7B</text>')
    for i, (sx, sy, ex) in enumerate([(cx+110, cy-30, cx+70), (cx+110, cy+22, cx+70), (cx-110, cy+40, cx-70)]):
        p.append(f'<circle class="pk" cx="{sx}" cy="{sy}" r="2.5" fill="{T.fg2}" style="--dx:{ex-sx}px;animation-delay:{i*0.9:.1f}s"/>')
    css = f"""
.mar{{animation:march 1.2s linear infinite}}.orb{{animation:spin 5s linear infinite}}
.nd{{animation:nd 5s linear infinite}}@keyframes nd{{0%,6%{{fill:{T.fg}}}12%,100%{{fill:{T.solid}}}}}
.pk{{animation:pk 2.7s ease-in infinite}}
@keyframes pk{{0%{{transform:translateX(0);opacity:0}}15%{{opacity:1}}70%{{transform:translateX(var(--dx));opacity:1}}85%,100%{{transform:translateX(var(--dx));opacity:0}}}}"""
    return "".join(p), css

def art_migrate():
    cx, cy = AX, AY
    p = [f'<text x="{cx-52}" y="{cy-58}" font-size="11" class="f3" text-anchor="middle">v1</text>',
         f'<text x="{cx+42}" y="{cy-58}" font-size="11" class="f3" text-anchor="middle">v2</text>',
         f'<path d="M{cx-9} {cy-6}l7 6-7 6" fill="none" stroke="{T.fg2}" stroke-width="1.5" stroke-linecap="round"/>']
    css, period = [], 6.0
    for i, w in enumerate([44, 30, 52, 24, 40, 34]):
        y = cy - 46 + i * 16
        p.append(f'<rect x="{cx-74}" y="{y}" width="{w}" height="6" rx="3" fill="{T.d1}"/>')
        s = (0.10 + i * 0.1) * 100
        css.append(f'@keyframes m{i}{{0%,{s:.0f}%{{fill:{T.d2}}}{s+4:.0f}%,88%{{fill:{T.fg}}}96%,100%{{fill:{T.d2}}}}}.m{i}{{animation:m{i} {period}s linear infinite}}')
        p.append(f'<rect class="m{i}" x="{cx+20}" y="{y}" width="{w}" height="6" rx="3" fill="{T.d2}"/>')
    p.append(f'<rect class="scn" x="{cx-80}" y="{cy-50}" width="62" height="1.5" rx=".75" fill="{T.fg}"/>')
    p.append(f'<g class="ok"><circle cx="{cx+40}" cy="{cy+62}" r="9" fill="none" stroke="{T.fg}" stroke-width="1.5"/>'
             f'<path d="M{cx+35} {cy+62}l3.5 3.5 6-7" fill="none" stroke="{T.fg}" stroke-width="1.5" stroke-linecap="round"/></g>')
    p.append(f'<text x="{cx-42}" y="{cy+66}" font-size="10" class="f3" text-anchor="middle">tests</text>')
    css.append(f""".scn{{animation:scn {period}s linear infinite}}
@keyframes scn{{0%,8%{{transform:translateY(0);opacity:0}}10%{{opacity:1}}70%{{transform:translateY(96px);opacity:1}}72%,100%{{transform:translateY(96px);opacity:0}}}}
.ok{{animation:ok {period}s linear infinite}}@keyframes ok{{0%,74%{{opacity:0}}76%,90%{{opacity:1}}96%,100%{{opacity:0}}}}""")
    return "".join(p), "".join(css)

def art_sonar():
    cx, cy = AX, AY
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{T.d2}"/>' for r in (22, 44, 66)]
    p.append(f'<path d="M{cx-72} {cy}H{cx+72}M{cx} {cy-72}V{cy+72}" stroke="{T.d2}"/>')
    wedge = []
    for k, op in enumerate([.30, .18, .10, .05]):
        a0, a1 = math.radians(-90 - k*10), math.radians(-90 - (k+1)*10)
        wedge.append(f'<path d="M{cx} {cy}L{cx+66*math.cos(a0):.1f} {cy+66*math.sin(a0):.1f}A66 66 0 0 0 {cx+66*math.cos(a1):.1f} {cy+66*math.sin(a1):.1f}Z" fill="{T.ink}" fill-opacity="{op}"/>')
    p.append(f'<g class="sw" style="transform-origin:{cx}px {cy}px">{"".join(wedge)}<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-66}" stroke="{T.fg}" stroke-width="1.5"/></g>')
    for ang, rad in [(40, 50), (130, 30), (250, 58), (320, 36)]:
        a = math.radians(ang - 90)
        p.append(f'<circle class="bp" cx="{cx+rad*math.cos(a):.1f}" cy="{cy+rad*math.sin(a):.1f}" r="3.2" fill="{T.fg}" style="animation-delay:{ang/360*4:.2f}s"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{T.fg}"/>')
    return "".join(p), ".sw{animation:spin 4s linear infinite}@keyframes bp{0%{opacity:1}70%,100%{opacity:0}}.bp{opacity:0;animation:bp 4s linear infinite}"

def art_arch():
    cx, cy = AX, AY + 18
    a, bb, up = (30, 17), (-30, 17), (0, -40)
    P = lambda i, j, k: (cx + i*a[0] + j*bb[0] + k*up[0], cy + 6 + i*a[1] + j*bb[1] + k*up[1])
    pt = lambda q: f"{q[0]:.1f} {q[1]:.1f}"
    base = [P(0,0,0), P(1.6,0,0), P(1.6,1.4,0), P(0,1.4,0)]
    top = [P(0,0,1), P(1.6,0,1), P(1.6,1.4,1), P(0,1.4,1)]
    r1 = (P(0,.7,1)[0], P(0,.7,1)[1]-30); r2 = (P(1.6,.7,1)[0], P(1.6,.7,1)[1]-30)
    paths = ["M" + "L".join(map(pt, base)) + "Z", "".join(f"M{pt(base[i])}L{pt(top[i])}" for i in range(4)),
             "M" + "L".join(map(pt, top)) + "Z",
             f"M{pt(r1)}L{pt(r2)}M{pt(top[0])}L{pt(r1)}L{pt(top[3])}M{pt(top[1])}L{pt(r2)}L{pt(top[2])}",
             f"M{pt(P(.5,1.4,0))}L{pt(P(.5,1.4,.55))}L{pt(P(.9,1.4,.55))}L{pt(P(.9,1.4,0))}"]
    p = [f'<path class="dr" d="{d}" pathLength="1" fill="none" stroke="{T.fg}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round" style="animation-delay:{i*.35:.2f}s"/>' for i, d in enumerate(paths)]
    y = cy + 62
    p.append(f'<g class="tag"><path d="M{cx-48} {y}H{cx+48}M{cx-48} {y-4}v8M{cx+48} {y-4}v8" stroke="{T.fg2}"/>'
             f'<text x="{cx}" y="{y+16}" font-size="10.5" class="f2" text-anchor="middle">&#8377; itemised</text></g>')
    return "".join(p), """.dr{stroke-dasharray:1;stroke-dashoffset:1;animation:dr 7s cubic-bezier(.6,0,.3,1) infinite}
@keyframes dr{0%{stroke-dashoffset:1;opacity:1}25%,78%{stroke-dashoffset:0;opacity:1}90%,100%{stroke-dashoffset:0;opacity:0}}
.tag{animation:tg 7s linear infinite}@keyframes tg{0%,40%{opacity:0}46%,78%{opacity:1}88%,100%{opacity:0}}"""

def art_mlops():
    cx, cy = AX - 20, AY
    p = [f'<line x1="{cx}" y1="{cy-60}" x2="{cx}" y2="{cy+60}" stroke="{T.d2}" stroke-width="1.5"/>']
    for i, s in enumerate(["data", "train", "track", "serve"]):
        y = cy - 60 + i * 40
        p.append(f'<rect class="st" x="{cx-9}" y="{y-9}" width="18" height="18" rx="4" fill="{T.solid}" stroke="{T.fg}" stroke-width="1.5" style="animation-delay:{i*.75:.2f}s"/>')
        p.append(f'<text x="{cx+22}" y="{y+4}" font-size="11" class="f2">{s}</text>')
    for i in range(2):
        p.append(f'<circle class="fw" cx="{cx}" cy="{cy-60}" r="3" fill="{T.fg}" style="animation-delay:{i*1.5:.1f}s"/>')
    return "".join(p), f""".fw{{animation:fw 3s linear infinite}}
@keyframes fw{{0%{{transform:translateY(0);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateY(120px);opacity:0}}}}
.st{{animation:stp 3s linear infinite}}@keyframes stp{{0%,10%{{fill:{T.fg}}}22%,100%{{fill:{T.solid}}}}}"""

def art_debug():
    cx, cy = AX, AY
    x0 = cx - 70
    p = []
    for i, w in enumerate([96, 70, 118, 88, 60, 104, 76]):
        p.append(f'<rect{" class=er" if i == 3 else ""} x="{x0}" y="{cy-54+i*16}" width="{w}" height="6" rx="3" fill="{T.d1}"/>'.replace("class=er", 'class="er"'))
    y3 = cy - 54 + 48
    p.append(f'<g class="pz"><rect x="{x0+96}" y="{y3-5}" width="30" height="16" rx="4" fill="{T.fg}"/>'
             f'<text x="{x0+111}" y="{y3+7}" font-size="10.5" text-anchor="middle" style="fill:{T.inv}" class="b">P0</text></g>')
    p.append(f'<g class="fx"><path d="M{x0+100} {y3+3}l4 4 7-8" fill="none" stroke="{T.fg}" stroke-width="1.8" stroke-linecap="round"/>'
             f'<text x="{x0+116}" y="{y3+7}" font-size="10.5" class="f2">fixed</text></g>')
    p.append(f'<rect class="cu" x="{x0}" y="{cy+62}" width="8" height="12" rx="1" fill="{T.fg}"/>')
    return "".join(p), f""".er{{animation:er 4s linear infinite}}@keyframes er{{0%,15%{{fill:{T.d1}}}18%,55%{{fill:{T.fg}}}62%,100%{{fill:{T.d1}}}}}
.pz{{animation:pz 4s linear infinite}}@keyframes pz{{0%,18%{{opacity:0}}20%,55%{{opacity:1}}58%,100%{{opacity:0}}}}
.fx{{animation:fx 4s linear infinite}}@keyframes fx{{0%,60%{{opacity:0}}63%,92%{{opacity:1}}97%,100%{{opacity:0}}}}
.cu{{animation:blink 1.06s step-end infinite}}"""

def art_ajrasakha():
    x0, bw, bh = 680, 250, 28
    tiers = [(66, "golden dataset", "verified"), (116, "package of practices", "verified"), (166, "general LLM", "fallback")]
    p = [f'<line x1="{x0+bw/2}" y1="30" x2="{x0+bw/2}" y2="{tiers[-1][0]}" stroke="{T.d1}" stroke-dasharray="2 4"/>']
    for i, (ty, label, k) in enumerate(tiers):
        dash = ' stroke-dasharray="4 3"' if i == 2 else ""
        p.append(f'<rect class="t{i}" x="{x0}" y="{ty}" width="{bw}" height="{bh}" rx="8" fill="{rgba(T.ink,.04)}" stroke="{T.fg}" stroke-opacity=".7" stroke-width="1.2"{dash}/>')
        p.append(f'<text class="l{i}" x="{x0+14}" y="{ty+18.5}" font-size="12">{label}</text>')
        p.append(f'<text class="l{i} k" x="{x0+bw-14}" y="{ty+18.5}" font-size="12" text-anchor="end">{k}</text>')
    p.append(f'<circle class="q" cx="{x0+bw/2}" cy="34" r="5" fill="{T.fg}"/>')
    p.append(f'<text x="{x0+bw/2}" y="{tiers[-1][0]+bh+26}" font-size="11" class="f3" text-anchor="middle">verified knowledge first, LLM last</text>')
    s1, s2, s3 = [ty - 41 for ty, *_ in tiers]
    off, on = rgba(T.ink, .04), T.fg
    return "".join(p), f"""
.q{{animation:q 9s cubic-bezier(.5,0,.5,1) infinite}}
@keyframes q{{0%{{transform:translateY(0);opacity:0}}3%{{transform:translateY(0);opacity:1}}10%,28%{{transform:translateY({s1}px);opacity:1}}31%{{transform:translateY({s1}px);opacity:0}}
33.3%{{transform:translateY(0);opacity:0}}36%{{transform:translateY(0);opacity:1}}43%{{transform:translateY({s1}px)}}50%,61%{{transform:translateY({s2}px);opacity:1}}64%{{transform:translateY({s2}px);opacity:0}}
66.6%{{transform:translateY(0);opacity:0}}69%{{transform:translateY(0);opacity:1}}76%{{transform:translateY({s1}px)}}83%{{transform:translateY({s2}px)}}90%,97%{{transform:translateY({s3}px);opacity:1}}100%{{transform:translateY({s3}px);opacity:0}}}}
.t0{{animation:t0 9s linear infinite}}@keyframes t0{{0%,10%{{fill:{off}}}11%,28%{{fill:{on}}}30%,100%{{fill:{off}}}}}
.t1{{animation:t1 9s linear infinite}}@keyframes t1{{0%,50%{{fill:{off}}}51%,61%{{fill:{on}}}63%,100%{{fill:{off}}}}}
.t2{{animation:t2 9s linear infinite}}@keyframes t2{{0%,90%{{fill:{off}}}91%,97%{{fill:{on}}}99%,100%{{fill:{off}}}}}
.l0{{animation:x0 9s linear infinite}}@keyframes x0{{0%,10%{{fill:{T.fg}}}11%,28%{{fill:{T.inv}}}30%,100%{{fill:{T.fg}}}}}
.l1{{animation:x1 9s linear infinite}}@keyframes x1{{0%,50%{{fill:{T.fg}}}51%,61%{{fill:{T.inv}}}63%,100%{{fill:{T.fg}}}}}
.l2{{animation:x2 9s linear infinite}}@keyframes x2{{0%,90%{{fill:{T.fg}}}91%,97%{{fill:{T.inv}}}99%,100%{{fill:{T.fg}}}}}
.k{{opacity:.6}}"""


# =================================================================== EXPERIENCE
EXPERIENCE = [
    dict(role="AI Engineer Intern", org="IIT Ropar", when="now", where="remote", live=True,
         line="Ajrasakha: a multilingual farm assistant. Expert-verified answers first, local LLMs as fallback.",
         tags=["RAG", "MongoDB vector search", "Sarvam AI", "Ollama"]),
    dict(role="Intern", org="REVA Center for AI & ML", when="now", where="Bengaluru", live=True,
         line="Building an LLM agent that migrates whole codebases across breaking version changes.",
         tags=["LLM agents", "AST", "Docker"]),
    dict(role="Team Alpha", org="Smart India Hackathon 2026", when="2026", where="PS SIH26117", live=False,
         line="AEGIS: an air-gapped agentic AI workbench for Mangalore Refinery, running on a 4 GB GPU.",
         tags=["LangGraph", "FAISS", "Qwen2.5-7B"]),
    dict(role="Head of Media", org="Yantra IoT Club, REVA", when="core member", where="Bengaluru", live=False,
         line="Runs media for the university's IoT club.", tags=[]),
]

def experience():
    Wd = 960
    rowh = 96
    H = 30 + len(EXPERIENCE) * rowh - 4
    g, gcss = glass(Wd, H, 16, orbs=[(Wd - 80, 10, 130), (60, H, 120)])
    b = [g]
    lx = 46
    y0 = 52
    yl = y0 + (len(EXPERIENCE) - 1) * rowh
    b.append(f'<path d="M{lx} {y0}V{yl}" stroke="{T.d2}" stroke-width="1.5"/>')
    b.append(f'<rect class="tr" x="{lx-1}" y="{y0}" width="2" height="34" rx="1" fill="{T.fg}"/>')
    for i, e in enumerate(EXPERIENCE):
        y = y0 + i * rowh
        if e["live"]:
            b.append(f'<circle class="rg" cx="{lx}" cy="{y}" r="5" fill="none" stroke="{T.fg}" style="transform-origin:{lx}px {y}px;animation-delay:{i*.4}s"/>'
                     f'<circle cx="{lx}" cy="{y}" r="5" fill="{T.fg}"/>')
        else:
            b.append(f'<circle cx="{lx}" cy="{y}" r="5" fill="#10151D" stroke="{T.fg2}" stroke-width="1.5"/>')
        tx = 74
        rw = len(e["role"]) * 9.6
        b.append(f'<text x="{tx}" y="{y+5}" font-size="16" class="b">{esc(e["role"])}</text>'
                 f'<text x="{tx+rw+10:.0f}" y="{y+5}" font-size="13" class="f2">{esc(e["org"])}</text>')
        pill = f'{e["when"]}  /  {e["where"]}'
        pw = len(pill) * 7.2 + 26
        px = Wd - 28 - pw
        fill = 'fill="#fff" fill-opacity=".09"' if e["live"] else 'fill="none"'
        b.append(f'<rect x="{px:.0f}" y="{y-11}" width="{pw:.0f}" height="22" rx="11" {fill} stroke="{T.ln}"/>'
                 f'<text x="{px+pw/2:.0f}" y="{y+4}" font-size="11.5" class="{"" if e["live"] else "f2"}" text-anchor="middle">{esc(pill)}</text>')
        assert len(e["line"]) <= 100, e["line"]
        b.append(f'<text x="{tx}" y="{y+28}" font-size="12.5" class="f2">{esc(e["line"])}</text>')
        cx = tx
        for t in e["tags"]:
            w = len(t) * 6 + 18
            b.append(f'<rect x="{cx:.0f}" y="{y+42}" width="{w:.0f}" height="20" rx="10" fill="#fff" fill-opacity=".04" stroke="{T.ln}"/>'
                     f'<text x="{cx+w/2:.0f}" y="{y+55.5}" font-size="10" class="f2" text-anchor="middle">{esc(t)}</text>')
            cx += w + 6
    css = gcss + f""".rg{{animation:ring 2.2s cubic-bezier(.2,.6,.3,1) infinite}}
.tr{{animation:tr 5s cubic-bezier(.45,0,.55,1) infinite}}
@keyframes tr{{0%{{transform:translateY(0);opacity:0}}10%{{opacity:.9}}85%{{opacity:.9}}100%{{transform:translateY({yl-y0-34}px);opacity:0}}}}"""
    alt = "Experience. " + " ".join(f'{e["role"]}, {e["org"]} ({e["when"]}, {e["where"]}): {e["line"]}' for e in EXPERIENCE)
    write("experience.svg", svg(Wd, H, "Experience", alt, css, "".join(b)))
    return alt

# =================================================================== STACK
STACK = [("llm systems", ["LangGraph", "Ollama", "FAISS", "ChromaDB", "sentence-transformers", "Gemini API"]),
         ("ml + mlops", ["Python", "NumPy", "MLflow", "Docker", "GitHub Actions"]),
         ("backend", ["FastAPI", "Express", "PostgreSQL", "MongoDB", "SQLite"]),
         ("frontend", ["TypeScript", "React", "Next.js", "Vite", "Streamlit"]),
         ("systems", ["Arch Linux", "Bash", "fish", "Git", "C++"])]
def stack():
    Wd = 960
    H = 34 + len(STACK) * 44 + 8
    g, gcss = glass(Wd, H, 16, orbs=[(140, 30, 110)])
    b = [g]
    period = len(STACK) * 2.4
    css = [gcss, f".hl{{fill:{T.fg3}}}.mk{{opacity:0}}.hl{{animation:hl {period}s linear infinite}}",
           f"@keyframes hl{{0%{{fill:{T.fg3}}}3%,17%{{fill:{T.fg}}}20%,100%{{fill:{T.fg3}}}}}",
           f".mk{{animation:mk {period}s linear infinite}}@keyframes mk{{0%{{opacity:0}}3%,17%{{opacity:1}}20%,100%{{opacity:0}}}}"]
    for i, (label, items) in enumerate(STACK):
        y = 44 + i * 44
        d = i * 2.4
        b.append(f'<text class="mk" x="28" y="{y}" font-size="14" style="animation-delay:{d}s">&gt;</text>')
        b.append(f'<text class="hl" x="46" y="{y}" font-size="14" style="animation-delay:{d}s">{label}</text>')
        parts = []
        for j, it in enumerate(items):
            if j: parts.append('<tspan class="f3">  /  </tspan>')
            parts.append(f'<tspan>{esc(it)}</tspan>')
        b.append(f'<text x="250" y="{y}" font-size="14">{"".join(parts)}</text>')
        if i < len(STACK) - 1:
            b.append(f'<path d="M28 {y+18}H{Wd-28}" stroke="{rgba(T.ink, .06)}"/>')
    alt = "; ".join(f"{l}: {', '.join(it)}" for l, it in STACK)
    write("stack.svg", svg(Wd, H, "Stack", alt, "".join(css), "".join(b)))
    return alt

# =================================================================== CONTACT
ICONS = {
    "globe": '<circle cx="10" cy="10" r="9"/><ellipse cx="10" cy="10" rx="4" ry="9"/><path d="M1 10h18"/>',
    "in": '<rect x="1" y="1" width="18" height="18" rx="4"/><path d="M6 9v6M6 5.5v.1M10 15v-6M10 11.5c0-1.5 1-2.5 2.3-2.5S14.5 10 14.5 11.5V15"/>',
    "mail": '<rect x="1" y="3" width="18" height="14" rx="3"/><path d="M1.5 4.5l8.5 6.5 8.5-6.5"/>',
    "pad": '<rect x="1" y="5" width="18" height="11" rx="5.5"/><path d="M6 8.5v4M4 10.5h4"/><circle cx="13.5" cy="9.5" r=".6"/><circle cx="15.5" cy="11.8" r=".6"/>',
}
def button(fname, label, value, icon, delay):
    Wd, H = 232, 64
    g, gcss = glass(Wd, H, 14, orbs=[(40, 32, 50)])
    fs = 12 if len(value) <= 20 else 11
    b = [g,
         f'<g transform="translate(18 22)" fill="none" stroke="{T.fg}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{icon}</g>',
         f'<text x="54" y="27" font-size="11" class="f3">{label}</text>',
         f'<text x="54" y="45" font-size="{fs}">{esc(value)}</text>',
         f'<clipPath id="cc"><rect x="1" y="1" width="{Wd-2}" height="{H-2}" rx="14"/></clipPath>',
         f'<g clip-path="url(#cc)"><rect class="gl" x="-70" y="-10" width="30" height="{H+20}" fill="{T.ink}" fill-opacity="{.10 if T.name=="dark" else .06}" style="animation-delay:{delay}s"/></g>']
    css = gcss + ".gl{animation:gl 8s ease-in-out infinite}@keyframes gl{0%{transform:skewX(-20deg) translateX(0)}20%,100%{transform:skewX(-20deg) translateX(360px)}}"
    write(fname, svg(Wd, H, f"{label}: {value}", f"{label}: {value}", css, "".join(b)))

# =================================================================== FOOTER (no box)
def footer():
    Wd, H = 960, 84
    b = [f'<rect width="{Wd}" height="{H}" rx="10" fill="#0D1117"/>', f'<path d="M16 1H{Wd-16}" stroke="{T.ln}"/>',
         f'<text x="16" y="40" font-size="15"><tspan class="b">srinivas@s10</tspan><tspan class="f2"> ~&gt; </tspan>exit</text>',
         f'<text x="16" y="64" font-size="13" class="f3">[process completed]</text>',
         f'<rect class="cu" x="{16+20*9}" y="52" width="9" height="15" rx="1.5" fill="{T.fg}"/>',
         f'<text x="{Wd-16}" y="64" font-size="12" class="f3" text-anchor="end">made in Bengaluru on Arch Linux</text>']
    write("footer.svg", svg(Wd, H, "exit", "srinivas@s10 exit. Process completed. Made in Bengaluru on Arch Linux.",
                            ".cu{animation:blink 1.06s step-end infinite}", "".join(b)))

# =================================================================== CONTENT
CARDS = {
    "card-ajrasakha.svg": dict(stat="interning / IIT Ropar, remote", live=True, title="Ajrasakha",
        desc=["A multilingual assistant for farmers. They ask in their own",
              "language, by text or voice, and get reliable answers fast.",
              "Expert-verified answers come first. An LLM answers only when",
              "no verified answer exists, because bad advice can cost a crop."],
        tags=["React", "TypeScript", "Express", "MongoDB Atlas", "Vector search", "Sarvam AI", "Ollama"],
        art=art_ajrasakha, W=960, maxc=64,
        alt="Ajrasakha, AI engineer internship at IIT Ropar (remote): a multilingual assistant for farmers. Questions by text or voice in their own language. Expert-verified golden dataset first, then package-of-practices guidelines, then a general LLM only as a fallback. React, TypeScript, Express, MongoDB Atlas vector search, Sarvam AI, Ollama."),
    "card-aegis.svg": dict(stat="building / SIH 2026", live=True, title="AEGIS",
        desc=["Air-gapped agentic AI workbench", "for Mangalore Refinery. Runs a", "7B model on a 4 GB laptop GPU."],
        tags=["LangGraph", "Ollama", "FAISS", "Docker"], art=art_aegis,
        alt="AEGIS: air-gapped agentic AI workbench for Mangalore Refinery, Smart India Hackathon 2026. Runs a 7B model on a 4 GB laptop GPU. LangGraph, Ollama, FAISS, Docker."),
    "card-migration.svg": dict(stat="building / REVA CAIML", live=True, title="Migration Agent",
        desc=["An LLM agent that upgrades whole", "codebases across breaking version", "changes, then tests its own edits."],
        tags=["Python", "AST", "LLM agents", "Docker"], art=art_migrate,
        alt="Codebase migration agent: an LLM agent that upgrades whole codebases across breaking version changes and tests its own edits. Python, AST, Docker."),
    "card-aquasentinel.svg": dict(stat="shipped / live demo", live=False, title="AquaSentinel",
        desc=["Mission control for an underwater", "inspection robot: telemetry, route", "planning, AI defect detection."],
        tags=["React 19", "TypeScript", "Express", "Postgres"], art=art_sonar,
        alt="AquaSentinel: mission control for an underwater inspection robot with telemetry, route planning and AI defect detection. Opens the live demo."),
    "card-archagent.svg": dict(stat="shipped", live=False, title="ArchAgent",
        desc=["A plain-language brief becomes 3D", "renders and an itemised INR cost", "estimate in under 60 seconds."],
        tags=["React", "TypeScript", "Gemini API"], art=art_arch,
        alt="ArchAgent: a plain-language building brief becomes 3D renders and an itemised INR cost estimate in under 60 seconds. React, TypeScript, Gemini."),
    "card-mlops.svg": dict(stat="shipped", live=False, title="health-risk-mlops",
        desc=["A risk model taken to production", "shape: served, containerised,", "tracked, tested on every push."],
        tags=["FastAPI", "Docker", "MLflow", "Actions"], art=art_mlops,
        alt="health-risk-mlops: a health-risk model served by FastAPI, containerised with Docker, tracked in MLflow, tested by GitHub Actions."),
    "card-debugext.svg": dict(stat="shipped", live=False, title="Debug.ext",
        desc=["Chrome extension that catches", "runtime errors, ranks them P0-P3,", "and drafts the fix."],
        tags=["Chrome MV3", "FastAPI", "Streamlit"], art=art_debug,
        alt="Debug.ext: Chrome extension that catches runtime errors, ranks them P0 to P3, and drafts the fix. FastAPI and Streamlit."),
}
HEADERS = [("experience", "where I work"), ("now", "in progress"), ("shipped", "finished and public"), ("stack", "tools I can defend in an interview"),
           ("activity", "the last twelve months"), ("contact", "fastest reply: email")]
BUTTONS = [("btn-portfolio.svg", "portfolio", "srinivas-rc.is-a.dev", "globe", "https://srinivas-rc.is-a.dev"),
           ("btn-linkedin.svg", "linkedin", "Srinivas R C", "in", "https://www.linkedin.com/in/srinivas-r-c-169406294"),
           ("btn-email.svg", "email", "srinivasrc0408@gmail.com", "mail", "mailto:srinivasrc0408@gmail.com"),
           ("btn-steam.svg", "steam", "off the clock", "pad", "https://steamcommunity.com/profiles/76561199545795989/")]
LINKS = {"card-aegis.svg": "https://github.com/srinivas-rc0408/aegis",
         "card-migration.svg": "https://github.com/srinivas-rc0408/codebase-migration-agent",
         "card-aquasentinel.svg": "https://aqua-wheat.vercel.app",
         "card-archagent.svg": "https://github.com/srinivas-rc0408/archagent",
         "card-mlops.svg": "https://github.com/srinivas-rc0408/health-risk-mlops"}

def build_all():
    alts = {}
    for theme in ["dark"]:
        use(theme)
        alts["hero"] = hero()
        for s, n in HEADERS: header(s, n)
        for f, c in CARDS.items():
            W = c.get("W", 470)
            global AX
            AX = W - 24 - 78
            card(f, c["stat"], c["live"], c["title"], c["desc"], c["tags"], c["art"], c["alt"], Wd=W, maxc=c.get("maxc", 34))
        alts["stack"] = stack()
        alts["exp"] = experience()
        for i, (f, l, v, ic, _) in enumerate(BUTTONS): button(f, l, v, ICONS[ic], i * .5)
        footer()
    return alts

def pic(name, alt, width, href=None):
    v = __import__("hashlib").sha1(open(f"assets/{name}", "rb").read()).hexdigest()[:8]   # cache-buster: new URL whenever the file changes
    p = f'<img src="./assets/{name}?v={v}" width="{width}" alt="{esc(alt, {chr(34): "&quot;"})}" />'
    return f'<a href="{href}">{p}</a>' if href else p

def readme(alts):
    FW = "98.5%"
    H = lambda s, n: pic(f"h-{s}.svg", f"~/{s}: {n}", FW)
    card = lambda f, w="49%": pic(f, CARDS[f]["alt"], w, LINKS.get(f))
    snake = ('<picture><source media="(prefers-color-scheme: dark)" srcset="./profile/snake-dark.svg" />'
             '<source media="(prefers-color-scheme: light)" srcset="./profile/snake-light.svg" />'
             '<img src="./profile/snake-dark.svg" width="98.5%" alt="A snake eating the last year of contributions, square by square" /></picture>')
    hd = dict(HEADERS)
    out = f"""<!-- You opened the source. Respect. Every image here is hand-built SVG from assets/build.py. Say hi: srinivasrc0408@gmail.com -->

{pic("hero.svg", alts["hero"], FW, "https://srinivas-rc.is-a.dev")}

{H("experience", hd["experience"])}

{pic("experience.svg", alts["exp"], FW)}

{H("now", hd["now"])}

{card("card-ajrasakha.svg", FW)}

<p>
  {card("card-aegis.svg")}
  {card("card-migration.svg")}
</p>

{H("shipped", hd["shipped"])}

<p>
  {card("card-aquasentinel.svg")}
  {card("card-archagent.svg")}
  {card("card-mlops.svg")}
  {card("card-debugext.svg")}
</p>


{H("stack", hd["stack"])}

{pic("stack.svg", alts["stack"], FW)}

{H("activity", hd["activity"])}

{snake}

{H("contact", hd["contact"])}

<p>
""" + "\n".join(f"  {pic(f, f'{l}: {v}', '24%', href)}" for f, l, v, _, href in BUTTONS) + f"""
</p>

{pic("footer.svg", "srinivas@s10 exit. Process completed. Made in Bengaluru on Arch Linux.", FW)}
"""
    open("README.md", "w").write(out)

if __name__ == "__main__":
    alts = build_all()
    readme(alts)
    print("built", sum(len(f) for _, _, f in os.walk("assets")), "files")
