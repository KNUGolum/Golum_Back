-- Golum local development seed data.
-- This file wipes all current app data and inserts deterministic test data.
--
-- Apply from Golum_Back:
--   docker compose exec -T db psql -U golum_user -d golum_db < seed.sql

CREATE EXTENSION IF NOT EXISTS pgcrypto;
SET TIME ZONE 'Asia/Seoul';

BEGIN;

TRUNCATE TABLE
  settlements,
  bets,
  votes,
  poll_stats,
  poll_options,
  polls,
  auth_tokens,
  users,
  titles
RESTART IDENTITY CASCADE;

-- Test accounts
-- demo@example.com / Demo1234!
-- alice@example.com / Alice1234!
-- bob@example.com / Bob1234!
-- chris@example.com / Chris1234!
-- dana@example.com / Dana1234!
INSERT INTO users (id, email, password_hash, nickname, credit, created_at)
VALUES
  (1001, 'demo@example.com', crypt('Demo1234!', gen_salt('bf')), '데모유저', 2350, now() - interval '8 days'),
  (1002, 'alice@example.com', crypt('Alice1234!', gen_salt('bf')), '앨리스', 1800, now() - interval '7 days'),
  (1003, 'bob@example.com', crypt('Bob1234!', gen_salt('bf')), '밥', 1200, now() - interval '6 days'),
  (1004, 'chris@example.com', crypt('Chris1234!', gen_salt('bf')), '크리스', 3200, now() - interval '5 days'),
  (1005, 'dana@example.com', crypt('Dana1234!', gen_salt('bf')), '다나', 950, now() - interval '4 days');

-- Polls. 7 ongoing, 3 ended.
INSERT INTO polls (id, title, creator_id, status, end_time, created_at)
VALUES
  (2001, '점심 메뉴 뭐 먹을까?', 1002, 'ONGOING', now() + interval '21 hours', now() - interval '3 hours'),
  (2002, '이번 발표 결과는?', 1003, 'ENDED', now() - interval '2 hours', now() - interval '1 day'),
  (2003, '아이폰 vs 갤럭시, 당신의 선택은?', 1001, 'ONGOING', now() + interval '4 minutes', now() - interval '2 hours'),
  (2004, '여름 vs 겨울, 최애 계절은?', 1002, 'ONGOING', now() + interval '18 hours', now() - interval '8 hours'),
  (2005, '퇴근 후 운동 vs 휴식?', 1004, 'ONGOING', now() + interval '10 hours', now() - interval '4 hours'),
  (2006, '민트초코는 호인가 불호인가?', 1005, 'ONGOING', now() + interval '2 hours', now() - interval '11 hours'),
  (2007, '주말 여행은 바다 vs 산?', 1003, 'ENDED', now() - interval '5 hours', now() - interval '2 days'),
  (2008, '팀 프로젝트 방식은 온라인 vs 오프라인?', 1004, 'ONGOING', now() + interval '23 hours', now() - interval '50 minutes'),
  (2009, '아침형 인간 vs 저녁형 인간?', 1005, 'ENDED', now() - interval '1 day', now() - interval '3 days'),
  (2010, '디자인 먼저 vs 기능 먼저?', 1002, 'ONGOING', now() + interval '14 hours', now() - interval '6 hours');

-- Options. Odd IDs are A, even IDs are B.
INSERT INTO poll_options (id, poll_id, option_text, vote_count)
VALUES
  (3001, 2001, '김치찌개', 42),
  (3002, 2001, '제육볶음', 58),
  (3003, 2002, '성공', 81),
  (3004, 2002, '아쉬움', 27),
  (3005, 2003, '아이폰', 5),
  (3006, 2003, '갤럭시', 1),
  (3007, 2004, '여름', 33),
  (3008, 2004, '겨울', 41),
  (3009, 2005, '운동', 29),
  (3010, 2005, '휴식', 76),
  (3011, 2006, '호', 37),
  (3012, 2006, '불호', 64),
  (3013, 2007, '바다', 92),
  (3014, 2007, '산', 88),
  (3015, 2008, '온라인', 55),
  (3016, 2008, '오프라인', 21),
  (3017, 2009, '아침형', 44),
  (3018, 2009, '저녁형', 99),
  (3019, 2010, '디자인 먼저', 70),
  (3020, 2010, '기능 먼저', 83);

