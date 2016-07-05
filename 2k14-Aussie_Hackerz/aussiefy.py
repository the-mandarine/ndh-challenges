from __future__ import unicode_literals
import base64

BASE = {
  'a': '\u0250', 
  'b': 'q', 
  'c': '\u0254',
  'd': 'p',
  'e': '\u01DD',
  'f': '\u025F',
  'g': 'b',
  'h': '\u0265',
  'i': '\u0131',
  'j': '\u0638',
  'k': '\u029E',
  'l': '\u05DF',
  'm': '\u026F',
  'n': 'u',
  'o': 'o',
  'p': 'd',
  'q': 'b',
  'r': '\u0279',
  's': 's',
  't': '\u0287',
  'u': 'n',
  'v': '\u028C',
  'w': '\u028D',
  'x': 'x',
  'y': '\u028E',
  'z': 'z',
  '[': ']',
  ']': '[',
  '(': ')',
  ')': '(',
  '{': '}',
  '}': '{',
  '?': '\u00BF',
  '\u00BF': '?',
  '!': '\u00A1',
  "'": ',',
  ',': "'",
  '.': '\u02D9',
  '_': '\u203E',
  ';': '\u061B',
  '9': '6',
  '6': '9'
}

def main():
    submission = raw_input("flag> ")
    low_sub = submission.lower()
    temp_list = list(low_sub)
    temp_list.reverse()
    flag = "".join(temp_list)
    new_string = ""
    for char in flag:
        if char in BASE:
            new_char = BASE[char]
        else:
            new_char = char
        new_string += new_char

    to_encode = new_string.encode('utf8')

    to_give = base64.b16encode(to_encode)
    #to_give = base64.b32encode(to_encode)
    #to_give = base64.b64encode(to_encode)
    print to_give


if __name__ == '__main__':
    main()


