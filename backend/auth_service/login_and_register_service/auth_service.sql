CREATE TABLE IF NOT EXISTS auth_service (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'student' CHECK(role IN ('admin', 'student', 'teacher'))
);