---
name: Ragis
description: A white-paper legal triage surface with one ink of color, hairline rules instead of cards, and a scroll-driven walk through seven areas of Brazilian federal law.
colors:
  paper: "#FFFFFF"
  paper-soft: "#F5F5F3"
  rule: "#E2E2DD"
  rule-strong: "#C9C9C2"
  ink: "#16171B"
  ink-muted: "#5A5E6B"
  ink-faint: "#666A77"
  accent: "#B3164F"
  accent-soft: "#FBEEF3"
  danger: "#A3231C"
  danger-bg: "#FCEFEE"
  partial: "#8A5A00"
  partial-bg: "#FDF4E3"
  partial-rule: "rgba(138, 90, 0, 0.35)"
  glass-fill: "rgba(255, 255, 255, 0.72)"
  glass-edge: "rgba(255, 255, 255, 0.55)"
  rule: "rgba(0, 0, 0, 0.10)"
  rule-strong: "rgba(0, 0, 0, 0.18)"
  rule-contrast: "rgba(0, 0, 0, 0.28)"
  scrim: "rgba(0, 0, 0, 0.28)"
  shadow: "rgba(0, 0, 0, 0.35)"
  shadow-soft: "rgba(0, 0, 0, 0.45)"
typography:
  display:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "clamp(2.1rem, 5.4vw, 4rem)"
    fontWeight: 600
    lineHeight: 1.14
    letterSpacing: "-0.022em"
  headline:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "clamp(1.9rem, 4.4vw, 3.4rem)"
    fontWeight: 600
    lineHeight: 1.14
    letterSpacing: "-0.022em"
  title:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "clamp(1.45rem, 2.6vw, 2rem)"
    fontWeight: 600
    lineHeight: 1.14
    letterSpacing: "-0.022em"
  subtitle:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
    lineHeight: 1.14
    letterSpacing: "-0.022em"
  body:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  body-small:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  label:
    fontFamily: "JetBrains Mono, IBM Plex Mono, monospace"
    fontSize: "0.78rem"
    fontWeight: 500
    lineHeight: 1.55
    letterSpacing: "0.1em"
  meta:
    fontFamily: "JetBrains Mono, IBM Plex Mono, monospace"
    fontSize: "0.72rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0.06em"
  statement:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "clamp(1.15rem, 2.2vw, 1.5rem)"
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: "-0.015em"
  mark:
    fontFamily: "Familjen Grotesk, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "normal"
  readout:
    fontFamily: "JetBrains Mono, IBM Plex Mono, monospace"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
rounded:
  hairbar: "2px"
  focus: "4px"
  skip: "6px"
  icon: "7px"
  row: "8px"
  control: "9px"
  card: "10px"
  pill: "12px"
  input: "18px"
  bubble: "20px"
  circle: "50%"
spacing:
  hair: "1px"
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "20px"
  xl: "26px"
  gutter: "24px"
  section-gap: "56px"
  panel-gap: "96px"
  section-pad: "112px"
components:
  button-send:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    width: "40px"
    height: "40px"
  button-send-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  button-send-disabled:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
  input-pill:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.input}"
    padding: "8px 8px 8px 20px"
  chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.pill}"
    padding: "7px 14px"
    typography: "{typography.body-small}"
  chip-hover:
    backgroundColor: "{colors.accent-soft}"
    textColor: "{colors.accent}"
  history-fab:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "12px 19px"
    typography: "{typography.label}"
  history-fab-hover:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.paper}"
  button-clear:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.pill}"
    padding: "10px"
    typography: "{typography.label}"
  button-clear-armed:
    backgroundColor: "{colors.danger-bg}"
    textColor: "{colors.danger}"
  card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.card}"
    padding: "18px 20px"
  card-recessed:
    backgroundColor: "{colors.paper-soft}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.card}"
    padding: "22px 24px"
  verdict-infringe:
    backgroundColor: "{colors.danger-bg}"
    textColor: "{colors.danger}"
    rounded: "{rounded.card}"
    padding: "13px 18px"
  verdict-ok:
    backgroundColor: "{colors.ok-bg}"
    textColor: "{colors.ok}"
    rounded: "{rounded.card}"
    padding: "13px 18px"
  verdict-unknown:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "13px 18px"
  area-try:
    backgroundColor: "{colors.paper-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "16px 18px"
  area-try-hover:
    backgroundColor: "{colors.accent-soft}"
    textColor: "{colors.ink}"
  rail-item:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-faint}"
    rounded: "{rounded.xs}"
    padding: "11px 0 11px 18px"
  rail-item-active:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
  cite:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.cite}"
    padding: "18px 20px"
  drawer:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "min(380px, 88vw)"
