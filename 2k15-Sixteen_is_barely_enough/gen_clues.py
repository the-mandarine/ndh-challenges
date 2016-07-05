#!/usr/bin/env python

import hashlib
import string
import random

NB_CLUES = 6

def id_generator(size=40, chars=string.letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(random.randint(6,size)))

PHP_CODE = """$banned_passes = array(
""" + ",\n".join(NB_CLUES * ['"%s"']) + """
);
"""

def main():
    ok_hashes = []
    while len(ok_hashes) < NB_CLUES:
        msg = id_generator()
        hmsg = hashlib.sha384(msg).hexdigest()
        if hmsg.startswith('0') and hmsg[1] == 'e':
            if hmsg[2:16].isdigit():
                ok_hashes.append(msg)
    print "// copy this in the top of admin.php"
    print PHP_CODE % tuple(ok_hashes)



if __name__ == '__main__':
    main()