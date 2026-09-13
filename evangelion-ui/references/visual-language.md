# Visual language and screen atlas

## Composition

The recurring visual unit is an instrument face: a black ground, a precisely bounded area of responsibility, and an outsized label or reading. Use 1–2 px rules at normal CSS scale, 0–2 px corner radii, 4/8/12/16/24/32 px spacing, and 12–24 px panel gutters. Attach caption plates to rules or panel edges. Prefer one strong horizontal division and purposeful subordinate regions over a wallpaper of boxes. Let black occupy substantial space even on dense displays. Reference-derived measurements are starting values, not canonical production specifications.

Use an asymmetrical 2:1 or 3:2 main/secondary layout when the data warrants it. Keep one obvious dominant element per view: the current operation, a useful chart, a product title, or the primary task. A 4:3 inset can recall an instrument monitor; do not force a whole responsive application into a fixed 4:3 canvas. Do not rotate the interactive page just because a photographed screen is at an angle.

## Typography

Instrument title: naturally condensed heavy sans, approximately 28–56 px, tight leading and 0 to slightly negative tracking. Section captions: condensed medium/bold sans, 15–22 px. Micro-label: 11–13 px on secondary display annotations, with modest tracking; do not use micro-label sizes for essential form content. Body/control text: 14–18 px clear sans; long reading text: 16–20 px, 1.5–1.7 leading. Hero reading: 48–112 px responsive tabular numerals. Uppercase short captions; retain sentence case for explanations.

The starter bundles Barlow Condensed Bold with its license for deterministic headings. When adapting it, choose an available licensed condensed face (for example a project-bundled Barlow Condensed or Roboto Condensed) and verify the loaded font. Fallbacks: Arial Narrow / Liberation Sans Narrow / sans-serif. These are practical approximations, not claims about original production fonts. If the fallback is too wide, repair heading layout or load a suitable font; do not squeeze entire controls with CSS transforms. Keep a separate body stack and a monospace stack for genuinely tabular/technical identifiers. Seven-segment glyphs belong to real timers or numerical instruments only. A seven-segment display needs a plain-text accessible value; minutes/seconds and milliseconds must be truthful.

## Screen families

| Family | Reference grammar | Product translation | Avoid |
| --- | --- | --- | --- |
| Operations | Black fields, amber rules, oversized identifiers, strong status plates | Job queue, device list, inventory, command center | Fake health metrics or endless warnings |
| Analytical instrument | Amber traces, green fiducials, bounded axes, compact channel captions | Real sensor curves, plots, timelines, inspection tools | Random oscilloscope squiggles or spinning models |
| Resource/timer | Huge seven-segment numerals, subordinate mode selectors, colored limit bands | Actual stopwatch, time remaining, capacity, battery state | Invented countdowns and false precision |
| Approval network | Three chamfered panes around a named center, flat fills, orthogonal connectors | Actual review participants, dependencies, staged decisions | Forcing three fictitious services or votes |
| Emergency | Red/orange high-contrast status blocks, hazard edge, assertive type | Real failure, destructive action, blocking error | Permanent danger as a brand ornament |
| Editorial dossier | Huge compact title or deliberate serif title card, black space, white/amber facts | Portfolio, articles, product descriptions, case studies | Telemetry grafted onto ordinary prose |
| Spatial analysis | Wireframe objects, orbital paths, actual annotations, thin data leaders | Existing CAD, robotics transforms, maps or scientific objects | Decorative wireframe globe or meaningless coordinates |

Do not combine every family into one view. Use the dominant family for ~80% of the composition and secondary motifs only where the information calls for them. Three-panel approval geometry is a conditional pattern, not an app-wide card shape. Hexagonal grids are reserved for real networks or topology.

## Uploaded visual atlas

- `screens/IMG_8988.jpeg`: composite baseline; compare density, title/readout ratio, frame thickness, and black separation.
- `screens/IMG_8989.gif`: segmented channel bars; use for actual bounded scalar readings, preserving a numerical text equivalent and legend.
- `screens/IMG_8985.jpeg`: analytical trace, green fiducials, fine amber axes. Do not copy its fictional trace into an unrelated chart.
- `screens/IMG_8984.jpeg`: wider analytical framing and stronger bloom. Use cautiously; do not assume all supplied frames are from the classic TV master.
- `screens/IMG_8987.gif`: compartment states and red fault vocabulary. Distinguish a normal state from a real fault.
- `screens/IMG_8986.gif`: segmented countdown, flat mode plates, technical labels. Camera angle and severe transfer noise are reference context, not required interactions.
- `screens/IMG_8983.png`: dense wireframe analysis. Borrow hierarchy and line behavior only when there is genuine spatial data.

## Colors

Default: background #050605, surface #0b0e0b, text #ffe7b0, primary #ffb52e, secondary #70dfac, muted #b8ad94, border #9c742b, warning #ffd34d, danger #ff6255, success #8be09b, focus #e4fff2. These are authored starting tokens, not exact sampled canonical colors. Hot red can be a large alert fill with nearly black text; avoid small dark-red labels on black.

Most content should remain in background/text/primary. Secondary green or cyan identifies a second signal or active selection. Red occupies small meaningful areas until an actual emergency dominates. Large rainbow ramps only belong to quantitatively explained scales. Do not apply a rainbow to every control. Preset alternatives appear in the CSS; retain semantic status colors and explicit state labels.

## Analog rather than glossy digital

Model emitted light and a sampled display surface, not a transparent pane floating in space. Use a near-black warm ground; a crisp text core with a small low-opacity same-hue halo; scanlines spaced roughly 3–4 CSS px; faint grayscale grain; slight edge falloff. Saturation and bloom can be stronger on large numeric strokes than small prose. Prefer a static grain tile to changing random pixels every frame.

Cinematic can strengthen grain/bloom and use optional local trace afterglow, but leave essential text crisp. Strong curvature, VHS tracking damage, chromatic displacement, field jitter, and roll bars should be opt-in showcase treatments, localized away from controls. Never pulse the entire display, flash large bright fields, or add startup delay as mandatory theater. Actual sampled traces may update at their real source cadence; decorative texture must not make stale data seem live.
