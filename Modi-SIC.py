from tabulate import tabulate
from tkinter import * 
from tkinter import messagebox
import re
import sys


#Storing Instruction Set elements : Opcodes
InSet = open("InstructionSet.txt", "r")
opcode = {}

for line in InSet:
    a = line.split()

    if a[1] == 'm':
        opcode[a[0]] = [a[3], 3]

    else:
        opcode[a[0]] = [a[2], 1]

InSet.close()

#Extracting SIC Program
InTxt = open("in1.txt", "r")
program = []
linum = 2
flagError = 0
flagEnd = 0

#Validating the Start of the program 
a = InTxt.readline().upper().split()
strtAdrs = ""
pName = ""
try:
    if len(a[1]) > 6:
        raise Exception()
    else:
        pName = a[1]


except:
    messagebox.showwarning("Warning", "Program Name Exceeded limit(6 characters)!")
    flagError = 1  

try:
    if a[2] != "START":
        raise Exception()

except:
    messagebox.showwarning("Warning", "Syntax Error: START!")
    flagError = 1  

try:
    if a[3].isnumeric() == False:
        raise Exception()

    strtAdrs = a[3]

    program += [[a[1], a[2], a[3]]]

except:
    messagebox.showwarning("Warning", "Address must be a number!")
    flagError = 1  


#Validating the body of the program and generating Intermediate.txt
labelChk = {}
lblChkToo = []

