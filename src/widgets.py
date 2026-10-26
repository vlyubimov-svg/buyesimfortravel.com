"""Structural HTML widgets for the engine. Markup only: every site styles them in its own CSS.

mono colors come from providers.json ("color"), mockup texts from site.json ("mock").
Add topic-specific visuals for each site in src/visuals.py (see SKILL.md), not here.

Placeholders used in content files (replaced by build.py):
  <!--PHONE name|caption-->   iPhone mockup figure. names: cellular, add-esim, about, no-service, usage, checkout, travel-line
  <!--MINIRATING n-->          compact top-n rating card (scores, bars, review links)
  <!--PODIUM-->                top-3 podium for the rating hero
  <!--LATEST-->                latest guides grid (3 cards)
"""
import re

CFG = {}  # set by build.py to the parsed site.json
COVER = lambda m: ""
COLORS = {}  # slug -> color, filled from providers.json by build.py
FALLBACK = ["#3B5BDB", "#E8590C", "#0F9D8A", "#C2255C", "#5F3DC4", "#1971C2", "#343A40", "#E67700"]


def M(key, default):
    return CFG.get("mock", {}).get(key, default)

SIGNAL = '<svg viewBox="0 0 18 12" width="16" height="11"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/><rect x="10" y="2.5" width="3" height="9.5" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>'
WIFI = '<svg viewBox="0 0 16 12" width="14" height="11"><path d="M8 11.5l2.4-2.9a3.6 3.6 0 0 0-4.8 0z"/><path d="M3.4 6.6a7 7 0 0 1 9.2 0l-1.4 1.7a4.8 4.8 0 0 0-6.4 0z"/><path d="M1 3.8a10.6 10.6 0 0 1 14 0l-1.4 1.7a8.4 8.4 0 0 0-11.2 0z"/></svg>'
BATTERY = '<svg viewBox="0 0 26 12" width="23" height="11"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="currentColor" opacity=".4"/><rect x="2" y="2" width="16" height="8" rx="1.6"/><rect x="23.5" y="4" width="1.8" height="4" rx=".9" opacity=".4"/></svg>'


def mono(slug, name, size=""):
    color = COLORS.get(slug) or FALLBACK[abs(hash(slug)) % len(FALLBACK)]
    return f'<span class="mono {size}" style="--mc:{color}" aria-hidden="true">{name[0]}</span>'


def _status(text="9:41", carrier=None):
    left = f'<span>{text}</span>'
    right = (f'<span class="sb-right">{carrier}</span>' if carrier
             else f'<span class="sb-right">{SIGNAL}{WIFI}{BATTERY}</span>')
    return f'<div class="sbar">{left}{right}</div>'


def _row(label, value="", kind="", badge=None):
    b = f'<span class="line-badge" style="--lb:{badge[1]}">{badge[0]}</span>' if badge else ""
    if kind == "on":
        v = '<span class="tg on"></span>'
    elif kind == "off":
        v = '<span class="tg"></span>'
    elif kind == "link":
        return f'<div class="ios-row link">{b}<span>{label}</span></div>'
    else:
        v = f'<span class="ios-val">{value}</span>'
    return f'<div class="ios-row">{b}<span class="ios-l">{label}</span>{v}</div>'


QR = None


def _qr():
    """Deterministic decorative QR-like pattern (not a real code)."""
    global QR
    if QR:
        return QR
    n, cells, seed = 21, [], 7
    for y in range(n):
        for x in range(n):
            finder = any(fx <= x < fx + 7 and fy <= y < fy + 7 for fx, fy in ((0, 0), (14, 0), (0, 14)))
            if finder:
                fx = 0 if x < 7 else 14
                fy = 0 if y < 7 else 14
                lx, ly = x - fx, y - fy
                on = lx in (0, 6) or ly in (0, 6) or (2 <= lx <= 4 and 2 <= ly <= 4)
            else:
                seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
                on = (seed >> 16) % 2 == 0
            if on:
                cells.append(f'<rect x="{x}" y="{y}" width="1" height="1"/>')
    QR = f'<svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">{"".join(cells)}</svg>'
    return QR


