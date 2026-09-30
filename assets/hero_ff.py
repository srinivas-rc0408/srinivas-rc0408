import random
from build import *   # palette, svg(), crop_marks(), GLYPHS, esc, write

def hero_ff():
    Wd, H = 960, 600
    FS, CW, LH = 15, 9.0, 23
    rnd = random.Random(1008)
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>',
         f'<rect x=".5" y=".5" width="{Wd-1}" height="{H-1}" fill="none" stroke="{G3}"/>',
         crop_marks(12, 12, Wd - 24, H - 24, 14, W)]
    PX = 44
    prompt = f'<tspan class="b">srinivas@s10</tspan><tspan class="g1"> ~&gt; </tspan>'
    PC = len("srinivas@s10 ~> ")
    # command typed
    y1 = 58
    b.append(f'<text x="{PX}" y="{y1}" font-size="{FS}">{prompt}</text>')
    cx0 = PX + PC * CW
    for i, ch in enumerate("fastfetch"):
        b.append(f'<text class="in" x="{cx0+i*CW:.1f}" y="{y1}" font-size="{FS}" style="animation-delay:{0.35+(i+1)*0.07:.2f}s">{ch}</text>')
    b.append(f'<rect class="cur1" x="{cx0:.1f}" y="{y1-13}" width="{CW}" height="17" fill="{W}"/>')

    # S10 in contribution squares (grayscale)
    cell, gap = 13, 4; pitch = cell + gap
    cols, rows = 19, 9
    gx, gy = PX, 112
    lit, c0 = set(), 1
    for g in "S10":
        for r, row in enumerate(GLYPHS[g]):
            for c, v in enumerate(row):
                if v == "#": lit.add((c0 + c, 1 + r))
        c0 += 6
    for c in range(cols):
        for r in range(rows):
            x, y = gx + c*pitch, gy + r*pitch
            d = 1.10 + c*0.034 + r*0.011
            if (c, r) in lit:
                col = rnd.choices([W, "#D4D4D4", "#A8A8A8"], [5, 3, 2])[0]
                b.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{col}" style="animation-delay:{d:.3f}s"/>')
            else:
                near = any((c+dx, r+dy) in lit for dx in (-1,0,1) for dy in (-1,0,1))
                if rnd.random() < 0.10 and not near:
                    b.append(f'<rect class="cell" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="#3A3A3A" style="animation-delay:{d:.3f}s"/>')
                else:
                    b.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="#161616"/>')
    gw, gh = cols*pitch - gap, rows*pitch - gap
    ly = gy + gh + 26
    lx = gx + gw - 5*14 - 30
    b.append(f'<g class="in" style="animation-delay:1.95s"><text x="{lx-36}" y="{ly}" font-size="12" class="g2">Less</text>')
    for i, col in enumerate(["#161616", "#3A3A3A", "#A8A8A8", "#D4D4D4", W]):
        b.append(f'<rect x="{lx+i*14}" y="{ly-10}" width="10" height="10" rx="2" fill="{col}"/>')
    b.append(f'<text x="{lx+5*14+4}" y="{ly}" font-size="12" class="g2">More</text></g>')
    b.append(f'<g class="in" style="animation-delay:2.05s">'
             f'<text x="{gx}" y="{ly+50}" font-size="28" class="b" letter-spacing=".5">Srinivas R C</text>'
             f'<text x="{gx}" y="{ly+76}" font-size="13" class="g1">AI engineer, Bengaluru</text>'
             f'<text x="{gx}" y="{ly+98}" font-size="13" class="g2">github.com/srinivas-rc0408</text></g>')

    # fastfetch output
    RX, KW = 400, 10 * CW
    who = [
        ("Role",     "AI engineer intern, IIT Ropar (remote)"),
        ("Project",  "Ajrasakha, multilingual farm assistant"),
        ("Building", "AEGIS, air-gapped AI workbench (SIH '26)"),
        ("Agent",    "Codebase migration agent, REVA CAIML"),
        ("Degree",   "B.Tech AI &amp; ML, REVA University '27"),
        ("Stack",    "Python, TypeScript, LangGraph, Ollama"),
    ]
    rig = [
        ("OS",     "Arch Linux x86_64"),
        ("Host",   "ASUS TUF Gaming F15 (FX506HE)"),
        ("CPU",    "Intel i7-11800H (16) @ 4.60 GHz"),
        ("GPU",    "NVIDIA RTX 3050 Ti Mobile, 4 GB"),
        ("Memory", "16 GB"),
        ("WM",     "niri"),
        ("Shell",  "fish, bash"),
    ]
    t0, st = 1.18, 0.07
    n = 0
    def line(y, inner):
        nonlocal n
        b.append(f'<g class="in" style="animation-delay:{t0+n*st:.3f}s">{inner}</g>'); n += 1
    y = 112
    line(y, f'<text x="{RX}" y="{y}" font-size="{FS}" class="b">srinivas<tspan class="g1" style="font-weight:400">@</tspan>s10</text>')
    y += LH; line(y, f'<text x="{RX}" y="{y}" font-size="{FS}" class="g2">{"-"*12}</text>')
    def kv(y, k, v):
        line(y, f'<text x="{RX}" y="{y}" font-size="{FS}" class="g2">{k}</text><text x="{RX+KW:.0f}" y="{y}" font-size="{FS}">{v}</text>')
    for k, v in who:
        y += LH; kv(y, k, v)
    y += LH
    line(y, f'<text x="{RX}" y="{y}" font-size="{FS}" class="g2">Status</text>'
            f'<circle class="pl" cx="{RX+KW+5:.0f}" cy="{y-5}" r="4.5" fill="{W}"/>'
            f'<text x="{RX+KW+18:.0f}" y="{y}" font-size="{FS}">open to 2027 AI/ML roles</text>')
    y += LH * 0.9
    line(y, f'<line x1="{RX}" x2="{RX+KW+396:.0f}" y1="{y-5}" y2="{y-5}" stroke="{G3}"/>')
    y += LH * 0.3
    for k, v in rig:
        y += LH; kv(y, k, v)
    y += LH + 8
    sw = ["#000000", "#262626", "#3A3A3A", "#5C5C5C", "#8C8C8C", "#A8A8A8", "#D4D4D4", "#FFFFFF"]
    line(y, "".join(f'<rect x="{RX+i*30}" y="{y-12}" width="30" height="16" fill="{c}" stroke="{G3}" stroke-width=".5"/>' for i, c in enumerate(sw)))
    tend = t0 + n * st
    # bottom prompt
    yb = H - 40
    b.append(f'<g class="in" style="animation-delay:{tend+0.15:.2f}s"><text x="{PX}" y="{yb}" font-size="{FS}">{prompt}</text></g>')
    b.append(f'<g class="in" style="animation-delay:{tend+0.2:.2f}s"><rect class="bl2" x="{cx0:.1f}" y="{yb-13}" width="{CW}" height="17" fill="{W}"/></g>')
    b.append(f'<text x="{Wd-44}" y="{yb}" font-size="12" class="g2" text-anchor="end">12.97&#176; N  77.59&#176; E</text>')

    css = f"""
.in{{animation:show 0s step-end both}}
.cell{{animation:lit .32s cubic-bezier(.2,.7,.2,1) both}}
@keyframes lit{{from{{fill:#161616}}}}
.cur1{{animation:type .63s steps(9,end) .35s both, hide 0s step-end 1.02s both}}
@keyframes type{{from{{transform:translateX(0)}}to{{transform:translateX({9*CW}px)}}}}
@keyframes hide{{from{{opacity:1}}to{{opacity:0}}}}
.bl2{{animation:blink 1.06s step-end infinite}}
.pl{{animation:pulse 1.6s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{.cur1{{display:none}}}}
"""
    alt = ("Terminal running fastfetch. S10 drawn in contribution squares. Srinivas R C, AI engineer intern at IIT Ropar (remote) "
           "working on Ajrasakha, a multilingual farm assistant. Building AEGIS for SIH 2026 and a codebase migration agent at REVA CAIML. "
           "B.Tech AI and ML, REVA University 2027. Open to 2027 AI/ML roles. Arch Linux, niri, fish and bash, "
           "ASUS TUF Gaming F15 with i7-11800H and RTX 3050 Ti 4 GB.")
    write("hero.svg", svg(Wd, H, "srinivas@s10 fastfetch", alt, css, "".join(b)))