---

# Design System: Ragis

## Overview

**Creative North Star: "The Official Gazette, Set in Plain Type"**

Ragis is a legal triage tool, and its credibility is the product. The world is
therefore built like a well printed government document rather than like
software: a white sheet, black text, hairline rules, and exactly one ink of
color. Nothing on the page is trying to look impressive. Every surface either
holds text or separates text from text.

Depth is refused as a device. There are no floating cards, no glows, no
textures, and no gradients of any kind in the stylesheet. Where a grid is
needed, it is drawn as a ruled table: a rule-colored background showing
through 1px gaps between white cells. Where a block needs to recede, it takes
the single soft paper tone. Shadow appears only under the two objects that
genuinely float above the sheet, the fixed history pill and the history
drawer.

The page is also deliberately unchromed. There is no top navigation bar at
all; the first viewport is a full-height white field with the input already
waiting. The one moment of movement in the whole system is the coverage
sequence, where seven panels of law fade in and out of focus against a sticky
rail as the reader scrolls. That sequence is the signature; everything else
holds still.

**Key Characteristics:**
- White paper ground, near-black ink, one deep magenta accent and nothing else
- Zero gradients: every fill in the system is flat
- Hairline rules do the work that shadows and cards do elsewhere
- No fixed navigation; the only fixed element is a dark history pill bottom right
- Familjen Grotesk for reading, JetBrains Mono for anything a machine measured
- One scroll-driven sequence carries all the motion in the system

## Colors

A printed-paper neutral set carrying a single saturated ink, plus two muted
status pairs borrowed from document annotation rather than from UI alerts.

### Primary
- **Deep Magenta Ink** (`{colors.accent}`): the only accent in the system. It carries section eyebrow labels, the active rail rule, the send button fill, the tech icons, the step names, the "testar esta situação" label, citation scores, link hover, focus rings, text selection, and the single full-bleed band at the close of the page. It clears 4.5:1 as text on white and carries white text at 6.1:1 as a surface.
- **Magenta Tint** (`{colors.accent-soft}`): the accent at wash strength. Used for hover fills on chips and the try button, the active history row, and the 4px focus halo around the input pill. Never carries text of its own color; text over it stays ink or accent.

### Neutral
- **Paper** (`{colors.paper}`): the page ground and the fill of every card, cell and drawer. The default answer for any surface.
- **Soft Paper** (`{colors.paper-soft}`): the one recessed tone. Used for the proof blocks, the loading card, the try button at rest, hover fills on drawer rows, and the scrollbar track. There is no third surface tone.
- **Hairline** (`{colors.rule}`): the standard 1px divider and card border, and the background that shows through ruled grids.
- **Hairline Strong** (`{colors.rule-strong}`): the heavier stroke, reserved for controls that must read as controls at rest: the input pill border, the clear button outline, the scrollbar thumb.
- **Ink** (`{colors.ink}`): body and heading text, and the fill of the floating history pill.
- **Muted Ink** (`{colors.ink-muted}`): secondary prose, card body copy, leads, drawer row labels.
- **Faint Ink** (`{colors.ink-faint}`): meta text, counts, disclaimers, placeholders, inactive rail items.