def screen(name):
    P, T = ("P", "#8E8E93"), ("T", "#2F5BFF")
    if name == "cellular":
        return (_status() + '<div class="ios-nav"><span class="back">Settings</span></div><p class="ios-title">Cellular</p>'
                '<p class="ios-label">SIMs</p><div class="ios-group">'
                + _row("Primary", "On", badge=P) + _row(M("line_label", "Travel eSIM"), "On", badge=T) + _row("Add eSIM", kind="link") +
                '</div><div class="ios-group">' + _row("Cellular Data", M("line_label", "Travel eSIM")) + _row("Default Voice Line", "Primary") +
                '</div><p class="ios-label">' + M("line_label", "Travel eSIM") + '</p><div class="ios-group">' + _row("Turn On This Line", kind="on") +
                _row("Data Roaming", kind="on") + _row("Low Data Mode", kind="off") + '</div>')
    if name == "travel-line":
        return (_status() + '<div class="ios-nav"><span class="back">Cellular</span></div><p class="ios-title">' + M("line_label", "Travel eSIM") + '</p>'
                '<div class="ios-group">' + _row("Turn On This Line", kind="on") + '</div><div class="ios-group">' +
                _row("Data Roaming", kind="on") + _row("Network Selection", "Automatic") + _row("Voice &amp; Data", "5G Auto") +
                '</div><div class="ios-group">' + _row("Cellular Plan Label", "Travel") + '</div>'
                '<div class="ios-note">Data Roaming lets the travel line join its partner network abroad.</div>')
    if name == "add-esim":
        return (_status() + '<div class="sheet"><p class="sheet-title">Set Up Cellular</p><div class="qr-box">' + _qr() +
                '<span class="scan-line"></span></div><p class="sheet-sub">Position the QR code from your provider in the frame.</p>'
                '<div class="ios-group">' + _row("Use QR Code", kind="link") + _row("Enter Details Manually", kind="link") + '</div></div>')
    if name == "about":
        return (_status() + '<div class="ios-nav"><span class="back">General</span></div><p class="ios-title">About</p>'
                '<div class="ios-group">' + _row("Name", "iPhone") + _row("Model Name", "iPhone") + _row("Carrier Lock", '<b class="ok">No SIM restrictions</b>') +
                '</div><div class="ios-group">' + _row("EID", "8904 •••• 4821") + _row("Network", M("line_label", "Travel eSIM")) + _row("Carrier", "Primary") + '</div>'
                '<div class="ios-note">An EID line means the iPhone has an eSIM chip.</div>')
    if name == "no-service":
        return (_status("9:41", '<span class="nosvc">No Service</span>') + '<div class="ios-nav"><span class="back">Cellular</span></div><p class="ios-title">' + M("line_label", "Travel eSIM") + '</p>'
                '<div class="ios-group">' + _row("Turn On This Line", kind="on") + '</div><div class="ios-group hl">' +
                _row("Data Roaming", kind="off") + '</div><div class="fix-tag">Turn this on</div><div class="ios-group">' + _row("Network Selection", "Automatic") + '</div>')
    if name == "usage":
        rows = [("Maps", 38), ("Messages", 22), ("Browser", 18), ("Photos", 12), ("Video", 10)]
        bars = "".join(f'<div class="use-row"><span>{a}</span><i style="width:{w * 2}%"></i></div>' for a, w in rows)
        return (_status() + '<div class="ios-nav"><span class="back">Settings</span></div><p class="ios-title">Cellular</p>'
                '<p class="ios-label">Cellular data · Travel eSIM</p><div class="ios-group usage"><div class="use-total"><b>Current Period</b><span>Usage by app</span></div>'
                + bars + '</div><div class="ios-group">' + _row("Low Data Mode", kind="on") + _row("Wi-Fi Assist", kind="off") + '</div>')
    if name == "checkout":
        return (_status() + '<p class="ios-title" style="margin-top:22px">Checkout</p><div class="plan-card"><span class="pc-k">' + M("plan_kicker", "Plan") + '</span>'
                '<b>' + M("plan_name", "Country · 10 GB") + '</b><span>' + M("plan_meta", "30 days · 4G/5G") + '</span></div><p class="ios-label">Payment method</p><div class="ios-group pay">'
                '<div class="ios-row"><span class="pm">Card</span><span class="radio"></span></div>'
                '<div class="ios-row"><span class="pm">Apple Pay</span><span class="radio"></span></div>'
                '<div class="ios-row sel"><span class="pm">Crypto <small>BTC · USDT · TON</small></span><span class="radio on"></span></div></div>'
                '<div class="pay-btn">Continue</div>')
    raise KeyError(name)


