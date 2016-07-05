
from __future__ import unicode_literals
import sys
import os
from random import randint

FORTUNE_DIR = "fortunes"
SUFFIX = ".txt"

class Fortunes(object):
    def __init__(self, path):
        self.path = os.path.join(path, FORTUNE_DIR)
        
    def get_cat_path(self, category):
        """Return the file path for a category"""
        category_file = "%s%s" % (category, SUFFIX)
        path = os.path.join(self.path, category_file)
        if not os.path.isfile(path):
            open(path, 'w').close()
        return path
        
    def add(self, sentence, category):
        """Append a sentence to a fortune file."""
        fortune_path = self.get_cat_path(category)
        if not sentence.endswith("\n"):
                sentence += "\n"
        to_write = sentence.encode('utf-8')

        with open(fortune_path, 'a') as fortune_file:
            fortune_file.write(to_write)


    def get(self, category):
        """Get a random sentence from a category"""
        fortune_path = self.get_cat_path(category)
        fortune_size = os.path.getsize(fortune_path)
        line_length = randint(50, 100)
        max_offset = max(0, (fortune_size - line_length))
        rand_offset = randint(0, max_offset)
        with open(fortune_path, 'r') as fortune_file:
            fortune_file.seek(rand_offset)
            fortune_file.readline()
            line = fortune_file.readline().strip()
        return line

def test_main():
    f = Fortunes("data")
    print f.get("love")
    
if __name__ == '__main__':
    test_main()
