---
name: evangelion-ui
description: Design and implement classic Neon Genesis Evangelion screen interfaces for websites and apps, with configurable palettes, authentic instrument typography, functional information design, and analog CRT rendering. Use for Evangelion, NERV, or MAGI interface styling and refinements explicitly seeking this aesthetic.
---

# Evangelion UI

Create interfaces that plausibly belong on a classic Evangelion operations display while serving the actual product. Target the 1995 television series and 1997 film's instrument language. Treat later glossy holographic interfaces as a different direction unless requested. Aim for close visual fidelity; never promise that a prompt guarantees identical results across agents.

## Work from the product and references

1. Inspect the existing framework, routes, controls, content, data sources, and brand requirements. Preserve working behavior. Use the project's stack; do not require React, a backend, shaders, or external services solely for styling.
2. Read [visual-language.md](references/visual-language.md) and inspect at least the composite reference plus one relevant close-up in `references/screens/`. For GIFs, inspect representative frames if image tools permit. Read [sources.md](references/sources.md) for provenance and broader screen families. Do not require network access to use this skill.
3. Select one dominant screen family suited to the task: operations, analytical instrument, approval network, resource/timer, or editorial dossier. State the intended hierarchy and palette briefly, then implement. Do not turn every product into a monitoring dashboard.
4. Read [implementation.md](references/implementation.md). Reuse/adapt `assets/evangelion.css` and `assets/noise.svg` for web implementations; translate the same tokens into native toolkit styles for native apps. `assets/specimen.html` is a functioning display-settings and stopwatch specimen, not a template that dictates product layout.
5. Build one complete primary view first. Establish its typography, spacing, panel rules, states, and analog treatment, then carry those components across the requested views. Avoid a collection of individually art-directed inconsistent pages.
6. Render and inspect using [quality-gate.md](references/quality-gate.md); correct visible failures before delivering. Report concrete checks and remaining limits. If screenshots cannot be produced, say visual validation is incomplete rather than implying it passed.

## Choose and compose variations

Read [variations.md](references/variations.md) before choosing a layout. Use the six independent CSS/HTML recipes in `assets/templates/` and eight data-free SVG primitives in `assets/graphics/` as a composable library. Choose structure from the task, not from the default palette. Adapt or create additional layouts when needed; never shoehorn every app into the original stopwatch specimen, a three-column dashboard, or a three-node MAGI arrangement. Keep shared tokens consistent across distinct page types.

## Essential visual invariants

- Use a nearly black field, luminous flat color, sharp rectangular instrument framing, narrowly set prominent headings, and a conspicuous scale contrast between small labels and large task-relevant values or titles.
- Compose dense information in deliberate regions with black breathing room. Use fine rules, attached caption plates, baseline alignment, aligned digits, and a few larger command surfaces. Avoid rounded SaaS cards, glass blur, floating translucent panels, generic cyan/purple cyberpunk glow, ornamental HUD circles, and omnipresent hexagons.
- Use condensed grotesque/sans typography for instrument headings; tabular numerals for readings; clear sans text for controls and prose. Large Mincho/serif title cards are an alternate editorial mode, not the default telemetry font. Never use stretched monospace for all text.
- Use color as information: primary structure, secondary signals, text, warning, danger, success, inactive, and selection have separate semantic tokens. Palette changes must preserve readable hierarchy and distinguish states with labels/icons as well as hue.
- Make the screen feel emitted: subtle phosphor bloom, fine scanlines, faint fixed-grain texture, restrained edge falloff, and optional subpixel color bleed. Preserve a sharp readable text core. Analog texture must not falsify measurements or interfere with controls.

## Truthful interface contract

Every visible number, chart, status, badge, identifier, and progress indicator must derive from a real application value, user input, static factual content, or an explicitly requested and visibly labeled demonstration dataset. Trace each datum to its source or derivation during implementation. Treat absent telemetry as unavailable, not zero or healthy. Show freshness/disconnection when relevant.

Do not invent sync percentages, sensor streams, security classifications, CPU readings, task counts, approval votes, command codes, timestamps, or warning messages to decorate the screen. Do not add meaningless Japanese, bogus scientific language, fake shell output, unexplained units, arbitrary coordinates, or fake live charts. Preserve meaningful product terminology. Do not insert NERV logos, MAGI names, pilots, lore, or show dialogue unless the actual app is about Evangelion or the user specifically requests them.

If no numeric data exists, achieve fidelity through typography, borders, numbered real sections, content grouping, strong silhouettes, and editorial composition. A shop should sell products; a reading view should support reading. Reserve hazard stripes and dramatic alert plates for actual warnings, destructive actions, or a requested clearly labeled demonstration of those states. Decorative grain is permitted; decorative misinformation is not.

Controls must perform their stated actions. Keep pending, success, failure, disabled, loading, and empty states honest. Show progress only when measurable; otherwise use an indeterminate busy indicator. Chart axes, ranges, units, thresholds, and legends must describe the actual dataset. Never auto-rescale a chart to manufacture alarm.

## Customization contract

Maintain one theme definition, using the existing theme architecture where present. Expose the following developer-configurable options, and a user-facing settings control when requested or appropriate for a settings-bearing app:

- `palette`: classic-amber (default), terminal-green, ice-blue, unit-purple, or custom semantic colors.
- `primary`, `secondary`, `text`, `muted`, `background`, `surface`, `warning`, `danger`, `success`, `border`, `focus`: independently overridable colors.
- `analog`: off, subtle (default), or cinematic. Keep all modes legible. Provide a working disable-effects control when animated distortion is enabled.
- `density`: comfortable or compact; `typeScale`; heading and body font families.
- Individual scanline, grain, glow, and vignette strengths. Optional chromatic bleed should be minimal; do not introduce flicker, tracking tears, or whole-page jitter by default.

Respect supplied colors immediately. A purple/green palette must still retain Evangelion's instrument grammar; its color alone is insufficient. Centralize values; no scattered hard-coded neon colors. For custom combinations, measure text/control contrast and fix invalid pairings or clearly identify them before acceptance. Persist preferences only with the app's normal preference mechanism; fall back gracefully if storage is unavailable.

Honor reduced motion, zoom, keyboard navigation, focus, high-contrast modes, and print. Use the visual effects layer as optional presentation, independent from DOM accessibility and data. Prefer static analog texture to continuous animation for long work sessions.

## Portability

Keep this folder intact: standard `SKILL.md`, relative references, and framework-independent assets work with Codex and Claude Code without proprietary tool hooks. Resolve resources relative to this skill file, never to a hard-coded machine path. The Goosnav pack installers copy this folder into the pack's canonical `.agents/skills/evangelion-ui` location; use the existing pack install workflow. For standalone Claude Code installations that use its own skill directory, place the folder at `.claude/skills/evangelion-ui/` or `~/.claude/skills/evangelion-ui/` and invoke `/evangelion-ui`. In Codex, use its configured skills location and invoke `$evangelion-ui`. Product code must not depend on the installed skill's absolute path: copy only needed implementation assets into the product. Keep reference screenshots out of the shipped application unless specifically requested.
