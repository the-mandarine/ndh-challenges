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
    printf("\n");
}

int main(int argc, char* argv[]) {
    char xflag[41] = {52, 10, 56, 112, 97, 42, 102, 67, 88, 67, 8, 16, 82, 76, 84, 28, 87, 28, 83, 30, 2, 25, 6, 72, 4, 28, 81, 25, 6, 68, 9, 64, 11, 23, 89, 19, 91, 18, 12, 23};
    if (argc != 2) {
        printf("Usage %s <flag>\n", argv[0]);
        return 1;
    }
    encrypt("zzzzzzzzzz", argv[1]);
    if (strcmp(argv[1], xflag)) {
        printf("You're wrong.\n");
    } else {
        printf("You're right.\n");
    }
    return 0;
}
