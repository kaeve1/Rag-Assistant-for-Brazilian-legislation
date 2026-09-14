# Plano: Redesign do Frontend

> Este é um **plano**, não uma implementação. Escrito para ser executado
> depois (por mim mesmo em outra sessão, ou por você). Não mexe em nenhum
> arquivo do projeto além deste `.md`.

## Objetivo

Trocar `static/index.html` (formulário simples atual) por uma landing page
única com cara de produto de IA real: hero com input de chat, barra lateral
de histórico, e seções explicativas abaixo da dobra sobre o que é o
projeto, como funciona, e por que essa técnica (RAG) importa no mercado
hoje — pensado como peça de portfólio de quem está estudando RAG/IA.

## Referências de design (visitei as duas para tirar isso)

### Cerebrium.ai (cerebrium.ai) — a "pele"
- Fundo quase preto, navy bem escuro (não é preto puro).
- Acento em rosa/magenta vibrante (`#FF2E74`-ish) combinado com violeta
  (`#8B5CF6`-ish), às vezes como gradiente no texto do headline.
- Tipografia: fonte monoespaçada para nav, botões e labels pequenos, tudo
  em CAIXA ALTA com letter-spacing (ex: `TRY IT NOW`, `PRICING`) — dá o ar
  técnico/infra. Headlines em fonte grande, humanista, não-mono, às vezes
  com fill em gradiente.
- Texturas: grid de pontinhos sutil no fundo escuro; formas 3D tipo "fita"
  em gradiente magenta/roxo como elemento decorativo atrás de cards.
- Botões: pill (bordas bem arredondadas), CTA primário com fill sólido
  magenta, secundário outline/ghost.
- Cards de comparação/benchmark: painel escuro com gradiente, barras
  horizontais de progresso, números grandes à direita.
- Uma seção com lista de features empilhada onde o item "ativo" fica
  escuro/negrito e os outros ficam cinza-claro fantasma (sugere destaque ao
  rolar a página).
- Muito espaço em branco, composição assimétrica, confiança visual.

### Gemini (o app da Google) — a "forma de interação"
- Input central tipo pill, com botão de enviar embutido — exatamente o
  padrão que você pediu ("igual as IAs atuais").
- Barra lateral esquerda colapsável com o histórico de conversas.
- Cantos bem arredondados em geral, chrome mínimo ao redor das mensagens.
- Ícone/marca com gradiente colorido (o "spark" do Gemini).

### Mistura proposta
Pele visual = Cerebrium (fundo escuro, monoespaçada nos detalhes, gradiente
rosa/violeta, grid de pontos, cards com sombra/gradiente). Esqueleto de
interação = Gemini (input pill + sidebar de histórico + área de chat
limpa). Não misturar fundo claro/escuro no meio da página — mantém um tema
escuro único do topo ao rodapé, inclusive nas seções explicativas (usa
cards claros *dentro* do fundo escuro para variar contraste, como o
Cerebrium faz nos painéis).

## Tokens de design propostos (ponto de partida — refinar com a skill `ui-ux-pro-max` na hora de implementar)

```css
--bg-void: #0A0B12;        /* fundo geral */
--bg-surface: #14151F;     /* cards, sidebar, painel do input */
--bg-surface-2: #1C1E2B;   /* hover/elevação */
--border-subtle: #262838;

--accent-primary: #FF2E74;   /* magenta — CTA principal, links ativos */
--accent-secondary: #8B5CF6; /* violeta — gradientes, glows */
--accent-gemini: #4285F4;    /* azul — usar com parcimônia, nod ao Gemini
                                 (ex: glow do botão de enviar, ícone) */

--text-primary: #F5F5F7;
--text-muted: #9AA0B4;
--text-faint: #565B72;

--font-display: "General Sans", "Inter", sans-serif;  /* headlines grandes */
--font-body: "Inter", sans-serif;                       /* corpo de texto */
--font-mono: "JetBrains Mono", "IBM Plex Mono", monospace; /* labels, nav, badges */
```

