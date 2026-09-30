DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id     INT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL,
    created_at  DATETIME     NOT NULL
);


CREATE TABLE posts (
    post_id     INT PRIMARY KEY,
    user_id     INT          NOT NULL,
    title       VARCHAR(200) NOT NULL,
    body        TEXT,
    posted_at   DATETIME     NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users VALUES (1, 'hoohacker', 'hoohacker@example.com', '2026-01-05 09:15:00');
INSERT INTO users VALUES (2,  'rotundafan',  'rotundafan@example.com',  '2026-01-12 14:30:00');
INSERT INTO users VALUES (3,  'lawnlife',    'lawnlife@example.com',    '2026-02-01 08:00:00');
INSERT INTO users VALUES (4,  'corner_cafe', 'corner_cafe@example.com', '2026-02-14 19:45:00');
INSERT INTO users VALUES (5,  'datadude',    'datadude@example.com',    '2026-03-03 11:20:00');
INSERT INTO users VALUES (6,  'sqlqueen',    'sqlqueen@example.com',    '2026-03-18 16:05:00');
INSERT INTO users VALUES (7,  'wahoowa',     'wahoowa@example.com',     '2026-04-02 10:10:00');
INSERT INTO users VALUES (8,  'blueridge',   'blueridge@example.com',   '2026-04-22 13:40:00');
INSERT INTO users VALUES (9,  'mainstreet',  'mainstreet@example.com',  '2026-05-09 17:25:00');
INSERT INTO users VALUES (10, 'jeffersonj',  'jeffersonj@example.com',  '2026-06-01 07:55:00');


INSERT INTO posts VALUES (1, 1, 'First post', 'Hello from the Lawn!', '2026-06-02 09:00:00');
INSERT INTO posts VALUES (2,  2, 'Study spots',      'Clemons 3rd floor is underrated.', '2026-06-05 12:30:00');
INSERT INTO posts VALUES (3,  1, 'SQL is fun',       'Just learned about JOINs.',        '2026-06-10 15:15:00');
INSERT INTO posts VALUES (4,  3, 'Game day',         'Scott Stadium was loud today.',    '2026-06-15 18:00:00');
INSERT INTO posts VALUES (5,  5, 'Pandas tips',      'Always check df.dtypes first.',    '2026-07-01 10:45:00');
INSERT INTO posts VALUES (6,  6, 'Foreign keys',     'They keep your data consistent.',  '2026-07-12 14:20:00');
INSERT INTO posts VALUES (7,  4, 'Coffee rankings',  'Grit vs Mudhouse, discuss.',       '2026-08-03 08:10:00');
INSERT INTO posts VALUES (8,  7, 'Move-in week',     'Carrying boxes up four flights.',  '2026-08-20 16:50:00');
INSERT INTO posts VALUES (9,  5, 'Data engineering', 'ETL pipelines everywhere.',        '2026-09-08 11:35:00');
INSERT INTO posts VALUES (10, 8, 'Hiking Humpback',  'Great views this weekend.',        '2026-09-21 07:30:00');