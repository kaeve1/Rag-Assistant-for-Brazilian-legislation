"""Parse raw scraped law texts (Planalto markdown) into per-article chunks.

Each law's markdown uses a consistent pattern for Brazilian federal legislation:
  CAPÍTULO ...
  Seção ...
  Art. N[º|.] <text that may span multiple lines/paragraphs, including incisos
  and parágrafos, until the next Art./Capítulo/Seção marker>

Compiled texts (e.g. the CLT) also interleave historical, superseded redações
of the same article as markdown strikethrough (~~...~~) before the current
one, plus "Visualizar Jurisprudência Consolidada" link noise right before
each "Art." marker — both are stripped before parsing. When the same article
number appears more than once (redação history), only the LAST occurrence is
kept, since Planalto lists amendments chronologically ending with the text
currently in force.

Output: data/processed/articles.jsonl, one JSON object per article:
  {"law_id", "law_name", "law_short", "chapter", "section", "article", "text"}
"""
import json
import re
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LAWS = [
    {
        "file": "lgpd.md",
        "law_id": "lgpd",
        "law_name": "Lei nº 13.709/2018 - Lei Geral de Proteção de Dados Pessoais (LGPD)",
        "law_short": "LGPD",
    },
    {
        "file": "marco_civil.md",
        "law_id": "marco_civil",
        "law_name": "Lei nº 12.965/2014 - Marco Civil da Internet",
        "law_short": "Marco Civil da Internet",
    },
    {
        "file": "decreto_iot.md",
        "law_id": "decreto_iot",
        "law_name": "Decreto nº 9.854/2019 - Plano Nacional de Internet das Coisas",
        "law_short": "Decreto IoT",
    },
    {
        "file": "clt.md",
        "law_id": "clt",
        "law_name": "Decreto-Lei nº 5.452/1943 - Consolidação das Leis do Trabalho (CLT)",
        "law_short": "CLT",
    },
    {
        "file": "cdc.md",
        "law_id": "cdc",
        "law_name": "Lei nº 8.078/1990 - Código de Defesa do Consumidor (CDC)",
        "law_short": "CDC",
    },
    {
        "file": "ctn.md",
        "law_id": "ctn",
        "law_name": "Lei nº 5.172/1966 - Código Tributário Nacional (CTN)",
        "law_short": "CTN",
    },
    {
        "file": "eca.md",
        "law_id": "eca",
        "law_name": "Lei nº 8.069/1990 - Estatuto da Criança e do Adolescente (ECA)",
        "law_short": "ECA",
    },
    {
        "file": "codigo_penal.md",
        "law_id": "codigo_penal",
        "law_name": "Decreto-Lei nº 2.848/1940 - Código Penal",
        "law_short": "Código Penal",
    },
    {
        "file": "cpp.md",
        "law_id": "cpp",
        "law_name": "Decreto-Lei nº 3.689/1941 - Código de Processo Penal (CPP)",
        "law_short": "CPP",
    },
    {
        "file": "cpc.md",
        "law_id": "cpc",
        "law_name": "Lei nº 13.105/2015 - Código de Processo Civil (CPC)",
        "law_short": "CPC",
    },
    {
        "file": "codigo_civil.md",
        "law_id": "codigo_civil",
        "law_name": "Lei nº 10.406/2002 - Código Civil",
        "law_short": "Código Civil",
    },
]

CHAPTER_RE = re.compile(r"^CAP[ÍI]TULO\b", re.IGNORECASE)
SECTION_RE = re.compile(r"^Se[çc][ãa]o\b", re.IGNORECASE)
SUBSECTION_RE = re.compile(r"^Subse[çc][ãa]o\b", re.IGNORECASE)
TITLE_RE = re.compile(r"^T[ÍI]TULO\b", re.IGNORECASE)
ARTICLE_RE = re.compile(r"^Art\.\s*(\d{1,3}(?:\.\d{3})*(?:-[A-Z])?)[ºo°]?[.\-–]?\s*(.*)$")
NOISE_RE = re.compile(r"^(Vig[êe]ncia|Este texto n[ãa]o substitui|Mensagem de veto|Texto compilado)", re.IGNORECASE)

