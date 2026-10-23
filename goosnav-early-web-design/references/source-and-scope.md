# Source and scope

This skill is a new software design variant requested on 2026-10-23. It translates
Goosnav's existing precision into a more flavorful early-web aesthetic. It is not
a claim that the brand's older documents already prescribed Windows XP styling.

## Sources and precedence

1. Follow the user's current task and the target repository's instructions.
2. Preserve the target product's working behavior and established brand assets.
3. Use current Goosnav implementations as the default implementation evidence.
4. Use brand documents within their stated scope; distinguish Comics from Labs.
5. Use this skill's early-web treatment where the user requests that direction.

The sibling `goosnav-web-design` skill describes the core visual family.
This skill includes the necessary foundation and installs independently; it does
not require sibling files, private repositories, or the original PDFs at runtime.

## Implementation evidence

- **goosnav-labs-hq:** current styles use a white/black foundation, Helvetica Neue /
  Helvetica / Arial interface typography, Times editorial type, a roughly 1100px
  frame, 68-character reading width, a small spacing scale, 1px rules, square
  geometry, and 44px controls. Preserve this functional editorial discipline.
- **3D-comic-engine:** purposeful red, blue, and yellow accents support the current
  request for more color in software. Do not infer a requirement to color every UI.
- **Older Labs manual:** Eurostile or an approved Labs display alternative, Times
  body text, mono technical labels, and a yellow signature describe an older Labs
  expression. Keep existing licensed fonts when appropriate; do not silently
  replace the current repository's typography or ship proprietary font files.

## Supplied Comics documents

Both PDFs are GC-BRD-001 Rev B, dated 2026-09-04. The Bible states **Comics only**
on page 1 and refers to a separate Labs manual, GL-BRD-001.

| Evidence | Consequence for this skill |
| --- | --- |
| Bible pp. 8, 18: legible interfaces; mystery belongs in the work | Keep search, navigation, actions, errors, and checkout literal |
| Bible pp. 11-13: Helvetica system / Times document / hand-drawn comic; monochrome comics; artifact colors | Preserve artwork and product assignments; scope software effects to the interface |
| Bible pp. 12, 21-22: Eurostile remains Labs; Times is shared | Do not assume the Comics typography change rewrites every Labs product |
| Bible pp. 8, 17, 22: no goose identity; GOOSCORP is not the brand voice | Do not invent a goose mascot or a fictional company narrator |
| Bible pp. 14, 20-21: serious execution | Refine the behavior and finish, even for an absurd product |
| Bible pp. 21-22: Labs follows its own interface rules | Permit the expressly requested software color and retro variants |

The one-pager repeats the five Comics invariants, type roles, artifact colors,
plain voice, and clear checkout requirement on its single page.

The books own red `#DA291C`, blue `#0033A0`, and green `#009639`; yellow `#FFCD00`
is reserved for a future major artifact. Goosklerf owns its closed three-color set.
These are product assignments, not a complete application status palette. This
skill's UI tokens do not reassign any artifact's color or recolor comic linework.

Restrained blue title gradients, control bevels, semantic accent colors, and the
catalog specimen are new design choices for this requested software variant.
Do not describe them as immutable historical brand rules.

## Inspectable provenance

Source review date: 2026-10-23. These pointers document the foundation; they are not
runtime dependencies. Private repositories require the owner's access. Do not copy
private business records, credentials, or unrelated context into a skill package.

- [Current Labs stylesheet](https://github.com/goosnav/goosnav-labs-hq/blob/main/style/global.css)
  — source blob `31fdcc88333f4591c1667c57c55e0ca79cdd8235`.
- [Labs style guide](https://github.com/goosnav/goosnav-labs-hq/blob/main/style/README.md)
  — source blob `43e5fe72845e5781fe922e2b6150c4bcdfc52828`.
- [Labs base layout](https://github.com/goosnav/goosnav-labs-hq/blob/main/src/layouts/Base.astro)
  — source blob `443a22775ae393e20be52df61677c9059fc31663`.
- [Earlier Labs software specification](https://github.com/goosnav/goosnav-labs-hq/blob/main/docs/dev/Goosnav-Labs-Software-Bible.txt), section 03.
- [Comic engine stylesheet](https://github.com/goosnav/3D-comic-engine/blob/main/web/style.css).
- [Brain Labs guidance](https://github.com/goosnav/goosnav-brain/blob/main/01-BRANDING/Goosnav-Labs.md)
  — source blob `64b93e530543d8acd48bbbdfd5e1fb1256df5c2d`.
- [Brain Comics visual identity](https://github.com/goosnav/goosnav-brain/blob/main/01-BRANDING/Visual-Identity.md)
  — source blob `9ae1015146c8a34d2643a2f3d638a0661fd9be60`.
- [W3C text contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- [W3C tabs interaction pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/).
