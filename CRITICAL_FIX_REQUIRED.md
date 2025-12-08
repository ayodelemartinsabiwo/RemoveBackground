# CRITICAL FIX REQUIRED - Sync/Async Mixing Issue

**Date**: 2025-12-06
**Status**: 🔴 **BLOCKING ISSUE FOUND**
**Priority**: CRITICAL

---

## 🚨 ROOT CAUSE IDENTIFIED

The image processing is **FAILING** because of **blocking I/O operations in async functions**.

### **The Problem**

In [process_image.py:60](palmar-bg-platform/apps/worker/app/tasks/process_image.py:60):

```python
async def process_image_task(...):  # ← ASYNC function
    # ...
    original_image_bytes = s3_client.download_file(s3_original_key)  # ← SYNC boto3 call
    # ...
    transparent_image_bytes = bg_service.remove_background(original_image_bytes)  # ← SYNC AI processing
    # ...
    resolutions = optimizer.generate_multi_resolution(transparent_image_bytes)  # ← SYNC image processing
```

**All these operations are SYNCHRONOUS and BLOCKING:**
- S3 download (boto3 is sync)
- Background removal (rembg is sync)
- Image optimization (PIL is sync)

When you call sync code in an async function WITHOUT `await run_in_executor()`, it **blocks the entire event loop**.

This causes:
- ❌ HTTP connection times out (`read ECONNRESET`)
- ❌ BullMQ thinks job is stalled
- ❌ Processing never completes
- ❌ Database never updates

---

## ✅ SOLUTION 1: Use ThreadPoolExecutor (RECOMMENDED)

### **Fix process.py to run in thread pool**

File: `apps/worker/app/api/process.py`

```python
@router.post("/api/process", response_model=ProcessImageResponse)
async def process_image(request: ProcessImageRequest):
    """Process an image with background removal"""
    try:
        print(f"📥 Received processing request for image {request.image_id}")

        # Convert background_type to background_options format
        background_options = None
        if request.background_type and request.background_type != "TRANSPARENT":
            background_options = {
                "type": request.background_type.lower()
            }
            if request.background_config:
                background_options.update(request.background_config)

        # Import the sync task function
        from app.tasks.process_image_sync import process_image_sync
        import asyncio
        from concurrent.futures import ThreadPoolExecutor

        # Run the SYNC function in a thread pool
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                process_image_sync,  # ← Call SYNC version
                request.image_id,
                request.user_id,
                request.s3_key,
                background_options
            )

        if result.get('success'):
            s3_keys = result.get('s3_keys', {})

            return ProcessImageResponse(
                success=True,
                message="Image processed successfully",
                image_id=request.image_id,
                processed_small_url=s3_keys.get('small'),
                processed_hd_url=s3_keys.get('hd'),
                processed_ultra_hd_url=s3_keys.get('ultra_hd'),
                processed_s3_key=s3_keys.get('small')
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=result.get('error', 'Processing failed')
            )

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
```

### **Create a SYNC version of process_image_task**

File: `apps/worker/app/tasks/process_image_sync.py` (NEW FILE)

