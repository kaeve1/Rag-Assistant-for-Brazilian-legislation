# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Vanilla static HTML/CSS/JS, no build step, no framework. Decided in
`PLANO_FRONTEND.md`: `server.py` already serves `/static` as-is, and the
project's size does not justify a Node/Vite/React toolchain. Split into
`static/index.html` + `static/css/styles.css` + `static/js/app.js` +
`static/js/sidebar.js`.

## Users

Two overlapping audiences:
1. People with a real situation who want a quick pointer to which Brazilian
   federal law/article it may infringe (legal triage, not legal advice).
2. Technical reviewers (recruiters, hiring managers, other engineers)
   evaluating this as a portfolio piece demonstrating applied RAG/LLM
   engineering skill.

## Product Purpose

"Ragis" is a RAG (Retrieval-Augmented Generation) system: the user describes
a situation in Portuguese, the system retrieves the most relevant articles
from 11 Brazilian federal legal codes (6,034 articles total) via hybrid
search (dense + BM25 + RRF fusion + cross-encoder reranking), then asks
Gemini to analyze the situation using only that retrieved text as context.
Output: verdict (infringes or not), which law/article, justification,
recommendation, and the source excerpts consulted. Success = an answer
anchored in a verifiable article of law, not model memory.

## Positioning

Most LLM legal-assistant demos generate an answer directly from model
memory. Ragis inverts the flow: retrieval happens first, over the actual
official text (scraped from Planalto, the government's own portal), and
generation is constrained to cite what was retrieved. The retrieval layer
itself is hybrid + reranked (not just single-vector similarity), which is
the detail a naive "chatbot over a PDF" competitor would not replicate.

## Operating Context

Backend: FastAPI (`app/server.py`), single endpoint `POST /api/query`
already implemented and stable — takes `{ situacao }`, returns
`{ infringe, confianca, analise, recomendacao, violacoes: [{lei, artigo,
motivo}], artigos_relevantes: [{law_short, article, score, text}] }`. The
endpoint never returns a raw error; empty input, retrieval failure, or LLM
failure all come back as HTTP 200 with an explanatory message, so the
frontend can always render something sensible. Free-tier Gemini quota is
limited, which is why history in the new frontend is designed to cache full
responses client-side rather than re-querying.

## Capabilities and Constraints

- No auth/session system exists or is planned for this redesign — history
  is client-side only (`localStorage`), per-browser/device.
- No backend changes are in scope for this frontend redesign.
- Content for the explanatory scroll sections (what it is / how it works /
  why it matters / stack) is specified in `PLANO_FRONTEND.md` and should be
  adapted in tone, not invented from scratch.
- 11 legal codes covered: see `README.md` for the exact list and article
  count (6,034 articles) — cite this real number, do not round or invent a
  different one.

## Brand Commitments

- Product name: **Ragis** (nav/title). Subtitle/tagline context: "Legislação
  Brasileira".
- GitHub repo (nav + footer link):
  https://github.com/kaeve1/Rag-Assistant-for-Brazilian-legislation
- Footer contact links: github.com/kaeve1 and
  https://www.linkedin.com/in/kevin-rosa-189b453aa/

## Evidence on Hand

- Real article/law count and pipeline diagram: `ARQUITETURA.md`.
- Real law list and API contract: `README.md`.
- No customer testimonials, case studies, or press exist — do not fabricate
  any for the scroll sections; the "why it matters" section is framed as
  the author's own portfolio/learning narrative, not third-party proof.

## Product Principles

1. Every claim on the page must trace to real code/data (article counts,
   pipeline steps, stack) — this is a technical portfolio piece, credibility
   is the product.
2. The tool must never look broken when the LLM/retrieval layer errors —
   the backend already guarantees a 200 with a message; the frontend must
   render that gracefully.
3. No dark pattern, no fake urgency — this is a triage tool, not a sales
   funnel; CTAs stay honest ("Analisar situação", not manufactured scarcity).
4. Ship without a build step; keep the deploy story (`Dockerfile` copying
   `static/`) unchanged.

## Accessibility & Inclusion

AA contrast minimum on the white ground, visible focus on all interactive
elements, keyboard-navigable sidebar, `aria-expanded` on the mobile drawer
toggle, `prefers-reduced-motion` respected for the scroll-driven area sequence.
Stated explicitly in `PLANO_FRONTEND.md`, not optional.
