#!/usr/bin/env python3
"""Static site builder (satellite engine). All per-site settings come from site.json.

Usage:  python3 build.py          -> builds ./dist
Content lives in src/content/{pages,blog}/*.html (HTML fragments with a META json comment).
"""
import json, re, shutil, sys, html
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

sys.path.insert(0, str(Path(__file__).parent / "src"))
import widgets  # noqa: E402
try:
    import visuals  # optional, site-specific topic visuals: src/visuals.py with expand(html, site) -> html
except ImportError:
    visuals = None

ROOT = Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT / "dist"

SITE = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
SITE["url"] = "https://" + SITE["domain"].strip().strip("/")
SITE["year"] = date.today().year
SITE["version"] = date.today().strftime("%Y%m%d")

# Links to these hosts always get rel="nofollow" (competitors of the partner).
NOFOLLOW_HOSTS = set(SITE.get("nofollow_hosts", []))
# Followed links: the partner and app stores.
FOLLOW_HOSTS = set(SITE["partner"]["hosts"]) | set(SITE.get("follow_hosts_extra", []))
if NOFOLLOW_HOSTS & FOLLOW_HOSTS:
    sys.exit(f"Host in both follow and nofollow lists: {NOFOLLOW_HOSTS & FOLLOW_HOSTS}")

META_RE = re.compile(r"<!--META\s*(\{.*?\})\s*-->", re.S)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’+.\-]*")

env = Environment(loader=FileSystemLoader(str(SRC / "templates")), autoescape=False)


def host_of(href):
    h = (urlparse(href).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def matches(host, pool):
    return any(host == d or host.endswith("." + d) for d in pool)


def process_links(soup, report):
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("http"):
            continue
        host = host_of(href)
        if matches(host, NOFOLLOW_HOSTS):
            a["rel"] = "nofollow noopener"
            report["nofollow"] += 1
        elif matches(host, FOLLOW_HOSTS):
            a["rel"] = "noopener"
            report["follow"] += 1
        else:
            a["rel"] = "noopener"
        a["target"] = "_blank"


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = META_RE.search(raw)
    if not m:
        sys.exit(f"Missing META in {path}")
    meta = json.loads(m.group(1))
    body = raw[m.end():].strip()
    hero = ""
    if "<!--HERO-->" in body:
        hero, body = body.split("<!--HERO-->", 1)
    return meta, hero.strip(), body.strip()


def word_count(fragment):
    text = BeautifulSoup(fragment, "html.parser").get_text(" ")
    return len(WORD_RE.findall(text))


def build_toc(soup):
    toc = []
    for h2 in soup.find_all("h2"):
        if not h2.get("id"):
            slug = re.sub(r"[^a-z0-9]+", "-", h2.get_text().lower()).strip("-")[:60]
            h2["id"] = slug
        toc.append({"id": h2["id"], "label": h2.get_text(" ", strip=True)})
    return toc


def faq_schema(soup):
    items = []
    for d in soup.select("details.faq-item"):
        q = d.find("summary").get_text(" ", strip=True)
        a = d.select_one(".faq-a").get_text(" ", strip=True)
        items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    if not items:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}


def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": c["name"], "item": SITE["url"] + c["url"]}
        for i, c in enumerate(crumbs)]}


def article_schema(meta, url):
    return {"@context": "https://schema.org", "@type": "Article", "headline": meta["h1"],
            "description": meta["description"], "datePublished": meta.get("date"),
            "dateModified": meta.get("updated", meta.get("date")), "mainEntityOfPage": SITE["url"] + url,
            "image": SITE["url"] + "/assets/img/og.png",
            "author": {"@type": "Organization", "name": SITE["name"] + " " + SITE.get("author", "Editorial team"), "url": SITE["url"] + "/about/"},
            "publisher": {"@type": "Organization", "name": SITE["name"], "logo": {"@type": "ImageObject", "url": SITE["url"] + "/assets/img/logo.png"}}}


def load_providers():
    data = json.loads((SRC / "data" / "providers.json").read_text(encoding="utf-8"))
    for p in data["providers"]:
        p["score"] = round(sum(p["scores"]) / len(p["scores"]), 1)
        if p.get("color"):
            widgets.COLORS[p["slug"]] = p["color"]
    data["providers"].sort(key=lambda p: -sum(p["scores"]))
    return data


