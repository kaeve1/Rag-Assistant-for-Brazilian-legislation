import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .retrieve import get_retriever
from .llm import classify_situation, LLMError, MODEL
from .logging_config import log_query_event

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="RAG LGPD / Direito Digital Brasileiro")


class Esclarecimento(BaseModel):
    pergunta: str
    resposta: str


class QueryRequest(BaseModel):
    situacao: str
    top_k: int = 6
    historico: list[Esclarecimento] = []


class ArticleHit(BaseModel):
    law_short: str
    law_name: str
    article: str
    chapter: str | None = None
    section: str | None = None
    text: str
    score: float


class QueryResponse(BaseModel):
    infringe: bool | None
    confianca: str | None
    violacoes: list[dict]
    analise: str
    recomendacao: str
    pergunta: str = ""
    artigos_relevantes: list[ArticleHit]


def _empty_response(analise: str, hits: list | None = None) -> QueryResponse:
    return QueryResponse(
        infringe=None,
        confianca=None,
        violacoes=[],
        analise=analise,
        recomendacao="",
        pergunta="",
        artigos_relevantes=[ArticleHit(**h) for h in (hits or [])],
    )


@app.post("/api/query", response_model=QueryResponse)
def query(req: QueryRequest):
    start = time.perf_counter()
    situacao = req.situacao.strip()
    if not situacao:
        return _empty_response("Nenhuma situação foi informada. Descreva o que aconteceu para que eu possa analisar.")

    # As respostas de esclarecimento entram na busca: sem isso, a segunda
    # chamada recuperaria exatamente os mesmos artigos da primeira.
    historico = [t.model_dump() for t in req.historico]
    texto_busca = " ".join(
        [situacao] + [t["resposta"] for t in historico if t.get("resposta")]
    )

    try:
        retriever = get_retriever()
        hits = retriever.query(texto_busca, top_k=req.top_k)
    except Exception as e:
        log_query_event(
            situacao=situacao, hits=[], result={}, model=MODEL,
            latency_ms=(time.perf_counter() - start) * 1000, error=f"retrieval: {e}",
        )
        return _empty_response(f"Não foi possível buscar nos textos de lei indexados: {e}")

    try:
        result = classify_situation(situacao, hits, historico)
    except LLMError as e:
        log_query_event(
            situacao=situacao, hits=hits, result={}, model=MODEL,
            latency_ms=(time.perf_counter() - start) * 1000, error=str(e),
        )
        return _empty_response(str(e), hits)
    except Exception as e:
        log_query_event(
            situacao=situacao, hits=hits, result={}, model=MODEL,
            latency_ms=(time.perf_counter() - start) * 1000, error=f"unexpected: {e}",
        )
        return _empty_response(f"Erro inesperado ao analisar a situação: {e}", hits)

    log_query_event(
        situacao=situacao, hits=hits, result=result, model=MODEL,
        latency_ms=(time.perf_counter() - start) * 1000, usage=result.get("_usage"),
    )

    return QueryResponse(
        infringe=result.get("infringe"),
        confianca=result.get("confianca"),
        violacoes=result.get("violacoes", []),
        analise=result.get("analise", ""),
        pergunta=result.get("pergunta", "") or "",
        recomendacao=result.get("recomendacao", ""),
        artigos_relevantes=[ArticleHit(**h) for h in hits],
    )


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
