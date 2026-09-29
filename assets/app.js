/* Study Hub — 靜態多科目複習站（無需 build，直接放 GitHub Pages）
 * 路由：
 *   #/                               首頁（科目列表）
 *   #/s/:sid                         科目總覽
 *   #/s/:sid/c/:cid/:tab             章節（summary | slides | exam | practice）
 *   #/s/:sid/practice?ch=&src=&...   練習區
 *   #/s/:sid/analysis                考題分析
 *   #/report?...                     問題回報
 */
(() => {
  'use strict';
  const CFG = window.STUDY_HUB_CONFIG || {};
  const $app = document.getElementById('app');
  const $nav = document.getElementById('topnav');

  // ------------------------------------------------------------ utilities
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* ignore */ } },
  };
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const countBy = (arr, f) => { const m = new Map(); for (const x of arr) for (const k of [].concat(f(x))) m.set(k, (m.get(k) || 0) + 1); return m; };
  const toast = (msg) => {
    let t = document.querySelector('.toast');
    if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 1800);
  };
  const md = (text) => (window.marked ? window.marked.parse(text || '') : `<pre>${esc(text)}</pre>`);
  const fetchJSON = async (url) => { const r = await fetch(url, { cache: 'no-cache' }); if (!r.ok) throw new Error(`${url}: ${r.status}`); return r.json(); };
  const fetchText = async (url) => { const r = await fetch(url, { cache: 'no-cache' }); if (!r.ok) throw new Error(`${url}: ${r.status}`); return r.text(); };

  const SOURCE_COLORS = { '113 考古': '#2f7d6d', '111 期中考古': '#3b6fb6', '2026 課堂題': '#d08a2c', '模擬新題': '#8a5cc2' };
  const srcColor = (s) => SOURCE_COLORS[s] || '#888';
  const isExamSource = (s) => /考古/.test(s);

  // theme
  const applyTheme = (t) => { if (t) document.documentElement.setAttribute('data-theme', t); else document.documentElement.removeAttribute('data-theme'); };
  applyTheme(store.get('sh:theme', null));
  document.getElementById('themeBtn').addEventListener('click', () => {
    const cur = document.documentElement.getAttribute('data-theme')
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    applyTheme(next); store.set('sh:theme', next);
  });

  // ------------------------------------------------------------ data layer
  const DB = { index: null, subjects: {} };
  async function loadIndex() {
    if (!DB.index) DB.index = await fetchJSON('subjects/index.json');
    return DB.index;
  }
  async function loadSubject(sid) {
    if (DB.subjects[sid]) return DB.subjects[sid];
    const idx = await loadIndex();
    const ent = idx.find((x) => x.id === sid);
    if (!ent) throw new Error(`找不到科目 ${sid}`);
    const meta = await fetchJSON(`${ent.path}/subject.json`);
    const files = meta.questionFiles || [];
    const lists = await Promise.all(files.map((f) => fetchJSON(`${ent.path}/${f}`).catch(() => [])));
    const questions = lists.flat();
    const chMap = Object.fromEntries(meta.chapters.map((c, i) => [c.id, { ...c, idx: i + 1 }]));
    const subj = { meta, path: ent.path, questions, chMap, content: {} };
    DB.subjects[sid] = subj;
    return subj;
  }
  async function loadContent(subj, cid) {
    if (subj.content[cid]) return subj.content[cid];
    let raw = '';
    try { raw = await fetchText(`${subj.path}/content/${cid}.md`); } catch { raw = ''; }
    const parts = { summary: '', slides: '', exam: '' };
    let cur = 'summary';
    for (const line of raw.split('\n')) {
      const m = line.match(/^===\s*(\w+)\s*===\s*$/);
      if (m) { cur = m[1]; parts[cur] = parts[cur] || ''; continue; }
      parts[cur] = (parts[cur] || '') + line + '\n';
    }
    subj.content[cid] = parts;
    return parts;
  }

  // progress: { qid: { c: n, w: n, last: 'c'|'w', t: ts } }
  const progKey = (sid) => `sh:${sid}:progress`;
  const starKey = (sid) => `sh:${sid}:stars`;
  const getProg = (sid) => store.get(progKey(sid), {});
  const record = (sid, qid, ok) => {
    const p = getProg(sid);
    const r = p[qid] || { c: 0, w: 0 };
    ok ? r.c++ : r.w++; r.last = ok ? 'c' : 'w'; r.t = Date.now();
    p[qid] = r; store.set(progKey(sid), p);
  };
  const getStars = (sid) => new Set(store.get(starKey(sid), []));
  const toggleStar = (sid, qid) => { const s = getStars(sid); s.has(qid) ? s.delete(qid) : s.add(qid); store.set(starKey(sid), [...s]); return s.has(qid); };

  // ------------------------------------------------------------ router
  function parseHash() {
    const h = location.hash.replace(/^#/, '') || '/';
    const [path, qs] = h.split('?');
    const seg = path.split('/').filter(Boolean).map(decodeURIComponent);
    const q = Object.fromEntries(new URLSearchParams(qs || ''));
    return { seg, q };
  }
  async function route() {
    const { seg, q } = parseHash();
    window.scrollTo(0, 0);
    try {
      if (seg.length === 0) return await pageHome();
      if (seg[0] === 'report') return await pageReport(q);
      if (seg[0] === 's' && seg[1]) {
        const sid = seg[1];
        if (seg.length === 2) return await pageSubject(sid);
        if (seg[2] === 'c' && seg[3]) return await pageChapter(sid, seg[3], seg[4] || 'summary');
        if (seg[2] === 'practice') return await pagePractice(sid, q);
        if (seg[2] === 'analysis') return await pageAnalysis(sid);
      }
      $app.innerHTML = `<div class="card"><h1>找不到頁面</h1><p><a href="#/">回首頁</a></p></div>`;
    } catch (e) {
      console.error(e);
      $app.innerHTML = `<div class="card"><h1>載入失敗</h1><p class="muted">${esc(e.message)}</p>
        <p class="small muted">如果你是直接用瀏覽器打開 index.html（file://），請改用 GitHub Pages 網址或 <code>python3 -m http.server</code> 開啟。</p></div>`;
    }
  }
  window.addEventListener('hashchange', route);

  function setNav(sid, active) {
    if (!sid) { $nav.innerHTML = `<a href="#/" class="${active === 'home' ? 'active' : ''}">科目</a><a href="#/report" class="${active === 'report' ? 'active' : ''}">問題回報</a>`; return; }
    const s = DB.subjects[sid];
    const short = s?.meta.short || '科目';
    $nav.innerHTML = [
      ['#/', '所有科目', 'home'],
      [`#/s/${sid}`, `${short}總覽`, 'subject'],
      [`#/s/${sid}/practice`, '練習區', 'practice'],
      [`#/s/${sid}/analysis`, '考題分析', 'analysis'],
      [`#/report?sid=${sid}`, '問題回報', 'report'],
    ].map(([h, t, k]) => `<a href="${h}" class="${active === k ? 'active' : ''}">${t}</a>`).join('');
  }

  // ------------------------------------------------------------ pages
  async function pageHome() {
    setNav(null, 'home');
    const idx = await loadIndex();
    const subs = await Promise.all(idx.map((x) => loadSubject(x.id).catch(() => null)));
    const cards = subs.filter(Boolean).map((s) => {
      const prog = getProg(s.meta.id);
      const qs = s.questions.filter((q) => !q.imageOnly);
      const done = qs.filter((q) => prog[q.id]).length;
      return `<a class="card ch-item" href="#/s/${s.meta.id}" style="display:block">
        <div class="row"><span style="font-size:1.8rem">${esc(s.meta.icon || '📘')}</span>
          <div><div class="title" style="font-size:1.15rem">${esc(s.meta.title)}</div>
          <div class="muted small">${esc(s.meta.term || '')}</div></div></div>
        <p class="small muted" style="margin:.6em 0">${esc(s.meta.description || '')}</p>
        <div class="row small"><span class="badge">${s.meta.chapters.length} 章</span><span class="badge">${qs.length} 題</span>
          <span class="badge accent">已練 ${done} 題</span></div>
        <div class="progress"><i style="width:${qs.length ? (done / qs.length) * 100 : 0}%"></i></div></a>`;
    }).join('');
    $app.innerHTML = `
      <h1>📚 Study Hub 複習站</h1>
      <p class="muted">選一個科目開始：重點整理 → 上課 slides 重點 → 考點分析 → 考古練習與模擬新題。練習紀錄會存在你這台裝置的瀏覽器。</p>
      <div class="grid cols-2" style="margin-top:18px">${cards}</div>
      <p class="small muted" style="margin-top:28px">想新增科目？請看 repo 的 <code>README.md</code>（在 <code>subjects/</code> 新增一個資料夾即可）。</p>`;
  }

  function chapterStats(subj, cid) {
    const qs = subj.questions.filter((q) => q.chapter === cid && !q.imageOnly);
    const prog = getProg(subj.meta.id);
    const done = qs.filter((q) => prog[q.id]).length;
    const wrong = qs.filter((q) => prog[q.id]?.last === 'w').length;
    const exam = qs.filter((q) => isExamSource(q.source)).length;
    return { total: qs.length, done, wrong, exam, other: qs.length - exam };
  }

  async function pageSubject(sid) {
    const subj = await loadSubject(sid);
    setNav(sid, 'subject');
    const m = subj.meta;
    const qs = subj.questions.filter((q) => !q.imageOnly);
    const prog = getProg(sid);
    const done = qs.filter((q) => prog[q.id]).length;
    const correct = qs.filter((q) => prog[q.id]?.last === 'c').length;
    const wrong = qs.filter((q) => prog[q.id]?.last === 'w').length;
    const srcCounts = countBy(qs, (q) => q.source);
    const groups = (m.groups || [{ title: '章節', chapters: m.chapters.map((c) => c.id) }]).map((g) => {
      const items = g.chapters.map((cid) => {
        const c = subj.chMap[cid]; if (!c) return '';
        const st = chapterStats(subj, cid);
        const status = c.slides ? `<span class="badge good">已上課 ${esc(c.week || '')}</span>` : `<span class="badge warn">未上課</span>`;
        return `<a class="card ch-item" href="#/s/${sid}/c/${cid}/summary">
          <div class="num">${c.idx}</div>
          <div style="flex:1;min-width:0">
            <div class="row" style="gap:6px"><span class="title">${esc(c.title)}</span>${status}</div>
            <div class="en">${esc(c.en || '')} · ${esc(c.teacher || '')}</div>
            <div class="row small" style="gap:6px;margin-top:4px">
              <span class="badge">考古 ${st.exam}</span><span class="badge">課堂/新題 ${st.other}</span>
              ${st.wrong ? `<span class="badge bad">錯 ${st.wrong}</span>` : ''}
            </div>
            <div class="progress" title="已練 ${st.done}/${st.total}"><i style="width:${st.total ? (st.done / st.total) * 100 : 0}%"></i></div>
          </div></a>`;
      }).join('');
      return `<section class="ch-group"><h2>${esc(g.title)}</h2><div class="grid cols-2">${items}</div></section>`;
    }).join('');
    $app.innerHTML = `
      <div class="crumbs"><a href="#/">所有科目</a> / ${esc(m.title)}</div>
      <div class="hero"><div class="emoji">${esc(m.icon || '📘')}</div>
        <div><h1>${esc(m.title)}</h1><div class="muted">${esc(m.term || '')} · ${esc(m.description || '')}</div></div></div>
      <div class="stat-row">
        <div class="stat"><b>${m.chapters.length}</b><span>章節</span></div>
        ${[...srcCounts].map(([k, v]) => `<div class="stat"><b style="color:${srcColor(k)}">${v}</b><span>${esc(k)}</span></div>`).join('')}
        <div class="stat"><b>${done}</b><span>已練習題數</span></div>
        <div class="stat"><b>${done ? Math.round((correct / done) * 100) : 0}%</b><span>最近答對率</span></div>
      </div>
      <div class="row" style="margin:14px 0 4px">
        <a class="btn primary" href="#/s/${sid}/practice">✏️ 開始練習</a>
        <a class="btn" href="#/s/${sid}/practice?filter=wrong&start=1" ${wrong ? '' : 'aria-disabled="true"'}>❌ 錯題本（${wrong}）</a>
        <a class="btn" href="#/s/${sid}/practice?filter=star&start=1">⭐ 收藏題</a>
        <a class="btn" href="#/s/${sid}/analysis">📊 考題分析</a>
      </div>
      ${groups}`;
  }

  const TABS = [['summary', '重點整理'], ['slides', '上課 slides'], ['exam', '考點分析'], ['practice', '練習']];
  async function pageChapter(sid, cid, tab) {
    const subj = await loadSubject(sid);
    setNav(sid, 'subject');
    const c = subj.chMap[cid];
    if (!c) throw new Error(`找不到章節 ${cid}`);
    const content = await loadContent(subj, cid);
    const order = subj.meta.chapters.map((x) => x.id);
    const i = order.indexOf(cid);
    const prev = order[i - 1], next = order[i + 1];
    let body = '';
    if (tab === 'exam') body = chapterExamStats(subj, cid) + `<div class="md">${md(content.exam)}</div>`;
    else if (tab === 'practice') body = chapterPracticePanel(subj, cid);
    else body = `<div class="md">${md(content[tab] || '_（尚無內容）_')}</div>`;
    $app.innerHTML = `
      <div class="crumbs"><a href="#/">所有科目</a> / <a href="#/s/${sid}">${esc(subj.meta.title)}</a> / 第 ${c.idx} 章</div>
      <h1>${esc(c.title)}</h1>
      <div class="row small muted">${esc(c.en || '')} · ${esc(c.teacher || '')} · ${c.slides ? `<span class="badge good">已上課 ${esc(c.week)}</span>` : '<span class="badge warn">未上課（依去年共筆 / 考古）</span>'}</div>
      <nav class="tabs">${TABS.map(([k, t]) => `<a href="#/s/${sid}/c/${cid}/${k}" class="${k === tab ? 'active' : ''}">${t}</a>`).join('')}</nav>
      <div class="card">${body}</div>
      <div class="row" style="margin-top:16px">
        ${prev ? `<a class="btn" href="#/s/${sid}/c/${prev}/${tab}">← ${esc(subj.chMap[prev].title)}</a>` : ''}
        <span class="spacer"></span>
        ${next ? `<a class="btn" href="#/s/${sid}/c/${next}/${tab}">${esc(subj.chMap[next].title)} →</a>` : ''}
      </div>
      <p class="small muted" style="margin-top:18px">內容有誤？<a href="#/report?sid=${sid}&where=${encodeURIComponent(`${c.title}／${TABS.find((t) => t[0] === tab)?.[1] || tab}`)}">回報這一頁</a></p>`;
  }

  function barsHTML(entries, total, color) {
    const max = Math.max(1, ...entries.map((e) => e[1]));
    return `<div class="bars">${entries.map(([label, n, segs]) => {
      const inner = segs ? segs.map(([v, col]) => `<i style="width:${(v / max) * 100}%;background:${col}"></i>`).join('')
        : `<i style="width:${(n / max) * 100}%;background:${color || 'var(--accent)'}"></i>`;
      return `<div class="bar"><span class="label" title="${esc(label)}">${esc(label)}</span><span class="track">${inner}</span><span class="n">${n}</span></div>`;
    }).join('')}</div>`;
  }

  function chapterExamStats(subj, cid) {
    const qs = subj.questions.filter((q) => q.chapter === cid);
    const exam = qs.filter((q) => isExamSource(q.source));
    if (!exam.length) return `<p class="muted">這章去年考古沒有題目。</p>`;
    const topics = [...countBy(exam, (q) => q.topics || [])].sort((a, b) => b[1] - a[1]).slice(0, 12);
    const patterns = [...countBy(exam, (q) => q.pattern || '其他')].sort((a, b) => b[1] - a[1]);
    const srcs = [...countBy(exam, (q) => q.source)];
    const img = exam.filter((q) => q.imageOnly).length;
    return `
      <h2 style="margin-top:0">📊 自動統計（考古 ${exam.length} 題${img ? `，其中 ${img} 題為看圖題未收錄練習` : ''}）</h2>
      <div class="legend">${srcs.map(([s, n]) => `<span><i style="background:${srcColor(s)}"></i>${esc(s)} ${n}</span>`).join('')}</div>
      <div class="grid cols-2">
        <div><h3>考點出現次數</h3>${barsHTML(topics.map(([k, v]) => [k, v]))}</div>
        <div><h3>題型分布</h3>${barsHTML(patterns.map(([k, v]) => [k, v]), 0, '#8a5cc2')}</div>
      </div>
      <hr style="border:none;border-top:1px solid var(--border);margin:22px 0">`;
  }

  function chapterPracticePanel(subj, cid) {
    const sid = subj.meta.id;
    const qs = subj.questions.filter((q) => q.chapter === cid && !q.imageOnly);
    const by = countBy(qs, (q) => q.source);
    const st = chapterStats(subj, cid);
    const link = (qsx) => `#/s/${sid}/practice?${new URLSearchParams(qsx).toString()}`;
    return `
      <p>本章共有 <b>${qs.length}</b> 題可練習：${[...by].map(([s, n]) => `<span class="badge" style="border-color:${srcColor(s)};color:${srcColor(s)}">${esc(s)} ${n}</span>`).join(' ')}</p>
      <div class="grid cols-2" style="margin-top:12px">
        <a class="card" href="${link({ ch: cid, src: 'exam', mode: 'order', start: 1 })}"><b>📝 考古題（依序）</b><div class="small muted">照原考卷順序作答，看詳解</div></a>
        <a class="card" href="${link({ ch: cid, mode: 'random', start: 1 })}"><b>🎲 本章全部隨機</b><div class="small muted">考古 + 課堂題 + 模擬新題</div></a>
        <a class="card" href="${link({ ch: cid, src: 'new,class', mode: 'random', start: 1 })}"><b>✨ 課堂題與模擬新題</b><div class="small muted">依考古出題模式編寫的新題</div></a>
        <a class="card" href="${link({ ch: cid, filter: 'wrong', start: 1 })}"><b>❌ 本章錯題（${st.wrong}）</b><div class="small muted">只練上次答錯的題目</div></a>
        <a class="card" href="${link({ ch: cid, view: 'browse' })}"><b>📖 瀏覽模式</b><div class="small muted">一次看全部題目，答案可展開</div></a>
      </div>`;
  }

  // ------------------------------------------------------------ practice
  const SRC_GROUPS = [
    ['k113', '113 考古', (q) => q.source === '113 考古'],
    ['k111', '111 期中考古', (q) => q.source === '111 期中考古'],
    ['class', '2026 課堂題', (q) => q.source === '2026 課堂題'],
    ['new', '模擬新題', (q) => q.source === '模擬新題'],
  ];
  function srcMatch(srcParam) {
    if (!srcParam) return () => true;
    const keys = new Set(srcParam.split(','));
    if (keys.has('exam')) { keys.add('k113'); keys.add('k111'); }
    return (q) => SRC_GROUPS.some(([k, , f]) => keys.has(k) && f(q));
  }
  function buildPool(subj, q) {
    const sid = subj.meta.id;
    const chs = q.ch ? new Set(q.ch.split(',')) : null;
    const sm = srcMatch(q.src);
    const prog = getProg(sid);
    const stars = getStars(sid);
    const kw = (q.kw || '').trim().toLowerCase();
    let pool = subj.questions.filter((x) => !x.imageOnly && (!chs || chs.has(x.chapter)) && sm(x));
    if (q.short === '0') pool = pool.filter((x) => x.type !== 'short');
    if (q.filter === 'wrong') pool = pool.filter((x) => prog[x.id]?.last === 'w');
    if (q.filter === 'new') pool = pool.filter((x) => !prog[x.id]);
    if (q.filter === 'star') pool = pool.filter((x) => stars.has(x.id));
    if (kw) pool = pool.filter((x) => (x.stem + ' ' + (x.options || []).map((o) => o.t).join(' ') + ' ' + (x.topics || []).join(' ') + ' ' + (x.explain || '')).toLowerCase().includes(kw));
    if (q.mode === 'random') pool = shuffle(pool);
    const n = parseInt(q.n, 10);
    if (n > 0) pool = pool.slice(0, n);
    return pool;
  }

  async function pagePractice(sid, q) {
    const subj = await loadSubject(sid);
    setNav(sid, 'practice');
    if (q.view === 'browse') return renderBrowse(subj, q);
    if (q.start) return runSession(subj, buildPool(subj, q), q);
    renderPracticeSetup(subj, q);
  }

  function renderPracticeSetup(subj, q) {
    const sid = subj.meta.id;
    const m = subj.meta;
    const chSel = new Set(q.ch ? q.ch.split(',') : []);
    const srcSel = new Set(q.src ? q.src.split(',') : SRC_GROUPS.map((s) => s[0]));
    const groups = (m.groups || [{ title: '章節', chapters: m.chapters.map((c) => c.id) }]);
    $app.innerHTML = `
      <div class="crumbs"><a href="#/">所有科目</a> / <a href="#/s/${sid}">${esc(m.title)}</a> / 練習區</div>
      <h1>✏️ 練習區</h1>
      <p class="muted small">選擇範圍後開始。作答後立即顯示答案與詳解；鍵盤可用 A–E（或 1–5）作答、Enter 下一題。</p>
      <form class="filters card" id="pf">
        <fieldset><legend>章節（不選 = 全部）</legend>
          ${groups.map((g) => `<div style="margin:4px 0 8px"><div class="small muted" style="margin-bottom:4px">${esc(g.title)}
            <a href="#" data-grp="${g.chapters.join(',')}" class="small">全選</a></div><div class="chips">
            ${g.chapters.map((cid) => { const c = subj.chMap[cid]; const st = chapterStats(subj, cid);
              return `<label class="chip ${chSel.has(cid) ? 'on' : ''}"><input type="checkbox" name="ch" value="${cid}" ${chSel.has(cid) ? 'checked' : ''}>${esc(c.title)} <span class="muted">${st.total}</span></label>`; }).join('')}
          </div></div>`).join('')}
        </fieldset>
        <fieldset><legend>題目來源</legend><div class="chips">
          ${SRC_GROUPS.map(([k, t]) => `<label class="chip ${srcSel.has(k) ? 'on' : ''}"><input type="checkbox" name="src" value="${k}" ${srcSel.has(k) ? 'checked' : ''}><i style="width:8px;height:8px;border-radius:50%;background:${srcColor(t)};display:inline-block"></i>${t}</label>`).join('')}
        </div></fieldset>
        <div class="grid cols-3">
          <label class="field">順序<select name="mode"><option value="random">隨機</option><option value="order" ${q.mode === 'order' ? 'selected' : ''}>依原題序</option></select></label>
          <label class="field">篩選<select name="filter">
            <option value="">全部題目</option><option value="new">只練沒做過的</option>
            <option value="wrong">只練上次答錯的</option><option value="star">只練收藏的</option></select></label>
          <label class="field">題數<select name="n"><option value="10">10 題</option><option value="20" selected>20 題</option><option value="50">50 題</option><option value="0">全部</option></select></label>
          <label class="field">簡答題<select name="short"><option value="1">包含（自我評分）</option><option value="0">不包含</option></select></label>
        </div>
        <label class="field">關鍵字（選填，可搜題幹、選項、考點）<input type="search" name="kw" placeholder="例如：C3 convertase、IgA、Listeria" value="${esc(q.kw || '')}"></label>
        <div class="row"><button class="btn primary" type="submit">開始練習</button><span class="muted small" id="poolCount"></span>
          <span class="spacer"></span><button class="btn small" type="button" id="browseBtn">📖 用瀏覽模式看</button>
          <button class="btn small" type="button" id="resetBtn" title="清除這台裝置上本科的作答紀錄">🗑 清除紀錄</button></div>
      </form>`;
    const form = document.getElementById('pf');
    const read = () => {
      const fd = new FormData(form);
      const o = { ch: fd.getAll('ch').join(','), src: fd.getAll('src').join(','), mode: fd.get('mode'), filter: fd.get('filter'), n: fd.get('n'), short: fd.get('short'), kw: fd.get('kw') };
      Object.keys(o).forEach((k) => { if (!o[k]) delete o[k]; });
      return o;
    };
    const updateCount = () => {
      const o = read(); const full = buildPool(subj, { ...o, n: 0, mode: 'order' });
      document.getElementById('poolCount').textContent = `符合條件：${full.length} 題`;
    };
    form.addEventListener('change', (e) => {
      if (e.target.matches('input[type=checkbox]')) e.target.closest('.chip').classList.toggle('on', e.target.checked);
      updateCount();
    });
    form.addEventListener('input', (e) => { if (e.target.name === 'kw') updateCount(); });
    form.querySelectorAll('[data-grp]').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      const ids = a.dataset.grp.split(',');
      const boxes = ids.map((id) => form.querySelector(`input[name=ch][value="${id}"]`)).filter(Boolean);
      const allOn = boxes.every((b) => b.checked);
      boxes.forEach((b) => { b.checked = !allOn; b.closest('.chip').classList.toggle('on', !allOn); });
      updateCount();
    }));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const o = read();
      if (!o.src) return toast('請至少選一個題目來源');
      location.hash = `#/s/${sid}/practice?${new URLSearchParams({ ...o, start: 1 })}`;
    });
    document.getElementById('browseBtn').addEventListener('click', () => {
      const o = read(); delete o.n; location.hash = `#/s/${sid}/practice?${new URLSearchParams({ ...o, mode: 'order', view: 'browse' })}`;
    });
    document.getElementById('resetBtn').addEventListener('click', () => {
      if (confirm('確定要清除這台裝置上本科目的所有作答紀錄與收藏嗎？')) { store.set(progKey(sid), {}); store.set(starKey(sid), []); toast('已清除'); updateCount(); }
    });
    updateCount();
  }

  const reportLink = (sid, qq) => `#/report?${new URLSearchParams({ sid, qid: qq.id, where: `${qq.source} ${qq.id}` })}`;

  function qMeta(subj, qq) {
    const c = subj.chMap[qq.chapter];
    return `<div class="q-meta">
      <span class="badge" style="border-color:${srcColor(qq.source)};color:${srcColor(qq.source)}">${esc(qq.source)}${qq.num ? ` #${qq.num}` : ''}</span>
      ${c ? `<a class="badge" href="#/s/${subj.meta.id}/c/${c.id}/summary">${esc(c.title)}</a>` : ''}
      ${qq.pattern ? `<span class="badge">${esc(qq.pattern)}</span>` : ''}
      ${(qq.topics || []).filter((t) => t !== '其他').map((t) => `<span class="badge accent">${esc(t)}</span>`).join('')}
      ${qq.disputed ? '<span class="badge warn">答案有爭議</span>' : ''}
    </div>`;
  }

  function runSession(subj, pool, q) {
    const sid = subj.meta.id;
    if (!pool.length) {
      $app.innerHTML = `<div class="card"><h1>沒有符合條件的題目</h1><p class="muted">${q.filter === 'wrong' ? '目前沒有錯題，太棒了！' : q.filter === 'star' ? '還沒有收藏任何題目，練習時按 ☆ 就能收藏。' : '換個範圍試試看。'}</p>
        <a class="btn" href="#/s/${sid}/practice">回練習設定</a></div>`;
      return;
    }
    const S = { i: 0, correct: 0, answered: 0, wrongIds: [], answeredCur: false };
    const render = () => {
      const qq = pool[S.i];
      const stars = getStars(sid);
      const isShort = qq.type === 'short' || !(qq.options || []).length;
      $app.innerHTML = `
        <div class="crumbs"><a href="#/s/${sid}">${esc(subj.meta.title)}</a> / <a href="#/s/${sid}/practice">練習區</a> / 作答中</div>
        <div class="row"><b>第 ${S.i + 1} / ${pool.length} 題</b><span class="spacer"></span>
          <span class="score muted">答對 ${S.correct} / ${S.answered}</span>
          <a class="btn small" href="#/s/${sid}/practice">結束</a></div>
        <div class="pbar"><i style="width:${(S.i / pool.length) * 100}%"></i></div>
        <div class="card q-card">
          ${qMeta(subj, qq)}
          <div class="q-stem">${esc(qq.stem)}</div>
          ${isShort ? `<div class="note">📝 簡答題：先在心裡或紙上作答，再按「顯示參考答案」自我評分。</div>
              <div class="q-foot"><button class="btn primary" id="reveal">顯示參考答案</button></div>`
            : `<div class="opts">${qq.options.map((o) => `<button class="opt" data-k="${o.k}"><span class="k">${o.k}</span><span>${esc(o.t)}</span></button>`).join('')}</div>`}
          <div id="fb"></div>
          <div class="q-foot">
            <button class="btn small" id="star">${stars.has(qq.id) ? '★ 已收藏' : '☆ 收藏'}</button>
            <a class="btn small" href="${reportLink(sid, qq)}">⚠️ 回報此題</a>
            <span class="spacer"></span>
            <button class="btn primary" id="next" style="display:none">${S.i + 1 < pool.length ? '下一題 →' : '看結果'}</button>
          </div>
        </div>`;
      S.answeredCur = false;
      const fb = document.getElementById('fb');
      const next = document.getElementById('next');
      document.getElementById('star').onclick = (e) => { const on = toggleStar(sid, qq.id); e.target.textContent = on ? '★ 已收藏' : '☆ 收藏'; };
      const showExplain = (verdictHTML, cls) => {
        fb.innerHTML = `<div class="feedback ${cls}">${verdictHTML}
          ${qq.answerText ? `<div class="explain"><b>參考答案：</b>${esc(qq.answerText)}</div>` : ''}
          ${qq.explain ? `<div class="explain" style="margin-top:6px">${esc(qq.explain)}</div>` : ''}
          ${qq.note ? `<div class="note">📌 ${esc(qq.note)}</div>` : ''}</div>`;
        next.style.display = '';
      };
      const answer = (k) => {
        if (S.answeredCur) return;
        S.answeredCur = true; S.answered++;
        const ans = qq.answer || [];
        const ok = ans.length ? ans.includes(k) : false;
        if (ok) S.correct++; else S.wrongIds.push(qq.id);
        record(sid, qq.id, ok);
        $app.querySelectorAll('.opt').forEach((b) => {
          b.disabled = true;
          if (ans.includes(b.dataset.k)) b.classList.add('correct');
          else if (b.dataset.k === k) b.classList.add('wrong');
        });
        const ansTxt = ans.length ? ans.map((a) => `(${a})`).join(' 或 ') : '（原考古無正確選項）';
        showExplain(`<div class="verdict">${ok ? '✅ 答對了！' : `❌ 答錯了，正確答案是 ${ansTxt}`}</div>`, ok ? 'good' : 'bad');
        next.focus();
      };
      $app.querySelectorAll('.opt').forEach((b) => b.addEventListener('click', () => answer(b.dataset.k)));
      const rv = document.getElementById('reveal');
      if (rv) rv.onclick = () => {
        rv.parentElement.remove();
        showExplain(`<div class="verdict">自我評分：</div><div class="row" style="margin:6px 0 10px"><button class="btn small" id="selfOk">🙆 我會</button><button class="btn small" id="selfNo">🙅 還不熟</button></div>`, '');
        next.style.display = 'none';
        const grade = (ok) => { if (S.answeredCur) return; S.answeredCur = true; S.answered++; if (ok) S.correct++; else S.wrongIds.push(qq.id); record(sid, qq.id, ok); next.style.display = ''; next.focus(); };
        document.getElementById('selfOk').onclick = () => grade(true);
        document.getElementById('selfNo').onclick = () => grade(false);
      };
      next.onclick = () => { S.i++; S.i < pool.length ? render() : finish(); window.scrollTo(0, 0); };
    };
    const finish = () => {
      document.removeEventListener('keydown', onKey);
      const pct = S.answered ? Math.round((S.correct / S.answered) * 100) : 0;
      const wrongQs = pool.filter((x) => S.wrongIds.includes(x.id));
      $app.innerHTML = `<div class="card" style="text-align:center">
          <div style="font-size:3rem">${pct >= 80 ? '🎉' : pct >= 60 ? '👍' : '💪'}</div>
          <h1>答對 ${S.correct} / ${S.answered}（${pct}%）</h1>
          <div class="row" style="justify-content:center;margin-top:10px">
            <a class="btn primary" href="#/s/${sid}/practice">再練一組</a>
            ${wrongQs.length ? `<a class="btn" href="#/s/${sid}/practice?filter=wrong&start=1&n=0">❌ 練全部錯題</a>` : ''}
            <a class="btn" href="#/s/${sid}">回總覽</a></div></div>
        ${wrongQs.length ? `<h2>這次答錯的題目</h2>${wrongQs.map((x) => browseItem(subj, x, true)).join('')}` : ''}`;
    };
    const onKey = (e) => {
      if (!location.hash.includes('/practice') || e.target.matches('input,textarea,select')) return;
      const k = e.key.toUpperCase();
      const map = { 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E' };
      const key = map[k] || k;
      const btn = $app.querySelector(`.opt[data-k="${key}"]`);
      if (btn && !btn.disabled) { btn.click(); return; }
      if ((e.key === 'Enter' || e.key === 'ArrowRight')) { const n = document.getElementById('next'); if (n && n.style.display !== 'none') { e.preventDefault(); n.click(); } }
    };
    document.addEventListener('keydown', onKey);
    window.addEventListener('hashchange', () => document.removeEventListener('keydown', onKey), { once: true });
    render();
  }

  function browseItem(subj, qq, open) {
    const ans = qq.answer || [];
    return `<div class="card browse-item">
      ${qMeta(subj, qq)}
      <div class="q-stem" style="margin-bottom:4px">${esc(qq.stem)}</div>
      ${(qq.options || []).length ? `<ul class="opts-list">${qq.options.map((o) => `<li class="${open && ans.includes(o.k) ? 'ans' : ''}">(${o.k}) ${esc(o.t)}</li>`).join('')}</ul>` : ''}
      <details ${open ? 'open' : ''}><summary>看答案與詳解</summary>
        <div class="feedback"><div class="verdict">答案：${ans.length ? ans.map((a) => `(${a})`).join(' 或 ') : (qq.answerText ? '見參考答案' : '無正確選項')}</div>
        ${qq.answerText ? `<div class="explain"><b>參考答案：</b>${esc(qq.answerText)}</div>` : ''}
        ${qq.explain ? `<div class="explain" style="margin-top:6px">${esc(qq.explain)}</div>` : ''}
        ${qq.note ? `<div class="note">📌 ${esc(qq.note)}</div>` : ''}</div>
        <div class="small" style="margin-top:6px"><a href="${reportLink(subj.meta.id, qq)}">⚠️ 回報此題</a></div>
      </details></div>`;
  }

  function renderBrowse(subj, q) {
    const sid = subj.meta.id;
    const pool = buildPool(subj, { ...q, n: 0, mode: 'order' });
    const title = q.ch && q.ch.split(',').length === 1 ? subj.chMap[q.ch]?.title : '自訂範圍';
    const img = subj.questions.filter((x) => x.imageOnly && (!q.ch || q.ch.split(',').includes(x.chapter))).length;
    $app.innerHTML = `
      <div class="crumbs"><a href="#/s/${sid}">${esc(subj.meta.title)}</a> / <a href="#/s/${sid}/practice">練習區</a> / 瀏覽</div>
      <h1>📖 瀏覽：${esc(title || '')}</h1>
      <div class="row"><span class="muted">${pool.length} 題${img ? `（另有 ${img} 題看圖題未收錄）` : ''}</span><span class="spacer"></span>
        <button class="btn small" id="openAll">全部展開答案</button></div>
      <div style="margin-top:12px">${pool.map((x) => browseItem(subj, x, false)).join('')}</div>`;
    document.getElementById('openAll').onclick = (e) => {
      const ds = $app.querySelectorAll('details'); const open = e.target.textContent.includes('展開');
      ds.forEach((d) => { d.open = open; }); e.target.textContent = open ? '全部收合' : '全部展開答案';
    };
  }

  // ------------------------------------------------------------ analysis
  async function pageAnalysis(sid) {
    const subj = await loadSubject(sid);
    setNav(sid, 'analysis');
    const exam = subj.questions.filter((q) => isExamSource(q.source));
    const srcs = [...new Set(exam.map((q) => q.source))];
    const chRows = subj.meta.chapters.map((c) => {
      const qs = exam.filter((q) => q.chapter === c.id);
      return [c.title, qs.length, srcs.map((s) => [qs.filter((q) => q.source === s).length, srcColor(s)])];
    }).filter((r) => r[1] > 0).sort((a, b) => b[1] - a[1]);
    const topics = [...countBy(exam, (q) => (q.topics || []).filter((t) => t !== '其他'))].sort((a, b) => b[1] - a[1]).slice(0, 20);
    const patterns = [...countBy(exam, (q) => q.pattern || '其他')].sort((a, b) => b[1] - a[1]);
    const taught = subj.meta.chapters.filter((c) => c.slides).map((c) => c.id);
    const taughtN = exam.filter((q) => taught.includes(q.chapter)).length;
    const neg = exam.filter((q) => q.pattern === '選錯誤（否定）題').length;
    const en = exam.filter((q) => /^[A-Za-z]/.test(q.stem)).length;
    $app.innerHTML = `
      <div class="crumbs"><a href="#/s/${sid}">${esc(subj.meta.title)}</a> / 考題分析</div>
      <h1>📊 考題分析</h1>
      <p class="muted">統計 ${srcs.join('、')} 共 <b>${exam.length}</b> 題。考點標籤是依題目關鍵字自動歸類，再人工校正。</p>
      <div class="stat-row">
        <div class="stat"><b>${exam.length}</b><span>考古總題數</span></div>
        <div class="stat"><b>${taughtN}</b><span>已上課章節的考古題</span></div>
        <div class="stat"><b>${Math.round((neg / exam.length) * 100)}%</b><span>「選錯誤」否定題</span></div>
        <div class="stat"><b>${Math.round((en / exam.length) * 100)}%</b><span>英文題幹</span></div>
      </div>
      <div class="card" style="margin-top:14px"><h2 style="margin-top:0">各章考古題數</h2>
        <div class="legend">${srcs.map((s) => `<span><i style="background:${srcColor(s)}"></i>${esc(s)}</span>`).join('')}</div>
        ${barsHTML(chRows)}</div>
      <div class="grid cols-2" style="margin-top:14px">
        <div class="card"><h2 style="margin-top:0">🔥 最常考的考點 Top 20</h2>${barsHTML(topics)}</div>
        <div class="card"><h2 style="margin-top:0">題型分布</h2>${barsHTML(patterns, 0, '#8a5cc2')}
          <h3>出題模式觀察</h3>
          <ul class="small">
            <li><b>同一概念換句話重複出</b>：補體 C3 convertase、MAC、TLR4–LPS、IgA／IgE 情境等在同一份考古中出現 5–10 次，熟練一題等於拿下一整組。</li>
            <li><b>否定題比例高</b>：約三成題目問「何者錯誤／NOT」，選項常把兩個正確概念互換（fimbriae↔flagella、G+↔G−、C3a↔C3b）。</li>
            <li><b>老師課堂題會原題出現</b>：李岳倫老師 slides 上的題目幾乎一字不差出現在 111、113 考古。</li>
            <li><b>各論以臨床情境 + 實驗室鑑別為主</b>：catalase／溶血／CAMP／optochin／乳糖發酵。</li>
            <li><b>真菌章有約 10 題看圖題</b>（孢子、皮癬菌大孢子）→ 搭配課本圖譜複習。</li>
          </ul></div>
      </div>
      <div class="card" style="margin-top:14px"><h2 style="margin-top:0">各章考點分析</h2>
        <div class="grid cols-3">${subj.meta.chapters.map((c) => `<a href="#/s/${sid}/c/${c.id}/exam">${c.idx}. ${esc(c.title)}</a>`).join('')}</div></div>`;
  }

  // ------------------------------------------------------------ report
  async function pageReport(q) {
    let subj = null;
    if (q.sid) { try { subj = await loadSubject(q.sid); } catch { subj = null; } }
    setNav(subj ? q.sid : null, 'report');
    const qq = subj && q.qid ? subj.questions.find((x) => x.id === q.qid) : null;
    const repo = CFG.githubRepo;
    $app.innerHTML = `
      <h1>⚠️ 問題回報</h1>
      <p class="muted">發現答案錯誤、詳解有誤、錯字或網站 bug？填寫下方表單後會開啟 GitHub Issue（需要 GitHub 帳號）。沒有帳號的話，可以按「複製內容」傳給網站維護者。</p>
      <form class="card filters" id="rf">
        <div class="grid cols-2">
          <label class="field">類型<select name="type">
            <option>答案錯誤</option><option>詳解有誤或不清楚</option><option>題目文字錯誤 / 缺漏</option>
            <option>重點整理內容錯誤</option><option>網站功能 bug</option><option>建議 / 其他</option></select></label>
          <label class="field">位置<input type="text" name="where" value="${esc(q.where || '')}" placeholder="例如：先天免疫／重點整理，或題號 k113-innate-02"></label>
        </div>
        ${qq ? `<div class="note"><b>回報題目：</b>${esc(qq.source)} ${esc(qq.id)}<br>${esc(qq.stem.slice(0, 200))}${qq.stem.length > 200 ? '…' : ''}<br><span class="muted">目前答案：${(qq.answer || []).join('/') || '—'}</span></div>` : ''}
        <label class="field">說明（你認為正確的內容、出處或頁碼）<textarea name="desc" required placeholder="例如：應該選 (C)，因為…（上課 slides p.25）"></textarea></label>
        <div class="row"><button class="btn primary" type="submit">送出到 GitHub Issues</button>
          <button class="btn" type="button" id="copyBtn">📋 複製內容</button><span class="spacer"></span>
          ${repo ? `<a class="small" href="https://github.com/${esc(repo)}/issues" target="_blank" rel="noopener">查看已回報的問題 ↗</a>` : ''}</div>
      </form>`;
    const form = document.getElementById('rf');
    const compose = () => {
      const fd = new FormData(form);
      const type = fd.get('type'), where = fd.get('where'), desc = fd.get('desc');
      const title = `[${type}] ${qq ? qq.id : (where || '一般回報')}`;
      const body = [
        `**類型**：${type}`,
        `**科目**：${subj ? subj.meta.title : '—'}`,
        `**位置**：${where || '—'}`,
        qq ? `**題號**：${qq.id}（${qq.source}）\n**題目**：${qq.stem}\n**選項**：\n${(qq.options || []).map((o) => `- (${o.k}) ${o.t}`).join('\n')}\n**網站目前答案**：${(qq.answer || []).join('/') || '—'}` : '',
        `\n**說明**：\n${desc}`,
        `\n---\n頁面：${location.href}`,
      ].filter(Boolean).join('\n');
      return { title, body, type };
    };
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!repo) return toast('尚未設定 GitHub repo（config.js）');
      const { title, body } = compose();
      const url = `https://github.com/${repo}/issues/new?${new URLSearchParams({ title, body, labels: 'report' })}`;
      window.open(url, '_blank', 'noopener');
    });
    document.getElementById('copyBtn').onclick = async () => {
      const { title, body } = compose();
      try { await navigator.clipboard.writeText(`${title}\n\n${body}`); toast('已複製，可以貼給維護者'); }
      catch { toast('複製失敗，請手動選取文字'); }
    };
  }

  route();
})();
