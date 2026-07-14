---
name: aesthetic-web-design
description: >-
  Design genuinely good-looking web interfaces that read as intentional, human, and high-craft --
  the opposite of generic AI-generated "slop." Use this whenever the visual quality of a web page or
  app matters: landing pages, marketing sites, portfolios, hero sections, dashboards, pricing pages,
  product UI, or any time the user says "make it beautiful", "make it look good/premium/polished",
  "not generic", "not templated", "distinctive", "high-end", "modern", "clean but not boring", or
  reacts that something looks "AI-generated", "cheap", or "like every other site". Covers art
  direction, type, color, spacing, layout, components, motion, and a final polish pass. Produces
  CSS/HTML (framework-agnostic; works with plain CSS, Tailwind, or any stack). Pair with a component
  library skill for implementation; this skill owns the taste and the decisions.
---

# Aesthetic Web Design

## What this is for

Make web pages that look like a person with taste made them on purpose. The bar is not "clean" —
clean is easy and forgettable. The bar is **intentional, coherent, and distinctive**: every choice
looks deliberate, the whole thing hangs together as one system, and it doesn't look like the default
output everyone else ships.

This skill owns the *design decisions*. It produces real CSS you can drop into any stack. It does not
depend on a particular framework — the same type scale, palette, and spacing system express fine in
plain CSS, Tailwind, or CSS-in-JS.

## The anti-slop thesis

Most AI-generated (and template-generated) web design fails the same way: it reaches for the safest
default at every fork, and safe defaults stacked on safe defaults read as generic. The fix is not
"more effects" — it's **committing to a point of view** and executing the fundamentals precisely.

Read `references/anti-slop.md` for the full field guide. The short version — if your design has these,
stop and reconsider:

- A purple/indigo→blue gradient hero, glassmorphism cards, and a big blurred blob background.
- `Inter` / system-sans for everything, one weight, no real type scale.
- Three feature cards, each with a rounded-square pastel icon and a one-line heading.
- Everything centered, everything `border-radius: 12px`, a soft drop shadow on every element.
- Tailwind's default `gray-*` / `blue-500` palette used raw.
- Emoji as iconography; hero copy that says "Build faster. Ship smarter." and means nothing.
- Uniform 60-70% opacity "muted" text everywhere instead of a real type hierarchy.

None of these are *illegal* — they're just what "no decision was made" looks like. Quality comes from
the opposite: a chosen typeface with intent, a committed palette, a real spatial system, one clear
focal point, and details that reward a second look.

## Workflow

Do these in order. Direction before pixels — skipping to components is how you end up with slop.

### 1. Establish a direction (before any CSS)

Pick a **reference and a mood** and write it down in one line: e.g. *"editorial print magazine — big
serif display, generous margins, one ink color + paper"* or *"technical/industrial — mono labels,
tight grid, hairline rules, near-black on off-white."* Name 2-3 adjectives you're committing to
(e.g. *warm, confident, unfussy*) and, just as important, 2-3 you're rejecting (*not playful, not
corporate, not techy-neon*). Every later decision serves this line. If you can't name the direction,
you'll default to slop.

### 2. Set the type system

Type is 80% of perceived quality on the web. Get this right and the page is already most of the way
there.

- **Choose a real pairing**, not one sans for everything. A display face with character for headings +
  a highly readable face for body is the reliable move. Superfamilies (a sans + its serif/mono
  sibling) pair safely. See `references/anti-slop.md` for specific non-generic pairings.
- **Build a modular scale**, don't eyeball sizes. Pick a base (16-18px body) and a ratio (~1.2 minor
  third for dense UI, ~1.25-1.33 for marketing) and generate steps. Real jumps between levels create
  hierarchy; timid 2px increments read as mush.
- **Set the body measure to 60-75 characters** (`max-width: ~65ch`). Long lines are the single most
  common readability failure.
- **Line-height inversely with size**: ~1.5-1.65 for body, ~1.05-1.2 for large display. Tighten
  tracking slightly on big display type; never track-out lowercase body.
- Use weight and size for hierarchy before you reach for color or opacity.

### 3. Commit to a palette

- **One dominant neutral family + one (maybe two) accents.** Not a rainbow. The accent earns attention
  precisely because it's rare — CTA, links, one key highlight.
- **Neutrals should be tinted, not pure gray.** Nudge them warm or cool toward the accent; pure
  `#888` is the default-gray tell. Build a ramp of ~6-8 steps and use it consistently.
