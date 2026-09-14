# Arquitetura do Projeto

Este documento explica o que este repositório faz, por que ele existe, e o
papel de cada arquivo/pasta. Serve como referência para quem chega no
projeto pela primeira vez (inclusive você, daqui a alguns meses).

## O que é

Um sistema de **RAG (Retrieval-Augmented Generation)** que recebe a
descrição de uma situação em português e responde qual(is) dispositivo(s)
da legislação federal brasileira ela pode infringir — citando lei e artigo
específicos, com justificativa e recomendação.

Não é um parecer jurídico. É uma ferramenta de **triagem**: aponta por onde
começar a investigar, com base em busca semântica sobre o texto real das
leis (não em "achismo" do modelo).

## Que problema isso resolve

LLMs "sabem" direito brasileiro de forma genérica, mas:
- Alucinam número de artigo com frequência.
- Não têm como te dizer *de onde* tiraram a resposta.
- Misturam redações antigas/revogadas com a lei em vigor.

RAG resolve isso invertendo o fluxo: em vez de perguntar "o que você sabe
sobre X" para o modelo, primeiro **buscamos os artigos de lei realmente
relevantes** num índice construído a partir do texto oficial (Planalto), e
só then pedimos para o modelo analisar a situação **usando esse texto como
contexto**. A resposta fica ancorada em uma fonte verificável.

## Por que isso importa (mercado)

RAG é hoje a técnica mais usada em produção para aplicações de LLM que
precisam de respostas factualmente corretas sobre uma base de conhecimento
própria (jurídico, suporte, documentação interna, saúde). Empresas que
contratam para vagas de "AI Engineer" / "LLM Engineer" esperam que o
candidato saiba, na prática:

