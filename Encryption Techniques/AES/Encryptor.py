import numpy as np
from AES import KeyGenerator
from AES import AESEncryptor


class Encryptor():
    
    def __init__(self):
        
        self.keygen=KeyGenerator.KeyGenerator()
        self.aes=AESEncryptor.AESEncryptor()
        
        
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
        
    
    def run(self):
        
        while True:
            
            key=self.convertToMatrix(input())
            plain=self.convertToMatrix(input())
            
            roundKeys=self.keygen.generateRoundKeys(key)
            cipher=self.aes.encrypt(plain,roundKeys)
                
            print(self.aes.convertToString(cipher))
                