/* Study Hub — 小遊戲的出題與解題（純邏輯，不碰 DOM）
 * window.SH_GAMES = { sudoku, killer, nonogram }；也可當 Web Worker 在背景出題
 * 三種都只出 expert：
 *   數獨      唯一解、最少提示數（逐格挖到再挖就不唯一），且只用唯一候選數 / 隱性唯一解不能解完
 *   殺手數獨  沒有提示數字、籠子 2–5 格，唯一解
 *   數織      15×15，唯一解且只靠逐行推理就能解完（不用猜）
 */
(() => {
  "use strict";
  const rand = (n) => Math.floor(Math.random() * n);
  const shuffle = (a) => {
    a = a.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = rand(i + 1);
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };
  const popc = (m) => {
    let c = 0;
    for (; m; c++) m &= m - 1;
    return c;
  };
  const digitsOf = (m) => {
    const out = [];
    for (let d = 1; d <= 9; d++) if (m & (1 << d)) out.push(d);
    return out;
  };
  const ALL = 0b1111111110;

  // ------------------------------------------------------------ 9×9 共用
  const ROW = (i) => (i / 9) | 0;
  const COL = (i) => i % 9;
  const BOX = (i) => ((ROW(i) / 3) | 0) * 3 + ((COL(i) / 3) | 0);
  const UNITS = [];
  for (let r = 0; r < 9; r++) UNITS.push([...Array(9)].map((_, c) => r * 9 + c));
  for (let c = 0; c < 9; c++) UNITS.push([...Array(9)].map((_, r) => r * 9 + c));
  for (let b = 0; b < 9; b++)
    UNITS.push(
      [...Array(9)].map(
        (_, k) => (((b / 3) | 0) * 3 + ((k / 3) | 0)) * 9 + (b % 3) * 3 + (k % 3),
      ),
    );
  const PEERS = [...Array(81)].map((_, i) => {
    const s = new Set();
    for (let j = 0; j < 81; j++)
      if (j !== i && (ROW(j) === ROW(i) || COL(j) === COL(i) || BOX(j) === BOX(i)))
        s.add(j);
    return [...s];
  });
  const NB4 = (i) => {
    const r = ROW(i),
      c = COL(i),
      out = [];
    if (r > 0) out.push(i - 9);
    if (r < 8) out.push(i + 9);
    if (c > 0) out.push(i - 1);
    if (c < 8) out.push(i + 1);
    return out;
  };

  // COMBOS[size][sum] = 所有 size 個不同數字加起來是 sum 的組合（bitmask）
  const COMBOS = [...Array(10)].map(() => [...Array(46)].map(() => []));
  for (let m = 2; m <= ALL; m += 2) {
    const ds = digitsOf(m);
    COMBOS[ds.length][ds.reduce((a, b) => a + b, 0)].push(m);
  }
  // 籠子已用了 used 這些數字，剩下的格子還能放哪些數字
  function cageAllow(c) {
    let m = 0;
    for (const combo of COMBOS[c.size][c.sum])
      if ((combo & c.used) === c.used) m |= combo;
    return m & ~c.used;
  }

  // cages: [{ sum, cells }]；回傳每格的候選數 bitmask（已填的格子為 0）
  function makeState(grid, cages) {
    const rowM = new Int32Array(9),
      colM = new Int32Array(9),
      boxM = new Int32Array(9);
    const cageOf = new Int16Array(81).fill(-1);
    const cs = cages
      ? cages.map((c, k) => {
          c.cells.forEach((i) => (cageOf[i] = k));
          return { sum: c.sum, size: c.cells.length, used: 0 };
        })
      : null;
    const g = Int8Array.from(grid);
    const st = { g, rowM, colM, boxM, cageOf, cs, ok: true };
    if (cages) st.cells = cages.map((c) => c.cells);
    for (let i = 0; i < 81; i++)
      if (g[i]) {
        const b = 1 << g[i];
        if ((rowM[ROW(i)] | colM[COL(i)] | boxM[BOX(i)]) & b) st.ok = false;
        g[i] = 0;
        place(st, i, Math.abs(grid[i]));
      }
    return st;
  }
  function place(st, i, d) {
    const b = 1 << d;
    st.g[i] = d;
    st.rowM[ROW(i)] |= b;
    st.colM[COL(i)] |= b;
    st.boxM[BOX(i)] |= b;
    if (st.cs && st.cageOf[i] >= 0) {
      const c = st.cs[st.cageOf[i]];
      if (c.used & b) st.ok = false;
      c.used |= b;
    }
  }
  function unplace(st, i) {
    const d = st.g[i],
      b = 1 << d;
    st.g[i] = 0;
    st.rowM[ROW(i)] &= ~b;
    st.colM[COL(i)] &= ~b;
    st.boxM[BOX(i)] &= ~b;
    if (st.cs && st.cageOf[i] >= 0) {
      const c = st.cs[st.cageOf[i]];
      c.used &= ~b;
    }
  }
  function cand(st, i) {
    let m = ALL & ~(st.rowM[ROW(i)] | st.colM[COL(i)] | st.boxM[BOX(i)]);
    if (st.cs && st.cageOf[i] >= 0) {
      m &= cageAllow(st.cs[st.cageOf[i]]);
    }
    return m;
  }

  // 回溯解題：limit 解就停；maxNodes 超過就丟 "abort"
  function solve(grid, { cages = null, limit = 2, random = false, maxNodes = Infinity } = {}) {
    const st = makeState(grid, cages);
    const sols = [];
    if (!st.ok) return sols;
    let nodes = 0;
    const order = (m) => (random ? shuffle(digitsOf(m)) : digitsOf(m));
    const cm = new Int32Array(81);
    // 每一步挑分支最少的選擇：某格的候選數，或某數字在某列 / 行 / 宮 / 籠子裡能放的格子
    const rec = () => {
      if (++nodes > maxNodes) throw new Error("abort");
      let best = -1,
        bm = 0,
        bc = 10;
      for (let i = 0; i < 81; i++)
        if (!st.g[i]) cm[i] = ALL & ~(st.rowM[ROW(i)] | st.colM[COL(i)] | st.boxM[BOX(i)]);
      // 籠子：只留「剩下的數字都還有格子可放」的組合
      if (st.cs)
        for (let k = 0; k < st.cs.length; k++) {
          const c = st.cs[k];
          let room = 0,
            allow = 0,
            must = ALL;
          for (const i of st.cells[k]) if (!st.g[i]) room |= cm[i];
          for (const combo of COMBOS[c.size][c.sum])
            if ((combo & c.used) === c.used && !(combo & ~c.used & ~room))
              (allow |= combo), (must &= combo);
          if (!allow) return false;
          c.allow = allow & ~c.used;
          c.must = must & ~c.used;
          for (const i of st.cells[k]) if (!st.g[i]) cm[i] &= c.allow;
        }
      for (let i = 0; i < 81; i++) {
        if (st.g[i]) continue;
        const c = popc(cm[i]);
        if (!c) return false;
        if (c < bc) (bc = c), (bm = cm[i]), (best = i);
      }
      if (best < 0) {
        sols.push(Array.from(st.g));
        return sols.length >= limit;
      }
      let digit = 0,
        spots = null;
      const scan = (cells, need) => {
        for (let d = 1; d <= 9 && bc > 1; d++) {
          if (!(need & (1 << d))) continue;
          const at = [];
          for (const i of cells) if (!st.g[i] && cm[i] & (1 << d)) at.push(i);
          if (!at.length) return false;
          if (at.length < bc) (bc = at.length), (digit = d), (spots = at);
        }
        return true;
      };
      if (bc > 1)
        for (const u of UNITS) {
          let have = 0;
          for (const i of u) if (st.g[i]) have |= 1 << st.g[i];
          if (!scan(u, ALL & ~have)) return false;
        }
      if (bc > 1 && st.cs)
        for (let k = 0; k < st.cs.length; k++) {
          if (!scan(st.cells[k], st.cs[k].must)) return false;
        }
      if (spots) {
        for (const i of random ? shuffle(spots) : spots) {
          place(st, i, digit);
          const done = rec();
          unplace(st, i);
          if (done) return true;
        }
        return false;
      }
      for (const d of order(bm)) {
        place(st, best, d);
        const done = rec();
        unplace(st, best);
        if (done) return true;
      }
      return false;
    };
    rec();
    return sols;
  }

  const fullGrid = () => solve(Array(81).fill(0), { limit: 1, random: true })[0];

  // 只用唯一候選數（naked single）與隱性唯一解（hidden single）能不能解完
  function singlesSolve(grid) {
    const st = makeState(grid, null);
    for (let progress = true; progress; ) {
      progress = false;
      for (let i = 0; i < 81; i++) {
        if (st.g[i]) continue;
        const m = cand(st, i);
        if (!m) return false;
        if (popc(m) === 1) {
          place(st, i, digitsOf(m)[0]);
          progress = true;
        }
      }
      for (const u of UNITS)
        for (let d = 1; d <= 9; d++) {
          let at = -1,
            n = 0,
            have = false;
          for (const i of u) {
            if (st.g[i] === d) have = true;
            else if (!st.g[i] && cand(st, i) & (1 << d)) (at = i), n++;
          }
          if (!have && n === 1) {
            place(st, at, d);
            progress = true;
          }
        }
    }
    return st.g.every((v) => v);
  }

  // 提示：依目前盤面（只含正確數字）找下一步；回傳 { i, d, why }
  function sudokuHint(grid, solution, cages, prefer = -1) {
    const st = makeState(grid, cages);
    for (let i = 0; i < 81; i++) {
      if (st.g[i]) continue;
      const m = cand(st, i);
      if (popc(m) === 1) return { i, d: solution[i], why: "naked" };
    }
    const names = ["橫列", "直行", "宮"];
    for (let k = 0; k < 27; k++)
      for (let d = 1; d <= 9; d++) {
        let at = -1,
          n = 0,
          have = false;
        for (const i of UNITS[k]) {
          if (st.g[i] === d) have = true;
          else if (!st.g[i] && cand(st, i) & (1 << d)) (at = i), n++;
        }
        if (!have && n === 1)
          return { i: at, d, why: "hidden", unit: names[(k / 9) | 0] };
      }
    let best = -1,
      bc = 10;
    if (prefer >= 0 && !st.g[prefer]) best = prefer;
    else
      for (let i = 0; i < 81; i++) {
        if (st.g[i]) continue;
        const c = popc(cand(st, i));
        if (c < bc) (bc = c), (best = i);
      }
    return best < 0 ? null : { i: best, d: solution[best], why: "reveal" };
  }

  // ------------------------------------------------------------ 數獨
  function genSudoku() {
    let best = null;
    for (let tries = 0; tries < 12; tries++) {
      const sol = fullGrid();
      const p = sol.slice();
      for (const i of shuffle([...Array(81).keys()])) {
        const v = p[i];
        p[i] = 0;
        if (solve(p, { limit: 2 }).length !== 1) p[i] = v;
      }
      const clues = p.filter(Boolean).length;
      const hard = !singlesSolve(p);
      if (!best || (hard && !best.hard) || (hard === best.hard && clues < best.clues))
        best = { puzzle: p, solution: sol, clues, hard };
      if (hard && clues <= 25) break;
    }
    return { puzzle: best.puzzle, solution: best.solution };
  }

  // ------------------------------------------------------------ 殺手數獨
  // 在 free 的格子上長出新籠子（2–5 格、籠內數字不重複），寫回 cageOf
  function growCages(sol, cageOf, free, next) {
    const sizes = [2, 2, 3, 3, 3, 3, 4, 4, 4, 5];
    const cages = new Map();
    for (const start of shuffle(free)) {
      if (cageOf[start] >= 0) continue;
      const k = next++,
        target = sizes[rand(sizes.length)];
      const cells = [start];
      let used = 1 << sol[start];
      cageOf[start] = k;
      while (cells.length < target) {
        const opts = [];
        for (const c of cells)
          for (const n of NB4(c))
            if (cageOf[n] < 0 && !(used & (1 << sol[n]))) opts.push(n);
        if (!opts.length) break;
        const n = opts[rand(opts.length)];
        cells.push(n);
        cageOf[n] = k;
        used |= 1 << sol[n];
      }
      cages.set(k, cells);
    }
    return next;
  }
  function cagesFrom(sol, cageOf) {
    const m = new Map();
    for (let i = 0; i < 81; i++) {
      if (!m.has(cageOf[i])) m.set(cageOf[i], []);
      m.get(cageOf[i]).push(i);
    }
    // 單格籠子盡量併進隔壁的籠子
    for (const [k, cells] of m) {
      if (cells.length !== 1) continue;
      const i = cells[0];
      const host = shuffle(NB4(i))
        .map((n) => cageOf[n])
        .find((h) => {
          const hc = m.get(h);
          return h !== k && hc.length && hc.length < 6 && !hc.some((c) => sol[c] === sol[i]);
        });
      if (host === undefined) continue;
      m.get(host).push(i);
      cageOf[i] = host;
      m.set(k, []);
    }
    return [...m.values()]
      .filter((c) => c.length)
      .map((cells) => ({
        cells: cells.sort((a, b) => a - b),
        sum: cells.reduce((s, i) => s + sol[i], 0),
      }));
  }
  function genKiller() {
    for (let tries = 0; tries < 40; tries++) {
      const sol = fullGrid();
      const cageOf = new Int16Array(81).fill(-1);
      let next = growCages(sol, cageOf, [...Array(81).keys()], 0);
      // 有兩組解 → 把兩解不同的格子所在的籠子拆掉重長，直到唯一解
      for (let fix = 0; fix < 30; fix++) {
        const cages = cagesFrom(sol, cageOf);
        let sols;
        try {
          sols = solve(Array(81).fill(0), { cages, limit: 2, maxNodes: 40000 });
        } catch {
          break; // 解太久 → 換一盤
        }
        if (sols.length === 1) return { cages, solution: sol };
        const diff = new Set();
        for (let i = 0; i < 81; i++) if (sols[0][i] !== sols[1][i]) diff.add(cageOf[i]);
        const free = [];
        for (let i = 0; i < 81; i++)
          if (diff.has(cageOf[i])) free.push(i), (cageOf[i] = -1);
        next = growCages(sol, cageOf, free, next);
      }
    }
    throw new Error("killer generation failed");
  }

  // ------------------------------------------------------------ 數織
  // line: -1 未知 / 0 空 / 1 塗黑；回傳推得的新 line，矛盾回傳 null
  function lineSolve(clue, line) {
    const n = line.length,
      k = clue.length;
    const canE = (i) => line[i] !== 1,
      canF = (i) => line[i] !== 0;
    const runF = new Int32Array(n + 1); // runF[i] = 從 i 往右連續可塗格數
    for (let i = n - 1; i >= 0; i--) runF[i] = canF(i) ? runF[i + 1] + 1 : 0;
    const fw = [...Array(n + 1)].map(() => new Uint8Array(k + 1));
    const bw = [...Array(n + 2)].map(() => new Uint8Array(k + 1));
    fw[0][0] = 1;
    for (let i = 1; i <= n; i++)
      for (let j = 0; j <= k; j++) {
        let v = canE(i - 1) && fw[i - 1][j];
        if (!v && j > 0) {
          const L = clue[j - 1],
            s = i - L;
          if (s >= 0 && runF[s] >= L)
            v = s === 0 ? j === 1 : canE(s - 1) && fw[s - 1][j - 1];
        }
        fw[i][j] = v ? 1 : 0;
      }
    if (!fw[n][k]) return null;
    bw[n][k] = 1;
    bw[n + 1][k] = 1;
    for (let i = n - 1; i >= 0; i--)
      for (let j = k; j >= 0; j--) {
        let v = canE(i) && bw[i + 1][j];
        if (!v && j < k) {
          const L = clue[j],
            e = i + L;
          if (e <= n && runF[i] >= L)
            v = e === n ? j + 1 === k : canE(e) && bw[e + 1][j + 1];
        }
        bw[i][j] = v ? 1 : 0;
      }
    const empt = new Uint8Array(n),
      fill = new Int32Array(n + 1);
    for (let i = 0; i < n; i++)
      if (canE(i)) for (let j = 0; j <= k; j++) if (fw[i][j] && bw[i + 1][j]) empt[i] = 1;
    for (let j = 0; j < k; j++) {
      const L = clue[j];
      for (let s = 0; s + L <= n; s++) {
        if (runF[s] < L) continue;
        const pre = s === 0 ? j === 0 : canE(s - 1) && fw[s - 1][j];
        const e = s + L;
        const suf = e === n ? j + 1 === k : canE(e) && bw[e + 1][j + 1];
        if (pre && suf) fill[s]++, fill[e]--;
      }
    }
    const out = line.slice();
    for (let i = 0, run = 0; i < n; i++) {
      run += fill[i];
      const f = run > 0,
        e = empt[i] === 1;
      if (!f && !e) return null;
      out[i] = f && e ? -1 : f ? 1 : 0;
    }
    return out;
  }
  const runsOf = (cells) => {
    const out = [];
    let r = 0;
    for (const v of cells) {
      if (v === 1) r++;
      else if (r) out.push(r), (r = 0);
    }
    if (r) out.push(r);
    return out;
  };
  const rowOf = (g, W, r) => g.slice(r * W, r * W + W);
  const colOf = (g, W, H, c) => [...Array(H)].map((_, r) => g[r * W + c]);
  // 逐行推理到不能再推；step=true 時只推一行就停（給提示用）
  function nonoPropagate(rows, cols, grid, step = false) {
    const H = rows.length,
      W = cols.length,
      g = grid.slice();
    nonoPropagate.rounds = 0;
    for (let changed = true; changed; nonoPropagate.rounds++) {
      changed = false;
      for (let r = 0; r < H; r++) {
        const cur = rowOf(g, W, r),
          nx = lineSolve(rows[r], cur);
        if (!nx) return null;
        const diff = nx.findIndex((v, c) => v !== cur[c]);
        if (diff < 0) continue;
        nx.forEach((v, c) => (g[r * W + c] = v));
        if (step) return { grid: g, line: { kind: "row", idx: r }, at: r * W + diff };
        changed = true;
      }
      for (let c = 0; c < W; c++) {
        const cur = colOf(g, W, H, c),
          nx = lineSolve(cols[c], cur);
        if (!nx) return null;
        const diff = nx.findIndex((v, r) => v !== cur[r]);
        if (diff < 0) continue;
        nx.forEach((v, r) => (g[r * W + c] = v));
        if (step) return { grid: g, line: { kind: "col", idx: c }, at: diff * W + c };
        changed = true;
      }
    }
    return step ? null : g;
  }
  // 填色比例壓低、多出幾盤挑「要推最多輪」的那盤，當作 expert
  function genNonogram(W = 15, H = 15) {
    let best = null;
    for (let tries = 0, found = 0; found < 8 && tries < 4000; tries++) {
      const p = 0.47 + Math.random() * 0.06;
      const sol = [...Array(W * H)].map(() => (Math.random() < p ? 1 : 0));
      const rows = [...Array(H)].map((_, r) => runsOf(rowOf(sol, W, r)));
      const cols = [...Array(W)].map((_, c) => runsOf(colOf(sol, W, H, c)));
      const g = nonoPropagate(rows, cols, Array(W * H).fill(-1));
      if (!g || g.some((v) => v < 0)) continue;
      found++;
      if (!best || nonoPropagate.rounds > best.rounds)
        best = { W, H, rows, cols, solution: sol, rounds: nonoPropagate.rounds };
    }
    if (!best) throw new Error("nonogram generation failed");
    delete best.rounds;
    return best;
  }

  const G = {
    sudoku: { generate: genSudoku, hint: (g, s, p) => sudokuHint(g, s, null, p) },
    killer: {
      generate: genKiller,
      hint: (g, s, cages, p) => sudokuHint(g, s, cages, p),
    },
    nonogram: { generate: genNonogram, propagate: nonoPropagate, runsOf, lineSolve },
    peers: PEERS,
    box: BOX,
  };
  // 一般 <script> 載入時掛在 window；當 Web Worker 跑時，收到遊戲名稱就出題回傳
  if (typeof window !== "undefined") window.SH_GAMES = G;
  else
    self.onmessage = (e) => {
      try {
        self.postMessage({ ok: true, game: G[e.data].generate() });
      } catch (err) {
        self.postMessage({ ok: false, error: String(err.message || err) });
      }
    };
})();
