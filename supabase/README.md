# 登入與學習軌跡設定（Supabase）

沒設定也能用：網站會照常運作，紀錄只存在瀏覽器裡。設定好之後，學習軌跡頁（`#/me`）會出現登入按鈕，作答紀錄會同步到你的帳號。

全部用免費方案就夠了，大約 10 分鐘。

## 1. 建立專案

1. 到 <https://supabase.com> 用 GitHub 帳號登入 → **New project**。
2. 名稱隨意（例如 `study-hub`），Region 選 **Northeast Asia (Tokyo)** 或 **Southeast Asia (Singapore)**，資料庫密碼記下來。

## 2. 建資料表

左側 **SQL Editor** → **New query** → 把 [`schema.sql`](schema.sql) 整份貼上 → **Run**。

會建立：
- `attempts`：每次作答一筆（題目、對錯、時間、花了幾秒）。
- `user_state`：每人一列，存各題最新狀態、收藏、已讀，用於跨裝置同步。
- `attempt_intervals`（view）：每筆作答加上「第幾次做這題」「距離上次幾天」，分析記憶曲線用。

權限規則（RLS）已經寫好：每個人只能讀寫自己的資料。

## 3. 設定網址

**Authentication → URL Configuration**：
- **Site URL**：`https://yienlyu.github.io/study-hub/`
- **Redirect URLs** 加上：
  - `https://yienlyu.github.io/study-hub/`
  - `http://localhost:8000/`（本機測試用，可省略）

## 4. 開啟登入方式

**Authentication → Sign In / Providers**：

- **Email**：預設已開啟。登入頁用 Email + 密碼註冊、登入；忘記密碼可改寄登入連結，登入後在「設定密碼」改密碼。
  預設註冊時會寄確認信；若想註冊完直接登入，把 Email provider 的 **Confirm email** 關掉。
  免費方案每小時能寄的信有限（幾封），自己用沒問題；很多人一起用時建議改用 Google。
- **Google**（建議）：
  1. 到 <https://console.cloud.google.com> → 建立專案 → **APIs & Services → OAuth consent screen**，User type 選 External，填 App 名稱與 Email。
  2. **Credentials → Create credentials → OAuth client ID**，類型選 **Web application**。
  3. **Authorized redirect URIs** 填 Supabase Google provider 頁面上顯示的 Callback URL（長得像 `https://xxxx.supabase.co/auth/v1/callback`）。
  4. 把 Client ID、Client Secret 貼回 Supabase 的 Google provider，按 Save。
  5. （建議）讓登入畫面顯示本站網域而不是 `xxxx.supabase.co`：
     - 同一個 OAuth client 的 **Authorized JavaScript origins** 加上 `https://yienlyu.github.io`（本機測試再加 `http://localhost:8000`，origin 不含路徑）。
     - 把 Client ID 填進 `config.js` 的 `googleClientId`。網站就會改用 Google 自己的登入按鈕。
- **GitHub**（可選）：GitHub → Settings → Developer settings → OAuth Apps → New，Callback URL 一樣填 Supabase 給的那個。

`config.js` 的 `authProviders` 決定登入頁顯示哪些按鈕，例如 `["google", "email"]` 或 `["github"]`。

## 5. 填進 config.js

**Project Settings → API**（新版後台叫 **API Keys**）複製：
- Project URL → `supabaseUrl`
- `anon` `public` key（新版叫 publishable key）→ `supabaseAnonKey`

```js
supabaseUrl: "https://xxxx.supabase.co",
supabaseAnonKey: "eyJhbGciOi...",
```

這把 key 本來就設計成公開放在網頁裡，可以 commit。**不要**放 `service_role` / secret key。

## 同步怎麼運作

- 每答一題，先存在瀏覽器，2–3 秒後上傳。離線時會排隊，下次連線再補傳。
- 沒登入時做的題目，登入後會一起上傳到你的帳號。
- 開啟網站、切回分頁時會自動同步；學習軌跡頁也可以按「立即同步」。
- 「清除作答紀錄」只會重設練習進度（錯題本、答對率），逐筆的學習軌跡會保留。

## 自己做分析

SQL Editor 可以直接查，`schema.sql` 最下面有遺忘曲線、每日練習量的範例查詢。
也可以在 **Table Editor → attempts → Export → CSV** 匯出，或在學習軌跡頁按「下載作答紀錄（CSV）」。
