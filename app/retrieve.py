"""Hybrid retrieval: dense embeddings + BM25, fused with Reciprocal Rank
Fusion, then reranked with a cross-encoder — the production-standard RAG
retrieval pipeline (retrieve wide with two complementary signals, fuse, then
rerank down to a small precise set before handing it to the LLM)."""
import json
import re
from pathlib import Path
from functools import lru_cache

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder, SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_DIR = BASE_DIR / "data" / "index"

RERANKER_MODEL = "unicamp-dl/mMiniLM-L6-v2-mmarco-v2"

# candidate pool sizes before fusion/rerank narrows things down — wider than
# a single-domain corpus would need, since at 6k+ articles spanning many
# unrelated legal areas a narrow pool lets the wrong domain crowd out the
# right one before the reranker even sees it
N_DENSE = 60
N_BM25 = 60
N_FUSED = 25
RRF_K = 60  # standard constant from the RRF literature

TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class Retriever:
    def __init__(self):
        self.embeddings = np.load(INDEX_DIR / "embeddings.npy")
        self.metadata = [
            json.loads(l) for l in (INDEX_DIR / "metadata.jsonl").open(encoding="utf-8")
        ]
        model_name = (INDEX_DIR / "model.txt").read_text(encoding="utf-8").strip()
        self.model = SentenceTransformer(model_name)
        # max_length kept safely below the model's absolute position-embedding
        # cap (some LGPD/CLT articles — e.g. the sanctions list — are long
        # enough to overflow it otherwise, which crashes the forward pass)
        self.reranker = CrossEncoder(RERANKER_MODEL, max_length=384)

        self._bm25_corpus_tokens = [_tokenize(m["text"]) for m in self.metadata]
        self.bm25 = BM25Okapi(self._bm25_corpus_tokens)

    def _dense_ranking(self, situacao: str) -> list[int]:
        q_emb = self.model.encode([situacao], normalize_embeddings=True)[0]
        scores = self.embeddings @ q_emb
        return list(np.argsort(-scores)[:N_DENSE])

    def _bm25_ranking(self, situacao: str) -> list[int]:
        scores = self.bm25.get_scores(_tokenize(situacao))
        return list(np.argsort(-scores)[:N_BM25])

    def _fuse(self, dense_idx: list[int], bm25_idx: list[int]) -> list[int]:
        rrf_scores: dict[int, float] = {}
        for rank, idx in enumerate(dense_idx, start=1):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (RRF_K + rank)
        for rank, idx in enumerate(bm25_idx, start=1):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + 1.0 / (RRF_K + rank)
        ranked = sorted(rrf_scores.items(), key=lambda kv: -kv[1])
        return [idx for idx, _ in ranked[:N_FUSED]]

    def query(self, situacao: str, top_k: int = 6):
        dense_idx = self._dense_ranking(situacao)
        bm25_idx = self._bm25_ranking(situacao)
        fused_idx = self._fuse(dense_idx, bm25_idx)

        if not fused_idx:
            return []

        pairs = [(situacao, self.metadata[i]["text"]) for i in fused_idx]
        rerank_scores = self.reranker.predict(pairs)

        order = np.argsort(-rerank_scores)[:top_k]
        results = []
        for pos in order:
            idx = fused_idx[pos]
            item = dict(self.metadata[idx])
            item["score"] = float(rerank_scores[pos])
            results.append(item)
        return results


@lru_cache(maxsize=1)
def get_retriever() -> "Retriever":
    return Retriever()
