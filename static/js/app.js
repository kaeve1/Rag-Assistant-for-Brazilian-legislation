function escapeHtml(s) {
  const d = document.createElement('div');
  d.textContent = s ?? '';
  return d.innerHTML;
}

const ICON_ALERT = '<svg class="answer__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4M12 17h.01M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>';
const ICON_CHECK = '<svg class="answer__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 12 5.5 5.5L20 7"/></svg>';
const ICON_PARTIAL = '<svg class="answer__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5"/><path d="M12 16.5h.01"/></svg>';
const ICON_CHEVRON = '<svg class="sources__chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>';

// Este sistema nao consegue afirmar ausencia de infracao: ele so sabe o que
// a busca trouxe. Um "infringe: false" costuma significar "nao recuperei o
// dispositivo aplicavel", e a confianca alta ai e confianca na propria frase
// do modelo, nao em inocencia. Por isso nao existe estado verde de veredito.
function verdictOf(data) {
  const violacoes = Array.isArray(data.violacoes) ? data.violacoes : [];
  // O modelo as vezes marca false e ainda lista dispositivos. Nesse
  // conflito vale o que ele citou, nao o booleano.
  if (data.infringe === true || violacoes.length > 0) {
    return { cls: 'infringe', icon: ICON_ALERT, title: 'Possível infração na situação descrita' };
  }
  if (data.infringe === false) {
    return { cls: 'partial', icon: ICON_PARTIAL, title: 'Nenhum dispositivo aplicável foi encontrado' };
  }
  return { cls: 'partial', icon: ICON_PARTIAL, title: 'Não foi possível analisar a situação' };
}

// Para uma infracao encontrada, a confianca qualifica a leitura dos artigos.
const CONFIDENCE_NOTE = {
  alta: 'Confiança alta nos artigos recuperados.',
  media: 'Confiança média. Confira os trechos citados.',
  baixa: 'Confiança baixa: os artigos sustentam mal essa leitura.',
};

// Quando nada foi encontrado, o que o leitor precisa saber nao e a
// confianca, e que ausencia de resultado nao e atestado de legalidade.
const NOT_FOUND_NOTE =
  'Não é atestado de legalidade: a busca pode ter falhado. Confira os trechos consultados.';

function renderClarify(data) {
  return `<div class="answer">
    <div class="clarify">
      <p class="clarify__label">Falta um dado</p>
      <p class="clarify__q">${escapeHtml(data.pergunta)}</p>
    </div>
  </div>`;
}

