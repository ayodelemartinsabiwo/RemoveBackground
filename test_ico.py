from PIL import Image
import os

# Load one PNG
img = Image.open('assets/Icon PNGs/icon_256x256.png')
print(f'Image size: {img.size}, mode: {img.mode}')

# Try to save as ICO
img.save('test_single.ico', format='ICO')
print(f'Single ICO size: {os.path.getsize("test_single.ico")} bytes')

# Try multi-resolution
images = []
for size in [16, 24, 32, 48, 64, 128, 256]:
    png_path = f'assets/Icon PNGs/icon_{size}x{size}.png'
    img = Image.open(png_path)
    images.append(img)
    print(f'Loaded: {size}x{size}')

# Save multi-res ICO
images[0].save(
    'test_multi.ico',
    format='ICO',
    sizes=[(img.width, img.height) for img in images],
    append_images=images[1:]
)
print(f'Multi ICO size: {os.path.getsize("test_multi.ico")} bytes')