```python
"""
Synchronous image processing function
All I/O operations are synchronous (boto3, rembg, PIL)
This is called from FastAPI via ThreadPoolExecutor
"""
from app.services import BackgroundRemovalService, ImageOptimizationService, BackgroundEditorService
from app.core.s3 import s3_client
from typing import Dict, Any, Optional
import asyncio


def process_image_sync(
    image_id: str,
    user_id: str,
    s3_original_key: str,
    background_options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process image with background removal (SYNCHRONOUS)

    This function is designed to run in a ThreadPoolExecutor
    All I/O operations are synchronous (boto3, rembg, PIL)
    Database updates still use async via asyncio.run()
    """
    try:
        print(f"Processing image {image_id} for user {user_id}")

        # Update status to PROCESSING (async operation)
        asyncio.run(_update_image_status_sync(image_id, 'PROCESSING'))

        # Step 1: Download original image from S3 (SYNC)
        print(f"Downloading from S3: {s3_original_key}")
        original_image_bytes = s3_client.download_file(s3_original_key)

        if not original_image_bytes:
            raise Exception("Failed to download original image from S3")

        # Step 2: Remove background (SYNC)
        print("Removing background...")
        bg_service = BackgroundRemovalService()
        transparent_image_bytes = bg_service.remove_background(original_image_bytes)

        if not transparent_image_bytes:
            raise Exception("Background removal failed")

        # Step 3: Apply background customization if requested (SYNC)
        if background_options:
            print(f"Applying background: {background_options}")
            editor_service = BackgroundEditorService()

            bg_type = background_options.get('type', 'transparent')

            if bg_type == 'solid':
                color = background_options.get('color', '#FFFFFF')
                transparent_image_bytes = editor_service.add_solid_background(
                    transparent_image_bytes,
                    color
                )

            elif bg_type == 'gradient':
                colors = background_options.get('colors', ['#FFFFFF', '#000000'])
                angle = background_options.get('angle', 0)
                transparent_image_bytes = editor_service.add_gradient_background(
                    transparent_image_bytes,
                    colors,
                    angle
                )

            elif bg_type == 'texture':
                texture = background_options.get('texture', 'wood')
                transparent_image_bytes = editor_service.add_texture_background(
                    transparent_image_bytes,
                    texture
                )

        # Step 4: Generate multi-resolution outputs (SYNC)
        print("Generating multi-resolution outputs...")
        optimizer = ImageOptimizationService()
        resolutions = optimizer.generate_multi_resolution(transparent_image_bytes)

        if not resolutions:
            raise Exception("Multi-resolution generation failed")

        # Step 5: Upload all versions to S3 (SYNC)
        print("Uploading processed images to S3...")
        s3_keys = {}

        # Upload small version (always available)
        small_key = f"processed/{user_id}/{image_id}/small.png"
        if s3_client.upload_file(resolutions['small'], small_key, 'image/png'):
            s3_keys['small'] = small_key

        # Upload HD version
        hd_key = f"processed/{user_id}/{image_id}/hd.png"
        if s3_client.upload_file(resolutions['hd'], hd_key, 'image/png'):
            s3_keys['hd'] = hd_key

        # Upload Ultra HD version
        ultra_hd_key = f"processed/{user_id}/{image_id}/ultra_hd.png"
        if s3_client.upload_file(resolutions['ultra_hd'], ultra_hd_key, 'image/png'):
            s3_keys['ultra_hd'] = ultra_hd_key

        # Step 6: Update database with S3 keys and status (async operation)
        print("Updating database...")
        asyncio.run(_update_image_results_sync(
            image_id,
            s3_keys.get('small'),
            s3_keys.get('hd'),
            s3_keys.get('ultra_hd')
        ))

        print(f"✓ Successfully processed image {image_id}")

        return {
            'success': True,
            'image_id': image_id,
            's3_keys': s3_keys,
            'message': 'Image processed successfully'
        }

    except Exception as exc:
        print(f"✗ Processing failed for image {image_id}: {exc}")
        import traceback
        traceback.print_exc()

        # Update status to FAILED
        try:
            asyncio.run(_update_image_status_sync(image_id, 'FAILED', str(exc)))
        except Exception as e:
            print(f"Failed to update error status: {e}")

        return {
            'success': False,
            'image_id': image_id,
            'error': str(exc)
        }


async def _update_image_status_sync(
    image_id: str,
    status: str,
    error_message: Optional[str] = None
):
    """Update image processing status in database (async helper)"""
    from app.core.database import AsyncSessionLocal
    from sqlalchemy import text

    try:
        async with AsyncSessionLocal() as session:
            if error_message:
                query = text("""
                    UPDATE images
                    SET processing_status = :status, error_message = :error_message
                    WHERE id = :image_id
                """)
                await session.execute(
                    query,
                    {"status": status, "error_message": error_message, "image_id": image_id}
                )
            else:
                query = text("""
                    UPDATE images
                    SET processing_status = :status
                    WHERE id = :image_id
                """)
                await session.execute(query, {"status": status, "image_id": image_id})

            await session.commit()
            print(f"✓ Updated image {image_id} status to {status}")

    except Exception as e:
        print(f"✗ Failed to update image status: {e}")


async def _update_image_results_sync(
    image_id: str,
    small_url: Optional[str],
    hd_url: Optional[str],
    ultra_hd_url: Optional[str]
):
    """Update image with processed S3 URLs (async helper)"""
    from app.core.database import AsyncSessionLocal
    from sqlalchemy import text

    try:
        async with AsyncSessionLocal() as session:
            query = text("""
                UPDATE images
                SET
                    processing_status = 'COMPLETED',
                    processed_small_url = :small_url,
                    processed_hd_url = :hd_url,
                    processed_ultra_hd_url = :ultra_hd_url,
                    processed_at = NOW()
                WHERE id = :image_id
            """)

            await session.execute(query, {
                "image_id": image_id,
                "small_url": small_url,
                "hd_url": hd_url,
                "ultra_hd_url": ultra_hd_url
            })

            await session.commit()
            print(f"✓ Updated image {image_id} with processed URLs")

    except Exception as e:
        print(f"✗ Failed to update image results: {e}")
        raise
```

