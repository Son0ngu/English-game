# Debugging /classroom/increment_win 500 Error

## Error Description

When winning a game, the frontend calls `POST /classroom/increment_win` and receives a 500 Internal Server Error:

```
POST http://127.0.0.1:13371/classroom/increment_win 500 (INTERNAL SERVER ERROR)
```

## Root Cause Analysis

The `/classroom/increment_win` endpoint fails when:
1. The student is not enrolled in the class (no row in `student_class` table)
2. The `class_id` or `student_id` don't match database records

### How It Works

**JWT Flow:**
1. User logs in → JWT created with `identity=user_id` from `auth_service` table
2. Game room created → Uses `get_jwt_identity()` to get `student_id`
3. On win → Frontend sends `{ class_id, student_id: gameSession.student_id }`
4. Backend tries: `UPDATE student_class SET wins = wins + 1 WHERE class_id = ? AND student_id = ?`

**Code Locations:**
- JWT creation: `api_gateway/services_route.py:504`
- Game room creation: `api_gateway/services_route.py:404` (`student_id = get_jwt_identity()`)
- Increment win: `classroom_service/classroom_service.py:228-241`

### Database Schema

```sql
-- auth_service table
CREATE TABLE auth_service (
    user_id TEXT PRIMARY KEY,      -- Can be username or UUID
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'student'
);

-- student_class junction table
CREATE TABLE student_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id TEXT NOT NULL,
    student_id TEXT NOT NULL,      -- Must match auth_service.user_id
    wins INTEGER DEFAULT 0,
    UNIQUE(class_id, student_id),
    FOREIGN KEY(class_id) REFERENCES classes(id)
);
```

**Sample Data:**
```
-- auth_service
user_id | username | role
--------+----------+---------
student1 | student1 | student
student2 | student2 | student
246e... | hehe     | student   (UUID-based ID)

-- student_class
class_id | student_id | wins
---------+------------+------
class1   | student1   | 0
class1   | student2   | 0
class2   | student2   | 0
```

## Why It Fails (500 Error)

The `increment_student_win()` method returns `False` when:
1. **No matching row found**: Student not enrolled in that class
2. **Database error**: Exception occurs during UPDATE

```python
# classroom_service/classroom_service.py:228
def increment_student_win(self, class_id: str, student_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE student_class SET wins = wins + 1 WHERE class_id = ? AND student_id = ?;",
            (class_id, student_id)
        )
        conn.commit()
        return cursor.rowcount > 0  # False if no rows updated
    except Exception:
        return False
    finally:
        conn.close()
```

If `cursor.rowcount > 0` is False (no rows matched), the controller returns 500:
```python
# classroom_controller.py:170
else:
    return jsonify({"error": "Update failed"}), 500
```

## Fixed Frontend Error Handling

Previously, the frontend treated ALL 500 errors as token expiration and redirected to login. This has been fixed:

**Before (WRONG):**
```javascript
if (incrementResponse.status === 401 || incrementResponse.status === 500) {
    // Redirect to login
}
```

**After (CORRECT):**
```javascript
if (incrementResponse.status === 401) {
    // Only 401 = token expired, redirect to login
} else if (!incrementResponse.ok) {
    const errorText = await incrementResponse.text();
    console.error('Failed to increment win count:', errorText);
    console.error('Payload sent:', { class_id, student_id });
    // Continue anyway - don't block user from seeing results
}
```

## How to Debug

### Step 1: Check Console Logs

With the updated frontend, you'll now see detailed logs:
```javascript
Failed to increment win count: {"error":"Update failed"}
Payload sent: {
    class_id: "class1",
    student_id: "student1"  // or might be UUID
}
```

### Step 2: Verify Student Enrollment

Check if the student is enrolled in the class:
```sql
SELECT * FROM student_class
WHERE class_id = 'class1' AND student_id = 'student1';
```

If this returns no rows, the student needs to be enrolled first.

### Step 3: Check JWT Identity

When creating game room, backend logs the student_id:
```
Creating game room with student_id: student1 difficulty: easy class_id: class1
```

Verify this ID exists in `student_class` for that class.

## Solutions

### Solution 1: Enroll Student in Class (Recommended)

Students must join the class before playing:
```javascript
// Frontend should call this first
POST /classroom/join
Body: { code: "ABC123" }  // Class code from teacher
```

This inserts a row into `student_class`:
```sql
INSERT OR IGNORE INTO student_class (class_id, student_id) VALUES (?, ?);
```

### Solution 2: Auto-Enroll on Game Start (Quick Fix)

Modify the game room creation to auto-enroll:
```python
# In gameroom_service.py create_game_room():
# After line 26, add:
from classroom_service.classroom_service import ClassroomService
classroom_service = ClassroomService()

# Check if student is in class, if not, auto-enroll
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute(
    "INSERT OR IGNORE INTO student_class (class_id, student_id) VALUES (?, ?)",
    (class_id, student_id)
)
conn.commit()
conn.close()
```

### Solution 3: Make Endpoint More Forgiving (Backend Fix)

Change the endpoint to return 200 even if no rows updated:
```python
# classroom_controller.py:159
def increment_win(self):
    data = request.get_json()
    if not data or "class_id" not in data or "student_id" not in data:
        return jsonify({"error": "Missing class_id or student_id"}), 400

    success = self.service.increment_student_win(
        data["class_id"], data["student_id"]
    )

    # Changed: Don't fail if student not in class
    if success:
        return jsonify({"success": True, "incremented": True}), 200
    else:
        # Log the issue but don't fail the request
        print(f"Could not increment win for student {data['student_id']} in class {data['class_id']}")
        return jsonify({"success": True, "incremented": False, "message": "Student not enrolled in class"}), 200
```

## Testing

1. **Login as student1**:
   ```bash
   curl -X POST http://localhost:13371/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"student1","password":"stud123"}'
   ```

2. **Join a class**:
   ```bash
   curl -X POST http://localhost:13371/classroom/join \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"code":"CLASS_CODE"}'
   ```

3. **Play game and win** - increment_win should now succeed

4. **Verify win count**:
   ```sql
   SELECT * FROM student_class WHERE student_id = 'student1';
   ```

## Files Modified

1. `front-end/templates/gamePage/gamePage.js` - Fixed error handling
2. `front-end/templates/gamePage2/gamePage2.js` - Fixed error handling
3. `front-end/templates/gamePage3/gamePage3.js` - Fixed error handling

All three files now:
- Only redirect on 401 (not 500)
- Log detailed error information
- Continue to game results even if backend calls fail
