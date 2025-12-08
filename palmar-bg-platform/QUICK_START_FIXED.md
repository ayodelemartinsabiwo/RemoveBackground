# QUICK START GUIDE - Palmar Background Remover

## 🚀 Starting the Application (Development Mode)

### Option 1: Run Services Locally (Recommended for Development)

**Step 1: Start Docker Services Only**
```powershell
cd C:\RemoveBackground\palmar-bg-platform
docker-compose -f docker-compose.dev.yml up -d postgres redis minio minio-setup
```

**Step 2: Start API Server (Terminal 1)**
```powershell
cd C:\RemoveBackground\palmar-bg-platform\apps\api
npm run dev
```

**Step 3: Start Web Frontend (Terminal 2)**
```powershell
cd C:\RemoveBackground\palmar-bg-platform\apps\web
npm run dev
```

**Step 4: Open Application**
```
http://localhost:5173
```

### Option 2: Run Everything in Docker

```powershell
cd C:\RemoveBackground\palmar-bg-platform
docker-compose -f docker-compose.dev.yml up -d
```

Then wait ~30 seconds for all services to start.

---

## ✅ Key Fixes Applied

### 1. **Authentication Protection**
- ✅ Added `ProtectedRoute` component
- ✅ Dashboard and Editor now require login
- ✅ Automatic redirect to `/login` if not authenticated

### 2. **Route Configuration**
- ✅ Public routes: `/`, `/login`, `/register`, `/pricing`
- ✅ Protected routes: `/dashboard`, `/editor`
- ✅ No more "Login failed" errors on dashboard load

### 3. **API Authentication Flow**
```
User visits /dashboard → Not logged in → Redirect to /login
User logs in → JWT token stored → Access dashboard → API calls with Bearer token
```

---

## 🧪 Testing the Fixed Application

### Test 1: Visit Dashboard Without Login
1. Clear browser localStorage (F12 → Application → Local Storage → Clear)
2. Go to http://localhost:5173/dashboard
3. **Expected:** Immediately redirected to /login
4. **No errors in console**

### Test 2: Register New User
1. Go to http://localhost:5173/register
2. Fill in:
   - Email: test@example.com
   - Password: Test123!@#
   - Name: Test User
3. Click Register
4. **Expected:**
   - Success message
   - Redirect to /dashboard
   - Dashboard loads with data
   - No "Failed to load dashboard data" error

### Test 3: Login Existing User
1. Go to http://localhost:5173/login
2. Enter credentials
3. Click Login
4. **Expected:**
   - JWT token stored in localStorage
   - Redirect to /dashboard
   - API calls include `Authorization: Bearer <token>`
   - Dashboard data loads successfully

### Test 4: Image Upload
1. Login first
2. Go to /editor or click "Upload Image"
3. Select an image
4. **Expected:**
   - Upload succeeds (has auth token)
   - Processing starts
   - Background removed
   - Download available

---

## 🔍 How to Verify Fixes

### Check Browser Console (F12)
**Before fixes:**
```
❌ Failed to load dashboard data
❌ Login failed
❌ GET /api/v1/users/credits 401 (Unauthorized)
❌ No authorization token provided
```

**After fixes:**
```
✅ 🔧 API Client initialized: { baseURL: 'http://localhost:3001/api/v1', ... }
✅ POST /api/v1/auth/login 200 OK
✅ GET /api/v1/users/credits 200 OK (with Bearer token)
```

### Check localStorage
Open DevTools (F12) → Application → Local Storage → `http://localhost:5173`

**Should see:**
```json
{
  "auth-storage": {
    "state": {
      "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "isAuthenticated": true,
      "user": {
        "id": "...",
        "email": "test@example.com",
        "name": "Test User"
      }
    }
  }
}
```

### Check API Server Logs
**Before login:**
```
GET /api/v1/users/credits 401 - No authorization token provided
```

**After login:**
```
POST /api/v1/auth/login 200 - User authenticated
GET /api/v1/users/credits 200 - Credits retrieved
```

---

## 🛑 Common Issues & Solutions

### Issue: "Failed to load dashboard data"
**Cause:** Trying to access dashboard without logging in
**Solution:** ✅ FIXED - Now redirects to /login automatically

### Issue: "Login failed"
**Cause:** API not running or wrong credentials
**Solution:**
1. Check API is running: `curl http://localhost:3001/health`
2. Check database has users table
3. Try registering a new user first

### Issue: "No authorization token provided"
**Cause:** Token not being sent with requests
**Solution:** ✅ FIXED - API client now includes token in Authorization header

### Issue: Image shows original after processing
**Cause:** Worker not processing or wrong image being displayed
**Solution:**
1. Check worker is running: `docker ps | Select-String worker`
2. Check Redis: `docker-compose -f docker-compose.dev.yml logs redis`
3. Check MinIO bucket exists: http://localhost:9001

---

## 📊 Service Status Check

```powershell
# Run health check
cd C:\RemoveBackground\palmar-bg-platform
.\scripts\health-check.ps1
```

**Expected output:**
```
✅ PostgreSQL: Connected
✅ Redis: Connected
✅ MinIO: Connected
✅ API Server: Responding
✅ Web Frontend: Responding
```

---

## 🎯 What Changed

| File | Change |
|------|--------|
| `apps/web/src/App.tsx` | Added ProtectedRoute wrapper for /dashboard and /editor |
| `apps/web/src/components/common/ProtectedRoute.tsx` | NEW - Checks authentication before rendering |
| No more Firebase errors | Already removed in previous fix |
| API token handling | Already fixed - Bearer token in headers |

---

## 📝 Next Steps

1. **Start services** using Option 1 above
2. **Clear browser cache** (F12 → Application → Clear storage)
3. **Register a new user** at `/register`
4. **Upload an image** at `/editor`
5. **Check dashboard** for processed images

All authentication errors should now be resolved! 🎉
