#!/usr/bin/env python

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy

def gen_image(msg, fname, top = True):
    t_pos = (10, 100)
    if top:
        t_pos = (10, 10)
    font = ImageFont.truetype("Arial.ttf",42)
    #img = Image.new("RGBA", (500,180),(255,255,255))
    rand_array = numpy.random.rand(90, 500, 3) * 255
    white_array = numpy.random.rand(90, 500, 3) * 0
    if top:
        full_array = numpy.vstack((rand_array, white_array))
    else:
        full_array = numpy.vstack((white_array, rand_array))
    img = Image.fromarray(full_array.astype('uint8')).convert('RGB')
    draw = ImageDraw.Draw(img)
    draw.text(t_pos, msg, (255,255,255), font=font)
    draw = ImageDraw.Draw(img)
    img.save(fname)


def main():
    flag = raw_input("flag> ")
    limit = len(flag) / 2
    flag_p1 = flag[:limit]
    flag_p2 = flag[limit:]

    gen_image(flag_p1, "part_1.png")
    gen_image(flag_p2, "part_2.png", False)


if __name__ == '__main__':
    main()
