const HISTORY_KEY = 'rag_history';
const PROJECTS_KEY = 'rag_projects';

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveHistory(items) {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(items));
  } catch {
    /* localStorage unavailable (private mode, quota): history just won't persist */
  }
}

function loadProjects() {
  try {
    const raw = localStorage.getItem(PROJECTS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveProjects(items) {
  try {
    localStorage.setItem(PROJECTS_KEY, JSON.stringify(items));
  } catch {
    /* sem localStorage os projetos nao persistem */
  }
}

const Projects = {
  all() {
    return loadProjects();
  },
  add(nome) {
    const items = loadProjects();
    const proj = { id: crypto.randomUUID(), nome, ts: Date.now() };
    items.push(proj);
    saveProjects(items);
    return proj;
  },
  remove(id) {
    saveProjects(loadProjects().filter((p) => p.id !== id));
    // as conversas sobrevivem ao projeto, apenas saem dele
    saveHistory(loadHistory().map((h) => (h.projectId === id ? { ...h, projectId: null } : h)));
  },
};

const History = {
  add(situacao, response, projectId = null) {
    const items = loadHistory();
    const entry = { id: crypto.randomUUID(), ts: Date.now(), situacao, response, projectId };
    items.unshift(entry);
    saveHistory(items);
    return entry;
  },
  remove(id) {
    saveHistory(loadHistory().filter((it) => it.id !== id));
  },
  clear() {
    saveHistory([]);
  },
  all() {
    return loadHistory();
  },
  move(id, projectId) {
    saveHistory(loadHistory().map((h) => (h.id === id ? { ...h, projectId } : h)));
  },
};

class HistoryRail {
  constructor({ onSelect, onNew }) {
    this.onSelect = onSelect;
    this.onNew = onNew;
    this.listEl = document.getElementById('historyList');
    this.projListEl = document.getElementById('projectList');
    this.projForm = document.getElementById('projForm');
    this.projInput = document.getElementById('projName');
    this.activeProject = null;
    this.countEl = document.getElementById('historyCount');
    this.rail = document.getElementById('rail');
    this.scrim = document.getElementById('railScrim');
    this.openBtn = document.getElementById('btnRailOpen');
    this.app = document.querySelector('.app');
    this.activeId = null;

    const novaConversa = () => {
      this.activeId = null;
      this.render();
      this.onNew();
      this.closeOverlay();
    };
    document.getElementById('btnNew').addEventListener('click', novaConversa);
    document.getElementById('btnBrand').addEventListener('click', novaConversa);

    document.getElementById('btnRail').addEventListener('click', () => this.collapse());
    this.openBtn.addEventListener('click', () => this.expand());
    this.scrim.addEventListener('click', () => this.closeOverlay());
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.rail.classList.contains('is-open')) this.closeOverlay();
    });

    document.getElementById('btnNewProject').addEventListener('click', () => {
      this.projForm.hidden = !this.projForm.hidden;
      if (!this.projForm.hidden) this.projInput.focus();
    });
    this.projForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const nome = this.projInput.value.trim();
      if (!nome) return;
      const proj = Projects.add(nome);
      this.projInput.value = '';
      this.projForm.hidden = true;
      this.activeProject = proj.id;
      this.render();
    });
    this.projInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { this.projForm.hidden = true; this.projInput.value = ''; }
    });

    this.clearBtn = document.getElementById('btnClearHistory');
    this.clearBtn.addEventListener('click', () => this.handleClear());
    this.clearBtn.addEventListener('blur', () => this.resetClear());

    this.render();
  }

  isOverlay() {
    return window.matchMedia('(max-width: 900px)').matches;
  }

  collapse() {
    this.app.classList.add('is-collapsed');
    this.openBtn.setAttribute('aria-expanded', 'false');
  }

  expand() {
    if (this.isOverlay()) {
      this.rail.classList.add('is-open');
      this.scrim.classList.add('is-open');
    } else {
      this.app.classList.remove('is-collapsed');
    }
    this.openBtn.setAttribute('aria-expanded', 'true');
  }

  closeOverlay() {
    this.rail.classList.remove('is-open');
    this.scrim.classList.remove('is-open');
    this.openBtn.setAttribute('aria-expanded', 'false');
    this.resetClear();
  }

  handleClear() {
    if (History.all().length === 0) return;
    if (!this.clearArmed) {
      this.clearArmed = true;
      this.clearBtn.textContent = 'Confirmar exclusão?';
      this.clearBtn.classList.add('is-armed');
      return;
    }
    History.clear();
    this.activeId = null;
    this.resetClear();
    this.render();
  }

  resetClear() {
    this.clearArmed = false;
    this.clearBtn.textContent = 'Limpar tudo';
    this.clearBtn.classList.remove('is-armed');
  }

  setActive(id) {
    this.activeId = id;
    this.render();
  }

  currentProject() {
    return this.activeProject;
  }

  renderProjects() {
    const projetos = Projects.all();
    const itens = History.all();
    this.projListEl.innerHTML = '';

    if (projetos.length === 0) {
      const vazio = document.createElement('li');
      vazio.className = 'proj-empty';
      vazio.textContent = 'Agrupe consultas por caso.';
      this.projListEl.appendChild(vazio);
      return;
    }

    for (const proj of projetos) {
      const n = itens.filter((h) => h.projectId === proj.id).length;
      const li = document.createElement('li');
      li.className = 'proj-item' + (proj.id === this.activeProject ? ' is-active' : '');

      const btn = document.createElement('button');
      btn.className = 'proj-item__btn';
      btn.type = 'button';
      btn.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6.5A1.5 1.5 0 0 1 5.5 5H9l2 2h7.5A1.5 1.5 0 0 1 20 8.5v9A1.5 1.5 0 0 1 18.5 19h-13A1.5 1.5 0 0 1 4 17.5Z"/></svg>' +
        `<span class="proj-item__name"></span><span class="proj-item__n">${n}</span>`;
      btn.querySelector('.proj-item__name').textContent = proj.nome;
      btn.title = proj.nome;
      btn.addEventListener('click', () => {
        this.activeProject = this.activeProject === proj.id ? null : proj.id;
        this.render();
      });

      const del = document.createElement('button');
      del.className = 'history-item__del';
      del.type = 'button';
      del.setAttribute('aria-label', `Apagar o projeto ${proj.nome}`);
      del.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0-1 14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2L4 6"/></svg>';
      del.addEventListener('click', (e) => {
        e.stopPropagation();
        Projects.remove(proj.id);
        if (this.activeProject === proj.id) this.activeProject = null;
        this.render();
      });

      li.appendChild(btn);
      li.appendChild(del);
      this.projListEl.appendChild(li);
    }
  }

  openMoveMenu(item, anchor) {
    document.querySelectorAll('.move-menu').forEach((m) => m.remove());
    const menu = document.createElement('div');
    menu.className = 'move-menu';

    const opcoes = [{ id: null, nome: 'Sem projeto' }, ...Projects.all()];
    for (const opt of opcoes) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'move-menu__item' + (item.projectId === opt.id ? ' is-current' : '');
      b.textContent = opt.nome;
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        History.move(item.id, opt.id);
        menu.remove();
        this.render();
      });
      menu.appendChild(b);
    }

    anchor.appendChild(menu);
    const fora = (e) => {
      if (!menu.contains(e.target)) { menu.remove(); document.removeEventListener('click', fora); }
    };
    setTimeout(() => document.addEventListener('click', fora), 0);
  }

  render() {
    this.renderProjects();

    const todos = History.all();
    const items = this.activeProject
      ? todos.filter((h) => h.projectId === this.activeProject)
      : todos;
    this.listEl.innerHTML = '';

    const proj = Projects.all().find((p) => p.id === this.activeProject);
    const label = document.getElementById('historyLabel');
    label.firstChild.textContent = proj ? `Em ${proj.nome}` : 'Consultas';

    this.countEl.textContent = String(items.length);
    this.countEl.hidden = items.length === 0;

    if (items.length === 0) {
      const empty = document.createElement('li');
      empty.className = 'history-empty';
      empty.textContent = this.activeProject
        ? 'Nenhuma consulta neste projeto. A próxima que você fizer entra aqui.'
        : 'Suas consultas ficam salvas aqui.';
      this.listEl.appendChild(empty);
      return;
    }

    for (const item of items) {
      const li = document.createElement('li');
      li.className = 'history-item' + (item.id === this.activeId ? ' is-active' : '');

      const btn = document.createElement('button');
      btn.className = 'history-item__btn';
      btn.type = 'button';
      btn.textContent = item.situacao;
      btn.title = item.situacao;
      btn.addEventListener('click', () => {
        this.setActive(item.id);
        this.onSelect(item);
        this.closeOverlay();
      });

      const del = document.createElement('button');
      del.className = 'history-item__del';
      del.type = 'button';
      del.setAttribute('aria-label', 'Apagar esta consulta');
      del.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0-1 14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2L4 6"/></svg>';
      del.addEventListener('click', (e) => {
        e.stopPropagation();
        History.remove(item.id);
        if (this.activeId === item.id) this.activeId = null;
        this.render();
      });

      const projetos = Projects.all();
      if (projetos.length) {
        const mover = document.createElement('button');
        mover.className = 'history-item__del history-item__move';
        mover.type = 'button';
        mover.setAttribute('aria-label', 'Mover para um projeto');
        mover.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6.5A1.5 1.5 0 0 1 5.5 5H9l2 2h7.5A1.5 1.5 0 0 1 20 8.5v9A1.5 1.5 0 0 1 18.5 19h-13A1.5 1.5 0 0 1 4 17.5Z"/></svg>';
        mover.addEventListener('click', (e) => {
          e.stopPropagation();
          this.openMoveMenu(item, li);
        });
        li.appendChild(mover);
      }

      li.appendChild(btn);
      li.appendChild(del);
      this.listEl.appendChild(li);
    }
  }
}