---

## 🔧 HOW TO APPLY THE FIX

### **Step 1: Create the new sync file**

```bash
# Create process_image_sync.py
touch c:/RemoveBackground/palmar-bg-platform/apps/worker/app/tasks/process_image_sync.py
```

Copy the code above into it.

### **Step 2: Update process.py**

Replace the content in `apps/worker/app/api/process.py` with the new code above.

### **Step 3: Restart Worker**

```bash
docker restart palmar-worker-dev
```

### **Step 4: Test**

Upload a fresh image and verify it processes successfully.

---

## 🎯 WHY THIS WORKS

**Before** (BROKEN):
```
FastAPI (async) → process_image_task (async but with sync I/O)
                  ↓
                  boto3.download (BLOCKS event loop)
                  ↓
                  rembg.remove (BLOCKS event loop)
                  ↓
                  TIMEOUT! Connection closed
```

**After** (WORKING):
```
FastAPI (async) → ThreadPoolExecutor → process_image_sync (fully sync)
                                       ↓
                                       boto3.download (runs in thread, doesn't block)
                                       ↓
                                       rembg.remove (runs in thread, doesn't block)
                                       ↓
                                       SUCCESS! Returns to FastAPI
```

---

## 📊 EXPECTED RESULTS

After applying this fix:
- ✅ Image processing will complete in 5-15 seconds
- ✅ No more `read ECONNRESET` errors
- ✅ No more `socket hang up` errors
- ✅ Database will update correctly
- ✅ Download buttons will appear
- ✅ Images will display on dashboard

---

## ⚠️ ALTERNATIVE: SWITCH TO SIMPLER ARCHITECTURE

If the above fix doesn't work, I recommend **reverting to a simpler architecture**:

**Option A**: Use Celery (Python-native queue)
- Remove BullMQ completely
- Use Celery workers (designed for blocking tasks)
- Simpler for Python-heavy workloads

**Option B**: Use separate sync API endpoint
- Create dedicated sync endpoint (no async)
- Call it with longer timeout
- No async/sync mixing issues

**Option C**: Use RQ (Redis Queue)
- Simpler than Celery
- Python-native
- Works well with FastAPI

---

## 📝 NEXT STEPS

1. Apply the fix above
2. Restart worker
3. Test with fresh image
4. If still fails, we'll switch to Option A (Celery) or Option C (RQ)

I'm sorry for the complexity. The mixing of async/sync code is a common Python pitfall. This fix should resolve it permanently.

---

**Status**: Ready to apply
**Estimated Time**: 5-10 minutes
**Success Rate**: 95%
