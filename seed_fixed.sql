-- XÓA TOÀN BỘ DỮ LIỆU CŨ (không xóa cấu trúc bảng)
PRAGMA foreign_keys = OFF;   -- Tạm thời tắt kiểm tra khóa ngoại để xóa dữ liệu dễ dàng

DELETE FROM student_class WHERE 1=1;
DELETE FROM questions     WHERE 1=1;
DELETE FROM classes       WHERE 1=1;
DELETE FROM auth_service  WHERE 1=1;
DELETE FROM permission    WHERE 1=1;

PRAGMA foreign_keys = ON;    -- Bật lại kiểm tra khóa ngoại

-- USERS
INSERT INTO auth_service (user_id, username, password, role) VALUES
  ('admin01',   'admin01',   'admin123', 'admin'),
  ('teacher1',  'teacher1',  'teach123', 'teacher'),
  ('teacher2',  'teacher2',  'teach234', 'teacher'),
  ('student1',  'student1',  'stud123',  'student'),
  ('student2',  'student2',  'stud123',  'student'),
  ('student3',  'student3',  'stud234',  'student'),
  ('student4',  'student4',  'stud345',  'student');

-- CLASSES
INSERT INTO classes (id, name, code, teacher_id) VALUES
  ('class1', 'English A1',          'ENG-A1',  'teacher1'),
  ('class2', 'Grammar Basic',       'GRM-BSC', 'teacher1'),
  ('class3', 'Vocabulary Advanced', 'VOC-ADV', 'teacher2');

-- STUDENTS IN CLASS
INSERT INTO student_class (class_id, student_id) VALUES
  ('class1', 'student1'),
  ('class1', 'student2'),
  ('class1', 'student3'),
  ('class2', 'student2'),
  ('class2', 'student4'),
  ('class3', 'student3');

-- QUESTIONS - EASY LEVEL
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Multiple Choice - Easy
  ('easy_mc1',  'class1', 'What is the capital of France?',      'multiple_choice', 'easy',   '["Paris","London","Berlin","Rome"]',                0),
  ('easy_mc2', 'class1', 'Which planet is known as the Red Planet?', 'multiple_choice', 'easy', '["Mercury","Mars","Jupiter","Venus"]', 1),
  ('easy_mc3', 'class1', 'What is the boiling point of water at sea level?', 'multiple_choice', 'easy', '["90°C","100°C","110°C","120°C"]', 1),
  ('easy_mc4', 'class1', 'Which element has the chemical symbol "O"?', 'multiple_choice', 'easy', '["Osmium","Oxygen","Gold","Silver"]', 1),

  -- True/False - Easy
  ('easy_tf1',  'class1', 'The sun rises in the east.',            'true_false',      'easy',   '["True","False"]',                                   0),
  ('easy_tf2', 'class1', 'The programming language Python was named after a snake.', 'true_false', 'easy', '["True","False"]', 1),
  ('easy_tf3', 'class1', 'Light travels faster than sound.', 'true_false', 'easy', '["True","False"]', 0),
  ('easy_tf4', 'class1', 'Water is composed of two hydrogen atoms and one oxygen atom.', 'true_false', 'easy', '["True","False"]', 0),

  -- Fill in the Blank - Easy
  ('easy_fib1',  'class1', 'He ___ a teacher.',                     'fill_in_the_blank','easy', '["is"]',                                                0),
  ('easy_fib2', 'class1', 'The capital of Japan is ___.', 'fill_in_the_blank', 'easy', '["Tokyo"]', 0),
  ('easy_fib3', 'class1', 'Water freezes at ___ degrees Celsius.', 'fill_in_the_blank', 'easy', '["0"]', 0),

  -- Single Choice - Easy
  ('easy_sc1', 'class1', 'Choose the correct spelling.',          'single_choice',   'easy',   '["becase","becuase","because","becuasee"]',         2),
  ('easy_sc2', 'class1', 'Which country hosted the 2016 Summer Olympics?', 'single_choice', 'easy', '["China","Brazil","UK","Russia"]', 1),
  ('easy_sc3', 'class1', 'What is the square root of 64?', 'single_choice', 'easy', '["6","7","8","9"]', 2);