INSERT INTO poll_stats (poll_id, total_votes, option1_ratio, option2_ratio, updated_at)
VALUES
  (2001, 100, 42.00, 58.00, now()),
  (2002, 108, 75.00, 25.00, now()),
  (2003, 6, 83.33, 16.67, now()),
  (2004, 74, 44.59, 55.41, now()),
  (2005, 105, 27.62, 72.38, now()),
  (2006, 101, 36.63, 63.37, now()),
  (2007, 180, 51.11, 48.89, now()),
  (2008, 76, 72.37, 27.63, now()),
  (2009, 143, 30.77, 69.23, now()),
  (2010, 153, 45.75, 54.25, now());

-- User participation for UI states.
-- demo@example.com has: mine list data, can-bet case, already-bet case, skip case, ended result case.
INSERT INTO votes (id, user_id, poll_id, option_id, created_at)
VALUES
  (4001, 1001, 2001, 3001, now() - interval '2 hours'),
  (4002, 1001, 2002, 3003, now() - interval '20 hours'),
  (4003, 1001, 2004, 3008, now() - interval '5 hours'),
  (4004, 1001, 2005, 3010, now() - interval '2 hours'),
  (4005, 1001, 2006, 3012, now() - interval '1 hour'),
  (4006, 1003, 2001, 3002, now() - interval '90 minutes'),
  (4007, 1002, 2007, 3013, now() - interval '1 day'),
  (4008, 1004, 2002, 3003, now() - interval '21 hours'),
  (4009, 1003, 2004, 3008, now() - interval '4 hours'),
  (4010, 1003, 2010, 3020, now() - interval '3 hours'),
  (4011, 1002, 2008, 3015, now() - interval '30 minutes'),
  (4012, 1004, 2009, 3018, now() - interval '2 days');

-- Bets. amount 0 represents "skip betting".
INSERT INTO bets (id, user_id, poll_id, option_id, amount, result, reward_amount, created_at)
VALUES
  (5001, 1001, 2002, 3003, 300, 'WIN', 450, now() - interval '19 hours'),
  (5002, 1001, 2004, 3008, 0, 'PENDING', 0, now() - interval '4 hours'),
  (5003, 1001, 2005, 3010, 250, 'PENDING', 0, now() - interval '90 minutes'),
  (5004, 1003, 2001, 3002, 150, 'PENDING', 0, now() - interval '1 hour'),
  (5005, 1002, 2007, 3013, 200, 'WIN', 320, now() - interval '1 day'),
  (5006, 1004, 2002, 3003, 100, 'WIN', 150, now() - interval '20 hours'),
  (5007, 1003, 2010, 3020, 0, 'PENDING', 0, now() - interval '2 hours'),
  (5008, 1002, 2008, 3015, 500, 'PENDING', 0, now() - interval '20 minutes');

INSERT INTO settlements (id, poll_id, status, created_at, completed_at)
VALUES
  (6001, 2002, 'COMPLETED', now() - interval '90 minutes', now() - interval '80 minutes'),
  (6002, 2007, 'COMPLETED', now() - interval '4 hours', now() - interval '3 hours'),
  (6003, 2009, 'PENDING', now() - interval '20 hours', null);

-- Title shop items.
INSERT INTO titles (id, name, grade, price)
VALUES
  (1, '초보', 'COMMON', 300),
  (2, '승부사', 'RARE', 800),
  (3, '타짜', 'EPIC', 1500),
  (4, '골룸', 'LEGENDARY', 3000);

-- Keep auto-increment sequences ahead of fixed seed IDs.
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE((SELECT MAX(id) FROM users), 1), true);
SELECT setval(pg_get_serial_sequence('polls', 'id'), COALESCE((SELECT MAX(id) FROM polls), 1), true);
SELECT setval(pg_get_serial_sequence('poll_options', 'id'), COALESCE((SELECT MAX(id) FROM poll_options), 1), true);
SELECT setval(pg_get_serial_sequence('votes', 'id'), COALESCE((SELECT MAX(id) FROM votes), 1), true);
SELECT setval(pg_get_serial_sequence('bets', 'id'), COALESCE((SELECT MAX(id) FROM bets), 1), true);
SELECT setval(pg_get_serial_sequence('settlements', 'id'), COALESCE((SELECT MAX(id) FROM settlements), 1), true);
SELECT setval(pg_get_serial_sequence('titles', 'id'), COALESCE((SELECT MAX(id) FROM titles), 1), true);

COMMIT;
