# Phase 2: Core Services Development - APPROVED ✅
**Status**: IN PROGRESS
**Approval Date**: 2025-11-28
**Duration**: Weeks 5-10 (6 weeks)
**Approved By**: Project Owner

---

## Objectives
Build the three core services: Node.js API, Python AI Worker, and React Frontend.

---

## Project Decisions

### Authentication
- ✅ Email/Password (bcrypt hashing)
- ✅ JWT with refresh token rotation
- ✅ **OAuth: Google ONLY** (GitHub excluded)
- ⏳ OAuth implementation: Phase 3
- ⏳ Email verification: Optional for Phase 2

### Payments
- ⏳ Stripe integration: Phase 3
- Focus on core processing first

### Rate Limiting
- ✅ Lenient for development (1000 req/min)
- Will tighten in production

### Admin Dashboard
- ⏳ Separate phase (after user-facing features)

---

## Implementation Sequence

### **Week 5-6: Node.js API Service** ✅ APPROVED

#### Structure
```
apps/api/
├── src/
│   ├── config/
│   │   ├── database.ts          # Prisma singleton
│   │   ├── redis.ts             # Redis with reconnection
│   │   ├── s3.ts                # MinIO/AWS S3 client
│   │   └── env.ts               # Zod validation
│   │
│   ├── middleware/
│   │   ├── auth.ts              # JWT verification
│   │   ├── rateLimit.ts         # Express rate limiter
│   │   ├── errorHandler.ts      # Global error handler
│   │   ├── logger.ts            # Winston logging
│   │   ├── validation.ts        # Zod schema validation
│   │   └── upload.ts            # Multer file upload
│   │
│   ├── routes/
│   │   ├── auth.routes.ts       # Register, login, refresh
│   │   ├── user.routes.ts       # Profile, credits
│   │   ├── image.routes.ts      # Upload, process, download
│   │   ├── subscription.routes.ts
│   │   └── health.routes.ts     # Health checks
│   │
│   ├── controllers/
│   │   ├── auth.controller.ts
│   │   ├── image.controller.ts
│   │   ├── user.controller.ts
│   │   └── subscription.controller.ts
│   │
│   ├── services/
│   │   ├── auth.service.ts      # bcrypt, JWT
│   │   ├── s3.service.ts        # Upload, presigned URLs
│   │   ├── queue.service.ts     # BullMQ jobs
│   │   ├── credit.service.ts    # Balance, deduction
│   │   └── email.service.ts     # SendGrid (optional)
│   │
│   ├── utils/
│   │   ├── crypto.ts
│   │   ├── jwt.ts
│   │   └── logger.ts
│   │
│   └── server.ts
│
├── tests/
├── Dockerfile
├── Dockerfile.prod
├── package.json
└── tsconfig.json
```

#### Features
- [x] User registration (email/password)
- [x] Login with JWT (access + refresh tokens)
- [x] Refresh token rotation
- [x] Password hashing (bcrypt, 12 rounds)
- [x] Multipart file upload (Multer)
- [x] S3/MinIO upload
- [x] Job queue creation (BullMQ)
- [x] Credit system (check, deduct, log)
- [x] Health endpoints (/health, /ready)
- [x] Structured logging (JSON)

#### Dependencies
- express, @prisma/client, bcrypt, jsonwebtoken
- bullmq, ioredis
- multer, @aws-sdk/client-s3
- zod, winston
- jest, supertest (testing)

---

### **Week 7-8: Python AI Worker Service** ✅ APPROVED

