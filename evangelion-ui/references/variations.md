# Composable variants, not one template

Open `assets/templates/index.html` to inspect the six structural specimens. Each HTML file imports the shared token/component CSS plus its own small scoped CSS file. Copy only the recipe that serves the product. Do not ship the specimens' instructional copy. These are deliberately different information architectures, not recolors of one layout.

| Recipe | Shape | Use | Do not force |
|---|---|---|---|
| operations | Navigation rail / main task / selected detail | Editors, inventory, device workspaces | A marketing page into three monitoring panes |
| analysis | Dominant data plane / channel strip / interpretation | Actual measurements and research | Charts when no dataset exists |
| approval | Central proposal / adaptable chamfered participant panes | Actual review or dependency workflow | Exactly three participants or fabricated approvals |
| dossier | Contents margin / long reading measure / source region | Articles, portfolios, whitepapers | Small monospace prose or dashboard cards |
| catalog | Large imagery / purchase column / full-width specs | Hardware, software, merchandise | Fake stock urgency or technical telemetry |
| process | Dominant operation / vertical stages / events | Exports, builds, jobs, timed work | Invented completion percentages or event streams |

Vary these independent axes: information architecture; amber/green/blue/purple/custom palette; condensed or editorial-serif headline; framed, open-rule or chamfered panels; comfortable/compact density; off/subtle/cinematic screen treatment. Palette selection must never dictate layout. A catalog can be amber; a dossier can be blue. Use the original stopwatch only for actual timing tasks.

Select the primary family from the user's task, then adapt columns, order, proportions and components freely. If no supplied recipe fits, build a new layout from the shared primitives and document the choice briefly. Never cycle templates randomly or combine all six on a page. Within an application keep a coherent token system while letting a reading page, shop page and operational tool have different structures.

## Graphic primitives

`assets/graphics/` contains eight authored SVG primitives and their CSS masks: corner brackets, chamfered frame, double rule, caption frame, fiducial grid, hazard edge, crosshair and elbow leader. They contain no embedded words, measurements or invented traces. Each has a 200×100 viewBox; preserve its ratio or rebuild geometry for the actual panel. Prefer inline SVG for non-scaling strokes and responsive aspect ratios. Remove its root color attribute to inherit `currentColor`; CSS masks already use theme tokens. External SVG images do not inherit host CSS color.

Use brackets/rules/caption frames as decorative structure with `aria-hidden="true"`. Crosshairs require a real selection/target context, leaders must connect actual annotations, and grids belong to calibrated visualization surfaces. Label axes and units from data in application code; the graphic itself supplies none. Hazard edges are reserved for genuine warning or destructive-action contexts. Do not use primitives as wallpaper to fake technical complexity. Generated charts and wireframe models must be implemented from actual data, not from canned ornamental SVGs.

Apply analog effects to framing and instruments, not product photography, QR codes, documents, or precise color-inspection surfaces. CSS starter effects cover their wrapper; isolate these exempt regions outside that wrapper or apply the wrapper only to their surrounding UI.

## Repo integration

The inspected Goosnav pack discovers top-level folders containing install.sh; no registry or install-all edits are required. Put `evangelion-ui/` beside `aesthetic-web-design/`. The included installers follow that pack's source-copy conventions, canonical `.agents/skills/evangelion-ui` destination and same-name legacy cleanup. Run `python3 evangelion-ui/scripts/validate_skill.py`, then the pack's `python3 validate-pack.py`. Optional: add an Evangelion UI row to the README's primary-skills table. The downloaded package does not replace the repo README or other skills.
