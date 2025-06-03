INSERT INTO user_profiles (
    id, email, role, created_at, last_login
) VALUES (
    'bf52e8fd-3f84-4f5e-a256-db811adc8b7c',
    'student021@example.com',
    'student',
    strftime('%s', 'now'),
    strftime('%s', 'now')
);

-- Thêm profile học sinh tương ứng vào student_profiles
INSERT INTO student_profiles (
    id, language_level, points, money, hp, atk, items
) VALUES (
    'bf52e8fd-3f84-4f5e-a256-db811adc8b7c',
    1, 0, 100, 100, 10, '[]'
);