STRIKE_RE = re.compile(r"~~.*?~~", re.DOTALL)
JURIS_LINK_RE = re.compile(r"\[Visualizar Jurisprud[êe]ncia Consolidada[^\]]*\]\([^)]*\)")
# some scrapes render "Art." and its number on separate lines (e.g. CTN's
# "Art.\n1º ..."), which would otherwise hide the article entirely since
# neither resulting line matches ARTICLE_RE on its own
ART_SPLIT_RE = re.compile(r"Art\.\s+(?=\d)")
# markdown-escapes a period after a digit as "\." (to stop it looking like a
# numbered-list marker) — e.g. "75\." for "75." — which otherwise survives
# into the article body as a stray leading "\."
MD_DIGIT_ESCAPE_RE = re.compile(r"(?<=\d)\\\.")


def parse_law(path: Path, law_id: str, law_name: str, law_short: str):
    raw_text = path.read_text(encoding="utf-8")
    raw_text = MD_DIGIT_ESCAPE_RE.sub(".", raw_text)
    raw_text = ART_SPLIT_RE.sub("Art. ", raw_text)
    raw_text = STRIKE_RE.sub("", raw_text)
    raw_text = JURIS_LINK_RE.sub("", raw_text)
    lines = raw_text.splitlines()

    articles: dict[str, dict] = {}
    order: list[str] = []
    chapter = None
    section = None
    current = None  # dict being accumulated

    def flush():
        if current is None:
            return
        text = "\n".join(current["lines"]).strip()
        text = re.sub(r"\n{3,}", "\n\n", text)
        # a lone ordinal indicator (º/o/°) sometimes lands on its own line,
        # split away from both "Art. N" and the article body by the scrape
        text = re.sub(r"^[ºo°]\s+", "", text)
        if not text or re.fullmatch(r"\(vetado\)\.?", text, re.IGNORECASE):
            return
        key = current["article"]
        if key not in articles:
            order.append(key)
        articles[key] = {
            "law_id": law_id,
            "law_name": law_name,
            "law_short": law_short,
            "chapter": current["chapter"],
            "section": current["section"],
            "article": current["article"],
            "text": text,
        }

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line == "\\*" or NOISE_RE.match(line):
            continue

        if TITLE_RE.match(line):
            chapter = None
            section = None
            continue
        if CHAPTER_RE.match(line):
            chapter = line
            section = None
            continue
        if SECTION_RE.match(line) or SUBSECTION_RE.match(line):
            section = line
            continue

        m = ARTICLE_RE.match(line)
        if m:
            flush()
            art_num, rest = m.group(1), m.group(2).strip()
            rest = re.sub(r"^[-–]\s*", "", rest)
            current = {
                "chapter": chapter,
                "section": section,
                "article": f"Art. {art_num}",
                "lines": [rest] if rest else [],
            }
            continue

        if current is not None:
            current["lines"].append(line)
        # lines before the first "Art." (preamble) are ignored

    flush()
    return [articles[k] for k in order]


def main():
    all_articles = []
    for law in LAWS:
        path = RAW_DIR / law["file"]
        if not path.exists():
            print(f"(pulando {law['law_short']}: {law['file']} não encontrado)")
            continue
        arts = parse_law(path, law["law_id"], law["law_name"], law["law_short"])
        print(f"{law['law_short']}: {len(arts)} artigos extraídos de {law['file']}")
        all_articles.extend(arts)

    out_path = OUT_DIR / "articles.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for art in all_articles:
            f.write(json.dumps(art, ensure_ascii=False) + "\n")

    print(f"\nTotal: {len(all_articles)} artigos salvos em {out_path}")


if __name__ == "__main__":
    main()