Validar/ajustar esses hex e o pareamento de fontes com a base de dados da
skill `ui-ux-pro-max` (tem 192 paletas e 74 pareamentos de fonte
pesquisáveis) antes de fixar — os valores acima são um ponto de partida
razoável, não a palavra final.

## Estrutura da página

```
┌─────────────────────────────────────────────────────────┐
│ [logo] Nome do projeto                    [GitHub] [link]│  <- nav fixo, fundo escuro translúcido
├──────────┬──────────────────────────────────────────────┤
│          │                                               │
│ SIDEBAR  │   HERO (1ª dobra, altura de tela cheia)       │
│          │                                               │
│ + Nova   │   Headline grande: algo como                  │
│   consulta│  "Descreva a situação. Eu digo qual lei      │
│          │   isso infringe."                             │
│ [lista   │   Subheadline: 1 linha explicando (RAG sobre  │
│  do       │   11 códigos federais, X mil artigos)         │
│  histórico│                                               │
│  clicável]│  ┌───────────────────────────────────┐        │
│          │  │ [textarea placeholder...]      [➤]  │  <- input pill, igual ChatGPT/Gemini
│          │  └───────────────────────────────────┘        │
│          │   chips de exemplo clicáveis (3-4 situações)  │
│          │                                               │
│          │   [resultado da análise aparece aqui, quando  │
│          │    houver — reaproveita o layout já existente │
│          │    de veredito/violações/fontes, restilizado] │
├──────────┴──────────────────────────────────────────────┤
│  (scroll ↓)                                              │
│  SEÇÃO 1 — O que é este projeto                          │
│  SEÇÃO 2 — Como funciona (pipeline de retrieval, visual) │
│  SEÇÃO 3 — Por que isso importa (mercado / narrativa     │
│            pessoal de quem está estudando RAG/IA)         │
│  SEÇÃO 4 — Stack tecnológico (badges/lista)               │
│  FOOTER — link do repo, contato                           │
└───────────────────────────────────────────────────────────┘
```

No mobile: sidebar vira um drawer off-canvas (ícone de hambúrguer no nav),
hero empilha em coluna única, chips de exemplo quebram em 2 linhas.

## Conteúdo sugerido para as seções de scroll

### Seção 1 — O que é
Curto, 2-3 frases. Ex: *"Este é um sistema de RAG (Retrieval-Augmented
Generation) que busca nos textos oficiais de 11 códigos da legislação
federal brasileira — mais de 6 mil artigos — antes de responder. A
resposta vem sempre ancorada no artigo de lei real, não em memória do
modelo."*

### Seção 2 — Como funciona
Visualizar o pipeline (busca densa + BM25 → fusão RRF → reranking →
Gemini) como uma sequência de 3-4 cards/steps, no estilo do painel de
benchmark do Cerebrium (números, barras, comparação "antes/depois" de
usar reranking, por exemplo). Reaproveitar o diagrama de
`ARQUITETURA.md` como base do texto.

### Seção 3 — Por que isso importa
Esta é a seção mais pessoal — enquadrar como nota de portfólio: *"Construí
isso estudando RAG na prática: chunking de documentos legais reais (com
todas as particularidades de scraping que isso implica), retrieval híbrido,
reranking, avaliação com métricas estilo RAGAS, tratamento de erro de API
em produção. RAG é hoje a técnica mais pedida em vagas de AI/LLM Engineer
porque é como se resolve o problema real: respostas ancoradas numa base de
conhecimento própria, não alucinadas."* Ajustar o tom para a voz do usuário
antes de publicar.

### Seção 4 — Stack tecnológico
Lista/badges (like a logo strip, mas com nomes de tecnologia em vez de
logos de clientes): FastAPI · Gemini · sentence-transformers · BM25 ·
cross-encoder rerank · Docker · RAGAS-style eval.

## Decisões técnicas

### Histórico na sidebar: localStorage (não backend)
Sem sistema de login/sessão hoje, então o histórico fica **client-side**,
em `localStorage`, por navegador/dispositivo. Cada entrada guarda a
pergunta **e a resposta completa** (não só a pergunta), para que clicar num
item antigo re-renderize na hora, sem gastar uma nova chamada ao Gemini
(importante dado o limite de cota gratuita que já vimos). Estrutura
sugerida:

