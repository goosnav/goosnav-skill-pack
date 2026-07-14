# Anti-Slop Field Guide

A catalog of the specific tells that make web design read as generic/AI-generated, each paired with
the fix, plus concrete starting points (typefaces, palettes, scale) that skip the defaults.

## The tells and their fixes

| Slop tell | Why it reads cheap | Fix |
|---|---|---|
| Two-hue diagonal gradient hero (indigo→violet→blue) | It's the #1 default; signals "no palette chosen" | One committed accent on a tinted neutral; if gradient, a subtle single-hue tonal shift |
| Glassmorphism cards + blurred background blobs | Effect standing in for hierarchy | Solid surfaces, real spacing/contrast for hierarchy |
| `Inter`/system-sans everywhere, one weight | No typographic voice | A display + text pairing (below); use weight contrast |
| Near-uniform font sizes, "muted" 60% text everywhere | Hierarchy faked with opacity | A real modular scale; hierarchy via size + weight |
| Universal `border-radius: 12-16px` pillowing | The Bootstrap/Tailwind default look | Commit to `0` or a small `4-6px`; be consistent |
| Soft drop shadow on every element | Shadow as decoration, no light logic | Hairline `1px` borders; shadows only for true elevation, one light source |
| Three centered feature cards w/ pastel icon squares | The canonical template block | Vary layout; asymmetry; real content-driven structure |
| Emoji as icons | Reads as placeholder | A real icon set (Lucide, Phosphor, Heroicons) or none |
| Everything centered | No grid, no tension | Left-align text blocks; use a grid; center only for deliberate emphasis |
| Raw Tailwind `gray-*`/`blue-500` | The signature "untouched defaults" palette | Custom tinted neutral ramp + chosen accent |
| Vague hero copy ("Build faster. Ship smarter.") | Says nothing, could be any product | Specific, concrete copy; the words are part of the design |
| Icon + heading + paragraph, ×N, forever | One rhythm repeated flattens the page | Alternate section shapes; break the pattern intentionally |

## Non-generic typeface pairings

All widely available (Google Fonts / system). Pick to serve the direction, not by habit.

- **Editorial / confident:** Fraunces or Playfair Display (display) + Inter or Source Sans (body).
- **Modern serif body (high trust, warm):** Newsreader or Source Serif 4 (body) + a clean sans for UI.
- **Technical / precise:** Space Grotesk or Archivo (headings) + IBM Plex Sans (body) + IBM Plex Mono
  (labels/code). Mono for small-caps labels is a strong, underused move.
- **Geometric / crisp:** Sora or Manrope (display) + Inter (body) — better than Inter alone because of
  the weight/shape contrast.
- **Neo-grotesque, understated luxury:** a single superfamily used across weights (e.g. IBM Plex or the
  Söhne/Neue Haas family if licensed) — restraint reads as premium when the spacing is right.
- **Character / distinctive:** Instrument Serif or Bricolage Grotesque for display against a neutral
  body — instantly non-default.

Rules: pair a high-contrast/character display with a low-contrast readable body; don't pair two
display faces; a superfamily (sans + serif + mono siblings) always harmonizes.

## Type scale (modular)

Base 16px. Multiply/divide by a ratio to get steps. Two useful ratios:

| Step | 1.2 (minor third — UI/dense) | 1.25 (major third — marketing) |
|---|---|---|
| -1 (small) | 13px | 13px |
| 0 (body) | 16px | 16px |
| 1 | 19px | 20px |
| 2 | 23px | 25px |
| 3 | 28px | 31px |
| 4 | 33px | 39px |
| 5 (display) | 40px | 49px |
| 6 | 48px | 61px |

Marketing display can go much larger (72-140px) — when it does, tighten line-height to ~1.0-1.1 and
tracking slightly negative. Round to whole pixels or use `rem`/`clamp()` for fluid scaling.

## Palette recipes

Build a neutral ramp of ~7 steps from near-white to near-black, **tinted** toward the accent (add a few
degrees of the accent's hue and a little saturation). Then one accent, optionally one secondary.

- **Ink & paper:** warm off-white bg (`hsl(40 30% 97%)`), near-black warm ink (`hsl(30 8% 12%)`), one
  saturated accent (a deep red, forest, or cobalt). Editorial, timeless.
- **Cool slate + one signal:** blue-gray neutrals (`hsl(220 12% X%)`) with a single high-chroma accent
  (electric lime, amber, or magenta) used only for action. Technical, modern.
- **Warm monochrome:** a single hue at varying lightness/saturation for the whole ramp; accent is just
  the most-saturated step. Cohesive, calm, hard to get wrong.

Contrast: verify body ≥ 4.5:1 and large/UI text ≥ 3:1 against its background (WCAG AA). Tools:
`hsl()`/`oklch()` make it easy to hold hue constant and vary only lightness.

## Spacing & layout quick rules

- 4px (or 8px) base scale; nothing off-scale.
- Section vertical padding on marketing pages is usually *bigger than feels necessary* (e.g. 96-160px
  top/bottom on desktop). Cramped sections are a slop tell.
- Content column ~`60-72ch` for text; wider full-bleed bands for contrast.
- Align to a grid; introduce one deliberate asymmetry per view as a focal accent.
- Proximity: reduce space within a group, increase it between groups — this alone reads as "designed."

## When you *do* want an effect

Effects aren't banned — undifferentiated effects are. A grain/noise texture overlay, a duotone photo
treatment, a single tasteful gradient mesh confined to one section, or a bespoke cursor can be great
*if* they serve the one direction and appear once, not everywhere. The test: does it reinforce the
committed mood, or is it there because it was easy?
