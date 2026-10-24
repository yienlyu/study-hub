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
 *   #/me                             學習軌跡 / 登入
 *   #/play[/:game]                   小遊戲（sudoku | killer | nonogram）；彩蛋，選單不列，入口見 easter eggs
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
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    cloud:
      '<path d="M7 18a5 5 0 0 1-.6-9.96A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9z"/>',
    download: '<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
    logout: '<path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h10"/>',
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
  let onStoreSet = () => {};
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
      onStoreSet(k);
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
    reset: (s) => `sh:${s}:resetT`,
  };
  const getProg = (sid) => store.get(K.prog(sid), {});
  const record = (sid, qid, ok, { ms = null, mode = "mcq" } = {}) => {
    const now = Date.now();
    const p = getProg(sid);
    const r = p[qid] || { c: 0, w: 0 };
    ok ? r.c++ : r.w++;
    r.last = ok ? "c" : "w";
    r.t = now;
    p[qid] = r;
    store.set(K.prog(sid), p);
    logAttempt([
      uuid(),
      sid,
      qid,
      ok ? 1 : 0,
      now,
      ms > 0 && ms < 30 * 60e3 ? Math.round(ms) : null,
      mode,
    ]);
  };

  // 逐筆作答紀錄（學習軌跡、記憶曲線用）。每筆：[id, sid, qid, ok, t, ms, mode]
  // 本機只留最近 LOG_MAX 筆；登入後完整紀錄存在 Supabase。
  const LOG = "sh:log";
  const PENDING = "sh:log:pending";
  const LOG_MAX = 20000;
  const uuid = () =>
    crypto.randomUUID?.() ||
    "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
      (
        c ^
        (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
      ).toString(16),
    );
  const getLog = () => store.get(LOG, []);
  const logAttempt = (e) => {
    const log = getLog();
    log.push(e);
    store.set(LOG, log.slice(-LOG_MAX));
    const pend = store.get(PENDING, []);
    pend.push(e);
    store.set(PENDING, pend.slice(-LOG_MAX));
    Cloud.flushSoon();
  };
  const getStars = (sid) => new Set(store.get(K.star(sid), []));
  const toggleStar = (sid, qid) => {
    const s = getStars(sid);
    s.has(qid) ? s.delete(qid) : s.add(qid);
    store.set(K.star(sid), [...s]);
    return s.has(qid);
  };
  const getRead = (sid) => new Set(store.get(K.read(sid), []));

  // ------------------------------------------------------------ cloud（Supabase 登入 / 同步）
  // 沒填 config.js 的 supabaseUrl / supabaseAnonKey 時整段不啟用，網站照常只用本機紀錄。
  const SUPABASE_JS =
    "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js";
  const GSI_JS = "https://accounts.google.com/gsi/client";
  const loadScript = (src) =>
    new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = res;
      s.onerror = () => rej(new Error(`載入失敗：${src}`));
      document.head.appendChild(s);
    });
  const ss = {
    get: (k) => {
      try {
        return sessionStorage.getItem(k);
      } catch {
        return null;
      }
    },
    set: (k, v) => {
      try {
        v == null ? sessionStorage.removeItem(k) : sessionStorage.setItem(k, v);
      } catch {
        /* */
      }
    },
  };
  // 合併本機與雲端狀態：每題取較新的紀錄；收藏 / 已讀取較晚修改的一方；清除紀錄（reset）之前的進度一律丟掉。
  function mergeState(L, R) {
    const M = { prog: {}, stars: {}, read: {}, reset: {}, T: {} };
    const T = (o, k) => o.T?.[k] || 0;
    for (const k of new Set([
      ...Object.keys(L.T || {}),
      ...Object.keys(R.T || {}),
    ]))
      M.T[k] = Math.max(T(L, k), T(R, k));
    const sids = new Set(
      ["prog", "stars", "read"].flatMap((f) => [
        ...Object.keys(L[f] || {}),
        ...Object.keys(R[f] || {}),
      ]),
    );
    for (const s of sids) {
      const rs = Math.max(L.reset?.[s] || 0, R.reset?.[s] || 0);
      if (rs) M.reset[s] = rs;
      const a = L.prog?.[s] || {},
        b = R.prog?.[s] || {},
        p = {};
      for (const q of new Set([...Object.keys(a), ...Object.keys(b)])) {
        const x = a[q],
          y = b[q];
        const w = !y || (x && (x.t || 0) >= (y.t || 0)) ? x : y;
        if (w && (w.t || 0) >= rs) p[q] = w;
      }
      M.prog[s] = p;
      for (const kind of ["stars", "read"]) {
        const k = `${kind}:${s}`,
          la = L[kind]?.[s],
          ra = R[kind]?.[s];
        M[kind][s] = !ra
          ? la || []
          : !la
            ? ra
            : T(L, k) > T(R, k)
              ? la
              : T(R, k) > T(L, k)
                ? ra
                : [...new Set([...la, ...ra])];
      }
    }
    return M;
  }
  const Cloud = {
    on: !!(CFG.supabaseUrl && CFG.supabaseAnonKey),
    sb: null,
    user: null,
    ready: Promise.resolve(),
    busy: false,
    applying: false,
    status: "", // "" | "syncing" | "error"
    error: "",
    lastSync: store.get("sh:cloud:lastSync", null),
    _ft: 0,
    _st: 0,
    emit(changed = false) {
      paintAcct();
      dispatchEvent(new CustomEvent("sh:cloud", { detail: { changed } }));
    },
    fail(e) {
      console.error(e);
      this.status = "error";
      this.error = e?.message || String(e);
      this.emit();
    },
    init() {
      if (!this.on) return;
      this.ready = (async () => {
        try {
          await loadScript(SUPABASE_JS);
          this.sb = window.supabase.createClient(
            CFG.supabaseUrl,
            CFG.supabaseAnonKey,
            {
              auth: {
                flowType: "pkce",
                detectSessionInUrl: true,
                persistSession: true,
                autoRefreshToken: true,
              },
            },
          );
          // getSession 會等 ?code= 換成登入狀態後才回來
          const { data } = await this.sb.auth.getSession();
          this.user = data.session?.user || null;
          const u = new URL(location.href);
          const err =
            u.searchParams.get("error_description") ||
            u.searchParams.get("error");
          if (u.searchParams.has("code") || err) {
            const back = ss.get("sh:auth:back") || "#/me";
            ss.set("sh:auth:back", null);
            history.replaceState(null, "", u.pathname + back);
            if (err) toast(`登入失敗：${err}`);
            else if (this.user) toast("登入成功");
            route();
          }
          this.sb.auth.onAuthStateChange((ev, session) => {
            const prev = this.user?.id;
            this.user = session?.user || null;
            // 不能在這個 callback 裡直接 await supabase 呼叫，延到下一輪
            if (this.user && this.user.id !== prev)
              setTimeout(() => this.sync(), 0);
            this.emit();
          });
          this.emit();
          if (this.user) this.sync();
        } catch (e) {
          this.fail(e);
        }
      })();
    },
    async signIn(provider, email) {
      await this.ready;
      if (!this.sb) throw new Error(this.error || "登入元件尚未載入");
      const redirectTo = location.origin + location.pathname;
      ss.set("sh:auth:back", location.hash || "#/");
      if (provider === "email") {
        const { error } = await this.sb.auth.signInWithOtp({
          email,
          options: { emailRedirectTo: redirectTo },
        });
        if (error) throw error;
        return;
      }
      const { error } = await this.sb.auth.signInWithOAuth({
        provider,
        options: { redirectTo },
      });
      if (error) throw error;
    },
    // Email + 密碼。Supabase 的錯誤訊息是英文，常見的翻成中文
    authErr(e) {
      const m = e?.message || String(e);
      const T = {
        "Invalid login credentials": "Email 或密碼錯誤",
        "User already registered": "這個 Email 已經註冊過，請直接登入",
        "Email not confirmed": "Email 還沒驗證，請先點確認信裡的連結",
      };
      return new Error(
        T[m] ||
          (/at least \d+ characters/.test(m) ? "密碼太短，至少要 6 個字元" : m),
      );
    },
    async signInPassword(email, password) {
      await this.ready;
      if (!this.sb) throw new Error(this.error || "登入元件尚未載入");
      const { error } = await this.sb.auth.signInWithPassword({
        email,
        password,
      });
      if (error) throw this.authErr(error);
    },
    // 回傳 true 表示已直接登入；false 表示要先點確認信
    async signUp(email, password) {
      await this.ready;
      if (!this.sb) throw new Error(this.error || "登入元件尚未載入");
      ss.set("sh:auth:back", location.hash || "#/");
      const { data, error } = await this.sb.auth.signUp({
        email,
        password,
        options: { emailRedirectTo: location.origin + location.pathname },
      });
      if (error) throw this.authErr(error);
      // 已註冊過的 Email 在開啟驗證信時不會報錯，只會回傳沒有 identities 的 user
      if (data.user && !data.user.identities?.length)
        throw this.authErr({ message: "User already registered" });
      return !!data.session;
    },
    // 自訂名稱存在 user_metadata.display_name（full_name / name 會被 Google 登入蓋回去）
    async setName(name) {
      const { error } = await this.sb.auth.updateUser({
        data: { display_name: name || null },
      });
      if (error) throw error;
    },
    async setPassword(password) {
      const { error } = await this.sb.auth.updateUser({ password });
      if (error) throw this.authErr(error);
    },
    // 自訂頭像：裁成正方形縮到 256px，存到 Storage 的 avatars/<user id>/，網址記在 user_metadata.custom_avatar
    // （不用 avatar_url：Google 登入每次都會把它蓋回 Google 的頭像）
    async setAvatar(file) {
      if (!/^image\//.test(file.type)) throw new Error("請選擇圖片檔");
      if (file.size > 20e6) throw new Error("圖片太大（上限 20 MB）");
      let img;
      try {
        img = await createImageBitmap(file);
      } catch {
        throw new Error("讀不了這張圖片，請換成 JPG 或 PNG");
      }
      const S = 256,
        side = Math.min(img.width, img.height),
        cv = document.createElement("canvas");
      cv.width = cv.height = S;
      cv.getContext("2d").drawImage(
        img,
        (img.width - side) / 2,
        (img.height - side) / 2,
        side,
        side,
        0,
        0,
        S,
        S,
      );
      const blob = await new Promise((r) => cv.toBlob(r, "image/jpeg", 0.88));
      const path = `${this.user.id}/avatar.jpg`;
      const bucket = this.sb.storage.from("avatars");
      const up = await bucket.upload(path, blob, {
        upsert: true,
        contentType: "image/jpeg",
        cacheControl: "3600",
      });
      if (up.error)
        throw /bucket not found/i.test(up.error.message)
          ? new Error(
              "還沒建立頭像儲存空間：請在 Supabase SQL Editor 執行 supabase/schema.sql",
            )
          : up.error;
      const url = `${bucket.getPublicUrl(path).data.publicUrl}?v=${Date.now()}`;
      const { error } = await this.sb.auth.updateUser({
        data: { custom_avatar: url },
      });
      if (error) throw error;
    },
    async clearAvatar() {
      const { error } = await this.sb.auth.updateUser({
        data: { custom_avatar: null },
      });
      if (error) throw error;
      await this.sb.storage
        .from("avatars")
        .remove([`${this.user.id}/avatar.jpg`])
        .catch(() => {});
    },
    // Google Identity Services：在本站頁面拿到 Google 的 ID token，再交給 Supabase 換成登入狀態
    _gsi: null,
    gsi() {
      return (this._gsi ||= (async () => {
        await loadScript(GSI_JS);
        // Google 收雜湊後的 nonce，Supabase 收原始值再自己比對
        const raw = btoa(
          String.fromCharCode(...crypto.getRandomValues(new Uint8Array(24))),
        );
        const buf = await crypto.subtle.digest(
          "SHA-256",
          new TextEncoder().encode(raw),
        );
        const hashed = [...new Uint8Array(buf)]
          .map((b) => b.toString(16).padStart(2, "0"))
          .join("");
        google.accounts.id.initialize({
          client_id: CFG.googleClientId,
          nonce: hashed,
          use_fedcm_for_button: true,
          callback: async ({ credential }) => {
            try {
              await this.ready;
              const { error } = await this.sb.auth.signInWithIdToken({
                provider: "google",
                token: credential,
                nonce: raw,
              });
              if (error) throw error;
              toast("登入成功");
            } catch (e) {
              toast(`登入失敗：${e.message || e}`);
            }
          },
        });
      })().catch((e) => {
        this._gsi = null;
        throw e;
      }));
    },
    // Google 的按鈕是 iframe 改不了樣式：做成透明疊在本站按鈕上，看到的是本站按鈕、點到的是 Google 的
    async renderGoogle(el) {
      await this.gsi();
      if (!el.isConnected) return;
      const hit = $(".gsi-hit", el);
      google.accounts.id.renderButton(hit, {
        size: "large",
        shape: "pill",
        text: "signin_with",
        locale: "zh-TW",
        width: Math.min(400, Math.max(200, Math.ceil(el.offsetWidth))),
      });
    },
    async signOut() {
      await this.flush().catch(() => {});
      if (window.google?.accounts?.id) google.accounts.id.disableAutoSelect();
      await this.sb.auth.signOut();
      this.user = null;
      this.emit();
    },
    flushSoon() {
      if (!this.user) return;
      clearTimeout(this._ft);
      this._ft = setTimeout(
        () => this.flush().catch((e) => this.fail(e)),
        2500,
      );
    },
    stateSoon() {
      if (!this.user) return;
      clearTimeout(this._st);
      this._st = setTimeout(() => {
        if (this.busy) return this.stateSoon();
        this.syncState().catch((e) => this.fail(e));
      }, 4000);
    },
    // 上傳還沒送出的逐筆紀錄（id 由本機產生，重送不會重複）
    async flush() {
      if (!this.user) return;
      const pend = store.get(PENDING, []);
      for (let i = 0; i < pend.length; i += 500) {
        const chunk = pend.slice(i, i + 500);
        const { error } = await this.sb.from("attempts").upsert(
          chunk.map(([id, subject, qid, ok, t, ms, mode]) => ({
            id,
            subject,
            qid,
            ok: !!ok,
            ms,
            mode,
            answered_at: new Date(t).toISOString(),
          })),
          { onConflict: "id", ignoreDuplicates: true },
        );
        if (error) throw error;
        const done = new Set(chunk.map((e) => e[0]));
        store.set(
          PENDING,
          store.get(PENDING, []).filter((e) => !done.has(e[0])),
        );
      }
    },
    // 下載其他裝置的逐筆紀錄（依上傳時間往後接；第一次只抓最近 180 天）
    async pullAttempts() {
      const ck = `sh:cloud:cursor:${this.user.id}`;
      let cursor =
        store.get(ck, null) || new Date(Date.now() - 180 * 864e5).toISOString();
      const got = [];
      for (;;) {
        const { data, error } = await this.sb
          .from("attempts")
          .select("id,subject,qid,ok,ms,mode,answered_at,created_at")
          .gte("created_at", cursor)
          .order("created_at")
          .limit(1000);
        if (error) throw error;
        got.push(...data);
        if (data.length) cursor = data[data.length - 1].created_at;
        if (data.length < 1000) break;
      }
      const log = getLog();
      const have = new Set(log.map((e) => e[0]));
      let added = 0;
      for (const r of got)
        if (!have.has(r.id)) {
          have.add(r.id);
          log.push([
            r.id,
            r.subject,
            r.qid,
            r.ok ? 1 : 0,
            Date.parse(r.answered_at),
            r.ms,
            r.mode,
          ]);
          added++;
        }
      if (added) {
        log.sort((a, b) => a[4] - b[4]);
        store.set(LOG, log.slice(-LOG_MAX));
      }
      store.set(ck, cursor);
      return added > 0;
    },
    localState() {
      const o = {
        prog: {},
        stars: {},
        read: {},
        reset: {},
        T: store.get("sh:T", {}),
      };
      for (const { id: s } of DB.index || []) {
        o.prog[s] = getProg(s);
        o.stars[s] = [...getStars(s)];
        o.read[s] = [...getRead(s)];
        const r = store.get(K.reset(s), 0);
        if (r) o.reset[s] = r;
      }
      return o;
    },
    async syncState() {
      if (!this.user) return false;
      await loadIndex();
      const { data, error } = await this.sb
        .from("user_state")
        .select("data")
        .maybeSingle();
      if (error) throw error;
      const L = this.localState();
      const M = mergeState(L, data?.data || {});
      const changed = JSON.stringify(L) !== JSON.stringify(M);
      this.applying = true;
      try {
        for (const s of Object.keys(M.prog)) {
          store.set(K.prog(s), M.prog[s]);
          store.set(K.star(s), M.stars[s]);
          store.set(K.read(s), M.read[s]);
          if (M.reset[s]) store.set(K.reset(s), M.reset[s]);
        }
        store.set("sh:T", M.T);
      } finally {
        this.applying = false;
      }
      const { error: e2 } = await this.sb.from("user_state").upsert({
        user_id: this.user.id,
        data: M,
        updated_at: new Date().toISOString(),
      });
      if (e2) throw e2;
      return changed;
    },
    async sync() {
      if (!this.user || this.busy) return;
      this.busy = true;
      this.status = "syncing";
      this.emit();
      let changed = false;
      try {
        await this.flush();
        changed = (await this.pullAttempts()) || changed;
        changed = (await this.syncState()) || changed;
        this.lastSync = Date.now();
        store.set("sh:cloud:lastSync", this.lastSync);
        this.status = "";
        this.error = "";
      } catch (e) {
        console.error(e);
        this.status = "error";
        this.error = e?.message || String(e);
      } finally {
        this.busy = false;
        this.emit(changed);
      }
    },
  };
  onStoreSet = (k) => {
    if (Cloud.applying) return;
    const m = k.match(/^sh:([^:]+):(progress|stars|read|resetT)$/);
    if (!m) return;
    if (m[2] === "stars" || m[2] === "read") {
      const T = store.get("sh:T", {});
      T[`${m[2]}:${m[1]}`] = Date.now();
      store.set("sh:T", T);
    }
    Cloud.stateSoon();
  };
  document.addEventListener("visibilitychange", () => {
    if (!Cloud.user) return;
    if (document.hidden) Cloud.flush().catch(() => {});
    else if (Date.now() - (Cloud.lastSync || 0) > 60e3) Cloud.sync();
  });
  const userName = (u) =>
    u?.user_metadata?.display_name ||
    u?.user_metadata?.full_name ||
    u?.user_metadata?.name ||
    u?.email ||
    "";
  const userAvatar = (u) =>
    u?.user_metadata?.custom_avatar || u?.user_metadata?.avatar_url || "";
  function paintAcct() {
    const b = $("#acctBtn");
    if (!b) return;
    const u = Cloud.user;
    b.classList.toggle("signed", !!u);
    b.classList.toggle("err", Cloud.status === "error");
    b.setAttribute(
      "aria-label",
      u ? `學習軌跡（已登入：${userName(u)}）` : "學習軌跡與登入",
    );
    const av = userAvatar(u);
    b.innerHTML = av
      ? `<img src="${esc(av)}" alt="" referrerpolicy="no-referrer">`
      : ic("user");
  }

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
      nav.innerHTML = `<a href="#/">所有科目</a><a href="#/s/${sid}"${cur("subject")}>${esc(s?.meta.short || "總覽")}總覽</a><a href="#/s/${sid}/practice"${cur("practice")}>練習區</a>${s?.meta.mock ? `<a href="#/s/${sid}/mock"${cur("mock")}>模擬考</a>` : ""}<a href="#/s/${sid}/analysis"${cur("analysis")}>考題分析</a><a href="#/s/${sid}/sheet"${cur("sheet")}>速記・圖解</a><a href="#/report?sid=${sid}"${cur("report")}>回報 / 回饋</a>`;
    } else {
      nav.innerHTML = `<a href="#/"${cur("home")}>所有科目</a><a href="#/practice"${cur("practice")}>練習區</a><a href="#/me"${cur("me")}>學習軌跡</a><a href="#/report"${cur("report")}>回報 / 回饋</a>`;
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
        T(
          sid ? `#/s/${sid}/practice` : "#/practice",
          "pen",
          "練習",
          "practice",
        ) +
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
  // 作答 / 翻卡時手機底部選單不要擋題目：往下捲收起，往上捲或捲到底再出現
  function autoHideTabbar() {
    let y0 = scrollY;
    const f = () => {
      const y = scrollY,
        atEnd = y + innerHeight >= document.documentElement.scrollHeight - 8;
      if (Math.abs(y - y0) < 6 && !atEnd) return;
      document.body.classList.toggle("tb-hide", y > y0 && y > 40 && !atEnd);
      y0 = y;
    };
    addEventListener("scroll", f, { passive: true });
    onLeave(() => {
      removeEventListener("scroll", f);
      document.body.classList.remove("tb-hide");
    });
  }
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
      if (seg[0] === "me") return await pageMe();
      if (seg[0] === "practice") return await pagePracticePick();
      if (seg[0] === "play" && !seg[1]) return await pageGames();
      if (seg[0] === "play" && GAMES.some((g) => g.id === seg[1]))
        return await pageGame(seg[1]);
      if (seg[0] === "s" && seg[1]) {
        const sid = seg[1];
        if (seg.length === 2) return await pageSubject(sid);
        if (seg[2] === "c" && seg[3])
          return await pageChapter(sid, seg[3], seg[4] || "summary", q);
        if (seg[2] === "sheet") return await pageSheet(sid, seg[3] || "", q);
        if (seg[2] === "practice") return await pagePractice(sid, q);
        if (seg[2] === "mock") return await pageMock(sid, q);
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
          `<a class="btn primary" href="#/">${ic("home")}回首頁</a><a class="egg-dice" href="#/play" aria-label="迷路了？來玩小遊戲" title="迷路了？">🎲</a>`,
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
        // 短儲存格（例：「✅ 直接接觸」、細菌名）不換行，避免字被拆到兩行
        $$("td", t).forEach((td) => {
          const n = td.textContent.trim().length;
          if (n <= (td.cellIndex === 0 ? 16 : 12)) td.classList.add("nw");
        });
        // 不換行反而撐出橫向捲軸的話，就放回去讓它換行
        requestAnimationFrame(() => {
          const w = t.parentElement;
          if (w.clientWidth && w.scrollWidth > w.clientWidth + 1)
            $$("td.nw", t).forEach((td) => td.classList.remove("nw"));
        });
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
      cc: cssVar("--colony-c"),
      cw: cssVar("--colony-w"),
      cs: cssVar("--colony-seed"),
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
        const colr = c.kind === "c" ? C.cc : c.kind === "w" ? C.cw : C.cs;
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
                ? `<a class="btn primary lg" href="${hasPractice ? `#/s/${last.meta.id}/practice` : "#/practice"}">${ic("pen")}${hasPractice ? "繼續練習" : "開始練習"}</a>`
                : ""
            }
          </div>
        </div>
        <figure class="plate-fig">
          <div class="plate-wrap"><canvas id="plate" role="img" aria-label="${hasPractice ? `你的練習菌落：已作答 ${totals.done} 題，其中 ${totals.right} 題答對、${totals.wrong} 題答錯` : "示意培養皿，開始練習後會依作答紀錄長出菌落"}"></canvas></div>
          <figcaption><span>${hasPractice ? `你的練習菌落 — 已作答 <b class="num">${totals.done}</b> 題` : ""}
            ${hasPractice ? `<span class="plate-legend"><span><i style="background:var(--colony-c)"></i>答對 ${totals.right}</span><span><i style="background:var(--colony-w)"></i>答錯 ${totals.wrong}</span></span>` : ""}</span></figcaption>
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
        if (cv) {
          mountPlate(cv, coloniesFromProgress(subs));
          // 彩蛋：連點培養皿 5 下
          let n = 0,
            h = 0;
          cv.addEventListener("click", () => {
            clearTimeout(h);
            h = setTimeout(() => (n = 0), 600);
            if (++n === 5) findEgg("🧫 培養皿裡長出了⋯⋯小遊戲！");
          });
        }
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
  // ------------------------------------------------------------ pages: 小遊戲（出題邏輯在 games.js）
  const GAMES = [
    {
      id: "sudoku",
      name: "數獨",
      en: "Sudoku",
      blurb: "經典 9×9。",
      rules:
        "每一橫列、每一直行、每個 3×3 宮都要剛好放進 1–9 各一次。填錯的數字會變紅並記一次錯誤。",
    },
    {
      id: "killer",
      name: "殺手數獨",
      en: "Killer Sudoku",
      blurb: "虛線籠子和總和，外加零星幾個提示數字。",
      rules:
        "規則同數獨；另外每個虛線籠子裡的數字加起來要等於左上角的總和，籠子裡的數字也不能重複。小技巧：任何一橫列、一直行、一宮加起來都是 45。",
    },
    {
      id: "nonogram",
      name: "數織",
      en: "Nonogram",
      blurb: "15×15 的方格，照著每一行的數字線索畫出圖案。",
      rules:
        "格子外的數字代表那一橫列（由左到右）或那一直行（由上到下）依序有幾段連續塗黑的格子，每段之間至少隔一格空白。每一盤都只靠逐行推理就能解完，不用猜。",
    },
  ];
  const GAME_ART = {
    sudoku: `<svg viewBox="0 0 60 60"><rect x="1" y="1" width="58" height="58" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20.3 1v58M39.7 1v58M1 20.3h58M1 39.7h58" stroke="currentColor" stroke-width="1" opacity=".35"/><g font-family="var(--f-serif)" font-size="13" text-anchor="middle" fill="currentColor"><text x="10.7" y="15">5</text><text x="49.3" y="15">3</text><text x="30" y="34.5" fill="var(--violet)">7</text><text x="10.7" y="54">1</text><text x="49.3" y="54" fill="var(--violet)">9</text></g></svg>`,
    killer: `<svg viewBox="0 0 60 60"><rect x="1" y="1" width="58" height="58" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><g fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="2.5 2" opacity=".75"><path d="M5 5h31v12H17v14H5z"/><path d="M40 5h15v31H40z"/><path d="M21 21h15v15H21zM5 35h12v20H5z"/><path d="M21 40h34v15H21z"/></g><g font-family="var(--f-mono)" font-size="5.5" fill="var(--violet)"><text x="7" y="11">17</text><text x="42" y="11">9</text><text x="23" y="27">6</text><text x="7" y="41">11</text><text x="23" y="46">20</text></g></svg>`,
    nonogram: `<svg viewBox="0 0 60 60"><rect x="1" y="1" width="58" height="58" rx="4" fill="none" stroke="currentColor" stroke-width="2"/><g fill="currentColor"><rect x="13" y="8" width="8" height="8"/><rect x="39" y="8" width="8" height="8"/><rect x="8" y="16" width="44" height="8" fill="var(--violet)"/><rect x="8" y="24" width="44" height="8" fill="var(--violet)"/><rect x="13" y="32" width="34" height="8"/><rect x="21" y="40" width="18" height="6"/><rect x="26" y="46" width="8" height="6"/></g></svg>`,
  };
  const gameKey = (id) => `sh:game:${id}`;
  const gameCards = () =>
    `<div class="game-cards">${GAMES.map((g) => {
      const s = store.get(gameKey(g.id), null),
        best = store.get("sh:game:best", {})[g.id];
      const meta = [
        s && !s.done
          ? `<span class="pill violet"><span class="dot"></span>進行中 ${fmtTime(s.elapsed)}</span>`
          : "",
        best ? `<span class="pill line">最佳 ${fmtTime(best)}</span>` : "",
      ].join("");
      return `<a class="card game-card" href="#/play/${g.id}">
        <div class="game-art" aria-hidden="true">${GAME_ART[g.id]}</div>
        <div class="eyebrow"><b>${g.en}</b> · Expert</div>
        <h3>${g.name}</h3>
        <p>${g.blurb}</p>
        <div class="game-card-meta">${meta}<span class="go">${s && !s.done ? "繼續玩" : "開始"} ${ic("arrowR")}</span></div>
      </a>`;
    }).join("")}</div>`;
  const gameHintNote = `<p class="game-note small">${ic("help")}<span>三種都只有 <b>Expert</b> 難度。卡關時按「提示」，會告訴你下一步可以從哪一格推起；數織的提示還會先幫你找出放錯的格子。</span></p>`;

  async function pageGames() {
    setChrome(null, "play");
    render(`
      <div class="wrap">
        <header style="padding-top:28px">
          <div class="eyebrow">Take a break</div>
          <h1 class="display h-l" style="margin-top:12px">讀累了？來玩小遊戲</h1>
          <p class="lede">三種邏輯謎題，每盤都是隨機產生、保證唯一解。進度自動存在這台裝置，下次回來可以接著玩。</p>
        </header>
        <div class="section" style="padding-top:32px">${gameCards()}${gameHintNote}</div>
      </div>`);
  }

  // 出題放在 Web Worker，殺手數獨要算好一陣子也不會卡住畫面；Worker 開不起來（例如 file://）就直接算
  let gameWorker = null;
  const stopGameWorker = () => {
    gameWorker?.terminate();
    gameWorker = null;
  };
  function generateGame(id) {
    stopGameWorker();
    const direct = () =>
      new Promise((res, rej) =>
        setTimeout(() => {
          try {
            res(window.SH_GAMES[id].generate());
          } catch (e) {
            rej(e);
          }
        }, 30),
      );
    try {
      gameWorker = new Worker(
        document.querySelector('script[src*="games.js"]').src,
      );
    } catch {
      return direct();
    }
    const w = gameWorker;
    return new Promise((res, rej) => {
      w.onmessage = (e) => {
        stopGameWorker();
        e.data.ok ? res(e.data.game) : rej(new Error(e.data.error));
      };
      w.onerror = (e) => {
        e.preventDefault();
        stopGameWorker();
        direct().then(res, rej);
      };
      w.postMessage(id);
    });
  }

  function newGameState(id, g) {
    const base = { hints: 0, elapsed: 0, done: false };
    if (id === "nonogram")
      return { ...g, ...base, cells: Array(g.W * g.H).fill(0), err: [] };
    const puzzle = g.puzzle || Array(81).fill(0);
    return {
      ...base,
      puzzle,
      solution: g.solution,
      cages: g.cages || null,
      vals: puzzle.slice(),
      notes: Array(81).fill(0),
      locked: Array(81).fill(0),
      mistakes: 0,
      sel: -1,
      notesMode: false,
    };
  }

  async function pageGame(id) {
    const meta = GAMES.find((g) => g.id === id);
    setChrome(null, "play");
    const sudokuLike = id !== "nonogram";
    render(`
      <div class="wrap">
        <nav class="crumbs" aria-label="路徑"><a href="#/play">小遊戲</a><span class="sep">/</span><span>${meta.name}</span></nav>
        <header class="game-head">
          <div>
            <div class="eyebrow"><b>${meta.en}</b> · Expert</div>
            <h1 class="display h-l" style="margin-top:12px">${meta.name}</h1>
          </div>
          <div class="game-stats">
            <div class="fact"><b class="num" id="gTime">0:00</b><span>時間</span></div>
            <div class="fact"><b class="num" id="gHints">0</b><span>提示</span></div>
            ${sudokuLike ? `<div class="fact"><b class="num" id="gMiss">0</b><span>錯誤</span></div>` : ""}
            <button class="btn sm" type="button" id="gNew">${ic("shuffle")}新的一盤</button>
          </div>
        </header>
        <div class="game-layout">
          <div class="game-board-wrap"><div id="gBoard"></div></div>
          <aside class="game-side" id="gSide"></aside>
        </div>
        <details class="game-rules"><summary>${ic("help")}玩法</summary><p>${meta.rules}</p></details>
      </div>`);

    const board = $("#gBoard"),
      side = $("#gSide"),
      newBtn = $("#gNew");
    let S = store.get(gameKey(id), null);
    let alive = true,
      dispose = null,
      last = 0,
      ticks = 0;
    const save = () => S && store.set(gameKey(id), S);
    const tick = () => {
      const now = performance.now();
      if (S && !S.done && last && !document.hidden) S.elapsed += now - last;
      last = document.hidden ? 0 : now;
      $("#gTime").textContent = fmtTime(S?.elapsed || 0);
      if (++ticks % 10 === 0) save();
    };
    const timer = setInterval(tick, 500);
    const onVis = () => {
      tick();
      save();
    };
    document.addEventListener("visibilitychange", onVis);
    onLeave(() => {
      alive = false;
      clearInterval(timer);
      document.removeEventListener("visibilitychange", onVis);
      tick();
      save();
      dispose?.();
      stopGameWorker();
    });

    const stats = () => {
      $("#gHints").textContent = S.hints;
      if (sudokuLike) $("#gMiss").textContent = S.mistakes;
    };
    const winPanel = () => {
      const best = store.get("sh:game:best", {})[id];
      side.innerHTML = `<div class="card game-win">
        <div class="eyebrow">Solved</div>
        <h2 class="display h-m">完成！</h2>
        <div class="game-win-facts">
          <div class="fact"><b class="num">${fmtTime(S.elapsed)}</b><span>用時</span></div>
          <div class="fact"><b class="num">${S.hints}</b><span>提示</span></div>
          ${sudokuLike ? `<div class="fact"><b class="num">${S.mistakes}</b><span>錯誤</span></div>` : ""}
        </div>
        <p class="small muted">${best && Math.round(S.elapsed) <= best ? "這是你目前最快的紀錄。" : best ? `最佳紀錄 ${fmtTime(best)}。` : ""}休息夠了就回去讀書吧。</p>
        <div class="game-tools"><button class="btn primary" type="button" data-again>${ic("shuffle")}再來一盤</button><a class="btn" href="#/">回首頁</a></div>
      </div>`;
      side
        .querySelector("[data-again]")
        .addEventListener("click", () => fresh());
    };
    const finish = () => {
      S.done = true;
      S.sel = -1;
      tick();
      save();
      const best = store.get("sh:game:best", {});
      if (!best[id] || S.elapsed < best[id]) {
        best[id] = Math.round(S.elapsed);
        store.set("sh:game:best", best);
      }
      board.classList.add("solved");
      winPanel();
      toast(`完成！用時 ${fmtTime(S.elapsed)}`);
    };
    const ui = {
      board,
      side,
      save,
      stats,
      finish,
      msg: (html) => {
        const m = $("#gMsg");
        if (m) m.innerHTML = html;
      },
    };
    const start = () => {
      dispose?.();
      board.classList.remove("solved");
      newBtn.disabled = false;
      stats();
      dispose = (sudokuLike ? mountSudoku : mountNonogram)(id, S, ui);
      if (S.done) {
        board.classList.add("solved");
        winPanel();
      }
    };
    const fresh = async () => {
      dispose?.();
      dispose = null;
      S = null;
      newBtn.disabled = true;
      board.className = "game-loading";
      board.innerHTML = `<div class="boot" aria-label="出題中"><span></span><span></span><span></span></div><p class="small muted">${id === "killer" ? "正在出一盤唯一解的殺手數獨，可能要幾秒⋯" : "出題中⋯"}</p>`;
      side.innerHTML = "";
      let g;
      try {
        g = await generateGame(id);
      } catch (e) {
        if (!alive) return;
        board.innerHTML = `<p>出題失敗：<span class="mono">${esc(e.message)}</span></p><button class="btn" type="button" id="gRetry">${ic("rotate")}再試一次</button>`;
        $("#gRetry").addEventListener("click", () => fresh());
        return;
      }
      if (!alive) return;
      S = newGameState(id, g);
      save();
      start();
    };
    let armed = 0;
    newBtn.addEventListener("click", () => {
      if (S && !S.done && S.elapsed > 15e3 && !armed) {
        newBtn.innerHTML = `${ic("alert")}再按一次放棄這盤`;
        armed = setTimeout(() => {
          armed = 0;
          newBtn.innerHTML = `${ic("shuffle")}新的一盤`;
        }, 3000);
        return;
      }
      clearTimeout(armed);
      armed = 0;
      newBtn.innerHTML = `${ic("shuffle")}新的一盤`;
      fresh();
    });
    if (S) start();
    else fresh();
  }

  const gameKeyOK = (e) =>
    $("#cmdk").hidden && !e.target.matches?.("input, textarea, select");

  // 數獨 / 殺手數獨：回傳 dispose
  function mountSudoku(id, S, ui) {
    const GM = window.SH_GAMES,
      killer = id === "killer",
      { board, side } = ui;
    const cageOf = new Int16Array(81).fill(-1),
      cageHead = new Map();
    if (killer)
      S.cages.forEach((c, k) => {
        c.cells.forEach((i) => (cageOf[i] = k));
        cageHead.set(c.cells[0], c.sum);
      });
    board.className = `sd-board${killer ? " killer" : ""}`;
    board.setAttribute("role", "grid");
    board.setAttribute("aria-label", killer ? "殺手數獨盤面" : "數獨盤面");
    board.innerHTML = [...Array(81)]
      .map((_, i) => {
        const r = (i / 9) | 0,
          c = i % 9;
        let cls = "sd-cell";
        if (c === 2 || c === 5) cls += " bx-r";
        if (r === 2 || r === 5) cls += " bx-b";
        let cage = "";
        if (killer) {
          const same = (j, ok) => ok && cageOf[j] === cageOf[i];
          const sides = [
            !same(i - 9, r > 0) && "t",
            !same(i + 1, c < 8) && "r",
            !same(i + 9, r < 8) && "b",
            !same(i - 1, c > 0) && "l",
          ].filter(Boolean);
          cage = `<span class="cage ${sides.join(" ")}"></span>${cageHead.has(i) ? `<span class="cg-sum">${cageHead.get(i)}</span>` : ""}`;
        }
        return `<button type="button" class="${cls}" data-i="${i}" tabindex="-1">${cage}<span class="sd-in"></span></button>`;
      })
      .join("");
    side.innerHTML = `
      <div class="game-msg" id="gMsg" aria-live="polite">${killer ? "先找總和很小或很大的籠子（例如 2 格 = 3 只能是 1、2），再用「每一宮總和 45」去推。" : "點一格，再按數字或用鍵盤輸入。"}</div>
      <div class="sd-pad">${[1, 2, 3, 4, 5, 6, 7, 8, 9].map((d) => `<button type="button" class="sd-key" data-d="${d}"><b>${d}</b><small></small></button>`).join("")}</div>
      <div class="game-tools">
        <button class="btn" type="button" id="gUndo">${ic("rotate")}復原</button>
        <button class="btn" type="button" id="gErase">${ic("x")}擦除</button>
        <button class="btn" type="button" id="gNotes" aria-pressed="false">${ic("pen")}筆記</button>
        <button class="btn accent" type="button" id="gHint">${ic("bolt")}提示</button>
      </div>
      <p class="small muted game-keys hide-touch">鍵盤：數字鍵填入、<kbd>Shift</kbd>+數字寫筆記、<kbd>N</kbd> 切換筆記、方向鍵移動、<kbd>Backspace</kbd> 擦除、<kbd>H</kbd> 提示、<kbd>${IS_MAC ? "⌘" : "Ctrl"}</kbd>+<kbd>Z</kbd> 復原</p>`;
    const cells = $$(".sd-cell", board),
      keys = $$(".sd-key", side);
    const undo = [];
    let flash = -1;

    const paint = () => {
      const sv = S.sel >= 0 ? S.vals[S.sel] : 0;
      const peers = new Set(S.sel >= 0 ? GM.peers[S.sel] : []);
      cells.forEach((el, i) => {
        const v = S.vals[i],
          given = S.puzzle[i] > 0;
        el.classList.toggle("given", given);
        el.classList.toggle("hinted", !given && !!S.locked[i]);
        el.classList.toggle("err", !!v && v !== S.solution[i]);
        el.classList.toggle("sel", i === S.sel);
        el.classList.toggle("peer", peers.has(i));
        el.classList.toggle("same", !!sv && v === sv && i !== S.sel);
        el.classList.toggle("flash", i === flash);
        el.lastElementChild.innerHTML = v
          ? `<span class="v">${v}</span>`
          : S.notes[i]
            ? `<span class="nt">${[1, 2, 3, 4, 5, 6, 7, 8, 9].map((d) => `<i>${S.notes[i] & (1 << d) ? d : ""}</i>`).join("")}</span>`
            : "";
        el.setAttribute(
          "aria-label",
          `第 ${((i / 9) | 0) + 1} 橫列第 ${(i % 9) + 1} 直行${killer && cageHead.has(i) ? `，籠子總和 ${cageHead.get(i)}` : ""}：${v || "空白"}`,
        );
      });
      const left = Array(10).fill(9);
      S.vals.forEach((v, i) => v && v === S.solution[i] && left[v]--);
      keys.forEach((k) => {
        const d = +k.dataset.d;
        k.querySelector("small").textContent = left[d] || "";
        k.disabled = !left[d] || S.done;
      });
      const nb = $("#gNotes");
      if (nb) {
        nb.setAttribute("aria-pressed", S.notesMode ? "true" : "false");
        nb.classList.toggle("on", S.notesMode);
      }
      ui.stats();
    };
    const setCell = (ch, i, v, n) => {
      ch.push([i, S.vals[i], S.notes[i]]);
      S.vals[i] = v;
      S.notes[i] = n;
    };
    const clearPeers = (ch, i, d) => {
      for (const j of GM.peers[i])
        if (S.notes[j] & (1 << d))
          setCell(ch, j, S.vals[j], S.notes[j] & ~(1 << d));
    };
    const commit = (ch, track = true) => {
      if (track && ch.length) undo.push(ch);
      ui.save();
      paint();
      if (S.vals.every((v, i) => v === S.solution[i])) {
        ui.finish();
        paint();
      }
    };
    const editable = (i) => !S.done && i >= 0 && !S.puzzle[i] && !S.locked[i];
    const input = (d, asNote = S.notesMode) => {
      const i = S.sel;
      if (!editable(i)) return;
      const ch = [];
      if (asNote) {
        if (S.vals[i]) return;
        setCell(ch, i, 0, S.notes[i] ^ (1 << d));
      } else if (S.vals[i] === d) setCell(ch, i, 0, 0);
      else {
        setCell(ch, i, d, 0);
        if (d !== S.solution[i]) S.mistakes++;
        else clearPeers(ch, i, d);
      }
      flash = -1;
      commit(ch);
    };
    const erase = () => {
      const i = S.sel;
      if (!editable(i) || (!S.vals[i] && !S.notes[i])) return;
      const ch = [];
      setCell(ch, i, 0, 0);
      commit(ch);
    };
    const doUndo = () => {
      const ch = undo.pop();
      if (!ch || S.done) return;
      for (const [i, v, n] of ch.reverse())
        if (!S.locked[i]) ((S.vals[i] = v), (S.notes[i] = n));
      ui.save();
      paint();
    };
    const toggleNotes = () => {
      S.notesMode = !S.notesMode;
      paint();
    };
    const hint = () => {
      if (S.done) return;
      const grid = S.vals.map((v, i) => (v === S.solution[i] ? v : 0));
      const prefer = S.sel >= 0 && !grid[S.sel] ? S.sel : -1;
      const h = killer
        ? GM.killer.hint(grid, S.solution, S.cages, prefer)
        : GM.sudoku.hint(grid, S.solution, prefer);
      if (!h) return;
      const ch = [];
      setCell(ch, h.i, h.d, 0);
      clearPeers(ch, h.i, h.d);
      S.locked[h.i] = 1;
      S.hints++;
      S.sel = flash = h.i;
      const where = `第 ${((h.i / 9) | 0) + 1} 橫列第 ${(h.i % 9) + 1} 直行`;
      ui.msg(
        h.why === "naked"
          ? `<b>${where}</b>：把同一橫列、直行、宮${killer ? "和籠子總和" : ""}已有的數字刪掉後，這格只剩 <b>${h.d}</b>。`
          : h.why === "hidden"
            ? `<b>${h.d}</b> 在這一${h.unit}裡只剩 <b>${where}</b> 能放。`
            : `這一步需要進階技巧，直接揭曉 <b>${where}</b> 是 <b>${h.d}</b>。`,
      );
      commit(ch, false);
    };

    const onClick = (e) => {
      const el = e.target.closest(".sd-cell");
      if (!el || S.done) return;
      S.sel = +el.dataset.i;
      flash = -1;
      paint();
    };
    board.addEventListener("click", onClick);
    keys.forEach((k) => k.addEventListener("click", () => input(+k.dataset.d)));
    $("#gUndo").addEventListener("click", doUndo);
    $("#gErase").addEventListener("click", erase);
    $("#gNotes").addEventListener("click", toggleNotes);
    $("#gHint").addEventListener("click", hint);
    const MOVE = { ArrowUp: -9, ArrowDown: 9, ArrowLeft: -1, ArrowRight: 1 };
    const onKey = (e) => {
      if (!gameKeyOK(e) || S.done) return;
      if (e.metaKey || e.ctrlKey) {
        if (e.key.toLowerCase() === "z") {
          e.preventDefault();
          doUndo();
        }
        return;
      }
      if (e.altKey) return;
      const m = /^(?:Digit|Numpad)([1-9])$/.exec(e.code);
      if (m) {
        e.preventDefault();
        input(+m[1], e.shiftKey || S.notesMode);
      } else if (MOVE[e.key]) {
        e.preventDefault();
        const i = S.sel < 0 ? 40 : S.sel,
          d = MOVE[e.key],
          n = i + d;
        if (
          n < 0 ||
          n > 80 ||
          (d === -1 && i % 9 === 0) ||
          (d === 1 && i % 9 === 8)
        )
          return;
        S.sel = n;
        paint();
      } else if (["Backspace", "Delete", "0"].includes(e.key)) {
        e.preventDefault();
        erase();
      } else if (e.key === "n" || e.key === "N") toggleNotes();
      else if (e.key === "h" || e.key === "H") hint();
    };
    addEventListener("keydown", onKey);
    paint();
    return () => {
      removeEventListener("keydown", onKey);
      board.removeEventListener("click", onClick);
    };
  }

  // 數織：cells 0 = 未填、1 = 塗黑、2 = 打叉
  function mountNonogram(id, S, ui) {
    const NG = window.SH_GAMES.nonogram,
      { board, side } = ui,
      { W, H } = S;
    const row = (i) => (i / W) | 0,
      col = (i) => i % W;
    let mode = 1,
      cur = -1,
      flash = -1,
      hl = null;
    const undo = [];
    const maxR = Math.max(...S.rows.map((r) => r.length || 1));
    board.className = "ng-board";
    board.setAttribute("role", "grid");
    board.setAttribute("aria-label", `數織 ${W}×${H} 盤面`);
    board.tabIndex = 0;
    board.style.gridTemplateColumns = `auto repeat(${W}, var(--cs))`;
    const clue = (c) =>
      (c.length ? c : [0]).map((n) => `<span>${n}</span>`).join("");
    const edge = (n, N) => (n % 5 === 4 && n < N - 1 ? " bx" : "");
    let html = `<div class="ng-corner"></div>`;
    S.cols.forEach((c, x) => {
      html += `<div class="ng-clue col${edge(x, W)}" data-col="${x}">${clue(c)}</div>`;
    });
    for (let y = 0; y < H; y++) {
      html += `<div class="ng-clue row${edge(y, H)}" data-row="${y}">${clue(S.rows[y])}</div>`;
      for (let x = 0; x < W; x++)
        html += `<div class="ng-cell${edge(x, W) ? " bx-r" : ""}${edge(y, H) ? " bx-b" : ""}" data-i="${y * W + x}"></div>`;
    }
    board.innerHTML = html;
    side.innerHTML = `
      <div class="game-msg" id="gMsg" aria-live="polite">先從數字加起來接近 15 的行下手，例如 15 格裡的「8」中間 1 格一定是黑的。</div>
      <div class="seg ng-mode" role="group" aria-label="點格子時">
        <button type="button" data-mode="1" aria-pressed="true"><i class="ng-sw f"></i>塗黑</button>
        <button type="button" data-mode="2" aria-pressed="false"><i class="ng-sw x"></i>打叉</button>
      </div>
      <div class="game-tools">
        <button class="btn" type="button" id="gUndo">${ic("rotate")}復原</button>
        <button class="btn accent" type="button" id="gHint">${ic("bolt")}提示</button>
      </div>
      <p class="small muted game-keys">按住拖曳可以一次畫一整排${IS_TOUCH ? "" : "；右鍵直接打叉。鍵盤：方向鍵移動、<kbd>Space</kbd> 塗黑、<kbd>X</kbd> 打叉、<kbd>Backspace</kbd> 清除、<kbd>H</kbd> 提示"}。</p>`;
    const cells = $$(".ng-cell", board),
      rowClues = $$(".ng-clue.row", board),
      colClues = $$(".ng-clue.col", board);

    const fit = () => {
      const avail = board.parentElement.clientWidth;
      const cs = Math.floor(avail / (W + maxR * 0.62 + 0.8));
      board.style.setProperty("--cs", `${Math.max(15, Math.min(30, cs))}px`);
    };
    const runs = (idx) => NG.runsOf(idx.map((i) => (S.cells[i] === 1 ? 1 : 0)));
    const same = (a, b) =>
      (a.length ? a : [0]).join() === (b.length ? b : [0]).join();
    const paint = () => {
      const err = new Set(S.err);
      cells.forEach((el, i) => {
        const v = S.cells[i];
        el.classList.toggle("f", v === 1);
        el.classList.toggle("x", v === 2);
        el.classList.toggle("err", err.has(i));
        el.classList.toggle("flash", i === flash);
        el.classList.toggle("cur", i === cur);
        el.classList.toggle(
          "hl",
          cur >= 0 && (row(i) === row(cur) || col(i) === col(cur)),
        );
      });
      for (let y = 0; y < H; y++) {
        const idx = [...Array(W)].map((_, x) => y * W + x);
        rowClues[y].classList.toggle("done", same(runs(idx), S.rows[y]));
        rowClues[y].classList.toggle(
          "hint",
          hl?.kind === "row" && hl.idx === y,
        );
      }
      for (let x = 0; x < W; x++) {
        const idx = [...Array(H)].map((_, y) => y * W + x);
        colClues[x].classList.toggle("done", same(runs(idx), S.cols[x]));
        colClues[x].classList.toggle(
          "hint",
          hl?.kind === "col" && hl.idx === x,
        );
      }
      ui.stats();
    };
    const solved = () =>
      S.solution.every((s, i) =>
        s === 1 ? S.cells[i] === 1 : S.cells[i] !== 1,
      );
    const commit = (ch, track = true) => {
      if (track && ch.length) undo.push(ch);
      ui.save();
      paint();
      if (solved()) {
        cur = -1;
        ui.finish();
        paint();
      }
    };
    const setCell = (ch, i, v) => {
      if (S.cells[i] === v) return;
      ch.push([i, S.cells[i]]);
      S.cells[i] = v;
    };

    // 拖曳：鎖定在起點那一橫列或直行；塗的時候只動空格，清的時候只清同一種記號
    let stroke = null;
    const strokeTo = (i) => {
      const { i0, v, act, ch } = stroke;
      const r0 = row(i0),
        c0 = col(i0);
      if (!stroke.axis && i !== i0)
        stroke.axis =
          Math.abs(row(i) - r0) <= Math.abs(col(i) - c0) ? "r" : "c";
      const step = stroke.axis === "c" ? W : 1;
      const to = stroke.axis === "c" ? row(i) * W + c0 : r0 * W + col(i);
      for (let j = i0; ; j += to >= i0 ? step : -step) {
        if (act === 0 ? S.cells[j] === v : S.cells[j] === 0)
          setCell(ch, j, act);
        if (j === to) break;
      }
      cur = to;
      paint();
    };
    const cellAt = (e) => {
      const el = document.elementFromPoint(e.clientX, e.clientY);
      return el && el.closest ? el.closest(".ng-cell") : null;
    };
    const onDown = (e) => {
      const el = e.target.closest(".ng-cell");
      if (!el || S.done || (e.button !== 0 && e.button !== 2)) return;
      e.preventDefault();
      const i = +el.dataset.i,
        v = e.button === 2 ? 2 : mode;
      const act = S.cells[i] === v ? 0 : v;
      stroke = { i0: i, v, act, ch: [], axis: null };
      S.err = [];
      flash = -1;
      setCell(stroke.ch, i, act);
      cur = i;
      paint();
      board.setPointerCapture(e.pointerId);
    };
    const onMove = (e) => {
      if (!stroke) return;
      const el = cellAt(e);
      if (el) strokeTo(+el.dataset.i);
    };
    const onUp = () => {
      if (!stroke) return;
      const ch = stroke.ch;
      stroke = null;
      commit(ch);
    };
    const doUndo = () => {
      const ch = undo.pop();
      if (!ch || S.done) return;
      for (const [i, v] of ch.reverse()) S.cells[i] = v;
      S.err = [];
      ui.save();
      paint();
    };
    const hint = () => {
      if (S.done) return;
      const wrong = [];
      S.cells.forEach((v, i) => {
        if ((v === 1 && !S.solution[i]) || (v === 2 && S.solution[i]))
          wrong.push(i);
      });
      S.hints++;
      hl = null;
      if (wrong.length) {
        S.err = wrong;
        flash = -1;
        ui.msg(
          `有 <b>${wrong.length}</b> 格放錯了，已用紅色標出來。改掉之後再按一次提示，就會告訴你下一步。`,
        );
        commit([], false);
        return;
      }
      const known = S.cells.map((v) => (v === 1 ? 1 : v === 2 ? 0 : -1));
      const st = NG.propagate(S.rows, S.cols, known, true);
      let i, why;
      if (st) {
        i = st.at;
        hl = st.line;
        const name = st.line.kind === "row" ? "橫列" : "直行";
        why = `看第 <b>${st.line.idx + 1}</b> ${name}的線索（已標出）：不管怎麼排，這格都一定是${st.grid[i] ? "<b>黑的</b>" : "<b>空白</b>"}。`;
      } else {
        i = S.cells.findIndex((v) => v === 0);
        why = "直接揭曉一格。";
      }
      if (i < 0) return;
      const ch = [];
      setCell(ch, i, S.solution[i] ? 1 : 2);
      S.err = [];
      flash = cur = i;
      ui.msg(why);
      commit(ch, false);
    };
    const setMode = (m) => {
      mode = m;
      $$(".ng-mode button", side).forEach((b) =>
        b.setAttribute(
          "aria-pressed",
          +b.dataset.mode === m ? "true" : "false",
        ),
      );
    };
    const keyMark = (v) => {
      if (cur < 0 || S.done) return;
      const ch = [];
      setCell(ch, cur, S.cells[cur] === v ? 0 : v);
      S.err = [];
      commit(ch);
    };
    const onKey = (e) => {
      if (!gameKeyOK(e) || S.done) return;
      if (e.metaKey || e.ctrlKey) {
        if (e.key.toLowerCase() === "z") {
          e.preventDefault();
          doUndo();
        }
        return;
      }
      const MOVE = {
        ArrowUp: [-1, 0],
        ArrowDown: [1, 0],
        ArrowLeft: [0, -1],
        ArrowRight: [0, 1],
      };
      if (MOVE[e.key]) {
        e.preventDefault();
        if (cur < 0) cur = 0;
        else {
          const y = Math.min(H - 1, Math.max(0, row(cur) + MOVE[e.key][0])),
            x = Math.min(W - 1, Math.max(0, col(cur) + MOVE[e.key][1]));
          cur = y * W + x;
        }
        paint();
      } else if (
        e.key === " " ||
        e.key === "Enter" ||
        e.key === "f" ||
        e.key === "F"
      ) {
        if (
          e.key === " " &&
          e.target !== board &&
          e.target.matches("button, a")
        )
          return;
        e.preventDefault();
        keyMark(1);
      } else if (e.key === "x" || e.key === "X") keyMark(2);
      else if (e.key === "Backspace" || e.key === "Delete") {
        e.preventDefault();
        keyMark(S.cells[cur] || 0);
      } else if (e.key === "h" || e.key === "H") hint();
    };
    const noMenu = (e) => {
      if (e.target.closest(".ng-cell")) e.preventDefault();
    };
    board.addEventListener("pointerdown", onDown);
    board.addEventListener("pointermove", onMove);
    board.addEventListener("pointerup", onUp);
    board.addEventListener("pointercancel", onUp);
    board.addEventListener("contextmenu", noMenu);
    $$(".ng-mode button", side).forEach((b) =>
      b.addEventListener("click", () => setMode(+b.dataset.mode)),
    );
    $("#gUndo").addEventListener("click", doUndo);
    $("#gHint").addEventListener("click", hint);
    addEventListener("keydown", onKey);
    addEventListener("resize", fit);
    fit();
    paint();
    return () => {
      removeEventListener("keydown", onKey);
      removeEventListener("resize", fit);
      board.removeEventListener("pointerdown", onDown);
      board.removeEventListener("pointermove", onMove);
      board.removeEventListener("pointerup", onUp);
      board.removeEventListener("pointercancel", onUp);
      board.removeEventListener("contextmenu", noMenu);
    };
  }

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
          ${m.mock ? `<a class="card flash-cta" href="#/s/${sid}/mock"><span class="ico">${ic("clock")}</span><span><b>${esc(m.mock.title || "模擬考")}</b><span>照老師公告的範圍與配分出一份完整考卷，限時 ${m.mock.minutes} 分鐘，交卷後才看分數與詳解。</span></span><span class="go">去考一份 ${ic("arrowR")}</span></a>` : ""}
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
              <div class="chips">${sourcesOf(subj)
                .map(
                  (s) =>
                    `<label class="chip"><input type="checkbox" name="src" value="${s.key}"${srcSel.has(s.key) ? " checked" : ""}>${box}${s.label}<span class="n">${subj.questions.filter((x) => s.match(x) && !x.imageOnly).length}</span></label>`,
                )
                .join("")}</div>
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
              Cloud.user
                ? "確定要清除本科目的作答紀錄與收藏嗎？已登入，其他裝置上的進度也會一起清除（學習軌跡的逐筆紀錄會保留）。這個動作無法復原。"
                : "確定要清除這台裝置上本科目的所有作答紀錄與收藏嗎？（學習軌跡的逐筆紀錄會保留）這個動作無法復原。",
            )
          ) {
            store.set(K.reset(sid), Date.now());
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
    autoHideTabbar();
    const S = {
      i: 0,
      ans: pool.map(() => null),
      streak: 0,
      best: 0,
      t0: Date.now(),
      qt: Date.now(),
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
          <span class="quiz-nav">${pool.length > 1 ? `<button class="btn sm ghost" type="button" id="prevTop" aria-label="上一題"${S.i > 0 ? "" : " disabled"}>${ic("arrowL")}</button>` : ""}<span class="prog"><b>${S.i + 1}</b> / ${pool.length}</span>${pool.length > 1 ? `<button class="btn sm ghost" type="button" id="nextTop" aria-label="${S.i === pool.length - 1 ? "看結果" : "下一題"}">${ic("arrowR")}</button>` : ""}</span>
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
      S.qt = Date.now();
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
      record(sid, qq.id, ok, { ms: Date.now() - S.qt, mode: "mcq" });
      paint(false);
      $("#next")?.focus({ preventScroll: true });
    };
    const selfGrade = (ok) => {
      const qq = pool[S.i];
      S.ans[S.i] = { k: null, ok, self: true };
      S.last = S.i;
      S.streak = ok ? S.streak + 1 : 0;
      record(sid, qq.id, ok, { ms: Date.now() - S.qt, mode: "self" });
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
      $("#nextTop")?.addEventListener("click", () => go(S.i + 1));
      $("#prevTop")?.addEventListener("click", () => go(S.i - 1));
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
              ${c.done >= 10 && c.w === 0 ? `<a class="btn ghost" href="#/play">🎮 全對！獎勵你玩一盤</a>` : ""}
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

  // ------------------------------------------------------------ mock exam
  // subject.json 的 "mock"：老師公告的範圍與配分。sections[].from 每一項是
  // "章節 id"、"章節 id:考點1|考點2"（只取這些考點）或 "章節 id:!考點1|考點2"（排除這些考點）
  const mockKey = (sid) => `sh:${sid}:mock`;
  const mockHistKey = (sid) => `sh:${sid}:mockHist`;
  const mockOK = (q) =>
    q.type === "mcq" &&
    !q.imageOnly &&
    (q.options || []).length >= 2 &&
    (q.answer || []).length > 0;
  function mockSectionPool(subj, sec) {
    const rules = sec.from.map((f) => {
      const [ch, t = ""] = f.split(":");
      const neg = t.startsWith("!");
      const set = new Set((neg ? t.slice(1) : t).split("|").filter(Boolean));
      return { ch, neg, set };
    });
    return subj.questions.filter(
      (q) =>
        mockOK(q) &&
        rules.some((r) => {
          if (q.chapter !== r.ch) return false;
          if (!r.set.size) return true;
          const hit = (q.topics || []).some((t) => r.set.has(t));
          return r.neg ? !hit : hit;
        }),
    );
  }
  // 每個單元：約 newRatio 的模擬新題，其餘從考古／課堂原題隨機抽；不夠就互相補
  function mockDraw(subj) {
    const M = subj.meta.mock;
    const src = sourcesOf(subj);
    const isNew = (q) => src.find((s) => s.match(q))?.kind === "new";
    const used = new Set();
    const ids = [],
      sec = [];
    M.sections.forEach((s, si) => {
      const pool = shuffle(
        mockSectionPool(subj, s).filter((q) => !used.has(q.id)),
      );
      const nw = pool.filter(isNew),
        old = pool.filter((q) => !isNew(q));
      const nNew = Math.min(nw.length, Math.round(s.n * (M.newRatio ?? 0.2)));
      const pick = [...old.slice(0, s.n - nNew), ...nw.slice(0, nNew)];
      if (pick.length < s.n)
        pick.push(...nw.slice(nNew, nNew + s.n - pick.length));
      for (const q of shuffle(pick)) {
        used.add(q.id);
        ids.push(q.id);
        sec.push(si);
      }
    });
    return {
      ids,
      sec,
      ans: ids.map(() => null),
      flag: ids.map(() => false),
      i: 0,
      t0: Date.now(),
      dl: Date.now() + M.minutes * 60e3,
    };
  }
  function mockScore(subj, st) {
    const M = subj.meta.mock;
    const secs = M.sections.map((s) => ({
      title: s.title,
      points: s.points,
      n: 0,
      right: 0,
      got: 0,
    }));
    st.sec.forEach((si) => secs[si].n++);
    st.ids.forEach((id, k) => {
      const q = subj.qById[id],
        x = secs[st.sec[k]];
      if (q && (q.answer || []).includes(st.ans[k])) {
        x.right++;
        x.got += x.points / x.n;
      }
    });
    const total = secs.filter((x) => x.n).reduce((a, x) => a + x.points, 0);
    const got = secs.reduce((a, x) => a + x.got, 0);
    return { secs, total, got };
  }
  const fmtPts = (v) => (Math.round(v * 10) / 10).toString();

  async function pageMock(sid, q) {
    const subj = await loadSubject(sid);
    setChrome(sid, "mock");
    const M = subj.meta.mock;
    if (!M)
      return render(
        emptyState(
          "這個科目還沒有模擬考",
          "老師公告考試範圍與配分後就會加上。",
          `<a class="btn primary" href="#/s/${sid}/practice">去練習區</a>`,
        ),
      );
    if (q.start) return runMock(subj, q.start === "new");
    const cur = store.get(mockKey(sid), null);
    const hist = store.get(mockHistKey(sid), []);
    const nQ = M.sections.reduce((a, s) => a + s.n, 0);
    const total = M.sections.reduce((a, s) => a + s.points, 0);
    const rows = M.sections
      .map((s) => {
        const pool = mockSectionPool(subj, s);
        const chs = [...new Set(s.from.map((f) => f.split(":")[0]))]
          .map((c) => subj.chMap[c]?.title)
          .filter(Boolean);
        return `<tr><td><b>${esc(s.title)}</b><div class="small muted">${esc(chs.join("、"))}</div></td><td class="n">${s.points}</td><td class="n">${Math.min(s.n, pool.length)}</td><td class="n muted">${pool.length}</td></tr>`;
      })
      .join("");
    const left = cur ? cur.dl - Date.now() : 0;
    render(`
      <div class="wrap">
        <nav class="crumbs" aria-label="路徑"><a href="#/s/${sid}">${esc(subj.meta.title)}</a><span class="sep">/</span><span>模擬考</span></nav>
        <header style="padding-top:14px">
          <div class="eyebrow">Mock exam${M.when ? ` · 正式考試 ${esc(M.when)}` : ""}</div>
          <h1 class="display h-l" style="margin-top:12px">${esc(M.title || "模擬考")}</h1>
          <p class="lede">照老師公告的範圍和配分出一份完整考卷：題目從考古與課堂原題隨機抽，約兩成混入模擬新題。作答時不顯示答案，交卷後才看分數和詳解，每次抽到的題目都不一樣。</p>
        </header>
        <div class="section mock-intro" style="padding-top:28px">
          <div class="card panel">
            <div class="mock-facts">
              <div class="fact"><b>${M.minutes}</b><span>分鐘</span></div>
              <div class="fact"><b>${nQ}</b><span>題單選</span></div>
              <div class="fact"><b>${total}</b><span>滿分</span></div>
            </div>
            <div class="toolbar" style="margin-top:20px">
              ${
                cur
                  ? `<a class="btn accent lg" href="#/s/${sid}/mock?start=1">${ic("arrowR")}繼續作答${left > 0 ? `（剩 ${fmtTime(left)}）` : "（時間到，交卷）"}</a><a class="btn" href="#/s/${sid}/mock?start=new">${ic("shuffle")}放棄這份，重新抽題</a>`
                  : `<a class="btn accent lg" href="#/s/${sid}/mock?start=new">${ic("clock")}開始模擬考</a>`
              }
            </div>
            <p class="small muted" style="margin:16px 0 0">中途離開或重新整理都會保留進度，計時不會暫停。<span class="hide-touch">鍵盤：<kbd>A</kbd>–<kbd>E</kbd> 作答、<kbd>←</kbd><kbd>→</kbd> 換題、<kbd>F</kbd> 標記。</span></p>
          </div>
          <div class="card panel" style="margin-top:14px">
            <h3>範圍與配分</h3>
            <p class="sub">${esc(M.note || "")}</p>
            <div class="mock-table-wrap"><table class="mock-table">
              <thead><tr><th>單元</th><th class="n">配分</th><th class="n">題數</th><th class="n">題庫</th></tr></thead>
              <tbody>${rows}</tbody>
            </table></div>
          </div>
          ${
            hist.length
              ? `<div class="card panel" style="margin-top:14px"><h3>歷次成績</h3><div class="mock-table-wrap"><table class="mock-table">
              <thead><tr><th>日期</th><th class="n">得分</th><th class="n">答對</th><th class="n">用時</th></tr></thead>
              <tbody>${hist
                .slice(-8)
                .reverse()
                .map(
                  (h) =>
                    `<tr><td>${new Date(h.t).toLocaleString("zh-TW", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" })}</td><td class="n"><b>${fmtPts(h.got)}</b> / ${h.total}</td><td class="n">${h.right} / ${h.n}</td><td class="n">${fmtTime(h.ms)}</td></tr>`,
                )
                .join("")}</tbody></table></div></div>`
              : ""
          }
        </div>
      </div>`);
  }

  function runMock(subj, fresh) {
    const sid = subj.meta.id;
    const M = subj.meta.mock;
    let S = fresh ? null : store.get(mockKey(sid), null);
    if (S && S.ids.some((id) => !subj.qById[id])) S = null;
    if (!S) S = mockDraw(subj);
    const save = () => store.set(mockKey(sid), S);
    save();
    if (fresh) history.replaceState(null, "", `#/s/${sid}/mock?start=1`);
    autoHideTabbar();
    const pool = S.ids.map((id) => subj.qById[id]);
    let timer = 0,
      confirming = false;
    const answered = () => S.ans.filter((x) => x !== null).length;
    const left = () => Math.max(0, S.dl - Date.now());
    const dots = () =>
      `<div class="dots" role="group" aria-label="題目導覽">${pool
        .map(
          (_, k) =>
            `<button type="button" class="${k === S.i ? "cur" : S.flag[k] ? "f" : S.ans[k] !== null ? "a" : ""}" data-go="${k}" aria-label="第 ${k + 1} 題${S.ans[k] !== null ? "，已作答" : "，未作答"}${S.flag[k] ? "，已標記" : ""}"></button>`,
        )
        .join("")}</div>`;
    const top = () => `<div class="quiz-top">
        <a class="btn ghost sm" href="#/s/${sid}/mock" aria-label="離開（保留進度）">${ic("x")}<span class="hide-s">離開</span></a>
        <span class="prog"><b>${S.i + 1}</b> / ${pool.length}</span>
        <div class="quiz-stats">
          <span title="已作答">${ic("pen")}<b class="num">${answered()}</b></span>
          <span title="剩餘時間" class="mock-clock${left() < 5 * 60e3 ? " low" : ""}">${ic("clock")}<span class="num" id="clock">${fmtTime(left())}</span></span>
          <button class="btn sm primary" type="button" id="submitTop">${confirming ? "確認交卷" : "交卷"}</button>
        </div>
      </div>`;
    const card = () => {
      const qq = pool[S.i],
        a = S.ans[S.i];
      const last = S.i === pool.length - 1;
      return `<article class="card qcard" aria-labelledby="qstem">
        <div class="q-meta"><span class="pill line">${esc(M.sections[S.sec[S.i]].title)}</span>${S.flag[S.i] ? `<span class="pill warn">${ic("flag")}已標記</span>` : ""}</div>
        <p class="q-stem" id="qstem">${esc(qq.stem)}</p>
        <div class="options" role="radiogroup" aria-label="選項">${qq.options
          .map(
            (o) =>
              `<button type="button" role="radio" aria-checked="${a === o.k}" class="option${a === o.k ? " picked" : ""}" data-k="${o.k}"><span class="key">${o.k}</span><span class="txt">${esc(o.t)}</span></button>`,
          )
          .join("")}</div>
        <div class="q-foot">
          <button class="btn sm ghost" type="button" id="flag" aria-pressed="${S.flag[S.i]}">${ic("flag")}${S.flag[S.i] ? "取消標記" : "標記這題"}</button>
          <span class="spacer"></span>
          ${S.i > 0 ? `<button class="btn sm" type="button" id="prev" aria-label="上一題">${ic("arrowL")}</button>` : ""}
          ${last ? `<button class="btn primary" type="button" id="submit">${confirming ? "確認交卷" : "交卷"}${ic("arrowR")}</button>` : `<button class="btn ${a ? "primary" : ""}" type="button" id="next">${a ? "下一題" : "跳過"}${ic("arrowR")}</button>`}
        </div>
      </article>`;
    };
    const paint = (keepConfirm) => {
      if (!keepConfirm) confirming = false;
      $app.innerHTML = `<div class="wrap"><div class="quiz">${top()}${dots()}<div id="qslot">${card()}</div>
        <div class="shortcut-hint" aria-hidden="true"><span><kbd>A</kbd>–<kbd>E</kbd> 作答</span><span><kbd>←</kbd><kbd>→</kbd> 上／下一題</span><span><kbd>F</kbd> 標記</span></div></div></div>`;
      $$("[data-go]").forEach((b) =>
        b.addEventListener("click", () => go(+b.dataset.go)),
      );
      $$(".option").forEach((b) =>
        b.addEventListener("click", () => pick(b.dataset.k)),
      );
      $("#next")?.addEventListener("click", () => go(S.i + 1));
      $("#prev")?.addEventListener("click", () => go(S.i - 1));
      $("#flag").addEventListener("click", toggleFlag);
      $("#submit")?.addEventListener("click", trySubmit);
      $("#submitTop").addEventListener("click", trySubmit);
    };
    const go = (k) => {
      if (k < 0 || k >= pool.length) return;
      S.i = k;
      save();
      paint();
      if (innerWidth < 760) scrollTo({ top: 0 });
    };
    const pick = (k) => {
      S.ans[S.i] = S.ans[S.i] === k ? null : k;
      save();
      paint();
    };
    const toggleFlag = () => {
      S.flag[S.i] = !S.flag[S.i];
      save();
      paint();
    };
    const trySubmit = () => {
      const miss = pool.length - answered();
      const flagged = S.flag.filter(Boolean).length;
      if ((miss || flagged) && !confirming) {
        confirming = true;
        paint(true);
        toast(
          `${miss ? `還有 ${miss} 題沒作答` : ""}${miss && flagged ? "、" : ""}${flagged ? `${flagged} 題有標記` : ""}，按「確認交卷」送出`,
        );
        return;
      }
      finish(false);
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
      const key = { 1: "A", 2: "B", 3: "C", 4: "D", 5: "E" }[k] || k;
      if ($(`.option[data-k="${key}"]`)) {
        e.preventDefault();
        pick(key);
      } else if (e.key === "ArrowRight" || e.key === "Enter") {
        if (e.key === "Enter" && document.activeElement?.tagName === "BUTTON")
          return;
        e.preventDefault();
        go(S.i + 1);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(S.i - 1);
      } else if (key === "F") {
        e.preventDefault();
        toggleFlag();
      }
    };
    const stop = () => {
      clearInterval(timer);
      removeEventListener("keydown", onKey);
    };
    const finish = (timeUp) => {
      stop();
      const ms = Math.min(Date.now(), S.dl) - S.t0;
      const { secs, total, got } = mockScore(subj, S);
      const right = secs.reduce((a, x) => a + x.right, 0);
      pool.forEach((qq, k) => {
        if (S.ans[k] !== null)
          record(sid, qq.id, qq.answer.includes(S.ans[k]), { mode: "mock" });
      });
      const hist = store.get(mockHistKey(sid), []);
      hist.push({ t: Date.now(), got, total, right, n: pool.length, ms });
      store.set(mockHistKey(sid), hist.slice(-30));
      store.set(mockKey(sid), null);
      const p = total ? Math.round((got / total) * 100) : 0;
      const miss = pool
        .map((qq, k) => ({ qq, a: S.ans[k] }))
        .filter((x) => !x.qq.answer.includes(x.a));
      const title =
        p >= 85
          ? "穩穩過關"
          : p >= 70
            ? "表現不錯"
            : p >= 60
              ? "低空飛過"
              : "還要再加油";
      render(
        `<div class="wrap"><div class="result">
        <div class="card result-hero">
          <div class="score-ring" style="--p:${p}"><div><b>${fmtPts(got)}</b><span>/ ${total} 分</span></div></div>
          <div>
            <div class="eyebrow">Mock exam · ${timeUp ? "時間到自動交卷" : `用時 ${fmtTime(ms)}`}</div>
            <h1 class="display h-m" style="margin:10px 0 6px">${title}</h1>
            <p class="muted" style="margin:0 0 18px">答對 <b class="num" style="color:var(--ink)">${right}</b> / ${pool.length} 題${pool.length - answered() ? `，${pool.length - answered()} 題沒作答` : ""}。作答結果已記進練習紀錄與錯題本。</p>
            <div class="toolbar">
              ${miss.length ? `<a class="btn accent" href="#/s/${sid}/practice?${qs({ ids: miss.map((x) => x.qq.id).join(","), start: 1 })}">${ic("rotate")}重做這 ${miss.length} 題</a>` : ""}
              <a class="btn primary" href="#/s/${sid}/mock?start=new">${ic("shuffle")}再考一份</a>
              ${p >= 90 ? `<a class="btn ghost" href="#/play">🎮 考這麼好，獎勵你玩一盤</a>` : ""}
              <a class="btn" href="#/s/${sid}/mock">回模擬考</a>
            </div>
          </div>
        </div>
        <div class="card panel" style="margin-top:14px"><h3>各單元得分</h3>
          <div class="mock-table-wrap"><table class="mock-table">
            <thead><tr><th>單元</th><th class="n">答對</th><th class="n">得分</th></tr></thead>
            <tbody>${secs
              .filter((x) => x.n)
              .map(
                (x) =>
                  `<tr><td>${esc(x.title)}<div class="mock-bar" aria-hidden="true"><i style="width:${(x.right / x.n) * 100}%"></i></div></td><td class="n">${x.right} / ${x.n}</td><td class="n"><b>${fmtPts(x.got)}</b> / ${x.points}</td></tr>`,
              )
              .join("")}</tbody>
          </table></div>
        </div>
        ${miss.length ? `<div class="section" style="padding-top:40px"><div class="eyebrow" style="margin-bottom:12px">答錯或沒作答 · ${miss.length}</div>${miss.map((x) => `<div class="mock-yours">${x.a ? `你選 (${x.a})` : "沒作答"}</div>${browseCard(subj, x.qq, true)}`).join("")}</div>` : ""}
      </div></div>`,
        () => bindTips($app),
      );
    };
    if (!left()) return finish(true);
    paint();
    timer = setInterval(() => {
      const el = $("#clock");
      if (!left()) {
        toast("時間到，已自動交卷");
        return finish(true);
      }
      if (el) {
        el.textContent = fmtTime(left());
        el.parentElement.classList.toggle("low", left() < 5 * 60e3);
      }
    }, 1000);
    addEventListener("keydown", onKey);
    onLeave(stop);
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
    autoHideTabbar();
    const S = {
      i: 0,
      flipped: false,
      res: pool.map(() => null),
      qt: Date.now(),
    };
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
      S.qt = Date.now();
      paint();
      if (innerWidth < 760) scrollTo({ top: 0 });
    };
    const know = (ok) => {
      S.res[S.i] = ok;
      record(sid, pool[S.i].id, ok, { ms: Date.now() - S.qt, mode: "card" });
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

  // ------------------------------------------------------------ 學習軌跡 / 登入
  // 答對率長條：rows = [{ label, n, c, href? }]，樣本少於 min 的列淡化
  function pctChart(rows, { caption = "", min = 5 } = {}) {
    const body = rows
      .map((r) => {
        const p = pct(r.c, r.n);
        const v = r.n ? `${p}%` : "—";
        const tip = `<b>${esc(r.label)}</b><div class="row">答對率 ${v}</div><div class="row" style="opacity:.7">${r.n} 次作答${r.n && r.n < min ? "（樣本少，僅供參考）" : ""}</div>`;
        const tag = r.href ? "a" : "div";
        return `<${tag} class="chart-row${r.n < min ? " few" : ""}" ${r.href ? `href="${r.href}"` : ""} tabindex="0" data-tip="${esc(tip)}" style="color:inherit;text-decoration:none"><span class="lab">${esc(r.label)}</span><span style="display:block"><span class="track" style="width:${p}%">${p ? `<i style="flex:1;background:var(--series-1)"></i>` : ""}</span></span><span class="val">${v}</span></${tag}>`;
      })
      .join("");
    const table = `<details class="data-table"><summary>以表格檢視${caption ? `（${esc(caption)}）` : ""}</summary><table><thead><tr><th>項目</th><th>作答次數</th><th>答對</th><th>答對率</th></tr></thead><tbody>${rows.map((r) => `<tr><td>${esc(r.label)}</td><td class="n">${r.n}</td><td class="n">${r.c}</td><td class="n">${r.n ? `${pct(r.c, r.n)}%` : "—"}</td></tr>`).join("")}</tbody></table></details>`;
    return `<div class="chart">${body}</div>${table}`;
  }

  const DAY = 864e5;
  const dayKey = (t) => {
    const d = new Date(t);
    return `${d.getFullYear()}-${pad2(d.getMonth() + 1)}-${pad2(d.getDate())}`;
  };
  const fmtWhen = (t) => {
    const d = new Date(t);
    return `${d.getMonth() + 1}/${d.getDate()} ${pad2(d.getHours())}:${pad2(d.getMinutes())}`;
  };

  function acctPanel() {
    const pend = store.get(PENDING, []).length;
    if (!Cloud.on)
      return `<div class="card panel acct"><div class="acct-ico">${ic("cloud")}</div><div><h3>雲端同步尚未設定</h3><p class="sub" style="margin:0">目前紀錄只存在這台裝置。在 <span class="mono">config.js</span> 填入 Supabase 設定後，這裡會出現登入按鈕，作答紀錄就能跨裝置保存。</p></div></div>`;
    const u = Cloud.user;
    if (!u) {
      const prov = CFG.authProviders || ["google", "email"];
      const LBL = { google: "Google", github: "GitHub", apple: "Apple" };
      const oauth = prov
        .filter((p) => p !== "email")
        .map((p) =>
          p === "google" && CFG.googleClientId
            ? `<div id="gsiBtn" class="gsi-btn"><span class="btn primary" aria-hidden="true">${ic("user")}用 Google 登入</span><div class="gsi-hit"></div></div>`
            : `<button class="btn primary" type="button" data-login="${esc(p)}">${ic("user")}用 ${esc(LBL[p] || p)} 登入</button>`,
        )
        .join("");
      const email = prov.includes("email")
        ? `<form class="acct-email" id="emailLogin"><label class="sr-only" for="loginEmail">Email</label><input id="loginEmail" type="email" required autocomplete="email" placeholder="Email"><label class="sr-only" for="loginPw">密碼</label><input id="loginPw" type="password" required minlength="6" autocomplete="current-password" placeholder="密碼（至少 6 個字元）"><div class="acct-email-btns"><button class="btn" type="submit" value="in">${ic("user")}登入</button><button class="btn ghost" type="submit" value="up">註冊新帳號</button></div></form>
          <p class="small acct-alt"><button class="linkish" type="button" id="magicBtn">忘記密碼？改用 Email 登入連結</button></p>`
        : "";
      return `<div class="card panel acct"><div class="acct-ico">${ic("cloud")}</div><div style="min-width:0;flex:1"><h3>登入，保存你的學習軌跡</h3><p class="sub">登入後，每一題的作答紀錄會存到你的帳號，換手機或電腦也看得到。${pend ? `這台裝置有 <b>${pend}</b> 筆紀錄還沒上傳，登入後會自動存到你的帳號。` : ""}</p>
        <div class="acct-actions">${oauth}</div>${email}
        ${Cloud.status === "error" ? `<p class="small" style="color:var(--bad);margin:12px 0 0">${ic("alert")} ${esc(Cloud.error)}</p>` : ""}</div></div>`;
    }
    const av = userAvatar(u);
    const st =
      Cloud.status === "syncing"
        ? "同步中…"
        : Cloud.status === "error"
          ? `<span style="color:var(--bad)">${ic("alert")} 同步失敗：${esc(Cloud.error)}</span>`
          : Cloud.lastSync
            ? `${ic("check")} 已同步 · ${fmtWhen(Cloud.lastSync)}${pend ? ` · ${pend} 筆待上傳` : ""}`
            : "尚未同步";
    return `<div class="card panel acct"><button class="acct-ico acct-av" type="button" id="avatarBtn" title="更換頭像" aria-label="更換頭像">${av ? `<img src="${esc(av)}" alt="" referrerpolicy="no-referrer">` : ic("user")}<span class="acct-av-badge">${ic("pen")}</span></button><input type="file" id="avatarFile" accept="image/*" hidden><div style="min-width:0;flex:1">
      <h3>${esc(userName(u))}</h3><p class="sub" style="margin:0">${u.email && u.email !== userName(u) ? `${esc(u.email)} · ` : ""}<span class="acct-status">${st}</span></p></div>
      <div class="acct-actions"><button class="btn sm" type="button" id="syncBtn"${Cloud.busy ? " disabled" : ""}>${ic("rotate")}立即同步</button><button class="btn sm ghost" type="button" id="nameBtn" aria-expanded="false" aria-controls="nameForm">${ic("user")}更改名稱</button><button class="btn sm ghost" type="button" id="pwBtn" aria-expanded="false" aria-controls="pwForm">${ic("pen")}設定密碼</button>${u.user_metadata?.custom_avatar ? `<button class="btn sm ghost" type="button" id="avatarReset">${ic("rotate")}恢復預設頭像</button>` : ""}<button class="btn sm ghost" type="button" id="logoutBtn">${ic("logout")}登出</button></div>
      <form class="acct-email" id="nameForm" hidden><label class="sr-only" for="newName">顯示名稱</label><input id="newName" type="text" maxlength="40" autocomplete="nickname" value="${esc(userName(u))}" placeholder="顯示名稱（留空恢復預設）"><button class="btn" type="submit">${ic("check")}儲存名稱</button></form>
      <form class="acct-email" id="pwForm" hidden><label class="sr-only" for="newPw">新密碼</label><input type="email" autocomplete="username" value="${esc(u.email || "")}" hidden><input id="newPw" type="password" required minlength="6" autocomplete="new-password" placeholder="新密碼（至少 6 個字元）"><button class="btn" type="submit">${ic("check")}儲存密碼</button></form></div>`;
  }

  function heatmap(days, weeks = 26) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const at = (i) =>
      new Date(today.getFullYear(), today.getMonth(), today.getDate() - i);
    const start = at(today.getDay() + 7 * (weeks - 1)); // 第一欄的星期日
    const lv = (n) => (!n ? 0 : n < 10 ? 1 : n < 30 ? 2 : n < 60 ? 3 : 4);
    let cols = "",
      months = "",
      lastM = -1;
    for (let w = 0; w < weeks; w++) {
      let cells = "";
      const first = new Date(
        start.getFullYear(),
        start.getMonth(),
        start.getDate() + w * 7,
      );
      const m = first.getMonth();
      months += `<span>${m !== lastM ? `${m + 1}月` : ""}</span>`;
      lastM = m;
      for (let d = 0; d < 7; d++) {
        const day = new Date(
          first.getFullYear(),
          first.getMonth(),
          first.getDate() + d,
        );
        if (day > today) {
          cells += `<i class="off"></i>`;
          continue;
        }
        const k = dayKey(day);
        const x = days.get(k) || { n: 0, c: 0 };
        const tip = `<b>${day.getMonth() + 1}/${day.getDate()}（${"日一二三四五六"[day.getDay()]}）</b><div class="row">${x.n ? `${x.n} 題 · 答對 ${pct(x.c, x.n)}%` : "沒有練習"}</div>`;
        cells += `<i class="l${lv(x.n)}" tabindex="0" data-tip="${esc(tip)}" aria-label="${k}：${x.n} 題"></i>`;
      }
      cols += `<span class="heat-col">${cells}</span>`;
    }
    const rows = [...days.entries()]
      .filter(([k]) => k >= dayKey(start))
      .sort((a, b) => (a[0] < b[0] ? 1 : -1));
    return `<div class="heat-scroll"><div class="heat">
      <div class="heat-months" aria-hidden="true"><span></span>${months}</div>
      <div class="heat-body"><span class="heat-days" aria-hidden="true"><span></span><span>一</span><span></span><span>三</span><span></span><span>五</span><span></span></span>${cols}</div>
    </div></div>
    <div class="heat-legend" aria-hidden="true">少<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>多<span class="muted">（1–9 · 10–29 · 30–59 · 60+ 題）</span></div>
    <details class="data-table"><summary>以表格檢視（每日練習）</summary><table><thead><tr><th>日期</th><th>題數</th><th>答對率</th></tr></thead><tbody>${rows.map(([k, x]) => `<tr><td>${k}</td><td class="n">${x.n}</td><td class="n">${pct(x.c, x.n)}%</td></tr>`).join("") || `<tr><td colspan="3" class="muted">還沒有紀錄</td></tr>`}</tbody></table></details>`;
  }

  function downloadLogCSV(log) {
    const cell = (v) => {
      const t = v == null ? "" : String(v);
      return /[",\n]/.test(t) ? `"${t.replace(/"/g, '""')}"` : t;
    };
    const csv =
      "﻿id,subject,qid,ok,answered_at,ms,mode\n" +
      log
        .map((e) =>
          [e[0], e[1], e[2], e[3], new Date(e[4]).toISOString(), e[5], e[6]]
            .map(cell)
            .join(","),
        )
        .join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
    a.download = `study-hub-log-${dayKey(Date.now())}.csv`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }

  async function pageMe() {
    const subs = await loadAllSubjects();
    setChrome(null, "me");
    const byId = Object.fromEntries(subs.map((s) => [s.meta.id, s]));
    const log = getLog();
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const at = (i) =>
      new Date(today.getFullYear(), today.getMonth(), today.getDate() - i);

    const days = new Map();
    for (const e of log) {
      const k = dayKey(e[4]);
      const d = days.get(k) || { n: 0, c: 0 };
      d.n++;
      d.c += e[3];
      days.set(k, d);
    }
    let streak = 0;
    for (let i = days.has(dayKey(today)) ? 0 : 1; days.has(dayKey(at(i))); i++)
      streak++;
    const wk = log.filter((e) => e[4] >= +at(6));
    const wkC = wk.reduce((a, e) => a + e[3], 0);

    // 每週答對 / 答錯
    const W = 12;
    const sun = at(today.getDay());
    const weekRows = [];
    for (let w = W - 1; w >= 0; w--) {
      const a = new Date(
        sun.getFullYear(),
        sun.getMonth(),
        sun.getDate() - 7 * w,
      );
      const b = +a + 7 * DAY;
      const es = log.filter((e) => e[4] >= +a && e[4] < b);
      const c = es.reduce((x, e) => x + e[3], 0);
      weekRows.push({
        label: w ? `${a.getMonth() + 1}/${a.getDate()} 那週` : "本週",
        segs: [
          { name: "答對", color: "var(--series-1)", v: c },
          { name: "答錯", color: "var(--series-2)", v: es.length - c },
        ],
      });
    }

    // 記憶曲線（距上次做同一題多久 → 答對率）與學習曲線（第幾次做 → 答對率）
    const byQ = new Map();
    for (const e of log) {
      const k = `${e[1]}|${e[2]}`;
      if (!byQ.has(k)) byQ.set(k, []);
      byQ.get(k).push(e);
    }
    const GAPS = [
      ["不到 1 天", 1],
      ["1–3 天", 3],
      ["3–7 天", 7],
      ["7–14 天", 14],
      ["14–30 天", 30],
      ["30 天以上", Infinity],
    ];
    const gap = GAPS.map(([label]) => ({ label, n: 0, c: 0 }));
    const NTH = ["第 1 次", "第 2 次", "第 3 次", "第 4 次", "第 5 次以上"];
    const nth = NTH.map((label) => ({ label, n: 0, c: 0 }));
    let reviewed = 0;
    for (const arr of byQ.values()) {
      arr.sort((a, b) => a[4] - b[4]);
      if (arr.length > 1) reviewed++;
      arr.forEach((e, i) => {
        const r = nth[Math.min(i, NTH.length - 1)];
        r.n++;
        r.c += e[3];
        if (!i) return;
        const g = (e[4] - arr[i - 1][4]) / DAY;
        const b = gap[GAPS.findIndex(([, lim]) => g < lim)];
        b.n++;
        b.c += e[3];
      });
    }

    const subjRows = subs
      .map((s) => {
        const es = log.filter((e) => e[1] === s.meta.id);
        return {
          label: s.meta.short || s.meta.title,
          href: `#/s/${s.meta.id}`,
          n: es.length,
          c: es.reduce((a, e) => a + e[3], 0),
        };
      })
      .filter((r) => r.n);

    const recent = log
      .slice(-12)
      .reverse()
      .map((e) => {
        const s = byId[e[1]];
        const q = s?.qById[e[2]];
        const stem = q ? q.stem.replace(/\s+/g, " ").slice(0, 160) : e[2];
        return `<a class="recent-row" href="#/s/${esc(e[1])}/q/${esc(e[2])}">
          <span class="res ${e[3] ? "ok" : "no"}">${ic(e[3] ? "check" : "x")}${e[3] ? "答對" : "答錯"}</span>
          <span class="stem">${esc(stem)}</span>
          <span class="meta">${esc(s?.meta.short || e[1])} · ${fmtWhen(e[4])}</span></a>`;
      })
      .join("");

    const legacy = subs.reduce((a, s) => a + subjectStats(s).done, 0);
    const empty = !log.length;
    render(
      `<div class="wrap">
      <header style="padding-top:14px">
        <div class="eyebrow">Learning log · 學習軌跡</div>
        <h1 class="display h-l" style="margin-top:12px">每一題，<br>都留下痕跡。</h1>
        <p class="lede">每次作答都會記下時間與對錯。累積下來，就能看到自己哪天讀最多、隔多久會忘、哪一科最需要回頭複習。</p>
      </header>
      <div id="acct" style="margin-top:28px">${acctPanel()}</div>
      ${
        empty
          ? `<div class="card empty" style="margin-top:14px"><div class="eyebrow">還沒有逐筆紀錄</div><h2 class="display">從下一題開始記錄</h2><p>學習軌跡從這次更新後開始累積${legacy ? `；之前做過的 ${legacy} 題只有「最後一次對錯」，沒有每次的時間，所以不會出現在圖表裡` : ""}。</p><a class="btn primary" href="#/practice">${ic("pen")}去練習</a></div>`
          : `
      <div class="tiles" style="margin-top:14px">
        <div class="tile"><div class="v">${log.length}</div><div class="l">總作答次數</div></div>
        <div class="tile"><div class="v">${days.size}<small>天</small></div><div class="l">有練習的日子</div></div>
        <div class="tile"><div class="v">${streak}<small>天</small></div><div class="l">目前連續練習</div></div>
        <div class="tile"><div class="v">${wk.length ? pct(wkC, wk.length) : "—"}${wk.length ? "<small>%</small>" : ""}</div><div class="l">近 7 天答對率（${wk.length} 題）</div></div>
      </div>
      <div class="card panel" style="margin-top:14px"><h3>練習日曆</h3><p class="sub">最近半年，每一格是一天，顏色越深代表那天做越多題</p>${heatmap(days)}</div>
      <div class="card panel" style="margin-top:14px"><h3>每週作答</h3><p class="sub">最近 12 週，答對與答錯的題數</p>${barChart(weekRows, { series: weekRows[0].segs.map(({ name, color }) => ({ name, color })), tableCaption: "每週作答" })}</div>
      <div class="grid2" style="margin-top:14px">
        <div class="card panel"><h3>記憶曲線</h3><p class="sub">同一題隔多久再做，答對率是多少。越往下掉得少，代表記得越牢。已重複練習 ${reviewed} 題；淡色列樣本少於 5 次。</p>${pctChart(gap, { caption: "記憶曲線" })}</div>
        <div class="card panel"><h3>學習曲線</h3><p class="sub">同一題做到第幾次時的答對率。越往下越高，代表重複練習有效。</p>${pctChart(nth, { caption: "學習曲線" })}</div>
      </div>
      <div class="grid2" style="margin-top:14px">
        <div class="card panel"><h3>各科答對率</h3><p class="sub">所有作答次數合計，點一列進入該科</p>${pctChart(subjRows, { caption: "各科" })}</div>
        <div class="card panel"><h3>最近作答</h3><p class="sub">點一題可以再做一次</p><div class="recent">${recent}</div></div>
      </div>`
      }
      <p class="small muted" style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap;align-items:center">
        ${log.length ? `<button class="btn sm" type="button" id="csvBtn">${ic("download")}下載作答紀錄（CSV）</button>` : ""}
        <span>這台裝置保留最近 ${LOG_MAX.toLocaleString()} 筆${Cloud.user ? "；完整紀錄在雲端，可在 Supabase 用 SQL 分析" : ""}。</span>
      </p>
    </div>`,
      () => {
        bindTips($app);
        bindAcct();
        const hs = $(".heat-scroll");
        if (hs) hs.scrollLeft = hs.scrollWidth; // 手機上先看到最近幾週
        $("#csvBtn")?.addEventListener("click", () => downloadLogCSV(getLog()));
      },
    );
  }
  function bindLogin(b) {
    b.addEventListener("click", async () => {
      b.disabled = true;
      try {
        await Cloud.signIn(b.dataset.login);
      } catch (e) {
        b.disabled = false;
        toast(`登入失敗：${e.message || e}`);
      }
    });
  }
  function bindAcct() {
    const gb = $("#gsiBtn");
    if (gb)
      Cloud.renderGoogle(gb).catch((e) => {
        console.error(e);
        // Google 按鈕載入失敗（例如被擋）時退回 Supabase 轉址登入
        gb.innerHTML = `<button class="btn primary" type="button" data-login="google">${ic("user")}用 Google 登入</button>`;
        bindLogin($("button", gb));
      });
    $$("[data-login]").forEach(bindLogin);
    $("#emailLogin")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.currentTarget;
      const v = $("#loginEmail", f).value.trim();
      const pw = $("#loginPw", f).value;
      const up = e.submitter?.value === "up";
      const btns = $$("button", f);
      btns.forEach((b) => (b.disabled = true));
      try {
        if (!up) {
          await Cloud.signInPassword(v, pw);
          toast("登入成功");
        } else if (await Cloud.signUp(v, pw)) toast("註冊完成，已登入");
        else
          f.outerHTML = `<p class="small" style="margin:14px 0 0">${ic("mail")} 確認信已寄到 <b>${esc(v)}</b>。點信裡的連結完成註冊，之後就能用 Email 和密碼登入。</p>`;
      } catch (err) {
        btns.forEach((b) => (b.disabled = false));
        toast(`${up ? "註冊" : "登入"}失敗：${err.message || err}`);
      }
    });
    // 沒設過密碼（以前用登入連結）或忘記密碼：寄登入連結，登入後再到「設定密碼」改
    $("#magicBtn")?.addEventListener("click", async (e) => {
      const btn = e.currentTarget;
      const inp = $("#loginEmail");
      const v = inp.value.trim();
      if (!v || !inp.checkValidity()) {
        inp.focus();
        return toast("請先在上方輸入 Email");
      }
      btn.disabled = true;
      try {
        await Cloud.signIn("email", v);
        btn.parentElement.innerHTML = `${ic("mail")} 登入連結已寄到 <b>${esc(v)}</b>。請用<b>這個瀏覽器</b>打開信裡的連結（在其他瀏覽器或 App 內開啟會登入失敗），登入後可以按「設定密碼」。`;
      } catch (err) {
        btn.disabled = false;
        toast(`寄送失敗：${err.message || err}`);
      }
    });
    $("#nameBtn")?.addEventListener("click", (e) => {
      const f = $("#nameForm");
      f.hidden = !f.hidden;
      e.currentTarget.setAttribute("aria-expanded", String(!f.hidden));
      if (!f.hidden) $("#newName", f).select();
    });
    $("#nameForm")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.currentTarget;
      const btn = $("button", f);
      btn.disabled = true;
      try {
        await Cloud.setName($("#newName", f).value.trim());
        toast("名稱已更新");
      } catch (err) {
        toast(`更改失敗：${err.message || err}`);
        btn.disabled = false;
      }
    });
    $("#pwBtn")?.addEventListener("click", (e) => {
      const f = $("#pwForm");
      f.hidden = !f.hidden;
      e.currentTarget.setAttribute("aria-expanded", String(!f.hidden));
      if (!f.hidden) $("#newPw", f).focus();
    });
    $("#avatarBtn")?.addEventListener("click", () => $("#avatarFile").click());
    $("#avatarFile")?.addEventListener("change", async (e) => {
      const file = e.currentTarget.files[0];
      if (!file) return;
      const btn = $("#avatarBtn");
      btn.classList.add("busy");
      btn.disabled = true;
      try {
        await Cloud.setAvatar(file);
        toast("頭像已更新");
      } catch (err) {
        console.error(err);
        toast(`更換失敗：${err.message || err}`);
        btn.classList.remove("busy");
        btn.disabled = false;
      }
    });
    $("#avatarReset")?.addEventListener("click", async (e) => {
      e.currentTarget.disabled = true;
      try {
        await Cloud.clearAvatar();
        toast("已恢復預設頭像");
      } catch (err) {
        e.currentTarget.disabled = false;
        toast(`操作失敗：${err.message || err}`);
      }
    });
    $("#pwForm")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const f = e.currentTarget;
      const btn = $("button", f);
      btn.disabled = true;
      try {
        await Cloud.setPassword($("#newPw", f).value);
        f.hidden = true;
        f.reset();
        toast("密碼已設定，下次可以用 Email 和密碼登入");
      } catch (err) {
        toast(`設定失敗：${err.message || err}`);
      } finally {
        btn.disabled = false;
      }
    });
    $("#syncBtn")?.addEventListener("click", () => Cloud.sync());
    $("#logoutBtn")?.addEventListener("click", async () => {
      await Cloud.signOut();
      toast("已登出；這台裝置上的紀錄仍會保留");
    });
  }
  // 登入狀態或同步結果改變時：學習軌跡頁重畫；首頁在資料有變時重畫
  addEventListener("sh:cloud", (e) => {
    const { seg } = parseHash();
    if (seg[0] === "me") {
      if (e.detail.changed) {
        const y = scrollY;
        pageMe().then(() => scrollTo({ top: y }));
      } else {
        const box = $("#acct");
        if (box) {
          box.innerHTML = acctPanel();
          bindAcct();
        }
      }
    } else if (!seg.length && e.detail.changed) pageHome();
  });

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
              toast(
                line
                  ? "已複製，開啟 LINE 後貼上送出"
                  : "已複製，貼到 LINE 傳給我",
              );
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
    // 彩蛋：只有搜「遊戲 / 數獨 / 數織 / game…」才會出現
    const items = [
      {
        g: "彩蛋",
        icon: "grid",
        t: "🎮 讀累了？來玩小遊戲",
        s: "你發現了隱藏頁面",
        k: "遊戲 小遊戲 玩 休息 game games play puzzle 彩蛋 egg",
        href: "#/play",
      },
      ...GAMES.map((g) => ({
        g: "彩蛋",
        icon: "grid",
        t: `${g.name} ${g.en}`,
        s: "Expert · 隱藏小遊戲",
        k: `${g.blurb} 遊戲 game`,
        href: `#/play/${g.id}`,
      })),
    ];
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
      if (s.meta.mock)
        items.push({
          g: "頁面",
          icon: "clock",
          t: "模擬考",
          s: s.meta.title,
          k: "mock exam 期中 考試",
          href: `#/s/${sid}/mock`,
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
          彩蛋: 4,
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
          "彩蛋",
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

  // ------------------------------------------------------------ easter eggs → #/play
  // 入口：連點首頁培養皿 5 下、連點頁尾「Study Hub」3 下、連點左上 logo 7 下、在頁面上直接打 play、
  // Konami code（↑↑↓↓←→←→BA）、連續切換深淺色 6 次、搜尋「遊戲」、404 頁的骰子、
  // 練習全對（10 題以上）或模擬考 90 分以上的結果頁
  function findEgg(msg) {
    toast(msg);
    setTimeout(() => (location.hash = "#/play"), 700);
  }
  // 在 ms 內連續觸發 times 次就開彩蛋
  const rapid = (el, times, ms, msg) => {
    let n = 0,
      h = 0;
    el?.addEventListener("click", () => {
      clearTimeout(h);
      h = setTimeout(() => (n = 0), ms);
      if (++n === times) {
        n = 0;
        findEgg(msg);
      }
    });
  };
  {
    const KONAMI = "ArrowUp ArrowUp ArrowDown ArrowDown ArrowLeft ArrowRight ArrowLeft ArrowRight b a";
    let typed = "",
      keys = [];
    addEventListener("keydown", (e) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (!cmdk.hidden || e.target.matches?.("input, textarea, select")) return;
      if (location.hash.startsWith("#/play") || $("#qslot")) return;
      keys = [...keys, e.key.length === 1 ? e.key.toLowerCase() : e.key].slice(-10);
      if (keys.join(" ") === KONAMI) {
        keys = [];
        return findEgg("🕹️ ↑↑↓↓←→←→BA，老玩家喔");
      }
      if (e.key.length !== 1) return;
      typed = (typed + e.key.toLowerCase()).slice(-4);
      if (typed === "play") findEgg("🎮 被你發現了！");
    });
    rapid($(".site-footer .sig"), 3, 600, "✨ 你找到彩蛋了");
    rapid($(".masthead .logo"), 7, 700, "🔬 菌落太多了，出去透透氣吧");
    rapid(themeBtn, 6, 900, "🌗 眼睛累了嗎？來玩點別的");
  }

  // boot: wait for marked (deferred) then route
  const boot = () => {
    route();
    paintAcct();
    Cloud.init();
  };
  if (window.marked) boot();
  else addEventListener("load", boot, { once: true });
})();
