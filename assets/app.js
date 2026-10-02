/* Study Hub — 靜態多科目複習站（無需 build，直接放 GitHub Pages）
 * 路由：
 *   #/                               首頁
 *   #/practice                       練習區：先選科目
 *   #/s/:sid                         科目總覽
 *   #/s/:sid/c/:cid/:tab             章節（summary | slides | exam | practice）
 *   #/s/:sid/practice?...            練習設定 / 作答（start=1）/ 瀏覽（view=browse）
 *   #/s/:sid/q/:qid                  單題
 *   #/s/:sid/analysis                考題分析
 *   #/s/:sid/sheet[/figs]            速記表 / 觀念圖庫
 *   #/report?...                     回報 / 回饋
 */
(() => {
  "use strict";
  const CFG = window.STUDY_HUB_CONFIG || {};
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const $app = $("#app");
  const REDUCED = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const IS_MAC = /Mac|iPhone|iPad/.test(
    navigator.platform || navigator.userAgent,
  );
  const IS_TOUCH = matchMedia("(hover: none)").matches;

  // ------------------------------------------------------------ icons (stroke, 24 grid)
  const P = {
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    arrowR: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    arrowL: '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    arrowUR: '<path d="M7 17 17 7M8 7h9v9"/>',
    chevR: '<path d="m9 6 6 6-6 6"/>',
    check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    x: '<path d="M6 6l12 12M18 6 6 18"/>',
    book: '<path d="M2 5h7a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H2zM22 5h-7a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h8z"/>',
    chart: '<path d="M4 20V11M10 20V5M16 20v-6M21 20H3"/>',
    pen: '<path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"/>',
    flag: '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    star: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
    shuffle: '<path d="M16 3h5v5M4 20 21 3M21 16v5h-5M15 15l6 6M4 4l5 5"/>',
    list: '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    alert: '<circle cx="12" cy="12" r="9"/><path d="M12 8v4.5M12 16h.01"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    git: '<circle cx="6" cy="6" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="8" r="2.2"/><path d="M6 8.2v7.6M18 10.2c0 4-6 3-10.4 6.2"/>',
    chat: '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    copy: '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h8"/>',
    target:
      '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r=".8"/>',
    home: '<path d="M3 10.5 12 3l9 7.5V21H3z"/><path d="M9.5 21v-6h5v6"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    flame:
      '<path d="M12 3c1 4 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3.5 2-4.5 0 2 1 3 2 3 0-3-1-5 1-8.5z"/>',
    rotate: '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
    eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    file: '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4M9 13h6M9 17h6"/>',
    slides:
      '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.7M12 17h.01"/>',
    tag: '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.3"/>',
    trash: '<path d="M4 7h16M9 7V4h6v3M6 7l1 14h10l1-14"/>',
    bolt: '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    expand: '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
    image:
      '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 17-5-5-9 8"/>',
    cards:
      '<rect x="7" y="3" width="13" height="16" rx="2"/><path d="M4 7v12a2 2 0 0 0 2 2h9"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    printer:
      '<path d="M7 9V3h10v6M7 17H4v-7h16v7h-3"/><rect x="7" y="14" width="10" height="7"/>',
    minus: '<path d="M5 12h14"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
  };
  const ic = (n, cls = "") =>
    `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${P[n] || ""}</svg>`;
  const icFill = (n) =>
    `<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true">${P[n]}</svg>`;

  // ------------------------------------------------------------ utils
  const esc = (s) =>
    String(s ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const store = {
    get(k, d) {
      try {
        const v = localStorage.getItem(k);
        return v ? JSON.parse(v) : d;
      } catch {
        return d;
      }
    },
    set(k, v) {
      try {
        localStorage.setItem(k, JSON.stringify(v));
      } catch {
        /* private mode */
      }
    },
  };
  const shuffle = (a) => {
    a = a.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };
  const countBy = (arr, f) => {
    const m = new Map();
    for (const x of arr)
      for (const k of [].concat(f(x))) m.set(k, (m.get(k) || 0) + 1);
    return m;
  };
  const pct = (a, b) => (b ? Math.round((a / b) * 100) : 0);
  const pad2 = (n) => String(n).padStart(2, "0");
  const hash = (s) => {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return (h >>> 0) / 4294967295;
  };
  const qs = (o) =>
    new URLSearchParams(
      Object.entries(o).filter(
        ([, v]) => v !== undefined && v !== null && v !== "",
      ),
    ).toString();
  const toast = (msg) => {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(t._h);
    t._h = setTimeout(() => t.classList.remove("show"), 2000);
  };
  const fetchJSON = async (u) => {
    const r = await fetch(u, { cache: "no-cache" });
    if (!r.ok) throw new Error(`${u}：${r.status}`);
    return r.json();
  };
  const fetchText = async (u) => {
    const r = await fetch(u, { cache: "no-cache" });
    if (!r.ok) throw new Error(`${u}：${r.status}`);
    return r.text();
  };
  const cssVar = (n) =>
    getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const fmtTime = (ms) => {
    const s = Math.floor(ms / 1000);
    return `${Math.floor(s / 60)}:${pad2(s % 60)}`;
  };

  // ------------------------------------------------------------ theme
  const themeBtn = $("#themeBtn");
  const currentTheme = () =>
    document.documentElement.getAttribute("data-theme") ||
    (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  const paintThemeBtn = () => {
    themeBtn.innerHTML = ic(currentTheme() === "dark" ? "sun" : "moon");
  };
  paintThemeBtn();
  themeBtn.addEventListener("click", () => {
    const next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    store.set("sh:theme", next);
    paintThemeBtn();
    window.dispatchEvent(new Event("themechange"));
  });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    paintThemeBtn();
    window.dispatchEvent(new Event("themechange"));
  });
  $("#kbdHint").textContent = IS_MAC ? "⌘ K" : "Ctrl K";
  if (CFG.githubRepo)
    $("#repoLink").href = `https://github.com/${CFG.githubRepo}`;

  // masthead shadow + reading progress
  const onScroll = () => {
    $("#masthead").classList.toggle("scrolled", scrollY > 4);
    const rp = $("#readProgress");
    if (document.body.dataset.reading === "1") {
      const h = document.documentElement.scrollHeight - innerHeight;
      rp.style.width = `${h > 0 ? Math.min(100, (scrollY / h) * 100) : 0}%`;
    } else rp.style.width = "0";
  };
  addEventListener("scroll", onScroll, { passive: true });

  // ------------------------------------------------------------ data
  const DB = { index: null, subjects: {} };
  async function loadIndex() {
    if (!DB.index) DB.index = await fetchJSON("subjects/index.json");
    return DB.index;
  }
  async function loadSubject(sid) {
    if (DB.subjects[sid]) return DB.subjects[sid];
    const idx = await loadIndex();
    const ent = idx.find((x) => x.id === sid);
    if (!ent) throw new Error(`找不到科目「${sid}」`);
    const meta = await fetchJSON(`${ent.path}/subject.json`);
    const lists = await Promise.all(
      (meta.questionFiles || []).map((f) =>
        fetchJSON(`${ent.path}/${f}`).catch(() => []),
      ),
    );
    const questions = lists.flat();
    const figs = await fetchJSON(`${ent.path}/figures.json`).catch(() => []);
    const chMap = Object.fromEntries(
      meta.chapters.map((c, i) => [c.id, { ...c, idx: i + 1 }]),
    );
    const qById = Object.fromEntries(questions.map((q) => [q.id, q]));
    return (DB.subjects[sid] = {
      meta,
      path: ent.path,
      questions,
      qById,
      chMap,
      figs,
      figById: (() => {
        let n = 0;
        return Object.fromEntries(
          figs.map((f) => [f.id, { ...f, n: f.type === "slide" ? 0 : ++n }]),
        );
      })(),
      content: {},
    });
  }
  async function loadAllSubjects() {
    const idx = await loadIndex();
    return (
      await Promise.all(idx.map((x) => loadSubject(x.id).catch(() => null)))
    ).filter(Boolean);
  }
  async function loadContent(subj, cid) {
    if (subj.content[cid]) return subj.content[cid];
    let raw = "";
    try {
      raw = await fetchText(`${subj.path}/content/${cid}.md`);
    } catch {
      raw = "";
    }
    const parts = { summary: "", slides: "", exam: "" };
    let cur = "summary";
    for (const line of raw.split("\n")) {
      const m = line.match(/^===\s*(\w+)\s*===\s*$/);
      if (m) {
        cur = m[1];
        parts[cur] = parts[cur] || "";
        continue;
      }
      parts[cur] = (parts[cur] || "") + line + "\n";
    }
    return (subj.content[cid] = parts);
  }

  // progress
  const K = {
    prog: (s) => `sh:${s}:progress`,
    star: (s) => `sh:${s}:stars`,
    read: (s) => `sh:${s}:read`,
    last: (s) => `sh:${s}:lastChapter`,
  };
  const getProg = (sid) => store.get(K.prog(sid), {});
  const record = (sid, qid, ok) => {
    const p = getProg(sid);
    const r = p[qid] || { c: 0, w: 0 };
    ok ? r.c++ : r.w++;
    r.last = ok ? "c" : "w";
    r.t = Date.now();
    p[qid] = r;
    store.set(K.prog(sid), p);
  };
  const getStars = (sid) => new Set(store.get(K.star(sid), []));
  const toggleStar = (sid, qid) => {
    const s = getStars(sid);
    s.has(qid) ? s.delete(qid) : s.add(qid);
    store.set(K.star(sid), [...s]);
    return s.has(qid);
  };
  const getRead = (sid) => new Set(store.get(K.read(sid), []));

  // 題目來源：每個科目可在 subject.json 的 "sources" 自訂；沒寫就用下面的預設。
  // kind：exam（考古）、class（課堂題）、new（模擬新題）
  const DEFAULT_SOURCES = [
    { key: "k113", label: "113 考古", kind: "exam", pill: "violet" },
    { key: "k111", label: "111 期中考古", kind: "exam", pill: "line" },
    { key: "class", label: "2026 課堂題", kind: "class", pill: "warn" },
    { key: "new", label: "模擬新題", kind: "new", pill: "good" },
  ];
  const SERIES = ["var(--series-1)", "var(--series-2)", "var(--ink-3)"];
  const sourcesOf = (subj) =>
    (subj?.meta?.sources || DEFAULT_SOURCES).map((s, i, all) => ({
      ...s,
      match: (q) => q.source === s.label,
      color:
        SERIES[all.filter((x) => x.kind === "exam").indexOf(s)] ||
        "var(--ink-3)",
    }));
  const srcKeys = (subj, kind) =>
    sourcesOf(subj)
      .filter((s) => s.kind === kind)
      .map((s) => s.key)
      .join(",");
  const srcColor = (subj, label) =>
    sourcesOf(subj).find((s) => s.label === label)?.color || "var(--ink-3)";
  const isExam = (q) => /考古/.test(q.source);
  const pillFor = (src) =>
    Object.values(DB.subjects)
      .flatMap((x) => sourcesOf(x))
      .concat(DEFAULT_SOURCES)
      .find((s) => s.label === src)?.pill || "line";

  function chapterStats(subj, cid) {
    const list = subj.questions.filter(
      (q) => q.chapter === cid && !q.imageOnly,
    );
    const prog = getProg(subj.meta.id);
    let done = 0,
      right = 0,
      wrong = 0;
    for (const q of list) {
      const r = prog[q.id];
      if (r) {
        done++;
        r.last === "c" ? right++ : wrong++;
      }
    }
    const exam = subj.questions.filter(
      (q) => q.chapter === cid && isExam(q),
    ).length;
    return {
      total: list.length,
      done,
      right,
      wrong,
      exam,
      mastery: pct(right, list.length),
    };
  }
  function subjectStats(subj) {
    const list = subj.questions.filter((q) => !q.imageOnly);
    const prog = getProg(subj.meta.id);
    let done = 0,
      right = 0,
      wrong = 0;
    for (const q of list) {
      const r = prog[q.id];
      if (r) {
        done++;
        r.last === "c" ? right++ : wrong++;
      }
    }
    return { total: list.length, done, right, wrong, acc: pct(right, done) };
  }

  // ------------------------------------------------------------ chrome
  function setChrome(sid, active) {
    const nav = $("#mainnav");
    const last = sid || store.get("sh:lastSubject", null) || DB.index?.[0]?.id;
    const cur = (k) => (active === k ? ' aria-current="page"' : "");
    if (sid) {
      store.set("sh:lastSubject", sid);
      const s = DB.subjects[sid];
      nav.innerHTML = `<a href="#/">所有科目</a><a href="#/s/${sid}"${cur("subject")}>${esc(s?.meta.short || "總覽")}總覽</a><a href="#/s/${sid}/practice"${cur("practice")}>練習區</a><a href="#/s/${sid}/analysis"${cur("analysis")}>考題分析</a><a href="#/s/${sid}/sheet"${cur("sheet")}>速記・圖解</a><a href="#/report?sid=${sid}"${cur("report")}>回報 / 回饋</a>`;
    } else {
      nav.innerHTML = `<a href="#/"${cur("home")}>所有科目</a><a href="#/practice"${cur("practice")}>練習區</a><a href="#/report"${cur("report")}>回報 / 回饋</a>`;
    }
    const tb = $("#tabbar");
    const T = (href, icon, label, k) =>
      `<a href="${href}"${cur(k)}>${ic(icon)}<span>${label}</span></a>`;
    tb.innerHTML = last
      ? T(
          sid ? `#/s/${sid}` : "#/",
          "home",
          sid ? "總覽" : "首頁",
          sid ? "subject" : "home",
        ) +
        T(sid ? `#/s/${sid}/practice` : "#/practice", "pen", "練習", "practice") +
        T(`#/s/${last}/analysis`, "chart", "分析", "analysis") +
        T(`#/s/${last}/sheet`, "grid", "速記", "sheet") +
        `<a href="#" data-open-search>${ic("search")}<span>搜尋</span></a>`
      : "";
    const s = tb.querySelector("[data-open-search]");
    if (s)
      s.addEventListener("click", (e) => {
        e.preventDefault();
        openPalette();
      });
    document.body.dataset.reading = active === "reading" ? "1" : "0";
    onScroll();
  }

  // ------------------------------------------------------------ router
  let cleanup = [];
  const onLeave = (fn) => cleanup.push(fn);
  function parseHash() {
    const h = location.hash.replace(/^#/, "") || "/";
    const [path, q] = h.split("?");
    return {
      seg: path.split("/").filter(Boolean).map(decodeURIComponent),
      q: Object.fromEntries(new URLSearchParams(q || "")),
    };
  }
  function render(html, mount) {
    $app.innerHTML = `<div class="enter">${html}</div>`;
    enhanceProse($app);
    mount?.();
  }
  async function route() {
    cleanup.forEach((f) => {
      try {
        f();
      } catch {
        /* */
      }
    });
    cleanup = [];
    hideTip();
    closeFigZoom(true);
    const { seg, q } = parseHash();
    const keepScroll = q.keep === "1";
    if (!keepScroll) scrollTo({ top: 0 });
    try {
      await loadIndex();
      if (!seg.length) return await pageHome();
      if (seg[0] === "report") return await pageReport(q);
      if (seg[0] === "practice") return await pagePracticePick();
      if (seg[0] === "s" && seg[1]) {
        const sid = seg[1];
        if (seg.length === 2) return await pageSubject(sid);
        if (seg[2] === "c" && seg[3])
          return await pageChapter(sid, seg[3], seg[4] || "summary", q);
        if (seg[2] === "sheet") return await pageSheet(sid, seg[3] || "", q);
        if (seg[2] === "practice") return await pagePractice(sid, q);
        if (seg[2] === "analysis") return await pageAnalysis(sid);
        if (seg[2] === "q" && seg[3]) {
          const subj = await loadSubject(sid);
          setChrome(sid, "practice");
          const one = subj.qById[seg[3]];
          return runSession(subj, one ? [one] : [], { single: 1 });
        }
      }
      setChrome(null, "");
      render(
        emptyState(
          "找不到這一頁",
          "網址可能打錯了，或這個頁面已經移動。",
          `<a class="btn primary" href="#/">${ic("home")}回首頁</a>`,
        ),
      );
    } catch (e) {
      console.error(e);
      setChrome(null, "");
      render(
        emptyState(
          "載入失敗",
          `錯誤訊息：<span class="mono">${esc(e.message)}</span><br>剛更新網站時，瀏覽器可能還留著舊版檔案，請按「重新載入」或 <kbd>Ctrl</kbd>/<kbd>⌘</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>。如果是直接雙擊 index.html 開啟，請改用 GitHub Pages 網址或執行 python3 -m http.server。`,
          `<button class="btn primary" type="button" onclick="location.reload()">重新載入</button> <a class="btn" href="#/">回首頁</a>`,
        ),
      );
    }
  }
  addEventListener("hashchange", route);
  const emptyState = (title, text, actions = "") =>
    `<div class="wrap"><div class="card empty" style="margin-top:48px"><div class="eyebrow">Study Hub</div><h1 class="display">${title}</h1><p>${text}</p>${actions}</div></div>`;

  // ------------------------------------------------------------ markdown enhancement
  const slug = (s, i) =>
    `h-${i}-${s.replace(/[^\w\u4e00-\u9fff]+/g, "-").slice(0, 40)}`;
  function mdToHTML(text) {
    return window.marked
      ? window.marked.parse(text || "")
      : `<pre>${esc(text)}</pre>`;
  }
  function enhanceProse(root) {
    $$(".prose", root).forEach((p) => {
      $$("table", p).forEach((t) => {
        if (!t.parentElement.classList.contains("table-scroll")) {
          const w = document.createElement("div");
          w.className = "table-scroll";
          t.replaceWith(w);
          w.appendChild(t);
        }
      });
      $$("h2, h3", p).forEach((h, i) => {
        h.id = slug(h.textContent, i);
      });
    });
  }

  // ------------------------------------------------------------ tooltip (charts)
  const tip = $("#tip");
  function showTip(html, x, y) {
    tip.innerHTML = html;
    tip.classList.add("show");
    const r = tip.getBoundingClientRect();
    let left = x + 14,
      top = y + 14;
    if (left + r.width > innerWidth - 8) left = x - r.width - 14;
    if (top + r.height > innerHeight - 8) top = y - r.height - 14;
    left = Math.max(8, Math.min(left, innerWidth - r.width - 8));
    top = Math.max(8, top);
    tip.style.left = `${left}px`;
    tip.style.top = `${top}px`;
  }
  function hideTip() {
    tip.classList.remove("show");
  }
  function bindTips(root) {
    $$("[data-tip]", root).forEach((el) => {
      const h = () => el.getAttribute("data-tip");
      el.addEventListener("pointermove", (e) =>
        showTip(h(), e.clientX, e.clientY),
      );
      el.addEventListener("pointerleave", hideTip);
      el.addEventListener("focus", () => {
        const r = el.getBoundingClientRect();
        showTip(h(), r.left + r.width / 2, r.bottom);
      });
      el.addEventListener("blur", hideTip);
    });
  }

  addEventListener("scroll", hideTip, { passive: true });

  // ------------------------------------------------------------ figures
  // 觀念圖是手繪 SVG（subjects/<sid>/figures/<id>.svg），以 inline 方式插入，
  // 顏色全部走 CSS 變數，所以會跟著深淺色模式切換。
  // Markdown 內用 <div data-fig="id"></div> 插圖；清單與說明在 figures.json。
  const svgCache = new Map();
  function fetchSVG(subj, id) {
    const k = `${subj.path}/figures/${id}.svg`;
    if (!svgCache.has(k))
      svgCache.set(
        k,
        fetchText(k).catch((e) => {
          svgCache.delete(k);
          throw e;
        }),
      );
    return svgCache.get(k);
  }
  const figHint = () =>
    `<span class="hint"><i></i>虛線底線的名詞可以${IS_TOUCH ? "點一下" : "滑過"}看說明</span>`;
  const isSlide = (f) => f?.type === "slide";
  const figLabel = (f) =>
    isSlide(f) ? `Slides · p.${f.page}` : `Fig. ${pad2(f.n)}`;
  const slideImg = (subj, f, cls = "") =>
    `<img class="${cls}" src="${esc(subj.path)}/${esc(f.src)}" width="${f.w || 1400}" height="${f.h || 788}" loading="lazy" decoding="async" alt="${esc(`上課投影片：${f.title}（${f.deck} 第 ${f.page} 頁）`)}">`;
  const slideCaption = (f) =>
    `${f.caption ? `${f.caption} ` : ""}<span class="src">出自上課 slides <span class="mono">${esc(f.deck)}</span> page ${esc(f.page)}</span>`;
  function figureHTML(subj, id) {
    const f = subj.figById?.[id];
    if (!f) return "";
    const slide = isSlide(f);
    return `<figure class="fig${slide ? " fig-slide" : ""}" data-fig-id="${esc(id)}" data-sid="${esc(subj.meta.id)}">
      <div class="fig-head"><span class="eyebrow">${figLabel(f)}</span><b>${esc(f.title)}</b><button class="btn sm ghost" type="button" data-zoom="${esc(id)}" aria-label="放大「${esc(f.title)}」">${ic("expand")}<span class="hide-s">放大</span></button></div>
      ${slide ? `<div class="fig-body">${slideImg(subj, f)}</div>` : `<div class="fig-body loading" data-src="${esc(id)}"></div>`}
      <figcaption>${slide ? slideCaption(f) : `${f.caption || ""} ${figHint()}`}</figcaption></figure>`;
  }
  async function hydrateFigs(root, subj) {
    $$("[data-fig]", root).forEach((el) => {
      const h = figureHTML(subj, el.getAttribute("data-fig"));
      if (h) el.outerHTML = h;
      else el.remove();
    });
    await Promise.all(
      $$(".fig-body[data-src]", root).map(async (b) => {
        const id = b.dataset.src;
        b.removeAttribute("data-src");
        try {
          b.innerHTML = await fetchSVG(subj, id);
          // 圖庫縮圖整張是一顆按鈕：裡面不能再有可聚焦元素
          if (b.closest(".thumb"))
            $("svg", b)?.setAttribute("aria-hidden", "true");
          else prepSVG(b);
        } catch {
          b.innerHTML =
            '<p class="small muted" style="padding:24px;margin:0">這張圖載入失敗，請重新整理頁面。</p>';
        }
        b.classList.remove("loading");
      }),
    );
  }
  function prepSVG(root) {
    const svg = $("svg", root);
    if (!svg) return;
    const hots = $$(".hot", svg);
    if (hots.length) svg.setAttribute("role", "group");
    hots.forEach((g) => {
      const note = g.getAttribute("data-tip") || "";
      const label = (
        g.getAttribute("data-label") ||
        $("text", g)?.textContent ||
        ""
      ).trim();
      g.setAttribute("tabindex", "0");
      g.setAttribute("role", "button");
      // 虛線底線（SVG 文字不支援 dashed text-decoration，所以自己畫）
      const t = $("text:not(.nou)", g);
      if (t && !$(".uline", g)) {
        try {
          const bb = t.getBBox();
          const ln = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "path",
          );
          ln.setAttribute("class", "uline");
          ln.setAttribute("d", `M${bb.x} ${bb.y + bb.height - 1}h${bb.width}`);
          g.appendChild(ln);
        } catch {
          /* not rendered yet */
        }
      }
      g.setAttribute("aria-label", `${label}：${note.replace(/<[^>]+>/g, "")}`);
      g.setAttribute(
        "data-tip",
        `${label ? `<b>${esc(label)}</b><br>` : ""}${note}`,
      );
      g.addEventListener("click", (e) => {
        e.stopPropagation();
        const r = g.getBoundingClientRect();
        showTip(g.getAttribute("data-tip"), r.left + r.width / 2, r.bottom);
      });
      g.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          g.dispatchEvent(new Event("focus"));
        }
      });
    });
    bindTips(svg);
  }
  document.addEventListener("pointerdown", (e) => {
    if (!e.target.closest?.(".hot")) hideTip();
  });

  // zoom view
  let zoom = null;
  function closeFigZoom(silent) {
    if (!zoom) return;
    zoom.el.remove();
    removeEventListener("keydown", zoom.onKey);
    document.documentElement.style.overflow = "";
    const back = zoom.back;
    zoom = null;
    hideTip();
    if (!silent) back?.focus?.();
  }
  async function openFigZoom(subj, id, back) {
    const f = subj.figById?.[id];
    if (!f) return;
    closeFigZoom(true);
    const el = document.createElement("div");
    el.className = "figzoom";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-label", f.title);
    el.innerHTML = `<div class="figzoom-bar"><span class="eyebrow hide-s">${figLabel(f)}</span><b>${esc(f.title)}</b><span class="spacer"></span>
      <button class="btn sm" type="button" data-z="-1" aria-label="縮小">${ic("minus")}</button><span class="num" aria-live="polite">100%</span><button class="btn sm" type="button" data-z="1" aria-label="放大">${ic("plus")}</button>
      <button class="btn sm primary" type="button" data-close aria-label="關閉">${ic("x")}<span class="hide-s">關閉</span></button></div>
      <div class="figzoom-stage"><div class="fig-body" style="padding:0;overflow:visible"></div></div>
      <div class="figzoom-cap">${isSlide(f) ? slideCaption(f) : `${f.caption || ""} ${figHint()}`}</div>`;
    document.body.appendChild(el);
    document.documentElement.style.overflow = "hidden";
    const steps = [0.6, 0.8, 1, 1.25, 1.5, 2, 2.5, 3];
    let k = 2;
    const stage = $(".figzoom-stage", el);
    const body = $(".fig-body", el);
    const apply = () => {
      const svg = $("svg, img", body);
      if (!svg) return;
      const natural = isSlide(f)
        ? f.w || 1400
        : (svg.viewBox?.baseVal?.width || 900) * 1.5;
      // 手機上 SVG 預設畫到接近原始寬度，字才看得清楚，左右滑動看全圖
      const fit = isSlide(f)
        ? Math.min(stage.clientWidth - 8, natural)
        : Math.max(
            Math.min(stage.clientWidth - 8, natural),
            Math.min(natural / 1.5, 720),
          );
      svg.style.width = `${Math.round(fit * steps[k])}px`;
      svg.style.minWidth = "0";
      svg.style.maxWidth = "none";
      $(".num", el).textContent = `${Math.round(steps[k] * 100)}%`;
    };
    const onKey = (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        closeFigZoom();
      } else if (e.key === "+" || e.key === "=") {
        k = Math.min(steps.length - 1, k + 1);
        apply();
      } else if (e.key === "-") {
        k = Math.max(0, k - 1);
        apply();
      } else if (e.key === "Tab") {
        const f = $$("button, [tabindex='0']", el);
        const i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) {
          e.preventDefault();
          f[f.length - 1].focus();
        } else if (!e.shiftKey && i === f.length - 1) {
          e.preventDefault();
          f[0].focus();
        }
      }
    };
    zoom = { el, onKey, back };
    addEventListener("keydown", onKey);
    el.addEventListener("click", (e) => {
      const z = e.target.closest("[data-z]");
      if (z) {
        k = Math.max(0, Math.min(steps.length - 1, k + +z.dataset.z));
        apply();
      }
      if (e.target.closest("[data-close]")) closeFigZoom();
    });
    $("[data-close]", el).focus();
    try {
      if (isSlide(f)) {
        body.innerHTML = slideImg(subj, f);
        $("img", body).loading = "eager";
      } else {
        body.innerHTML = await fetchSVG(subj, id);
        prepSVG(body);
      }
      apply();
    } catch {
      body.innerHTML = '<p class="muted">這張圖載入失敗。</p>';
    }
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-zoom]");
    if (!b) return;
    const sid = b.closest("[data-sid]")?.dataset.sid;
    const subj = sid && DB.subjects[sid];
    if (subj) openFigZoom(subj, b.dataset.zoom, b);
  });

  // 題目 → 相關觀念圖（依考點比對，同章節優先）
  function figsFor(subj, q) {
    const tops = new Set(q.topics || []);
    return (subj.figs || [])
      .filter((f) => (f.topics || []).some((t) => tops.has(t)))
      .sort(
        (a, b) =>
          isSlide(a) - isSlide(b) ||
          (b.chapter === q.chapter) - (a.chapter === q.chapter),
      )
      .filter((f, i, arr) => !isSlide(f) || arr.indexOf(f) < 3)
      .slice(0, 3);
  }
  const figLinks = (subj, q) =>
    figsFor(subj, q)
      .map(
        (f) =>
          `<details class="fig-inline" data-sid="${esc(subj.meta.id)}" data-lazy-fig="${esc(f.id)}"><summary>${ic(isSlide(f) ? "slides" : "image")}${isSlide(f) ? "看上課 slides" : "看觀念圖"}：${esc(f.title)}</summary></details>`,
      )
      .join("");
  document.addEventListener(
    "toggle",
    (e) => {
      const d = e.target;
      if (!d.matches?.("details[data-lazy-fig]") || !d.open) return;
      const subj = DB.subjects[d.dataset.sid];
      if (!subj) return;
      const id = d.dataset.lazyFig;
      d.removeAttribute("data-lazy-fig");
      d.insertAdjacentHTML("beforeend", figureHTML(subj, id));
      hydrateFigs(d, subj);
    },
    true,
  );

  /** Horizontal bar chart. rows: [{label, segs:[{v, color, name}], href?}] */
  function barChart(rows, { series = null, tableCaption = "" } = {}) {
    const max = Math.max(
      1,
      ...rows.map((r) => r.segs.reduce((a, s) => a + s.v, 0)),
    );
    const legend =
      series && series.length > 1
        ? `<div class="legend">${series.map((s) => `<span><i style="background:${s.color}"></i>${esc(s.name)}</span>`).join("")}</div>`
        : "";
    const body = rows
      .map((r) => {
        const total = r.segs.reduce((a, s) => a + s.v, 0);
        const tipHtml = `<b>${esc(r.label)}</b>${r.segs.map((s) => `<div class="row">${series && series.length > 1 ? `<i style="background:${s.color}"></i>${esc(s.name)}：` : ""}${s.v} 題</div>`).join("")}${series && series.length > 1 ? `<div class="row" style="opacity:.7">合計 ${total} 題</div>` : ""}`;
        const segs = r.segs.filter((s) => s.v > 0);
        const track = `<span class="track" style="width:${(total / max) * 100}%">${segs.map((s) => `<i style="flex:${s.v};background:${s.color}"></i>`).join("")}</span>`;
        const tag = r.href ? "a" : "div";
        return `<${tag} class="chart-row" ${r.href ? `href="${r.href}"` : ""} tabindex="0" data-tip="${esc(tipHtml)}" style="color:inherit;text-decoration:none"><span class="lab">${esc(r.label)}</span><span style="display:block">${track}</span><span class="val">${total}</span></${tag}>`;
      })
      .join("");
    const cols =
      series && series.length > 1 ? series.map((s) => s.name) : ["題數"];
    const table = `<details class="data-table"><summary>以表格檢視${tableCaption ? `（${esc(tableCaption)}）` : ""}</summary><table><thead><tr><th>項目</th>${cols.map((c) => `<th>${esc(c)}</th>`).join("")}${cols.length > 1 ? "<th>合計</th>" : ""}</tr></thead><tbody>${rows.map((r) => `<tr><td>${esc(r.label)}</td>${r.segs.map((s) => `<td class="n">${s.v}</td>`).join("")}${cols.length > 1 ? `<td class="n">${r.segs.reduce((a, s) => a + s.v, 0)}</td>` : ""}</tr>`).join("")}</tbody></table></details>`;
    return `${legend}<div class="chart">${body}</div>${table}`;
  }

  // ------------------------------------------------------------ petri plate (signature visual)
  function mountPlate(canvas, colonies) {
    const ctx = canvas.getContext("2d");
    let W = 0,
      raf = 0,
      t0 = performance.now();
    const dpr = Math.min(2, devicePixelRatio || 1);
    const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
    const size = () => {
      const r = canvas.getBoundingClientRect();
      W = r.width;
      canvas.width = W * dpr;
      canvas.height = W * dpr;
    };
    const col = () => ({
      ink: cssVar("--ink"),
      ink3: cssVar("--ink-3"),
      rule: cssVar("--rule"),
      rs: cssVar("--rule-strong"),
      card: cssVar("--card"),
      p2: cssVar("--paper-2"),
      v: cssVar("--violet"),
      s: cssVar("--safranin"),
      g: cssVar("--good"),
    });
    let C = col();
    const onTheme = () => {
      C = col();
      if (!raf) draw(performance.now());
    };
    const draw = (now) => {
      const t = (now - t0) / 1000;
      pointer.x += (pointer.tx - pointer.x) * 0.06;
      pointer.y += (pointer.ty - pointer.y) * 0.06;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, W);
      const cx = W / 2,
        cy = W / 2,
        R = W * 0.47;
      // shadow + dish
      ctx.save();
      ctx.shadowColor = "rgba(0,0,0,.10)";
      ctx.shadowBlur = W * 0.06;
      ctx.shadowOffsetY = W * 0.025;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.fillStyle = C.card;
      ctx.fill();
      ctx.restore();
      const g = ctx.createRadialGradient(
        cx - R * 0.3 + pointer.x * 10,
        cy - R * 0.35 + pointer.y * 10,
        R * 0.05,
        cx,
        cy,
        R,
      );
      g.addColorStop(0, C.card);
      g.addColorStop(1, C.p2);
      ctx.beginPath();
      ctx.arc(cx, cy, R * 0.93, 0, Math.PI * 2);
      ctx.fillStyle = g;
      ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = C.rs;
      ctx.beginPath();
      ctx.arc(cx, cy, R, 0, Math.PI * 2);
      ctx.stroke();
      ctx.lineWidth = 1;
      ctx.strokeStyle = C.rule;
      ctx.beginPath();
      ctx.arc(cx, cy, R * 0.93, 0, Math.PI * 2);
      ctx.stroke();
      // ticks (lab markings)
      ctx.strokeStyle = C.rs;
      ctx.lineWidth = 1;
      for (let i = 0; i < 120; i++) {
        const a = (i / 120) * Math.PI * 2 - Math.PI / 2;
        const long = i % 10 === 0;
        const r1 = R * 0.955,
          r2 = R * (long ? 0.985 : 0.97);
        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1);
        ctx.lineTo(cx + Math.cos(a) * r2, cy + Math.sin(a) * r2);
        ctx.stroke();
      }
      // colonies (phyllotaxis spiral in order of time → grows outward)
      const n = colonies.length;
      const inner = R * 0.86;
      const golden = Math.PI * (3 - Math.sqrt(5));
      let alive = false;
      colonies.forEach((c, i) => {
        const k = (i + 0.5) / Math.max(n, 1);
        const rr = Math.sqrt(k) * inner * 0.96;
        const a = i * golden + c.j * 0.6;
        const x = cx + Math.cos(a) * rr + pointer.x * 6 * k,
          y = cy + Math.sin(a) * rr + pointer.y * 6 * k;
        const delay = REDUCED ? 0 : 0.25 + (i / Math.max(n, 1)) * 1.6;
        const dur = 0.9;
        const p = REDUCED ? 1 : Math.min(1, Math.max(0, (t - delay) / dur));
        if (p < 1) alive = true;
        const e = 1 - Math.pow(1 - p, 3);
        const breathe = REDUCED ? 1 : 1 + Math.sin(t * 1.2 + c.j * 9) * 0.03;
        const r = c.r * (W / 480) * e * breathe;
        if (r <= 0.2) return;
        const colr = c.kind === "c" ? C.v : c.kind === "w" ? C.s : C.ink3;
        ctx.globalAlpha = c.kind === "seed" ? 0.12 : 0.16;
        ctx.fillStyle = colr;
        ctx.beginPath();
        ctx.arc(x, y, r * 1.75, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = c.kind === "seed" ? 0.45 : 0.92;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 0.35;
        ctx.fillStyle = C.card;
        ctx.beginPath();
        ctx.arc(x - r * 0.3, y - r * 0.3, r * 0.32, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      });
      // glare
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, R * 0.93, 0, Math.PI * 2);
      ctx.clip();
      const gl = ctx.createLinearGradient(
        cx - R,
        cy - R,
        cx + R * 0.2,
        cy + R * 0.2,
      );
      gl.addColorStop(0, "rgba(255,255,255,.22)");
      gl.addColorStop(0.35, "rgba(255,255,255,0)");
      ctx.fillStyle = gl;
      ctx.fillRect(cx - R, cy - R, 2 * R, 2 * R);
      ctx.restore();
      const moving =
        Math.abs(pointer.tx - pointer.x) + Math.abs(pointer.ty - pointer.y) >
        0.002;
      raf =
        !REDUCED && (alive || moving || true) ? requestAnimationFrame(draw) : 0;
    };
    const onMove = (e) => {
      const r = canvas.getBoundingClientRect();
      pointer.tx = ((e.clientX - r.left) / r.width - 0.5) * 2;
      pointer.ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
    };
    const onLeaveP = () => {
      pointer.tx = 0;
      pointer.ty = 0;
    };
    const ro = new ResizeObserver(() => {
      size();
      if (!raf) draw(performance.now());
    });
    ro.observe(canvas);
    size();
    draw(performance.now());
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerleave", onLeaveP);
    addEventListener("themechange", onTheme);
    // pause when offscreen / tab hidden
    const io = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting && raf) {
        cancelAnimationFrame(raf);
        raf = 0;
      } else if (en.isIntersecting && !raf && !REDUCED)
        raf = requestAnimationFrame(draw);
    });
    io.observe(canvas);
    onLeave(() => {
      cancelAnimationFrame(raf);
      raf = 0;
      ro.disconnect();
      io.disconnect();
      removeEventListener("themechange", onTheme);
    });
  }
  function coloniesFromProgress(subs) {
    const out = [];
    for (const s of subs) {
      const p = getProg(s.meta.id);
      for (const [id, r] of Object.entries(p))
        out.push({
          t: r.t || 0,
          kind: r.last,
          r: 5 + Math.min(9, (r.c + r.w) * 1.6) + hash(id) * 4,
          j: hash(id + "j"),
        });
    }
    out.sort((a, b) => a.t - b.t);
    if (out.length >= 12) return out.slice(-420);
    const seeds = [];
    for (let i = 0; i < 70; i++)
      seeds.push({ kind: "seed", r: 3 + hash(`s${i}`) * 11, j: hash(`j${i}`) });
    return seeds.concat(out);
  }

  // ------------------------------------------------------------ pages: home
  async function pageHome() {
    const subs = await loadAllSubjects();
    setChrome(null, "home");
    const lastSid = store.get("sh:lastSubject", null) || subs[0]?.meta.id;
    const last = subs.find((s) => s.meta.id === lastSid) || subs[0];
    const totals = subs.reduce(
      (a, s) => {
        const st = subjectStats(s);
        a.done += st.done;
        a.right += st.right;
        a.wrong += st.wrong;
        return a;
      },
      { done: 0, right: 0, wrong: 0 },
    );
    const cards = subs
      .map((s) => {
        const st = subjectStats(s);
        return `<a class="card subject-card" href="#/s/${s.meta.id}">
        <div>
          <div class="eyebrow">${esc(s.meta.term || "Subject")}</div>
          <h3 class="display" style="margin-top:10px">${esc(s.meta.title)}</h3>
          <p class="muted small" style="margin:10px 0 0;max-width:40em">${esc(s.meta.description || "")}</p>
        </div>
        <span class="arrow" aria-hidden="true">${ic("arrowR")}</span>
        <div class="facts">
          <div class="fact"><b>${s.meta.chapters.length}</b><span>章節</span></div>
          <div class="fact"><b>${st.total}</b><span>練習題</span></div>
          <div class="fact"><b>${st.done}</b><span>已練習</span></div>
          <div class="fact"><b>${st.done ? `${st.acc}%` : "—"}</b><span>最近答對率</span></div>
        </div></a>`;
      })
      .join("");
    const hasPractice = totals.done > 0;
    render(
      `
      <section class="wrap hero">
        <div>
          <div class="eyebrow"><b>Study Hub</b> · 考前複習工作台</div>
          <h1 class="display h-xl">讀成<em>直覺</em></h1>
          <p class="lede">重點整理、上課 slides、考點分析和互動練習放在同一個地方。每答一題，右邊的培養皿就長出一顆菌落：紫色是答對，粉紅是還要再看的題目。</p>
          <div class="hero-actions">
            ${
              last
                ? `<a class="btn primary lg" href="${hasPractice ? `#/s/${last.meta.id}/practice` : "#/practice"}">${ic("pen")}${hasPractice ? "繼續練習" : "開始練習"}</a>
            <a class="btn lg" href="#/s/${last.meta.id}">${ic("book")}${esc(last.meta.short || last.meta.title)}總覽</a>`
                : ""
            }
          </div>
        </div>
        <figure class="plate-fig">
          <div class="plate-wrap"><canvas id="plate" role="img" aria-label="${hasPractice ? `你的練習菌落：已作答 ${totals.done} 題，其中 ${totals.right} 題答對、${totals.wrong} 題答錯` : "示意培養皿，開始練習後會依作答紀錄長出菌落"}"></canvas></div>
          <figcaption><span>${hasPractice ? `你的練習菌落 — 已作答 <b class="num">${totals.done}</b> 題` : ""}
            ${hasPractice ? `<span class="plate-legend"><span><i style="background:var(--violet)"></i>答對 ${totals.right}</span><span><i style="background:var(--safranin)"></i>答錯 ${totals.wrong}</span></span>` : ""}</span></figcaption>
        </figure>
      </section>

      <section class="wrap section">
        <div class="section-head"><div><div class="eyebrow">01 — 科目</div><h2 class="display h-m" style="margin-top:8px">選一個科目開始</h2></div></div>
        <div style="display:grid;gap:14px">${cards}</div>
      </section>

      <section class="wrap section">
        <div class="section-head"><div><div class="eyebrow">02 — 使用方式</div><h2 class="display h-m" style="margin-top:8px">從讀懂到答對</h2></div></div>
        <div class="steps">
          <div class="step"><div class="mono">01</div><h3>重點整理</h3><p>整合上課 slides 與共筆，表格化比較、標出陷阱。</p></div>
          <div class="step"><div class="mono">02</div><h3>上課 slides</h3><p>逐份 slides 的頁面重點，和老師的課堂題。</p></div>
          <div class="step"><div class="mono">03</div><h3>考點分析</h3><p>哪些考點最常考、用什麼方式考，一眼看出優先順序。</p></div>
          <div class="step"><div class="mono">04</div><h3>練習</h3><p>考古題、課堂題、模擬新題，即時詳解與錯題本。</p></div>
        </div>
      </section>`,
      () => {
        const cv = $("#plate");
        if (cv) mountPlate(cv, coloniesFromProgress(subs));
      },
    );
  }

  // ------------------------------------------------------------ pages: subject
  async function pageSubject(sid, sortMode) {
    const subj = await loadSubject(sid);
    setChrome(sid, "subject");
    const m = subj.meta;
    const st = subjectStats(subj);
    const sort = sortMode || store.get("sh:sort", "course");
    const read = getRead(sid);
    const stats = Object.fromEntries(
      m.chapters.map((c) => [c.id, chapterStats(subj, c.id)]),
    );
    const maxExam = Math.max(1, ...Object.values(stats).map((s) => s.exam));

    // next-up
    const lastCh = store.get(K.last(sid), null);
    const lastC = lastCh && subj.chMap[lastCh];
    const firstUnread =
      m.chapters.find((c) => c.slides && !read.has(c.id)) || m.chapters[0];
    const cont = subj.chMap[(lastC || firstUnread).id];
    const priority = m.chapters
      .map((c) => ({
        c,
        s: stats[c.id],
        score:
          stats[c.id].exam *
          (1 - stats[c.id].mastery / 100) *
          (c.slides ? 1.4 : 1),
      }))
      .filter((x) => x.s.total)
      .sort((a, b) => b.score - a.score)[0];
    const exam = m.examDate
      ? Math.ceil((new Date(m.examDate) - new Date()) / 864e5)
      : null;

    const row = (c) => {
      const s = stats[c.id];
      return `<a class="syl-row" href="#/s/${sid}/c/${c.id}/summary">
        <span class="idx">${pad2(c.idx)}</span>
        <span><span class="t">${esc(c.title)}</span>
          <span class="sub"><span>${esc(c.en || "")}</span><span aria-hidden="true">·</span><span>${esc(c.teacher || "")}</span>
          ${c.slides ? `<span class="pill good"><span class="dot"></span>已上課 ${esc(c.week || "")}</span>` : `<span class="pill line">未上課</span>`}
          ${read.has(c.id) ? `<span class="pill violet">${ic("check")}已讀</span>` : ""}</span></span>
        <span class="heat" title="去年考古 ${s.exam} 題"><span class="lbl"><span>考古</span><b class="num">${s.exam} 題</b></span><span class="heat-bar"><i style="width:${(s.exam / maxExam) * 100}%"></i></span></span>
        <span class="mastery"><span class="ring" style="--p:${s.mastery}"></span><span><b class="num">${s.mastery}%</b><br><span class="muted num">${s.right} / ${s.total} 題</span></span></span>
        <span class="chev">${ic("chevR")}</span></a>`;
    };
    let list;
    if (sort === "course") {
      list = (
        m.groups || [{ title: "章節", chapters: m.chapters.map((c) => c.id) }]
      )
        .map(
          (g, gi) => `
        <div class="part-title"><span class="mono">PART ${["I", "II", "III", "IV", "V", "VI"][gi] || gi + 1}</span><span class="display">${esc(g.title)}</span></div>
        ${g.chapters
          .map((id) => subj.chMap[id])
          .filter(Boolean)
          .map(row)
          .join("")}`,
        )
        .join("");
    } else {
      const key =
        sort === "exam"
          ? (c) => -stats[c.id].exam
          : (c) =>
              -(
                stats[c.id].wrong * 100 +
                stats[c.id].exam * (1 - stats[c.id].mastery / 100)
              );
      list = m.chapters
        .map((c) => subj.chMap[c.id])
        .sort((a, b) => key(a) - key(b))
        .map(row)
        .join("");
    }

    render(
      `
      <div class="wrap">
        <nav class="crumbs" aria-label="路徑"><a href="#/">所有科目</a><span class="sep">/</span><span>${esc(m.title)}</span></nav>
        <header class="page-head">
          <div>
            <div class="eyebrow">Subject · ${esc(m.term || "")}${exam !== null && exam >= 0 ? ` · <b>距離考試 ${exam} 天</b>` : ""}</div>
            <h1 class="display h-l">${esc(m.title)}</h1>
            <p class="lede">${esc(m.description || "")}</p>
          </div>
          <div class="statline">
            <div class="fact"><b>${st.total}</b><span>練習題</span></div>
            <div class="fact"><b>${m.chapters.length}</b><span>章節</span></div>
            <div class="fact"><b>${st.done}</b><span>已練習</span></div>
            <div class="fact"><b>${st.done ? `${st.acc}%` : "—"}</b><span>答對率</span></div>
          </div>
        </header>

        <div class="next-up">
          <a class="card next-card feature" href="#/s/${sid}/c/${cont.id}/summary">
            <span class="eyebrow">${ic("book")}${lastC ? "繼續閱讀" : "從這裡開始"}</span>
            <h3>第 ${cont.idx} 章　${esc(cont.title)}</h3>
            <p>${esc(cont.en || "")}</p>
            <span class="go">打開重點整理 ${ic("arrowR")}</span></a>
          ${
            st.wrong
              ? `<a class="card next-card" href="#/s/${sid}/practice?${qs({ filter: "wrong", start: 1, n: 0, mode: "random" })}">
            <span class="eyebrow">${ic("rotate")}錯題複習</span><h3>${st.wrong} 題上次答錯</h3><p>把錯的題目再做一次，答對就會從錯題本移除。</p><span class="go">開始 ${ic("arrowR")}</span></a>`
              : `<a class="card next-card" href="#/s/${sid}/practice?${qs({
                  start: 1,
                  n: 20,
                  mode: "random",
                  ch: m.chapters
                    .filter((c) => c.slides)
                    .map((c) => c.id)
                    .join(","),
                })}">
            <span class="eyebrow">${ic("shuffle")}暖身</span><h3>已上課範圍隨機 20 題</h3><p>考古、課堂題和模擬新題混合出題。</p><span class="go">開始 ${ic("arrowR")}</span></a>`
          }
          ${
            priority
              ? `<a class="card next-card" href="#/s/${sid}/c/${priority.c.id}/exam">
            <span class="eyebrow">${ic("target")}優先補強</span><h3>${esc(priority.c.title)}</h3><p>考古 ${priority.s.exam} 題、目前掌握 ${priority.s.mastery}% — CP 值最高的一章。</p><span class="go">看考點分析 ${ic("arrowR")}</span></a>`
              : ""
          }
        </div>

        <section class="section" style="padding-top:56px">
          <div class="section-head">
            <div><div class="eyebrow">Syllabus</div><h2 class="display h-m" style="margin-top:8px">課程章節</h2></div>
            <div class="seg" role="group" aria-label="排序方式">
              <button type="button" data-sort="course" aria-pressed="${sort === "course"}">課程順序</button>
              <button type="button" data-sort="exam" aria-pressed="${sort === "exam"}">考古題數</button>
              <button type="button" data-sort="weak" aria-pressed="${sort === "weak"}">待加強</button>
            </div>
          </div>
          <div class="syllabus">
            <div class="syl-head"><span>No.</span><span>章節</span><span>去年考古</span><span>掌握度</span><span></span></div>
            ${list}
          </div>
        </section>
      </div>`,
      () => {
        $$("[data-sort]").forEach((b) =>
          b.addEventListener("click", () => {
            store.set("sh:sort", b.dataset.sort);
            const y = scrollY;
            pageSubject(sid, b.dataset.sort).then(() => scrollTo({ top: y }));
          }),
        );
      },
    );
  }

  // ------------------------------------------------------------ pages: chapter
  const TABS = [
    ["summary", "重點整理", "file"],
    ["slides", "上課 slides", "slides"],
    ["exam", "考點分析", "chart"],
    ["practice", "練習", "pen"],
  ];
  async function pageChapter(sid, cid, tab, q = {}) {
    const subj = await loadSubject(sid);
    const c = subj.chMap[cid];
    if (!c) throw new Error(`找不到章節「${cid}」`);
    const content = await loadContent(subj, cid);
    setChrome(
      sid,
      tab === "practice" || tab === "exam" ? "subject" : "reading",
    );
    store.set(K.last(sid), cid);
    const order = subj.meta.chapters.map((x) => x.id);
    const i = order.indexOf(cid);
    const prev = subj.chMap[order[i - 1]],
      next = subj.chMap[order[i + 1]];
    const st = chapterStats(subj, cid);
    const read = getRead(sid);

    let body;
    if (tab === "exam")
      body = `<div style="padding-top:36px">${chapterExamPanel(subj, cid)}<div class="reader" style="padding-top:48px"><aside class="toc" id="toc"></aside><article class="prose">${proseFrom(content.exam)}</article></div></div>`;
    else if (tab === "practice") body = chapterPracticePanel(subj, cid);
    else {
      const slides =
        tab === "slides"
          ? (subj.figs || []).filter((f) => isSlide(f) && f.chapter === cid)
          : [];
      const strip = slides.length
        ? `<section class="slide-strip" data-sid="${esc(sid)}" aria-label="本章上課 slides 圖"><div class="section-head" style="margin-bottom:12px"><div><div class="eyebrow">上課 slides 重點圖 · ${slides.length} 張</div></div><a class="small" href="#/s/${sid}/sheet/figs">全部觀念圖 →</a></div>
          <div class="strip">${slides.map((f) => `<button type="button" class="strip-item" data-zoom="${esc(f.id)}" aria-label="放大投影片：${esc(f.title)}">${slideImg(subj, subj.figById[f.id])}<span><b>${esc(f.title)}</b><span class="mono">p.${f.page}</span></span></button>`).join("")}</div></section>`
        : "";
      body = `${strip}<div class="reader"><aside class="toc" id="toc"></aside><article class="prose">${proseFrom(content[tab]) || `<div class="empty-state">這一頁還沒有內容。</div>`}</article></div>`;
    }

    render(
      `
      <div class="wrap">
        <nav class="crumbs" aria-label="路徑"><a href="#/">所有科目</a><span class="sep">/</span><a href="#/s/${sid}">${esc(subj.meta.title)}</a><span class="sep">/</span><span>第 ${c.idx} 章</span></nav>
        <header class="ch-head">
          <div class="eyebrow">Ch.${pad2(c.idx)} · ${esc(c.week || "")} · ${esc(c.teacher || "")}</div>
          <h1 class="display h-l">${esc(c.title)}</h1>
          <div class="en">${esc(c.en || "")}</div>
          <div class="ch-meta">
            ${c.slides ? `<span class="pill good"><span class="dot"></span>已上課</span>` : `<span class="pill warn"><span class="dot"></span>未上課・依去年共筆與考古</span>`}
            <span class="pill line">考古 ${st.exam} 題</span>
            <span class="pill line">可練習 ${st.total} 題</span>
            <span class="pill line">掌握 ${st.mastery}%</span>
            <button class="btn sm ${read.has(cid) ? "" : "ghost"}" id="readBtn" type="button" aria-pressed="${read.has(cid)}" style="margin-left:auto">${ic("check")}${read.has(cid) ? "已讀" : "標記為已讀"}</button>
          </div>
        </header>
      </div>
      <div class="ch-tabs"><div class="wrap"><nav class="seg" aria-label="章節分頁">
        ${TABS.map(([k, t, icn]) => `<a href="#/s/${sid}/c/${cid}/${k}"${k === tab ? ' aria-current="page"' : ""}>${ic(icn)}${t}</a>`).join("")}
      </nav></div></div>
      <div class="wrap">
        ${body}
        <nav class="pager" aria-label="上一章 / 下一章">
          ${prev ? `<a class="card" href="#/s/${sid}/c/${prev.id}/${tab}"><span class="eyebrow">← 上一章 · Ch.${pad2(prev.idx)}</span><b>${esc(prev.title)}</b></a>` : "<span></span>"}
          ${next ? `<a class="card next" href="#/s/${sid}/c/${next.id}/${tab}"><span class="eyebrow">下一章 · Ch.${pad2(next.idx)} →</span><b>${esc(next.title)}</b></a>` : ""}
        </nav>
        <p class="small muted" style="margin-top:28px">內容有誤？<a href="#/report?${qs({ sid, where: `${c.title}／${TABS.find((t) => t[0] === tab)?.[1] || tab}` })}">回報這一頁</a></p>
      </div>`,
      () => {
        buildToc();
        bindTips($app);
        hydrateFigs($app, subj).then(() => q.find && findInPage(q.find));
        if (q.fig && subj.figById[q.fig]) openFigZoom(subj, q.fig);
        $("#readBtn").addEventListener("click", (e) => {
          const r = getRead(sid);
          const on = !r.has(cid);
          on ? r.add(cid) : r.delete(cid);
          store.set(K.read(sid), [...r]);
          const b = e.currentTarget;
          b.setAttribute("aria-pressed", on);
          b.classList.toggle("ghost", !on);
          b.innerHTML = `${ic("check")}${on ? "已讀" : "標記為已讀"}`;
          toast(on ? "已標記為已讀" : "已取消已讀");
        });
      },
    );
  }
  // 搜尋結果跳到段落：比對去掉空白後的文字
  const squash = (t) =>
    String(t || "")
      .replace(/\s+/g, "")
      .toLowerCase();
  function findInPage(needle) {
    const want = squash(needle);
    if (!want) return;
    const el = $$(
      ".prose :is(h2, h3, li, tr, p, blockquote), .sheet :is(h2, li, tr, p)",
      $app,
    ).find((e) => squash(e.textContent).includes(want));
    if (!el) return;
    el.scrollIntoView({
      block: "center",
      behavior: REDUCED ? "auto" : "smooth",
    });
    el.classList.remove("find-flash");
    void el.offsetWidth;
    el.classList.add("find-flash");
  }
  function proseFrom(md) {
    if (!md || !md.trim()) return "";
    let html = mdToHTML(md);
    // 第一個 h1 與頁首重複 → 改為小標
    html = html.replace(
      /^\s*<h1[^>]*>(.*?)<\/h1>/,
      (_, t) => `<p class="eyebrow" style="margin-bottom:1.6em">${t}</p>`,
    );
    return html;
  }
  function buildToc() {
    const toc = $("#toc");
    if (!toc) return;
    const hs = $$(".prose h2, .prose h3", $app);
    if (hs.length < 3) {
      toc.remove();
      $(".reader")?.style.setProperty("grid-template-columns", "1fr");
      return;
    }
    toc.innerHTML = `<div class="eyebrow">本頁目錄</div><ol>${hs.map((h) => `<li class="lvl${h.tagName[1]}"><a href="#" data-target="${h.id}">${esc(h.textContent.replace(/[\p{Extended_Pictographic}\uFE0F]/gu, "").trim())}</a></li>`).join("")}</ol>`;
    $$("a", toc).forEach((a) =>
      a.addEventListener("click", (e) => {
        e.preventDefault();
        document.getElementById(a.dataset.target)?.scrollIntoView({
          behavior: REDUCED ? "auto" : "smooth",
          block: "start",
        });
      }),
    );
    const links = new Map($$("a", toc).map((a) => [a.dataset.target, a]));
    const io = new IntersectionObserver(
      (ents) => {
        ents.forEach((en) => {
          if (en.isIntersecting) {
            links.forEach((a) => a.classList.remove("active"));
            links.get(en.target.id)?.classList.add("active");
          }
        });
      },
      { rootMargin: "-120px 0px -70% 0px" },
    );
    hs.forEach((h) => io.observe(h));
    onLeave(() => io.disconnect());
  }

  function chapterExamPanel(subj, cid) {
    const list = subj.questions.filter((q) => q.chapter === cid && isExam(q));
    if (!list.length)
      return `<div class="card panel"><h3>去年考古沒有這一章的題目</h3><p class="sub" style="margin:0">下方是依共筆與上課內容整理的預測考點。</p></div>`;
    const srcs = [...new Set(list.map((q) => q.source))];
    const colors = Object.fromEntries(srcs.map((x) => [x, srcColor(subj, x)]));
    const topics = [
      ...countBy(list, (q) => (q.topics || []).filter((t) => t !== "其他")),
    ]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
    const patterns = [...countBy(list, (q) => q.pattern || "其他")].sort(
      (a, b) => b[1] - a[1],
    );
    const img = list.filter((q) => q.imageOnly).length;
    const topicRows = topics.map(([t]) => ({
      label: t,
      href: `#/s/${subj.meta.id}/practice?${qs({ ch: cid, topic: t, start: 1, n: 0, mode: "random" })}`,
      segs: srcs.map((s) => ({
        name: s,
        color: colors[s] || "var(--ink-3)",
        v: list.filter((q) => q.source === s && (q.topics || []).includes(t))
          .length,
      })),
    }));
    const patRows = patterns.map(([p, n]) => ({
      label: p,
      segs: [{ name: "題數", color: "var(--ink-2)", v: n }],
    }));
    return `
      <div class="tiles" style="margin-bottom:14px">
        <div class="tile"><div class="v">${list.length}<small>題</small></div><div class="l">去年考古（${srcs.join("、")}）</div></div>
        <div class="tile"><div class="v">${topics.length ? esc(topics[0][1]) : 0}<small>題</small></div><div class="l">最常考：${topics.length ? esc(topics[0][0]) : "—"}</div></div>
        <div class="tile"><div class="v">${pct(list.filter((q) => q.pattern === "選錯誤（否定）題").length, list.length)}<small>%</small></div><div class="l">「選錯誤」否定題比例</div></div>
        <div class="tile"><div class="v">${chapterStats(subj, cid).mastery}<small>%</small></div><div class="l">你的掌握度${img ? `（另有 ${img} 題看圖題未收錄）` : ""}</div></div>
      </div>
      <div class="grid2">
        <div class="card panel"><h3>考點出現次數</h3><p class="sub">點一列就能只練這個考點的題目</p>${barChart(topicRows, { series: srcs.map((s) => ({ name: s, color: colors[s] })), tableCaption: "考點" })}</div>
        <div class="card panel"><h3>題型分布</h3><p class="sub">這章老師喜歡怎麼問</p>${barChart(patRows, { tableCaption: "題型" })}</div>
      </div>`;
  }

  function chapterPracticePanel(subj, cid) {
    const sid = subj.meta.id;
    const list = subj.questions.filter(
      (q) => q.chapter === cid && !q.imageOnly,
    );
    const by = countBy(list, (q) => q.source);
    const st = chapterStats(subj, cid);
    const L = (o) => `#/s/${sid}/practice?${qs(o)}`;
    const topics = [
      ...countBy(list, (q) => (q.topics || []).filter((t) => t !== "其他")),
    ].sort((a, b) => b[1] - a[1]);
    const P = (href, icon, title, sub, n) =>
      `<a class="card preset" href="${href}"><span class="ico">${ic(icon)}</span><b>${title}</b><span>${sub}</span>${n !== undefined ? `<span class="mono" style="color:var(--ink)">${n} 題</span>` : ""}</a>`;
    return `<div style="padding-top:36px">
      <div class="presets">
        ${P(L({ ch: cid, src: srcKeys(subj, "exam"), mode: "order", start: 1, n: 0 }), "file", "考古題・依序", "照原考卷順序作答，看詳解", list.filter(isExam).length)}
        ${P(L({ ch: cid, mode: "random", start: 1, n: 0 }), "shuffle", "本章全部・隨機", "考古、課堂題、模擬新題混合", list.length)}
        ${P(L({ ch: cid, src: [srcKeys(subj, "class"), srcKeys(subj, "new")].filter(Boolean).join(","), mode: "random", start: 1, n: 0 }), "bolt", "課堂題＋模擬新題", "依考古出題模式編寫的新題", list.filter((x) => !isExam(x)).length)}
        ${P(L({ ch: cid, filter: "wrong", start: 1, n: 0 }), "rotate", "本章錯題", "只練上次答錯的題目", st.wrong)}
      </div>
      <div class="card panel" style="margin-top:14px">
        <h3>依考點練習</h3><p class="sub">只想加強某個觀念？選一個考點直接開始。</p>
        <div class="chips">${topics.map(([t, n]) => `<a class="chip" href="${L({ ch: cid, topic: t, start: 1, n: 0, mode: "random" })}" style="color:inherit;text-decoration:none">${ic("tag")}${esc(t)}<span class="n">${n}</span></a>`).join("")}</div>
      </div>
      <div class="toolbar" style="margin-top:14px"><a class="btn" href="${L({ ch: cid, view: "cards", mode: "random" })}">${ic("cards")}本章翻卡</a><a class="btn" href="${L({ ch: cid, view: "browse", mode: "order" })}">${ic("eye")}瀏覽本章全部題目（含答案）</a></div>
    </div>`;
  }

  // ------------------------------------------------------------ practice
  function sourceMatcher(subj, src) {
    if (!src) return () => true;
    const keys = new Set(src.split(","));
    const all = sourcesOf(subj);
    if (keys.has("exam"))
      all.filter((s) => s.kind === "exam").forEach((s) => keys.add(s.key));
    return (q) => all.some((s) => keys.has(s.key) && s.match(q));
  }
  function buildPool(subj, q) {
    const sid = subj.meta.id;
    if (q.ids) {
      const want = q.ids.split(",");
      return want.map((id) => subj.qById[id]).filter(Boolean);
    }
    const chs = q.ch ? new Set(q.ch.split(",")) : null;
    const sm = sourceMatcher(subj, q.src);
    const prog = getProg(sid);
    const stars = getStars(sid);
    const kw = (q.kw || "").trim().toLowerCase();
    let pool = subj.questions.filter(
      (x) => !x.imageOnly && (!chs || chs.has(x.chapter)) && sm(x),
    );
    if (q.short === "0") pool = pool.filter((x) => x.type !== "short");
    if (q.topic) pool = pool.filter((x) => (x.topics || []).includes(q.topic));
    if (q.filter === "wrong")
      pool = pool.filter((x) => prog[x.id]?.last === "w");
    if (q.filter === "new") pool = pool.filter((x) => !prog[x.id]);
    if (q.filter === "star") pool = pool.filter((x) => stars.has(x.id));
    if (kw)
      pool = pool.filter((x) =>
        `${x.stem} ${(x.options || []).map((o) => o.t).join(" ")} ${(x.topics || []).join(" ")} ${x.explain || ""}`
          .toLowerCase()
          .includes(kw),
      );
    if (q.mode === "random") pool = shuffle(pool);
    const n = parseInt(q.n, 10);
    return n > 0 ? pool.slice(0, n) : pool;
  }

  // 練習區入口：先選科目
  async function pagePracticePick() {
    const subs = await loadAllSubjects();
    setChrome(null, "practice");
    const lastSid = store.get("sh:lastSubject", null);
    const cards = subs
      .map((s) => {
        const st = subjectStats(s);
        const isLast = s.meta.id === lastSid && st.done > 0;
        return `<a class="card subject-card" href="#/s/${s.meta.id}/practice">
        <div>
          <div class="eyebrow">${esc(s.meta.term || "Subject")}${isLast ? " · 上次練習" : ""}</div>
          <h3 class="display" style="margin-top:10px">${esc(s.meta.title)}</h3>
        </div>
        <span class="arrow" aria-hidden="true">${ic("arrowR")}</span>
        <div class="facts">
          <div class="fact"><b>${st.total}</b><span>練習題</span></div>
          <div class="fact"><b>${st.done}</b><span>已作答</span></div>
          <div class="fact"><b>${st.done ? `${st.acc}%` : "—"}</b><span>最近答對率</span></div>
          <div class="fact"><b>${st.wrong}</b><span>錯題</span></div>
        </div></a>`;
      })
      .join("");
    render(`
      <div class="wrap">
        <header style="padding-top:28px">
          <div class="eyebrow">Practice</div>
          <h1 class="display h-l" style="margin-top:12px">練習區</h1>
          <p class="lede">選一個科目開始練習。作答紀錄依科目分開保存。</p>
        </header>
        <div class="section" style="padding-top:32px"><div style="display:grid;gap:14px">${cards}</div></div>
      </div>`);
  }

  async function pagePractice(sid, q) {
    const subj = await loadSubject(sid);
    setChrome(sid, "practice");
    if (q.view === "browse") return renderBrowse(subj, q);
    if (q.view === "cards") return runCards(subj, buildPool(subj, q), q);
    if (q.start) return runSession(subj, buildPool(subj, q), q);
    return renderSetup(subj, q);
  }

  function renderSetup(subj, q) {
    const sid = subj.meta.id;
    const m = subj.meta;
    const chSel = new Set(q.ch ? q.ch.split(",") : []);
    const srcSel = new Set(
      q.src ? q.src.split(",") : sourcesOf(subj).map((s) => s.key),
    );
    const S = {
      mode: q.mode || "random",
      n: q.n || "20",
      filter: q.filter || "",
      short: q.short || "1",
    };
    const st = subjectStats(subj);
    const taught = m.chapters
      .filter((c) => c.slides)
      .map((c) => c.id)
      .join(",");
    const groups = m.groups || [
      { title: "章節", chapters: m.chapters.map((c) => c.id) },
    ];
    const box = `<span class="box">${ic("check")}</span>`;
    const L = (o) => `#/s/${sid}/practice?${qs(o)}`;
    const preset = (href, icon, title, sub) =>
      `<a class="card preset" href="${href}"><span class="ico">${ic(icon)}</span><b>${title}</b><span>${sub}</span></a>`;
    const seg = (name, opts) =>
      `<div class="seg" role="radiogroup" data-seg="${name}">${opts.map(([v, t]) => `<button type="button" role="radio" data-v="${v}" aria-checked="${S[name] === v}">${t}</button>`).join("")}</div>`;
    render(
      `
      <div class="wrap">
        <nav class="crumbs" aria-label="路徑"><a href="#/practice">練習區</a><span class="sep">/</span><span>${esc(m.title)}</span>${(DB.index?.length || 0) > 1 ? `<a class="crumb-switch" href="#/practice">${ic("shuffle")}換科目</a>` : ""}</nav>
        <header style="padding-top:14px">
          <div class="eyebrow">Practice · 已作答 ${st.done} / ${st.total}</div>
          <h1 class="display h-l" style="margin-top:12px">練習區</h1>
          <p class="lede">作答後立刻看到答案和詳解。<span class="hide-touch">用鍵盤作答更快：<kbd>A</kbd>–<kbd>E</kbd> 選答案、<kbd>Enter</kbd> 下一題。</span></p>
        </header>
        <div class="section" style="padding-top:32px">
          <div class="eyebrow" style="margin-bottom:12px">快速開始</div>
          <div class="presets">
            ${preset(L({ start: 1, n: 20, mode: "random" }), "shuffle", "全範圍隨機 20 題", "所有章節、所有來源")}
            ${preset(L({ start: 1, n: 20, mode: "random", ch: taught }), "book", "已上課範圍 20 題", "只出已經上過的章節")}
            ${preset(L({ start: 1, n: 0, mode: "random", filter: "wrong" }), "rotate", `錯題本（${st.wrong}）`, "上次答錯的全部題目")}
            ${preset(L({ start: 1, n: 0, mode: "random", filter: "star" }), "star", `收藏題（${getStars(sid).size}）`, "練習時按 S 收藏")}
          </div>
          <a class="card flash-cta" href="${L({ view: "cards", n: 20, mode: "random", ch: taught })}"><span class="ico">${ic("cards")}</span><span><b>翻卡模式</b><span>正面看題目、翻面看答案和觀念圖，自己判斷記得或不熟。適合考前快速過一輪。</span></span><span class="go">已上課範圍 20 張 ${ic("arrowR")}</span></a>
        </div>
        <form class="setup" id="pf" novalidate>
          <div>
            <fieldset class="fieldset">
              <legend>章節範圍 <span class="muted">不選 = 全部章節</span></legend>
              ${groups
                .map(
                  (
                    g,
                  ) => `<div class="group-title"><span>${esc(g.title)}</span><button type="button" class="link-btn" data-grp="${g.chapters.join(",")}">全選 / 取消</button></div>
                <div class="chips">${g.chapters
                  .map((cid) => {
                    const c = subj.chMap[cid];
                    if (!c) return "";
                    const n = chapterStats(subj, cid).total;
                    return `<label class="chip"><input type="checkbox" name="ch" value="${cid}"${chSel.has(cid) ? " checked" : ""}>${box}${esc(c.title)}<span class="n">${n}</span></label>`;
                  })
                  .join("")}</div>`,
                )
                .join("")}
            </fieldset>
            <fieldset class="fieldset">
              <legend>題目來源</legend>
              <div class="chips">${sourcesOf(subj).map((s) => `<label class="chip"><input type="checkbox" name="src" value="${s.key}"${srcSel.has(s.key) ? " checked" : ""}>${box}${s.label}<span class="n">${subj.questions.filter((x) => s.match(x) && !x.imageOnly).length}</span></label>`).join("")}</div>
            </fieldset>
            <div class="opts-grid">
              <div><div class="field-label">出題順序</div>${seg("mode", [
                ["random", "隨機"],
                ["order", "依原題序"],
              ])}</div>
              <div><div class="field-label">題數</div>${seg("n", [
                ["10", "10"],
                ["20", "20"],
                ["50", "50"],
                ["0", "全部"],
              ])}</div>
              <div><div class="field-label">篩選</div>${seg("filter", [
                ["", "全部"],
                ["new", "沒做過"],
                ["wrong", "答錯過"],
                ["star", "收藏"],
              ])}</div>
              <div><div class="field-label">簡答題</div>${seg("short", [
                ["1", "包含（自評）"],
                ["0", "不包含"],
              ])}</div>
            </div>
            <div style="margin-top:22px"><label class="field-label" for="kw">關鍵字 <span class="muted">搜尋題幹、選項、考點、詳解</span></label>
              <div class="search-field">${ic("search")}<input class="input" id="kw" name="kw" type="search" placeholder="例如：C3 convertase、IgA、Listeria" value="${esc(q.kw || "")}" autocomplete="off"></div></div>
          </div>
          <aside class="card setup-summary" aria-live="polite">
            <div><div class="eyebrow hide-m">符合條件</div><div class="count" id="cnt">0<small>題</small></div><div class="small muted hide-m" id="cntBreak"></div></div>
            <button class="btn accent lg" type="submit">${ic("arrowR")}開始練習</button>
            <div class="hide-m setup-links">
              <button class="link-btn" type="button" id="browseBtn">${"瀏覽模式（看答案）"}</button>
              <button class="link-btn" type="button" id="cardsBtn">翻卡模式</button>
              <button class="link-btn" type="button" id="resetBtn" style="color:var(--bad)">清除作答紀錄</button>
            </div>
          </aside>
        </form>
      </div>`,
      () => {
        const form = $("#pf");
        const read = () => {
          const fd = new FormData(form);
          return {
            ch: fd.getAll("ch").join(","),
            src: fd.getAll("src").join(","),
            kw: (fd.get("kw") || "").trim(),
            ...S,
          };
        };
        const update = () => {
          const o = read();
          const full = buildPool(subj, { ...o, n: 0, mode: "order" });
          const n = parseInt(o.n, 10);
          const shown = n > 0 ? Math.min(n, full.length) : full.length;
          $("#cnt").innerHTML = `${shown}<small>題</small>`;
          const by = countBy(full, (x) => x.source);
          $("#cntBreak").textContent = full.length
            ? `共 ${full.length} 題符合：${[...by].map(([k, v]) => `${k} ${v}`).join("、")}`
            : "沒有符合的題目，放寬條件試試。";
          form.querySelector("[type=submit]").disabled = !full.length;
        };
        $$("[data-seg]", form).forEach((g) =>
          g.addEventListener("click", (e) => {
            const b = e.target.closest("button");
            if (!b) return;
            S[g.dataset.seg] = b.dataset.v;
            $$("button", g).forEach((x) => {
              x.setAttribute("aria-checked", x === b);
            });
            update();
          }),
        );
        form.addEventListener("change", update);
        $("#kw").addEventListener("input", update);
        $$("[data-grp]", form).forEach((b) =>
          b.addEventListener("click", () => {
            const boxes = b.dataset.grp
              .split(",")
              .map((id) => form.querySelector(`input[name=ch][value="${id}"]`))
              .filter(Boolean);
            const all = boxes.every((x) => x.checked);
            boxes.forEach((x) => {
              x.checked = !all;
            });
            update();
          }),
        );
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          const o = read();
          if (!o.src) return toast("請至少選一個題目來源");
          location.hash = `#/s/${sid}/practice?${qs({ ...o, start: 1 })}`;
        });
        $("#browseBtn").addEventListener("click", () => {
          const o = read();
          location.hash = `#/s/${sid}/practice?${qs({ ...o, n: "", mode: "order", view: "browse" })}`;
        });
        $("#cardsBtn").addEventListener("click", () => {
          const o = read();
          location.hash = `#/s/${sid}/practice?${qs({ ...o, view: "cards" })}`;
        });
        $("#resetBtn").addEventListener("click", () => {
          if (
            confirm(
              "確定要清除這台裝置上本科目的所有作答紀錄與收藏嗎？這個動作無法復原。",
            )
          ) {
            store.set(K.prog(sid), {});
            store.set(K.star(sid), []);
            toast("已清除作答紀錄");
            update();
          }
        });
        update();
      },
    );
  }

  function qMeta(subj, q) {
    const c = subj.chMap[q.chapter];
    return `<div class="q-meta">
      <span class="pill ${pillFor(q.source)}"><span class="dot"></span>${esc(q.source)}${q.num ? ` · 第 ${q.num} 題` : ""}</span>
      ${c ? `<a class="pill line" href="#/s/${subj.meta.id}/c/${c.id}/summary">Ch.${pad2(c.idx)} ${esc(c.title)}</a>` : ""}
      ${(q.topics || [])
        .filter((t) => t !== "其他")
        .map((t) => `<span class="pill line">${ic("tag")}${esc(t)}</span>`)
        .join("")}
      ${q.disputed ? `<span class="pill warn">答案有爭議</span>` : ""}
    </div>`;
  }
  const reportHref = (sid, q) =>
    `#/report?${qs({ sid, qid: q.id, where: `${q.source} ${q.id}` })}`;
  const ansText = (q) =>
    (q.answer || []).length
      ? q.answer.map((a) => `(${a})`).join(" 或 ")
      : "無正確選項";

  function runSession(subj, pool, q) {
    const sid = subj.meta.id;
    if (!pool.length) {
      const msg =
        q.filter === "wrong"
          ? ["沒有錯題", "目前沒有答錯的題目，太棒了。去挑戰還沒做過的題目吧。"]
          : q.filter === "star"
            ? ["還沒有收藏", "作答時按「收藏」或鍵盤 S，就能把題目加進這裡。"]
            : ["沒有符合的題目", "換個範圍或放寬篩選條件試試看。"];
      render(
        emptyState(
          msg[0],
          msg[1],
          `<a class="btn primary" href="#/s/${sid}/practice">回練習設定</a>`,
        ),
      );
      return;
    }
    const S = {
      i: 0,
      ans: pool.map(() => null),
      streak: 0,
      best: 0,
      t0: Date.now(),
    };
    let timer = 0;
    const counts = () =>
      S.ans.reduce(
        (a, x) => {
          if (x) {
            a.done++;
            x.ok ? a.c++ : a.w++;
          }
          return a;
        },
        { done: 0, c: 0, w: 0 },
      );
    const shell = () => {
      const c = counts();
      return `<div class="wrap"><div class="quiz">
        <div class="quiz-top">
          <a class="btn ghost sm" href="#/s/${sid}/practice" aria-label="結束練習">${ic("x")}<span class="hide-s">結束</span></a>
          <span class="prog"><b>${S.i + 1}</b> / ${pool.length}</span>
          <div class="quiz-stats">
            <span title="答對" style="color:var(--good)">${ic("check")}<b class="num">${c.c}</b></span>
            <span title="答錯" style="color:var(--bad)">${ic("x")}<b class="num">${c.w}</b></span>
            ${S.streak >= 3 ? `<span class="streak" title="連續答對">${ic("flame")}連對 ${S.streak}</span>` : ""}
            <span title="經過時間">${ic("clock")}<span class="num" id="clock">${fmtTime(Date.now() - S.t0)}</span></span>
          </div>
        </div>
        ${
          pool.length > 1
            ? `<div class="dots" role="group" aria-label="題目導覽">${pool
                .map((_, k) => {
                  const a = S.ans[k];
                  const cls =
                    k === S.i
                      ? "cur"
                      : a
                        ? a.self
                          ? a.ok
                            ? "c"
                            : "s"
                          : a.ok
                            ? "c"
                            : "w"
                        : "";
                  return `<button type="button" class="${cls}" data-go="${k}" aria-label="第 ${k + 1} 題${a ? (a.ok ? "，答對" : "，答錯") : ""}"></button>`;
                })
                .join("")}</div>`
            : '<div style="height:22px"></div>'
        }
        <div id="qslot"></div>
        <div class="shortcut-hint" aria-hidden="true"><span><kbd>A</kbd>–<kbd>E</kbd> 作答</span><span><kbd>Enter</kbd> 下一題</span><span><kbd>←</kbd><kbd>→</kbd> 上／下一題</span><span><kbd>S</kbd> 收藏</span></div>
      </div></div>`;
    };
    const cardHTML = () => {
      const qq = pool[S.i];
      const a = S.ans[S.i];
      const stars = getStars(sid);
      const isShort = qq.type === "short" || !(qq.options || []).length;
      const ans = qq.answer || [];
      const opts = isShort
        ? ""
        : `<div class="options" role="group" aria-label="選項">${qq.options
            .map((o) => {
              let cls = "";
              if (a) {
                if (ans.includes(o.k)) cls = "correct";
                else if (a.k === o.k) cls = "wrong";
                else cls = "dim";
              }
              return `<button type="button" class="option ${cls}" data-k="${o.k}"${a ? " disabled" : ""}><span class="key">${o.k}</span><span class="txt">${esc(o.t)}</span>${ic(cls === "wrong" ? "x" : "check", "mark")}</button>`;
            })
            .join("")}</div>`;
      let verdict = "";
      if (a) {
        const tone = a.self ? "neutral" : a.ok ? "good" : "bad";
        const head = a.self
          ? `${ic("check")}已自我評分：${a.ok ? "我會了" : "還不熟"}`
          : a.ok
            ? `${ic("check")}答對了${S.streak >= 3 && S.i === S.last ? `・連對 ${S.streak} 題` : ""}`
            : `${ic("x")}答錯了，正確答案是 ${ansText(qq)}`;
        verdict = `<div class="verdict ${tone}" role="status"><div class="verdict-head">${head}</div><div class="verdict-body">
          ${qq.answerText ? `<div class="answer-text"><div class="explain-title">參考答案</div>${esc(qq.answerText)}</div>` : ""}
          ${qq.explain ? `<div class="explain-title">詳解</div><div class="explain">${esc(qq.explain)}</div>` : qq.answerText ? "" : '<div class="muted">這題沒有附詳解。</div>'}
          ${qq.note ? `<div class="note">${ic("alert")}<div>${esc(qq.note)}</div></div>` : ""}${figLinks(subj, qq)}</div></div>`;
      } else if (isShort && S.revealed === S.i) {
        verdict = `<div class="verdict neutral"><div class="verdict-head">${ic("eye")}參考答案</div><div class="verdict-body">
          ${qq.answerText ? `<div class="answer-text">${esc(qq.answerText)}</div>` : ""}${qq.explain ? `<div class="explain">${esc(qq.explain)}</div>` : ""}
          <div class="self-grade"><button class="btn" type="button" data-self="1">${ic("check")}我會了</button><button class="btn" type="button" data-self="0">${ic("rotate")}還不熟</button></div></div></div>`;
      }
      const shortBox =
        isShort && !a && S.revealed !== S.i
          ? `<div class="note" style="margin-top:0">${ic("pen")}<div>簡答題：先在心裡或紙上作答，再看參考答案自我評分。</div></div><div class="q-foot"><button class="btn accent" type="button" id="reveal">${ic("eye")}顯示參考答案</button></div>`
          : "";
      const last = S.i === pool.length - 1;
      return `<article class="card qcard" aria-labelledby="qstem">
        ${qMeta(subj, qq)}
        <p class="q-stem" id="qstem">${esc(qq.stem)}</p>
        ${opts}${shortBox}
        <div aria-live="polite">${verdict}</div>
        <div class="q-foot">
          <button class="btn sm ghost" type="button" id="star" aria-pressed="${stars.has(qq.id)}">${stars.has(qq.id) ? icFill("star") : ic("star")}${stars.has(qq.id) ? "已收藏" : "收藏"}</button>
          <a class="btn sm ghost" href="${reportHref(sid, qq)}">${ic("flag")}回報此題</a>
          <span class="spacer"></span>
          ${S.i > 0 ? `<button class="btn sm" type="button" id="prev" aria-label="上一題">${ic("arrowL")}</button>` : ""}
          <button class="btn ${a ? "primary" : ""}" type="button" id="next">${a ? (last ? "看結果" : "下一題") : last ? "結束並看結果" : "跳過"}${ic("arrowR")}</button>
        </div>
      </article>`;
    };
    const paint = (full) => {
      if (full) {
        $app.innerHTML = `<div class="enter">${shell()}</div>`;
        $$("[data-go]").forEach((b) =>
          b.addEventListener("click", () => go(+b.dataset.go)),
        );
      } else {
        const top = $(".quiz-top");
        const tmp = document.createElement("div");
        tmp.innerHTML = shell();
        top.replaceWith($(".quiz-top", tmp));
        const d = $(".dots");
        const nd = $(".dots", tmp);
        if (d && nd) {
          d.replaceWith(nd);
          $$("[data-go]").forEach((b) =>
            b.addEventListener("click", () => go(+b.dataset.go)),
          );
        }
      }
      $("#qslot").innerHTML = cardHTML();
      bindCard();
    };
    const go = (k) => {
      if (k < 0) return;
      if (k >= pool.length) return finish();
      S.i = k;
      paint(false);
      $("#qslot").scrollIntoView({ block: "nearest" });
      if (innerWidth < 760) scrollTo({ top: 0 });
    };
    const answer = (k) => {
      const qq = pool[S.i];
      if (S.ans[S.i]) return;
      const ok = (qq.answer || []).includes(k);
      S.ans[S.i] = { k, ok };
      S.last = S.i;
      S.streak = ok ? S.streak + 1 : 0;
      S.best = Math.max(S.best, S.streak);
      record(sid, qq.id, ok);
      paint(false);
      $("#next")?.focus({ preventScroll: true });
    };
    const selfGrade = (ok) => {
      const qq = pool[S.i];
      S.ans[S.i] = { k: null, ok, self: true };
      S.last = S.i;
      S.streak = ok ? S.streak + 1 : 0;
      record(sid, qq.id, ok);
      paint(false);
      $("#next")?.focus({ preventScroll: true });
    };
    const bindCard = () => {
      $$(".option").forEach((b) =>
        b.addEventListener("click", () => answer(b.dataset.k)),
      );
      $("#reveal")?.addEventListener("click", () => {
        S.revealed = S.i;
        paint(false);
      });
      $$("[data-self]").forEach((b) =>
        b.addEventListener("click", () => selfGrade(b.dataset.self === "1")),
      );
      $("#next").addEventListener("click", () => go(S.i + 1));
      $("#prev")?.addEventListener("click", () => go(S.i - 1));
      $("#star").addEventListener("click", (e) => {
        const on = toggleStar(sid, pool[S.i].id);
        const b = e.currentTarget;
        b.setAttribute("aria-pressed", on);
        b.innerHTML = `${on ? icFill("star") : ic("star")}${on ? "已收藏" : "收藏"}`;
        toast(on ? "已加入收藏" : "已取消收藏");
      });
    };
    const onKey = (e) => {
      if (
        e.target.matches("input, textarea, select") ||
        e.metaKey ||
        e.ctrlKey ||
        e.altKey ||
        !$("#qslot")
      )
        return;
      const k = e.key.toUpperCase();
      const map = { 1: "A", 2: "B", 3: "C", 4: "D", 5: "E" };
      const key = map[k] || k;
      const opt = $(`.option[data-k="${key}"]:not(:disabled)`);
      if (opt) {
        e.preventDefault();
        opt.click();
        return;
      }
      if (
        e.key === "Enter" &&
        document.activeElement?.tagName !== "BUTTON" &&
        document.activeElement?.tagName !== "A"
      ) {
        e.preventDefault();
        $("#next")?.click();
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        go(S.i + 1);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(S.i - 1);
      } else if (key === "S") {
        e.preventDefault();
        $("#star")?.click();
      }
    };
    const finish = () => {
      clearInterval(timer);
      removeEventListener("keydown", onKey);
      const c = counts();
      const p = pct(c.c, c.done);
      const wrongQs = pool.filter((_, k) => S.ans[k] && !S.ans[k].ok);
      const skipped = pool.length - c.done;
      const topicMiss = [
        ...countBy(wrongQs, (x) =>
          (x.topics || []).filter((t) => t !== "其他"),
        ),
      ]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6);
      const title =
        c.done === 0
          ? "還沒有作答"
          : p >= 85
            ? "非常穩！"
            : p >= 70
              ? "表現不錯"
              : p >= 50
                ? "有進步空間"
                : "先別灰心";
      render(
        `<div class="wrap"><div class="result">
        <div class="card result-hero">
          <div class="score-ring" style="--p:${p}"><div><b>${p}<small style="font-size:.4em">%</small></b><span>答對率</span></div></div>
          <div>
            <div class="eyebrow">Session complete · ${fmtTime(Date.now() - S.t0)}</div>
            <h1 class="display h-m" style="margin:10px 0 6px">${title}</h1>
            <p class="muted" style="margin:0 0 18px">答對 <b class="num" style="color:var(--ink)">${c.c}</b> 題、答錯 <b class="num" style="color:var(--ink)">${c.w}</b> 題${skipped ? `、跳過 ${skipped} 題` : ""}${S.best >= 3 ? `，最長連對 ${S.best} 題` : ""}。</p>
            <div class="toolbar">
              ${wrongQs.length ? `<a class="btn accent" href="#/s/${sid}/practice?${qs({ ids: wrongQs.map((x) => x.id).join(","), start: 1 })}">${ic("rotate")}重做這 ${wrongQs.length} 題錯題</a>` : ""}
              <a class="btn primary" href="#/s/${sid}/practice">${ic("shuffle")}再練一組</a>
              <a class="btn" href="#/s/${sid}">回總覽</a>
            </div>
          </div>
        </div>
        ${
          topicMiss.length
            ? `<div class="card panel" style="margin-top:14px"><h3>這次錯在哪些考點</h3><p class="sub">點一列直接練這個考點</p>${barChart(
                topicMiss.map(([t, n]) => ({
                  label: t,
                  href: `#/s/${sid}/practice?${qs({ topic: t, start: 1, n: 0, mode: "random" })}`,
                  segs: [{ name: "答錯", color: "var(--series-2)", v: n }],
                })),
                { tableCaption: "答錯題數" },
              )}</div>`
            : ""
        }
        ${wrongQs.length ? `<div class="section" style="padding-top:40px"><div class="eyebrow" style="margin-bottom:12px">答錯的題目 · ${wrongQs.length}</div>${wrongQs.map((x) => browseCard(subj, x, true)).join("")}</div>` : ""}
      </div></div>`,
        () => bindTips($app),
      );
    };
    paint(true);
    timer = setInterval(() => {
      const el = $("#clock");
      if (el) el.textContent = fmtTime(Date.now() - S.t0);
    }, 1000);
    addEventListener("keydown", onKey);
    onLeave(() => {
      clearInterval(timer);
      removeEventListener("keydown", onKey);
    });
  }

  // ------------------------------------------------------------ flashcards
  function runCards(subj, pool, q) {
    const sid = subj.meta.id;
    pool = pool.filter((x) => x.answer?.length || x.answerText);
    if (!pool.length) {
      render(
        emptyState(
          "沒有可以翻的卡",
          "換個範圍或放寬篩選條件試試看。",
          `<a class="btn primary" href="#/s/${sid}/practice">回練習設定</a>`,
        ),
      );
      return;
    }
    const S = { i: 0, flipped: false, res: pool.map(() => null) };
    const tally = () =>
      S.res.reduce((a, r) => (r === null ? a : (r ? a.y++ : a.n++, a)), {
        y: 0,
        n: 0,
      });
    const face = () => {
      const x = pool[S.i];
      const ans = x.answer || [];
      const opts = (x.options || []).length
        ? `<ol>${x.options.map((o) => `<li><span class="k">${o.k}</span><span>${esc(o.t)}</span></li>`).join("")}</ol>`
        : "";
      const optsBack = (x.options || []).length
        ? `<ol>${x.options.map((o) => `<li class="${ans.includes(o.k) ? "ans" : ""}"><span class="k">${o.k}</span><span>${esc(o.t)}</span></li>`).join("")}</ol>`
        : "";
      const big = ans.length
        ? ans
            .map((k) => {
              const o = (x.options || []).find((y) => y.k === k);
              return o ? `(${k}) ${esc(o.t)}` : `(${k})`;
            })
            .join("　或　")
        : x.answerText
          ? ""
          : "無正確選項";
      return `<div class="flash-card${S.flipped ? " flipped" : ""}" id="fc">
        <div class="flash-inner">
          <section class="card flash-face front"${S.flipped ? " inert" : ""}>
            ${qMeta(subj, x)}
            <p class="q-stem">${esc(x.stem)}</p>${opts}
            <div class="flip-hint"><button class="btn accent lg" type="button" id="flip">${ic("rotate")}翻面看答案<span class="kbd-hint hide-touch"><kbd>Space</kbd></span></button></div>
          </section>
          <section class="card flash-face back"${S.flipped ? "" : " inert"}>
            <div class="eyebrow">答案</div>
            ${big ? `<div class="flash-answer">${big}</div>` : ""}
            ${x.answerText ? `<div class="answer-text">${esc(x.answerText)}</div>` : ""}
            ${optsBack && ans.length ? `<details class="fig-inline" style="border:0;padding:0;margin:0 0 6px"><summary>全部選項</summary>${optsBack}</details>` : ""}
            ${x.explain ? `<div class="explain-title" style="margin-top:14px">詳解</div><div class="explain">${esc(x.explain)}</div>` : ""}
            ${x.note ? `<div class="note">${ic("alert")}<div>${esc(x.note)}</div></div>` : ""}
            ${figLinks(subj, x)}
          </section>
        </div>
      </div>
      <div class="flash-actions" ${S.flipped ? "" : "hidden"}>
        <button class="btn no" type="button" data-know="0">${ic("rotate")}還不熟<span class="kbd-hint hide-touch"><kbd>1</kbd></span></button>
        <button class="btn yes" type="button" data-know="1">${ic("check")}記得<span class="kbd-hint hide-touch"><kbd>2</kbd></span></button>
      </div>`;
    };
    const paint = () => {
      const t = tally();
      const n = pool.length;
      $app.innerHTML = `<div class="enter"><div class="wrap"><div class="flash">
        <div class="quiz-top">
          <a class="btn ghost sm" href="#/s/${sid}/practice" aria-label="結束翻卡">${ic("x")}<span class="hide-s">結束</span></a>
          <span class="prog"><b>${S.i + 1}</b> / ${n}</span>
          <div class="quiz-stats">
            <span title="記得" style="color:var(--good)">${ic("check")}<b class="num">${t.y}</b></span>
            <span title="還不熟" style="color:var(--bad)">${ic("rotate")}<b class="num">${t.n}</b></span>
          </div>
        </div>
        <div class="flash-bar" aria-hidden="true"><i style="width:${(t.y / n) * 100}%;background:var(--good)"></i><i style="width:${(t.n / n) * 100}%;background:var(--bad)"></i></div>
        ${face()}
        <div class="shortcut-hint" aria-hidden="true"><span><kbd>Space</kbd> 翻面</span><span><kbd>1</kbd> 還不熟</span><span><kbd>2</kbd> 記得</span><span><kbd>←</kbd><kbd>→</kbd> 上／下一張</span></div>
      </div></div></div>`;
      $("#flip")?.addEventListener("click", flip);
      $$("[data-know]").forEach((b) =>
        b.addEventListener("click", () => know(b.dataset.know === "1")),
      );
    };
    const flip = () => {
      S.flipped = !S.flipped;
      $("#fc").classList.toggle("flipped", S.flipped);
      $("#fc .front").inert = S.flipped;
      $("#fc .back").inert = !S.flipped;
      $(".flash-actions").hidden = !S.flipped;
      if (S.flipped) $("[data-know='1']")?.focus({ preventScroll: true });
    };
    const go = (k) => {
      if (k < 0) return;
      if (k >= pool.length) return finish();
      S.i = k;
      S.flipped = false;
      paint();
      if (innerWidth < 760) scrollTo({ top: 0 });
    };
    const know = (ok) => {
      S.res[S.i] = ok;
      record(sid, pool[S.i].id, ok);
      go(S.i + 1);
    };
    const onKey = (e) => {
      if (
        e.target.matches("input, textarea, select") ||
        e.metaKey ||
        e.ctrlKey ||
        e.altKey ||
        !$(".flash")
      )
        return;
      if (e.key === " " && !e.target.closest("summary, .hot")) {
        e.preventDefault();
        flip();
      } else if ((e.key === "1" || e.key === "2") && S.flipped) {
        e.preventDefault();
        know(e.key === "2");
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        go(S.i + 1);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(S.i - 1);
      }
    };
    const finish = () => {
      removeEventListener("keydown", onKey);
      const t = tally();
      const unsure = pool.filter((_, k) => S.res[k] === false);
      render(`<div class="wrap"><div class="result">
        <div class="card result-hero">
          <div class="score-ring" style="--p:${pct(t.y, t.y + t.n)}"><div><b>${t.y}<small style="font-size:.4em"> / ${t.y + t.n}</small></b><span>記得</span></div></div>
          <div>
            <div class="eyebrow">Flashcards complete</div>
            <h1 class="display h-m" style="margin:10px 0 6px">${t.n ? `還有 ${t.n} 張要再看` : t.y ? "全部記得！" : "還沒有翻卡"}</h1>
            <p class="muted" style="margin:0 0 18px">「還不熟」的卡片已經加進錯題本，之後可以在練習區用作答模式再確認一次。</p>
            <div class="toolbar">
              ${unsure.length ? `<a class="btn accent" href="#/s/${sid}/practice?${qs({ ids: unsure.map((x) => x.id).join(","), view: "cards" })}">${ic("rotate")}只翻這 ${unsure.length} 張</a>` : ""}
              <a class="btn primary" href="#/s/${sid}/practice?${qs({ ...q, view: "cards" })}">${ic("shuffle")}再翻一組</a>
              <a class="btn" href="#/s/${sid}/practice">回練習區</a>
            </div>
          </div>
        </div>
        ${unsure.length ? `<div class="section" style="padding-top:40px"><div class="eyebrow" style="margin-bottom:12px">還不熟的卡片 · ${unsure.length}</div>${unsure.map((x) => browseCard(subj, x, true)).join("")}</div>` : ""}
      </div></div>`);
    };
    paint();
    addEventListener("keydown", onKey);
    onLeave(() => removeEventListener("keydown", onKey));
  }

  function browseCard(subj, q, open) {
    const ans = q.answer || [];
    return `<article class="card bq${open ? " open" : ""}">
      ${qMeta(subj, q)}
      <p class="q-stem">${esc(q.stem)}</p>
      ${(q.options || []).length ? `<ol>${q.options.map((o) => `<li class="${ans.includes(o.k) ? "ans" : ""}"><span class="k">${o.k}</span><span>${esc(o.t)}</span></li>`).join("")}</ol>` : ""}
      <details${open ? " open" : ""}><summary>${ic("eye")}答案與詳解</summary>
        <div class="verdict neutral" style="margin-top:0"><div class="verdict-head">答案：${ans.length ? ansText(q) : q.answerText ? "見參考答案" : "無正確選項"}</div><div class="verdict-body">
        ${q.answerText ? `<div class="answer-text">${esc(q.answerText)}</div>` : ""}
        ${q.explain ? `<div class="explain">${esc(q.explain)}</div>` : '<div class="muted">這題沒有附詳解。</div>'}
        ${q.note ? `<div class="note">${ic("alert")}<div>${esc(q.note)}</div></div>` : ""}${figLinks(subj, q)}
        <div style="margin-top:12px;display:flex;gap:14px;font-size:.85rem"><a href="#/s/${subj.meta.id}/q/${q.id}">單獨練這題</a><a href="${reportHref(subj.meta.id, q)}">回報此題</a></div></div></div>
      </details></article>`;
  }

  function renderBrowse(subj, q) {
    const sid = subj.meta.id;
    const pool = buildPool(subj, { ...q, n: 0, mode: "order" });
    const one = q.ch && q.ch.split(",").length === 1 ? subj.chMap[q.ch] : null;
    const img = subj.questions.filter(
      (x) => x.imageOnly && (!q.ch || q.ch.split(",").includes(x.chapter)),
    ).length;
    render(
      `<div class="wrap">
      <nav class="crumbs" aria-label="路徑"><a href="#/s/${sid}">${esc(subj.meta.title)}</a><span class="sep">/</span>${one ? `<a href="#/s/${sid}/c/${one.id}/practice">${esc(one.title)}</a><span class="sep">/</span>` : ""}<span>瀏覽題目</span></nav>
      <header style="padding-top:14px" class="section-head">
        <div><div class="eyebrow">Browse · ${pool.length} 題${img ? `（另有 ${img} 題看圖題未收錄）` : ""}</div><h1 class="display h-l" style="margin-top:12px">${one ? esc(one.title) : "瀏覽題目"}</h1></div>
        <div class="toolbar"><button class="btn" type="button" id="toggleAll">${ic("eye")}全部顯示答案</button>
          <a class="btn primary" href="#/s/${sid}/practice?${qs({ ...q, view: "", start: 1, n: 0, mode: "random" })}">${ic("pen")}改成作答模式</a></div>
      </header>
      <div style="margin-top:24px">${pool.map((x) => browseCard(subj, x, false)).join("") || '<div class="card empty"><p>沒有符合的題目。</p></div>'}</div>
    </div>`,
      () => {
        $("#toggleAll").addEventListener("click", (e) => {
          const open = !$app.querySelector(".bq.open");
          $$(".bq").forEach((c) => {
            c.classList.toggle("open", open);
            c.querySelector("details").open = open;
          });
          e.currentTarget.innerHTML = `${ic("eye")}${open ? "全部隱藏答案" : "全部顯示答案"}`;
        });
        $$(".bq details").forEach((d) =>
          d.addEventListener("toggle", () =>
            d.closest(".bq").classList.toggle("open", d.open),
          ),
        );
      },
    );
  }

  // ------------------------------------------------------------ cheatsheet & figure gallery
  async function loadSheet(subj) {
    if (subj.sheet !== undefined) return subj.sheet;
    let raw = "";
    if (subj.meta.sheet)
      raw = await fetchText(`${subj.path}/${subj.meta.sheet}`).catch(() => "");
    // 以 "## " 切成卡片；卡片內 "@ch id,id" 與 "@fig id" 是連結設定
    const cards = [];
    let cur = null;
    for (const line of raw.split("\n")) {
      const h = line.match(/^##\s+(.+)$/);
      if (h) {
        cur = { title: h[1].trim(), ch: [], fig: [], md: "" };
        cards.push(cur);
        continue;
      }
      if (!cur) continue;
      const m = line.match(/^@(ch|fig)\s+(.+)$/);
      if (m) cur[m[1]].push(...m[2].split(",").map((x) => x.trim()));
      else cur.md += line + "\n";
    }
    return (subj.sheet = cards);
  }
  async function pageSheet(sid, tab, q = {}) {
    const subj = await loadSubject(sid);
    setChrome(sid, "sheet");
    const m = subj.meta;
    const figs = subj.figs || [];
    const cards = await loadSheet(subj);
    const isFigs = tab === "figs";
    let body;
    if (isFigs) {
      const byCh = m.chapters
        .map((c) => ({
          c: subj.chMap[c.id],
          list: figs.filter((f) => f.chapter === c.id),
        }))
        .filter((g) => g.list.length)
        .sort((a, b) => a.list.every(isSlide) - b.list.every(isSlide));
      body = byCh
        .map(
          (g) => `<section class="section" style="padding-top:28px">
          <div class="eyebrow" style="margin-bottom:12px">Ch.${pad2(g.c.idx)} · ${esc(g.c.title)}</div>
          <div class="fig-gallery">${g.list
            .slice()
            .sort((a, b) => isSlide(a) - isSlide(b))
            .map((f) => {
              const F = subj.figById[f.id];
              const slide = isSlide(F);
              return `<article class="card fig-card${slide ? " is-slide" : ""}" data-sid="${esc(sid)}">
              <button type="button" class="thumb" data-zoom="${esc(f.id)}" aria-label="放大「${esc(f.title)}」" style="pointer-events:auto;border:0;cursor:zoom-in;width:100%">${slide ? slideImg(subj, F) : `<div class="fig-body loading" data-src="${esc(f.id)}" style="padding:0;overflow:hidden;width:100%;height:100%"></div>`}</button>
              <div class="meta"><span class="eyebrow">${figLabel(F)}${slide ? ` · ${esc(F.deck.split(" ")[0])}` : ""}</span><b>${esc(f.title)}</b></div>
              <div class="foot">${slide ? `<a href="#/s/${sid}/c/${f.chapter}/slides">本章 slides 重點</a>` : `<a href="#/s/${sid}/c/${f.chapter}/summary?${qs({ find: f.title })}">在章節裡看</a>`}${(
                f.topics || []
              )
                .slice(0, 1)
                .map(
                  (t) =>
                    `<a href="#/s/${sid}/practice?${qs({ topic: t, start: 1, n: 0, mode: "random" })}">練「${esc(t)}」</a>`,
                )
                .join("")}</div>
            </article>`;
            })
            .join("")}</div></section>`,
        )
        .join("");
    } else {
      body = cards.length
        ? `<div class="sheet">${cards
            .map(
              (c, i) => `<section class="card" id="sheet-${i}">
            <h2><span class="mono">${pad2(i + 1)}</span>${esc(c.title)}</h2>
            <div class="prose">${mdToHTML(c.md)}</div>
            ${c.fig.map((f) => (subj.figById[f] ? `<div data-sid="${esc(sid)}" style="margin-top:6px"><button class="btn sm noprint" type="button" data-zoom="${esc(f)}">${ic("image")}${esc(subj.figById[f].title)}</button></div>` : "")).join("")}
            ${
              c.ch.length
                ? `<div class="go noprint">${c.ch
                    .filter((id) => subj.chMap[id])
                    .map(
                      (id) =>
                        `<a href="#/s/${sid}/c/${id}/summary">→ Ch.${pad2(subj.chMap[id].idx)} ${esc(subj.chMap[id].title)}</a>`,
                    )
                    .join("")}</div>`
                : ""
            }
          </section>`,
            )
            .join("")}</div>`
        : `<div class="card empty"><p>這個科目還沒有速記表。</p></div>`;
    }
    render(
      `<div class="wrap">
        <nav class="crumbs" aria-label="路徑"><a href="#/s/${sid}">${esc(m.title)}</a><span class="sep">/</span><span>${isFigs ? "觀念圖" : "速記表"}</span></nav>
        <header class="section-head" style="padding-top:14px;align-items:end">
          <div><div class="eyebrow">${isFigs ? `Figures · ${figs.filter((f) => !isSlide(f)).length} 張手繪觀念圖 · ${figs.filter(isSlide).length} 張上課 slides` : `Cheatsheet · ${cards.length} 張表`}</div>
          <h1 class="display h-l" style="margin-top:12px">${isFigs ? "觀念圖庫" : "考前速記表"}</h1>
          <p class="lede" style="margin-bottom:0">${isFigs ? "手繪觀念圖把最常考的機轉重新畫清楚（滑過虛線名詞看說明）；上課 slides 是老師原圖，對照著看。點任何一張都能放大。" : "考前十分鐘掃一遍：最常被拿來出題的對照表都濃縮在這裡。可以直接列印成 A4。"}</p></div>
          <div class="toolbar noprint">
            <nav class="seg" aria-label="切換"><a href="#/s/${sid}/sheet"${isFigs ? "" : ' aria-current="page"'}>${ic("grid")}速記表</a><a href="#/s/${sid}/sheet/figs"${isFigs ? ' aria-current="page"' : ""}>${ic("image")}觀念圖</a></nav>
            ${isFigs ? "" : `<button class="btn" type="button" id="printBtn">${ic("printer")}列印</button>`}
          </div>
        </header>
        <div class="sheet-wrap">${body}</div>
      </div>`,
      () => {
        $("#printBtn")?.addEventListener("click", () => print());
        hydrateFigs($app, subj).then(() => q.find && findInPage(q.find));
      },
    );
  }

  // ------------------------------------------------------------ analysis
  async function pageAnalysis(sid) {
    const subj = await loadSubject(sid);
    setChrome(sid, "analysis");
    const m = subj.meta;
    const exam = subj.questions.filter(isExam);
    const srcs = [...new Set(exam.map((q) => q.source))];
    const colors = Object.fromEntries(srcs.map((x) => [x, srcColor(subj, x)]));
    const series = srcs.map((s) => ({
      name: s,
      color: colors[s] || "var(--ink-3)",
    }));
    const chRows = m.chapters
      .map((c) => ({
        label: `${pad2(subj.chMap[c.id].idx)} ${c.title}`,
        href: `#/s/${sid}/c/${c.id}/exam`,
        segs: srcs.map((s) => ({
          name: s,
          color: colors[s],
          v: exam.filter((q) => q.chapter === c.id && q.source === s).length,
        })),
      }))
      .filter((r) => r.segs.some((s) => s.v))
      .sort(
        (a, b) =>
          b.segs.reduce((x, s) => x + s.v, 0) -
          a.segs.reduce((x, s) => x + s.v, 0),
      );
    const topics = [
      ...countBy(exam, (q) => (q.topics || []).filter((t) => t !== "其他")),
    ]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);
    const patterns = [...countBy(exam, (q) => q.pattern || "其他")].sort(
      (a, b) => b[1] - a[1],
    );
    const taught = new Set(m.chapters.filter((c) => c.slides).map((c) => c.id));
    const taughtN = exam.filter((q) => taught.has(q.chapter)).length;
    const neg = exam.filter((q) => q.pattern === "選錯誤（否定）題").length;
    const en = exam.filter((q) => /^[A-Za-z]/.test(q.stem)).length;
    render(
      `<div class="wrap">
      <nav class="crumbs" aria-label="路徑"><a href="#/s/${sid}">${esc(m.title)}</a><span class="sep">/</span><span>考題分析</span></nav>
      <header style="padding-top:14px">
        <div class="eyebrow">Analysis · ${srcs.join(" + ")}</div>
        <h1 class="display h-l" style="margin-top:12px">去年考了什麼，<br>怎麼考。</h1>
        <p class="lede">統計 ${exam.length} 題考古題。考點標籤依題目關鍵字自動歸類後人工校正；點任一列可以直接進入該章考點分析或開始練習。</p>
      </header>
      <div class="tiles" style="margin-top:32px">
        <div class="tile"><div class="v">${exam.length}</div><div class="l">考古總題數</div></div>
        <div class="tile"><div class="v">${pct(taughtN, exam.length)}<small>%</small></div><div class="l">落在已上課章節（${taughtN} 題）</div></div>
        <div class="tile"><div class="v">${pct(neg, exam.length)}<small>%</small></div><div class="l">「何者錯誤」否定題</div></div>
        <div class="tile"><div class="v">${pct(en, exam.length)}<small>%</small></div><div class="l">英文題幹</div></div>
      </div>
      <div class="card panel" style="margin-top:14px"><h3>各章考古題數</h3><p class="sub">題數越多，代表這章在期中考的份量越重</p>${barChart(chRows, { series, tableCaption: "各章題數" })}</div>
      <div class="grid2" style="margin-top:14px">
        <div class="card panel"><h3>最常考的 15 個考點</h3><p class="sub">點一列就練這個考點</p>${barChart(
          topics.map(([t, n]) => ({
            label: t,
            href: `#/s/${sid}/practice?${qs({ topic: t, start: 1, n: 0, mode: "random" })}`,
            segs: [{ name: "題數", color: "var(--series-1)", v: n }],
          })),
          { tableCaption: "考點" },
        )}</div>
        <div class="card panel"><h3>題型分布</h3><p class="sub">熟悉題型，比較不會被選項繞進去</p>${barChart(
          patterns.map(([p, n]) => ({
            label: p,
            segs: [{ name: "題數", color: "var(--ink-2)", v: n }],
          })),
          { tableCaption: "題型" },
        )}
          ${
            (m.insights || []).length
              ? `<h3 style="margin-top:28px">出題模式觀察</h3><ol class="insights">${m.insights.map(([b, t]) => `<li><span><b>${esc(b)}</b>${esc(t)}</span></li>`).join("")}</ol>`
              : ""
          }</div>
      </div>
    </div>`,
      () => bindTips($app),
    );
  }

  // ------------------------------------------------------------ report
  async function pageReport(q) {
    let subj = null;
    if (q.sid) {
      try {
        subj = await loadSubject(q.sid);
      } catch {
        subj = null;
      }
    }
    setChrome(subj ? q.sid : null, "report");
    const qq = subj && q.qid ? subj.qById[q.qid] : null;
    const mail = CFG.contactEmail;
    const line = CFG.lineUrl;
    render(
      `<div class="wrap">
      <div class="report">
        <div>
          <div class="eyebrow" style="padding-top:28px">Report · Feedback</div>
          <h1 class="display h-l" style="margin-top:12px">回報 / 回饋</h1>
          <p class="lede">答案錯、詳解不清楚、錯字、網站壞掉，或是用起來的感想、想要的功能，都歡迎告訴我。</p>
          <ul class="channels">
            ${mail ? `<li><span class="ico">${ic("mail")}</span><span><b>用 Email 寄送</b>會開啟你的郵件程式，內容自動帶入。</span></li>` : ""}
            <li><span class="ico">${ic("chat")}</span><span><b>用 LINE 傳送</b>${line ? "會開啟 LINE；填了說明的話，內容會先複製好，貼上送出就好。" : "填了說明的話，內容會先複製好，貼到 LINE 傳給我。"}</span></li>
          </ul>
        </div>
        <form class="card form" id="rf" style="margin-top:28px">
          ${qq ? `<div class="q-ref"><div class="mono">${esc(qq.source)} · ${esc(qq.id)} · 目前答案 ${esc((qq.answer || []).join("/") || "—")}</div><div style="margin-top:6px">${esc(qq.stem.slice(0, 180))}${qq.stem.length > 180 ? "…" : ""}</div></div>` : ""}
          <div class="opts-grid">
            <label>類型<select class="input" name="type"><option>答案錯誤</option><option>詳解有誤或不清楚</option><option>題目文字錯誤 / 缺漏</option><option>重點整理內容錯誤</option><option>網站功能問題</option><option>使用回饋 / 功能建議</option><option>其他</option></select></label>
            <label>位置<input class="input" type="text" name="where" value="${esc(q.where || (qq ? `${qq.source} ${qq.id}` : ""))}" placeholder="例如：先天免疫／重點整理"></label>
          </div>
          <label>說明<textarea class="input" name="desc" placeholder="回報錯誤：寫下你認為正確的內容，最好附上出處或 slides 頁碼。使用回饋：哪裡好用、哪裡卡卡的、想要什麼功能都可以。"></textarea></label>
          <div class="toolbar">
            ${mail ? `<button class="btn accent" type="submit" id="mailBtn">${ic("mail")}用 Email 寄送</button>` : ""}
            <button class="btn${mail ? "" : " accent"}" type="button" id="lineBtn">${ic("chat")}用 LINE 傳送</button>
          </div>
        </form>
      </div>
    </div>`,
      () => {
        const form = $("#rf");
        const compose = () => {
          const fd = new FormData(form);
          const type = fd.get("type"),
            where = fd.get("where"),
            desc = fd.get("desc");
          const title = `[${type}] ${qq ? qq.id : where || "一般回報"}`;
          const body = [
            `**類型**：${type}`,
            `**科目**：${subj ? subj.meta.title : "—"}`,
            `**位置**：${where || "—"}`,
            qq
              ? `**題號**：${qq.id}（${qq.source}）\n**題目**：${qq.stem}\n**選項**：\n${(qq.options || []).map((o) => `- (${o.k}) ${o.t}`).join("\n")}\n**網站目前答案**：${(qq.answer || []).join("/") || "—"}`
              : "",
            `\n**說明**：\n${desc}`,
            `\n---\n頁面：${location.href}`,
          ]
            .filter(Boolean)
            .join("\n");
          return { title, body: body.replace(/\*\*/g, "") };
        };
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          if (!form.reportValidity() || !mail) return;
          const { title, body } = compose();
          location.href = `mailto:${mail}?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
        });
        $("#lineBtn").addEventListener("click", async () => {
          // LINE 無法預先帶入訊息給特定好友：有寫說明就先複製內容，再開啟 LINE
          if (String(new FormData(form).get("desc") || "").trim()) {
            const { title, body } = compose();
            try {
              await navigator.clipboard.writeText(`${title}\n\n${body}`);
              toast(line ? "已複製，開啟 LINE 後貼上送出" : "已複製，貼到 LINE 傳給我");
            } catch {
              /* 複製失敗不影響開啟 LINE */
            }
          }
          if (line) window.open(line, "_blank", "noopener");
        });
      },
    );
  }

  // ------------------------------------------------------------ command palette
  const cmdk = $("#cmdk");
  let cmdIndex = null;
  async function buildIndex() {
    if (cmdIndex) return cmdIndex;
    const subs = await loadAllSubjects();
    const items = [];
    for (const s of subs) {
      const sid = s.meta.id;
      items.push({
        g: "頁面",
        icon: "home",
        t: `${s.meta.title} 總覽`,
        s: s.meta.term || "",
        href: `#/s/${sid}`,
      });
      items.push({
        g: "頁面",
        icon: "pen",
        t: "練習區",
        s: s.meta.title,
        href: `#/s/${sid}/practice`,
      });
      items.push({
        g: "頁面",
        icon: "chart",
        t: "考題分析",
        s: s.meta.title,
        href: `#/s/${sid}/analysis`,
      });
      items.push({
        g: "頁面",
        icon: "rotate",
        t: "錯題本",
        s: s.meta.title,
        href: `#/s/${sid}/practice?${qs({ filter: "wrong", start: 1, n: 0, mode: "random" })}`,
      });
      items.push({
        g: "頁面",
        icon: "grid",
        t: "考前速記表",
        s: s.meta.title,
        href: `#/s/${sid}/sheet`,
        k: "cheatsheet 速記 列印",
      });
      items.push({
        g: "頁面",
        icon: "image",
        t: "觀念圖庫",
        s: s.meta.title,
        href: `#/s/${sid}/sheet/figs`,
        k: "figures 圖解 diagram",
      });
      items.push({
        g: "頁面",
        icon: "cards",
        t: "翻卡模式",
        s: s.meta.title,
        href: `#/s/${sid}/practice?${qs({ view: "cards", n: 20, mode: "random" })}`,
        k: "flashcards 閃卡 翻卡",
      });
      for (const f of s.figs || [])
        items.push(
          isSlide(f)
            ? {
                g: "觀念圖",
                icon: "slides",
                t: `${f.title}（上課 slides）`,
                s: `${f.deck} · p.${f.page}`,
                href: `#/s/${sid}/c/${f.chapter}/slides?${qs({ fig: f.id })}`,
                k: (f.topics || []).join(" "),
              }
            : {
                g: "觀念圖",
                icon: "image",
                t: f.title,
                s: `Fig. ${pad2(s.figById[f.id].n)} · ${s.chMap[f.chapter]?.title || ""}`,
                href: `#/s/${sid}/c/${f.chapter}/summary?${qs({ find: f.title })}`,
                k: `${f.keywords || ""} ${(f.topics || []).join(" ")}`,
              },
        );
      // 章節內文：每個標題、條列、表格列都能被搜到
      const blocks = await Promise.all(
        s.meta.chapters.map(async (c) => [c, await loadContent(s, c.id)]),
      );
      for (const [c, parts] of blocks)
        for (const tab of ["summary", "slides", "exam"]) {
          let sec = "";
          for (const raw of (parts[tab] || "").split("\n")) {
            const line = raw.trim();
            if (!line || (/^(\||-{3,}|===|<)/.test(line) && !/^\|/.test(line)))
              continue;
            if (/^\|[\s|:-]+\|?$/.test(line)) continue;
            const plain = mdPlain(line);
            if (plain.length < 4) continue;
            const hd = line.match(/^(#{2,3})\s+/);
            if (hd) sec = plain;
            if (/^#\s/.test(line)) continue;
            const first = /^\|/.test(line)
              ? mdPlain(line.split("|")[1] || "")
              : plain;
            items.push({
              g: hd ? "段落" : "重點",
              icon: hd ? "list" : "file",
              t: plain,
              s: `Ch.${pad2(s.chMap[c.id].idx)} ${c.title}${sec && !hd ? ` › ${sec}` : ""} · ${{ summary: "重點整理", slides: "上課 slides", exam: "考點分析" }[tab]}`,
              href: `#/s/${sid}/c/${c.id}/${tab}?${qs({ find: first.slice(0, 40) })}`,
            });
          }
        }
      for (const card of await loadSheet(s))
        items.push({
          g: "段落",
          icon: "grid",
          t: `速記：${card.title}`,
          s: s.meta.title,
          href: `#/s/${sid}/sheet?${qs({ find: card.title })}`,
          k: mdPlain(card.md).slice(0, 600),
        });
      for (const c of s.meta.chapters)
        items.push({
          g: "章節",
          icon: "book",
          t: `${pad2(s.chMap[c.id].idx)}　${c.title}`,
          s: `${c.en || ""} · ${c.teacher || ""}`,
          href: `#/s/${sid}/c/${c.id}/summary`,
          k: `${c.title} ${c.en} ${c.teacher} ${c.id}`,
        });
      for (const [t, n] of countBy(s.questions, (q) =>
        (q.topics || []).filter((x) => x !== "其他"),
      ))
        items.push({
          g: "考點",
          icon: "tag",
          t,
          s: `練習 ${n} 題 · ${s.meta.short || s.meta.title}`,
          href: `#/s/${sid}/practice?${qs({ topic: t, start: 1, n: 0, mode: "random" })}`,
        });
      for (const q of s.questions)
        if (!q.imageOnly)
          items.push({
            g: "題目",
            icon: "help",
            t: q.stem,
            s: `${q.source} · ${s.chMap[q.chapter]?.title || ""}`,
            href: `#/s/${sid}/q/${q.id}`,
            k: `${q.stem} ${(q.options || []).map((o) => o.t).join(" ")}`,
          });
    }
    return (cmdIndex = items);
  }
  const mdPlain = (t) =>
    String(t || "")
      .replace(/^#{1,6}\s+/, "")
      .replace(/^[-*]\s+|^\d+\.\s+|^>\s*/g, "")
      .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
      .replace(/<br\s*\/?>/g, " ")
      .replace(/<[^>]+>/g, "")
      .replace(/\\(?=[*_`#|])/g, "")
      .replace(/[*_`]/g, "")
      .replace(/\|/g, " · ")
      .replace(/^\s*·\s*|\s*·\s*$/g, "")
      .replace(/\s+/g, " ")
      .trim();
  const hl = (text, terms) => {
    let h = esc(text);
    for (const t of terms) {
      if (!t) continue;
      h = h.replace(
        new RegExp(
          t
            .replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;"),
          "gi",
        ),
        (m) => `<mark>${m}</mark>`,
      );
    }
    return h;
  };
  async function openPalette() {
    const items = await buildIndex();
    cmdk.hidden = false;
    cmdk.innerHTML = `<div class="cmdk" role="dialog" aria-modal="true" aria-label="搜尋">
      <div class="cmdk-input">${ic("search")}<input id="cmdkIn" type="text" placeholder="搜尋章節、重點、觀念圖或題目，例如 TLR4、CLIP…" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="cmdkList"><kbd>Esc</kbd></div>
      <div class="cmdk-list" id="cmdkList" role="listbox"></div>
      <div class="cmdk-foot"><span><kbd>↑</kbd><kbd>↓</kbd> 選擇</span><span><kbd>Enter</kbd> 開啟</span><span><kbd>Esc</kbd> 關閉</span></div></div>`;
    const input = $("#cmdkIn");
    const list = $("#cmdkList");
    let results = [];
    let sel = 0;
    const draw = () => {
      const qv = input.value.trim().toLowerCase();
      const terms = qv.split(/\s+/).filter(Boolean);
      if (!terms.length)
        results = items
          .filter((x) => x.g === "頁面" || x.g === "章節")
          .slice(0, 14);
      else {
        // 英數關鍵字用字邊界比對（避免 IgA 命中 ligand），並依命中位置排序
        // 使用者打全大寫縮寫（MAC、TAP、CLIP）時要求完整字詞，避免 MAC 命中 macrophage
        const raw = input.value.trim().split(/\s+/).filter(Boolean);
        const res = terms.map((t, i) =>
          /^[\w-]+$/.test(t)
            ? /^[A-Z0-9-]{2,6}$/.test(raw[i] || "") && /[A-Z]/.test(raw[i])
              ? new RegExp(
                  `(^|[^A-Za-z0-9])${raw[i].replace(/[-]/g, "\\-")}($|[^A-Za-z])`,
                )
              : new RegExp(`(^|[^a-z0-9])${t.replace(/[-]/g, "\\-")}`, "i")
            : null,
        );
        const has = (text, t, i) =>
          res[i] ? res[i].test(text) : text.toLowerCase().includes(t);
        const score = (x) => {
          let s = 0;
          for (let i = 0; i < terms.length; i++) {
            if (has(x.t, terms[i], i)) s += 3;
            else if (has(x.s, terms[i], i)) s += 2;
            else if (x.k && has(x.k, terms[i], i)) s += 1;
            else return 0;
          }
          return s;
        };
        const lim = {
          頁面: 4,
          章節: 5,
          觀念圖: 5,
          段落: 5,
          重點: 8,
          考點: 5,
          題目: 20,
        };
        const byG = {};
        for (const x of items) {
          const sc = score(x);
          if (sc) (byG[x.g] = byG[x.g] || []).push([sc, x]);
        }
        results = [
          "頁面",
          "章節",
          "觀念圖",
          "段落",
          "重點",
          "考點",
          "題目",
        ].flatMap((g) =>
          (byG[g] || [])
            .sort((a, b) => b[0] - a[0])
            .slice(0, lim[g])
            .map((p) => p[1]),
        );
      }
      sel = Math.min(sel, Math.max(0, results.length - 1));
      let lastG = "";
      list.innerHTML = results.length
        ? results
            .map((x, i) => {
              const head =
                x.g !== lastG ? `<div class="cmdk-group">${x.g}</div>` : "";
              lastG = x.g;
              return `${head}<a class="cmdk-item" href="${x.href}" role="option" id="ci${i}" aria-selected="${i === sel}" data-i="${i}"><span class="ico">${ic(x.icon)}</span><span style="min-width:0"><div class="t">${hl(x.t, terms)}</div><div class="s">${esc(x.s)}</div></span><span class="r">↵</span></a>`;
            })
            .join("")
        : `<div class="cmdk-empty">找不到「${esc(input.value)}」。試試英文名稱或中文關鍵字。</div>`;
      input.setAttribute(
        "aria-activedescendant",
        results.length ? `ci${sel}` : "",
      );
    };
    const move = (d) => {
      if (!results.length) return;
      sel = (sel + d + results.length) % results.length;
      $$(".cmdk-item", list).forEach((el) =>
        el.setAttribute("aria-selected", +el.dataset.i === sel),
      );
      $(`#ci${sel}`)?.scrollIntoView({ block: "nearest" });
    };
    input.addEventListener("input", () => {
      sel = 0;
      draw();
    });
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        move(1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        move(-1);
      } else if (e.key === "Enter") {
        e.preventDefault();
        const r = results[sel];
        if (r) {
          closePalette();
          location.hash = r.href;
        }
      } else if (e.key === "Escape") {
        e.preventDefault();
        closePalette();
      }
    });
    list.addEventListener("click", (e) => {
      if (e.target.closest(".cmdk-item")) closePalette();
    });
    list.addEventListener("pointermove", (e) => {
      const it = e.target.closest(".cmdk-item");
      if (it && +it.dataset.i !== sel) {
        sel = +it.dataset.i;
        $$(".cmdk-item", list).forEach((el) =>
          el.setAttribute("aria-selected", +el.dataset.i === sel),
        );
      }
    });
    draw();
    input.focus();
  }
  function closePalette() {
    cmdk.hidden = true;
    cmdk.innerHTML = "";
  }
  cmdk.addEventListener("mousedown", (e) => {
    if (e.target === cmdk) closePalette();
  });
  $("#searchBtn").addEventListener("click", openPalette);
  addEventListener("keydown", (e) => {
    if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      cmdk.hidden ? openPalette() : closePalette();
    } else if (
      e.key === "/" &&
      cmdk.hidden &&
      !e.target.matches("input, textarea, select")
    ) {
      e.preventDefault();
      openPalette();
    } else if (e.key === "Escape" && !cmdk.hidden) closePalette();
  });

  // boot: wait for marked (deferred) then route
  const boot = () => route();
  if (window.marked) boot();
  else addEventListener("load", boot, { once: true });
})();
