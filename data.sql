-- Insert dummy data into app_user table
INSERT INTO app_user (email, username, hashed_password) VALUES
('user1@example.com', 'user1', 'hashed_password_1'),
('user2@example.com', 'user2', 'hashed_password_2'),
('user3@example.com', 'user3', 'hashed_password_3');

-- Insert dummy data into course table
INSERT INTO course (course_letter, course_number, title, credits, major) VALUES
('COMP', 1101, 'Introduction to Computer Science', 3, 'Computer Science'),
('MATH', 1201, 'Calculus I', 4, 'Mathematics'),
('PHYS', 1301, 'Physics Mechanics', 4, 'Physics');

-- Insert dummy data into rating table
INSERT INTO rating (course_id, author_id, instructor, quality, difficulty, grade, description) VALUES
(1, 1, 'Prof. Smith', 4, 3, 'A', 'Great course!'),
(2, 2, 'Prof. Johnson', 3, 4, 'B', 'Challenging but interesting'),
(3, 3, 'Prof. Davis', 5, 2, 'A', 'Best physics class ever!');

-- Insert dummy data into post table
INSERT INTO post (course_id, author_id, subject, body) VALUES
(1, 1, 'Question about Assignment 1', 'I need help with question 3. Any suggestions?'),
(2, 2, 'Midterm Review Session', 'Let''s organize a review session for the upcoming midterm.'),
(3, 3, 'Exciting News!', 'I aced the physics exam!');

-- Insert dummy data into comment table
INSERT INTO comment (post_id, author_id, body) VALUES
(1, 2, 'Sure! I had trouble with that too. Let''s discuss it.'),
(1, 3, 'I found question 3 tricky as well. Let''s work on it together.'),
(2, 1, 'I''m in for the review session!'),
(3, 2, 'Congratulations! That''s awesome!');