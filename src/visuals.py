"""Topic visuals for buyesimfortravel.com: rail-board graphics drawn in code.

Placeholders in content: <!--VISUAL name|caption-->
Names: route-map, board-plans, cap-meter, border-days, breakeven
Covers for blog cards: cover(meta) -> svg, chosen by meta["cover"].
"""
import re
import scenes as scn

VISUAL_RE = re.compile(r"<!--VISUAL\s+([a-z0-9-]+)(?:\|(.*?))?-->", re.S)

INK, BOARD, BLUE, YEL, ALERT, MUTE, PALE = "#14202B", "#0E1A24", "#0B5C9E", "#FFC20E", "#C9432B", "#5B6A76", "#DCE9F3"


def fig(inner, caption, cls=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="visual {cls}">{inner}{cap}</figure>'


def route_map(caption):
    svg = f'''<svg class="visual-svg" viewBox="0 0 640 260" role="img" aria-label="Illustrative route: one main country with a day trip to a neighbour">
<rect width="640" height="260" fill="{PALE}"/>
<g fill="none" stroke="#ffffff" stroke-width="2"><path d="M0 60 H640 M0 130 H640 M0 200 H640 M110 0 V260 M260 0 V260 M410 0 V260 M560 0 V260"/></g>
<path d="M70 190 L190 150 L300 150 L380 95 L520 95" fill="none" stroke="{BLUE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M300 150 L370 205 L540 205" fill="none" stroke="{ALERT}" stroke-width="5" stroke-dasharray="2 10" stroke-linecap="round"/>
<g fill="#fff" stroke="{INK}" stroke-width="3"><circle cx="70" cy="190" r="9"/><circle cx="190" cy="150" r="9"/><circle cx="300" cy="150" r="11"/><circle cx="380" cy="95" r="9"/><circle cx="520" cy="95" r="9"/><circle cx="540" cy="205" r="9"/></g>
<g font-family="Barlow Condensed, sans-serif" font-size="17" font-weight="600" fill="{INK}" letter-spacing=".5"><text x="48" y="222">ARRIVAL</text><text x="170" y="130">CITY A</text><text x="278" y="128">BASE</text><text x="360" y="75">CITY B</text><text x="490" y="75">LAST STOP</text><text x="505" y="232">DAY TRIP</text></g>
<rect x="24" y="22" width="206" height="30" fill="{BOARD}"/><text x="36" y="43" font-family="Barlow Condensed, sans-serif" font-size="16" fill="{YEL}" font-weight="600" letter-spacing="1">ONE COUNTRY: ONE ESIM</text>
<rect x="395" y="150" width="190" height="28" fill="#fff" stroke="{ALERT}"/><text x="406" y="169" font-family="Barlow Condensed, sans-serif" font-size="15" fill="{ALERT}" font-weight="600">SECOND ESIM FOR SIDE TRIP</text>
<text x="616" y="250" text-anchor="end" font-family="IBM Plex Sans, sans-serif" font-size="11" fill="{MUTE}">Illustrative schematic, not a coverage map</text></svg>'''
    return fig(svg, caption)


def board_plans(caption):
    rows = [("TonMobile", "1 GB", "One country", "Europe fixed plan: 35", True), ("Nomad", "2 GB", "35 countries", "5 or 10 days", False),
            ("Jetpac", "3 GB", "33 to 43 countries", "3 to 30 days", False), ("GigSky", "3.5 GB", "43 countries", "1 to 30 days", False),
            ("Saily", "5 GB", "35 countries", "7 to 30 days", False), ("Airalo Eurolink", "5 GB", "41 countries", "3 to 30 days", False),
            ("Maya Mobile", "5 GB", "36 to 49 countries", "3 to 30 days", False), ("Ubigi", "25 GB fair use", "38 countries", "7 to 30 days", False),
            ("Holafly", "Fair use", "33 countries", "3 to 30 days", False)]
    body = "".join(f'<div class="bp-row{" lead" if t else ""}"><span class="bp-prov">{n}</span><span>{a}</span><span>{b}</span><span>{c}</span></div>' for n, a, b, c, t in rows)
    inner = ('<div class="board-plans" role="table" aria-label="Unlimited Europe eSIM departure board"><div class="bp-head"><span>PLAN</span><span>FULL SPEED / DAY</span><span>RANGE</span><span>LENGTHS</span></div>' + body + "</div>")
    return fig(inner, caption)


def cap_meter(caption):
    data = [("TonMobile", 1), ("Nomad", 2), ("Airalo EUconnect", 3), ("Jetpac", 3), ("GigSky", 3.5), ("Saily", 5), ("Airalo Eurolink", 5), ("Maya Mobile", 5)]
    rows = "".join(f'<div class="cm-row"><span class="cm-name">{n}</span><span class="cm-track"><i style="width:{g * 20}%"></i></span><b>{g:g} GB</b></div>' for n, g in data)
    return fig(f'<div class="cap-meter"><p class="cm-title">Full-speed data per day</p>{rows}</div>', caption)


def border_days(caption):
    stops = [("Day 1", "Country A", "Base plan"), ("Day 2", "Country A", "Base plan"), ("Day 3", "Country B", "Check list"), ("Day 4", "Country C", "Check list"), ("Day 5", "Country C", "Check list")]
    items = "".join(f'<li><span class="bd-dot"></span><b>{d}</b><span>{c}</span><small>{n}</small></li>' for d, c, n in stops)
    return fig(f'<ol class="border-days" aria-label="Route with a country change every day or two">{items}</ol>', caption)


def breakeven(caption):
    svg = f'''<svg class="visual-svg" viewBox="0 0 640 240" role="img" aria-label="Fixed plan below about 1.5 to 2 GB a day, unlimited above">
<rect width="640" height="240" fill="#fff"/>
<rect x="40" y="60" width="270" height="70" fill="{PALE}"/><rect x="310" y="60" width="290" height="70" fill="{YEL}"/>
<text x="175" y="102" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="24" font-weight="700" fill="{INK}">FIXED PLAN</text>
<text x="455" y="102" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="24" font-weight="700" fill="{INK}">UNLIMITED</text>
<path d="M40 160 H600" stroke="{INK}" stroke-width="3"/>
<g stroke="{INK}" stroke-width="3"><path d="M40 152 V168 M175 152 V168 M310 152 V168 M455 152 V168 M600 152 V168"/></g>
<g font-family="Barlow Condensed, sans-serif" font-size="18" font-weight="600" fill="{INK}" text-anchor="middle"><text x="40" y="192">0</text><text x="175" y="192">1 GB</text><text x="310" y="192">1.5 to 2 GB</text><text x="455" y="192">3 GB</text><text x="600" y="192">5 GB+</text></g>
<text x="320" y="224" text-anchor="middle" font-family="IBM Plex Sans, sans-serif" font-size="12" fill="{MUTE}">Daily data use. A rule of thumb from the supplied comparison, not a guarantee.</text></svg>'''
    return fig(svg, caption)


VISUALS = {"route-map": route_map, "board-plans": board_plans, "cap-meter": cap_meter, "border-days": border_days, "breakeven": breakeven}


def render(name, caption, site):
    if name in scn.SCENES:
        cap = f"<figcaption>{caption}</figcaption>" if caption else ""
        return f'<figure class="scene">{scn.svg(name)}{cap}</figure>'
    if name == "skyline":
        return scn.skyline()
    if name not in VISUALS:
        raise KeyError(f"Unknown visual '{name}': add it to src/visuals.py")
    return VISUALS[name](caption)


def cover(meta):
    """Small scene for blog cards, chosen by meta['cover']."""
    if meta.get("scene") in scn.SCENES:
        return scn.svg(meta["scene"], "cover-svg")
    c = meta.get("cover", "rail")
    bg = {"rail": PALE, "roam": "#F5E3A8", "sim": "#E3E8EC", "phone": PALE, "key": "#F5E3A8"}.get(c, PALE)
    scenes = {
        "rail": f'<path d="M0 150 H320 M0 165 H320" stroke="{INK}" stroke-width="3"/><g stroke="{INK}" stroke-width="3">{"".join(f"<path d=\"M{x} 144 V171\"/>" for x in range(10, 320, 28))}</g><rect x="60" y="70" width="170" height="60" fill="{BLUE}"/><rect x="72" y="82" width="30" height="22" fill="#fff"/><rect x="112" y="82" width="30" height="22" fill="#fff"/><rect x="152" y="82" width="30" height="22" fill="#fff"/><circle cx="244" cy="100" r="14" fill="{YEL}" stroke="{INK}" stroke-width="3"/>',
        "roam": f'<rect x="40" y="55" width="110" height="80" fill="#fff" stroke="{INK}" stroke-width="3"/><text x="95" y="105" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="30" font-weight="700" fill="{ALERT}">ROAM</text><rect x="170" y="55" width="110" height="80" fill="{BOARD}"/><text x="225" y="105" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="30" font-weight="700" fill="{YEL}">eSIM</text>',
        "sim": f'<path d="M110 40 H190 L220 70 V150 H110 Z" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="132" y="88" width="66" height="44" fill="{YEL}" stroke="{INK}" stroke-width="3"/><path d="M132 110 H198 M165 88 V132" stroke="{INK}" stroke-width="3"/>',
        "phone": f'<rect x="120" y="22" width="80" height="136" rx="10" fill="{BOARD}"/><rect x="128" y="40" width="64" height="100" fill="#fff"/><rect x="136" y="52" width="48" height="8" fill="{BLUE}"/><rect x="136" y="68" width="34" height="6" fill="{PALE}"/><circle cx="160" cy="112" r="14" fill="{YEL}" stroke="{INK}" stroke-width="3"/>',
        "key": f'<rect x="30" y="40" width="260" height="100" fill="{BOARD}"/><text x="160" y="96" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="26" font-weight="700" fill="{YEL}">NO ID</text><text x="160" y="124" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="16" fill="#fff" letter-spacing="1">CARD / APPLE PAY / CRYPTO</text>'}
    return f'<svg class="cover-svg" viewBox="0 0 320 180" role="img" aria-label="" aria-hidden="true"><rect width="320" height="180" fill="{bg}"/>{scenes.get(c, scenes["rail"])}</svg>'


def expand(html, site):
    return VISUAL_RE.sub(lambda m: render(m.group(1), (m.group(2) or "").strip(), site), html)
