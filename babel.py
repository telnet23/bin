from random import randrange
from PIL import Image

img = Image.new('RGB', (640, 480))
for i in range(img.width):
    for j in range(img.height):
        img.putpixel((i, j), randrange(1 << 24))
img.show()
