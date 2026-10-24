---
name: goosnav-web-design
description: Design and implement core Goosnav Labs websites, software interfaces, utilities, dashboards, and product pages with a white-and-ink editorial frame, strong typography, ruled structure, square controls, and selective primary-color accents. Use for Goosnav software styling, a Labs-like website, an interface inspired by goosnav-labs-hq or 3D-comic-engine, or a Goosnav UI redesign. Do not apply by default to canonical Comics artwork, explicit early-internet/Windows XP styling, or Evangelion/NERV/MAGI requests.
---

# Goosnav Web Design

Build a precise, authored interface: strong type, useful information, visible controls,
and an economical structure. Let the actual work provide the character.

## Start with the task

1. Inspect the current page, routes, components, design tokens, assets, and repo instructions.
2. Identify the user's main action, input, output, and likely failure. Keep that sequence visible.
3. Choose a composition: editorial page, working tool, catalog, or data workspace.
4. State the type roles and intended color roles in a few sentences, then implement.
5. Preserve working behavior and the project's framework. Do not rebuild the stack to restyle it.

For a small request, make the smallest coherent change. For a new screen, finish one complete
input-to-result path before adding secondary modules.

## Remove text before adding style

For working tools, keep copy that identifies an object, labels an action, or prevents a likely mistake.
Let layout, controls, and real content explain the workflow.

- Name the active object once. Remove repeated breadcrumbs, section names, and possessive headings such as “Your lead list.”
- Remove taglines, obvious instructions, numbered process summaries, and paragraphs that narrate visible controls.
- Keep routine success quiet. A populated table or enabled download can show completion without a permanent status panel.
- Put advanced settings and technical details behind a relevant disclosure or Help. Do not add a tooltip to justify every element.
- Label sample data once. Keep errors, stale-result warnings, required format constraints, and accessible control names.
- Inspect the first viewport. The user should reach useful controls and data without scrolling past explanatory chrome.

Before delivery, read every visible line. If its removal preserves meaning and task completion, remove it.
Do not replace deleted filler with shorter filler. Requested editorial content and necessary instructions still belong.

## Establish the visual foundation

| Element | Default | Adaptation |
|---|---|---|
| Canvas | White or near-white, black ink | Use gray surfaces only to separate a meaningful region. |
| Display | Helvetica Neue, Helvetica, Arial; bold | Use licensed Eurostile only when supplied/approved. |
| Controls | Same sans family; sentence case | Use uppercase for short labels, not long form answers. |
| Prose | Times New Roman, Times, serif | Use for introductions, articles, and explanations. |
| Values | System monospace, tabular figures | Use for filenames, code, IDs, and numeric comparisons. |
| Geometry | Square or near-square, 1px rules | Reserve a surrounding box for something that behaves as a unit. |
| Frame | Around 1100px; prose around 65–70ch | Expand a real editor/workspace toward 1440px when useful. |
| Spacing | 8, 16, 28, 48px reference steps | Adjust density by region; retain meaningful grouping. |

Use a few large, tightly composed headings and a clear reading order. Keep navigation visible
and concise. Prefer rows, dividers, lists, and native form groups to a uniform wall of cards.
Let a technical drawing, actual product, editor, or output preview carry visual interest.
Honor the existing project's tested font fallback order; do not break Unicode symbols to
enforce a particular Helvetica/Arial ordering.

In a repeated-use tool, omit the introduction when the controls already explain the task.
Use a compact object title and put useful controls and data above the fold.

## Add color where it earns its place

Use the primary family as available accents, not a requirement to show three colors.
Keep most of the screen neutral; assign one leading accent and a small number of supporting roles.

| Role | Starter color | Pairing and meaning |
|---|---|---|
| Action, link, selection | Blue `#1746C7` | White on filled blue; blue underlined text on white. |
| Attention, current step, small signature | Yellow `#FFD100` | Black text; never yellow text on white. |
| Error or destructive action | Red `#B42318` | Add an explicit word/icon; never ordinary success. |
| Verified success, if needed | Green `#17623B` | Say what completed; do not add it merely for variety. |

