# JWT Token Expiration Fix

## Bug Description

**Issue**: `/game/newroom` endpoint returned 500 Internal Server Error with message "signature has expired" when JWT token expired.

**Error Behavior**:
- User logs in successfully
- After 2 hours, JWT token expires
- User tries to play game
- Backend throws unhandled JWT expiration exception
- Returns 500 instead of proper 401 Unauthorized
- Frontend error handler doesn't trigger (expects 401, not 500)
- User sees generic "Failed to Load Game" error

## Root Cause

Flask-JWT-Extended raises exceptions when tokens are expired, invalid, or missing. Without proper error handlers, these exceptions bubble up as 500 Internal Server Errors instead of returning proper 401 Unauthorized responses.

**Missing Error Handlers**:
1. `@jwt.expired_token_loader` - handles expired tokens
2. `@jwt.invalid_token_loader` - handles invalid signatures
3. `@jwt.unauthorized_loader` - handles missing tokens
4. `@jwt.revoked_token_loader` - handles revoked tokens

**Frontend Handling**:
The frontend already had logic to handle 401 errors:
```javascript
if (response.status === 401) {
    console.log('Unauthorized, removing tokens and redirecting');
    localStorage.removeItem('jwtToken');
    sessionStorage.removeItem('jwtToken');
    window.location.href = '/login';
    return;
}
```

But this code never ran because backend returned 500, not 401.

## The Fix

### Backend Changes

**File**: `app.py` (lines 1, 28-65)

#### 1. Extended Token Expiration Time

Changed from 2 hours to 24 hours:
```python
# BEFORE
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)

# AFTER
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
```

#### 2. Added JWT Error Handlers

```python
from flask import Flask, jsonify  # Added jsonify import
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

# JWT Error Handlers - Return 401 instead of 500
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'token_expired',
        'message': 'The token has expired. Please login again.'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'message': 'Signature verification failed. Please login again.'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        'message': 'Request does not contain a valid token.'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'token_revoked',
        'message': 'The token has been revoked. Please login again.'
    }), 401
```

### How It Works

**Before Fix**:
1. User's token expires
2. User makes request to `/game/newroom`
3. `@jwt_required` decorator checks token → raises `ExpiredSignatureError`
4. Exception not caught → returns 500
5. Frontend sees 500 → shows generic error
6. User stuck, must manually clear localStorage

**After Fix**:
1. User's token expires
2. User makes request to `/game/newroom`
3. `@jwt_required` decorator checks token → raises `ExpiredSignatureError`
4. `@jwt.expired_token_loader` catches it → returns 401 with message
5. Frontend sees 401 → auto-clears tokens and redirects to login
6. User can login again seamlessly

### Error Response Format

All JWT errors now return consistent JSON:
```json
{
    "error": "token_expired",
    "message": "The token has expired. Please login again."
}
```

Error types:
- `token_expired` - Token is valid but past expiration time
- `invalid_token` - Token signature verification failed (wrong secret, corrupted)
- `authorization_required` - No token provided in request
- `token_revoked` - Token has been revoked (if using token revocation)

## Benefits

✅ **Proper HTTP Status Codes**: Returns 401 instead of 500 for auth errors
✅ **Frontend Auto-Handles**: Existing 401 handler triggers automatically
✅ **Better UX**: User redirected to login instead of seeing error screen
✅ **Longer Sessions**: 24-hour tokens reduce login frequency
✅ **Clear Error Messages**: JSON responses explain what went wrong
✅ **Security**: Invalid/tampered tokens properly rejected

## Testing

### Test 1: Normal Login (Token Valid)
1. Login as `student1` / `password`
2. Navigate to any game level
3. Game loads successfully
4. Token valid for 24 hours

### Test 2: Expired Token (Simulated)
1. Get a JWT token
2. Wait 24 hours OR manually decode and change `exp` field
3. Try to access `/game/newroom`
4. **Expected**: 401 response with `"error": "token_expired"`
5. Frontend auto-redirects to login page

### Test 3: Invalid Token
1. Manually modify JWT token in localStorage (corrupt signature)
2. Try to access any protected endpoint
3. **Expected**: 401 response with `"error": "invalid_token"`
4. Frontend auto-redirects to login page

### Test 4: Missing Token
1. Clear localStorage
2. Try to access `/game/newroom` directly
3. **Expected**: 401 response with `"error": "authorization_required"`
4. Frontend auto-redirects to login page

### Manual Testing Commands

```bash
# Test with expired token (after 24 hours)
curl -X POST http://127.0.0.1:13371/game/newroom \
  -H "Authorization: Bearer YOUR_EXPIRED_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "easy", "class_id": "class1"}'

# Expected response:
# HTTP/1.1 401 UNAUTHORIZED
# {
#   "error": "token_expired",
#   "message": "The token has expired. Please login again."
# }
```

## Files Modified

- ✅ `app.py` (lines 1, 28-65)
  - Added `jsonify` import
  - Extended token expiration to 24 hours
  - Added 4 JWT error handler decorators

## No Frontend Changes Needed

The frontend already has proper 401 error handling in all gamePage files:
- `front-end/templates/gamePage/gamePage.js` (lines 394-400)
- `front-end/templates/gamePage2/gamePage2.js` (lines 394-400)
- `front-end/templates/gamePage3/gamePage3.js` (lines 394-400)

## Deployment Notes

**IMPORTANT**: After applying this fix, **restart the Flask application**:

```bash
# Stop the current Flask process (Ctrl+C if running in terminal)
# Or kill the process:
pkill -f "python app.py"

# Start Flask again
python app.py
```

**Token Invalidation**: Existing tokens issued before the change will still have 2-hour expiration. Users need to login again to get new 24-hour tokens.

## Additional Improvements (Optional)

### Token Refresh Implementation

For even better UX, consider implementing token refresh:

```python
from flask_jwt_extended import create_refresh_token, jwt_required, get_jwt_identity

@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200
```

Then frontend can automatically refresh tokens before they expire.

### Frontend Token Refresh Logic

```javascript
// Check token expiration before requests
function isTokenExpiringSoon() {
    const token = getJWTToken();
    if (!token) return false;

    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp * 1000; // Convert to milliseconds
    const now = Date.now();
    const fiveMinutes = 5 * 60 * 1000;

    return (exp - now) < fiveMinutes;
}

async function refreshTokenIfNeeded() {
    if (isTokenExpiringSoon()) {
        const response = await fetch('/auth/refresh', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getRefreshToken()}`
            }
        });
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
    }
}
```

## Notes

- JWT tokens are stateless - cannot be revoked without additional infrastructure (Redis, database)
- 24 hours is a reasonable balance between UX and security for a learning application
- For production, consider implementing refresh tokens for longer sessions
- Monitor token expiration times and adjust based on user behavior
- Consider adding "Remember Me" option for longer token validity (7 days)

## Related Issues

This fix resolves:
- ✅ "signature has expired" 500 errors
- ✅ Generic "Failed to Load Game" errors from expired tokens
- ✅ Users unable to play after 2 hours without manual token clearing