- desenhar um pipeline de ingestão e chunking de documentos;
- escolher e comparar estratégias de retrieval (denso, léxico, híbrido);
- avaliar qualidade de retrieval e de geração com métricas (não só "parece
  bom");
- lidar com os problemas reais de produção: erros de API, rate limits,
  observability, custo.

Este projeto foi construído deliberadamente para cobrir essas peças de
ponta a ponta, em vez de só chamar `model.generate()` em cima de um PDF.

## Arquitetura (visão geral)

```
Texto oficial (Planalto)
        │
        ▼
 parse_laws.py  ──► data/processed/articles.jsonl  (um JSON por artigo)
        │
        ▼
   ingest.py    ──► data/index/  (embeddings + metadados)
        │
        ▼
┌───────────────────── retrieve.py ─────────────────────┐
│  busca densa (embeddings)  +  busca léxica (BM25)      │
│              │                        │                │
│              └────────► RRF fusão ◄───┘                │
│                            │                            │
│                     cross-encoder rerank                │
└──────────────────────────┬───────────────────────────-─┘
                            ▼
                        llm.py  ──► Gemini (com contexto recuperado)
                            │
                            ▼
                       server.py (FastAPI)
                            │
                            ▼
                    static/index.html (UI)
```

Cada consulta do usuário passa pelas 3 primeiras etapas (retrieval) antes de
qualquer chamada ao Gemini — o modelo nunca responde "no vácuo".

## Tour pelo repositório

### `data/`
- **`data/raw/*.md`** — texto bruto de cada lei, raspado diretamente do
  Planalto (fonte oficial) via Firecrawl. Um arquivo por lei/código.
- **`data/processed/articles.jsonl`** — saída do parser: um JSON por
  artigo, já limpo (sem redações históricas revogadas, sem ruído de
  markdown), com metadados (`law_id`, `law_name`, `law_short`, `chapter`,
  `section`, `article`, `text`).
- **`data/index/`** — gerado por `ingest.py`, não versionado no git
  (`.gitignore`): embeddings (`.npy`), metadados (`.jsonl`) e o nome do
  modelo usado. É o índice vetorial que o servidor carrega em memória.

### `app/parse_laws.py`
Converte os textos brutos em artigos estruturados. É a parte mais
"artesanal" do projeto — cada lei tem suas próprias particularidades de
formatação vindas do scraping, e o parser evoluiu para lidar com elas:
redações revogadas em *strikethrough* markdown, "Art." e o número em linhas
separadas, o indicador ordinal "º" virando letra "o" solta, números de
milhar com ponto separador ("Art. 1.641"), pontos escapados em markdown, e
artigos "(VETADO)" sem conteúdo. Cada um desses foi um bug real, encontrado
comparando a contagem de artigos extraídos com a contagem oficial da lei.

### `app/ingest.py`
Gera os embeddings de cada artigo usando um modelo multilingue local
(`paraphrase-multilingual-mpnet-base-v2`, via `sentence-transformers` —
roda na sua máquina, sem custo de API) e salva o índice em `data/index/`.
Roda uma vez após qualquer mudança no corpus.

### `app/retrieve.py`
O núcleo do retrieval. Implementa o padrão usado em RAG de produção, em 3
estágios:
1. **Busca densa** (similaridade de cosseno sobre os embeddings) — boa para
   sinônimos e paráfrase ("demitido" ≈ "dispensado").
2. **Busca léxica (BM25)** — boa para termos exatos que aparecem
   literalmente na lei (nomes de institutos jurídicos, números).
3. **Fusão por Reciprocal Rank Fusion (RRF)** dos dois rankings, seguida de
   **reranking** com um cross-encoder treinado em português
   (`unicamp-dl/mMiniLM-L6-v2-mmarco-v2`), que reordena os candidatos
   olhando a situação e cada artigo *juntos* (mais caro computacionalmente,
   mas muito mais preciso que similaridade pura).

### `app/llm.py`
Envia a situação + os artigos recuperados para o **Gemini** (Google), com
um prompt que pede uma resposta em JSON estruturado (infringe? qual
lei/artigo? por quê? o que fazer?). Trata os erros que uma API de LLM
realmente produz em uso real: chave inválida, limite de requisições (429),
indisponibilidade temporária (503, com retry automático), resposta
bloqueada por filtro de segurança, JSON malformado — nada disso deveria
derrubar a aplicação.

### `app/logging_config.py`
Logging estruturado (JSON-lines) de cada consulta: o que foi perguntado,
quais artigos foram recuperados e com que score, latência, tokens
consumidos, veredito. Vai para `logs/app.jsonl` (não versionado) e stdout.
É a base para plugar uma ferramenta de observability (Langfuse, LangSmith)
depois, sem reinstrumentar nada.

### `app/server.py`
API **FastAPI**. Um único endpoint principal, `POST /api/query`, que
orquestra retrieval → geração → logging, e serve a página estática em `/`.
Desenhado para nunca devolver um erro cru: situação vazia, falha de
retrieval, falha de LLM — tudo vira uma resposta `200` com uma mensagem
explicativa, para o frontend sempre ter algo sensato para mostrar.

### `static/index.html`
Interface web atual — uma página HTML/CSS/JS simples (sem framework), sem
build step. Está sendo redesenhada (ver `PLANO_FRONTEND.md`).

### `eval/`
- **`golden_set.jsonl`** — situações rotuladas manualmente com a
  lei/artigo esperado, cobrindo as leis originais (LGPD, Marco Civil, CLT).
- **`run_eval.py`** — roda o pipeline completo contra o golden set e
  calcula métricas no estilo RAGAS (context_precision, context_recall,
  mrr, faithfulness, article_f1, infringe_accuracy) — reimplementadas sem
  depender do pacote `ragas` (ver comentário no arquivo: `scikit-network`
  não compila neste ambiente). Ainda não foi expandido para os códigos
  adicionados depois (CDC, Código Civil, etc.).

### `Dockerfile` / `.dockerignore`
Container pronto para produção: builda a imagem já com o índice de
embeddings gerado e os modelos baixados (parser + ingest rodam no build),
então o container sobe instantâneo, sem depender de internet em runtime
(exceto para chamar a API do Gemini).

### `requirements.txt`, `.env` / `.env.example`
Dependências Python e configuração (chave da API do Gemini). `.env` nunca é
commitado (está no `.gitignore`); `.env.example` documenta as variáveis
esperadas.

## Tecnologias usadas e por quê

| Camada | Tecnologia | Por quê |
|---|---|---|
| Backend/API | **FastAPI** + **uvicorn** | Async, tipagem via Pydantic, docs automáticas, padrão de facto para APIs Python hoje |
| Embeddings | **sentence-transformers** (local) | Sem custo de API, modelo multilingue já validado para português |
| Busca léxica | **rank-bm25** | Complementa embeddings — captura correspondência exata de termos jurídicos |
| Reranking | **cross-encoder** (HuggingFace) | Maior ganho de precisão por custo computacional no pipeline de RAG |
| LLM | **Google Gemini** (`google-genai`) | Modelo de análise/geração da resposta final |
| Config | **python-dotenv** | Chave de API fora do código, fora do git |
| Avaliação | Métricas estilo **RAGAS** (implementação própria) | `ragas` não instala neste ambiente (Python 3.14 + Windows, sem MSVC) |
| Deploy | **Docker** | Empacotamento reprodutível, padrão de mercado |

## Como rodar

Ver `README.md` — setup, variáveis de ambiente, comandos de ingestão e de
subida do servidor.

## Limitações conhecidas

Ver a seção "Limitações" do `README.md` para o detalhamento honesto (não só
o que funciona, mas onde o retrieval ainda erra e por quê).