### Status
- **Alert Red** (`{colors.danger}`) on **Alert Wash** (`{colors.danger-bg}`): the infringement verdict banner, the error card border and text, the armed destructive button, and the history delete hover.
- **Clear Green** (`{colors.ok}`) on **Clear Wash** (`{colors.ok-bg}`): the no-infringement verdict banner only.

### Named Rules
**The One Ink Rule.** The system has exactly one accent. There is no secondary and no tertiary color. If a new surface seems to need a second accent, it needs a hairline or a soft paper tone instead.

**The Flat Fill Rule.** Every fill in this system is a flat color. No gradient, no glow, no texture, no tinted blur. This is an invariant, not a default. Audit test: `grep gradient` over the stylesheet must return zero.

**The Hairline Before Shadow Rule.** Separation is drawn, not lit. A 1px hairline, a rule-colored gap, or the soft paper tone resolves nearly every grouping problem. Shadow is reserved for objects that literally float.

## Typography

**Display Font:** Familjen Grotesk (with system sans fallback)
**Body Font:** Familjen Grotesk (with system sans fallback)
**Label/Mono Font:** JetBrains Mono (with IBM Plex Mono, then monospace)

**Character:** One humanist grotesque does all the reading, tightened at
display sizes (-0.022em, line-height 1.14) so headlines set as compact blocks
rather than airy ones. The mono face never sets prose; it appears only where
the page is reporting something counted or measured, which makes numbers on
this page look like evidence.

### Hierarchy
- **Display** (600, `{typography.display.fontSize}`, 1.14): the single page headline in the first viewport. One per page.
- **Headline** (600, `{typography.headline.fontSize}`, 1.14): the three section titles (coverage, pipeline, stack).
- **Title** (600, `{typography.title.fontSize}`, 1.14): the name of each of the seven area panels.
- **Subtitle** (600, 1rem, 1.14): card-level headings inside ruled grid cells (step and tech names).
- **Body** (400, 1rem, 1.55): lead paragraphs and card prose. Measure is capped: 52ch for the hero sub, 56ch for area leads, 42ch for the closing note, 58ch for the footer disclaimer.
- **Body Small** (400, 0.9rem, 1.55): grid cell copy, source snippets, drawer rows, violation reasons.
- **Label** (mono, 500, 0.78rem, 0.08em to 0.1em, uppercase): section labels, card field labels, step names, the try-button label, the history pill, the clear button, footer links.
- **Meta** (mono, 400, 0.72rem, 0.06em): article counts, retrieval scores, confidence, citation chapter line, metric keys.
- **Readout** (mono, 400, 1.15rem, tabular-nums): the evaluation metric values.

The shipped size set is exactly five fixed steps, in rem: 0.72, 0.78, 0.9, 1,
1.15, plus 1.35 for the section mark in the wordmark, plus the three clamps above and the closing note's
`clamp(1.15rem, 2.2vw, 1.5rem)`. Nothing else ships. An earlier build carried
twenty-two steps, several within three percent of each other, which is ad hoc
sizing rather than a scale; they were collapsed onto these five. New surfaces
reuse from this set rather than introduce further steps.

### Named Rules
**The Mono Means Measured Rule.** JetBrains Mono is only for facts a machine produced or a label naming a field: counts, scores, metric keys and values, uppercase section and field labels. It never sets a sentence.

**The No Dash Rule.** No em dashes and no en dashes appear anywhere in the prose of this product. Use a comma, a colon, or a full stop. Hyphens inside real technical names are deliberate and stay: cross-encoder, rank-bm25, sentence-transformers, top-k.

**The One Display Rule.** One display-size headline per page, in the first viewport. Sections below it start at headline size.

## Layout

The page is a single centered column of full-width sections, each capped at a
1140px content maximum with a 24px gutter that tightens to 16px under 560px.
Sections open with 112px of top padding, dropping to 84px under 900px. There
is no top navigation and no sticky header; the only fixed elements are the
history pill (bottom right, 24px inset, 14px under 560px) and the drawer it
opens.

