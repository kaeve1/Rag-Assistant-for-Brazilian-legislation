"""Structured (JSON-lines) request logging for the RAG pipeline.

Every /api/query call emits one JSON line with: the situação (truncated),
which articles were retrieved and their rerank scores, which model answered,
latency, token usage, and the verdict — the minimum needed to debug
retrieval quality and cost after the fact, and a prerequisite for wiring up
a real observability platform (Langfuse/LangSmith/etc.) later without
having to instrument the code again.
"""
import json
import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("rag")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stream_handler)

    file_handler = RotatingFileHandler(
        LOG_DIR / "app.jsonl", maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(file_handler)


def log_query_event(
    *,
    situacao: str,
    hits: list[dict],
    result: dict,
    model: str,
    latency_ms: float,
    usage: dict | None = None,
    error: str | None = None,
) -> None:
    event = {
        "ts": time.time(),
        "event": "query",
        "situacao_preview": situacao[:200],
        "situacao_len": len(situacao),
        "retrieved": [
            {"law": h["law_short"], "article": h["article"], "score": round(h["score"], 4)}
            for h in hits
        ],
        "model": model,
        "latency_ms": round(latency_ms, 1),
        "infringe": result.get("infringe"),
        "confianca": result.get("confianca"),
        "num_violacoes": len(result.get("violacoes", [])),
        "usage": usage,
        "error": error,
    }
    logger.info(json.dumps(event, ensure_ascii=False))
