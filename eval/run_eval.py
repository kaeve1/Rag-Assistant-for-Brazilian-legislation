"""RAGAS-style evaluation harness for the RAG pipeline.

Runs the full retrieve -> rerank -> classify pipeline against a small
hand-labeled golden set (eval/golden_set.jsonl) and reports the same
metrics RAGAS is known for:

  - context_precision / context_recall / mrr  (retrieval quality, computed
    directly from the golden labels — no LLM judge needed)
  - faithfulness                              (is the model's answer
    grounded in the retrieved articles, or is it making things up? scored
    by an LLM judge, RAGAS-style)
  - article_f1 / infringe_accuracy            (did the pipeline point at
    the right law/article, and get the yes/no verdict right?)

Note: this reimplements the RAGAS metrics natively instead of depending on
the `ragas` package, because `ragas` pulls in `scikit-network`, which has no
prebuilt wheel for this Python/OS combo and fails to compile without the
MSVC Build Tools. The metrics and methodology are the same.

Usage: python eval/run_eval.py
"""
import json
import re
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from google import genai  # noqa: E402
from google.genai import errors as genai_errors  # noqa: E402

from app.retrieve import get_retriever  # noqa: E402
from app.llm import classify_situation, LLMError, API_KEY, MODEL  # noqa: E402

GOLDEN_SET_PATH = Path(__file__).resolve().parent / "golden_set.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "results.json"

JUDGE_PROMPT = """Você avalia se uma resposta jurídica está fundamentada no \
contexto fornecido (trechos de lei), sem inventar informação que não está lá.

Contexto (trechos de lei recuperados):
\"\"\"
{context}
\"\"\"

Resposta a avaliar:
\"\"\"
{answer}
\"\"\"

Dê uma nota de 0.0 a 1.0 para "faithfulness": a fração das afirmações na \
resposta que podem ser verificadas/inferidas a partir do contexto acima \
(1.0 = totalmente fundamentada, 0.0 = totalmente inventada/sem relação com \
o contexto). Responda ESTRITAMENTE em JSON: {{"faithfulness": <float>, \
"motivo": "<explicação em 1 frase>"}}"""


def judge_faithfulness(context: str, answer: str) -> dict:
    if not context.strip() or not answer.strip():
        return {"faithfulness": None, "motivo": "sem contexto ou resposta para avaliar"}
    try:
        client = genai.Client(api_key=API_KEY)
        resp = client.models.generate_content(
            model=MODEL,
            contents=JUDGE_PROMPT.format(context=context[:8000], answer=answer[:2000]),
            config={"response_mime_type": "application/json", "max_output_tokens": 300},
        )
        data = json.loads(resp.text)
        return {"faithfulness": float(data.get("faithfulness")), "motivo": data.get("motivo", "")}
    except (genai_errors.APIError, Exception) as e:
        return {"faithfulness": None, "motivo": f"erro no julgamento: {e}"}


ARTICLE_NUM_RE = re.compile(r"(art\.?\s*\d+[a-z]?(?:-[a-z])?)")


def article_key(law: str, article: str) -> tuple[str, str]:
    """Normalize to (law, 'art. n') — drops trailing §/inciso/alínea
    qualifiers (e.g. 'Art. 14, § 1º' -> 'art. 14') so those still count as a
    match against the golden label, which only names the article."""
    article_norm = article.strip().lower()
    m = ARTICLE_NUM_RE.match(article_norm)
    if m:
        article_norm = re.sub(r"\s+", " ", m.group(1)).strip()
    return (law.strip().lower(), article_norm)