```js
// localStorage key: "rag_history"
[
  { id, ts, situacao, response: { infringe, violacoes, analise, ... } }
]
```

Ações da sidebar: nova consulta, selecionar item antigo, apagar item,
limpar tudo. Se no futuro quiser histórico entre dispositivos, isso vira um
endpoint novo (`GET/POST /api/history`) com algum id de sessão anônima em
cookie — fora do escopo deste plano, mas deixo anotado como próximo passo
natural.

### Stack do frontend: continuar vanilla (sem build step)
O projeto é uma API Python simples servindo um HTML estático — não vale a
pena introduzir um toolchain Node/Vite/React só para isso. Plano é dividir
o atual `static/index.html` monolítico em:

```
static/
  index.html      (estrutura/semântica)
  css/styles.css  (tokens + layout + componentes)
  js/app.js       (fetch da API, estado do histórico, render)
  js/sidebar.js   (localStorage, lista, seleção)
```

Sem framework, sem bundler — `server.py` já serve `/static` como está.

### Sem mudança no backend
`app/server.py` e `app/llm.py` não precisam mudar para este plano
(histórico é client-side). Se decidir migrar para histórico
server-side depois, aí sim mexe no backend.

## Acessibilidade e responsividade (não é opcional)

- Contraste mínimo AA nos textos sobre o fundo escuro (checar com a paleta
  final).
- Foco visível em todos os elementos interativos (input, botão enviar,
  itens da sidebar, chips de exemplo).
- Sidebar navegável por teclado; no mobile, drawer com `aria-expanded` no
  botão de hambúrguer.
- `prefers-reduced-motion`: desativar/reduzir animações de scroll-reveal
  para quem pedir isso no SO.
- Testar em largura de ~400px (celular) — sidebar em drawer, hero em
  coluna única, cards de resultado sem overflow horizontal.

## Ordem de execução (para quando for implementar)

1. **Confirmar que os plugins estão ativos** — `ui-ux-pro-max` e
   `impeccable` foram instalados nesta sessão mas só carregam numa sessão
   nova do Claude Code. Reinicie a sessão antes de começar.
2. Invocar a skill `impeccable` no `static/index.html` atual como ponto de
   partida — mesmo sendo um redesign do zero, ela ajuda a não repetir
   anti-padrões de hierarquia/contraste/densidade.
3. Usar `ui-ux-pro-max` para validar/ajustar a paleta e o pareamento de
   fontes propostos acima antes de codar (buscar por algo como "dark
   technical gradient pink violet" e "monospace + humanist sans pairing"
   na base pesquisável da skill).
4. Implementar nesta ordem:
   a. Scaffold: tokens CSS + layout de 2 colunas (sidebar + main) + nav.
   b. Hero: headline, input pill, botão enviar, chips de exemplo — ligar
      no `POST /api/query` já existente.
   c. Renderização do resultado (reaproveitar a lógica atual de
      veredito/violações/fontes de `static/index.html`, só restilizar).
   d. Sidebar: localStorage (salvar, listar, selecionar, apagar).
   e. Seções de scroll (conteúdo acima) com scroll-reveal sutil.
   f. Passo de responsividade (mobile: drawer, coluna única).
   g. Passo de acessibilidade (foco, contraste, `prefers-reduced-motion`).
5. Testar manualmente: pergunta nova → aparece na sidebar → clicar num item
   antigo re-renderiza sem nova chamada de API → limpar histórico funciona
   → mobile não quebra.
6. Opcional: atualizar `README.md` com um screenshot da nova UI.

## Fora de escopo deste plano

- Autenticação/contas de usuário.
- Histórico persistente entre dispositivos (precisaria de backend + sessão).
- Migração para um framework frontend (React/Vue/etc.) — vanilla é
  suficiente pro tamanho do projeto.
- Alterações no pipeline de retrieval/LLM — este plano é só de UI.
