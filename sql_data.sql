-- StarTrack SQL Query Examples
-- 본 파일은 StarTrack 프로젝트에서 사용되는 대표 SQL 질의문을 정리한 파일이다.
-- 실제 테이블 생성 SQL은 schema.sql에 작성되어 있다.

-- 1. 전체 기사 최신순 조회
SELECT article_id, title, source_name, published_at, summary, category, source_url
FROM articles
ORDER BY published_at DESC;


-- 2. 특정 카테고리 기사 조회
SELECT article_id, title, source_name, published_at, summary, category, source_url
FROM articles
WHERE category = '게임'
ORDER BY published_at DESC;


-- 3. 키워드 검색
-- 제목, 요약, 출처명에서 특정 키워드가 포함된 기사 검색
SELECT article_id, title, source_name, published_at, summary, category, source_url
FROM articles
WHERE title ILIKE '%Mandalorian%'
   OR summary ILIKE '%Mandalorian%'
   OR source_name ILIKE '%Mandalorian%'
ORDER BY published_at DESC;


-- 4. 카테고리 목록 조회
SELECT DISTINCT category
FROM articles
WHERE category IS NOT NULL
ORDER BY category;


-- 5. 전체 작품 목록 최신순 조회
SELECT work_id, title, type, release_date, status, description, source_url
FROM works
ORDER BY release_date DESC;


-- 6. 공개 예정 작품 조회
SELECT work_id, title, type, release_date, status, description, source_url
FROM works
WHERE status = 'Upcoming'
ORDER BY release_date ASC;


-- 7. 작품 유형별 개수 조회
SELECT type, COUNT(*) AS work_count
FROM works
GROUP BY type
ORDER BY work_count DESC;


-- 8. 기사 카테고리별 개수 조회
SELECT category, COUNT(*) AS article_count
FROM articles
GROUP BY category
ORDER BY article_count DESC;


-- 9. 특정 사용자의 북마크 기사 조회
SELECT b.bookmark_id, u.username, a.title, a.source_name, a.published_at, a.source_url
FROM bookmarks b
JOIN users u ON b.user_id = u.user_id
JOIN articles a ON b.article_id = a.article_id
WHERE u.username = 'test_user'
ORDER BY b.created_at DESC;


-- 10. 특정 사용자의 메모 조회
SELECT n.note_id, u.username, a.title, n.note_text, n.created_at
FROM notes n
JOIN users u ON n.user_id = u.user_id
JOIN articles a ON n.article_id = a.article_id
WHERE u.username = 'test_user'
ORDER BY n.created_at DESC;


-- 11. 특정 작품과 관련된 기사 조회
SELECT w.title AS work_title,
       a.title AS article_title,
       a.source_name,
       a.published_at,
       a.source_url
FROM work_articles wa
JOIN works w ON wa.work_id = w.work_id
JOIN articles a ON wa.article_id = a.article_id
ORDER BY w.title, a.published_at DESC;


-- 12. 태그별 기사 조회
SELECT t.tag_name,
       a.title,
       a.source_name,
       a.published_at,
       a.source_url
FROM article_tags at
JOIN tags t ON at.tag_id = t.tag_id
JOIN articles a ON at.article_id = a.article_id
ORDER BY t.tag_name, a.published_at DESC;