#### Structure
```
apps/worker/
├── app/
│   ├── core/
│   │   ├── config.py            # Pydantic settings
│   │   ├── database.py          # Async SQLAlchemy
│   │   ├── redis.py
│   │   └── s3.py                # Boto3
│   │
│   ├── services/
│   │   ├── background_removal.py # rembg integration
│   │   ├── image_optimization.py # Pillow processing
│   │   ├── artifact_removal.py   # From desktop app
│   │   ├── background_editor.py  # Solid/gradient/texture
│   │   └── s3_service.py
│   │
│   ├── tasks/
│   │   ├── celery_app.py
│   │   └── process_image.py     # Main task
│   │
│   ├── api/
│   │   └── health.py            # FastAPI health
│   │
│   └── main.py
│
├── models/
│   ├── birefnet-portrait.onnx
│   └── u2net.onnx
│
├── tests/
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

#### Features
- [x] BiRefNet-portrait model loading
- [x] rembg background removal
- [x] Hair strand preservation
- [x] Edge refinement (from desktop app)
- [x] Artifact removal logic (from `bg_remove_v1_2_bulletproof.py`)
- [x] Gamma correction
- [x] File size optimization
- [x] Background customization:
  - Solid colors (hex input)
  - Gradients (2-3 colors, 0-360° angle)
  - Textures (wood, fabric, concrete, etc.)
- [x] Multi-resolution output (small, HD, ultra-HD)
- [x] Celery async processing
- [x] S3 upload/download
- [x] Database status updates
- [x] Error handling with retries (3 attempts)

#### Dependencies
- fastapi, celery, redis
- rembg>=2.0.60, onnxruntime==1.17.0
- Pillow>=10.0.0, opencv-contrib-python
- boto3 (S3), asyncpg (database)
- pytest

---

### **Week 9-10: React Frontend** ✅ APPROVED

#### Structure
```
apps/web/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   │
│   │   ├── upload/
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── UploadProgress.tsx
│   │   │   └── ImagePreview.tsx
│   │   │
│   │   ├── editor/
│   │   │   ├── ImageEditor.tsx
│   │   │   ├── BackgroundSelector.tsx
│   │   │   ├── ColorPicker.tsx
│   │   │   ├── GradientEditor.tsx
│   │   │   ├── TextureGallery.tsx
│   │   │   └── PreviewPanel.tsx
│   │   │
│   │   ├── dashboard/
│   │   │   ├── CreditBalance.tsx
│   │   │   └── UsageHistory.tsx
│   │   │
│   │   └── common/
│   │       ├── Header.tsx
│   │       ├── Footer.tsx
│   │       └── Button.tsx
│   │
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── EditorPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── PricingPage.tsx
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useImageUpload.ts
│   │   ├── useImageProcessing.ts
│   │   └── useCredits.ts
│   │
│   ├── store/
│   │   ├── authStore.ts         # Zustand
│   │   ├── imageStore.ts
│   │   └── userStore.ts
│   │
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.service.ts
│   │   ├── image.service.ts
│   │   └── user.service.ts
│   │
│   └── App.tsx
│
├── public/
├── Dockerfile
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

#### Features
- [x] User registration/login UI
- [x] Drag & drop image upload
- [x] Processing status polling
- [x] Background customization UI:
  - Color picker (solid colors)
  - Gradient editor (2-3 colors, angle slider)
  - Texture gallery
- [x] Download buttons (small, HD, ultra-HD)
- [x] Credit balance display
- [x] Usage history
- [x] Responsive design (mobile/tablet/desktop)

#### Design Reuse
- ✅ Landing page from `docs/index.html`
- ✅ Pricing table (updated prices: $2 less)
- ✅ Same color scheme (#ff6b35 primary)
- ✅ Mobile viewport improvements from branch

#### Dependencies
- react, react-router-dom
- vite, typescript
- tailwind, @headlessui/react
- zustand, @tanstack/react-query
- axios
- vitest (testing)

---

## Definition of Done (Phase 2)

### Functional Requirements
- [ ] Users can register and login
- [ ] Users can upload images (max 25MB)
- [ ] Images are processed with background removal
- [ ] Users can customize backgrounds (solid, gradient, texture)
- [ ] Users can download small version (free tier)
- [ ] Users can see credit balance
- [ ] Processing completes in < 10 seconds
- [ ] All services run in Docker

### Technical Requirements
- [ ] API has 15+ documented endpoints
- [ ] Worker processes images asynchronously
- [ ] Database has 1000+ seeded test records
- [ ] Redis queue handles 100+ concurrent jobs
- [ ] S3 stores original + processed images
- [ ] Logging captures all errors
- [ ] Health checks for all services
- [ ] 75%+ test coverage

### Documentation
- [ ] API documentation (Swagger)
- [ ] Postman collection
- [ ] Frontend component docs
- [ ] Updated deployment guide

---

## Deliverables by Week

### Week 5-6: API Service
- ✅ Authentication system
- ✅ Image upload endpoint
- ✅ S3 integration
- ✅ Job queue creation
- ✅ Credit system API
- ✅ Health checks
- ✅ 70%+ test coverage
- ✅ Postman collection

### Week 7-8: Worker Service
- ✅ Background removal
- ✅ Background customization
- ✅ Multi-resolution output
- ✅ S3 upload
- ✅ Database updates
- ✅ 80%+ test coverage
- ✅ Processing < 10s

### Week 9-10: Frontend
- ✅ Registration/login
- ✅ Image upload
- ✅ Background editor
- ✅ Download functionality
- ✅ Credit balance
- ✅ Responsive design
- ✅ Production build

---

## Technology Stack

### API Service
- Express.js (Node.js 20)
- Prisma ORM
- BullMQ (job queue)
- Zod (validation)
- Winston (logging)
- Jest (testing)

### Worker Service
- FastAPI (Python 3.11)
- Celery (task queue)
- rembg 2.0.60
- ONNX Runtime 1.17.0
- Pillow, OpenCV
- pytest (testing)

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS
- Zustand (state)
- TanStack Query (server state)
- Vitest (testing)

---

## Timeline

**Start Date**: Week 5 (after Phase 1 completion)
**End Date**: Week 10
**Duration**: 6 weeks
**Status**: ✅ APPROVED - Ready to implement

---

## Next Phase
→ **Phase 3: Payment Integration & Advanced Features (Weeks 11-16)**

---

**Signed off**: 2025-11-28
**Phase Status**: 🚧 IN PROGRESS
**Last Updated**: 2025-11-28