def ranking_cards(data):
    out = ['<div class="rank-list">']
    for i, p in enumerate(data["providers"], 1):
        top = i == 1
        crit = "".join(
            f'<div class="crit"><div class="crit-row"><span>{c}</span><b>{s:.1f}</b></div><div class="bar"><i style="width:{s * 10:.0f}%"></i></div></div>'
            for c, s in zip(data["criteria"], p["scores"]))
        facts = "".join(f'<span class="chip">{f}</span>' for f in p["facts"])
        pros = "".join(f"<li>{x}</li>" for x in p["pros"])
        cons = "".join(f"<li>{x}</li>" for x in p["cons"])
        btn = "btn-primary" if top else "btn-ghost"
        badge = '<span class="badge badge-top">Editor\'s choice</span> ' if top else ""
        out.append(
            f'<section class="rank-card{" is-top" if top else ""}" id="{p["slug"]}">'
            f'<div class="rank-num">{i}</div>'
            f'<div class="rank-main">{badge}<h3 class="rank-title">{widgets.mono(p["slug"], p["name"])}{p["name"]}</h3><p class="rank-tag">{p["tag"]}. Best for: {p["best_for"].lower()}.</p>'
            f'<div class="facts">{facts}</div><p>{p["summary"]}</p><div class="criteria">{crit}</div>'
            f'<div class="proscons"><div class="pros"><p class="pc-title">Pros</p><ul>{pros}</ul></div>'
            f'<div class="cons"><p class="pc-title">Cons</p><ul>{cons}</ul></div></div></div>'
            f'<div class="rank-side"><div class="score-ring lg{" top" if top else ""}" style="--v:{p["score"] * 10:.0f}"><span>{p["score"]:.1f}</span></div>'
            f'<small>Editorial score out of 10</small><a class="btn {btn}" href="{p["url"]}">{p["cta"]}</a></div></section>')
    out.append("</div>")
    return "".join(out)


def ranking_table(data):
    head = "".join(f"<th>{c}</th>" for c in data["criteria"])
    rows = []
    for i, p in enumerate(data["providers"], 1):
        cells = "".join(f"<td>{s:.1f}</td>" for s in p["scores"])
        rows.append(f'<tr{" class=is-top" if i == 1 else ""}><td><span class="cell-prov">{i}. {widgets.mono(p["slug"], p["name"], "sm")}<a href="#{p["slug"]}">{p["name"]}</a></span></td><td><b>{p["score"]:.1f}</b></td>{cells}</tr>')
    return ('<div class="table-wrap"><table class="data-table"><thead><tr><th>Provider</th><th>Score</th>'
            + head + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def ranking_schema(data):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": SITE["rating"]["title"],
            "itemListOrder": "https://schema.org/ItemListOrderDescending",
            "itemListElement": [{"@type": "ListItem", "position": i, "name": p["name"], "url": p["url"]}
                                for i, p in enumerate(data["providers"], 1)]}


def fmt_date(d):
    x = date.fromisoformat(d)
    return f"{x.strftime('%b')} {x.day}, {x.year}"


