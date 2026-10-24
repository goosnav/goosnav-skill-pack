---
name: goosnav-early-web-design
description: "Design or refine Goosnav websites and software with professional early-internet character: restrained Windows XP task chrome, early video-library layouts, or search-led marketplace catalogs. Use for Goosnav retro-web, Y2K, early YouTube/eBay/Amazon-inspired interfaces, or a more flavorful alternative to the core Goosnav software style. Preserve modern usability, responsive layouts, and restrained primary colors. Do not apply this theme merely because a task mentions Goosnav; select it when the requested aesthetic is retro or early web."
---

# Goosnav Early Web Design

Build a useful modern interface whose organization recalls the early web. Preserve
Goosnav's editorial precision, honest controls, plain language, and serious execution.
Make the nostalgia visible in structure and interaction before adding decoration.

## Establish the direction

1. Read the project's instructions, existing screens, components, routes, and styles.
2. Identify the user's main task, the content being handled, and the next action.
3. Choose **one dominant family** from the table below; state the choice briefly.
4. Keep working flows, contracts, data, and established brand assets intact.
5. Implement one representative screen and its states before extending the system.
6. Check actual behavior, keyboard use, narrow screens, and rendered output.

| Family | Use for | Structural cues |
| --- | --- | --- |
| XP workbench | Editors, batch jobs, local tools | One titled work area, grouped task controls, inset fields, restrained bevels, explicit progress and result areas |
| Early media library | Comics, videos, archives | Content-first player or preview, thumbnail-and-metadata rows, clear browsing and pagination, adjacent related items |
| Search-led catalog | Software libraries, products, research tools | Persistent search, category rail, count and sort toolbar, compact comparable rows, clear detail and action areas |

Use a second family only for a specific functional need. Do not combine a taskbar,
fake desktop, auction catalog, video portal, and storefront into one screen.
Read [pattern recipes](references/pattern-recipes.md) for component-level decisions.

## Keep the Goosnav foundation

- Start with white paper, black ink, rules, aligned edges, and a clear reading order.
- Use `Helvetica Neue, Helvetica, Arial, sans-serif` for interface text and headings.
- Use `Times New Roman, Times, serif` for a short editorial introduction or long-form
  reading; keep form labels, navigation, tables, and dense metadata in the UI face.
- Retain an existing licensed Eurostile/approved Labs display face if the project
  already uses it. Do not fetch or bundle proprietary fonts to imitate an era.
- Use a centered frame near 1100px for a catalog; let working tools use more width
  when their content needs it. Limit reading prose to about 68 characters per line.
- Use a coherent spacing scale: 0.5, 1, 1.75, and 3rem, with smaller internal gaps
  only where needed. Let density come from organization rather than tiny type.
- Use 1px structural rules, square panels, and at most 2-4px control corners.
- Keep the interface calm enough that the actual work supplies its personality.

## Keep the task ahead of the chrome

Retro character does not require more labels. In working tools, name the active object once.
Remove repeated titlebars, breadcrumbs, “Your…” headings, process narration, and permanent
success panels when the result already shows completion. Keep controls and useful data in the
first viewport. Put optional help in a disclosure; retain errors, required constraints, sample
labels, and accessible names. Remove text that does not change a decision or action.

## Apply color deliberately

Use blue for links, selected controls, and the principal action by default. Use red
for errors or destructive actions; use yellow for a local notice or important
annotation with dark text. A branded title stripe may repeat the active accent.

Keep most of the surface neutral. Do not color every section, metric, or button.
Use text, icons, borders, or position alongside color so meaning survives grayscale.
Distinguish product-identifying colors from status colors; never imply that a red
book cover is an error. Reserve strong primary fills for small, purposeful regions.

Use the starter tokens in [assets/early-web.css](assets/early-web.css). Treat these
as software defaults for this requested variant, not historical brand law. Override
the scoped `--gew-*` variables when an existing product palette has priority.

