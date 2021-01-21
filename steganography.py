import sys

from PIL import Image

# convert a byte into an interator that yield chunks
# where n is the number of chunks per byte
def chunks(byte, n):
    mask = (1 << (8 // n)) - 1
    for _ in range(n):
        yield byte & mask
        byte >>= (8 // n)


def main():
    img = Image.open(sys.argv[1])
    n = int(sys.argv[2])

    x, y, z = 0, 0, 0
    mask = (1 << (8 // n)) - 1  # e.g. 0b1111
    mask <<= (8 // n)  # e.g. 0b11110000

    for byte in sys.stdin.buffer:
        for chunk in chunks(byte, n):
            pixel = list(img.getpixel((x, y)))
            pixel[z] = (pixel[z] & mask) | chunk
            img.putpixel((x, y), tuple(pixel))

            # move to next primary color
            z += 1

            # move to next row
            y += (z // 3)
            z %= 3

            # move to next column
            x += (y // img.height)
            y %= img.height

            if x >= img.width:
                print('overflow!')
                continue

    img.show()


if __name__ == '__main__':
    main()
