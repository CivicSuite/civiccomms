"""Accessible public sample UI for CivicComms."""


def render_public_lookup_page() -> str:
    """Return a static, dependency-free HTML page for browser QA."""

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<title>CivicComms - public explainer support</title>
<style>
:root{--ink:#17202a;--blue:#174f6f;--gold:#d7a94b;--paper:#fffaf0}
body{margin:0;font-family:"Aptos","Segoe UI",sans-serif;color:var(--ink);background:linear-gradient(135deg,#eef8ff,var(--paper))}
header,main,footer{width:min(1080px,calc(100% - 32px));margin:auto}
header{padding:52px 0 20px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;color:var(--blue);font-weight:900}
h1{font:700 clamp(2.35rem,7vw,5.4rem)/.95 Georgia,serif;margin:.1em 0}.lede{font-size:1.2rem;line-height:1.6;max-width:820px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.card{background:rgba(255,255,255,.9);border:1px solid #dac7a4;border-radius:24px;padding:24px;box-shadow:0 18px 36px #26323b18}
.badge{display:inline-block;background:var(--blue);color:white;padding:.5rem .85rem;border-radius:999px;font-weight:900}
:focus-visible{outline:4px solid var(--gold);outline-offset:3px}@media(max-width:720px){.grid{grid-template-columns:1fr}header{padding-top:34px}}
</style>
</head>
<body>
<header>
  <p class="eyebrow">CivicSuite / CivicComms</p>
  <h1>Public explanations with sources attached.</h1>
  <p class="lede">CivicComms v0.1.1 helps staff shape meeting summaries, ordinance explainers, newsletters, FAQs, and audience variants from named municipal source material.</p>
  <p><span class="badge">Shipping v0.1.1</span></p>
</header>
<main>
  <section class="grid" aria-label="CivicComms release status">
    <article class="card"><h2>What ships</h2><ul><li>Source-readiness review.</li><li>Meeting summary draft outlines.</li><li>Ordinance plain-language explainer drafts.</li><li>Newsletter and FAQ draft scaffolds.</li><li>Audience-specific variant drafts.</li></ul></article>
    <article class="card"><h2>Human approval required</h2><p>Every draft must be reviewed, cited, edited, and published by staff. CivicComms does not autonomously publish or post content.</p></article>
    <article class="card"><h2>Boundaries</h2><p>No campaign or advocacy content, no legal advice, no certified translation, no live LLM calls, and no communications system-of-record integrations ship in v0.1.1.</p></article>
    <article class="card"><h2>Dependency</h2><p>Pinned to <code>civiccore==0.3.0</code>. CivicCore remains dependency-only; it never imports from CivicComms.</p></article>
  </section>
</main>
<footer><p>Apache 2.0 code. CC BY 4.0 docs. Run locally by the city.</p></footer>
</body>
</html>"""
