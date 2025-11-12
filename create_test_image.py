import os
from PIL import Image

# Create a test image
test_image = Image.new('RGB', (300, 300), color='blue')
test_path = 'test_exe.jpg'
test_image.save(test_path, 'JPEG')
print(f"Created test image: {test_path}")
