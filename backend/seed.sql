-- XÓA TOÀN BỘ DỮ LIỆU CŨ (không xóa cấu trúc bảng)
PRAGMA foreign_keys = OFF;   -- Tạm thời tắt kiểm tra khóa ngoại để xóa dữ liệu dễ dàng

DELETE FROM student_class WHERE 1=1;
DELETE FROM questions     WHERE 1=1;
DELETE FROM classes       WHERE 1=1;
DELETE FROM auth_service  WHERE 1=1;

PRAGMA foreign_keys = ON;    -- Bật lại kiểm tra khóa ngoại

-- USERS
INSERT OR IGNORE INTO auth_service (user_id, username, password, role) VALUES
  ('admin01',   'admin01',   'admin123', 'admin'),
  ('teacher1',  'teacher1',  'teach123', 'teacher'),
  ('teacher2',  'teacher2',  'teach234', 'teacher'),
  ('student1',  'student1',  'stud123',  'student'),
  ('student2',  'student2',  'stud123',  'student'),
  ('student3',  'student3',  'stud234',  'student'),
  ('student4',  'student4',  'stud345',  'student');

-- CLASSES
INSERT OR IGNORE INTO classes (id, name, code, teacher_id) VALUES
  ('class1', 'English A1',          'ENG-A1',  'teacher1'),
  ('0c8b623a', '123',          'ENG-A1',  'teacher1'),
  ('class2', 'Grammar Basic',       'GRM-BSC', 'teacher1'),
  ('class3', 'Vocabulary Advanced', 'VOC-ADV', 'teacher2');

-- STUDENTS IN CLASS
INSERT OR IGNORE INTO student_class (class_id, student_id) VALUES
  ('class1', 'student1'),
  ('class1', 'student2'),
  ('class1', 'student3'),
  ('class2', 'student2'),
  ('class2', 'student4'),
  ('class3', 'student3');

INSERT OR IGNORE INTO student_class (class_id, student_id) VALUES
  ('6f3303f2', 'student1'),
  ('6f3303f2', 'student2'),
  ('6f3303f2', 'student3'),
  ('6f3303f2', 'student2'),
  ('6f3303f2', 'student4'),
  ('6f3303f2', 'student3');

INSERT OR IGNORE INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Multiple Choice (có thể có nhiều lựa chọn, correct_index là vị trí đầu tiên của đáp án đúng)
  ('dawdwad',  'class1', 'What is the capital of France?',      'multiple_choice', 'easy',   '["Paris","London","Berlin","Rome"]',                0),
  ('rfwsavrnwoiv',  'class1', 'Which words are verbs?',                'multiple_choice', 'medium', '["run","book","jump","table"]',                    0),
  ('cbepiorchweoihc',  'class1', 'Which are prepositions?',              'multiple_choice', 'hard',   '["on","with","quickly","car"]',                     0),

  -- True/False (choices cố định luôn là ["True","False"])
  ('ipouecsoic',  'class1', 'The sun rises in the east.',            'true_false',      'easy',   '["True","False"]',                                   0),
  ('ubaiuduibwle',  'class1', 'Bananas are vegetables.',               'true_false',      'medium', '["True","False"]',                                   1),
  ('bsfiubfesiufbviesu',  'class1', 'Light travels slower than sound.',      'true_false',      'hard',   '["True","False"]',                                   1),

  -- Fill in the Blank (không có choices; ở đây ta ghi choices = '[]' và correct_index = 0,
  --   phần kiểm tra đáp án fill-in phải được xử lý riêng trong ứng dụng)
  ('q7',  'class1', 'He ___ a teacher.',                     'fill_in_the_blank','easy', '[]',                                                0),
  ('q8',  'class1', 'They ___ to school every day.',         'fill_in_the_blank','medium','[]',                                                0),
  ('q9',  'class1', 'The book ___ on the table.',            'fill_in_the_blank','hard',  '[]',                                                0),

  -- Single Choice (chỉ có một đáp án đúng, correct_index là vị trí của đáp án đúng)
  ('q10', 'class1', 'Choose the correct spelling.',          'single_choice',   'easy',   '["becase","becuase","because","becuasee"]',         2),
  ('q11', 'class1', 'What is the synonym of "happy"?',       'single_choice',   'medium', '["sad","glad","angry","tired"]',                     1),
  ('q12', 'class1', 'Which is an adverb?',                   'single_choice',   'hard',   '["quick","quickly","quicker","quickest"]',           1);

