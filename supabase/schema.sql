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

-- ------------------------------------------------------------ 5. 更新通知已讀
-- 登入的人在更新視窗按「知道了」時寫一筆（news_id = news.json 的 id）。
-- 只有本人能寫、能讀自己的；站長在 SQL Editor 查詢時不受限制（看下方範例查詢）。
create table if not exists public.news_seen (
  user_id  uuid not null default auth.uid()
           references auth.users (id) on delete cascade,
  news_id  text not null,
  seen_at  timestamptz not null default now(),
  primary key (user_id, news_id)
);

alter table public.news_seen enable row level security;

drop policy if exists "news_seen: read own"   on public.news_seen;
drop policy if exists "news_seen: insert own" on public.news_seen;
create policy "news_seen: read own"   on public.news_seen
  for select using (auth.uid() = user_id);
create policy "news_seen: insert own" on public.news_seen
  for insert with check (auth.uid() = user_id);

-- ------------------------------------------------------------ 6. 即時留言板（#/board）
-- 任何人（含未登入）都能看、都能留言。
-- 登入：名字與頭像由 trigger 從帳號資料帶入，無法冒名；同一人 10 秒內只能留一則；可刪自己的。
-- 未登入（訪客）：自填暱稱、標記 guest；瀏覽器產生一把隨機鑰匙，資料庫只存它的 sha256（owner_key），
--   之後用 board_delete_guest(id, 鑰匙) 刪自己的。防洗版：同一把鑰匙 10 秒一則、全站訪客每分鐘最多 10 則。
-- 站長在 Table Editor 可刪任何一則。
create table if not exists public.board_messages (
  id         bigint generated always as identity primary key,
  user_id    uuid default auth.uid() references auth.users (id) on delete cascade,
  name       text not null default '',
  avatar     text not null default '',
  body       text not null check (char_length(btrim(body)) between 1 and 500),
  created_at timestamptz not null default now()
);
alter table public.board_messages alter column user_id drop not null;
alter table public.board_messages add column if not exists guest     boolean not null default false;
alter table public.board_messages add column if not exists owner_key text;
-- 樓層：新增時依序配號，之後固定；刪掉的樓層留空號，不會往前補
alter table public.board_messages add column if not exists floor integer;
update public.board_messages b set floor = r.n
from (select id, row_number() over (order by id) as n from public.board_messages) r
where b.id = r.id and b.floor is null
  and not exists (select 1 from public.board_messages where floor is not null);
create unique index if not exists board_messages_floor on public.board_messages (floor);

create index if not exists board_messages_time on public.board_messages (created_at desc);

create or replace function public.board_messages_fill()
returns trigger language plpgsql security definer set search_path = public as $$
declare m jsonb;
begin
  new.created_at := now();
  new.body       := btrim(new.body);
  new.user_id    := auth.uid();
  if new.user_id is not null then
    if exists (select 1 from public.board_messages
               where user_id = new.user_id and created_at > now() - interval '10 seconds') then
      raise exception '留言太快了，等幾秒再送';
    end if;
    select raw_user_meta_data into m from auth.users where id = new.user_id;
    new.guest     := false;
    new.owner_key := null;
    new.name      := left(coalesce(nullif(m->>'display_name', ''), nullif(m->>'full_name', ''),
                                   nullif(m->>'name', ''), '同學'), 40);
    new.avatar    := coalesce(nullif(m->>'custom_avatar', ''), m->>'avatar_url', '');
  else
    -- 網頁端把原始鑰匙放在 owner_key 送來，這裡換成雜湊才存
    if coalesce(char_length(new.owner_key), 0) < 16 then
      raise exception '缺少訪客鑰匙';
    end if;
    new.owner_key := encode(sha256(convert_to(new.owner_key, 'UTF8')), 'hex');
    if exists (select 1 from public.board_messages
               where owner_key = new.owner_key and created_at > now() - interval '10 seconds') then
      raise exception '留言太快了，等幾秒再送';
    end if;
    if (select count(*) from public.board_messages
        where guest and created_at > now() - interval '1 minute') >= 10 then
      raise exception '訪客留言太多了，請稍候或登入後再留言';
    end if;
    new.guest  := true;
    new.avatar := '';
    new.name   := left(coalesce(nullif(btrim(new.name), ''), '匿名同學'), 20);
  end if;
  -- 配樓層：鎖住到交易結束，同時送出的兩則不會拿到同一層；被擋下的留言不會用掉號碼
  perform pg_advisory_xact_lock(hashtext('board_messages_floor'));
  new.floor := coalesce((select max(floor) from public.board_messages), 0) + 1;
  return new;
end $$;

drop trigger if exists board_messages_fill on public.board_messages;
create trigger board_messages_fill before insert on public.board_messages
  for each row execute function public.board_messages_fill();

-- 訪客刪除自己的留言
create or replace function public.board_delete_guest(p_id bigint, p_key text)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  delete from public.board_messages
  where id = p_id and guest
    and owner_key = encode(sha256(convert_to(p_key, 'UTF8')), 'hex');
  return found;
end $$;
grant execute on function public.board_delete_guest(bigint, text) to anon, authenticated;

alter table public.board_messages enable row level security;

drop policy if exists "board: read all"     on public.board_messages;
drop policy if exists "board: insert own"   on public.board_messages;
drop policy if exists "board: insert guest" on public.board_messages;
drop policy if exists "board: delete own"   on public.board_messages;
create policy "board: read all"     on public.board_messages
  for select using (true);
create policy "board: insert own"   on public.board_messages
  for insert to authenticated with check (auth.uid() = user_id);
create policy "board: insert guest" on public.board_messages
  for insert to anon with check (user_id is null and guest);
create policy "board: delete own"   on public.board_messages
  for delete to authenticated using (auth.uid() = user_id);

-- 開啟 Realtime（新增、刪除會即時推送給正在看的人）；刪除事件要帶整列才知道刪了哪則
alter table public.board_messages replica identity full;
do $$ begin
  alter publication supabase_realtime add table public.board_messages;
exception when duplicate_object then null;
end $$;

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
--
-- 某則更新誰還沒看（把 id 換成 news.json 最新一則；只看得到有登入過的人）
-- select u.email, u.last_sign_in_at
-- from auth.users u
-- where not exists (
--   select 1 from news_seen s where s.user_id = u.id and s.news_id = '20261103-2')
-- order by u.last_sign_in_at desc;
--
-- 每則更新的已讀人數
-- select news_id, count(*) as seen, max(seen_at) as last_seen
-- from news_seen group by 1 order by 1 desc;
