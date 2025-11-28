# Palmar Background Remover - Enterprise Web Platform

**Production-ready, scalable web-based background removal platform with AI processing**

![License](https://img.shields.io/badge/license-PROPRIETARY-red)
![Node](https://img.shields.io/badge/node-%3E%3D20.0.0-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![TypeScript](https://img.shields.io/badge/typescript-5.3%2B-blue)

---

## 🏗️ Architecture Overview

This is a **monorepo** containing all services for the Palmar Background Remover platform:

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   React     │────▶│   Node.js   │────▶│  PostgreSQL  │
│   Frontend  │     │   API       │     │   Database   │
└─────────────┘     └──────┬──────┘     └──────────────┘
                           │
                           ▼
                    ┌─────────────┐     ┌──────────────┐
                    │   Python    │────▶│    Redis     │
                    │  AI Worker  │     │ Queue/Cache  │
                    └─────────────┘     └──────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │     S3      │
                    │   Storage   │
                    └─────────────┘
```

## 📦 Project Structure

```
palmar-bg-platform/
├── apps/
│   ├── web/             # React frontend (Vite + TypeScript)
│   ├── api/             # Node.js REST API (Express + TypeScript)
│   ├── worker/          # Python AI processing service (FastAPI)
│   └── admin/           # Admin dashboard
│
├── packages/
│   ├── database/        # Prisma ORM + migrations
│   ├── shared/          # Shared TypeScript types
│   ├── ui/              # Shared React components
│   └── config/          # Shared ESLint/TypeScript configs
│
└── infrastructure/
    ├── docker/          # Docker Compose for local dev
    ├── kubernetes/      # K8s manifests for production
    └── terraform/       # Infrastructure as Code (AWS)
```

## 🚀 Quick Start (Development)

### Prerequisites

- **Node.js** 20+ and npm 10+
- **Python** 3.11+
- **Docker** & Docker Compose
- **Git**

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ayodelemartinsabiwo/RemoveBackground.git
cd RemoveBackground/palmar-bg-platform

# Install dependencies
npm install

# Copy environment variables
cp infrastructure/docker/.env.example infrastructure/docker/.env

# Edit .env with your configuration
nano infrastructure/docker/.env
```

### 2. Start Infrastructure

```bash
# Start all services (Postgres, Redis, MinIO, etc.)
npm run docker:up

# Check services are healthy
docker-compose -f infrastructure/docker/docker-compose.yml ps
```

### 3. Initialize Database

```bash
# Generate Prisma client
cd packages/database
npm run db:generate

# Run migrations
npm run db:migrate

# Seed initial data
npm run db:seed

# (Optional) Open Prisma Studio
npm run db:studio
```

### 4. Start Development Servers

```bash
# Terminal 1: Start API server
cd apps/api
npm install
npm run dev

# Terminal 2: Start Worker service
cd apps/worker
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Terminal 3: Start Frontend
cd apps/web
npm install
npm run dev
```

### 5. Access Services

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React web app |
| API | http://localhost:3000 | REST API endpoints |
| Worker | http://localhost:8000 | AI processing service |
| Adminer | http://localhost:8080 | Database UI |
| Redis Commander | http://localhost:8081 | Redis UI |
| MinIO Console | http://localhost:9001 | S3 storage UI |

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for blazing-fast builds
- **Tailwind CSS** + shadcn/ui components
- **TanStack Query** for server state
- **Zustand** for client state
- **React Router** for navigation

### Backend API
- **Node.js 20** with TypeScript
- **Express.js** for REST API
- **Prisma ORM** for database
- **JWT** for authentication
- **BullMQ** for job queues
- **Winston** for logging

### AI Worker
- **Python 3.11+** with FastAPI
- **rembg** for background removal
- **ONNX Runtime** for model inference
- **Celery** for task queue
- **Pillow** for image processing

### Infrastructure
- **PostgreSQL 15** (primary database)
- **Redis 7** (cache + job queue)
- **MinIO** (S3-compatible storage)
- **Docker** for containerization
- **Kubernetes** for orchestration

## 📋 Available Scripts

```bash
# Development
npm run dev              # Start all services in dev mode
npm run build            # Build all apps for production
npm run test             # Run all tests
npm run lint             # Lint all code
npm run format           # Format code with Prettier

# Docker
npm run docker:up        # Start infrastructure
npm run docker:down      # Stop infrastructure

# Database
npm run db:migrate       # Run database migrations
npm run db:seed          # Seed database
npm run db:studio        # Open Prisma Studio
```

## 🔐 Environment Variables

Create `.env` file in `infrastructure/docker/` with:

```env
# Database
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://palmar_admin:password@postgres:5432/palmar_bg_dev

# Redis
REDIS_PASSWORD=your_redis_password
REDIS_URL=redis://:password@redis:6379

# JWT
JWT_SECRET=your_256_bit_secret
JWT_EXPIRES_IN=7d

# AWS S3
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
S3_BUCKET_NAME=palmar-bg-production

# Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx

# SendGrid
SENDGRID_API_KEY=SG.xxx
```

See `.env.example` for full configuration.

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run tests for specific app
npm run test --workspace=@palmar/api

# Run tests with coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

## 📚 API Documentation

Once the API is running, visit:
- **Swagger UI**: http://localhost:3000/api-docs
- **OpenAPI JSON**: http://localhost:3000/api-docs/json

## 🔒 Security Features

✅ **Authentication**: JWT with refresh tokens
✅ **Authorization**: Role-based access control (RBAC)
✅ **Encryption**: AES-256 for data at rest
✅ **Rate Limiting**: Configurable per-endpoint limits
✅ **CORS**: Configurable origin whitelist
✅ **Helmet**: Security headers middleware
✅ **CSRF**: Protection for state-changing operations
✅ **SQL Injection**: Prisma ORM with parameterized queries
✅ **XSS**: Content Security Policy headers

## 📊 Monitoring & Logging

- **Application Logs**: Winston (JSON format)
- **Error Tracking**: Sentry integration
- **Metrics**: Prometheus + Grafana
- **APM**: Datadog integration
- **Uptime**: Health check endpoints

## 🚢 Deployment

### Development
```bash
npm run docker:up
```

### Staging
```bash
# Deploy to staging environment
npm run deploy:staging
```

### Production
```bash
# Build production images
npm run build:production

# Deploy to Kubernetes
kubectl apply -f infrastructure/kubernetes/production/
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🤝 Contributing

This is a proprietary codebase. For internal contributors:

1. Create feature branch from `main`
2. Make changes with tests
3. Submit PR for review
4. Ensure CI passes
5. Get 2 approvals
6. Merge to `main`

## 📄 License

**PROPRIETARY** - All rights reserved. Unauthorized copying, distribution, or modification is strictly prohibited.

## 👥 Team

- **Project Lead**: [Name]
- **Backend Lead**: [Name]
- **Frontend Lead**: [Name]
- **DevOps Lead**: [Name]

## 📞 Support

- **Internal Slack**: #palmar-bg-platform
- **Email**: dev@palmartech.com
- **Documentation**: https://docs.palmartech.com

---

**Built with ❤️ by Palmar Tech**