def render(meta, hero, body, url, kind, crumbs, posts, extra_schema=()):
    report = {"nofollow": 0, "follow": 0}
    body = widgets.expand(body, PROVIDERS, POSTS)
    hero = widgets.expand(hero, PROVIDERS, POSTS)
    if visuals:
        body, hero = visuals.expand(body, SITE), visuals.expand(hero, SITE)
    soup = BeautifulSoup(body, "html.parser")
    for box in soup.select("aside.pick-box"):
        box.replace_with(BeautifulSoup(widgets.mini_rating(PROVIDERS, 3, SITE["rating"]["article_title"]), "html.parser"))
    hero_soup = BeautifulSoup(hero, "html.parser")
    process_links(soup, report)
    process_links(hero_soup, report)
    toc = build_toc(soup) if meta.get("toc", kind in ("post", "home", "rating")) else []
    schema = [json.dumps(s, ensure_ascii=False) for s in extra_schema]
    if kind in ("post", "home"):
        schema.append(json.dumps(article_schema(meta, url), ensure_ascii=False))
    fs = faq_schema(soup)
    if fs:
        schema.append(json.dumps(fs, ensure_ascii=False))
    if len(crumbs) > 1:
        schema.append(json.dumps(crumbs_schema(crumbs), ensure_ascii=False))

    parts = []
    if hero_soup.contents:
        parts.append(str(hero_soup))
    parts.append('<div class="wrap">')
    if len(crumbs) > 1:
        parts.append('<nav class="breadcrumbs" aria-label="Breadcrumbs">' + "".join(
            f'<span><a href="{c["url"]}">{html.escape(c["name"])}</a></span>' if i < len(crumbs) - 1 else f'<span>{html.escape(c["name"])}</span>'
            for i, c in enumerate(crumbs)) + "</nav>")
    if not hero_soup.contents and meta.get("h1"):
        upd = meta.get("updated") or meta.get("date")
        byline = ""
        if kind == "post":
            byline = (f'<div class="byline"><span class="avatar">{SITE.get("author_initials", "ED")}</span><span>By <strong>{SITE.get("author", "Editorial team")}</strong></span>'
                      f'<span>Updated {fmt_date(upd)}</span><span>{meta.get("read", "")} min read</span></div>')
        parts.append(f'<header class="page-head"><h1>{meta["h1"]}</h1>{byline}</header>')
    if toc:
        toc_html = "".join(f'<li><a href="#{t["id"]}">{html.escape(t["label"])}</a></li>' for t in toc)
        parts.append('<div class="layout"><article class="article">' + str(soup) + "</article>"
                     '<aside class="toc-wrap"><nav class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>'
                     + toc_html + '</ol></nav>' + widgets.mini_rating(PROVIDERS, 3, SITE["rating"]["sidebar_title"], compact=True) + '</aside></div>')
    else:
        parts.append(f'<div class="layout {"wide" if meta.get("wide") else "no-toc"}"><article class="article prose">' + str(soup) + "</article></div>")
    parts.append("</div>")

    page = dict(meta, url=url, kind=kind)
    out = env.get_template("base.html").render(page=page, site=SITE, content="\n".join(parts), schema=schema, posts=posts)
    target = DIST / url.strip("/") / "index.html" if url != "/404.html" else DIST / "404.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return report


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(SRC / "assets", DIST / "assets")
    global PROVIDERS
    PROVIDERS = load_providers()
    widgets.CFG = SITE
    widgets.COVER = visuals.cover

    posts = []
    for f in sorted((SRC / "content" / "blog").glob("*.html")):
        meta, hero, body = parse(f)
        wc = word_count(body)
        meta.setdefault("read", max(3, round(wc / 230)))
        scene_ph = f'<!--VISUAL {meta["scene"]}|-->' if meta.get("scene") else ""
        body = scene_ph + body
        posts.append({"meta": meta, "hero": hero, "body": body, "slug": f.stem, "url": f"/blog/{f.stem}/",
                      "short": meta.get("short", meta["h1"]), "words": wc})
    posts.sort(key=lambda p: p["meta"].get("order", 99))
    nav_posts = [{"url": p["url"], "short": p["short"]} for p in posts]
    global POSTS
    POSTS = posts

    site_schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": SITE["url"] + "/"},
                   {"@context": "https://schema.org", "@type": "Organization", "name": SITE["name"], "url": SITE["url"] + "/",
                    "logo": SITE["url"] + "/assets/img/logo.png"}]

    pages = []
    totals = {"nofollow": 0, "follow": 0}
    log = []
    for f in sorted((SRC / "content" / "pages").glob("*.html")):
        meta, hero, body = parse(f)
        url = meta["url"]
        kind = meta.get("kind", "page")
        crumbs = [{"name": "Home", "url": "/"}] + ([] if url == "/" else [{"name": meta.get("crumb", meta["h1"]), "url": url}])
        extra = site_schema if url == "/" else []
        if "<!--RANKING-->" in body or "<!--RANKTABLE-->" in body:
            body = body.replace("<!--RANKING-->", ranking_cards(PROVIDERS)).replace("<!--RANKTABLE-->", ranking_table(PROVIDERS))
            if kind == "rating":
                extra = [ranking_schema(PROVIDERS)]
        if url == "/blog/":
            cards = []
            for i, p in enumerate(posts):
                m = p["meta"]
                cards.append(f'<a class="post-card" href="{p["url"]}"><div class="post-cover">{visuals.cover(m)}</div>'
                             f'<div class="post-body"><span class="badge badge-accent">{m.get("category", "Guide")}</span><h3>{m["h1"]}</h3>'
                             f'<p>{m.get("excerpt", "")}</p><span class="post-meta">{m["read"]} min read / Updated {fmt_date(m.get("updated", m["date"]))}</span></div></a>')
            body = body.replace("<!--POSTS-->", '<div class="post-grid">' + "".join(cards) + "</div>")
        r = render(meta, hero, body, url, kind, crumbs, nav_posts, extra)
        for k in totals:
            totals[k] += r[k]
        pages.append({"url": url, "updated": meta.get("updated", meta.get("date", SITE["version"])), "noindex": meta.get("noindex")})
        log.append((url, word_count(hero + body)))

    for p in posts:
        crumbs = [{"name": "Home", "url": "/"}, {"name": "Guides", "url": "/blog/"}, {"name": p["short"], "url": p["url"]}]
        r = render(dict(p["meta"], nav="blog"), p["hero"], p["body"], p["url"], "post", crumbs, nav_posts)
        for k in totals:
            totals[k] += r[k]
        pages.append({"url": p["url"], "updated": p["meta"].get("updated", p["meta"]["date"])})
        log.append((p["url"], p["words"]))

    # sitemap, robots, CNAME
    urls = "".join(f"<url><loc>{SITE['url']}{p['url']}</loc><lastmod>{p['updated']}</lastmod></url>"
                   for p in pages if not p.get("noindex") and p["url"] != "/404.html")
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>'
                                      f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    # Cloudflare Pages: security and cache headers
    (DIST / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n"
        "/assets/*\n  Cache-Control: public, max-age=604800\n", encoding="utf-8")

    print("Built pages (words):")
    for u, w in log:
        print(f"  {u:55s} {w}")
    print(f"External links: followed partner={totals['follow']}, nofollow competitor={totals['nofollow']}")


if __name__ == "__main__":
    main()