for line in InTxt:
    a = line.upper().split()

    if len(a) > 1 and a[1][0] != '.':

        for i in range(len(a)):

            if a[i] in opcode and opcode[a[i]][1] == 3:
               
                if a[i - 1].isnumeric():
                    a[i - 1] = ""

                else:
                    try:
                        if a[i - 1] in labelChk:
                            raise Exception()

                        else:
                            labelChk[a[i - 1]] = True

                    except:
                        messagebox.showwarning("Warning", "Repeated Label at line: " + str(linum) +"!")
                        flagError = 1
                    
                if a[i] == "RSUB":
                    program += [[a[i - 1], a[i], ""]]

                else:
                    try:
                        if a[i + 1] == "":
                            raise Exception()

                        else:
                            var = a[i + 1].translate({ord(letter): None for letter in "#"})

                            if var.isnumeric() == False:
                                lblChkToo += [var]

                        program += [[a[i - 1], a[i], a[i + 1]]]

                    except:
                        messagebox.showwarning("Warning", "Label Missing at line: " + str(linum) +"!")
                        flagError = 1
            
            elif a[i] in opcode and opcode[a[i]][1] == 1:

                if a[i - 1].isnumeric():
                    a[i - 1] = ""
                else:
                    labelChk[a[i - 1]] = True
                    

                program += [[a[i - 1], a[i], ""]]

            elif a[i] == 'BYTE':

                try:
                    if a[i - 1].isnumeric():
                        raise Exception()
                    else:
                        try:
                            if a[i - 1] in labelChk:
                                raise Exception()

                            else:
                                labelChk[a[i - 1]] = True

                        except:
                            messagebox.showwarning("Warning", "Repeated Label at line: " + str(linum) +"!")
                            flagError = 1

                except:
                    messagebox.showwarning("Warning", "Label Missing at line: "+ str(linum) +"!")
                    flagError = 1  
                    
                try:
                    match = re.match(r"X[\'|\"]([A-F0-9]{2}\s?)+[\'|\"]", a[i + 1])

                    if match == None:
                        match = re.match(r"C[\'|\"]([A-Z a-z 0-9]\s?)+[\'|\"]", a[i + 1])
                    
                    program += [[a[i - 1], a[i], match.string]]

                except:
                    messagebox.showwarning("Warning", "Invalid Value Of Byte at line: "+ str(linum) +"!")
                    flagError = 1

        
            elif a[i] == 'WORD':

                try:
                    if a[i - 1].isnumeric():
                        raise Exception()

                    else:
                        try:
                            if a[i - 1] in labelChk:
                                raise Exception()

                            else:
                                labelChk[a[i - 1]] = True

                        except:
                            messagebox.showwarning("Warning", "Repeated Label at line: " + str(linum) +"!")
                            flagError = 1

                except:
                    messagebox.showwarning("Warning", "Label Missing at line: "+ str(linum) +"!")
                    flagError = 1  


                try:
                    x = int(a[i + 1])

                    if x > 16777215 or x < -1048576:       #x > FFFFFF or x < F00000  check
                        raise ValueError("Value must be between 16777215 nad -1048576")

                    program += [[a[i - 1], a[i], str(x)]]

                except ValueError:
                    messagebox.showwarning("Warning", "Value at line "+ str(linum) +" must be between 16777215 nad -1048576")
                    flagError = 1

                except:
                    messagebox.showwarning("Warning", "Value at line "+ str(linum) +" must be Numeric!")
                    flagError = 1


            elif a[i] == 'RESB':

                try:
                    if a[i - 1].isnumeric():
                        raise Exception()
                    else:
                        try:
                            if a[i - 1] in labelChk:
                                raise Exception()

                            else:
                                labelChk[a[i - 1]] = True

                        except:
                            messagebox.showwarning("Warning", "Repeated Label at line: " + str(linum) +"!")
                            flagError = 1

                except:
                    messagebox.showwarning("Warning", "Label Missing at line: "+ str(linum) +"!")
                    flagError = 1  

                try:
                    x = int(a[i + 1])

                    program += [[a[i - 1], a[i], str(x)]]

                except:
                    messagebox.showwarning("Warning", "Value at line "+ str(linum) +" must be Numeric!")
                    flagError = 1
                    
            elif a[i] == 'RESW':

                try:
                    if a[i - 1].isnumeric():
                        raise Exception()

                    else:
                        try:
                            if a[i - 1] in labelChk:
                                raise Exception()

                            else:
                                labelChk[a[i - 1]] = True

                        except:
                            messagebox.showwarning("Warning", "Repeated Label at line: " + str(linum) +"!")
                            flagError = 1

                except:
                    messagebox.showwarning("Warning", "Label Missing at line: "+ str(linum) +"!")
                    flagError = 1  

                try:
                    x = int(a[i + 1])

                    program += [[a[i - 1], a[i], str(x)]]

                except:
                    messagebox.showwarning("Warning", "Value at line "+ str(linum) +" must be Numeric!")
                    flagError = 1
                    

            elif a[i] == "END" and i <= 2:

                flagEnd = 1

                if a[i - 1].isnumeric():
                    a[i - 1] = ""

                else:
                    labelChk[a[i - 1]] = True

                try:
                    if a[i + 1].isnumeric() == False:
                        raise Exception()

                except:
                    messagebox.showwarning("Warning", "Address at line "+ str(linum) +" must be Numeric!")
                    flagError = 1

                try:
                    if(a[i + 1] == strtAdrs):
                        program += [[a[i - 1], a[i], a[i + 1]]]

                    else:
                        raise Exception()

                except:
                    messagebox.showwarning("Warning", "Address at End is not equal to address at START!")
                    flagError = 1

    linum = linum + 1   

InTxt.close()

if flagEnd == 0:                                
    program += [["", "END", strtAdrs]]

for strr in lblChkToo:
    try:
        if(strr.find(",X") > -1):
            labelChk[strr[:-2]] 
        else:
            labelChk[strr]

    except:
        messagebox.showwarning("Warning", "Undefined Label:" + strr +"")
        flagError = 1


if flagError == 1:
    messagebox.showwarning("Warning", "Please Correct Errors and Come Back !")
    sys.exit(0)

#Generating File intermediate.txt
Inter = open("intermediate.txt", "w") 
Inter.writelines(tabulate(program,tablefmt="plain"))

#Reading from intermediate.txt
Inter = open("intermediate.txt", "r")

a = Inter.readline().split()
LoCounter = [["", a[0], a[1], a[2]]]

x = int(a[2], 16)

SymbolTable = {}
SArr = []

