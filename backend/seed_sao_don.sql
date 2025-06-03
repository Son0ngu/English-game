INSERT INTO user_profiles (
    id, email, role, created_at, last_login
) VALUES
      (
    'student1',
    'student03@example.com',
    'student',
    strftime('%s', 'now'),
    strftime('%s', 'now')
),
      (
    'student2',
    'student02@example.com',
    'student',
    strftime('%s', 'now'),
    strftime('%s', 'now')
),
      (
    'student3',
    'student04@example.com',
    'student',
    strftime('%s', 'now'),
    strftime('%s', 'now')
),
      (
    'student4',
    'student05@example.com',
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

INSERT INTO student_profiles (
    id, language_level, points, money, hp, atk, items
) VALUES (
    'student1',
    1, 0, 100, 100, 10, '[]'
),
      (
    'student2',
    1, 0, 100, 100, 10, '[]'
),
      (
    'student3',
    1, 0, 100, 100, 10, '[]'
);