function renderAnswer(data) {
  if (data && data.pergunta) return renderClarify(data);
  const v = verdictOf(data);
  const note = v.cls === 'infringe'
    ? CONFIDENCE_NOTE[(data.confianca || '').toLowerCase()]
    : NOT_FOUND_NOTE;

  let html = '<div class="answer">';

  html += `<div class="verdict verdict--${v.cls}">
    <p class="verdict__title">${v.icon}${v.title}</p>
    ${note ? `<p class="verdict__note">${escapeHtml(note)}</p>` : ''}
  </div>`;

  if (data.analise) html += `<p>${escapeHtml(data.analise)}</p>`;

  if (data.violacoes && data.violacoes.length) {
    html += '<p class="answer__heading">Dispositivos infringidos</p><div class="answer__laws">';
    for (const v of data.violacoes) {
      html += `<div class="answer__law">
        <div class="answer__lawname"><span class="answer__lawref">${escapeHtml(v.artigo || '')}</span>${escapeHtml(v.lei || '')}</div>
        <div class="answer__lawwhy">${escapeHtml(v.motivo || '')}</div>
      </div>`;
    }
    html += '</div>';
  }

  if (data.recomendacao) {
    html += `<p class="answer__heading">Recomendação</p><p>${escapeHtml(data.recomendacao)}</p>`;
  }

  if (data.artigos_relevantes && data.artigos_relevantes.length) {
    html += `<details class="sources"><summary>${ICON_CHEVRON}Trechos de lei consultados (${data.artigos_relevantes.length})</summary>`;
    for (const h of data.artigos_relevantes) {
      html += `<div class="hit">
        <div class="meta"><span>${escapeHtml(h.law_short)}, ${escapeHtml(h.article)}</span><span>score ${h.score.toFixed(3)}</span></div>
        <div class="snippet">${escapeHtml(h.text.slice(0, 400))}${h.text.length > 400 ? '…' : ''}</div>
      </div>`;
    }
    html += '</details>';
  }

  html += '</div>';
  return html;
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('btnSend');
  const textarea = document.getElementById('situacao');
  const chat = document.querySelector('.chat');
  const turnsEl = document.getElementById('turns');

  // Enquanto o modelo estiver pedindo esclarecimento, a proxima mensagem
  // do usuario e a resposta daquela pergunta, nao uma consulta nova.
  let pendente = null; // { situacao, historico: [{pergunta, resposta}], pergunta }

  function clearThread() {
    turnsEl.innerHTML = '';
    chat.classList.remove('has-thread');
    pendente = null;
  }

  function addTurn(situacao) {
    chat.classList.add('has-thread');
    const turn = document.createElement('article');
    turn.className = 'turn';

    const q = document.createElement('div');
    q.className = 'msg-user';
    q.textContent = situacao;

    const a = document.createElement('div');
    a.className = 'answer';
    a.innerHTML = '<p class="answer__loading">Buscando nos 6.034 artigos e analisando a situação…</p>';

    turn.appendChild(q);
    turn.appendChild(a);
    turnsEl.appendChild(turn);
    q.scrollIntoView({ behavior: 'smooth', block: 'start' });
    return a;
  }

  const history = new HistoryRail({
    onSelect(item) {
      clearThread();
      const slot = addTurn(item.situacao);
      slot.outerHTML = renderAnswer(item.response);
    },
    onNew() {
      showView(null);
      clearThread();
      textarea.value = '';
      textarea.style.height = 'auto';
      textarea.focus();
    },
  });

  async function submit(texto) {
    if (!texto || btn.disabled) return;

    // Continuacao de um esclarecimento, ou consulta nova
    let situacao = texto;
    let historico = [];
    if (pendente) {
      situacao = pendente.situacao;
      historico = pendente.historico.concat([{ pergunta: pendente.pergunta, resposta: texto }]);
    }

    btn.disabled = true;
    btn.classList.add('is-loading');
    const slot = addTurn(texto);
    textarea.value = '';
    textarea.style.height = 'auto';

    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ situacao, historico }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Erro HTTP ${res.status}`);
      }
      const data = await res.json();
      slot.outerHTML = renderAnswer(data);

      if (data.pergunta) {
        pendente = { situacao, historico, pergunta: data.pergunta };
        textarea.placeholder = 'Responda a pergunta acima…';
      } else {
        pendente = null;
        textarea.placeholder = 'Descreva o que aconteceu…';
        const entry = History.add(situacao, data, history.currentProject());
        history.setActive(entry.id);
      }
      textarea.focus();
    } catch (e) {
      slot.innerHTML = `<p class="answer__error">Erro: ${escapeHtml(e.message)}</p>`;
    } finally {
      btn.disabled = false;
      btn.classList.remove('is-loading');
    }
  }

  function askWith(text) {
    showView(null);
    submit(text);
  }

  btn.addEventListener('click', () => submit(textarea.value.trim()));
  textarea.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit(textarea.value.trim());
    }
  });
  textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px';
  });

  document.querySelectorAll('.chip').forEach((chip) => {
    chip.addEventListener('click', () => { pendente = null; submit(chip.dataset.text); });
  });

  document.querySelectorAll('.area__try').forEach((el) => {
    el.addEventListener('click', () => { pendente = null; askWith(el.dataset.text); });
  });

  // Views: o chat e as paginas de conteudo ocupam o mesmo espaco.
  const chatEl = document.querySelector('.chat');
  const views = [...document.querySelectorAll('.view')];
  const navItems = [...document.querySelectorAll('.rail__navitem')];

  function showView(id) {
    chatEl.hidden = Boolean(id);
    views.forEach((v) => { v.hidden = v.id !== id; });
    navItems.forEach((n) => n.classList.toggle('is-current', n.dataset.view === id));
    window.scrollTo(0, 0);
  }

  navItems.forEach((n) => n.addEventListener('click', () => {
    showView(n.dataset.view);
    history.closeOverlay();
  }));
  document.querySelectorAll('[data-back]').forEach((b) =>
    b.addEventListener('click', () => showView(null)));

  // Áreas: a ativa é a que cruza a faixa central da tela. Comparar
  // intersectionRatio faria um painel curto vencer um painel alto.
  const areas = [...document.querySelectorAll('.area')];
  const railItems = [...document.querySelectorAll('.areas__railitem')];

  function setActiveArea(id) {
    areas.forEach((a) => a.classList.toggle('is-active', a.id === id));
    railItems.forEach((r) => {
      const on = r.dataset.target === id;
      r.classList.toggle('is-active', on);
      if (on) r.setAttribute('aria-current', 'true');
      else r.removeAttribute('aria-current');
    });
  }

  railItems.forEach((item) => {
    item.addEventListener('click', () => {
      setActiveArea(item.dataset.target);
      document.getElementById(item.dataset.target).scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  if ('IntersectionObserver' in window && areas.length) {
    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) setActiveArea(entry.target.id);
        }
      },
      { rootMargin: '-28% 0px -58% 0px', threshold: 0 }
    );
    areas.forEach((a) => io.observe(a));

    // Se a pagina acabar antes de o ultimo painel cruzar a faixa,
    // o fim do scroll decide por ele.
    window.addEventListener('scroll', () => {
      const view = document.getElementById('view-cobertura');
      if (!view || view.hidden) return;
      const fim = window.innerHeight + window.scrollY >= document.body.scrollHeight - 4;
      if (fim) setActiveArea(areas[areas.length - 1].id);
    }, { passive: true });
  } else {
    areas.forEach((a) => a.classList.add('is-active'));
  }
});
