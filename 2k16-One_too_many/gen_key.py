#!/usr/bin/env python

from PIL import Image
import numpy

def main():
    #img = Image.new("RGBA", (500,180),(255,255,255))
    rand_array = numpy.random.rand(180, 500, 3) * 255
    img = Image.fromarray(rand_array.astype('uint8')).convert('RGB')
    img.save("key.png")

if __name__ == '__main__':
    main()
