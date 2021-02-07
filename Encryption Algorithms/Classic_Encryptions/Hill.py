import numpy as np
import os

class Hill():
    
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
        
            
    def transformToIndexes(self,text,key):
        
        textMatrices=[]
        textList=[]

        for i,letter in enumerate(text):
            
            if i%key==0:
                
                textMatrices.append(np.array(textList))
                textList=[]
                
            textList.append(self.lettersDict[letter.upper()])
        
        count=key-len(textList)
        if(count!=0):
            for i in range(count):
                textList.append(self.lettersDict["Z"])
                
        textMatrices.append(np.array(textList))
        textMatrices.pop(0)
        textMatrices=np.array(textMatrices)
        
        
        return textMatrices
    
    
    def transformToText(self,textMatrices):
        
        text=""
        
        for col in range(textMatrices.shape[1]):
            
            for row in range(textMatrices.shape[0]):
                
                text+=self.lettersList[textMatrices[row,col]]
        
        return text.lower()
    
        
    
    def encrypt(self,plain,key):
        
        plainMatrices=self.transformToIndexes(plain,key.shape[0])
                        
        cypherMatrices=np.mod(np.dot(key,plainMatrices.T),26)
        
        cypher=self.transformToText(cypherMatrices)
        
        return cypher
    
    
    def encryptFromFile(self,filePath,key):
        
        plains=self.readFile(os.path.join(filePath,f"hill_plain_{key.shape[0]}x{key.shape[1]}.txt"))
        
        ciphers=[]
        
        for plain in plains:
            
            ciphers.append(self.encrypt(plain,key))
            
         
        self.saveFile(os.path.join(filePath,f"hill_ciphers_{key.shape[0]}x{key.shape[1]}.txt"),ciphers)
        
        return ciphers