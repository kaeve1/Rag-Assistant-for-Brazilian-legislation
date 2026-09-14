"""Build the local vector index from data/processed/articles.jsonl.

Uses a multilingual sentence-transformer (good Portuguese support) to embed
each article chunk, and stores the vectors + metadata as .npz/.jsonl so the
server can do cosine-similarity retrieval without an external vector DB.
"""
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
ARTICLES_PATH = BASE_DIR / "data" / "processed" / "articles.jsonl"
INDEX_DIR = BASE_DIR / "data" / "index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "paraphrase-multilingual-mpnet-base-v2"


def build_chunk_text(article: dict) -> str:
    """Text that gets embedded: law + hierarchy + article body, so the
    embedding captures both the legal source and the content."""
    parts = [article["law_short"]]
    if article.get("chapter"):
        parts.append(article["chapter"])
    if article.get("section"):
        parts.append(article["section"])
    parts.append(article["article"])
    parts.append(article["text"])
    return " - ".join(p for p in parts[:-1] if p) + "\n" + article["text"]


def main():
    articles = [json.loads(l) for l in ARTICLES_PATH.open(encoding="utf-8")]
    print(f"Carregados {len(articles)} artigos. Gerando embeddings com {MODEL_NAME}...")

    model = SentenceTransformer(MODEL_NAME)
    texts = [build_chunk_text(a) for a in articles]
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    np.save(INDEX_DIR / "embeddings.npy", embeddings.astype(np.float32))
    with (INDEX_DIR / "metadata.jsonl").open("w", encoding="utf-8") as f:
        for a in articles:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    (INDEX_DIR / "model.txt").write_text(MODEL_NAME, encoding="utf-8")

    print(f"Índice salvo em {INDEX_DIR} ({embeddings.shape[0]} vetores, dim={embeddings.shape[1]}).")


if __name__ == "__main__":
    main()