if __name__ == "__main__":
    hero_ff()

def card_ajrasakha():
    Wd, H = 960, 262
    b = [f'<rect width="{Wd}" height="{H}" fill="{BK}"/>',
         f'<rect x=".5" y=".5" width="{Wd-1}" height="{H-1}" fill="none" stroke="{G3}"/>',
         crop_marks(8, 8, Wd - 16, H - 16, 10, G1),
         f'<circle class="pl" cx="30" cy="38" r="4" fill="{W}"/>',
         f'<text x="42" y="42" font-size="12" class="g1">interning / IIT Ropar, remote</text>',
         f'<text x="24" y="84" font-size="22" class="b">Ajrasakha</text>']
    desc = ["A multilingual assistant for farmers. They ask in their own",
            "language, by text or voice, and get reliable answers fast.",
            "Expert-verified answers come first. An LLM answers only when",
            "no verified answer exists, because bad advice can cost a crop."]
    for i, l in enumerate(desc):
        assert len(l) <= 64, l
        b.append(f'<text x="24" y="{114+i*20}" font-size="12.5" class="g1">{esc(l)}</text>')
    from build import chips
    b.append(chips(["React", "TypeScript", "Express", "MongoDB Atlas", "Vector search", "Sarvam AI", "Ollama"], 24, H - 50))
    # three-tier answer cascade
    x0, bw, bh = 680, 250, 28
    tiers = [(66, "golden dataset"), (116, "package of practices"), (166, "general LLM")]
    b.append(f'<line x1="{x0+bw/2}" y1="30" x2="{x0+bw/2}" y2="{tiers[-1][0]}" stroke="{G3}" stroke-dasharray="2 4"/>')
    for i, (ty, label) in enumerate(tiers):
        dash = ' stroke-dasharray="4 3"' if i == 2 else ""
        b.append(f'<rect class="t{i}" x="{x0}" y="{ty}" width="{bw}" height="{bh}" rx="4" fill="{BK}" stroke="{W}" stroke-width="1.2"{dash}/>')
        b.append(f'<text class="l{i}" x="{x0+14}" y="{ty+18.5}" font-size="12">{label}</text>')
        b.append(f'<text class="k{i}" x="{x0+bw-14}" y="{ty+18.5}" font-size="12" text-anchor="end">{["verified", "verified", "fallback"][i]}</text>')
    b.append(f'<circle class="q" cx="{x0+bw/2}" cy="34" r="5" fill="{W}"/>')
    b.append(f'<text x="{x0+bw/2}" y="{tiers[-1][0]+bh+26}" font-size="11" class="g2" text-anchor="middle">verified knowledge first, LLM last</text>')
    stop = [ty - 7 - 34 for ty, _ in tiers]  # dot offsets resting just above each tier
    s1, s2, s3 = stop
    css = f"""
.pl{{animation:pulse 1.6s ease-in-out infinite}}
.q{{animation:q 9s cubic-bezier(.5,0,.5,1) infinite}}
@keyframes q{{
0%{{transform:translateY(0);opacity:0}} 3%{{transform:translateY(0);opacity:1}}
10%,28%{{transform:translateY({s1}px);opacity:1}} 31%{{transform:translateY({s1}px);opacity:0}}
33.3%{{transform:translateY(0);opacity:0}} 36%{{transform:translateY(0);opacity:1}}
43%{{transform:translateY({s1}px)}} 50%,61%{{transform:translateY({s2}px);opacity:1}} 64%{{transform:translateY({s2}px);opacity:0}}
66.6%{{transform:translateY(0);opacity:0}} 69%{{transform:translateY(0);opacity:1}}
76%{{transform:translateY({s1}px)}} 83%{{transform:translateY({s2}px)}} 90%,97%{{transform:translateY({s3}px);opacity:1}} 100%{{transform:translateY({s3}px);opacity:0}}}}
.t0{{animation:t0 9s linear infinite}} @keyframes t0{{0%,10%{{fill:{BK}}}11%,28%{{fill:{W}}}30%,42%{{fill:{BK}}}43%,45%{{fill:{G3}}}46%,75%{{fill:{BK}}}76%,78%{{fill:{G3}}}79%,100%{{fill:{BK}}}}}
.t1{{animation:t1 9s linear infinite}} @keyframes t1{{0%,50%{{fill:{BK}}}51%,61%{{fill:{W}}}63%,82%{{fill:{BK}}}83%,85%{{fill:{G3}}}86%,100%{{fill:{BK}}}}}
.t2{{animation:t2 9s linear infinite}} @keyframes t2{{0%,90%{{fill:{BK}}}91%,97%{{fill:{W}}}99%,100%{{fill:{BK}}}}}
.l0,.k0{{animation:x0 9s linear infinite}} @keyframes x0{{0%,10%{{fill:{W}}}11%,28%{{fill:{BK}}}30%,100%{{fill:{W}}}}}
.l1,.k1{{animation:x1 9s linear infinite}} @keyframes x1{{0%,50%{{fill:{W}}}51%,61%{{fill:{BK}}}63%,100%{{fill:{W}}}}}
.l2,.k2{{animation:x2 9s linear infinite}} @keyframes x2{{0%,90%{{fill:{W}}}91%,97%{{fill:{BK}}}99%,100%{{fill:{W}}}}}
.k0,.k1,.k2{{opacity:.55}}
"""
    alt = ("Ajrasakha, AI engineer internship at IIT Ropar (remote): a multilingual assistant for farmers. Questions by text or voice in their own language. "
           "Answers come from an expert-verified golden dataset first, then package-of-practices guidelines, and a general LLM only as a fallback. "
           "React, TypeScript, Express, MongoDB Atlas vector search, Sarvam AI, Ollama.")
    write("card-ajrasakha.svg", svg(Wd, H, "Ajrasakha", alt, css, "".join(b)))

if __name__ == "__main__":
    card_ajrasakha()
