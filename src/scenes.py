"""Illustrated Europe scenes drawn in code (flat style). Used by visuals.py."""

INK, BOARD, BLUE, YEL, ALERT = "#14202B", "#0E1A24", "#0B5C9E", "#FFC20E", "#C9432B"
SKY, STONE, TERRA, GREEN, SNOW, SAND = "#CFE3F1", "#D9C9AE", "#C9683F", "#4E8A5B", "#F7FAFC", "#EBD9A8"


def _windows(x, y, cols, rows, w=9, h=12, gx=8, gy=9, fill="#FFF3C4"):
    return "".join(f'<rect x="{x + c * (w + gx)}" y="{y + r * (h + gy)}" width="{w}" height="{h}" fill="{fill}"/>'
                   for c in range(cols) for r in range(rows))


def _sun(x=540, y=48):
    return f'<circle cx="{x}" cy="{y}" r="26" fill="{YEL}"/>'


def _ground(color=INK):
    return (f'<rect x="0" y="176" width="640" height="24" fill="{color}"/>'
            f'<path d="M0 176 H640" stroke="{YEL}" stroke-width="3" stroke-dasharray="14 10"/>')


def paris():
    tower = (f'<polygon points="190,176 214,70 226,70 250,176 238,176 220,100 202,176" fill="{INK}"/>'
             f'<rect x="206" y="92" width="28" height="5" fill="{INK}"/><rect x="200" y="124" width="40" height="5" fill="{INK}"/>'
             f'<polygon points="217,70 223,70 220,36" fill="{INK}"/>')
    row = (f'<rect x="300" y="86" width="120" height="90" fill="{STONE}"/>{_windows(310, 98, 6, 3, 9, 12, 7, 12, BLUE)}'
           f'<rect x="420" y="100" width="110" height="76" fill="#E6D2B4"/>{_windows(430, 110, 5, 3, 9, 12, 8, 10, BLUE)}'
           f'<polygon points="300,86 420,86 410,72 310,72" fill="{TERRA}"/><polygon points="420,100 530,100 520,86 430,86" fill="#B65A35"/>')
    cafe = (f'<rect x="40" y="132" width="110" height="44" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M40 132 H150 L160 112 H30 Z" fill="{ALERT}"/>'
            f'<path d="M60 112 L52 132 M90 112 L86 132 M120 112 L120 132 M150 112 L156 132" stroke="#fff" stroke-width="5"/>'
            f'<circle cx="75" cy="160" r="9" fill="{YEL}" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="115" cy="160" r="9" fill="{YEL}" stroke="{INK}" stroke-width="2"/>')
    return f'<rect width="640" height="200" fill="{SKY}"/>{_sun()}{row}{tower}{cafe}{_ground()}'


def london():
    ben = (f'<rect x="120" y="56" width="52" height="120" fill="{STONE}" stroke="{INK}" stroke-width="3"/>'
           f'<polygon points="120,56 172,56 146,14" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
           f'<circle cx="146" cy="84" r="16" fill="#fff" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M146 84 V73 M146 84 H154" stroke="{INK}" stroke-width="3"/>'
           f'<rect x="136" y="120" width="8" height="22" fill="{INK}"/><rect x="150" y="120" width="8" height="22" fill="{INK}"/>')
    wins = "".join(f'<rect x="{312 + i * 34}" y="122" width="24" height="16" fill="#fff"/>'
                   f'<rect x="{312 + i * 34}" y="152" width="24" height="14" fill="#fff"/>' for i in range(5))
    bus = (f'<rect x="300" y="112" width="190" height="62" rx="6" fill="{ALERT}" stroke="{INK}" stroke-width="3"/>'
           f'<rect x="300" y="142" width="190" height="4" fill="{INK}"/>{wins}'
           f'<circle cx="340" cy="176" r="13" fill="{INK}"/><circle cx="450" cy="176" r="13" fill="{INK}"/>'
           f'<circle cx="340" cy="176" r="5" fill="#fff"/><circle cx="450" cy="176" r="5" fill="#fff"/>')
    bridge = (f'<path d="M520 176 V130 M590 176 V130 M500 130 H610" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M500 130 Q555 160 610 130" fill="none" stroke="{INK}" stroke-width="3"/>')
    return (f'<rect width="640" height="200" fill="#DDE5EA"/><circle cx="60" cy="50" r="24" fill="#fff"/>'
            f'<circle cx="90" cy="60" r="20" fill="#fff"/>{ben}{bus}{bridge}{_ground()}')


def alps():
    mount = (f'<polygon points="0,176 120,62 210,150 300,40 420,176" fill="#7C9DB5"/>'
             f'<polygon points="300,40 270,82 290,76 310,92 330,72 350,82" fill="{SNOW}"/>'
             f'<polygon points="120,62 98,96 118,90 134,102 146,84" fill="{SNOW}"/>'
             f'<polygon points="330,176 470,80 640,176" fill="#5E8199"/>'
             f'<polygon points="470,80 446,112 466,106 482,118 498,100" fill="{SNOW}"/>')
    trees = "".join(f'<polygon points="{x},176 {x + 12},176 {x + 6},{176 - h}" fill="{GREEN}"/>'
                    for x, h in [(30, 44), (52, 36), (560, 40), (584, 52), (606, 34)])
    cars = "".join(f'<rect x="{150 + k * 90}" y="144" width="86" height="28" rx="4" fill="{ALERT}" stroke="{INK}" stroke-width="3"/>'
                   + "".join(f'<rect x="{158 + k * 90 + i * 22}" y="150" width="14" height="10" fill="#fff"/>' for i in range(3))
                   for k in range(2))
    loco = f'<rect x="330" y="150" width="44" height="22" rx="8" fill="{INK}"/><rect x="340" y="154" width="16" height="9" fill="{YEL}"/>'
    return f'<rect width="640" height="200" fill="{SKY}"/>{_sun(80, 44)}{mount}{trees}{cars}{loco}{_ground(BLUE)}'


