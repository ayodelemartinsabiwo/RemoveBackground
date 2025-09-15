import os
import sys
from pathlib import Path

def test_background_removal():
    """Test the background removal functionality"""
    print("🧪 Testing Background Removal Functionality...")
    print("=" * 50)

    # Add src to path so we can import modules
    sys.path.insert(0, 'src')

    try:
        from bg_remove import BackgroundRemover

        # Create a simple test image
        from PIL import Image
        import tempfile

        # Create a simple test image (red square on white background)
        test_img = Image.new('RGB', (100, 100), (255, 255, 255))
        # Draw a red square in the center
        for x in range(25, 75):
            for y in range(25, 75):
                test_img.putpixel((x, y), (255, 0, 0))

        # Save test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            test_img.save(temp_file.name, 'PNG')
            temp_path = temp_file.name

        print(f"✅ Created test image: {temp_path}")

        # Test background removal
        remover = BackgroundRemover()
        success, result = remover.remove_background(temp_path)

        if success:
            print(f"✅ Background removal successful!")
            print(f"   Output saved to: {result}")

            # Verify output file exists
            if os.path.exists(result):
                print("✅ Output file created successfully")
                file_size = os.path.getsize(result)
                print(f"   File size: {file_size} bytes")
            else:
                print("❌ Output file not found")

        else:
            print(f"❌ Background removal failed: {result}")

        # Clean up
        try:
            os.unlink(temp_path)
            if success and os.path.exists(result):
                os.unlink(result)
            print("✅ Cleaned up test files")
        except:
            pass

        return success

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_background_removal()

    print("\n" + "=" * 50)
    if success:
        print("✅ All functionality tests passed!")
        print("\nYour Background Remover is ready to use!")
    else:
        print("❌ Some tests failed. Check the error messages above.")

    input("\nPress Enter to exit...")
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
