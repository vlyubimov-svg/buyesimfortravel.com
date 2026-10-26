#!/usr/bin/env python3
"""Pre-launch QA for a satellite site. Run after `python3 build.py`.

Usage:
  python3 qa.py                       # content, links, words, AI markers, design uniqueness
  python3 qa.py --registry ../registry/USED_DESIGNS.md --compare ../examples/bestesimforiphone/assets/css/style.css
  python3 qa.py --screens             # also mobile/desktop screenshots + horizontal-overflow check (needs playwright)

Exit code 1 if any FAIL. WARN lines need a human look but do not block.
"""
import argparse, difflib, json, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
fails, warns = [], []


def fail(m): fails.append(m)
def warn(m): warns.append(m)


def host(u):
    h = (urlparse(u).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def inpool(h, pool):
    return any(h == d or h.endswith("." + d) for d in pool)


BANNED = ["seamless", "dive in", "dive into", "game-changer", "game changer", "unlock the power", "in today's fast-paced",
          "elevate your", "look no further", "navigating the", "it's worth noting", "in the ever-evolving", "embark",
          "delve", "tapestry", "we tested", "we used it for", "our hands-on test"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", help="path to registry/USED_DESIGNS.md from the kit")
    ap.add_argument("--compare", nargs="*", default=[], help="CSS files of other sites/examples to compare against")
    ap.add_argument("--screens", action="store_true")
    a = ap.parse_args()

    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    qa_cfg = site.get("qa", {})

    # 1. TODO / wireframe markers
    for p in [ROOT / "site.json", ROOT / "docs" / "FACTS.md", ROOT / "src" / "data" / "providers.json",
              *(ROOT / "src" / "content").rglob("*.html")]:
        if p.exists() and "TODO" in p.read_text(encoding="utf-8"):
            fail(f"TODO left in {p.relative_to(ROOT)}")
    if not (ROOT / "docs" / "FACTS.md").exists():
        fail("docs/FACTS.md missing (verified fact base)")
    for p in [ROOT / "src/assets/css/style.css", ROOT / "src/templates/base.html"]:
        if "WIREFRAME" in p.read_text(encoding="utf-8"):
            fail(f"{p.relative_to(ROOT)} is still the wireframe: write this site's own design")
    if not (ROOT / "src/assets/img/logo.svg").exists():
        fail("src/assets/img/logo.svg missing (draw a unique logo)")
    if not (ROOT / "src/assets/img/og.png").exists():
        fail("src/assets/img/og.png missing (run make_brand.py)")

    # 2. providers order
    prov = json.loads((ROOT / "src/data/providers.json").read_text(encoding="utf-8"))
    ranked = sorted(prov["providers"], key=lambda p: -sum(p["scores"]))
    if ranked and ranked[0]["slug"] != site["partner"]["slug"]:
        fail(f"Partner '{site['partner']['slug']}' is not #1 by score (top is {ranked[0]['slug']})")
    if len(prov["providers"]) < 5:
        warn("Fewer than 5 providers in the rating")

    # 3. built pages
    if not DIST.exists():
        fail("dist/ missing: run python3 build.py first")
        return report()
    pages = {}
    for p in DIST.rglob("*.html"):
        r = p.relative_to(DIST).as_posix() and __import__("pathlib").PurePosixPath(p.relative_to(DIST).as_posix())
        url = "/" + str(r) if r.name != "index.html" else ("/" if str(r.parent) == "." else f"/{r.parent}/")
        pages[url] = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    follow = set(site["partner"]["hosts"]) | set(site.get("follow_hosts_extra", []))
    nofollow = set(site.get("nofollow_hosts", []))
    unknown, partner_links = set(), 0
    for url, s in pages.items():
        for el in s.find_all("a", href=True):
            h = el["href"]; rel = " ".join(el.get("rel") or [])
            if h.startswith("/") and not h.startswith("//"):
                path = h.split("#")[0]
                if path and path not in pages and not path.startswith("/assets"):
                    fail(f"Broken internal link {h} on {url}")
            elif h.startswith("http"):
                ho = host(h)
                if inpool(ho, follow):
                    if "nofollow" in rel: fail(f"Partner link has nofollow: {h} on {url}")
                    if inpool(ho, set(site["partner"]["hosts"])): partner_links += 1
                elif inpool(ho, nofollow):
                    if "nofollow" not in rel: fail(f"Competitor link without nofollow: {h} on {url}")
                else:
                    unknown.add(ho)
        text = s.get_text(" ")
        low = text.lower()
        for b in BANNED:
            if b in low: warn(f"Phrase '{b}' on {url}")
        em = text.count("—")
        if em > 3: warn(f"{em} em-dashes on {url}")
        if "→" in text or "->" in text: warn(f"Arrow characters on {url}")
        if re.search(r"[$€£]\s?\d", text): warn(f"Price-like figure on {url}: verify it is sourced in FACTS.md")
    for u in sorted(unknown):
        warn(f"External host not in follow/nofollow lists: {u} (is it a competitor? add to nofollow_hosts)")
    if partner_links < 8:
        warn(f"Only {partner_links} followed partner links across the site")

    # 4. word counts and visuals
    def words(s):
        main = s.find("article") or s.find("main") or s
        return len(re.findall(r"[A-Za-z0-9À-ɏЀ-ӿ][\w'’+.\-]*", main.get_text(" ")))
    home_min = qa_cfg.get("home_min_words", 3500)
    if "/" in pages:
        w = words(pages["/"])
        if w < home_min: fail(f"Home has {w} words, needs at least {home_min} (largest competitor + margin)")
        vis = len(pages["/"].select("svg, img, .phone, .visual, figure"))
        if vis < 6: warn(f"Home has only {vis} visual elements; add topic visuals")
    for url, s in pages.items():
        if url.startswith("/blog/") and url != "/blog/":
            w = words(s)
            if w < qa_cfg.get("post_min_words", 1400): fail(f"{url} has {w} words")
            if not s.select("figure, .visual, .phone, svg.visual"):
                warn(f"{url} has no figure or topic visual")
    posts = [u for u in pages if u.startswith("/blog/") and u != "/blog/"]
    if len(posts) < 5:
        fail(f"Only {len(posts)} blog posts, need 5")

    # 5. design uniqueness
    css = (ROOT / "src/assets/css/style.css").read_text(encoding="utf-8")
    base = (ROOT / "src/templates/base.html").read_text(encoding="utf-8")
    fonts = set(re.findall(r"family=([A-Za-z+]+)", base))
    colors = set(c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", css))
    if a.registry and Path(a.registry).exists():
        reg = Path(a.registry).read_text(encoding="utf-8").lower()
        for f in fonts:
            if f.replace("+", " ").lower() in reg:
                fail(f"Font '{f.replace('+', ' ')}' already used by another site (registry)")
        reused = [c for c in colors if c in reg]
        if len(reused) > 2:
            fail(f"Colors already used by other sites: {', '.join(sorted(reused))}")
    for other in a.compare:
        o = Path(other)
        if o.exists():
            a_, b_ = (set(x.strip() for x in re.split(r"[;{}]", t) if x.strip()) for t in (o.read_text(encoding="utf-8"), css))
            ratio = len(a_ & b_) / max(1, len(a_ | b_))
            if ratio > 0.6:
                fail(f"style.css is {ratio:.0%} similar to {o}: write a new design")
            elif ratio > 0.45:
                warn(f"style.css is {ratio:.0%} similar to {o}")

    if a.screens:
        screens(pages)
    return report()


def screens(pages):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        warn("playwright not installed: pip install playwright && playwright install chromium"); return
    out = ROOT / "qa-screens"; out.mkdir(exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8799", "--directory", str(DIST)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            for w, h, tag in [(1366, 900, "desktop"), (390, 844, "mobile")]:
                pg = b.new_page(viewport={"width": w, "height": h})
                for url in pages:
                    pg.goto("http://localhost:8799" + url, wait_until="networkidle")
                    if pg.evaluate("document.documentElement.scrollWidth") > w + 1:
                        fail(f"Horizontal scroll on {url} ({tag})")
                    if url in ("/", "/rating/", "/blog/") or (url.startswith("/blog/") and url.count("/") == 3 and tag == "desktop"):
                        name = (url.strip("/").replace("/", "_") or "home") + f"-{tag}.png"
                        pg.screenshot(path=str(out / name), full_page=(tag == "desktop"))
            b.close()
    finally:
        srv.terminate()
    print(f"Screenshots in {out}/ (review them visually)")


def report():
    for w in warns: print("WARN ", w)
    for f in fails: print("FAIL ", f)
    print(f"\n{len(fails)} fail, {len(warns)} warn")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
