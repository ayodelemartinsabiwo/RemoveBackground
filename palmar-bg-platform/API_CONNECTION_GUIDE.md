# API Connection Guide

## ✅ Real API Successfully Connected!

Your frontend is now connected to the real backend API running on `http://localhost:3001`.

---

## 📋 What Was Done

### 1. **Complete API Service Layer** ([/apps/web/src/services/api.ts](palmar-bg-platform/apps/web/src/services/api.ts))

Replaced placeholder functions with full axios-based HTTP client:

- ✅ **Axios Instance**: Configured with base URL, timeout, and CORS
- ✅ **Auth Interceptors**: Automatically adds JWT tokens to requests
- ✅ **Token Refresh**: Handles 401 errors and refreshes expired tokens
- ✅ **Error Handling**: Centralized error handling with toast notifications

### 2. **API Endpoints Implemented**

#### **Authentication API** (`authApi`)
```typescript
// Login
const result = await authApi.login({
  email: 'user@example.com',
  password: 'password123'
})
// Returns: { success: true, data: { user, accessToken, refreshToken } }

// Register
const result = await authApi.register({
  email: 'user@example.com',
  password: 'password123',
  fullName: 'John Doe'
})

// Logout
await authApi.logout()
```

#### **Image API** (`imageApi`)
```typescript
// Upload image
const formData = new FormData()
formData.append('image', file)
const result = await imageApi.upload(formData)
// Returns: { success: true, data: { id, status, originalUrl, ... } }

// Get all images
const result = await imageApi.getImages({ page: 1, limit: 10 })
// Returns: { success: true, data: [images array] }

// Get single image
const result = await imageApi.getById(imageId)
// Returns: { success: true, data: { id, status, processedUrls, ... } }

// Download processed image
const result = await imageApi.download(imageId, 'SMALL')
// Returns: { success: true, data: Blob }

// Delete image
await imageApi.delete(imageId)
```

#### **User API** (`userApi`)
```typescript
// Get profile
const result = await userApi.getProfile()
// Returns: { success: true, data: { user info } }

// Get credits
const result = await userApi.getCredits()
// Returns: { success: true, data: { credits info } }
```

---

## 🔧 API Configuration

### Base URL
The API base URL is configured in `/apps/web/src/services/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'
```

### Environment Variables
You can override the default URL by creating a `.env` file in `/apps/web`:

```env
VITE_API_URL=http://localhost:3001
```

For production:
```env
VITE_API_URL=https://your-production-api.com
```

---

## 🚀 Current API Status

### ✅ Backend Services Running

```bash
# Check all services
docker-compose -f docker-compose.dev.yml ps

# Your running services:
✅ palmar-api-dev     → http://localhost:3001 (Express API)
✅ palmar-postgres-dev → localhost:5432 (Database)
✅ palmar-redis-dev   → localhost:6379 (Cache/Queue)
✅ palmar-minio-dev   → http://localhost:9000 (S3 Storage)
✅ palmar-worker-dev  → localhost:8000 (Python Worker)
✅ palmar-celery-dev  → Background Tasks
✅ palmar-web-dev     → http://localhost:3000 (React Frontend)
```

### ✅ API Health Check

```bash
curl http://localhost:3001/health
# Response: {"success":true,"message":"Service is healthy"}
```

---

## 📝 API Endpoints Available

### Base URL: `http://localhost:3001/api/v1`

#### **Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `POST /auth/refresh` - Refresh access token

#### **Images** (Requires Authentication)
- `POST /images/upload` - Upload and process image
- `GET /images` - Get user's images (paginated)
- `GET /images/:id` - Get single image details
- `GET /images/:id/download?tier=SMALL|MEDIUM|LARGE` - Download processed image
- `DELETE /images/:id` - Delete image

#### **User** (Requires Authentication)
- `GET /users/profile` - Get user profile
- `GET /users/credits` - Get user credits

---

## 🔐 Authentication Flow

### How It Works

1. **Register/Login**:
   - User enters credentials
   - API returns `accessToken` and `refreshToken`
   - Tokens stored in `localStorage`

