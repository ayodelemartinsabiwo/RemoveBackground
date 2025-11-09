"""
Download AI models for bundling with the installer.
This ensures users don't need internet connection to use the app.

Run this BEFORE building the installer to pre-download models.
"""

import os
import sys
from pathlib import Path

def download_models():
    """Download all required AI models"""
    print("=" * 60)
    print("Downloading AI Models for Bundling")
    print("=" * 60)
    print("\nThis will download ~200MB of AI models.")
    print("These models will be bundled with your installer so users")
    print("don't need internet connection after installation.\n")
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Set environment variable to use our models directory
    os.environ['U2NET_HOME'] = str(models_dir.absolute())
    
    print(f"Models will be saved to: {models_dir.absolute()}\n")
    
    try:
        from rembg import new_session
        from PIL import Image
        
        # Download BiRefNet-Portrait (best quality for portraits)
        print("📥 Downloading BiRefNet-Portrait model...")
        print("   Size: ~170MB")
        print("   Purpose: Best for portraits with hair/complex edges")
        
        try:
            session = new_session("birefnet-portrait")
            
            # Test the model with a tiny image to ensure it works
            print("   ✓ Testing model...")
            test_img = Image.new('RGB', (10, 10), color='white')
            from rembg import remove
            _ = remove(test_img, session=session)
            
            print("   ✅ BiRefNet-Portrait model downloaded and verified!\n")
            
        except Exception as e:
            print(f"   ❌ BiRefNet-Portrait download failed: {e}")
            print("   Trying U2Net as fallback...\n")
            
            # Fallback to U2Net
            print("📥 Downloading U2Net model...")
            print("   Size: ~176MB")
            try:
                session = new_session("u2net")
                
                # Test the model
                print("   ✓ Testing model...")
                test_img = Image.new('RGB', (10, 10), color='white')
                _ = remove(test_img, session=session)
                
                print("   ✅ U2Net model downloaded and verified!\n")
                
            except Exception as e2:
                print(f"   ❌ U2Net download also failed: {e2}")
                return False
        
        # List downloaded files
        print("\n" + "=" * 60)
        print("Downloaded Models:")
        print("=" * 60)
        
        if models_dir.exists():
            for file in models_dir.rglob("*"):
                if file.is_file():
                    size_mb = file.stat().st_size / (1024 * 1024)
                    print(f"  ✓ {file.name} ({size_mb:.1f} MB)")
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Models ready for bundling")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Build the executable: python -m PyInstaller build_optimized.spec --clean")
        print("2. Models will be bundled automatically")
        print("3. Users won't need internet connection!\n")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Error: Required libraries not found: {e}")
        print("\nPlease install dependencies first:")
        print("  pip install -r src/requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Error downloading models: {e}")
        return False

if __name__ == "__main__":
    print("\n")
    success = download_models()
    sys.exit(0 if success else 1)
