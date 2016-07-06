#!/usr/bin/env python

import itertools

TEMPLATE = """\
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void encrypt(char *key, char *string) {
    int i;
    int string_length = strlen(string);
    int key_length = strlen(key);
    for(i=0; i<string_length; i++) {
        if (i != 0) {
            string[i]=string[i]^key[i%key_length]^string[i-1];
        } else {
            string[i]=string[i]^key[i%key_length];
        }
        printf("%i ", string[i]);
    }
    printf("\\n");
}

int main(int argc, char* argv[]) {
    char xflag[##lenxflag##] = {##xflag##};
    if (argc != 2) {
        printf("Usage %s <flag>\\n", argv[0]);
        return 1;
    }
    encrypt("##xkey##", argv[1]);
    if (strcmp(argv[1], xflag)) {
        printf("You're wrong.\\n");
    } else {
        printf("You're right.\\n");
    }
    return 0;
}
"""

def encrypt(flag, key):
    e = ""
    l = chr(0)
    for m, k in itertools.izip(flag, itertools.cycle(key)):
        if e:
            e += chr(ord(m) ^ ord(k) ^ ord(l))
        else:
            e += chr(ord(m) ^ ord(k))
        l = e[-1]
    return e

def main():
    flag = raw_input("flag> ")
    key = raw_input("key> ")

    xflag = encrypt(flag, key)
    if chr(0) in xflag:
        print "This flag and this key cannot be used together."
        exit (1)
    xflag_t = ", ".join([str(ord(l)) for l in xflag])

    a_src = TEMPLATE.replace("##xkey##", key)
    b_src = a_src.replace("##lenxflag##", str(len(xflag) + 1))
    c_src = b_src.replace("##xflag##", xflag_t)
    

    with open("lol_so_obfuscated.c", "w") as c_chall:
        c_chall.write(c_src)

    print "The C source has been populated. Please run "
    print "  gcc -O2 lol_so_obfuscated.c -o lol_so_obfuscated"
    print "to obtain the static file to publish."
if __name__ == '__main__':
    main()