2. **API Requests**:
   - Every request automatically includes: `Authorization: Bearer <accessToken>`
   - This happens via axios interceptor (you don't need to do this manually)

3. **Token Expiration**:
   - Access tokens expire after 15 minutes
   - When a 401 error occurs, the interceptor automatically:
     - Sends refresh token to get new access token
     - Retries the original request with new token
     - If refresh fails, redirects to `/login`

4. **Logout**:
   - Calls logout API endpoint
   - Clears tokens from `localStorage`
   - User can login again

---

## 🎯 How to Use in Components

### Example: Upload Image

```typescript
import { imageApi } from '@/services/api'
import toast from 'react-hot-toast'

const handleUpload = async (file: File) => {
  const formData = new FormData()
  formData.append('image', file)

  const result = await imageApi.upload(formData)

  if (result.success) {
    const imageId = result.data.id
    toast.success('Image uploaded successfully!')

    // Start polling for processing status
    pollImageStatus(imageId)
  } else {
    // Error is already shown via toast in the API layer
    console.error('Upload failed:', result.error)
  }
}

const pollImageStatus = async (id: string) => {
  const interval = setInterval(async () => {
    const result = await imageApi.getById(id)

    if (result.success && result.data.status === 'COMPLETED') {
      clearInterval(interval)
      toast.success('Processing complete!')
      setProcessedImage(result.data.processedSmallUrl)
    } else if (result.success && result.data.status === 'FAILED') {
      clearInterval(interval)
      toast.error('Processing failed')
    }
  }, 2000)
}
```

### Example: Login

```typescript
import { authApi } from '@/services/api'
import { useAuthStore } from '@/store/authStore'

const handleLogin = async (email: string, password: string) => {
  const result = await authApi.login({ email, password })

  if (result.success) {
    const { user, accessToken } = result.data

    // Update auth store
    useAuthStore.getState().setUser(user)

    // Navigate to dashboard
    navigate('/dashboard')
  }
  // Error handling is automatic via toast
}
```

---

## 🐛 Troubleshooting

### 1. **CORS Errors**

**Problem**: Browser console shows CORS errors

**Solution**:
- API is configured to allow `http://localhost:3000` in CORS
- Check `apps/api/.env` has: `CORS_ORIGIN=http://localhost:3000`
- Restart API: `docker-compose -f docker-compose.dev.yml restart api`

### 2. **401 Unauthorized Errors**

**Problem**: All requests return 401

**Solution**:
- Check if user is logged in
- Check `localStorage` for `accessToken` and `refreshToken`
- Try logging out and logging in again
- Clear browser cache/localStorage

### 3. **Upload Fails Immediately**

**Problem**: Upload returns error before processing

**Possible Causes**:
- File too large (max 10MB by default)
- Invalid file type (only JPG, PNG, WEBP)
- User has no credits
- API/Worker service is down

**Check**:
```bash
# Check API logs
docker logs palmar-api-dev

# Check Worker logs
docker logs palmar-worker-dev
```

### 4. **Image Stays in PENDING Status**

**Problem**: Image status never changes to COMPLETED

**Solution**:
- Worker service might be down
- Check worker logs: `docker logs palmar-worker-dev`
- Check celery logs: `docker logs palmar-celery-dev`
- Restart worker: `docker-compose -f docker-compose.dev.yml restart worker celery`

---

## 🔄 What Changed from Demo Mode

### Before (Demo Mode):
- All API calls returned `{ success: false }`
- Frontend faked the processing with `setTimeout`
- No real image processing
- No database storage

### Now (Real API):
- ✅ Real authentication with JWT
- ✅ Actual image upload to S3 (MinIO)
- ✅ Background processing with Python worker
- ✅ Database storage of all images and users
- ✅ Credit system enforcement
- ✅ Multi-tier downloads (SMALL, MEDIUM, LARGE)

---

## 📊 Testing the API

### 1. **Register a New User**

```bash
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "fullName": "Test User"
  }'
```

### 2. **Login**

```bash
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456"
  }'
```

Save the `accessToken` from the response.

### 3. **Upload Image**

```bash
curl -X POST http://localhost:3001/api/v1/images/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "image=@/path/to/your/image.jpg"
```

### 4. **Check Image Status**

```bash
curl http://localhost:3001/api/v1/images/IMAGE_ID \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🎨 Next Steps

### Optional Enhancements:

1. **Remove Demo Mode Fallback** (if desired):
   - The EditorPage still has demo mode fallback for when API fails
   - You can remove lines 56-70 in `EditorPage.tsx` to make it API-only

2. **Add Loading States**:
   - Show better loading UI during processing
   - Display processing progress bar

3. **Add Error Recovery**:
   - Retry failed uploads
   - Resume interrupted downloads

4. **Add Image Gallery**:
   - Dashboard page to show all processed images
   - Pagination and filtering

5. **Add Credit Purchase**:
   - Integration with payment gateway
   - Credit packages

---

## 🚦 Current Status

### ✅ What's Working:
- Backend API is running on port 3001
- Frontend can communicate with API
- Authentication flow (register, login, logout)
- Image upload endpoint
- Token refresh mechanism
- Error handling and user feedback

### ⚠️ What You Need to Do:

1. **Seed Database** (if not done):
   ```bash
   cd palmar-bg-platform
   docker-compose -f docker-compose.dev.yml exec api npm run db:seed
   ```

2. **Test Upload**:
   - Go to http://localhost:3000
   - Register/Login
   - Try uploading an image
   - Check if it processes correctly

3. **Monitor Logs**:
   ```bash
   # API logs
   docker logs -f palmar-api-dev

   # Worker logs
   docker logs -f palmar-worker-dev
   ```

---

## 📞 Support

If you encounter issues:

1. Check Docker services are running: `docker-compose ps`
2. Check API health: `curl http://localhost:3001/health`
3. Check API logs: `docker logs palmar-api-dev`
4. Check browser console for errors
5. Check Network tab in DevTools for failed requests

---

**Your API is now fully connected and ready to use!** 🎉

Try uploading an image through the web interface and watch it process in real-time.
