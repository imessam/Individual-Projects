import numpy as np
import os



class PlayFair():
    
    def __init__(self):
        
        self.lettersDict={}
        self.lettersList=["A","B","C","D","E","F","G","H","I","K","L",
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
      
    
            
    def update_dict(self,tempList):
        
        tempDict={}
        
        for i,letter in enumerate(tempList):
            
            tempDict[letter]=i
            
        return tempDict
    
    
    def unique(self,list1): 
  
        # intilize a null list 
        unique_list = [] 
      
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x) 
                
        return unique_list
    
    
    
    def splitPlain(self,plain):
        
        plainList=[]
        split=""
        prev=""
        count=0
        i=0
        
        while i != len(plain):
           
            nxt=plain[i]
            
            if count%2==0:
                
                plainList.append(split)
                split=""
             
            if prev==nxt:
                nxt="X"
                i-=1
             
            if(nxt.lower()=="j"):
                nxt="i"
            split+=nxt.upper()
            prev=nxt
            
            count+=1
            i+=1
            
        if len(split)!=2:
            split+="X"
        
        plainList.append(split)    
        plainList.pop(0)
        
        return plainList
    
            
    def createPlayFairMatrix(self,key):
        
        tempLetters=self.lettersList.copy()  
        tempDict=self.update_dict(tempLetters)
        playFairMatrix=[]
        key=self.unique(list(key.upper()))  
        
        
        for letter in key:
            tempLetters.pop(tempDict[letter.upper()])
            tempDict=self.update_dict(tempLetters)
                
        key.extend(tempLetters)   
        playFairMatrix=np.array(key,dtype=object)
        playFairMatrix=np.reshape(playFairMatrix,(5,5))
        
        return playFairMatrix
    
    
    def encrypt(self,plain,key):
        
        playFairMatrix=self.createPlayFairMatrix(key)
        plainList=self.splitPlain(plain)

        
        cipher=""
        
        for pl in plainList:
            
            cord0=np.where(playFairMatrix==pl[0])
            cord1=np.where(playFairMatrix==pl[1])
            
            if(cord0[0]==cord1[0]):
                new_cord0=[cord0[0],np.mod(cord0[1]+1,5)]
                new_cord1=[cord1[0],np.mod(cord1[1]+1,5)]
                
            elif(cord0[1]==cord1[1]):
                new_cord0=[np.mod(cord0[0]+1,5),cord0[1]]
                new_cord1=[np.mod(cord1[0]+1,5),cord1[1]]
                
            else: 
                new_cord0=[cord0[0],cord1[1]]
                new_cord1=[cord1[0],cord0[1]]
            
            cipher+=playFairMatrix[new_cord0[0],new_cord0[1]]
            cipher+=playFairMatrix[new_cord1[0],new_cord1[1]]
            
        return str(cipher).strip("\[\]\'\'").lower()
    
    
    def encryptFromFile(self,filePath,key):
        
        plains=self.readFile(os.path.join(filePath,"playfair_plain.txt"))
        
        ciphers=[]
        
        for plain in plains:
            
            ciphers.append(self.encrypt(plain,key))
            
         
        self.saveFile(os.path.join(filePath,f"playfair_ciphers_{key}.txt"),ciphers)
        
        return ciphers      
            
            
        