Separate brand accents from semantic status tokens even when their values coincide.
Use blue for the action and yellow for an instruction only if both improve scanning.
A restrained red category marker can suit a non-operational editorial page; keep that use
away from error/destructive affordances. Retain an existing application's approved palette
when extending it; these starter hex values are not compulsory replacements.

Avoid color-coded paragraphs, rainbow navigation, gradient heroes, tinted cards everywhere,
and status conveyed by color alone. Check actual contrast: 4.5:1 for ordinary text and 3:1
for qualifying large text; also inspect control boundaries and focus indicators.

## Make structure do the work

- **Editorial/product page:** a clear title, one useful visual, bounded prose, direct next action.
- **Working tool:** inputs and settings beside a result/preview; stack in task order on mobile.
- **Catalog:** search/filter when needed, meaningful names, useful thumbnails or facts, visible links.
- **Data workspace:** stable row/column alignment, units and dates, honest empty/unknown values.

Put import/upload near the start of an import-driven workflow. Keep row-specific actions with
their row. Offer batch selection when the task is genuinely repetitive. Make completion and the
download/open action easy to find. Do not make users traverse decorative panels to reach work.

Read [component and layout guidance](references/components.md) when implementing a new surface.

## Preserve truthful behavior

- Connect every actionable control to real behavior. Use links for navigation and buttons for actions.
- Distinguish empty, invalid, busy, success, and unavailable states. Preserve input on failure.
- Show progress only when measured; otherwise name the operation without a made-up percentage.
- Invalidate an old result when its inputs change, or label exactly which input it represents.
- Keep downloads disabled until a valid artifact exists. Use safe text insertion for user content.
- Give recovery instructions next to the problem. Avoid unexplained errors and permanent spinners.
- Use requested sample data only when clearly labeled. Do not invent business proof or healthy telemetry.

## Keep the brand boundary clear

Apply this skill to software and web interfaces. Preserve approved logos and artwork. Use a
plain text identifier if the correct mark is absent; do not invent a goose or GOOSCORP identity.
Keep canonical Comics drawings black and white and preserve their lettering and authorship.
Do not import Comics' mysterious voice or no-face rule into a Labs service/tool interface.

Treat the primary-accent direction as the owner's October 23, 2026 software extension. Do not
describe it as an unchanged historical brand manual or a newly deployed site theme.
Read [source and decision boundaries](references/sources-and-boundaries.md) when reconciling
an existing brand standard or explaining how the style was derived.

For an explicit early-internet or Evangelion request, select that visual direction instead of
mixing desktop nostalgia, CRT effects, and this core style indiscriminately. No sibling skill
is required to use this one.

## Implement and verify

1. Reuse the host's tokens/components. Copy selected rules from
   [the scoped CSS foundation](assets/goosnav.css) only where appropriate.
2. Use semantic landmarks, labels, real headings, native controls, and visible focus.
3. Default major controls to 44px targets for comfortable use; this is a design default,
   not a claim that WCAG AA requires every target to be 44px. Keep type readable at 320px width.
4. Respect reduced motion. Restrict motion to state feedback or a purposeful interactive visual.
5. Render desktop and narrow layouts. Check long names, long text, overflow, and zoom.
6. Exercise the main path with real input plus empty, invalid, interrupted, and repeat operations
   where relevant. Check that a stale result cannot masquerade as the latest output.
7. Inspect keyboard order, status announcements, focus placement, and contrast in actual states.
8. Report changes and what was exercised; identify any unavailable runtime verification.

Use [the functioning local workbench](assets/workbench.html) to inspect the visual system and an
input-to-download workflow. Its list-to-JSON utility is an example composition, not a mandatory
layout or backend integration. Keep `goosnav.css` and `workbench.js` beside the HTML to open it
directly in a browser; it uses no external services or fonts.

Run `python3 scripts/validate_skill.py` when editing this skill. Structural checks do not replace
rendering or trying the resulting interface.

## Final quality gate

Require a recognizable typographic identity, one obvious primary action, restrained meaningful
color, aligned structure, readable content, functioning controls, and a complete result state.
Complete the text-removal pass as well as visual and functional checks.
Remove anything that creates more visual work than functional value.
