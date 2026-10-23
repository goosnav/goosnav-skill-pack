# Pattern recipes

Use one dominant family for each screen. Borrow structure from the reference era,
then implement the task using current HTML, responsive layout, and actual data.
These are design interpretations, not replicas of specific historical releases.

## XP workbench

Use a neutral work surface with a blue title strip, a short group of task controls,
and a large central workspace. Put input selection before processing options, place
the primary action beside those options, and keep progress next to the eventual
result. Use a real job list for batch work, with per-item results and failures.

Make a narrow screen follow the same order: input, configuration, action, output.
Use a shallow button bevel and an inset field edge to communicate interactivity.
Keep the work surface stationary. Do not make users operate a desktop simulation
to reach an ordinary app. Add a close button only to something that actually closes.

## Early media library

Let the work lead: a preview or selected item, readable title, useful metadata,
direct controls, and a related-item column. Use compact image-and-text rows for a
library. Keep numbering, dates, and discoverability when the collection is archival.
Place search and categories where users can scan them without opening a menu.

Provide captions, alt text, and playback controls when media requires them. Preserve
the source artwork; do not colorize canonical comics or replace them with generated
approximations. Never reproduce a video service's wordmark, exact chrome, view counts,
or rating fiction just to make the layout feel familiar.

## Search-led catalog

Use a dominant search field, a category rail, a count/sort toolbar, and rows with a
stable anatomy: object preview, name, short purpose, comparable properties, action.
Put a short editorial introduction above the catalog, not a marketing hero that
hides it. Keep important product facts close to the action.

Use visible filters, removable selection, and an understandable zero-results state.
Preserve search and filters while viewing a detail. Do not turn ordinary browsing
into a series of modals. Use inline details for a small amount of secondary content
or a real route for substantial detail. Show prices and delivery terms when they
are part of the actual task; do not import commerce widgets into a software tool.

The bundled catalog demonstrates this family. It uses six explicitly fictional
examples, category filtering, case-insensitive search, sort, a saved-only filter,
details, and an example manifest download. Saved state lasts for the page session.
The state inspector can reload those examples or show a recoverable simulated error.
Remove that inspector when adapting the specimen to production.

## Color and material recipe

| Element | Default treatment | Reason |
| --- | --- | --- |
| Page | Warm neutral `#f4f4f0` | Separate application frame from the browser surface |
| Content | White, black text | Keep the work and facts legible |
| Chrome | Light gray `#e9e9e4`, 1px edge | Organize the controls without card clutter |
| Primary action and links | Blue `#0033a0`, white on fills | Give the next action a stable place in the hierarchy |
| Error | Dark red `#a32520` with an explicit label | Communicate a failure without relying on hue |
| Note | Yellow `#ffcd00` strip with black text | Mark a local instruction without making the screen loud |
| Fields | White with a restrained inset edge | Make editing affordances obvious |
| Buttons | Neutral or blue, 2px corner, shallow light edge | Recall tactile controls without plastic ornament |

These are chosen software defaults. The blue and yellow echo colors present in
Goosnav's artifact system; they do not change product color assignments. Check new
foreground/background pairs when overriding tokens. Keep color subordinate to
labels, grouping, alignment, and whitespace.

## Common failures

| Failure | Correction |
| --- | --- |
| A fake desktop with inert window buttons | Use one real workspace with actual task controls |
| Beige body, microscopic text, and endless blue links | Keep the useful link affordance; add a modern type and spacing scale |
| XP gradients on every panel | Limit material effects to the small amount of interactive chrome |
| Nostalgia requires horizontal scrolling on a phone | Reflow filters and row actions; keep the information order |
| Every control is a primary color | Establish one main action; reserve other colors for meaning |
| Ratings, online counts, or telemetry invented for atmosphere | Use real data or clearly labeled examples |
| Retro styling spreads into canonical comic artwork | Isolate software chrome from protected artwork |
| A single page mixes all reference brands | Select the family that serves the task and remove the rest |
