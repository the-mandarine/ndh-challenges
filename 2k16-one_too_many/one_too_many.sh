#!/bin/bash

python gen_both_images.py
python gen_key.py
python scramble_image.py part_1.png key.png one_too_many_1.png
python scramble_image.py part_2.png key.png one_too_many_2.png

rm ./*.png

echo "Done."
