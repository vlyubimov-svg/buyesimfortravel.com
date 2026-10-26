# Content components (HTML fragments)

This is the markup contract between content files and build.py. The class names are shared; how each component LOOKS is defined by every site's own CSS and must differ between sites (see DESIGN.md in the skill). You may add new site-specific components; document them at the bottom of this file in the site repo.

Every content file is an HTML fragment (no <html>, <head>, <body>). The first line is a META comment with JSON:

<!--META {"title":"<title tag, 50-60 chars>","description":"<meta description, 140-160 chars>","h1":"<H1>","date":"2026-10-27","updated":"2026-10-27","category":"Guides","excerpt":"<1-2 sentence card excerpt>"} -->

Then the body. The template adds H1, breadcrumbs, author line, TOC (built from h2 ids), schema (Article + FAQPage built from .faq-item) and the footer. Do not add them yourself.

Rules:
- Every <h2> needs a unique kebab-case id: <h2 id="how-to-check">…</h2>
- Use h3 inside sections. No h1.
- Lead paragraph first: <p class="lead">…</p> (answer the query in 2-3 sentences).
- Short paragraphs (max 3 sentences). Mix components; avoid long runs of plain paragraphs.
- Write menu paths with the path component, never with arrows.
- No em-dash chains; prefer commas and periods. No emoji.

## Components

Key takeaways
<div class="takeaways"><p class="takeaways-title">Key takeaways</p><ul><li>…</li></ul></div>

Callout (tip | warn | info)
<div class="callout callout-tip"><p class="callout-title">Tip</p><p>…</p></div>

Menu path
<span class="path"><span>Settings</span><span>Cellular</span><span>Add eSIM</span></span>

Numbered step cards
<ol class="steps"><li><h3>Step title</h3><p>…</p></li></ol>

Data table
<div class="table-wrap"><table class="data-table"><thead><tr><th>…</th></tr></thead><tbody><tr><td>…</td></tr></tbody></table></div>
Yes/No cells: <span class="yes">Yes</span> / <span class="no">No</span> / <span class="part">Partial</span>

Checklist
<ul class="checklist"><li>…</li></ul>

Pros and cons
<div class="proscons"><div class="pros"><p class="pc-title">Pros</p><ul><li>…</li></ul></div><div class="cons"><p class="pc-title">Cons</p><ul><li>…</li></ul></div></div>

Stat row (3-4 items)
<div class="stats"><div class="stat"><span class="stat-num">180+</span><span class="stat-label">Countries covered</span></div></div>

Card grid (2-4 cards)
<div class="card-grid"><div class="card"><p class="card-kicker">Light use</p><h3>…</h3><p>…</p></div></div>

Side-by-side comparison
<div class="vs"><div class="vs-col"><p class="vs-title">eSIM</p><ul><li>…</li></ul></div><div class="vs-col"><p class="vs-title">Roaming</p><ul><li>…</li></ul></div></div>

Pick box (one per article; build.py replaces it with a neutral top-3 mini rating)
<aside class="pick-box"><div class="pick-body"><p class="pick-label">Our top pick for iPhone</p><p class="pick-name">Partner</p><p>…one or two sentences tied to the section topic…</p></div><a class="btn btn-primary" href="https://partner.com/">CTA</a></aside>

Internal link box
<div class="related"><p class="related-title">Related</p><ul><li><a href="/rating/">eSIM provider rating</a></li></ul></div>

FAQ (always last section, 5-7 questions)
<section class="faq"><h2 id="faq">FAQ</h2>
<details class="faq-item"><summary>Question?</summary><div class="faq-a"><p>Answer, 2-3 sentences, self-contained.</p></div></details>
</section>

## Generated widgets (placeholders, replaced at build time)

Phone mockup figure (names: cellular, travel-line, add-esim, about, no-service, usage, checkout). Optional: style it to fit the site, or build topic-specific visuals in src/visuals.py instead.
<!--PHONE add-esim|Optional caption under the phone.-->

Mini rating, top n providers from src/data/providers.json (default 5)
<!--MINIRATING 3-->

Top-3 podium (rating hero), latest 3 guides grid
<!--PODIUM-->  <!--LATEST-->

Interactive tools: copy the markup of `.tool[data-checker]` (iPhone eSIM checker) or `.tool[data-calc]` (trip data calculator) from examples/bestesimforiphone/content/pages/home.html. The JS in assets/js/main.js picks them up automatically.

Note: any `<aside class="pick-box">` is automatically replaced by a neutral top-3 mini rating at build time, so articles never show a single-provider sales block.

## Internal URLs (fixed by the engine)
- / pillar article, /rating/, /blog/, /blog/<slug>/, /methodology/, /glossary/, /about/, /contact/, /disclosure/, /privacy/, /terms/, /404.html
