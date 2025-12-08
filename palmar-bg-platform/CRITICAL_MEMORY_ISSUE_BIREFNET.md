# ⚠️ CRITICAL: BiRefNet Model Memory Issue

## Problem Summary

**The AI worker is being killed by the system (SIGKILL signal 9) due to excessive memory consumption during image processing.**

### Symptoms:
- ✅ Worker starts successfully
- ✅ S3 connection works
- ✅ Model downloads (973MB)
- ✅ Model initializes successfully
- ❌ Worker killed during actual image processing inference
- ❌ Status stuck in `PROCESSING` forever

### Error Pattern:
```
[2025-12-07 14:28:27,032] ✓ Successfully initialized model: birefnet-portrait
[2025-12-07 14:45:15,207] ❌ Process 'ForkPoolWorker-157' pid:527 exited with 'signal 9 (SIGKILL)'
billiard.exceptions.WorkerLostError: Worker exited prematurely: signal 9 (SIGKILL)
```

## Root Cause

**BiRefNet-portrait model requires 8GB+ RAM during inference** (actual image processing), far exceeding:
- Initial attempt: No limit → Killed
- Second attempt: 4GB limit → Killed
- Third attempt: 6GB limit → Killed
- Current state: **Still getting killed with concurrency=1 and 6GB memory**

### Memory Breakdown:
1. **Model file**: 973MB (download size)
2. **Model loaded in memory**: ~2-3GB (uncompressed PyTorch model)
3. **Inference memory**: ~4-6GB (temporary tensors, gradients, activations)
4. **Total**: **8-10GB+ during active processing**

## What Was Tried

### Attempt 1: No Memory Limits
```yaml
# Initial configuration - no limits
worker:
  # No deploy.resources specified
```
**Result:** ❌ Worker killed immediately

### Attempt 2: 4GB Memory Limit
```yaml
deploy:
  resources:
    limits:
      memory: 4G
```
**Result:** ❌ Worker killed after model initialization

### Attempt 3: 6GB Memory + Concurrency=1
```yaml
deploy:
  resources:
    limits:
      memory: 6G
    reservations:
      memory: 3G
environment:
  CELERY_WORKER_CONCURRENCY: "1"
```
**Result:** ❌ Still getting killed during inference

## Solutions

### Option 1: Use Lighter AI Model (RECOMMENDED for Development)

Switch from BiRefNet-portrait to U2Net (much lighter):

**Changes needed:**

1. **docker-compose.dev.yml**:
```yaml
worker:
  environment:
    MODEL_NAME: u2net  # Changed from birefnet-portrait
    CELERY_WORKER_CONCURRENCY: "1"
  deploy:
    resources:
      limits:
        memory: 3G  # U2Net only needs ~2GB
```

2. **Model comparison:**
| Model | Size | RAM Needed | Quality | Speed |
|-------|------|------------|---------|-------|
| U2Net | 176MB | ~2GB | Good | Fast |
| BiRefNet-portrait | 973MB | ~8-10GB | Excellent | Slow |

**U2Net Pros:**
- ✅ Works with 3GB RAM
- ✅ Faster processing
- ✅ Good enough for development/testing
- ✅ No system kills

**U2Net Cons:**
- Quality slightly lower than BiRefNet
- Less accurate on complex backgrounds

### Option 2: Increase System RAM (Production)

**For production deployment:**

1. **Increase Docker Desktop Memory** (if using Docker Desktop):
   - Docker Desktop → Settings → Resources
   - Set Memory to **12GB minimum**
   - Restart Docker

2. **Update worker config**:
```yaml
worker:
  environment:
    MODEL_NAME: birefnet-portrait
    CELERY_WORKER_CONCURRENCY: "1"
  deploy:
    resources:
      limits:
        memory: 10G  # Give model enough headroom
      reservations:
        memory: 6G
```

3. **System requirements:**
   - Development: 16GB+ total RAM
   - Production: 32GB+ total RAM (for multiple workers)

### Option 3: Cloud GPU Instance (Best Quality)

For production with BiRefNet:

1. Deploy worker on GPU-enabled cloud instance:
   - AWS EC2 g4dn.xlarge (16GB RAM + GPU)
   - Google Cloud n1-standard-8 + T4 GPU
   - Azure NC6s_v3

2. Update worker to use GPU acceleration:
```python
# app/services/background_removal.py
# Add GPU support
device = "cuda" if torch.cuda.is_available() else "cpu"
```

### Option 4: External AI API Service

Use hosted AI service instead of self-hosting:

1. **Remove.bg API**: https://remove.bg/api
   - $0.20 per image
   - No infrastructure needed
   - Professional quality

2. **Clipdrop API**: https://clipdrop.co/apis
   - Better pricing for volume
   - Multiple AI models

3. **ImgBB + remove.bg combo**

## Immediate Action Required

**Choose one path:**

### Path A: Quick Fix (Development) - Switch to U2Net
```bash
# Update docker-compose.dev.yml MODEL_NAME to "u2net"
# Reduce memory limit to 3G
# Restart worker
docker-compose -f docker-compose.dev.yml up -d worker --force-recreate
```

### Path B: Production Setup - Increase RAM
```bash
# 1. Increase Docker Desktop memory to 12GB
# 2. Update worker memory limit to 10G
# 3. Restart Docker
# 4. Rebuild and restart worker
```

### Path C: Cloud Deployment - Use GPU Instance
```bash
# Deploy worker container to cloud GPU instance
# Keep local development with U2Net
# Production uses BiRefNet on GPU
```

## Recommendation

**For current development:**
✅ **Switch to U2Net model immediately**
   - Fast to implement (change one env var)
   - Works reliably with available RAM
   - Good enough quality for testing
   - Can always upgrade to BiRefNet in production

**For production:**
✅ **Deploy BiRefNet worker on cloud GPU instance**
   - Best quality results
   - Professional performance
   - Scalable
   - Cost-effective at scale

## Next Steps

1. **Immediate** (< 5 minutes):
   - Change `MODEL_NAME: u2net` in docker-compose.dev.yml
   - Reduce memory limit to 3G
   - Restart worker
   - Test image processing

2. **Short-term** (today):
   - Verify U2Net works end-to-end
   - Test with various image types
   - Document quality differences

3. **Long-term** (production):
   - Set up cloud GPU worker for BiRefNet
   - Configure model selection based on user tier
   - Implement cost controls

---

**Current Status:** ❌ Image processing **non-functional** due to worker OOM kills

**Action Required:** Choose solution path and implement today

**ETA to working system:**
- U2Net switch: 5 minutes
- RAM increase: 30 minutes
- Cloud setup: 2-4 hours
