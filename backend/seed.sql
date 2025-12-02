-- XÓA TOÀN BỘ DỮ LIỆU CŨ (không xóa cấu trúc bảng)
PRAGMA foreign_keys = OFF;   -- Tạm thời tắt kiểm tra khóa ngoại để xóa dữ liệu dễ dàng

DELETE FROM student_class WHERE 1=1;
DELETE FROM questions     WHERE 1=1;
DELETE FROM classes       WHERE 1=1;
DELETE FROM auth_service  WHERE 1=1;

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

INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_answers) VALUES
  ('mcq01', 'class1', 'Which animals are mammals?', 'multiple_choice', 'easy',
    '["Whale","Shark","Dolphin","Eagle"]', '["Whale","Dolphin"]'),
  ('mcq02', 'class1', 'Which of the following are prime numbers?', 'multiple_choice', 'easy',
    '["2","3","4","5","6","7"]', '["2","3","5","7"]'),
  ('mcq03', 'class1', 'Which elements are noble gases?', 'multiple_choice', 'medium',
    '["Helium","Neon","Oxygen","Nitrogen"]', '["Helium","Neon"]'),
  ('mcq04', 'class1', 'Which of these are programming languages?', 'multiple_choice', 'medium',
    '["Python","HTML","Java","Excel"]', '["Python","Java"]'),
  ('mcq05', 'class1', 'Select the fruits from the list below:', 'multiple_choice', 'hard',
    '["Apple","Tomato","Cucumber","Potato"]', '["Apple","Tomato"]'),

  ('tf01', 'class1', 'The programming language Python was named after a snake.', 'true_false', 'easy',
    '["True","False"]', '["False"]'),
  ('tf02', 'class1', 'Light travels faster than sound.', 'true_false', 'easy',
    '["True","False"]', '["True"]'),
  ('tf03', 'class1', 'The human heart has four chambers.', 'true_false', 'medium',
    '["True","False"]', '["True"]'),
  ('tf04', 'class1', 'Venus is the closest planet to the Sun.', 'true_false', 'medium',
    '["True","False"]', '["False"]'),
  ('tf05', 'class1', 'Water is composed of two hydrogen atoms and one oxygen atom.', 'true_false', 'easy',
    '["True","False"]', '["True"]'),

  ('fb01', 'class1', 'The capital of Japan is ___.', 'fill_in_the_blank', 'easy',
    '[]', '["Tokyo"]'),
  ('fb02', 'class1', '___ is known as the powerhouse of the cell.', 'fill_in_the_blank', 'medium',
    '[]', '["Mitochondria"]'),
  ('fb03', 'class1', 'Water freezes at ___ degrees Celsius.', 'fill_in_the_blank', 'easy',
    '[]', '["0"]'),
  ('fb04', 'class1', 'The largest mammal on Earth is the ___.', 'fill_in_the_blank', 'medium',
    '[]', '["Blue whale"]'),
  ('fb05', 'class1', 'The chemical formula for table salt is ___.', 'fill_in_the_blank', 'hard',
    '[]', '["NaCl"]'),

  ('sc01', 'class1', 'Which country hosted the 2016 Summer Olympic Games?', 'single_choice', 'easy',
    '["China","Brazil","UK","Russia"]', '["Brazil"]'),
  ('sc02', 'class1', 'What is the square root of 64?', 'single_choice', 'easy',
    '["6","7","8","9"]', '["8"]'),
  ('sc03', 'class1', 'Who painted the Mona Lisa?', 'single_choice', 'medium',
    '["Van Gogh","Da Vinci","Picasso","Rembrandt"]', '["Da Vinci"]'),
  ('sc04', 'class1', 'Which gas do plants absorb from the atmosphere?', 'single_choice', 'medium',
    '["Oxygen","Nitrogen","Carbon dioxide","Hydrogen"]', '["Carbon dioxide"]'),
  ('sc05', 'class1', 'In which year did World War II end?', 'single_choice', 'hard',
    '["1942","1945","1948","1950"]', '["1945"]');

-- ADMIN PERMISSIONS SEED DATA
INSERT OR IGNORE INTO permission (role, path, service, method) VALUES
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