#Generating Location Counter & Symbol Table
for line in Inter:
    a = line.split()

    if a[0] in opcode:
        if len(a) < 2:
            a += [""]

        if opcode[a[0]][1] == 3:
            LoCounter += [[hex(x)[2:].zfill(4), "", a[0], a[1]]]  
        else:
            LoCounter += [[hex(x)[2:].zfill(4), "", a[0], ""]]  

        x += opcode[a[0]][1]

    elif a[1] in opcode:

        if opcode[a[1]][1] == 3:
            LoCounter += [[hex(x)[2:].zfill(4), a[0], a[1], a[2]]]
        else:
            LoCounter += [[hex(x)[2:].zfill(4), a[0], a[1], ""]]

        SymbolTable[a[0]] = hex(x)[2:].zfill(4)    #Symbol Table Generation
        SArr += [[a[0], hex(x)[2:].zfill(4)]]               
        x += opcode[a[1]][1]

    elif a[0] == 'END':
        LoCounter += [[hex(x)[2:].zfill(4), "", a[0], a[1]]]

    elif a[1] == 'END':
        LoCounter += [[hex(x)[2:].zfill(4),a[0], a[1], a[2]]]

    else:
        
        LoCounter += [[hex(x)[2:].zfill(4), a[0], a[1], a[2]]]
        SymbolTable[a[0]] = hex(x)[2:].zfill(4)
        SArr += [[a[0], hex(x)[2:].zfill(4)]] 
        
        if a[1] == 'BYTE':                          
            if a[2][0] == 'X':
                x += int((len(a[2]) - 3) / 2)

            else:
                x += (len(a[2]) - 3)
        
        elif a[1] == 'WORD':
            x += 3

        elif a[1] == 'RESB':
            x += int(a[2])

        elif a[1] == 'RESW':
            x += (int(a[2]) * 3)                    

Inter.close()

passOne = open("out_pass1.txt", "w") 
passOne.writelines(tabulate(LoCounter,tablefmt="plain"))
passOne.close()

symbolTable = open("symbTable.txt", "w")                   
symbolTable.writelines(tabulate(SArr,tablefmt="plain"))                     
symbolTable.close()


Inter = open("intermediate.txt", "r")

a = Inter.readline().split()
objCode = [[a[0], a[1], a[2], ""]]

arrForHTE = []
#Generating Object Code
for line in Inter:
    a = line.split()

    if a[0] in opcode and opcode[a[0]][1] == 3:

        if a[0] == 'RSUB':
            a += [""]                                     
            objCode += [["", a[0], a[1], opcode[a[0]][0] + str(strtAdrs)]]
        
        elif(a[1].find(",X") == -1 and a[1].find("#") == -1):
            
            objCode += [[ "", a[0], a[1], opcode[a[0]][0] + SymbolTable[a[1]]]]
        
        elif (a[1].find(",X") > -1):
            modCode = opcode[a[0]][0] + SymbolTable[a[1][:-2]]
            modCode = int(modCode, 16)
            modCode = bin(modCode)[2:].zfill(24)  
            modCode = list(modCode)
            modCode[8] = '1'                
            modCode = int(''.join(modCode), 2)
            modCode = hex(modCode)[2:].upper().zfill(6)
            objCode += [[ "", a[0], a[1], modCode]]

        else:
            imm = list(bin(int(opcode[a[0]][0], 16))[2:].zfill(8))
            imm[7] = '1'
            imm = ''.join(imm)
            imm = int(imm, 2)
            imm = hex(imm)[2:].zfill(2)
            
            if(a[1][1:].isnumeric()):
                objCode += [[ "", a[0], a[1], imm + hex(int(a[1][1:]))[2:].zfill(4)]]

            else:
                objCode += [[ "", a[0], a[1], imm + SymbolTable[a[1][1:]]]]


    elif len(a) > 1 and a[1] in opcode and opcode[a[1]][1] == 3:

        if a[1] == 'RSUB': 
            a += [""]                                     
            objCode += [[a[0], a[1], a[2], opcode[a[0]][0] + str(strtAdrs)]]

        elif(a[2].find(",X") == -1 and a[2].find("#") == -1):

            objCode += [[a[0], a[1], a[2], opcode[a[1]][0] + SymbolTable[a[2]]]]
        
        elif (a[2].find(",X") > -1):

            modCode = opcode[a[1]][0] + SymbolTable[a[2][:-2]]
            modCode = int(modCode, 16)
            modCode = bin(modCode)[2:].zfill(24)     
            modCode = list(modCode)
            modCode[8] = '1'             
            modCode = ''.join(modCode)
            modCode= int(modCode, 2)
            modCode = hex(modCode)[2:].zfill(2)
            objCode += [[a[0], a[1], a[2], modCode]]

        else: 

            imm = list(bin(int(opcode[a[1]][0], 16))[2:].zfill(8))
            imm[7] = '1'
            imm = ''.join(imm)
            imm = int(imm, 2)
            imm = hex(imm)[2:].zfill(2)

            if(a[2][1:].isnumeric()):
                objCode += [[a[0], a[1], a[2], imm + hex(int(a[2][1:]))[2:].zfill(4)]]

            else:
                objCode += [[a[0], a[1], a[2], imm + SymbolTable[a[2][1:]]]]

    elif a[0] in opcode and opcode[a[0]][1] == 1:
        objCode += [[ "", a[0], "", opcode[a[0]][0]]]   
                                                                
    elif len(a) > 1 and a[1] in opcode and opcode[a[1]][1] == 1:
        if len(a) > 2:                    
            objCode += [[a[0], a[1], a[2], opcode[a[1]][0]]]
        else:                    
            objCode += [[a[0], a[1], "", opcode[a[1]][0]]]
               
    else:
        if a[1] == 'BYTE':

            if a[2][0] == 'X':
                objCode += [[a[0], a[1], a[2], a[2].translate({ord(letter): None for letter in "X'"})]]

            else:
                temp_str = a[2].translate({ord(letter): None for letter in "C'"})
                c = ""

                for i in temp_str:
                    c += hex(ord(i))[2:]

                objCode += [[a[0], a[1], a[2], c]]
        
        elif a[1] == 'WORD':
            objCode += [[a[0], a[1], a[2], hex(int(a[2]))[2:].zfill(6)]]

        elif a[1] == 'RESB':
            objCode += [[a[0], a[1], a[2], ""]]

        elif a[1] == 'RESW':
            objCode += [[a[0], a[1], a[2], ""]]                    

        elif a[0] == 'END':                                      
            objCode += [["", a[0], a[1]]]

        elif a[1] == 'END':                                       
            objCode += [[a[0], a[1], a[2]]]
       
