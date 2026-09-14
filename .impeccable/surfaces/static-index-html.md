---
version: 1
slug: "static-index-html"
primary_target: "static/index.html"
related_targets: ["static/css/styles.css","static/js/app.js","static/js/sidebar.js"]
---

## Direction contract

THESIS: A legal triage tool earns trust by being plainly legible, so the page
is white paper with black text and one ink of color, and it refuses every
device that makes software look impressive instead of readable: no fixed
navigation bar, no gradients anywhere, no dark chrome, no punctuation dashes
in the prose. The coverage section refuses the static feature grid this
category ships; the reader scrolls through the seven areas of law one at a
time, the way a table of contents reveals itself.

OWN-WORLD: White ground (`#FFFFFF`) with one soft paper tone (`#F5F5F3`) for
recessed blocks, hairline rules (`#E2E2DD`, `#C9C9C2`) instead of shadows and
cards, near-black ink (`#16171B`) for text. One color, a deep magenta
(`#B3164F`), carries section labels, the active rail rule, the send button,
the floating history control on hover, and one full-bleed band at the close;
it clears 4.5:1 on white as text and carries white text at 6.1:1 as a
surface. Every fill is flat: no gradient, no glow, no texture. Grids are
built from 1px gaps over a rule-colored background so cells read as a ruled
table, not as floating cards. IBM Plex Sans throughout, JetBrains Mono
uppercase and tracked for labels, counts, scores and footer links. Corners
are pills for anything pressed and 14px for anything read.

STORY: The visitor lands on white with an input already waiting, types or
clicks an example, and gets the verdict, the article and the source excerpts
inline. Scrolling, the page walks them through what it actually covers: seven
areas of Brazilian federal law, one at a time, each naming its real statutes
and article counts, each offering a real situation they can send straight
back into the tool. Then the pipeline that produced the answer, the real
retrieval excerpt and the real evaluation metrics including the weak one, the
stack, and a closing note in the author's voice on the one colored surface of
the page.

FIRST VIEWPORT: No navigation bar at all. A full-height white field, centered:
a small "Ragis" wordmark with a flat magenta square, a two-line display
headline, one muted line carrying the real numbers (11 códigos, 6.034
artigos), the pill input with a flat magenta send button, and four example
chips. The result renders inline directly beneath. A dark pill labelled
"Histórico" floats at the bottom right, the only fixed element on the page,
carrying a count badge.

FORM: Pinned by the user in session: white palette, no top nav, no gradients,
no punctuation dashes, and Cerebrium's "Why Cerebrium" behavior copied
literally, several sections in one that reveal as you scroll, with its four
feature names replaced by the seven areas of law this project actually covers.
A sticky rail on the left tracks the scroll through the seven areas; the
inactive ones sit at 32% opacity and the active one resolves to full, with its
article count appearing beside it. The rail collapses to wrapping pills under
900px, where the fade is dropped and every area reads at full strength.

FINISH: unreviewed and undocumented is unfinished; this build ends with the
finish review, the verdict, DESIGN.md, and every shipping raster carrying its
provenance.
