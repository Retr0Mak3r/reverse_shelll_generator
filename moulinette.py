#! /usr/bin/python
# Shellcode Tester

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


shellcode = input("Hello ! Collez votre shellcode ici, format '\\xde\\xad\\xbe\\xef' :\n")
if "\\x00" in shellcode:
    print(bcolors.FAIL + "NULL BYTE DETECTED" + bcolors.ENDC)
else :
    print(bcolors.OKGREEN + "No null byte detected" + bcolors.ENDC)
if "\\x48\\xbb\\x2f\\x2f\\x62\\x69\\x6e\\x2f" in shellcode:
    print(bcolors.FAIL + "CALL TO '/bin/*' DETECTED" + bcolors.ENDC)
else :
    print(bcolors.OKGREEN + "No '/bin/*' call detected" + bcolors.ENDC)
if "\\xb0\\x2a" in shellcode:
    print(bcolors.FAIL + "Seems like you're trying to connect a socket" + bcolors.ENDC)
else :
    print(bcolors.OKGREEN + "No connection call detected" + bcolors.ENDC)
if "\\x66\\x68\\x23\\x1d" in shellcode:
    print(bcolors.FAIL + "Hey, i know this port" + bcolors.ENDC)
else:
    print(bcolors.OKGREEN + "No classical port detected" + bcolors.ENDC)