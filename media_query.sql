SELECT
    p.post_id,
    u.username,
    p.title,
    p.posted_at
FROM posts AS p
JOIN users AS u
    ON p.user_id = u.user_id
WHERE p.posted_at >= '2026-08-01'
ORDER BY p.posted_at;