passTwo = open("out_pass2.txt", "w") 
passTwo.writelines(tabulate(objCode,tablefmt="plain"))
passTwo.close()

Inter.close()

WorB = ["WORD", "BYTE"]
r = ["RESW","RESB"]

for strr in objCode:
    
    for i in range(0, 2):
        if (strr[i] in opcode) or (strr[i] in WorB):
            arrForHTE += [["" ,strr[i], strr[len(strr) - 1]]]

        elif(strr[i] in r):
            arrForHTE += [["" ,strr[i], ""]]


Inter = open("out_pass1.txt", "r")

a = Inter.readline().split()

lastAdrs = ""

for i in range (0, len(arrForHTE) - 1):

    a = Inter.readline().split()

    arrForHTE[i][0] = a[0].zfill(6)

    lastAdrs = a[0]

Inter.close()

#print(arrForHTE)

size = hex(int(lastAdrs, 16) - int(strtAdrs, 16))[2:].zfill(6)

HTERecord = [["H", pName.zfill(6), strtAdrs.zfill(6), size]] 

temp = ["T", "", ""]

count = 0

for strr in arrForHTE:

    if(strr[1] in r or (count + 3 > 30)) and temp != ["T", "", ""]:
        temp[2] = hex(count)[2:].zfill(2)
        HTERecord += [temp]
        temp = ["T", "", ""]
        count = 0

    if (strr[1] in opcode) or (strr[1] in WorB):
        temp += [strr[2]]
        count = count + int(len(strr[2]) / 2)

if temp != ["T", "", ""]:
    temp[2] = hex(int(count))[2:].zfill(2)
    HTERecord += [temp]

for strr in HTERecord:

    for srt in arrForHTE:

        if strr[3] == srt[2]:
            strr[1] = srt[0]


HTERecord += [["E", lastAdrs.zfill(6), strtAdrs.zfill(6)]] 

Inter = open("HTE.txt", "w")
Inter.writelines(tabulate(HTERecord,tablefmt="plain"))
Inter.close()
print(HTERecord)