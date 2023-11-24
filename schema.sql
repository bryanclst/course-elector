CREATE TABLE IF NOT EXISTS app_user
(
    user_id  SERIAL,
    email    VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255)        NOT NULL,
    PRIMARY KEY (USER_ID)
);

CREATE TABLE IF NOT EXISTS course
(
    course_id     SERIAL,
    course_letter CHAR(4)      NOT NULL,
    course_number SMALLINT     NOT NULL,
    title         VARCHAR(255) NOT NULL,
    credits       SMALLINT,
    major         VARCHAR(255),
    PRIMARY KEY (COURSE_ID)
);

CREATE TABLE IF NOT EXISTS rating
(
    rating_id   SERIAL,
    course_id   INT          NOT NULL,
    author_id   INT          NOT NULL,
    instructor  VARCHAR(255) NOT NULL,
    quality     SMALLINT     NOT NULL,
    difficulty  SMALLINT     NOT NULL,
    grade       CHAR(1),
    description TEXT,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (course_id) REFERENCES course (course_id),
    FOREIGN KEY (author_id) REFERENCES app_user (user_id)
);

CREATE TABLE IF NOT EXISTS post
(
    post_id   SERIAL,
    course_id INT          NOT NULL,
    author_id INT          NOT NULL,
    subject   VARCHAR(255) NOT NULL,
    body      TEXT         NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (course_id) REFERENCES course (course_id),
    FOREIGN KEY (author_id) REFERENCES app_user (user_id)
);

CREATE TABLE IF NOT EXISTS comment
(
    comment_id SERIAL,
    post_id    INT  NOT NULL,
    author_id  INT  NOT NULL,
    body       TEXT NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_id) REFERENCES post (post_id),
    FOREIGN KEY (author_id) REFERENCES app_user (user_id)
);