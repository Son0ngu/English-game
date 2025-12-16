-- Seed user profile database (matching DBTable.sql schema)
-- Delete existing data
DELETE FROM items WHERE 1=1;
DELETE FROM student_profiles WHERE 1=1;
DELETE FROM teacher_profiles WHERE 1=1;
DELETE FROM user_profiles WHERE 1=1;

-- Insert user profiles for all auth users (id is TEXT)
INSERT INTO user_profiles (id, email, role, created_at, last_login) VALUES
  ('admin01', 'admin01@example.com', 'admin', strftime('%s', 'now'), strftime('%s', 'now')),
  ('teacher1', 'teacher1@example.com', 'teacher', strftime('%s', 'now'), strftime('%s', 'now')),
  ('teacher2', 'teacher2@example.com', 'teacher', strftime('%s', 'now'), strftime('%s', 'now')),
  ('student1', 'student1@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
  ('student2', 'student2@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
  ('student3', 'student3@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
  ('student4', 'student4@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now'));

-- Insert student profiles (with map progress fields)
INSERT INTO student_profiles (id, language_level, points, money, hp, atk, items, current_map, max_map_unlocked, maps_completed) VALUES
  ('student1', 1, 0, 100, 100, 10, '[]', 1, 1, '[]'),
  ('student2', 1, 0, 100, 100, 10, '[]', 1, 1, '[]'),
  ('student3', 1, 0, 100, 100, 10, '[]', 1, 1, '[]'),
  ('student4', 1, 0, 100, 100, 10, '[]', 1, 1, '[]');

-- Insert teacher profiles
INSERT INTO teacher_profiles (id, subjects) VALUES
  ('teacher1', '["English","Grammar"]'),
  ('teacher2', '["Vocabulary","Advanced English"]');

-- Create swords for each student
INSERT INTO items (id, name, description, price, effect, type, level, max_level, created_at, owner_id, is_template) VALUES
  ('sword_student1', 'Student1''s Sword', 'Personal sword', 0, 5, 'weapon', 1, 10, strftime('%s', 'now'), 'student1', 0),
  ('sword_student2', 'Student2''s Sword', 'Personal sword', 0, 5, 'weapon', 1, 10, strftime('%s', 'now'), 'student2', 0),
  ('sword_student3', 'Student3''s Sword', 'Personal sword', 0, 5, 'weapon', 1, 10, strftime('%s', 'now'), 'student3', 0),
  ('sword_student4', 'Student4''s Sword', 'Personal sword', 0, 5, 'weapon', 1, 10, strftime('%s', 'now'), 'student4', 0);
