import sys
from PIL import Image, ImageOps
src, dst = sys.argv[1], sys.argv[2]
im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
im.thumbnail((1400, 1400))
im.save(dst, 'JPEG', quality=78, optimize=True)  # re-encode drops EXIF (GPS etc.)
