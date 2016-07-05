#!/usr/bin/env python
from PIL import Image
import sys
import numpy

def usage():
    print "scramble_image.py img_in key_in img_out"

def main():
    if len(sys.argv) != 4:
        usage()
        exit(1)

    img_in = sys.argv[1]
    key_in = sys.argv[2]
    img_out = sys.argv[3]

    img = Image.open(img_in).convert("RGB")
    key = Image.open(key_in).convert("RGB")
    pimg = img.load()
    pkey = key.load()

    width, height = img.size

    for i in range(width):
        for j in range(height):
            imga = pimg[i, j]
            keya = pkey[i, j]
            encp = numpy.bitwise_xor(imga, keya)
            pimg[i,j] = tuple(encp)
    
    img.save(img_out)

if __name__ == '__main__':
    main()

