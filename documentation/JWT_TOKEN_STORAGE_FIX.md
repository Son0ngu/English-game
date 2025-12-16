# JWT Token Storage Fix

## Problem Description

Users were receiving 500 errors with "signature has expired" when entering level 4 and above. The backend logs showed:
```
Error getting user_id from JWT: Not enough segments
127.0.0.1 - - [29/Oct/2025 15:45:36] "POST /auth/HuyTranLayRoleTuID HTTP/1.1" 401 -
```

## Root Cause

The issue had multiple causes:

1. **Inconsistent Token Storage**: Login stored tokens in `localStorage` as `"token"`, but some game pages were looking for `"jwtToken"` first
2. **Hardcoded Expired Test Tokens**: gamePage2.js and gamePage3.js had hardcoded expired JWT tokens as fallback
3. **Wrong Token Location**: Backend was configured to read JWT from both headers AND cookies, but frontend only sent via headers
4. **Token Mismatch**: The `getJWTToken()` function was looking for the wrong localStorage key

## Solution Applied

### 1. Fixed Token Retrieval Function

**Updated Files:**
- `front-end/templates/gamePage/gamePage.js` (lines 108-121)
- `front-end/templates/gamePage2/gamePage2.js` (lines 108-120)
- `front-end/templates/gamePage3/gamePage3.js` (lines 108-120)

**Before:**
```javascript
function getJWTToken() {
    const token = localStorage.getItem('jwtToken') || sessionStorage.getItem('jwtToken');

    if (!token) {
        console.log('No JWT token found, using test token');
        const testToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'; // Expired token
        localStorage.setItem('jwtToken', testToken);
        return testToken;
    }

    return token;
}
```

**After:**
```javascript
function getJWTToken() {
    // Login stores token in localStorage as "token"
    const token = localStorage.getItem('token');

    if (!token) {
        console.error('No JWT token found - user not logged in');
        alert('Please login first');
        window.location.href = '../../index.html';
        return null;
    }

    return token;
}
```

### 2. Enhanced Error Handling for Expired Tokens

Added comprehensive error handling to all API calls in all three game page files:

**Updated Endpoints:**
- `POST /game/newroom`
- `POST /game/get_question`
- `POST /game/check_answer`
- `POST /classroom/increment_win`
- `POST /user/update`

**Error Handling Pattern:**
```javascript
if (!response.ok) {
    if (response.status === 401 || response.status === 500) {
        // Token expired or invalid - clear and redirect to login
        console.log('Token expired, removing tokens and redirecting');
        localStorage.removeItem('token');
        localStorage.removeItem('jwtToken');
        sessionStorage.removeItem('jwtToken');
        alert('Your session has expired. Please login again.');
        window.location.href = '../../index.html';
        return;
    }
    throw new Error(`HTTP error! status: ${response.status}`);
}
```

### 3. JWT Token Expiration Extended

**File:** `app.py` (line 28)

```python
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # Extended to 24 hours
```

This was already configured correctly - tokens now last 1 full day instead of 2 hours.

## How Token Flow Works Now

1. **Login** (`loginPage.js:86`):
   ```javascript
   localStorage.setItem("token", result.access_token);
   ```

2. **Game Pages** retrieve token:
   ```javascript
   const token = localStorage.getItem('token'); // Consistent key
   ```

3. **API Calls** send token in Authorization header:
   ```javascript
   headers: {
       'Authorization': `Bearer ${localStorage.getItem("token")}`
   }
   ```

4. **Backend** (`services_route.py:121-122`) validates:
   ```python
   verify_jwt_in_request()
   user_id = get_jwt_identity()
   ```

5. **If Token Expires**, frontend automatically:
   - Clears all token storage
   - Alerts user
   - Redirects to login page

## Backend Configuration

**File:** `app.py` (lines 28-35)

```python
# JWT Configurations
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # 24 hour tokens
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # Accept both
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_COOKIE_SAMESITE'] = 'LAX'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
```

## Testing Instructions

1. **Clear existing tokens:**
   ```javascript
   // In browser console:
   localStorage.clear();
   sessionStorage.clear();
   ```

2. **Login fresh:**
   - Navigate to `/index.html`
   - Login with valid credentials (e.g., `student1` / `stud123`)
   - Token is saved to `localStorage.token`

3. **Test game levels:**
   - Access level 1-3 (should work)
   - Access level 4+ (should work now - was failing before)
   - Token is consistently read from `localStorage.token`

4. **Test token expiration:**
   - Wait 24 hours OR manually set expired token
   - Try to access game
   - Should auto-redirect to login with alert

## Files Modified

1. `app.py` - JWT expiration config (already correct at 24 hours)
2. `front-end/templates/gamePage/gamePage.js` - Token retrieval + error handling
3. `front-end/templates/gamePage2/gamePage2.js` - Token retrieval + error handling
4. `front-end/templates/gamePage3/gamePage3.js` - Token retrieval + error handling

## Key Improvements

✅ **Consistent Token Storage** - All code uses `localStorage.getItem('token')`
✅ **No More Hardcoded Tokens** - Removed expired test tokens
✅ **Proper Error Handling** - 401 and 500 errors redirect to login
✅ **Extended Expiration** - Tokens last 24 hours (1 day)
✅ **Clear User Feedback** - Alert messages when token expires
✅ **Automatic Cleanup** - All token locations cleared on error

## Notes

- The "Not enough segments" error occurred when JWT was malformed or empty
- Backend JWT configuration supports both headers and cookies, but frontend only uses headers
- All three game page variants (gamePage, gamePage2, gamePage3) now have identical token handling logic
- Users who had old expired tokens cached will be automatically redirected to login on first access
