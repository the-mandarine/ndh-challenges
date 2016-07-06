#!/usr/bin/env python

import sqlite3
import os
import random, string

DB_PATH = "./standard.db"
NB_DATA_BEFORE = 5
NB_DATA_AFTER = 20


def random_word(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


def main():
    flag = raw_input("flag> ")

    try:
        os.remove(DB_PATH)
    except OSError:
        pass

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE users
                 (id INTEGER, name text, password text, admin INTEGER)''')
    c.execute('''CREATE TABLE items
                 (name text, value text, admin INTEGER)''')

    c.execute("INSERT INTO users VALUES (1, 'notadmin', 'Flag_aint_there', 0)")
    c.execute("INSERT INTO users VALUES (2, 'demo', 'demo', 0)")
    c.execute("INSERT INTO users VALUES (3, 'admin', 'Flag_aint_there_either', 1)")

    useless_q = "INSERT INTO items VALUES ('%s', '%s', 0) "
    for i in xrange(NB_DATA_BEFORE):
        c.execute(useless_q % (random_word(6), random_word(32)))

    c.execute("INSERT INTO items VALUES ('the_flag', '%s', 1)" % (flag))

    for i in xrange(NB_DATA_AFTER):
        c.execute(useless_q % (random_word(6), random_word(32)))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