def canal():
    cols = ["#C9683F", "#EBD9A8", "#4E8A5B", "#B4452E", "#D9C9AE", "#0B5C9E", "#C9683F", "#EBD9A8"]
    houses, x = "", 14
    for i, c in enumerate(cols):
        w, h = 62, 86 + (i % 3) * 14
        houses += (f'<rect x="{x}" y="{150 - h}" width="{w}" height="{h}" fill="{c}"/>'
                   f'<polygon points="{x},{150 - h} {x + w},{150 - h} {x + w // 2},{150 - h - 22}" fill="{INK}"/>'
                   + _windows(x + 10, 150 - h + 12, 3, 3 if h > 96 else 2, 11, 14, 5, 10))
        x += w + 4
    waves = "".join(f'<path d="M{20 + i * 70} {168 + (i % 2) * 10} q10 -6 20 0 t20 0" fill="none" stroke="#fff" stroke-width="3"/>' for i in range(9))
    water = f'<rect x="0" y="150" width="640" height="50" fill="#7AA6C2"/>{waves}'
    bike = (f'<circle cx="540" cy="186" r="10" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="574" cy="186" r="10" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M540 186 L555 168 L574 186 M555 168 H546" fill="none" stroke="{INK}" stroke-width="3"/>')
    return f'<rect width="640" height="200" fill="{SKY}"/>{_sun(580, 34)}{houses}{water}{bike}'


def rome():
    def arch(x, y):
        return f'<path d="M{x} {y} v-20 a12 12 0 0 1 24 0 v20 z" fill="{INK}"/>'
    arches = "".join(arch(x, 92) + arch(x, 128) + arch(x, 164) for x in range(170, 500, 36))
    colo = f'<rect x="156" y="58" width="360" height="118" fill="{SAND}" stroke="{INK}" stroke-width="3"/>{arches}'

    def pine(x):
        return f'<rect x="{x + 18}" y="132" width="6" height="44" fill="#6B4A2B"/><ellipse cx="{x + 21}" cy="124" rx="34" ry="16" fill="{GREEN}"/>'
    scooter = (f'<rect x="570" y="152" width="46" height="12" rx="6" fill="{TERRA}" stroke="{INK}" stroke-width="3"/>'
               f'<circle cx="576" cy="172" r="8" fill="{INK}"/><circle cx="610" cy="172" r="8" fill="{INK}"/>'
               f'<path d="M606 152 L612 130 H622" fill="none" stroke="{INK}" stroke-width="3"/>')
    return f'<rect width="640" height="200" fill="#F4E4C8"/>{_sun(96, 52)}{colo}{pine(40)}{pine(520)}{scooter}{_ground()}'


def lisbon():
    hill = '<path d="M0 176 L0 110 Q160 60 300 120 T640 100 V176 Z" fill="#E8C9A0"/>'
    tiles = "".join(f'<rect x="{x}" y="{y}" width="52" height="46" fill="{c}"/>{_windows(x + 8, y + 8, 3, 2, 8, 10, 6, 6, BLUE)}'
                    f'<polygon points="{x - 4},{y} {x + 56},{y} {x + 26},{y - 14}" fill="{TERRA}"/>'
                    for x, y, c in [(60, 84, "#fff"), (116, 92, "#F5E3A8"), (360, 90, "#fff"), (416, 80, "#DCE9F3"), (472, 88, "#fff")])
    tram = (f'<rect x="200" y="124" width="120" height="44" rx="10" fill="{YEL}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="214" y="132" width="26" height="18" fill="#fff"/><rect x="248" y="132" width="26" height="18" fill="#fff"/>'
            f'<rect x="282" y="132" width="26" height="18" fill="#fff"/>'
            f'<path d="M260 124 V104 M240 104 H280" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="226" cy="170" r="7" fill="{INK}"/><circle cx="294" cy="170" r="7" fill="{INK}"/>')
    return f'<rect width="640" height="200" fill="{SKY}"/>{_sun(560, 40)}{hill}{tiles}{tram}{_ground()}'


def skyline():
    d = "#2A4358"
    return ('<svg class="skyline" viewBox="0 0 1200 120" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            f'<g fill="{d}"><polygon points="90,120 112,26 122,26 144,120 136,120 117,60 98,120"/><polygon points="116,26 118,26 117,4"/>'
            '<rect x="210" y="60" width="40" height="60"/><polygon points="210,60 250,60 230,40"/><rect x="262" y="72" width="60" height="48"/>'
            '<rect x="400" y="30" width="26" height="90"/><polygon points="400,30 426,30 413,6"/><rect x="440" y="70" width="70" height="50"/>'
            '<polygon points="560,120 640,50 720,120"/>'
            '<rect x="790" y="50" width="12" height="70"/><polygon points="760,70 832,70 796,40"/>'
            '<rect x="880" y="76" width="60" height="44"/><rect x="950" y="58" width="44" height="62"/><polygon points="950,58 994,58 972,40"/>'
            '<rect x="1040" y="68" width="100" height="52"/><rect x="1060" y="46" width="14" height="22"/></g></svg>')


SCENES = {"scene-paris": paris, "scene-london": london, "scene-alps": alps, "scene-canal": canal,
          "scene-rome": rome, "scene-lisbon": lisbon}


def svg(name, cls="scene-svg"):
    return (f'<svg class="{cls}" viewBox="0 0 640 200" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true">'
            f'{SCENES[name]()}</svg>')
