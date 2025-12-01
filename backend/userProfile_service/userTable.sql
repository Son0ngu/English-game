-- Tạo bảng cho UserProfile
CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    role TEXT DEFAULT 'student',
    created_at INTEGER NOT NULL,
    last_login INTEGER NOT NULL
);

-- Tạo bảng cho StudentProfile
CREATE TABLE IF NOT EXISTS student_profiles (
    id INTEGER PRIMARY KEY,
    language_level INTEGER DEFAULT 1,
    points INTEGER DEFAULT 0,
    money INTEGER DEFAULT 100,
    hp INTEGER DEFAULT 100,
    atk INTEGER DEFAULT 10,
    items TEXT DEFAULT '[]',
    FOREIGN KEY (id) REFERENCES user_profiles(id)
);

-- Tạo bảng cho TeacherProfile
CREATE TABLE IF NOT EXISTS teacher_profiles (
    id INTEGER PRIMARY KEY,
    subjects TEXT DEFAULT '[]',
    FOREIGN KEY (id) REFERENCES user_profiles(id)
);

-- Tạo bảng cho Item
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price INTEGER DEFAULT 0,
    effect INTEGER DEFAULT 0,
    type TEXT,
    level INTEGER DEFAULT 1,
    max_level INTEGER DEFAULT 1,
    created_at INTEGER NOT NULL,
    owner_id TEXT,
    is_template BOOLEAN DEFAULT 0
);