-- Thêm 5 câu MULTIPLE CHOICE (q_type = 'multiple')
INSERT OR IGNORE INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('mcq01', 'class1', 'Which planet is known as the Red Planet?', 'multiple', 'easy',
             '["Mercury","Mars","Jupiter","Venus"]', 1),
  ('mcq02', 'class1', 'What is the boiling point of water at SEA LEVEL?', 'multiple', 'easy',
             '["90°C","100°C","110°C","120°C"]', 1),
  ('mcq03', 'class1', 'Which element has the chemical symbol "O"?', 'multiple', 'easy',
             '["Osmium","Oxygen","Gold","Silver"]', 1),
  ('mcq04', 'class1', 'What is the largest ocean on Earth?', 'multiple', 'medium',
             '["Atlantic","Indian","Arctic","Pacific"]', 3),
  ('mcq05', 'class1', 'Who wrote "To Kill a Mockingbird"?', 'multiple', 'medium',
             '["Harper Lee","Mark Twain","Jane Austen","Charles Dickens"]', 0);

-- Thêm 5 câu TRUE/FALSE (q_type = 'true_false')
--    (choices cố định: ["True","False"], chỉ cần đúng vị trí 0= True, 1= False)
INSERT OR IGNORE INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('tf01', 'class1', 'The programming language Python was named after a snake.', 'true_false', 'easy',
            '["True","False"]', 1),
  ('tf02', 'class1', 'Light travels faster than sound.', 'true_false', 'easy',
            '["True","False"]', 0),
  ('tf03', 'class1', 'The human heart has four chambers.', 'true_false', 'medium',
            '["True","False"]', 0),
  ('tf04', 'class1', 'Venus is the closest planet to the Sun.', 'true_false', 'medium',
            '["True","False"]', 1),
  ('tf05', 'class1', 'Water is composed of two hydrogen atoms and one oxygen atom.', 'true_false', 'easy',
            '["True","False"]', 0);

-- Thêm 5 câu FILL-IN-THE-BLANK (q_type = 'fill_blank')
--    Ở đây ta đặt choices = '[]' (chuỗi JSON rỗng) và correct_index = 0 (mặc định)
--    Khi kiểm tra đáp án, ứng dụng phía client/server phải so sánh thủ công.
INSERT OR IGNORE INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('fb01', 'class1', 'The capital of Japan is ___.', 'fill_blank', 'easy', '[]', 0),
  ('fb02', 'class1', '___ is known as the powerhouse of the cell.', 'fill_blank', 'medium', '[]', 0),
  ('fb03', 'class1', 'Water freezes at ___ degrees Celsius.', 'fill_blank', 'easy', '[]', 0),
  ('fb04', 'class1', 'The largest mammal on Earth is the ___.', 'fill_blank', 'medium', '[]', 0),
  ('fb05', 'class1', 'The chemical formula for table salt is ___.', 'fill_blank', 'hard', '[]', 0);

-- Thêm 5 câu SINGLE CHOICE (q_type = 'single')
--    (tương tự MCQ, nhưng chỉ có đúng 1 đáp án)
INSERT OR IGNORE INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  ('sc01', 'class1', 'Which country hosted the 2016 Summer Olympics?', 'single', 'easy',
             '["China","Brazil","UK","Russia"]', 1),
  ('sc02', 'class1', 'What is the square root of 64?', 'single', 'easy',
             '["6","7","8","9"]', 2),
  ('sc03', 'class1', 'Who painted the Mona Lisa?', 'single', 'medium',
             '["Van Gogh","Da Vinci","Picasso","Rembrandt"]', 1),
  ('sc04', 'class1', 'Which gas do plants absorb from the atmosphere?', 'single', 'medium',
             '["Oxygen","Nitrogen","Carbon dioxide","Hydrogen"]', 2),
  ('sc05', 'class1', 'In which year did World War II end?', 'single', 'hard',
             '["1942","1945","1948","1950"]', 1);

-- ADMIN PERMISSIONS SEED DATA
INSERT OR IGNORE INTO permissions (role, path, service, method) VALUES
-- Admin permissions (full access)
('admin', 'health', 'admin', 'GET'),
('admin', 'services', 'admin', 'GET'),
('admin', 'system-stats', 'admin', 'GET'),
('admin', 'users', 'admin', 'GET'),
('admin', 'users/add', 'admin', 'POST'),
('admin', 'users/change-role', 'admin', 'POST'),
('admin', 'permissions/add', 'admin', 'POST'),
('admin', 'permissions/list', 'admin', 'POST'),
('admin', 'permissions/delete', 'admin', 'POST'),
('admin', 'permissions/check', 'admin', 'POST'),
('admin', 'permissions/role', 'admin', 'POST'),

-- Teacher permissions (limited admin access)
('teacher', 'users', 'admin', 'GET'),
('teacher', 'system-stats', 'admin', 'GET'),

-- Student permissions (very limited)
('student', 'health', 'admin', 'GET');