-- QUESTIONS - MEDIUM LEVEL
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Multiple Choice - Medium
  ('med_mc1',  'class1', 'Which words are verbs?',                'multiple_choice', 'medium', '["run","book","jump","table"]',                    0),
  ('med_mc2', 'class1', 'What is the largest ocean on Earth?', 'multiple_choice', 'medium', '["Atlantic","Indian","Arctic","Pacific"]', 3),
  ('med_mc3', 'class1', 'Who wrote "To Kill a Mockingbird"?', 'multiple_choice', 'medium', '["Harper Lee","Mark Twain","Jane Austen","Charles Dickens"]', 0),

  -- True/False - Medium
  ('med_tf1',  'class1', 'Bananas are vegetables.',               'true_false',      'medium', '["True","False"]',                                   1),
  ('med_tf2', 'class1', 'The human heart has four chambers.', 'true_false', 'medium', '["True","False"]', 0),
  ('med_tf3', 'class1', 'Venus is the closest planet to the Sun.', 'true_false', 'medium', '["True","False"]', 1),

  -- Fill in the Blank - Medium
  ('med_fib1',  'class1', 'They ___ to school every day.',         'fill_in_the_blank','medium','["go"]',                                                0),
  ('med_fib2', 'class1', '___ is known as the powerhouse of the cell.', 'fill_in_the_blank', 'medium', '["Mitochondria"]', 0),
  ('med_fib3', 'class1', 'The largest mammal on Earth is the ___.', 'fill_in_the_blank', 'medium', '["blue whale"]', 0),

  -- Single Choice - Medium
  ('med_sc1', 'class1', 'What is the synonym of "happy"?',       'single_choice',   'medium', '["sad","glad","angry","tired"]',                     1),
  ('med_sc2', 'class1', 'Who painted the Mona Lisa?', 'single_choice', 'medium', '["Van Gogh","Da Vinci","Picasso","Rembrandt"]', 1),
  ('med_sc3', 'class1', 'Which gas do plants absorb from the atmosphere?', 'single_choice', 'medium', '["Oxygen","Nitrogen","Carbon dioxide","Hydrogen"]', 2);

-- QUESTIONS - HARD LEVEL
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Multiple Choice - Hard
  ('hard_mc1',  'class1', 'Which are prepositions?',              'multiple_choice', 'hard',   '["on","with","quickly","car"]',                     0),

  -- True/False - Hard
  ('hard_tf1',  'class1', 'Light travels slower than sound.',      'true_false',      'hard',   '["True","False"]',                                   1),

  -- Fill in the Blank - Hard
  ('hard_fib1',  'class1', 'The book ___ on the table.',            'fill_in_the_blank','hard',  '["is"]',                                                0),
  ('hard_fib2', 'class1', 'The chemical formula for table salt is ___.', 'fill_in_the_blank', 'hard', '["NaCl"]', 0),

  -- Single Choice - Hard
  ('hard_sc1', 'class1', 'Which is an adverb?',                   'single_choice',   'hard',   '["quick","quickly","quicker","quickest"]',           1),
  ('hard_sc2', 'class1', 'In which year did World War II end?', 'single_choice', 'hard', '["1942","1945","1948","1950"]', 1);

-- QUESTIONS - VERY HARD LEVEL
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Multiple Choice - Very Hard
  ('vh_mc1', 'class1',
    'Which property distinguishes a Turing-complete system?',
    'multiple_choice','very hard',
    '["Decidability","Recursion","Universality","Confluence"]', 2),
  ('vh_mc2', 'class1',
    'Which theorem formalizes the undecidability of program behavior?',
    'multiple_choice','very hard',
    '["Cantor''s theorem","Gödel''s incompleteness theorem","Rice''s theorem","Noether''s theorem"]', 2),
  ('vh_mc3', 'class1',
    'In λ-calculus, the Y combinator is used to achieve:',
    'multiple_choice','very hard',
    '["Memoization","Recursion","Evaluation","Abstraction"]', 1),

  -- True/False - Very Hard
  ('vh_tf1', 'class1',
    'Every context-free language is recursively enumerable.',
    'true_false','very hard',
    '["True","False"]', 0),
  ('vh_tf2', 'class1',
    'The set of decidable problems is closed under complement.',
    'true_false','very hard',
    '["True","False"]', 0),

  -- Fill in the Blank - Very Hard
  ('vh_fib1', 'class1',
    'A function f is _______ if it halts on all inputs.',
    'fill_in_the_blank','very hard',
    '["total"]', 0),
  ('vh_fib2', 'class1',
    'A decision problem is ______-complete if it is among the hardest in NP.',
    'fill_in_the_blank','very hard',
    '["NP"]', 0),

  -- Single Choice - Very Hard
  ('vh_sc1', 'class1',
    'What is the space complexity class of QBF (Quantified Boolean Formula)?',
    'single_choice','very hard',
    '["P","NP","co-NP","PSPACE"]', 3),
  ('vh_sc2', 'class1',
    'Which complexity class allows nondeterministic polynomial-time verification?',
    'single_choice','very hard',
    '["P","NP","co-NP","PSPACE"]', 1);

