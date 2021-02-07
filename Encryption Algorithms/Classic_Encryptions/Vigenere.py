import numpy as np
import os


class Vigenere():
    
    def __init__(self):
        
        self.lettersDict={}
        self.lettersList=["A","B","C","D","E","F","G","H","I","J","K","L",
            "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.init_dict()
        self.matrix=self.init_matrix()
        
    
    def init_dict(self):
        
        for i,letter in enumerate(self.lettersList):
            
            self.lettersDict[letter]=i
        
    def init_matrix(self):
        
        row=[]
        matrix=[]
        
        for i in range(len(self.lettersList)):
            
            for j in range(len(self.lettersList)):
                
                row.append(self.lettersList[np.mod(i+j,26)])
            
            matrix.append(row)
            row=[]
            
        return np.array(matrix,dtype=object)
    
    
    def readFile(self,filePath):
        
        lines=""
        f=open(filePath,'r')
        
        for line in f:
            
            lines+=line
            
        f.close()
        
        lines=lines.split("\n")
        
        return lines
    
    
    def saveFile(self,savePath,text):
        
        f=open(savePath,"x")
            
        for line in text:
                
            f.write(line)
            f.write("\n")
                
        f.close()
            
    
    
    
    
    def repeatKey(self,key,plain):
        
        keyRepeated=""
        
        for i in range(len(plain)):
            
            if len(keyRepeated)==len(plain):
                break
            
            keyRepeated+=key[np.mod(i,len(key))]
        
        return keyRepeated.upper()
    
    def autoKey(self,key,plain):
        
        autoKey=key
        
        for i in range(len(plain)):
            
            if(len(autoKey)==len(plain)):
                break
                
            autoKey+=(plain[np.mod(i,len(plain))])
            
        return autoKey.upper()
        
            
    
    def encrypt(self,plain,keyList):
        
        key=keyList[0]
        mode=keyList[1]
        
        if(mode):
            key=self.autoKey(key,plain)
        else:
            key=self.repeatKey(key,plain)
                   
        cipher=""
            
        for i in range(len(plain)):
            
            row=self.lettersDict[key[i]]
            col=self.lettersDict[plain[i].upper()]
            
            cipher+=self.matrix[row,col]
        
        return str(cipher).strip("\[\]\'\'").lower()
    
    
    def encryptFromFile(self,filePath,keyMode):
        
        plains=self.readFile(os.path.join(filePath,"vigenere_plain.txt"))
        
        ciphers=[]
        
        for plain in plains:
            
            ciphers.append(self.encrypt(plain,keyMode[0],keyMode[1]))
            
         
        self.saveFile(os.path.join(filePath,f"vigenere_ciphers_{keyMode[0]}.txt"),ciphers)
        
        return ciphers
            
    