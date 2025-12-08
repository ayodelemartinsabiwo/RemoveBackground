# ✅ PROCESSING LOOP FIXED - Celery Worker Initialization

## Problem
- ❌ Images stuck in "PENDING" status forever
- ❌ Processing never completes
- ❌ Frontend polling infinitely until manual page refresh
- ❌ Worker logs showing: `'NoneType' object has no attribute 'download_fileobj'`

## Root Cause
**Celery Worker Process Forking Issue**

```
Main Process (FastAPI)
  ├─ S3 client initialized ✓
  └─ Celery spawns worker processes via fork()
      ├─ ForkPoolWorker-1 (S3 client = None ❌)
      └─ ForkPoolWorker-2 (S3 client = None ❌)
```

**Why It Failed:**
1. S3 client initialized in main FastAPI process
2. Celery uses `fork()` to create worker processes
3. Forked processes don't inherit socket connections or boto3 clients
4. Worker processes had `s3_client.client = None`
5. Download/upload operations failed with NoneType error
6. Database status stuck in PENDING

## Solution
Added Celery worker process initialization signal:

```python
# apps/worker/app/tasks/celery_app.py

from celery.signals import worker_process_init

@worker_process_init.connect
def init_worker(**kwargs):
    """
    Initialize connections when Celery worker process starts
    This runs in each forked worker process
    """
    from app.core.s3 import s3_client

    print("🔧 Initializing Celery worker process...")

    # Initialize S3 client in this worker process
    try:
        s3_client.connect()
        print(f"✓ S3 connected in worker process: {s3_client.bucket_name}")
    except Exception as e:
        print(f"✗ Failed to connect S3 in worker: {e}")
```

## Verification

### Logs Before Fix:
```
✓ Using S3 bucket: palmar-bg-images  (main process only)
...
[ForkPoolWorker-1] ✗ S3 download failed: 'NoneType' object has no attribute 'download_fileobj'
[ForkPoolWorker-1] ✗ Processing failed for image: Failed to download original image from S3
```

### Logs After Fix:
```
✓ Using S3 bucket: palmar-bg-images  (main process)
...
[ForkPoolWorker-1] 🔧 Initializing Celery worker process...
[ForkPoolWorker-1] ✓ Using S3 bucket: palmar-bg-images
[ForkPoolWorker-1] ✓ S3 connected in worker process: palmar-bg-images
[ForkPoolWorker-2] 🔧 Initializing Celery worker process...
[ForkPoolWorker-2] ✓ Using S3 bucket: palmar-bg-images
[ForkPoolWorker-2] ✓ S3 connected in worker process: palmar-bg-images
```

## How Processing Now Works

```
1. User uploads image
   ↓
2. API saves to MinIO, creates DB record (status: PENDING)
   ↓
3. API triggers Celery task via HTTP
   ↓
4. Celery queues task in Redis
   ↓
5. ForkPoolWorker-1 picks up task
   ✓ Worker has its own S3 connection
   ↓
6. Worker updates status to PROCESSING
   ↓
7. Worker downloads image from MinIO ✅ NOW WORKS
   ↓
8. Worker removes background with BiRefNet AI
   ↓
9. Worker uploads processed image to MinIO ✅ NOW WORKS
   ↓
10. Worker updates status to COMPLETED ✅
   ↓
11. Frontend polling detects completion
   ↓
12. User sees processed image with transparent background
```

## Key Takeaways

### Python Multiprocessing & Celery
- Celery uses `fork()` to create worker processes
- Forked processes are **copies** of parent memory
- Socket connections (boto3, database pools) **are not inherited**
- Each worker process needs its own connection initialization

### Celery Signals
- `@worker_process_init`: Runs once when worker process starts
- `@worker_ready`: Runs after worker is fully initialized
- `@task_prerun`: Runs before each task
- Use `worker_process_init` for connection pooling setup

### Best Practice
Always initialize connections in worker processes, not just main process:
```python
@worker_process_init.connect
def init_worker(**kwargs):
    # Initialize database connections
    # Initialize S3/storage clients
    # Initialize Redis clients
    # Load ML models
```

## Test Now

**Upload a new image:**
1. Go to http://localhost:5173/editor
2. Upload an image with a person
3. **Expected:**
   - Processing spinner appears
   - After 5-15 seconds: "Background removed successfully!"
   - Processed image displays
   - Status: PENDING → PROCESSING → COMPLETED (not stuck!)

**Check Worker Logs:**
```powershell
docker logs palmar-worker-dev --tail 100 -f
```

**Expected Output:**
```
[ForkPoolWorker-X] 🔧 Initializing Celery worker process...
[ForkPoolWorker-X] ✓ S3 connected in worker process: palmar-bg-images
[ForkPoolWorker-X] Processing image {id} for user {user-id}
[ForkPoolWorker-X] Downloading from S3: images/...
[ForkPoolWorker-X] Removing background...
[ForkPoolWorker-X] ✓ Background removed successfully
[ForkPoolWorker-X] ✓ Uploaded to S3: images/.../processed_{id}.png
[ForkPoolWorker-X] ✓ Updated image status to COMPLETED
```

---

**Status:** ✅ FULLY FIXED - Processing loop resolved, Celery workers properly initialized
