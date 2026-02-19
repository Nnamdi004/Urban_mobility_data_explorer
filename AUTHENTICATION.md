# Authentication System

## Current Implementation: Mock Authentication

This project uses **mock authentication** for demonstration purposes. This allows the full user experience flow to be demonstrated without the complexity of a production authentication system.

## How It Works

### Frontend (Mock Auth)
- Users can "login" with any valid email format and password (6+ characters)
- Demo credentials: `demo@urbanmobility.com` / `demo1234`
- Tokens are generated client-side (timestamp-based)
- Full auth UI flow: login, signup, password reset, verification

### Backend (Data API)
- No authentication required for data endpoints
- Focus on data processing and analytics
- All routes are publicly accessible for demonstration

## Demo Credentials

```
Email: demo@urbanmobility.com
Password: demo1234
```

Or use any email format with a password of 6+ characters.

## Features Demonstrated

✅ Login flow with validation
✅ Signup with password strength indicator
✅ Password reset flow
✅ Email verification simulation
✅ Session management (localStorage/sessionStorage)
✅ Protected routes (dashboard requires "login")
✅ Logout functionality

## Security Note

⚠️ **This is NOT production-ready authentication**

Mock authentication provides:
- ✅ User experience demonstration
- ✅ UI/UX flow validation
- ✅ Frontend state management
- ❌ NO actual security
- ❌ NO password verification
- ❌ NO user database

## Production Deployment

For production use, this would be replaced with:

### Recommended: JWT Authentication
```
- User table in database
- Password hashing (bcrypt)
- JWT token generation
- Token validation middleware
- Refresh token mechanism
- Rate limiting
- HTTPS only
```

### Implementation Steps (Future)
1. Add `users` table to database
2. Install `Flask-JWT-Extended`
3. Implement password hashing with `bcrypt`
4. Create auth routes (`/api/auth/login`, `/api/auth/signup`)
5. Add JWT middleware to protect routes
6. Update frontend to use real auth endpoints

## Why Mock Auth for This Project?

This is an **academic project** focused on:
- ✅ Data cleaning and processing
- ✅ Database design and optimization
- ✅ Custom algorithms (Top-K, anomaly detection)
- ✅ Data visualization and analytics
- ✅ Full-stack integration

Authentication is demonstrated but not the core focus. The mock implementation allows us to:
- Show complete user flows
- Focus development time on data analytics
- Demonstrate frontend-backend integration
- Avoid scope creep on a non-core feature

## Switching to Real Auth

To enable real authentication:
1. Set `useMock: false` in `frontend/js/utils/api.js`
2. Implement backend auth routes
3. Add user database table
4. Configure JWT secret in `.env`

## Current Configuration

```javascript
// frontend/js/utils/api.js
const API = {
    baseURL: 'http://localhost:5000/api',
    useMock: true  // ← Mock auth enabled
}
```

## Testing

**Login:**
- Any email format + password (6+ chars)
- Or use: `demo@urbanmobility.com` / `demo1234`

**Signup:**
- Fill form with any valid data
- Password must be 8+ characters
- Redirects to verification page

**Dashboard Access:**
- Must be "logged in" (have token in storage)
- Logout clears tokens and redirects to login

---

**Note:** This documentation should be included in your project report to explain the authentication approach and design decisions.
