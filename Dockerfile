FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY static ./static
COPY data/raw ./data/raw

# Build the article store and the vector/BM25 index at image build time, so
# containers start instantly and don't need internet access to fetch the
# embedding/reranker models at runtime (they're cached into the image here).
RUN python -m app.parse_laws && python -m app.ingest
RUN python -c "from app.retrieve import get_retriever; get_retriever()"

EXPOSE 8000

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
