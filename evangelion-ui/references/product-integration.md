# Apply the instrument language to a real product

## Goosnav composition

Keep Goosnav's supplied wordmark, product name, artwork, and direct language. Preserve a supplied Labs Eurostile identity treatment where licensed; use the bundled condensed font for instrument hierarchy rather than claiming it is the Goosnav brand typeface. Keep long editorial passages readable in the product's established body font. Do not invent a goose mascot, GOOSCORP parent brand, military classification, NERV affiliation, or fictional operator persona.

Use Evangelion when explicitly requested. Use the core Goosnav software skill for its print-like working interface, or the early-web skill for refined desktop/portal character. Combine through shared behavior and content, not by accumulating all three visual treatments. A Goosnav navigation shell can lead to an Evangelion-styled tool, but each region needs one legible hierarchy and an intentional boundary.

Give saturated color a job: primary structure/action, secondary information, and separately labeled success/warning/error states. Do not add red, blue, and yellow merely to fill a color quota. Preserve actual artifact colors in catalog images. Instrument colors need not recolor the supplied art or logo.

## Useful applications

| Product task | Strongest treatment | Preserve |
| --- | --- | --- |
| Editor or file utility | Large work surface, attached heading, compact result region | Visible import, editable source, exact validation and export behavior |
| Batch processing | Ordered real inputs, current operation, per-item outcomes | Failed items, completed downloads, cancel/retry rules, actual progress |
| Measurement viewer | Dominant calibrated plot, readings with units, inspection controls | Data range, freshness, missing values, keyboard-accessible alternatives |
| Product page | Strong product image/title, readable specifications, clear purchase action | Real price and availability, accurate colors, ordinary commerce labels |
| Article or whitepaper | Editorial dossier with generous reading measure | Comfortable prose, working contents, authentic references |

## Form and state primitives

Use native labels, inputs, textareas, selects, buttons, and file controls. Apply `.eva-field`, `.eva-help`, `.eva-field-error`, and `aria-describedby` to keep instructions and errors attached to their field. Set `aria-invalid` only when the present field value is invalid. A failed file import need not mark the existing valid editor text as invalid.

Use native `disabled` for unavailable actions and explain the prerequisite nearby. Disabled primary buttons must use the subdued surface/text treatment rather than low-contrast muted text on a bright primary fill. Use `.eva-status[data-state]` with a meaningful label; supported states include `unknown`, `pending`, `success`, `warning`, and `error`. Loading is not success. Updating input must invalidate stale validation and dependent exports.

Keep file reading, cancellation, and edits race-safe. Preserve the current input when an import is refused. Render imported strings as text, never as HTML or evaluated JavaScript. Download the promised format and contents; a syntax check does not certify an application's schema.

## Keep work surfaces clear

Apply `.eva-screen` to the region that should receive analog texture. For an editor or image-inspection tool, put it around the header or instrument surround rather than the entire app. The JSON inspector demonstrates this narrower scope. A descendant cannot reliably cancel an ancestor's full-screen overlay; do not pretend that placing `data-analog="off"` on a photo removes the ancestor's pseudo-element.

Keep prose, source editors, product images, QR codes, and precision color surfaces clear. Allow long values to wrap or use a dedicated, labeled horizontal scrolling region for a genuinely two-dimensional dataset. Do not truncate or shrink a critical measurement until unreadable.

## Working application specimen

Open `assets/inspector.html` with its adjacent CSS/JS and existing font/texture assets intact. It starts empty and checks only user-provided JSON. Byte count, type, and entry count are derived from that source. No mock job stream or fake external data is present.

Exercise empty input, malformed JSON, object/array/primitive values, edits after a successful check, a refused oversized import, and download. Confirm downloaded text equals the checked source. Palette/effect controls modify this page only. The demo does not imply that a renderer, server, or application schema was tested.
