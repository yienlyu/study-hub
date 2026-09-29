# 📚 Study Hub 複習站

純靜態、多科目的複習網站（不需要 build），直接放在 GitHub Pages 就能用。

- **重點整理**：整合上課 slides 與共筆
- **上課 slides 重點**：逐份 slides 的頁面重點
- **考點分析**：自動統計考古考點、題型 + 人工整理的高頻考點與陷阱
- **互動式練習**：考古題、老師課堂題、依考古模式編寫的模擬新題；即時對答、詳解、錯題本、收藏、隨機 / 依序、關鍵字搜尋
- **問題回報**：一鍵開 GitHub Issue（題目頁會自動帶入題號與題目）

練習紀錄存在各自瀏覽器的 localStorage，不會上傳。

---

## 🚀 部署到 GitHub Pages

```bash
cd study-hub
git init
git add .
git commit -m "Initial study hub"
git branch -M main
git remote add origin https://github.com/yienlyu/study-hub.git
git push -u origin main
```

接著到 GitHub repo → **Settings → Pages** → Source 選 **Deploy from a branch**，Branch 選 **main**、資料夾 **/(root)** → Save。
約 1 分鐘後網站會在 `https://yienlyu.github.io/study-hub/`。

> 問題回報使用 GitHub Issues：請確認 repo 的 **Settings → General → Features → Issues** 是勾選的。
> 想要回報自動加上標籤，可在 Issues → Labels 建一個名為 `report` 的 label（沒建也可以正常回報）。

本機預覽（不能直接雙擊 index.html，因為要用 fetch 讀 JSON）：

```bash
python3 -m http.server 8000
# 打開 http://localhost:8000
```

---

## ➕ 新增一個科目

1. 複製 `subjects/_template/` 成 `subjects/<科目id>/`（例：`subjects/pharmacology/`）
2. 編輯 `subjects/<科目id>/subject.json`：科目名稱、章節列表、分組
3. 每一章寫一個 `content/<章節id>.md`，用三個分隔線分成三個分頁：

   ```markdown
   === summary ===
   # 重點整理（Markdown，可用表格）

   === slides ===
   # 上課 slides 重點

   === exam ===
   # 考點分析（網站會自動在上方加上考古統計圖）
   ```

4. 題目放在 `data/*.json`，並列在 `subject.json` 的 `questionFiles`
5. 在 `subjects/index.json` 加一行：

   ```json
   { "id": "pharmacology", "path": "subjects/pharmacology" }
   ```

### 題目格式

```json
{
  "id": "k113-innate-01",          // 唯一 id（錯題紀錄靠它）
  "source": "113 考古",              // 來源：顯示用，也用於篩選（含「考古」二字會算進考題分析）
  "chapter": "innate",               // 對應 subject.json 的章節 id
  "type": "mcq",                     // mcq（選擇）或 short（簡答，自我評分）
  "num": 1,                          // 原題號（選填）
  "stem": "題幹",
  "options": [{ "k": "A", "t": "選項文字" }, { "k": "B", "t": "..." }],
  "answer": ["B"],                   // 可多個（任一皆算對）；空陣列 = 無正確選項
  "answerText": "簡答題的參考答案",   // 選填
  "explain": "詳解",
  "note": "補充 / 爭議說明",          // 選填
  "topics": ["補體系統"],             // 考點標籤（用於統計）
  "pattern": "選錯誤（否定）題",      // 題型（用於統計）
  "imageOnly": false                 // true = 需要看圖，不放進練習
}
```

練習區的「題目來源」篩選目前內建四種：`113 考古`、`111 期中考古`、`2026 課堂題`、`模擬新題`。新科目若用不同來源名稱，改 `assets/app.js` 裡的 `SRC_GROUPS` 與 `SOURCE_COLORS` 即可。

---

## 🛠 tools/（微免資料的產生腳本）

| 檔案 | 作用 |
|---|---|
| `kaogu113.txt` | 113 考古原始文字 |
| `parse_kaogu.py` | 解析題目、答案表、詳解 → `kaogu-raw.json` |
| `fix_kaogu.py` | 人工修正、章節歸類、考點與題型標籤 → `subjects/micro-immuno/data/questions-kaogu.json` |
| `build_extra_questions.py` | 課堂題與模擬新題 → `questions-class.json`、`questions-new.json` |

```bash
cd tools && python3 parse_kaogu.py && python3 fix_kaogu.py && python3 build_extra_questions.py
```

## ⚙️ 設定

`config.js` 裡的 `githubRepo` 決定問題回報送到哪個 repo。