The first viewport is a full-height (`100vh`) centered field with its content
capped at 880px, and the input pill, chips and inline result all capped at
680px so the answer lands in the same measure as the question.

The coverage section is a two-column grid: a sticky rail of
`minmax(230px, 280px)` at `top: 96px` beside a 1fr column of panels separated
by 96px, with a 64px column gap. Under 900px it collapses to one column, the
rail becomes a static wrapping row of pills, and panel spacing drops to 64px.

Grids step down predictably: the pipeline grid runs 4 columns, then 2 under
900px, then 1 under 560px; the stack grid runs 3, then 2, then 1; the proof
pair runs 2, then 1; the chips row becomes a 2-up grid under 560px.

Spacing rhythm is tight and paper-like. Inside components: 4 to 12px. Between
elements in a block: 14 to 26px. Between blocks: 40 to 64px. Between the
coverage panels: 96px. Between sections: 112px.

### Named Rules
**The Ruled Table Rule.** Multi-cell grids are built as a 1px gap over a hairline-colored background, inside a single 1px hairline border with `overflow: hidden` and a 14px radius. Cells are plain white with no border of their own. The result reads as one ruled table, not as a row of floating cards. Both the pipeline grid and the stack grid are built this way and any new grid should be too.

**The No Chrome Rule.** The page carries no top navigation bar, no sticky header, and no persistent side nav. Wayfinding happens through the scroll sequence and the section rail.

## Elevation & Depth

This system is flat by conviction. Depth is expressed by hairlines, by the
single soft paper tone, and by opacity in the coverage sequence. Cards do not
lift on hover; they change border color or background tint instead. Only two
objects in the entire build cast a shadow, and both of them genuinely float
over the page rather than sit in it.

### Shadow Vocabulary
- **Floating control** (`box-shadow: 0 8px 20px -8px rgba(22, 23, 27, 0.45)`): the fixed history pill at rest.
- **Floating control raised** (`box-shadow: 0 12px 26px -10px rgba(22, 23, 27, 0.55)`): the same pill on hover.
- **Drawer edge** (`box-shadow: -20px 0 44px -28px rgba(22, 23, 27, 0.5)`): the right drawer, separating it from the page beneath.
- **Focus halo** (`box-shadow: 0 0 0 4px var(--accent-soft)`): the input pill on focus-within. A tint ring, not a glow.

### Named Rules
**The Two Shadows Rule.** Shadows belong only to elements with `position: fixed`. Everything in the document flow is flat. All shadows are soft, downward, and heavily negative-spread; a hard offset shadow does not belong in this world.

## Shapes

Corners follow function. Anything pressed is a pill (`{rounded.pill}`): chips,
the history pill and its count badge, the clear button, the mobile rail items,
the scrollbar thumb. The send button is a 40px circle. Anything read is 14px
(`{rounded.card}`): cards, verdict banners, the try button, the proof blocks,
and the ruled grids. The citation block sits one step tighter at 12px, drawer
rows at 10px, small icon buttons at 8px, and the focus outline at 4px. The
input pill is 26px, half its own height, so it reads as a capsule.

Strokes are always exactly 1px and always a rule color, with one exception:
the coverage rail item carries a 2px left border that switches from hairline
to accent when active. The wordmark mark is a flat 20px accent square with a
6px radius, the only decorative geometry in the system.

Icons are authored inline SVG on a 24px viewBox with `currentColor` strokes:
1.5px in the stack grid, 2px everywhere else. Rendered sizes are 14px (history
pill), 16px (drawer close), 17px (send, verdict), and 22px (stack).

### Named Rules
**The Pressed Is A Pill Rule.** If it takes a click, it is a pill or a circle. If it holds text to read, it is 14px. There is no square-cornered surface in this system and no radius above 26px that is not a full pill.

## Components

