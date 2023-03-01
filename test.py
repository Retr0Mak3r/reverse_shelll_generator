#/usr/bin/env python3

from random import randint as r


def verifOffus(binBashHexa):
    for i in range(0,18,2):
        if i == 0 :
                continue
        
        sub ="0x"+binBashHexa[i] + binBashHexa[i+1]
        numInHex = int(sub,16)
        if numInHex == int("0x00",16) or numInHex == int("0xff",16) :
            return False
    return True


def offus(string4Payload):
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
    #print ("Random = ", rand, type(rand) )

    newString = "0x"

    for i in range(0,16,2):
        if i == 0 :
                continue
        
        sub = string4Payload[i] + string4Payload[i+1]
        numInHex = int(sub,16) + rand
        newString = newString + str(numInHex)
    
    return rand

print(offus("0x68732f0069622f2f"))