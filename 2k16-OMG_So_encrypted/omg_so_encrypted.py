#!/usr/bin/env python

from random import choice, shuffle
from hashlib import md5
from textwrap import wrap

CHALL_PATH = "./omg_so_encrypted.txt"
FLAG_PREFIX = "NDH_"

TEXT_START = """\
This text is here to simulate a sementic analysis. It means that when you
get a corporate document, you usually have to read it and analyse it before 
you get the useful information.
"""
TEXT_END = """\
"""

ORDINALS = ("very first", "second", "third", "fourth", "fifth", "sixth", 
"seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", 
"fourteenth", "fifteenth", "sixteenth", "seventeenth", "eighteenth", 
"nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third",
"twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", 
"twenty-eighth", "twenty-ninth", "thirtieth", "thirty-first", "thirty-second")

BE_DICT = ("is", "seems to be", "appears to be", "will have the value of", 
"should be", "was set to")


def desc_hash(flag_h):
    descs = []
    for l_id in xrange(len(flag_h)):
        desc = "%s letter of the hash %s %s. " % (ORDINALS[l_id],
                                                    choice(BE_DICT),
                                                    flag_h[l_id])
        descs.append(desc)
        shuffle(descs)
    return "".join(descs)

def describe(flag_h):
    desc_str = TEXT_START
    desc_str += "The flag starts with '%s'. " % FLAG_PREFIX
    desc_str += "After that, there is the hash.\n"
    desc_str += desc_hash(flag_h)
    desc_str += TEXT_END
    desc = "\n".join(wrap(desc_str, 79))
    return desc

def main():
    flag = raw_input("flag> ")
    if flag.startswith(FLAG_PREFIX):
        flag_h = flag[len(FLAG_PREFIX):]
    else:
        flag_h = md5(flag).hexdigest()
    print "The flag is %s%s\n" % (FLAG_PREFIX, flag_h)
    flag_desc = describe(flag_h)
    challenge = flag_desc.encode("rot13")
    with open(CHALL_PATH, 'w') as chall_file:
        chall_file.write(challenge)

if __name__ == '__main__':
    main()
