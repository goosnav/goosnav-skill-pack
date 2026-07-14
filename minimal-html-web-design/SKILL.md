---
name: minimal-html-web-design
description: >-
  Build web pages with plain, semantic HTML and little to no CSS -- highly functional, fast,
  accessible, and still intelligently organized. Use when the user wants "just HTML", "no CSS", "no
  framework", "minimal", "plain", "barebones", "lightweight", "document-style", "brutalist/plain
  site", or a page that must work everywhere, load instantly, and stay maintainable without a build
  step. The philosophy: the browser is already a competent typesetter and layout engine, so lean on
  semantic elements and native controls, order the source so it reads correctly top-to-bottom, and add
  at most a tiny optional stylesheet for line length and breathing room. Choose this over
  aesthetic-web-design when function, portability, and simplicity beat visual art direction.
---

# Minimal HTML Web Design

## What this is for

Make pages out of correct, semantic HTML — the kind that works in every browser, loads instantly,
prints well, reads perfectly in a screen reader, and never rots because there's no framework, build
step, or design system to maintain. "Minimal" here does not mean ugly or unstructured. It means the
*structure* carries the design: well-chosen elements in a sensible order look organized on their own,
because the browser's default stylesheet is already good.

The default is **zero custom CSS**. If a little is warranted, it's a tiny classless baseline (line
length, font, spacing) — never a framework, grid system, or a wall of utility classes.

## The core idea

Two things the browser already does for free, that most sites reimplement badly:

1. **HTML is a layout system.** Block elements stack vertically in source order; the reading order of
   your markup *is* the visual order of the page. Organize the page by writing the document in the
   order a person should read it. No positioning required.
2. **The browser is a typesetter.** Default margins, heading sizes, list indentation, table borders,
   and form controls are sane and consistent. Semantic elements come pre-styled and
   pre-accessible. Reaching for a `<div>` + CSS throws that away.

So the whole method is: **pick the right element, put it in the right place in the source, and stop.**

## Workflow

### 1. Write the document outline first

Before markup, list the page's sections in reading order: what's the title, what's the primary
content, what's secondary, what's navigation, what's the footer. That outline *is* your layout. On a
single-column document, top-to-bottom source order handles all "placement" — put the most important
thing first.

### 2. Build the semantic skeleton

Use landmark elements so the page has structure a browser and screen reader understand:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Clear, specific page title</title>
</head>
<body>
  <header>…site title + <nav>…</header>
  <main>…the page's primary content lives here, exactly once…</main>
  <footer>…</footer>
