-- Thêm các user profile
INSERT INTO user_profiles (
    id, email, role, created_at, last_login
) VALUES 
    ('bf52e8fd-3f84-4f5e-a256-db811adc8b7c', 'student021@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
    ('student1', 'student03@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
    ('student2', 'student02@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
    ('student3', 'student04@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now')),
    ('student4', 'student05@example.com', 'student', strftime('%s', 'now'), strftime('%s', 'now'));

-- Thêm các student profile
INSERT INTO student_profiles (
    id, language_level, points, money, hp, atk, items
) VALUES 
    ('bf52e8fd-3f84-4f5e-a256-db811adc8b7c', 1, 0, 100, 100, 10, '[]'),
    ('student1', 1, 0, 100, 100, 10, '[]'),
    ('student2', 1, 0, 100, 100, 10, '[]'),
    ('student3', 1, 0, 100, 100, 10, '[]'),
    ('student4', 1, 0, 100, 100, 10, '[]');