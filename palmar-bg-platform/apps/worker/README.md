# Palmar Background Removal - Python AI Worker

Production-grade Python worker service for AI-powered background removal.

## Features

- ✅ BiRefNet-portrait model for accurate background removal
- ✅ Hair strand preservation and edge refinement
- ✅ Multi-resolution outputs (Small, HD, Ultra-HD)
- ✅ Background customization (solid colors, gradients, textures)
- ✅ Celery task queue for async processing
- ✅ S3/MinIO integration for file storage
- ✅ FastAPI health check endpoints
- ✅ BullMQ bridge for Node.js API integration

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Node.js    │─────▶│   BullMQ     │─────▶│   Bridge    │
│     API     │      │   (Redis)    │      │   Service   │
└─────────────┘      └──────────────┘      └──────┬──────┘
                                                   │
                                                   ▼
                                            ┌─────────────┐
                                            │   Celery    │
                                            │    Task     │
                                            └──────┬──────┘
                                                   │
                     ┌─────────────────────────────┴───────────────────────┐
                     │                                                     │
                     ▼                                                     ▼
              ┌─────────────┐                                      ┌─────────────┐
              │  Background │                                      │     S3/     │
              │   Removal   │                                      │   MinIO     │
              │   Service   │                                      │   Storage   │
              └─────────────┘                                      └─────────────┘
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Services

**FastAPI Server** (health checks):
```bash
python -m app.main
```

**Celery Worker**:
```bash
celery -A app.tasks.celery_app worker --loglevel=info --concurrency=2
```

**BullMQ Bridge**:
```bash
python bridge.py
```

## Docker Deployment

### Development

```bash
docker build -t palmar-bg-worker:dev -f Dockerfile .
docker run -p 8001:8001 --env-file .env palmar-bg-worker:dev
```

### Production

```bash
docker build -t palmar-bg-worker:prod -f Dockerfile.prod .
docker run -p 8001:8001 --env-file .env palmar-bg-worker:prod
```

## API Endpoints

### Health Checks

- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check (validates all dependencies)
- `GET /health/live` - Liveness check

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `REDIS_HOST` | Redis hostname | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `DATABASE_URL` | PostgreSQL connection string | - |
| `S3_ENDPOINT` | S3/MinIO endpoint | - |
| `S3_ACCESS_KEY` | S3 access key | `minioadmin` |
| `S3_SECRET_KEY` | S3 secret key | `minioadmin` |
| `MODEL_NAME` | Primary AI model | `birefnet-portrait` |
| `WORKER_CONCURRENCY` | Celery worker concurrency | `2` |

## Processing Flow

1. **Job Received** - BullMQ bridge receives job from Redis
2. **Trigger Celery** - Bridge triggers Celery task
3. **Download Image** - Celery worker downloads original from S3
4. **Remove Background** - AI model processes image
5. **Apply Customization** - Add background if requested
6. **Generate Resolutions** - Create small, HD, and ultra-HD versions
7. **Upload to S3** - Store all processed versions
8. **Update Database** - Mark image as completed with S3 URLs

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black app/
isort app/
```

## Troubleshooting

### Models not loading

Ensure the model files are present in the correct location:
- BiRefNet-portrait: Downloaded automatically by rembg
- U2Net: Downloaded automatically by rembg

### Redis connection failed

Check that Redis is running and accessible:
```bash
redis-cli ping
```

### S3 upload failed

Verify S3/MinIO credentials and endpoint configuration.

## License

Proprietary - Palmar Professional Background Remover