- **Check contrast** — body text ≥ 4.5:1, large text ≥ 3:1 (WCAG AA). Beautiful and unreadable is a
  failure, not a trade-off.
- If you use a gradient, make it *subtle and purposeful* (a slight tonal shift within one hue), not a
  two-hue diagonal spectacle.

### 4. Impose a spatial system

- **One spacing scale** (e.g. 4px base: 4, 8, 12, 16, 24, 32, 48, 64, 96…). Every margin and pad comes
  from it. Arbitrary `13px`/`27px` values are visible as sloppiness even when nobody can name why.
- **Use whitespace as a material**, generously and unevenly. Tight groups + wide gaps between groups
  create rhythm (proximity = relationship). Even, cramped spacing everywhere reads as cheap.
- **Establish a grid and let things break it intentionally.** Alignment to a shared grid is what makes
  a layout feel engineered rather than assembled. One deliberate break from the grid draws the eye —
  that's a focal point, use it sparingly.
- **One primary focal point per view.** Decide what the eye hits first and make the hierarchy enforce
  it. If everything is bold, nothing is.

### 5. Design the components to the system

Buttons, cards, inputs, nav — derive them from the tokens above, don't restyle each ad hoc. Consistent
radius (pick one or two values and commit — sharp/`0` and small/`4-6px` both read as more intentional
than universal `12-16px` pillows), consistent borders (a hairline `1px` in a neutral often beats a
shadow), consistent interactive states. Shadows: if used, make them soft, low-opacity, and physically
plausible (single light source) — not a glow on everything.

### 6. Add motion with restraint

Motion should feel like the interface responding, not decoration. Fast (`150-250ms`), eased
(`ease-out` for enter), on real interactions (hover, focus, disclosure). Respect
`prefers-reduced-motion`. One considered transition beats ten autoplaying ones. No parallax-for-its-
own-sake, no elements flying in on scroll unless it earns its keep.

### 7. Polish pass

Great design is separated from good design in the last 10%. Walk the page and fix:

- Optical alignment (icons/text often need a nudge past mathematical centering).
- Consistent corner radii, border weights, and shadow across every component.
- Real content, not lorem — bad copy makes good layout look bad.
- Empty, loading, error, and hover/focus states actually designed.
- Responsive: the type scale and spacing should *shrink sensibly*, not just reflow. Check ~375px and a
  wide viewport.
- Dark mode (if in scope) is a designed palette, not `invert()`.

## Operating principles

- **Commit, don't hedge.** A design with a clear opinion that some dislike beats a safe one nobody
  remembers. Slop is the average of all choices; taste is a specific choice.
- **Fundamentals over effects.** Type, spacing, hierarchy, and color decide 90% of quality. Reach for
  glass/gradient/blur last, if at all.
- **Consistency reads as competence.** Tokens (scale, palette, spacing, radius) applied uniformly are
  what make a page feel professionally made.
- **Readability is not negotiable.** Contrast, measure, and hierarchy come before decoration.
- **Distinctive, not weird.** The goal is a memorable point of view executed cleanly — not novelty that
  fights usability.

## Reference files

- `references/anti-slop.md` — the detailed catalog of slop tells and their fixes, plus concrete
  non-generic typeface pairings, palette recipes, and a type-scale table. Read before designing.
- `references/starter-tokens.css` — a ready-to-adapt CSS custom-property system (type scale, tinted
  neutral ramp, spacing scale, radius, motion) with comments on what to change. Start here, then bend
  it to the chosen direction — don't ship it unchanged.

## Verification checklist

Before calling a design done, confirm:

- [ ] I can state the design direction in one sentence, and the page obviously serves it.
- [ ] Headings and body use a real type scale (distinct, intentional steps), not near-uniform sizes.
- [ ] Body measure is ~60-75 characters; body text passes 4.5:1 contrast.
- [ ] The palette is one neutral family + ≤2 accents; neutrals are tinted, not pure gray.
- [ ] All spacing comes from one scale; groups use proximity to show relationship.
- [ ] There is exactly one primary focal point per view.
- [ ] Radius, border, and shadow are consistent across components.
- [ ] Motion is fast, purposeful, and respects `prefers-reduced-motion`.
- [ ] None of the anti-slop tells from `references/anti-slop.md` are present unintentionally.