</body>
</html>
```

`<!doctype html>`, `lang`, `<meta charset>`, `<meta viewport>`, and a real `<title>` are non-negotiable
even in the most minimal page — they're what make defaults work and the page render correctly on
mobile.

### 3. Use one `<h1>`, then nest headings truthfully

Exactly one `<h1>` (the page's subject). Section headings are `<h2>`, sub-points `<h3>`, and so on
**without skipping levels**. The heading hierarchy is simultaneously the visual hierarchy and the
document's accessible outline — get it right and the page is already organized. Never pick a heading
level for its default size; pick it for its meaning.

### 4. Reach for the native element every time

The browser has a built-in element for most things people build with `<div>`s and JavaScript. Prefer
it — you get behavior, styling, and accessibility for free. See `references/element-toolbox.md` for the
full map. Highlights:

- **Collapsible sections:** `<details><summary>` — no JS needed.
- **Tabular data:** `<table>` with `<thead>`/`<tbody>`/`<th scope>` — never fake a table with divs.
- **Forms:** `<form>` with `<label for>` on every field, `<fieldset>`/`<legend>` to group,
  `<input type="email|date|number|search|…">` for the right keyboard and validation, `<button>` (not a
  styled `<div>`).
- **Term/definition lists:** `<dl><dt><dd>` for key–value content.
- **Figures & captions:** `<figure><figcaption>`.
- **Quotes:** `<blockquote>`, `<cite>`. **Code:** `<pre><code>`.
- **Navigation:** `<nav>` wrapping a `<ul>` of links.
- **Emphasis with meaning:** `<strong>`, `<em>`, `<mark>` — semantic, and styled by default.

### 5. Organize placement with structure, not positioning

Even without CSS you have real organizational tools:

- **Order** — source order is reading order; lead with what matters.
- **Grouping** — wrap related content in `<section>`/`<article>` with its own heading so the outline
  shows the grouping.
- **Lists** — `<ul>`/`<ol>` turn prose into scannable structure; `<ol>` when sequence matters.
- **Tables** — genuine two-dimensional data lays out itself.
- **Horizontal rules** — `<hr>` for a real thematic break between sections.
- **Whitespace** — comes for free from default block margins between elements; don't fight it.

### 6. (Optional) add the tiny baseline stylesheet

If — and only if — the user is open to a touch of CSS, add the ~15-line baseline in
`references/baseline.css`. It does four humane things and nothing else: caps line length
(`max-width` on a wrapper) so text isn't unreadable full-width, sets a comfortable system font and
line-height, adds a little page padding, and makes images responsive. It uses **element selectors
only — no classes, no framework, no layout system.** That is the ceiling for this skill. If the design
truly needs art direction, that's the `aesthetic-web-design` skill instead.

### 7. Verify it actually works

- Loads and renders with a real, specific `<title>` and no console errors.
- **Works with CSS disabled** — this is the real test; it should still be fully usable and ordered.
- Keyboard-navigable: Tab reaches every link/control in a sensible order; `<summary>`, buttons, and
  inputs all operate.
- Passes the W3C HTML validator (or at least: closed tags, one `<h1>`, labels on inputs, `alt` on
  images).

## What NOT to do

- **No `<div>`/`<span>` soup** where a semantic element exists. A `<div class="nav">` should be `<nav>`.
- **No classes or IDs for styling** in this skill — if you're naming things to style them, you've left
  minimal-HTML territory.
- **No inline `style=` attributes**, no `<center>`, no `<font>`, no layout tables.
- **No JavaScript for things HTML does** — disclosure, form validation, navigation, and links all work
  without it. Add JS only for genuine interactivity that has no HTML equivalent.
- **No frameworks, no CSS resets, no build step.** A single `.html` file you can open with `file://` is
  the ideal deliverable.
- **Don't skip heading levels** or use headings for their size.

## Operating principles

- **Semantics first.** The right element is more readable, more accessible, more maintainable, and
  better-looking-by-default than a styled generic box.
- **Source order is layout.** Organize by writing the document in reading order; the single column is a
  feature, not a limitation.
- **Defaults are good.** The browser's built-in stylesheet is the work of decades. Inherit it instead
  of overriding it.
- **Accessibility is automatic when you're honest.** Correct headings, labels, `alt` text, and landmark
  elements give you an accessible page with no extra effort.
- **Less to break.** No CSS and no build means nothing to rot, nothing to debug, instant load, and it
  works on any device forever.

## Reference files

- `references/element-toolbox.md` — the "use this native element instead of building it" map, with the
  behavior and accessibility you get for free from each.
- `references/baseline.css` — the optional ~15-line, class-free humane baseline (line length, font,
  spacing, responsive images). The maximum CSS this skill endorses.
- `references/example.html` — a complete, self-contained page (article + nav + table + form + details)
  built with this skill's method, correct and usable with styles off.

## Verification checklist

- [ ] Valid `<!doctype html>`, `lang`, `charset`, `viewport`, and a specific `<title>`.
- [ ] Landmarks present: `<header>`, `<main>` (once), `<footer>`; `<nav>` around navigation.
- [ ] Exactly one `<h1>`; heading levels nest without skipping.
- [ ] Every interactive/data need uses its native element (details, table, form, button, dl…).
- [ ] Every form control has a `<label>`; every `<img>` has `alt`.
- [ ] The page is fully usable and correctly ordered **with CSS disabled**.
- [ ] No div/span soup, no classes-for-styling, no inline styles, no layout tables, no framework.
- [ ] If used, CSS is only the class-free baseline — element selectors, nothing more.
