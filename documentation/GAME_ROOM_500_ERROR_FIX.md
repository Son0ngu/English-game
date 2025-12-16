# Game Room 500 Error Fix

## Bug Description

**Issue**: gamePage2 (levels 4-6) showed "Failed to Load Game" error with 500 Internal Server Error when calling `/game/newroom` endpoint.

**Error Symptoms**:
```
127.0.0.1:13371/game/newroom:1 Failed to load resource: the server responded with a status of 500 (INTERNAL SERVER ERROR)
gamePage2.js:391 API Response status: 500
gamePage2.js:437 Failed to create game room: Error: HTTP error! status: 500
```

## Root Cause

The `/game/newroom` endpoint calls `user_service.get_user_stats_only(student_id)` to retrieve player HP and ATK stats from `userprofile.db`.

**Problem**: If a user exists in `database.db` (auth_service table) but NOT in `userprofile.db` (user_profiles + student_profiles tables), the game room creation fails with 500 error.

**How This Happens**:
1. User registers successfully → entry created in `auth_service` table
2. `signup_service.sign_up()` should call `add_user_id_only()` to create profile
3. If profile creation fails or user was created before this logic existed → profile missing
4. User logs in successfully (auth only checks `auth_service` table)
5. User tries to play → game service can't find their stats → 500 error

## The Fix

### Backend Changes

**File**: `game_service/gameroom/gameroom_service.py` (lines 17-34)

Added auto-create logic when user profile is missing:

```python
def create_game_room(self, student_id, difficulty, class_id):
    try:
        session_id = str(uuid.uuid4())
        player_data = self.user_service.get_user_stats_only(student_id)

        # Auto-create user profile if it doesn't exist
        if player_data is None:
            print(f"User profile not found for {student_id}, creating default profile...")
            self.user_service.add_user_id_only(student_id, role="student")
            player_data = self.user_service.get_user_stats_only(student_id)

        if player_data is None:
            raise ValueError(f"Failed to create user profile for {student_id}")

        atk = player_data.get("atk")
        hp = player_data.get("hp")
        if atk is None or hp is None:
            raise ValueError("Stats not found")

        # ... rest of game room creation
```

### How It Works

1. **Check for Profile**: Call `get_user_stats_only(student_id)`
2. **Auto-Create if Missing**: If `None`, call `add_user_id_only(student_id, role="student")`
3. **Default Stats Created**:
   - HP: 100
   - ATK: 10
   - Level: 1
   - Money: 100
   - Items: empty array
   - Default sword item
4. **Retry Fetch**: Get stats again after creation
5. **Validate**: Ensure HP and ATK exist before proceeding
6. **Continue**: Normal game room creation flow

### What Gets Created

When `add_user_id_only()` is called (from `user_profile_service/database_interface.py:489`):

**user_profiles table**:
```sql
INSERT INTO user_profiles (id, email, role, created_at, last_login)
VALUES (student_id, 'user_{id}@temp.com', 'student', timestamp, timestamp)
```

**student_profiles table**:
```sql
INSERT INTO student_profiles (id, language_level, points, money, hp, atk, items)
VALUES (student_id, 1, 0, 100, 100, 10, '[]')
```

**items table** (default sword):
```sql
INSERT INTO items (id, name, description, price, effect, type, level, max_level, created_at, owner_id, is_template)
VALUES ('sword_{id}', 'Basic Sword', 'A simple sword for beginners', 0, '+5 ATK', 'weapon', 1, 10, timestamp, student_id, 0)
```

## Benefits

✅ **Graceful Recovery**: Auto-fixes missing profiles instead of crashing
✅ **Better UX**: Users can play immediately after registration
✅ **Backwards Compatible**: Handles users created before profile creation logic
✅ **Consistent Stats**: All new players start with same baseline (HP=100, ATK=10)
✅ **Proper Logging**: Console logs when profile is auto-created for debugging

## Testing

### Scenario 1: Normal User (Profile Exists)
1. Login as `student1` (password: `password`)
2. Navigate to level 4 (gamePage2)
3. Game loads normally
4. No profile creation logs

### Scenario 2: Missing Profile (Auto-Created)
1. Create user in `auth_service` table without profile:
   ```sql
   INSERT INTO auth_service (user_id, username, password, role)
   VALUES ('test123', 'testuser', 'hashed_pass', 'student');
   ```
2. Login as `testuser`
3. Navigate to any game level
4. Check console logs: "User profile not found for test123, creating default profile..."
5. Game loads successfully with default stats
6. Verify profile created:
   ```sql
   SELECT * FROM user_profiles WHERE id = 'test123';
   SELECT * FROM student_profiles WHERE id = 'test123';
   ```

### Verification Queries

```sql
-- Check if user has profile
SELECT u.id, u.role, s.hp, s.atk
FROM user_profiles u
LEFT JOIN student_profiles s ON u.id = s.id
WHERE u.id = 'student_id';

-- Count users with missing profiles
SELECT COUNT(*) FROM auth_service a
WHERE NOT EXISTS (
    SELECT 1 FROM user_profiles u WHERE u.id = a.user_id
);
```

## Files Modified

- ✅ `game_service/gameroom/gameroom_service.py` (lines 17-34)
  - Added auto-create logic in `create_game_room()`

## No Changes Needed

- **Signup Flow**: Already calls `add_user_id_only()` correctly (signup_service.py:14)
- **Database Schema**: user_profiles and student_profiles tables correct
- **Frontend**: No changes needed, error was backend-only
- **User Service**: `add_user_id_only()` method already implemented correctly

## Notes

- This fix is defensive programming - it handles edge cases where profile creation failed
- The root cause (why profiles might be missing) could be:
  - Database transaction failures during signup
  - Manual user creation via SQL
  - Users created before `add_user_id_only()` logic was added
- Auto-creation only happens once per user (idempotent)
- Existing users with profiles are unaffected

## Related Issues

This fix also resolves similar 500 errors in:
- gamePage.js (levels 1-3)
- gamePage3.js (levels 7-10)

All three game difficulty ranges use the same `/game/newroom` endpoint.