def phone(name, small=False):
    cls = "phone sm" if small else "phone"
    return f'<div class="{cls}"><div class="screen"><span class="island"></span>{screen(name)}</div></div>'


def phone_figure(name, caption=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="phone-fig">{phone(name)}{cap}</figure>'


def mini_rating(data, n=5, title=None, base="/rating/", compact=False):
    title = title or CFG.get("rating", {}).get("title", "Top providers")
    rows = []
    for i, p in enumerate(data["providers"][:n], 1):
        rows.append(
            f'<li class="mr-row{" is-top" if i == 1 else ""}"><span class="mr-rank">{i}</span>{mono(p["slug"], p["name"])}'
            f'<span class="mr-main"><a class="mr-name" href="{base}#{p["slug"]}">{p["name"]}</a><span class="mr-tag">{p["tag"]}</span>'
            f'<span class="mr-bar"><i style="width:{p["score"] * 10:.0f}%"></i></span></span>'
            f'<b class="mr-score">{p["score"]:.1f}</b></li>')
    foot = '' if compact else f'<a class="mr-all" href="/rating/">See all {len(data["providers"])} providers and scores</a>'
    return (f'<div class="mini-rating{" compact" if compact else ""}"><div class="mr-head"><span class="mr-title">{title}</span>'
            f'<span class="mr-upd">Editorial score</span></div><ol>{"".join(rows)}</ol>{foot}</div>')


def podium(data):
    order = [1, 0, 2]
    cols = []
    for idx in order:
        p = data["providers"][idx]
        cols.append(f'<a class="pod pod-{idx + 1}" href="#{p["slug"]}">{mono(p["slug"], p["name"], "lg")}'
                    f'<span class="pod-name">{p["name"]}</span><span class="pod-score">{p["score"]:.1f}</span>'
                    f'<span class="pod-step"><b>{idx + 1}</b></span></a>')
    return f'<div class="podium">{"".join(cols)}</div>'


def latest(posts, n=3):
    cards = []
    for p in posts[:n]:
        m = p["meta"]
        cards.append(f'<a class="post-card" href="{p["url"]}"><div class="post-cover">{COVER(m)}</div>'
                     f'<div class="post-body"><span class="badge badge-accent">{m.get("category", "Guide")}</span><h3>{m["h1"]}</h3>'
                     f'<p>{m.get("excerpt", "")}</p><span class="post-meta">{m["read"]} min read</span></div></a>')
    return '<div class="post-grid three">' + "".join(cards) + "</div>"


PHONE_RE = re.compile(r"<!--PHONE\s+([a-z-]+)(?:\|(.*?))?-->", re.S)


def expand(body, data, posts):
    body = PHONE_RE.sub(lambda m: phone_figure(m.group(1), (m.group(2) or "").strip()), body)
    body = re.sub(r"<!--MINIRATING\s*(\d+)?-->", lambda m: mini_rating(data, int(m.group(1) or 5)), body)
    body = body.replace("<!--PODIUM-->", podium(data))
    body = body.replace("<!--HEROPHONE-->", phone("cellular"))
    body = body.replace("<!--LATEST-->", latest(posts))
    return body
