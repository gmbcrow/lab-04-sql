DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id     INT PRIMARY KEY,
    username    VARCHAR(50) NOT NULL,
    email       VARCHAR(100) NOT NULL,
    created_at  DATETIME NOT NULL
);

CREATE TABLE posts (
    post_id     INT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(100) NOT NULL,
    body        TEXT,
    created_at  DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, username, email, created_at) VALUES
    (1,  'avang',    'avang@example.com',    '2026-01-05 09:00:00'),
    (2,  'bholt',    'bholt@example.com',    '2026-01-06 10:15:00'),
    (3,  'cruiz',    'cruiz@example.com',    '2026-01-07 11:30:00'),
    (4,  'dpatel',   'dpatel@example.com',   '2026-01-08 12:45:00'),
    (5,  'ejones',   'ejones@example.com',   '2026-01-09 14:00:00'),
    (6,  'fkim',     'fkim@example.com',     '2026-01-10 15:15:00'),
    (7,  'glane',    'glane@example.com',    '2026-01-11 16:30:00'),
    (8,  'hmiller',  'hmiller@example.com',  '2026-01-12 17:45:00'),
    (9,  'inovak',   'inovak@example.com',   '2026-01-13 19:00:00'),
    (10, 'jortiz',   'jortiz@example.com',   '2026-01-14 20:15:00');

INSERT INTO posts (post_id, user_id, title, body, created_at) VALUES
    (101, 1,  'Getting started with SQL', 'My first post about databases.',         '2026-01-15 08:00:00'),
    (102, 2,  'Why foreign keys matter',  'Explaining referential integrity.',      '2026-01-16 09:10:00'),
    (103, 3,  'A weekend trip',           'Notes from a short hiking trip.',        '2026-01-17 10:20:00'),
    (104, 1,  'Follow-up thoughts',       'More on database design.',               '2026-01-18 11:30:00'),
    (105, 4,  'Cooking experiment',       'Tried a new recipe today.',              '2026-01-19 12:40:00'),
    (106, 5,  'Python tips',              'Some pandas tricks I learned.',          '2026-01-20 13:50:00'),
    (107, 6,  'Book review',              'Thoughts on a recent read.',             '2026-01-21 15:00:00'),
    (108, 7,  'Weekly update',            'Progress on my side project.',           '2026-01-22 16:10:00'),
    (109, 8,  'Debugging story',          'How I tracked down a tricky bug.',       '2026-01-23 17:20:00'),
    (110, 9,  'Class reflections',        'Thoughts halfway through the semester.', '2026-01-24 18:30:00');
