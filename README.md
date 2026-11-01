# Study Hub

## 重建題庫與圖表

`subjects/*/data/*.json`、`subjects/*/figures.json` 和部分 SVG 是 `tools/` 裡的 builder 產生的。這些檔案可以直接手改，但**重建時一律用 `tools/rebuild.py`**，不要直接跑 `build_*.py`：

```sh
python3 tools/rebuild.py tools/biochem/build_questions.py
python3 tools/rebuild.py --accept-builder tools/build_para_kaogu.py   # 這次以 builder 結果為準
```

`rebuild.py` 會在重建前拍快照，重建後依序套用 `tools/question_fixes.json`、`tools/explain_overrides.json`、`tools/manual_edits.json`。仍被蓋掉的手改會自動記進 `manual_edits.json` 並套回（手改的 SVG 另存到 `tools/manual_files/`），最後列出記了哪些。只有排版不同、內容相同的檔案會還原成原本的樣子。
