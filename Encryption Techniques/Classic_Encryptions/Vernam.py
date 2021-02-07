import numpy as np
import os


class Vernam():
    
    def __init__(self):
        
        self.lettersDict={}
        self.lettersList=["A","B","C","D","E","F","G","H","I","J","K","L",
            "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        self.init_dict()
        
    def init_dict(self):
        
        for i,letter in enumerate(self.lettersList):
            
            self.lettersDict[letter]=i
            
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
            
            
    def encryptFromFile(self,filePath,key):
        
        plains=self.readFile(os.path.join(filePath,"vernam_plain.txt"))
        
        ciphers=[]
        
        for plain in plains:
            
            ciphers.append(self.encrypt(plain,key))
            
         
        self.saveFile(os.path.join(filePath,f"vernam_ciphers_{key}.txt"),ciphers)
        
        return ciphers
    
        
            
    def encrypt(self,plain,key):
            
        cipher=""
        
        for i in range(len(plain)):
                  
            plainIndex=self.lettersDict[plain[i].upper()]
            keyIndex=self.lettersDict[key[i].upper()]
            sub=np.mod(plainIndex+keyIndex,26)
            cipher+=self.lettersList[sub]
            
        return cipher.lower()
    

        