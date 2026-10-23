# Implementation contract

## Web starter

Copy `assets/evangelion.css`, `assets/noise.svg`, and the `assets/fonts/` folder (including its OFL license) next to each other in the product's asset tree. Import the CSS after a reset or incorporate it into existing component styles. Scope an application region with `class="eva" data-palette="classic-amber" data-analog="subtle" data-density="comfortable"`. Use `.eva-screen` as an isolated relative wrapper with a direct `.eva-content` child. Pseudo-elements are presentation-only and pointer-transparent; ensure modal portals get theme tokens too. The stylesheet has no network, framework, font-service, or JavaScript dependencies. It includes Barlow Condensed Bold under the SIL Open Font License; preserve `fonts/OFL.txt`. The specimen uses local vanilla JavaScript. Keep the SVG path valid after bundling; inline or fingerprint it using the app's asset pipeline if needed.

Tokens on `.eva` include `--eva-primary`, `--eva-secondary`, `--eva-text`, `--eva-muted`, `--eva-bg`, `--eva-surface`, `--eva-warning`, `--eva-danger`, `--eva-success`, `--eva-border`, `--eva-focus`, `--eva-font-heading`, `--eva-font-body`, `--eva-font-mono`, `--eva-scale`, `--eva-space`, `--eva-scanline`, `--eva-grain`, `--eva-vignette`, `--eva-glow`. Override custom values on the theme root. Palette attributes set defaults; inline tokens or a later equal/more-specific rule override them. Numeric effect strengths are opacity fractions (glow uses px). Clamp user input to sensible bounds; off overrides individual effects. Never accept arbitrary CSS strings from untrusted external content.

Use the component classes as primitives, not compulsory markup. Preserve semantic headings, navigation, tables, buttons, labels and inputs. The starter includes native textarea, field/error/help, unknown/pending status, disabled-control and navigation patterns; see `assets/inspector.html` for a complete working example. Use logical properties and wrapping labels. Avoid line-clamping essential titles. Use `minmax(0,1fr)` tracks; permit horizontal scrolling only inside genuinely two-dimensional tables/plots. Mobile reorganizes reading order and secondary panels rather than shrinking the whole interface. Use real `<meter>` for a bounded measurement and `<progress>` for work completion, with textual values and units. Custom segmented instruments must retain equivalent semantics.

## Data and states

During development keep a short source mapping in implementation notes, existing docs, or typed component props: visible element -> source field/derivation -> unit -> missing/stale behavior. Do not show this internal mapping in ordinary product UI. Round only to warranted precision. Display measurement time versus current time correctly. Never use `Math.random()` for presented telemetry. Never label a browser timer as hardware latency or system uptime.

Implement empty, loading, error, disconnected/stale where applicable, and populated states. Render `—` with an explanation when data is unavailable, not 0. A UI preview can use truthful local input and computed values; mock business data requires visible Sample/Demo labeling and user authorization where not already implied by a mockup task. Status color and animation follow actual state transitions.

## Analog rendering budget

Subtle defaults: scanline .10, grain .035, vignette .18, glow 3px at low alpha. Cinematic ceilings should normally stay near scanline .16, grain .065, vignette .25, glow 5px. These are perceptual starting points; verify at actual display scale. No whole-screen blur. Keep grain static and cheap. Use no per-frame JS for analog effects. Apply text glow to headings/readings, not all paragraphs. Use a local SVG/canvas duplicate stroke for real trace afterglow only when profiling supports it.

Do not animate `filter`, large shadows, or full-screen noise. If optional animated effects are specifically requested, constrain their layers and opacity, use a pause/disable control, honor reduced motion, stop when hidden, and profile a representative mobile viewport. Do not animate fake data. Native apps should use equivalent compositing behind accessible native controls; retain native keyboard, IME, selection, scaling, and focus behavior.

## Typography and quality

Prefer project-supplied fonts. Bundle a licensed condensed font only when available and useful; do not silently rely on a network font request. Verify `document.fonts` plus the rendered screenshot. Keep font licensing intact. The CSS fallbacks are intentionally portable; they still require visual inspection because machines differ.

Meet 4.5:1 for ordinary text, 3:1 for large text and meaningful control boundaries/focus. Measure foreground against its actual composed background, including effects and selection. Do not assume preset names prove contrast. If user colors fail, preserve their hue where possible while adjusting text or separating a color fill from text. Always use a label/icon for status; color alone is insufficient.

## Working specimen

Open `assets/specimen.html` locally to inspect the starter. It contains a stopwatch based on monotonic elapsed time, actual browser-local display preferences, and a live summary of those preferences. It does not simulate external telemetry. Test palette/effect changes, start/pause/reset, keyboard navigation, narrow layout, and effect-off behavior. Do not transplant the stopwatch into products that do not need it.

Use `assets/inspector.html` for a local file workflow. Keep its adjacent `inspector.css` and `inspector.js` when opening it. It demonstrates real input, syntax errors, invalidation after edits, truthful derived summaries, and exact-source download. Its analog wrapper covers only the masthead so controls and source text remain clean. Read [product-integration.md](product-integration.md) for brand composition and state rules.
