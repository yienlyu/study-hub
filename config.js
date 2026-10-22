// 網站設定：換 repo 或 fork 給同學用時只要改這裡
window.STUDY_HUB_CONFIG = {
  siteTitle: "Study Hub",
  // 頁尾的 GitHub 連結
  githubRepo: "yienlyu/study-hub",
  // 「回報 / 回饋」的 Email 收件信箱；留空字串就不顯示 Email 按鈕
  contactEmail: "yienlyu@gmail.com",
  // 「用 LINE 傳送」按鈕開啟的 LINE 連結；留空字串時只複製內容，不開啟 LINE
  lineUrl: "https://line.me/ti/p/AcQw5PcjOB",

  // 登入與學習軌跡（Supabase）。兩個都留空字串就不顯示登入，紀錄只存在這台裝置。
  // 在 Supabase 後台 Project Settings → API 找：Project URL 與 anon public key（新版後台叫 publishable key）。
  // anon key 本來就是公開用的，資料靠 supabase/schema.sql 的權限規則保護，可以放心 commit。
  supabaseUrl: "https://rjjatolwgptadejokoxm.supabase.co",
  supabaseAnonKey: "sb_publishable_nkvjHvXOuzZQlj3p1YRwfw_DB-wKdu7",
  // 登入頁要顯示的方式：google、github（需在 Supabase 開啟對應 provider）、email（寄登入連結）
  authProviders: ["google", "email"],
  // Google Cloud 的 OAuth Client ID（跟 Supabase Google provider 填的同一個）。
  // 填了就改用 Google 自己的登入按鈕，登入畫面顯示本站網域而不是 xxxx.supabase.co；留空則走 Supabase 轉址登入。
  googleClientId:
    "563317688270-v72lvdfqi26u1jerbrm7etvfbrd6h96k.apps.googleusercontent.com",
};
