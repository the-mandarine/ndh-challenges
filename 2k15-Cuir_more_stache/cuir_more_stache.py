#!/usr/bin/env python

from pydub import AudioSegment

ADD_BLANKS = True
MORSE = {
        'A': '.-',   
        'B': '-...', 
        'C': '-.-.', 
        'D': '-..',  
        'E': '.',    
        'F': '..-.', 
        'G': '--.',  
        'H': '....', 
        'I': '..',   
        'J': '.---', 
        'K': '-.-',  
        'L': '.-..', 
        'M': '--',   
        'N': '-.',   
        'O': '---',  
        'P': '.--.', 
        'Q': '--.-', 
        'R': '.-.',  
        'S': '...',  
        'T': '-',    
        'U': '..-',  
        'V': '...-', 
        'W': '.--',  
        'X': '-..-', 
        'Y': '-.--', 
        'Z': '--..', 
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ' ': ' ',    
}

def morse(line):
    res = ''
    for letter in line.upper():
        try:
            res += MORSE[letter]
            if not letter == ' ':
                res += '!'
        except KeyError:
            pass
    return res

def repeat_to_length(string_to_expand, length):
   return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def main():
    flag = raw_input("flag> ")

    c_wave = AudioSegment.from_file("files/cuir.wav")
    m_wave = AudioSegment.from_file("files/moustache.wav")
    c_m_wave = AudioSegment.from_file("files/cuir_moustache.wav")
    space_wave = AudioSegment.from_file("files/space.wav")
    blank_wave = AudioSegment.from_file("files/blank.wav")
    overlay = AudioSegment.from_file("files/overlay.wav")

    intro_wave = AudioSegment.from_file("files/intro.wav")

    chall_wave = intro_wave[0:0]
    morse_flag = morse(flag)
    print morse_flag
    counter = 0
    while counter < len(morse_flag):
        bip = morse_flag[counter]
        if bip == '.':
            if counter < len(morse_flag) - 1 and morse_flag[counter+1] == '-':
                chall_wave += c_m_wave
                counter += 1
            else:
                chall_wave += c_wave
        elif bip == '-':
            chall_wave += m_wave
        elif bip == ' ':
            chall_wave += space_wave
        elif bip == '!':
            if ADD_BLANKS:
                chall_wave += blank_wave

        counter += 1


    overlay_wave = repeat_to_length(overlay, len(chall_wave))
    overlay_chall_wave = chall_wave.overlay(overlay_wave)
    full_chall_wave = intro_wave + overlay_chall_wave
    full_chall_wave.export("./challenge.mp4", format="mp4")

if __name__ == '__main__':
    main()
