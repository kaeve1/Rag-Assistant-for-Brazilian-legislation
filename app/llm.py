"""Calls Gemini with the retrieved law excerpts to classify a situation."""
import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
API_KEY = os.environ.get("GEMINI_KEY") or os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """Você é um assistente jurídico brasileiro. Este sistema \
indexa uma base ampla de legislação federal (proteção de dados, direito \
digital, trabalhista, consumidor, tributário, criança e adolescente, penal, \
processual civil, processual penal e civil, entre outras normas que podem \
ser adicionadas). Você recebe uma situação descrita pelo usuário e trechos \
de lei recuperados por busca semântica nessa base (que podem ou não ser \
relevantes — não se limite a nenhuma área específica do direito: se o \
contexto recuperado for de outra área da legislação indexada, analise-o \
normalmente). Sua tarefa:

1. Analisar se a situação descrita configura infração a algum dispositivo das \
leis fornecidas.
2. Apontar, com precisão, qual(is) lei(s) e artigo(s) específicos são \
potencialmente infringidos, citando o número do artigo.
3. Explicar brevemente o porquê, em linguagem clara.
4. Se a situação NÃO configurar infração aparente, ou não tiver relação com \
nenhuma das leis fornecidas (ex: pergunta genérica, assunto fora do escopo \
jurídico), diga isso explicitamente em vez de forçar uma resposta — nesse \
caso "infringe" deve ser false e "violacoes" uma lista vazia.
4.1. Sempre haverá pontos em aberto, e isso NÃO impede uma resposta. Só \
pergunte quando, sem aquele fato, nenhuma conclusão seria possível (ex: a \
situação não diz o que de fato aconteceu). Nesse caso preencha "pergunta" \
com UMA pergunta objetiva e curta, deixe "infringe" como null e "violacoes" \
vazia. Você tem direito a NO MÁXIMO UMA pergunta em toda a conversa: tendo a \
resposta, conclua com o que tiver, adotando a hipótese mais provável e \
registrando na análise o que permaneceu incerto.
5. Você não é um substituto para aconselhamento jurídico profissional — isso \
deve constar como um aviso breve.

Responda ESTRITAMENTE em JSON válido, sem markdown ao redor, no seguinte formato:
{
  "infringe": true|false,
  "confianca": "alta"|"media"|"baixa",
  "violacoes": [
    {"lei": "LGPD", "artigo": "Art. 7º", "motivo": "..."}
  ],
  "analise": "explicação em 2-4 frases",
  "recomendacao": "o que a parte deveria fazer para se adequar",
  "pergunta": "pergunta objetiva ao usuário, ou string vazia"
}
Se não houver infração ou não houver relação com as leis, "violacoes" deve \
ser uma lista vazia e "recomendacao" pode ser uma string vazia."""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "infringe": {"type": "boolean"},
        "confianca": {"type": "string", "enum": ["alta", "media", "baixa"]},
        "violacoes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "lei": {"type": "string"},
                    "artigo": {"type": "string"},
                    "motivo": {"type": "string"},
                },
                "required": ["lei", "artigo", "motivo"],
            },
        },
        "analise": {"type": "string"},
        "recomendacao": {"type": "string"},
        "pergunta": {"type": "string"},
    },
    "required": ["infringe", "confianca", "violacoes", "analise", "recomendacao"],
}


class LLMError(Exception):
    """Raised when the Gemini request fails or its response can't be used.
    Message is already user-friendly (pt-BR) and safe to show in the UI."""


