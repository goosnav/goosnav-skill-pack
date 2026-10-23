# Source and decision boundaries

## Authority

Apply the active user's explicit design request, then the applicable project instructions and
approved brand rules. Treat this skill as a reusable software design direction, not a replacement
for all Goosnav identities. Do not silently edit brand manuals or unrelated repositories.

The owner requested this direction on **October 23, 2026**: encapsulate Goosnav software/web
design found in `goosnav-labs-hq`, `goosnav-brain`, and `3D-comic-engine`, with a slightly more
colorful version using primary-color highlights where applicable. The owner separately requested
a refined early-internet variation. Keep those two modes distinct.

## Observed source versus new extension

| Source | Observed rule or pattern | Treatment in this skill |
|---|---|---|
| `goosnav-labs-hq/style/global.css` | White/black base, Helvetica display, Times body, 1100px frame, 68ch prose, thin rules, square controls | Use as the core visual foundation. |
| `goosnav-labs-hq/style/README.md` | System fonts; Eurostile needs a web license; engineering visuals have controls/static fallbacks | Preserve practical implementation and optional font boundary. |
| `goosnav-labs-hq/src/layouts/Base.astro` | Text identity, visible section navigation, semantic main content, skip link | Derive structure and behavior, not exact page markup. |
| `goosnav-labs-hq/src/pages/index.astro` | Meaningful engineering visual, direct next action, ruled directory | Translate to the product's actual content and task. |
| `goosnav-labs-hq/docs/dev/Goosnav-Labs-Software-Bible.txt`, §03 | Earlier white/ink/yellow system; Eurostile/Chakra Petch, Times, IBM Plex Mono; truthful content | Preserve intent; distinguish legacy specification from current CSS. |
| `3D-comic-engine/web/style.css` | 1440px tool workspace; primary red/blue/yellow plus green; Arial before Helvetica for glyph fallback | Allow wider workspaces and practical system-font fallbacks. |
| `goosnav-brain/01-BRANDING/Goosnav-Labs.md`, software section dated 2026-10-23 | Product-appropriate direction, shared tokens, honest state, functioning controls; Evangelion is context-specific | Preserve as software principles. |
| Owner's current request | Controlled primary-color highlights | Extend the reusable software palette; do not claim a newly deployed site theme. |

The old Labs Software Bible rejects a generic blue tech-brand appearance. The current accent
direction permits useful blue links, actions, and selection without replacing the white/ink
identity with an all-blue corporate theme. Its old yellow is `#FFD100`. The inspected comic
engine already defines `#DA291C`, `#0033A0`, `#009639`, and `#FFCD00`; preserve those when extending
that app. The blue `#1746C7` and red `#B42318` in these starter assets are implementation choices
for readable states, not newly assigned physical-artifact colors.

Current Labs CSS uses Helvetica, not embedded Eurostile. A comment in
`public/assets/branding/README.md` about a red `--accent` is stale relative to inspected CSS.
The site has a disabled blueprint theme; do not describe it as the active core style.

## Brand scope

The supplied *Goosnav Comics Brand & Marketing Bible*, Rev B (September 4, 2026), is Comics-only.
Its §§10 and 19 distinguish Labs' display face and voice; they permit shared Times body type.
The supplied Comics one-pager and `goosnav-brain/01-BRANDING/Visual-Identity.md` preserve black
ink on white canonical drawings, artist lettering, and assigned physical-artifact colors.

Keep those drawings and assignments intact inside software. Do not infer a goose logo from
the name, invent GOOSCORP as a brand, turn recurring artwork into a compulsory mascot, or
import Comics' faceless/mysterious commercial posture into Labs service copy.

Use existing approved marks. A plain text name is sufficient when a mark is unavailable.
Technical interfaces may be colorful without altering the canonical comic image.

## Inspectable provenance

Source review date: October 23, 2026. These pointers are not dependencies required to apply the
skill. Private repositories require owner access; never copy their business records or secrets
into this public package.

- [Labs stylesheet](https://github.com/goosnav/goosnav-labs-hq/blob/main/style/global.css)
  — inspected blob `31fdcc88333f4591c1667c57c55e0ca79cdd8235`.
- [Labs style guide](https://github.com/goosnav/goosnav-labs-hq/blob/main/style/README.md)
  — inspected blob `43e5fe72845e5781fe922e2b6150c4bcdfc52828`.
- [Labs base layout](https://github.com/goosnav/goosnav-labs-hq/blob/main/src/layouts/Base.astro)
  — inspected blob `443a22775ae393e20be52df61677c9059fc31663`.
- [Labs homepage](https://github.com/goosnav/goosnav-labs-hq/blob/main/src/pages/index.astro)
  — inspected blob `e4b8c450168a46bcc96677a4ee9016d0e5a70a5b`.
- [Labs software specification](https://github.com/goosnav/goosnav-labs-hq/blob/main/docs/dev/Goosnav-Labs-Software-Bible.txt), §03.
- [Comic engine stylesheet](https://github.com/goosnav/3D-comic-engine/blob/main/web/style.css).
- [Brain Labs guidance](https://github.com/goosnav/goosnav-brain/blob/main/01-BRANDING/Goosnav-Labs.md)
  — inspected blob `64b93e530543d8acd48bbbdfd5e1fb1256df5c2d`.
- [Brain Comics visual identity](https://github.com/goosnav/goosnav-brain/blob/main/01-BRANDING/Visual-Identity.md)
  — inspected blob `9ae1015146c8a34d2643a2f3d638a0661fd9be60`.
- [W3C text contrast explanation](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Treat numerical defaults as starting points. Preserve the project's task, content, accessibility
requirements, and current owner decisions when adaptation is needed.
