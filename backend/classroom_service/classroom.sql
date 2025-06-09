-- Bảng lưu thông tin các lớp
CREATE TABLE IF NOT EXISTS classes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    teacher_id TEXT NOT NULL
);

-- Bảng lưu câu hỏi (không có topic), mỗi câu hỏi thuộc về một lớp
CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    class_id TEXT NOT NULL,
    question TEXT NOT NULL,
    q_type TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    choices TEXT NOT NULL,
    correct_index INTEGER NOT NULL,
    FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE
);

-- Bảng liên kết giữa học sinh và lớp
CREATE TABLE IF NOT EXISTS student_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    wins INTEGER DEFAULT 0,
    FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE
);
