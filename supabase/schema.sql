-- Study Hub — 登入與學習軌跡用的資料表
-- 用法：Supabase 後台 → SQL Editor → New query → 整份貼上 → Run。
-- 重複執行是安全的（已存在的東西會略過或覆蓋成同樣內容）。

-- ------------------------------------------------------------ 1. 逐筆作答紀錄
-- 每答一題寫一筆。記憶曲線、學習曲線都從這張表算。
create table if not exists public.attempts (
  id          uuid primary key,                       -- 由網頁端產生，重送不會重複
  user_id     uuid not null default auth.uid()
              references auth.users (id) on delete cascade,
  subject     text not null,                          -- 科目 id，例如 biochem
  qid         text not null,                          -- 題目 id
  ok          boolean not null,                       -- 答對 / 答錯
  mode        text,                                   -- mcq（選擇）| self（自評）| card（字卡）| mock（模擬考）
  ms          integer,                                -- 從看到題目到作答的毫秒數
  answered_at timestamptz not null,                   -- 作答時間（裝置時間）
  created_at  timestamptz not null default now()      -- 上傳時間
);

create index if not exists attempts_user_time
  on public.attempts (user_id, answered_at);
create index if not exists attempts_user_question
  on public.attempts (user_id, subject, qid, answered_at);
create index if not exists attempts_user_created           -- 其他裝置下載新紀錄用
  on public.attempts (user_id, created_at);

alter table public.attempts enable row level security;

drop policy if exists "attempts: read own"   on public.attempts;
drop policy if exists "attempts: insert own" on public.attempts;
drop policy if exists "attempts: delete own" on public.attempts;
create policy "attempts: read own"   on public.attempts
  for select using (auth.uid() = user_id);
create policy "attempts: insert own" on public.attempts
  for insert with check (auth.uid() = user_id);
create policy "attempts: delete own" on public.attempts
  for delete using (auth.uid() = user_id);

-- ------------------------------------------------------------ 2. 目前狀態（每人一列）
-- 各題最新對錯、收藏、已讀章節。跨裝置同步用。
create table if not exists public.user_state (
  user_id    uuid primary key default auth.uid()
             references auth.users (id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.user_state enable row level security;

drop policy if exists "user_state: read own"   on public.user_state;
drop policy if exists "user_state: insert own" on public.user_state;
drop policy if exists "user_state: update own" on public.user_state;
create policy "user_state: read own"   on public.user_state
  for select using (auth.uid() = user_id);
create policy "user_state: insert own" on public.user_state
  for insert with check (auth.uid() = user_id);
create policy "user_state: update own" on public.user_state
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ------------------------------------------------------------ 3. 分析用 view
-- 每筆作答加上「這是第幾次做這題」「距離上次做這題幾天」。
-- security_invoker：查詢時套用查詢者自己的權限，只看得到自己的資料。
create or replace view public.attempt_intervals
with (security_invoker = true) as
select
  a.*,
  row_number() over w as nth,
  extract(epoch from a.answered_at - lag(a.answered_at) over w) / 86400.0 as gap_days,
  lag(a.ok) over w as prev_ok
from public.attempts a
window w as (partition by a.user_id, a.subject, a.qid order by a.answered_at);

-- ------------------------------------------------------------ 4. 自訂頭像（Storage）
-- 公開 bucket：頭像網址任何人都能看；只有本人能上傳、覆蓋、刪除自己資料夾 avatars/<user id>/ 裡的檔案。
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('avatars', 'avatars', true, 2097152, array['image/jpeg', 'image/png', 'image/webp'])
on conflict (id) do update
  set public = excluded.public,
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "avatars: insert own" on storage.objects;
drop policy if exists "avatars: update own" on storage.objects;
drop policy if exists "avatars: delete own" on storage.objects;
drop policy if exists "avatars: read own"   on storage.objects;
create policy "avatars: insert own" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "avatars: update own" on storage.objects
  for update to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "avatars: delete own" on storage.objects
  for delete to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
-- upsert 覆蓋舊檔時要先讀得到自己的檔案
create policy "avatars: read own" on storage.objects
  for select to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);

-- ------------------------------------------------------------ 範例查詢（不用執行，要分析時複製到 SQL Editor）
-- 遺忘曲線：距上次幾天 → 答對率
-- select
--   case
--     when gap_days < 1  then '0 <1 天'
--     when gap_days < 3  then '1 1–3 天'
--     when gap_days < 7  then '2 3–7 天'
--     when gap_days < 14 then '3 7–14 天'
--     when gap_days < 30 then '4 14–30 天'
--     else                    '5 30 天以上'
--   end as gap,
--   count(*) as n,
--   round(avg(ok::int) * 100, 1) as accuracy
-- from attempt_intervals
-- where nth > 1
-- group by 1 order by 1;
--
-- 每日練習量與答對率
-- select date(answered_at at time zone 'Asia/Taipei') as day,
--        count(*) as n, round(avg(ok::int) * 100, 1) as accuracy
-- from attempts group by 1 order by 1;