### Buttons
- **Shape:** circle for send (40px), pill for every other standalone button, 14px for the full-width try block.
- **Send:** flat accent circle with white icon, 17px arrow glyph. Hover scales to 1.06 and flips the fill to ink. Disabled drops to 0.45 opacity with no fill change. Loading swaps the arrow for a dashed-circle spinner rotating at 0.8s linear.
- **History pill (floating control):** ink fill, white mono uppercase label, optional white count badge in ink text. Hover flips the fill to accent and deepens the shadow. This is the only fixed control on the page.
- **Clear (destructive, two step):** ghost pill with a strong hairline outline and muted ink label. Hover turns the label and border red. First click arms it, swapping the label to a confirmation question and filling it with the alert wash; blur disarms it and restores the original label. Destruction never happens on a single click.
- **Hover / Focus:** all transitions run 0.15s to 0.28s on `cubic-bezier(0.16, 1, 0.3, 1)`. Focus is a 2px accent outline at 3px offset with a 4px radius, globally, on every focusable element.

### Chips
- **Style:** white pill, hairline border, muted ink label at 0.8rem, 7px by 14px padding.
- **State:** hover turns border and text accent and fills with the magenta tint. There is no selected state; a chip fires an action and the result renders below.

### Cards / Containers
- **Corner Style:** 14px.
- **Background:** white for content cards, soft paper for recessed blocks (proof, loading, try).
- **Shadow Strategy:** none. See Elevation.
- **Border:** 1px hairline. The error variant swaps border and text to alert red.
- **Internal Padding:** 18px by 20px for content cards, 22px by 24px for recessed blocks, 22px to 26px inside ruled grid cells.
- **Internal dividers:** repeated rows inside a card (violations, source hits, metrics) are separated by a 1px hairline, with the first row's top border and the last row's bottom border removed so the group reads as one block.

### Inputs / Fields
- **Style:** a 26px capsule, white fill, strong hairline border, 8px padding with a 20px left inset, aligned to flex-end so the send button stays at the bottom as the field grows.
- **Textarea:** borderless and transparent inside the capsule, autogrowing on input to a 160px ceiling (170px CSS max), faint ink placeholder. Enter submits, Shift+Enter breaks the line.
- **Focus:** the capsule border turns accent and gains a 4px magenta tint halo. The inner textarea has no outline of its own.

### Navigation
There is no navigation bar. The only navigational control is the coverage
rail (below) and the footer link row: mono, uppercase, 0.74rem, tracked
0.08em, muted ink, turning accent on hover.

### Area Sequence (signature component)

The coverage section is one scroll instrument, not a grid of features.

- **Structure:** a sticky rail of seven buttons pinned at `top: 96px` beside a column of seven article panels spaced 96px apart, with 6vh of tail padding so the last panel can reach the activation band.
- **Tracking:** an IntersectionObserver with `rootMargin: '-35% 0px -35% 0px'` and thresholds `[0, 0.25, 0.5, 0.75, 1]` watches all seven panels, keeps their ratios in a map, and marks the highest-ratio panel active on every callback. If IntersectionObserver is unavailable, every panel is activated at once and the section degrades to a plain list.
- **Panel state:** inactive panels sit at `opacity: 0.32` and the active one resolves to 1 over 0.5s on the standard ease. Nothing moves, nothing scales; only focus changes.
- **Rail state:** each item is a left-aligned ghost button with a 2px hairline left border and faint ink label. Active turns the border accent, the label ink at weight 600, and fades in the article count (mono, 0.68rem) beneath it, which is invisible otherwise.
- **Jump:** rail items are real buttons. Clicking one sets the active pair immediately and smooth-scrolls its panel to the viewport center.
- **Panel content:** area title, a lead capped at 56ch, a hairline-ruled list of the real statutes with their real article counts right-aligned in mono, then a full-width try block.
- **Try block:** a soft-paper 14px button with a mono accent uppercase label and the example situation in quotes. Clicking it fills the input, scrolls back to the first viewport, and submits for real. Hover turns the border accent and the fill to magenta tint.
- **Under 900px:** the rail becomes a static wrapping row of hairline pills (active takes an accent border and tint fill), the counts are hidden, and every panel reads at full opacity.
- **Reduced motion:** `prefers-reduced-motion: reduce` sets all panels to full opacity, so the section is fully legible without the fade. Global smooth scrolling is also disabled and all transitions collapse to 0.01ms.