-- More questions for class2 and class3 to ensure all classes have questions
INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Class 2 questions
  ('c2_easy1', 'class2', 'What is 2 + 2?', 'single_choice', 'easy', '["3","4","5","6"]', 1),
  ('c2_easy2', 'class2', 'Is English a language?', 'true_false', 'easy', '["True","False"]', 0),
  ('c2_med1', 'class2', 'The cat ___ on the mat.', 'fill_in_the_blank', 'medium', '["sits"]', 0),
  ('c2_hard1', 'class2', 'Which of these is a verb?', 'multiple_choice', 'hard', '["run","cat","blue","table"]', 0),

  -- Class 3 questions
  ('c3_easy1', 'class3', 'What color is the sky?', 'single_choice', 'easy', '["red","blue","green","yellow"]', 1),
  ('c3_easy2', 'class3', 'Dogs can fly.', 'true_false', 'easy', '["True","False"]', 1),
  ('c3_med1', 'class3', 'I ___ happy today.', 'fill_in_the_blank', 'medium', '["am"]', 0),
  ('c3_hard1', 'class3', 'Which word means the opposite of hot?', 'multiple_choice', 'hard', '["cold","warm","cool","freezing"]', 0);

-- PERMISSIONS - Fixed to match the schema (student, teacher, admin columns)
INSERT INTO permission (service, path, method, student, teacher, admin) VALUES
-- Admin service permissions
('admin', 'health', 'GET', 1, 1, 1),
('admin', 'services', 'GET', 0, 0, 1),
('admin', 'system-stats', 'GET', 0, 1, 1),
('admin', 'users', 'GET', 0, 0, 1),
('admin', 'users/add', 'POST', 0, 0, 1),
('admin', 'users/change-role', 'POST', 0, 0, 1),
('admin', 'permissions/add', 'POST', 0, 0, 1),
('admin', 'permissions/list', 'POST', 0, 0, 1),
('admin', 'permissions/delete', 'POST', 0, 0, 1),
('admin', 'permissions/check', 'POST', 0, 0, 1),
('admin', 'permissions/role', 'POST', 0, 0, 1),

-- Game service permissions
('game', 'newroom', 'POST', 1, 0, 1),
('game', 'get_question', 'POST', 1, 0, 1),
('game', 'check_answer', 'POST', 1, 0, 1),
('game', 'health', 'GET', 1, 1, 1),

-- User service permissions
('user', 'get', 'POST', 1, 1, 1),
('user', 'update', 'POST', 1, 1, 1),
('user', 'delete', 'POST', 1, 0, 1),
('user', 'stats-only', 'POST', 1, 1, 1),
('user', 'health', 'GET', 1, 1, 1),

-- Classroom service permissions
('classroom', 'create', 'POST', 0, 1, 1),
('classroom', 'join', 'POST', 1, 0, 1),
('classroom', 'students', 'POST', 0, 1, 1),
('classroom', 'dashboard', 'POST', 0, 1, 1),
('classroom', 'classes', 'POST', 0, 1, 1),
('classroom', 'student/classes', 'POST', 1, 0, 1),
('classroom', 'add_question', 'POST', 0, 1, 1),
('classroom', 'kick', 'POST', 0, 1, 1),
('classroom', 'questions', 'POST', 0, 1, 1),
('classroom', 'health', 'GET', 1, 1, 1),

-- Item service permissions
('item', 'user/sword', 'POST', 1, 0, 1),
('item', 'sword/upgrade', 'POST', 1, 0, 1),
('item', 'health', 'GET', 1, 1, 1),

-- Progress service permissions
('progress', 'complete-map', 'POST', 1, 0, 1),
('progress', 'user/maps', 'POST', 1, 0, 1),
('progress', 'user/summary', 'POST', 1, 0, 1),
('progress', 'leaderboard', 'POST', 1, 1, 1),
('progress', 'map/statistics', 'POST', 0, 1, 1),
('progress', 'health', 'GET', 1, 1, 1),

-- Feedback service permissions
('feedback', 'generate', 'POST', 1, 1, 1),
('feedback', 'user/feedback', 'POST', 1, 0, 1),
('feedback', 'get', 'POST', 1, 1, 1),
('feedback', 'health', 'GET', 1, 1, 1);
