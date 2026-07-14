# Element Toolbox — use the native element instead of building it

For each common need, the semantic HTML element that already does it, and the behavior + accessibility
you inherit for free by using it. Reaching for `<div>` + CSS + JS instead means reimplementing (usually
worse) what the browser already ships.

## Page structure (landmarks)

| Need | Element | You get for free |
|---|---|---|
| Page banner / masthead | `<header>` | Landmark role; screen readers can jump to it |
| Primary content | `<main>` (once per page) | "Skip to main" target; the `main` landmark |
| Site/section navigation | `<nav>` around a `<ul>` of links | Navigation landmark; announced as such |
| Standalone piece (post, card, comment) | `<article>` | Article role; self-contained outline |
| Thematic grouping | `<section>` (with a heading) | Region in the outline |
| Tangential content | `<aside>` | Complementary landmark |
| Page footer | `<footer>` | Contentinfo landmark |

## Text & content

| Need | Element | Notes |
|---|---|---|
| Title / heading hierarchy | `<h1>`–`<h6>` | One `<h1>`; don't skip levels; this is the accessible outline |
| Paragraph | `<p>` | Default vertical margins give rhythm |
| Emphasis (spoken stress) | `<em>` | Italic + semantic emphasis |
| Strong importance | `<strong>` | Bold + semantic weight |
| Highlight / relevance | `<mark>` | Yellow highlight by default |
| Key–value / metadata pairs | `<dl>`,`<dt>`,`<dd>` | Purpose-built for term→definition |
| Ordered steps | `<ol>` | Auto-numbered; renumbers on edit |
| Unordered list | `<ul>` | Scannable; default indentation |
| Quotation (block) | `<blockquote>` + `<cite>` | Indented; cite the source |
| Inline quote | `<q>` | Adds locale-correct quotation marks |
| Code | `<code>`, block via `<pre><code>` | Monospace; `<pre>` preserves whitespace |
| Abbreviation | `<abbr title="…">` | Tooltip + screen-reader expansion |
| Thematic break | `<hr>` | A real section divider, not decoration |
| Time / date | `<time datetime="…">` | Machine-readable date |

## Interactive — native, no JavaScript

| Need | Element | Why not a div |
|---|---|---|
| Collapsible / accordion | `<details><summary>` | Open/close, keyboard, and state built in — zero JS |
| Modal dialog | `<dialog>` + `.showModal()` | Focus trapping, backdrop, Esc-to-close handled by the browser |
| Button / action | `<button>` | Focusable, Enter/Space activation, announced as a button |
| Link / navigation | `<a href>` | The web's primitive; works with keyboard, middle-click, right-click |
| Disclosure of long text | `<details>` | Progressive disclosure without scripting |
| Progress / loading | `<progress value max>` | Native bar, announced to AT |
| Scalar measurement | `<meter value min max>` | Gauge for a known-range value (disk usage, score) |

## Forms — the biggest free-behavior win

Use `<form>`, and for **every** control a `<label for="id">` (or wrap the control in the label). Group
related controls with `<fieldset>` + `<legend>`.

| Need | Element / attribute | Free behavior |
|---|---|---|
| Text, email, URL, number, phone | `<input type="text|email|url|number|tel">` | Correct mobile keyboard + built-in validation |
| Date / time | `<input type="date|time|datetime-local">` | Native picker, no JS date library |
| Search box | `<input type="search">` | Clear button, search semantics |
| Choice from a list | `<select>` / `<option>` | Native dropdown, keyboard support |
| One of several | `<input type="radio" name="…">` | Grouping by shared `name`, arrow-key nav |
| Toggle | `<input type="checkbox">` | Native checkbox, Space to toggle |
| Multi-line text | `<textarea>` | Resizable input |
| Autocomplete from suggestions | `<input list>` + `<datalist>` | Suggestions without JS |
| Required / pattern / min / max | attributes on `<input>` | Client-side validation with no code |
| Submit | `<button type="submit">` | Enter-to-submit from any field |

Attributes worth using: `required`, `placeholder` (not a label substitute), `autocomplete`,
`inputmode`, `min`/`max`/`step`, `pattern`, `readonly`, `disabled`.

## Media

| Need | Element | Notes |
|---|---|---|
| Image | `<img src alt>` | `alt` is mandatory (empty `alt=""` if purely decorative) |
| Image + caption | `<figure><img><figcaption>` | Caption associated with the image |
| Responsive image | `<img>` + `srcset`/`sizes`, or `<picture>` | Serve the right size without JS |
| Video / audio | `<video controls>` / `<audio controls>` | Native player, keyboard, captions via `<track>` |

## The rule of thumb

If you're about to write `<div class="something">` and then style/script it into acting like one of the
things above — stop, and use the real element. It will be shorter, work without CSS or JS, and be
accessible by default. `<div>` and `<span>` are for the genuinely non-semantic leftover grouping only.
