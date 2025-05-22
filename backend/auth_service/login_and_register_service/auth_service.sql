CREATE TABLE auth_service (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    role TEXT DEFAULT 'student' CHECK(role IN ('admin', 'student', 'teacher'))
);