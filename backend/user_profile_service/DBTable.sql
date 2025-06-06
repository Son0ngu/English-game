-- English Game Database Schema
-- Created for UserProfile Service
-- Encoding: UTF-8

-- Tạo bảng cho UserProfile (thông tin cơ bản của người dùng)
CREATE TABLE IF NOT EXISTS user_profiles (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,           -- Email duy nhất cho mỗi user
    role TEXT DEFAULT 'student',          -- Vai trò: 'student' hoặc 'teacher'
    created_at INTEGER NOT NULL,          -- Thời gian tạo (Unix timestamp)
    last_login INTEGER NOT NULL           -- Lần đăng nhập cuối (Unix timestamp)
);

-- Tạo bảng cho StudentProfile (thông tin học sinh)
CREATE TABLE IF NOT EXISTS student_profiles (
    id TEXT PRIMARY KEY,               -- Khóa ngoại liên kết với user_profiles.id
    language_level INTEGER DEFAULT 1,     -- Cấp độ ngôn ngữ hiện tại
    points INTEGER DEFAULT 0,             -- Điểm số tích lũy
    money INTEGER DEFAULT 100,            -- Tiền trong game
    hp INTEGER DEFAULT 100,               -- Máu (Health Points)
    atk INTEGER DEFAULT 10,               -- Sức tấn công (Attack)
    items TEXT DEFAULT '[]',              -- Danh sách vật phẩm (JSON format)
    current_map INTEGER DEFAULT 1,         -- Bản đồ hiện tại
    maps_completed TEXT DEFAULT '[]',      -- JSON array các bản đồ đã hoàn thành
    max_map_unlocked INTEGER DEFAULT 1,     -- Bản đồ cao nhất đã mở khóa
    FOREIGN KEY (id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

-- Tạo bảng cho TeacherProfile (thông tin giáo viên)
CREATE TABLE IF NOT EXISTS teacher_profiles (
    id TEXT PRIMARY KEY,               -- Khóa ngoại liên kết với user_profiles.id
    subjects TEXT DEFAULT '[]',           -- Danh sách môn học giảng dạy (JSON format)
    FOREIGN KEY (id) REFERENCES user_profiles(id) ON DELETE CASCADE
);

-- Tạo bảng cho Item (vật phẩm trong game)
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,                  -- ID duy nhất của vật phẩm
    name TEXT NOT NULL,                   -- Tên vật phẩm
    description TEXT,                     -- Mô tả vật phẩm
    price INTEGER DEFAULT 0,              -- Giá mua vật phẩm
    effect INTEGER DEFAULT 0,             -- Hiệu ứng (damage, heal, etc.)
    type TEXT,                            -- Loại vật phẩm (weapon, armor, consumable, etc.)
    level INTEGER DEFAULT 1,              -- Cấp độ hiện tại của vật phẩm
    max_level INTEGER DEFAULT 1,          -- Cấp độ tối đa có thể nâng cấp
    created_at INTEGER NOT NULL,          -- Thời gian tạo (Unix timestamp)
    owner_id TEXT,                        -- ID người sở hữu (NULL nếu là template)
    is_template BOOLEAN DEFAULT 0         -- 1 nếu là template, 0 nếu là vật phẩm cá nhân
);

-- Tạo các index để tăng tốc độ truy vấn
CREATE INDEX IF NOT EXISTS idx_user_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_role ON user_profiles(role);
CREATE INDEX IF NOT EXISTS idx_student_level ON student_profiles(language_level);
CREATE INDEX IF NOT EXISTS idx_item_owner ON items(owner_id);
CREATE INDEX IF NOT EXISTS idx_item_template ON items(is_template);
CREATE INDEX IF NOT EXISTS idx_item_type ON items(type);
CREATE INDEX IF NOT EXISTS idx_student_current_map ON student_profiles(current_map);
CREATE INDEX IF NOT EXISTS idx_student_max_map ON student_profiles(max_map_unlocked);

-- Insert một số dữ liệu mẫu (optional - có thể comment lại nếu không cần)
-- INSERT OR IGNORE INTO user_profiles (email, role, created_at, last_login) 
-- VALUES ('admin@example.com', 'teacher', strftime('%s', 'now'), strftime('%s', 'now'));

-- Tạo một số item template mẫu
INSERT OR IGNORE INTO items (id, name, description, price, effect, type, level, max_level, created_at, owner_id, is_template)
VALUES 
    ('default_sword_template', 'Basic Sword', 'A basic sword for all students', 0, 5, 'weapon', 1, 10, strftime('%s', 'now'), NULL, 1);

