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

INSERT INTO questions (id, class_id, question, q_type, difficulty, choices, correct_index) VALUES
  -- Multiple Choice (có thể có nhiều lựa chọn, correct_index là vị trí đầu tiên của đáp án đúng)
  ('q1',  'class1', 'What is the capital of France?',      'multiple_choice', 'easy',   '["Paris","London","Berlin","Rome"]',                0),
  ('q2',  'class1', 'Which words are verbs?',                'multiple_choice', 'medium', '["run","book","jump","table"]',                    0),
  ('q3',  'class1', 'Which are prepositions?',              'multiple_choice', 'hard',   '["on","with","quickly","car"]',                     0),

  -- True/False (choices cố định luôn là ["True","False"])
  ('q4',  'class1', 'The sun rises in the east.',            'true_false',      'easy',   '["True","False"]',                                   0),
  ('q5',  'class1', 'Bananas are vegetables.',               'true_false',      'medium', '["True","False"]',                                   1),
  ('q6',  'class1', 'Light travels slower than sound.',      'true_false',      'hard',   '["True","False"]',                                   1),

  -- Fill in the Blank (không có choices; ở đây ta ghi choices = '[]' và correct_index = 0,
  --   phần kiểm tra đáp án fill-in phải được xử lý riêng trong ứng dụng)
  ('q7',  'class1', 'He ___ a teacher.',                     'fill_in_the_blank','easy', '[]',                                                0),
  ('q8',  'class1', 'They ___ to school every day.',         'fill_in_the_blank','medium','[]',                                                0),
  ('q9',  'class1', 'The book ___ on the table.',            'fill_in_the_blank','hard',  '[]',                                                0),

  -- Single Choice (chỉ có một đáp án đúng, correct_index là vị trí của đáp án đúng)
  ('q10', 'class1', 'Choose the correct spelling.',          'single_choice',   'easy',   '["becase","becuase","because","becuasee"]',         2),
  ('q11', 'class1', 'What is the synonym of "happy"?',       'single_choice',   'medium', '["sad","glad","angry","tired"]',                     1),
  ('q12', 'class1', 'Which is an adverb?',                   'single_choice',   'hard',   '["quick","quickly","quicker","quickest"]',           1);
