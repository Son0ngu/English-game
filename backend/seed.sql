-- USERS
INSERT INTO auth_service (username, password, role) VALUES
('admin01', 'admin123', 'admin'),
('teacher1', 'teach123', 'teacher'),
('student1', 'stud123', 'student'),
('student2', 'stud123', 'student');

-- CLASSES
INSERT INTO classroom (id, name, teacher_id) VALUES
(1, 'English A1', 'teacher1'),
(2, 'Grammar Basic', 'teacher1');

-- STUDENTS IN CLASS
INSERT INTO student_class (student_id, class_id) VALUES
('student1', 1),
('student2', 1);

-- QUESTIONS: Multiple Choice
INSERT INTO question (class_id, type, difficulty, content, ans1, ans2, ans3, ans4, correct_answer) VALUES
(1, 'multiple_choice', 'easy', 'What is the capital of France?', 'Paris', 'London', 'Berlin', 'Rome', '["Paris"]'),
(1, 'multiple_choice', 'medium', 'Which words are verbs?', 'run', 'book', 'jump', 'table', '["run", "jump"]'),
(1, 'multiple_choice', 'hard', 'Which are prepositions?', 'on', 'with', 'quickly', 'car', '["on", "with"]');

-- QUESTIONS: True/False
INSERT INTO question (class_id, type, difficulty, content, correct_answer) VALUES
(1, 'true_false', 'easy', 'The sun rises in the east.', 'True'),
(1, 'true_false', 'medium', 'Bananas are vegetables.', 'False'),
(1, 'true_false', 'hard', 'Light travels slower than sound.', 'False');

-- QUESTIONS: Fill in the Blank
INSERT INTO question (class_id, type, difficulty, content, correct_answer) VALUES
(1, 'fill_in_the_blank', 'easy', 'He ___ a teacher.', 'is'),
(1, 'fill_in_the_blank', 'medium', 'They ___ to school every day.', 'go'),
(1, 'fill_in_the_blank', 'hard', 'The book ___ on the table.', 'is');

-- QUESTIONS: Single Choice
INSERT INTO question (class_id, type, difficulty, content, ans1, ans2, ans3, ans4, correct_answer) VALUES
(1, 'single_choice', 'easy', 'Choose the correct spelling.', 'becase', 'becuase', 'because', 'becuasee', 'because'),
(1, 'single_choice', 'medium', 'What is the synonym of "happy"?', 'sad', 'glad', 'angry', 'tired', 'glad'),
(1, 'single_choice', 'hard', 'Which is an adverb?', 'quick', 'quickly', 'quicker', 'quickest', 'quickly');
