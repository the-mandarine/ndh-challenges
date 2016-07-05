#!/usr/bin/env python

import sys
from random import randint

def main():
    flag = raw_input("flag: ")
    hide = "" + flag + ""
    with open('input.txt', 'r') as f_in:
        text = f_in.read()
    text_l = list(text)
    t_len = len(text)
    h_len = len(hide)
    inter = t_len / (h_len + 1)
    margin = randint(-inter/2, inter/2)
    for dig in xrange(h_len):
        h_let = hide[dig]
        text_l.insert(dig * inter + margin, h_let)
        
    text = ''.join(text_l)
    with open('./samuel_l_flagson.txt', 'w') as f_out:
        f_out.write(text)

if __name__ == '__main__':
    main()
