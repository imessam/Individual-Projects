import numpy as np
import Classic_Encryptions.Caesar as cs
import Classic_Encryptions.Hill as hl
import Classic_Encryptions.PlayFair as pl
import Classic_Encryptions.Vigenere as vig
import Classic_Encryptions.Vernam as vr
import DES.DESEncryptor as des
import DES.KeyGenerator as desKeygen
import AES.AESEncryptor as aes
import AES.KeyGenerator as aesKeygen



class Encryptor():
    
    def __init__(self):
        
        self.encryptors=[cs.Caesar(),hl.Hill(),pl.PlayFair(),vr.Vernam(),vig.Vigenere(),des.DESEncryptor(),aes.AESEncryptor()]
        self.desKeygen=desKeygen.KeyGenerator()
        self.aesKeygen=aesKeygen.KeyGenerator()
        
    def convertToMatrix(self,st):
    
        matrix=[]
        elem=""
    
        for i in range(len(st)):
        
            if (i%2==0) and (i!=0):
            
                matrix.append(elem)
                elem=""
            
            elem+=st[i]
        
        matrix.append(elem)
    
        return np.transpose(np.reshape(np.array(matrix),(4,4)))
        
        
    
    def setEncryptor(self):
        
        print("Encrypt with : 1- Caesar cipher \n 2- Hill cipher \n 3- PlayFair cipher \n 4- Vernam cipher \n 5- Vigenere cipher \n 6- DES \n 7- AES \n 0- Exit ")
        self.index=int(input("Enter a number from 0-7 : ")) 
        
        if(self.index>0):
            self.encryptor=self.encryptors[self.index-1]
    
    
    def setPlainText(self):
                        
        self.plain=input("Enter the plain text : ")
        self.plain=self.plain.strip(" ")
        
        if(self.index==7):
        
            self.plain=self.convertToMatrix(self.plain)
    
    def setKey(self):
        
        self.key=None
                             
        if(self.index==2):
                             
            rows=int(input("Enter number of rows in the key matrix : "))
            cols= int(input("Enter number of columns in the key matrix : "))
            print("Enter the elements in the matrix in this form : ex : 2x2 matrix \[\[1,2\],\[3,4\]\] -> your input :  1 2 3 4")
            inp=input("Enter the key : ")
            inp=inp.split(" ")
            inp=np.array(inp,dtype=np.int)
            self.key=np.reshape(inp,(rows,cols))
        
        elif(self.index==5):
                             
            mode=bool(int(input("Enter mode of encryptions 0:repeating or auto:1 : ")))
            key=input("Enter the key : ")
            self.key=[key,mode]
            
        elif(self.index==6):
        
            key=input("Enter the key : ")
            self.key=self.desKeygen.generateKeys(key)
            
        elif(self.index==7):
            
            key=input("Enter the key : ")
            self.key=self.aesKeygen.generateRoundKeys(self.convertToMatrix(key))
        
        else  :
            
            self.key=input("Enter the key : ")
        
    def encrypt(self):
                             
            cipher=self.encryptor.encrypt(self.plain,self.key)
            
            if (self.index==7):
                cipher=self.encryptor.convertToString(cipher)
                
            return cipher
    
    def run(self):
        
        self.index=1
        
        while(True):
            
            self.setEncryptor()
            if not(self.index):
                print("Qutting....")
                break
            self.setPlainText()
            self.setKey()
            print(self.encrypt())
        