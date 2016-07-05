#!/usr/bin/env python

FLAG="NDH_0c10c8dc95612df2e0e0e9f433460433"
PREFIX_STRING="the fLag is "
SUFFIX_STRING=" ."
BASE="l o r e m i p s u md ol or si t a me tc".split()




def main():
    flag = FLAG
    string_to_encode = PREFIX_STRING + flag + SUFFIX_STRING
    final_string = ""
    for letter in string_to_encode:
        ascii_letter = ord(letter)
        chari1 = ascii_letter / 17
        chari2 = ascii_letter % 17
        final_string += BASE[chari1]
        final_string += BASE[chari2]

    print final_string

if __name__ == '__main__':
    main()