def _format_context(chunks: list[dict]) -> str:
    if not chunks:
        return "(nenhum trecho de lei relevante foi recuperado)"
    parts = []
    for c in chunks:
        header = f"[{c['law_short']} — {c['article']}]"
        parts.append(f"{header}\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def _fallback_result(analise: str) -> dict:
    return {
        "infringe": None,
        "confianca": None,
        "violacoes": [],
        "analise": analise,
        "recomendacao": "",
        "pergunta": "",
    }


def _extract_json(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return _fallback_result("O modelo não retornou nenhum conteúdo. Tente reformular a situação.")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    candidate = match.group(0) if match else text
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        return _fallback_result(
            "Não foi possível interpretar a resposta do modelo em formato estruturado. "
            "Resposta bruta: " + text[:500]
        )
    # normalize expected keys defensively, in case the model omits one
    data.setdefault("infringe", None)
    data.setdefault("confianca", None)
    data.setdefault("violacoes", [])
    data.setdefault("analise", "")
    data.setdefault("recomendacao", "")
    data.setdefault("pergunta", "")
    if not isinstance(data.get("pergunta"), str):
        data["pergunta"] = ""
    if not isinstance(data.get("violacoes"), list):
        data["violacoes"] = []
    return data


def _format_historico(historico: list[dict] | None) -> str:
    """Prior clarification exchanges, so a follow-up call keeps the context."""
    if not historico:
        return ""
    linhas = []
    for turno in historico:
        pergunta = (turno.get("pergunta") or "").strip()
        resposta = (turno.get("resposta") or "").strip()
        if pergunta and resposta:
            linhas.append(f"Você perguntou: {pergunta}\nUsuário respondeu: {resposta}")
    if not linhas:
        return ""
    return "\n\nEsclarecimentos já obtidos:\n" + "\n\n".join(linhas)


# Sempre haverá pontos em aberto. Depois deste número de esclarecimentos o
# modelo é obrigado a concluir, e qualquer nova pergunta é descartada aqui.
MAX_ESCLARECIMENTOS = 1


def classify_situation(situacao: str, chunks: list[dict], historico: list[dict] | None = None) -> dict:
    situacao = (situacao or "").strip()
    if not situacao:
        return _fallback_result("Nenhuma situação foi informada para análise.")

    if not API_KEY:
        raise LLMError(
            "GEMINI_KEY não está configurada. Defina a variável de ambiente no "
            "arquivo .env com sua chave da API do Gemini."
        )

    context = _format_context(chunks)
    user_msg = (
        f"Situação a analisar:\n\"\"\"\n{situacao}\n\"\"\""
        f"{_format_historico(historico)}\n\n"
        f"Trechos de lei recuperados (contexto, podem incluir itens irrelevantes):\n\n{context}"
    )

    deve_concluir = len(historico or []) >= MAX_ESCLARECIMENTOS
    if deve_concluir:
        user_msg += (
            "\n\nATENÇÃO: você já usou sua pergunta. NÃO faça outra. Deixe "
            '"pergunta" vazia e conclua agora com o que tem, adotando a '
            "hipótese mais provável e dizendo na análise o que ficou em aberto."
        )

    client = genai.Client(api_key=API_KEY)
    generate_config = {
        "system_instruction": SYSTEM_PROMPT,
        "response_mime_type": "application/json",
        "response_schema": RESPONSE_SCHEMA,
        "max_output_tokens": 2048,
    }

    max_attempts = 3
    resp = None
    for attempt in range(1, max_attempts + 1):
        try:
            resp = client.models.generate_content(model=MODEL, contents=user_msg, config=generate_config)
            break
        except genai_errors.ClientError as e:
            status = getattr(e, "status_code", None) or getattr(e, "code", None)
            if status in (401, 403):
                raise LLMError("Chave de API do Gemini inválida ou sem permissão. Verifique o GEMINI_KEY no .env.") from e
            if status == 429:
                raise LLMError("Limite de requisições da API do Gemini atingido. Tente novamente em instantes.") from e
            raise LLMError(f"A API do Gemini rejeitou a requisição ({status or 'erro de cliente'}).") from e
        except genai_errors.ServerError as e:
            # transient (e.g. 503 high demand) — retry with backoff, else surface a friendly error
            if attempt == max_attempts:
                raise LLMError("A API do Gemini está indisponível no momento (alta demanda). Tente novamente em instantes.") from e
            time.sleep(2 ** attempt)
        except genai_errors.APIError as e:
            raise LLMError(f"Erro ao chamar a API do Gemini: {e}") from e
        except Exception as e:  # network errors, timeouts, etc.
            raise LLMError(f"Falha de comunicação com a API do Gemini: {e}") from e

    if getattr(resp, "prompt_feedback", None) and getattr(resp.prompt_feedback, "block_reason", None):
        return _fallback_result(
            "A situação descrita foi bloqueada pelos filtros de segurança do Gemini "
            "e não pôde ser analisada. Tente reformular o texto."
        )

    raw_text = getattr(resp, "text", None)
    if not raw_text:
        return _fallback_result("O modelo não retornou uma resposta utilizável para esta situação.")

    result = _extract_json(raw_text)
    result["_raw"] = raw_text

    # O limite não pode depender de o modelo obedecer ao prompt.
    if deve_concluir and result.get("pergunta"):
        result["pergunta"] = ""

    usage = getattr(resp, "usage_metadata", None)
    if usage is not None:
        result["_usage"] = {
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "output_tokens": getattr(usage, "candidates_token_count", None),
            "total_tokens": getattr(usage, "total_token_count", None),
        }
    return result