def evaluate_item(retriever, item: dict) -> dict:
    situacao = item["situacao"]
    expected = {article_key(l["lei"], l["artigo"]) for l in item.get("leis_esperadas", [])}

    hits = retriever.query(situacao, top_k=6)
    retrieved = [article_key(h["law_short"], h["article"]) for h in hits]
    retrieved_set = set(retrieved)

    # --- retrieval metrics ---
    overlap = expected & retrieved_set
    context_precision = len(overlap) / len(retrieved_set) if retrieved_set else 0.0
    context_recall = (len(overlap) / len(expected)) if expected else None

    mrr = 0.0
    if expected:
        for rank, key in enumerate(retrieved, start=1):
            if key in expected:
                mrr = 1.0 / rank
                break

    # --- generation ---
    try:
        result = classify_situation(situacao, hits)
        error = None
    except LLMError as e:
        result = {"infringe": None, "violacoes": [], "analise": "", "recomendacao": ""}
        error = str(e)

    predicted = {article_key(v.get("lei", ""), v.get("artigo", "")) for v in result.get("violacoes", [])}
    gen_overlap = expected & predicted
    article_precision = len(gen_overlap) / len(predicted) if predicted else (1.0 if not expected else 0.0)
    article_recall = (len(gen_overlap) / len(expected)) if expected else (1.0 if not predicted else 0.0)
    article_f1 = (
        2 * article_precision * article_recall / (article_precision + article_recall)
        if (article_precision + article_recall) > 0
        else 0.0
    )

    expected_infringe = bool(expected)
    infringe_correct = result.get("infringe") == expected_infringe

    context_text = "\n\n".join(h["text"] for h in hits)
    answer_text = result.get("analise", "") + "\n" + json.dumps(result.get("violacoes", []), ensure_ascii=False)
    if result.get("infringe"):
        time.sleep(2)  # space out the two Gemini calls within one item
        faithfulness = judge_faithfulness(context_text, answer_text)
    else:
        faithfulness = {"faithfulness": None, "motivo": "n/a (sem infração apontada)"}

    return {
        "id": item["id"],
        "categoria": item["categoria"],
        "situacao": situacao,
        "expected": sorted(expected),
        "retrieved": retrieved,
        "predicted": sorted(predicted),
        "context_precision": round(context_precision, 3),
        "context_recall": round(context_recall, 3) if context_recall is not None else None,
        "mrr": round(mrr, 3),
        "article_f1": round(article_f1, 3),
        "infringe_correct": infringe_correct,
        "faithfulness": faithfulness["faithfulness"],
        "faithfulness_motivo": faithfulness["motivo"],
        "error": error,
    }


def main():
    items = [json.loads(l) for l in GOLDEN_SET_PATH.open(encoding="utf-8")]
    retriever = get_retriever()

    results = []
    for item in items:
        print(f"[{item['id']}] {item['situacao'][:70]}...")
        t0 = time.perf_counter()
        r = evaluate_item(retriever, item)
        r["latency_s"] = round(time.perf_counter() - t0, 2)
        results.append(r)
        print(
            f"    ctx_precision={r['context_precision']} ctx_recall={r['context_recall']} "
            f"mrr={r['mrr']} article_f1={r['article_f1']} infringe_ok={r['infringe_correct']} "
            f"faithfulness={r['faithfulness']}" + (f" ERROR={r['error']}" if r["error"] else "")
        )
        # two Gemini calls per item (classify + judge) — space them out to
        # stay under the free-tier requests-per-minute limit during a bulk run
        time.sleep(6)

    def avg(key, predicate=lambda r: True):
        vals = [r[key] for r in results if predicate(r) and r[key] is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    summary = {
        "n_items": len(results),
        "context_precision_avg": avg("context_precision"),
        "context_recall_avg": avg("context_recall"),
        "mrr_avg": avg("mrr"),
        "article_f1_avg": avg("article_f1"),
        "infringe_accuracy": round(sum(r["infringe_correct"] for r in results) / len(results), 3),
        "faithfulness_avg": avg("faithfulness"),
    }

    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    for k, v in summary.items():
        print(f"  {k}: {v}")

    RESULTS_PATH.write_text(
        json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nResultados salvos em {RESULTS_PATH}")


if __name__ == "__main__":
    main()