## Refine the early-web cues

- Make titlebars describe real work areas. Keep them short and visually subordinate
  to the content. Do not add decorative minimize, maximize, or close controls.
- Give buttons shallow raised edges and a pressed state. Use inset borders for
  editable fields; make affordances consistent rather than photorealistic.
- Use a restrained blue title gradient or neutral control gradient where helpful;
  keep content backgrounds flat. Avoid glass, bloom, scanlines, and bevels everywhere.
- Use underlined text links with a distinct visited state in browsable archives.
- Put useful metadata beside the object: name, type, version or date when real,
  relevant properties, and the next action. Do not fabricate popularity or reviews.
- Prefer list rows when people compare items. Use a gallery only when images do the
  comparison work. Include sort and result count when a collection warrants them.
- Use real tabs only for peer views. Implement their keyboard model; otherwise use
  ordinary links or pressed-state filter buttons with honest semantics.
- Use real product media or simple geometric diagrams. Do not invent canonical
  Goosnav comic drawings, goose mascots, or borrowed corporate logos.

## Maintain modern behavior

- Keep essential controls at least 44px high; preserve readable body text around
  16px and secondary text around 14px. Do not recreate historical tiny hit targets.
- Give every input a persistent label. Use native buttons, links, forms, headings,
  lists, and details where they solve the task; add ARIA only when necessary.
- Supply visible focus, keyboard completion of the main task, and visible selection.
- Meet at least 4.5:1 contrast for ordinary text and 3:1 for large text and essential
  component boundaries. Check actual pairs, including gradients and hover states.
- Reflow sidebars above results or into an explicit disclosure at narrow widths.
  Stack row actions without changing logical reading order. Avoid page overflow at
  320px and retain usability when text is enlarged to 200 percent.
- Preserve useful content while loading where possible. Mark the busy region and
  announce the result, not each transient keystroke. Prevent duplicate submissions.
- Explain empty states in terms of the current search or missing input; provide a
  useful reset or next step. Show a specific error and a functional retry path.
- Keep disabled controls visibly different and explain the prerequisite nearby.
- Respect reduced motion; avoid forced intros, blinking labels, custom cursors,
  autoplay audio, draggable windows, or ornamental status displays.

## Respect the Comics boundary

Apply this as a **Labs/general software variant** requested by the user. Preserve
canonical Comics artwork in black and white; do not recolor it to match the chrome.
Keep assigned artifact colors intact. Treat GOOSCORP as a fictional organization,
never the company's voice, and do not derive a goose mascot from the Goosnav name.

Use concise, literal product copy. Humor may sit in the contents or premise; keep
labels, prices, navigation, error recovery, and checkout unambiguous. Do not import
Comics-only rules such as facelessness or analog authorship into software engineering.
Read [source and scope notes](references/source-and-scope.md) when changing branding.

## Use the specimen

Open [assets/catalog.html](assets/catalog.html) with its adjacent stylesheet. Use it
as a component specimen: search, categories, sorting, saved items, inline details,
example JSON downloads, and loading/error recovery all operate locally. Every entry
is labeled example content. The page has no external dependencies or font downloads.

Copy only relevant components into the existing application. Preserve the `.gn-web`
scope or adapt it to the project's component system; do not paste a global reset over
an established app. Replace the specimen's sample data and demonstration controls
with the project's actual states. Do not ship the fixture catalog as real inventory.

## Finish the work

Verify search/filter/sort together, empty results, details, retries, disabled states,
and the primary action. Inspect a desktop and a narrow render, keyboard focus, text
zoom, and reduced motion. Use the project's meaningful checks. Report implemented
behavior and any unavailable verification plainly. Keep validation proportional to
the change; do not require a new framework or redesign working architecture.

For skill maintenance, run `python3 scripts/validate_skill.py` from this folder and
the pack's validation command. Follow the repository's delivery instructions.
