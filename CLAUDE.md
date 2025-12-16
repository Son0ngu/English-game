# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

English-game is a Flask-based educational game backend with a microservices-style architecture. The application provides an English learning platform where students answer questions in a game format with RPG elements (HP, ATK, items, monsters). Teachers can create classes and manage questions, while students progress through maps and earn rewards.

## Technology Stack

- **Backend**: Flask 3.1.2 (Python 3.11-3.13)
- **Database**: SQLite (multiple databases: `database.db` and `userprofile.db`)
- **Authentication**: Flask-JWT-Extended with role-based access control
- **Dependency Injection**: Flask-Injector (optional DI support)
- **Frontend**: Vanilla HTML/JS (served via Flask templates and static files)

## Development Setup

### Installation
```bash
# Install dependencies using Poetry
poetry install

# Or if using pip
pip install -r pyproject.toml  # Note: Convert dependencies manually
```

### Running the Application
```bash
# Run backend server (port 13371)
python app.py

# Or with Poetry
poetry run python app.py

# Run frontend (separate terminal, port 8000)
cd front-end
./run.sh  # or: python3 -m http.server
```

### Database Seeding
```bash
# Seed all databases with complete data (recommended)
./seed_all.sh

# Or manually:
sqlite3 database.db < seed_fixed.sql
sqlite3 database.db < seed_class2_class3_questions.sql
sqlite3 userprofile.db < user_profile_service/DBTable.sql
sqlite3 userprofile.db < seed_userprofile.sql
```

See `SEEDING.md` for detailed seeding documentation.

## Architecture

### Service-Based Architecture

The application uses an **API Gateway pattern** where all requests flow through a central gateway that routes to specialized services:

1. **API Gateway** (`api_gateway/gateway_service.py`):
   - Catchall Flask route handler at `app.py:77-80`
   - Routes all requests to appropriate services via `services_route.py`
   - URL pattern: `/<service>/<destination>`

2. **Services** (each has a controller → service → repository pattern):
   - `auth_service`: Authentication (login/signup), role/permission management
   - `user_profile_service`: User profiles (student HP/ATK/money, teacher subjects)
   - `game_service`: Game room management, question fetching, answer checking
   - `classroom_service`: Class creation, student enrollment, question management
   - `admin_service`: System stats, user management, permission control
   - `progress_feedback`: Progress tracking and feedback generation
   - `item`: Sword upgrade system (students have a personal sword)

### Database Structure

**Two separate SQLite databases**:

1. **`database.db`** (classroom/auth system):
   - `auth_service`: user_id, username, password, role
   - `classes`: id, name, code, teacher_id
   - `student_class`: class_id, student_id (junction table)
   - `questions`: id, class_id, question, q_type, difficulty, choices, correct_index

2. **`userprofile.db`** (user profiles/items):
   - `user_profiles`: id, email, role, created_at, last_login
   - `student_profiles`: id, language_level, points, money, hp, atk, items, current_map, max_map_unlocked, maps_completed
   - `teacher_profiles`: id, subjects (JSON array)
   - `items`: id, name, description, price, effect, type, level, max_level, created_at, owner_id, is_template

### Authentication & Authorization

- **JWT tokens** with role-based access control (roles: `admin`, `teacher`, `student`)
- JWT contains: `identity` (user_id) and `role` claim
- Token location: headers and cookies (configured in `app.py:28-35`)
- Permission system in `auth_service/role_permission_service/permission_service.py`
- User ID extraction via `_get_user_id_from_jwt()` in `services_route.py:118-130`

### Game Logic

**Game Room System** (`game_service/gameroom/`):
- Each game session has a unique `session_id`
- `gameroom.py`: Stores session state (student_id, difficulty, monster, money_win, status)
- `game_logic_handler.py`: Manages combat logic (HP/ATK calculations)
- `game_room_controller.py`: Coordinates room creation, question fetching, answer checking
- Status codes: 0=playing, 1=win, 2=lose

**Question Types** (`game_service/question/`):
- Abstract base: `question.py:QuestionAbstract`
- Implementations: `question_multiple_choice.py`, `question_true_false.py`, `question_fill_in_the_blank.py`
- Questions stored in `database.db:questions` table with type, difficulty, choices (JSON), correct_index

## Key API Endpoints

### Auth Service
- `POST /auth/login` - Login with username/password, returns JWT
- `POST /auth/signup` - Create new account
- `POST /auth/HuyTranLayRoleTuID` - Get role from JWT token

### Game Service (requires JWT)
- `POST /game/newroom` - Create game session (params: difficulty, class_id)
- `POST /game/get_question` - Fetch question (params: session_id, class_id)
- `POST /game/check_answer` - Submit answer (params: session_id, answer, question_id)

### User Service (requires JWT)
- `POST /user/get` - Get current user profile (from JWT)
- `POST /user/update` - Update user profile
- `POST /user/stats-only` - Get user stats (HP/ATK/money)

### Classroom Service (requires JWT)
- `POST /classroom/create` - Create new class (teacher only)
- `POST /classroom/join` - Join class with code
- `POST /classroom/students` - Get students in class
- `POST /classroom/student/classes` - Get classes student is enrolled in
- `POST /classroom/add_question` - Add question to class

### Item Service (requires JWT)
- `POST /item/user/sword` - Get user's sword details
- `POST /item/sword/upgrade` - Upgrade sword (costs money, increases effect/ATK)

## Important Implementation Notes

### Dependency Injection
- Optional DI setup in `app.py:57-74` using Flask-Injector
- Gracefully falls back if DI fails (wrapped in try-except)
- Database interfaces stored in `app.user_db` and `app.item_db`

### User Profile Creation
- New users automatically get profiles created via `add_user_id_only()` in `database_interface.py:489`
- Students get a default sword created: `sword_{user_id}` in items table
- Profile type (student/teacher/admin) determines which profile table is used

### Error Handling
- Services use fallback Mock controllers if initialization fails (see `services_route.py:50-97`)
- Database connections are created per-operation (not persistent) via `_get_connection()`
- JSON fields (items, subjects) stored as strings, parsed with `json.loads()`

### Front-end Structure
- Static HTML files in `front-end/` directory
- Served independently via Python HTTP server on port 8000
- Backend templates in `backend/templates/` (legacy, mostly unused)
- Assets in `front-end/static/` and `front-end/assets/`

## Common Development Tasks

### Adding a New Service
1. Create service directory: `{service_name}_service/`
2. Implement controller → service → repository pattern
3. Add route handler in `api_gateway/services_route.py`
4. Register in `gateway_service.py:8` service_list
5. Add routing logic in `gateway_service.py:43-64`

### Adding a New Question Type
1. Create subclass of `QuestionAbstract` in `game_service/question/`
2. Implement `check_answer()` method
3. Update `game_resource_interface.py` to handle new type
4. Add q_type to database schema if needed

### Modifying User Stats
- Student stats (HP/ATK/money) in `student_profiles` table
- Update via `user_profile_service/user/user_service.py`
- Item effects (sword ATK bonus) handled separately in item service
- Money changes should trigger sword upgrade eligibility checks

## Testing Credentials (from seed.sql)

- Admin: `admin01` / `admin123`
- Teacher: `teacher1` / `teach123`
- Student: `student1` / `stud123`, `student2` / `stud123`

## Git Workflow

- Main branch: `game-scene-final`
- Database files (.db) are gitignored
- Backend was previously in `backend/` directory (now moved to root per git status)
