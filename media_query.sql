SELECT
    users.username,
    posts.title,
    posts.created_at
FROM posts
JOIN users ON posts.user_id = users.user_id
WHERE posts.created_at >= '2026-01-18 00:00:00'
ORDER BY posts.created_at;