### Verdict Banner
A flat 14px band above the result with three states, each an authored 24px SVG
at 17px beside a 0.93rem semibold verdict line, with the confidence value
pushed right in mono at 0.7rem. Infringement takes alert red on alert wash
with a warning triangle; no infringement takes clear green on clear wash with
a check; an undetermined verdict takes no fill at all, defaulting to ink on
white with a question-mark circle. The neutral state is the honest one and it
is intentionally the quietest.

### Sources Block
A `<details>` card whose summary is a muted 0.86rem row; the native marker is
removed and a chevron rotates 90 degrees on open, with 12px of space opening
beneath the summary. Each hit inside is a hairline-separated row with a mono
meta line carrying the law, article and retrieval score, and the excerpt
truncated at 400 characters.

### Citation Block
A white 12px card with a mono head row splitting the law reference left and
the retrieval score right in accent with tabular numerals, the quoted article
text at 0.9rem and line-height 1.6, and a mono footer naming chapter, section
and statute in faint ink.

### Metric Readout
A hairline-separated list pairing a mono key in muted ink at 0.8rem with a
mono value at 1.15rem in tabular numerals, last row unruled, followed by a
0.78rem faint note. The weak metric is listed alongside the strong ones in
identical treatment; the system gives no visual advantage to the flattering
number.

### History Drawer
A right-anchored panel, `min(380px, 88vw)` wide, full height, white with a
left hairline and an edge shadow, sliding in over 0.28s on the standard ease
while a 35% ink backdrop fades in over 0.25s. Closed, the drawer is `inert`
and translated fully off-canvas. Rows are 10px ghost buttons, single-line with
ellipsis, hovering to soft paper and taking the magenta tint when active; each
row's delete icon is hidden at 0 opacity until row hover or its own
focus-visible, and turns alert red on the alert wash on hover.

## Do's and Don'ts

### Do:
- **Do** keep every fill flat. One color per surface, always.
- **Do** build multi-cell grids as a 1px gap over a hairline background inside one bordered, clipped container, per The Ruled Table Rule.
- **Do** reach for a hairline, the soft paper tone, or a border-color change before reaching for a shadow or a lift.
- **Do** reserve JetBrains Mono for counts, scores, metric keys and uppercase field labels, and set all prose in Familjen Grotesk.
- **Do** cap reading measure explicitly (42ch to 58ch for prose blocks, 680px for the question-and-answer column).
- **Do** give every destructive action a two-step arm and confirm, and disarm it on blur.
- **Do** author icons as inline SVG on a 24px viewBox using `currentColor`.
- **Do** give every scroll or opacity effect a `prefers-reduced-motion` path that leaves the content at full strength.
- **Do** write prose without em dashes or en dashes, keeping hyphens inside real technical names.

### Don't:
- **Don't** add a gradient, glow, or texture anywhere. Zero is the current count and it is the target.
- **Don't** introduce a second or third accent. One ink carries every emphasis in the system.
- **Don't** add a fixed top navigation bar or a sticky header. The history pill is the only fixed control.
- **Don't** put a shadow on anything in the document flow, and never a hard offset shadow anywhere.
- **Don't** give ruled-grid cells their own borders or radii; the container owns both.
- **Don't** set a square corner or a radius between 26px and a full pill.
- **Don't** make the fade in the area sequence load-bearing for legibility; the text must read at 0.32 opacity and the sequence must survive a missing IntersectionObserver.
- **Don't** style a weak number differently from a strong one in the metric readout.
