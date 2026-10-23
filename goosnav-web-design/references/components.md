# Components and compositions

## Page frame

Use a compact identity row, a ruled navigation row when the site has multiple destinations,
and a bounded main region. Keep the identity legible as text. An icon can support an existing
approved mark, but must not substitute an invented mascot or unrelated engineering symbol.
Use a compact footer for useful links, version, or context that actually exists.

For a marketing/editorial page, use one dominant heading and one meaningful image or
interactive artifact. For a workbench, let the active job occupy most of the screen. Avoid
repeating a landing-page hero above every workspace.

## Type hierarchy

Keep display type bold and compact; use tight tracking selectively for large headings, not
small text. Set short navigation/section labels in the sans family. Use Times for substantial
explanations, with approximately 65–70 characters per line and comfortable leading. Use a
monospace face for literal data and code, not an entire marketing page.

Default to the supplied system stacks. If the project already has a licensed Eurostile webfont,
its standard-width bold face can serve Labs headings. Do not fake Eurostile by stretching text,
introduce a font CDN dependency, or treat desktop-font ownership as permission to redistribute.

## Actions and form controls

Use one filled primary action per decision group. Use outlined or plain-text secondary actions.
Pair destructive controls with explicit verbs and the affected object. Keep hover, keyboard
focus, active/pressed, disabled, and busy states visibly distinct. Do not imply progress by
making every disabled control use a wait cursor.

Place persistent labels above fields. Put examples and format constraints in helper text.
Associate error text with its field, set `aria-invalid` on invalid input, and retain user
input. Treat conditional questions as fields within the form, not a new ornamental card.

For a file operation, show accepted inputs, selected file name, limits, and what the action
produces. File upload and clipboard entry can share one source field. Track which content is
current, and disable or relabel prior output after an edit. A busy label must correspond to
actual asynchronous work; do not add delay to make a spinner appear.

## Rows and panels

Prefer a ruled list for files, projects, article summaries, and simple settings. Use a real table
for values users compare across columns. Keep units in headers and exact values aligned.
Use a bounded, labeled horizontal scroll region for a table too wide to stack intelligibly.

A panel earns its border when it groups a coherent task, isolates a preview, or behaves
independently. Do not wrap each title, paragraph, and button in a separate card. Align related
labels and values across sibling groups.

## State language

| State | Show | Provide |
|---|---|---|
| Empty | What belongs here | A direct way to add/import it |
| Invalid | The specific failed requirement | The correction and retained input |
| Busy | The current operation | Disabled conflicting actions; cancel if supported |
| Success | What completed and the actual result | Open/download/continue action |
| Partial | Which items worked and failed | Per-item recovery without losing successes |
| Unavailable | What is missing or disconnected | A truthful path to restore availability |

Use restrained status treatment. A red error line or yellow instruction can be sufficient;
do not turn the whole page red or yellow. Announce asynchronous updates with a concise live
region; avoid announcing an entire changing results table on each keystroke.

## Responsive composition

Start from content constraints: a two-column editor/result workbench can stack when either
column stops being usable. Keep input before output in DOM order. Keep main actions reachable
without horizontal scrolling. Wrap action groups and navigation labels. Allow long filenames
and IDs to break within their container.

Test 320px and a normal desktop width, then zoom. Preserve labels, focus outlines, status, and
download access. Do not shrink all typography to preserve desktop density. A compact interface
can still use 44px buttons and well-separated inline links.

## Visual interest and motion

Use actual drawings, prototypes, screenshots, code, or a purposeful engineering visualization.
Keep a technical grid behind a graphic if useful; do not place texture behind prose. Use a
single lightweight visual with pause/static fallback when motion is central. Pause hidden or
offscreen renderers and honor reduced motion. Do not add simulated oscilloscope traces,
percentages, logs, or warnings merely to make a screen look technical.
