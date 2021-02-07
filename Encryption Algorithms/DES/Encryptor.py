import numpy as np
from DES import KeyGenerator
from DES import DESEncryptor


class Encryptor():
    
    def __init__(self):
        
        self.keygen=KeyGenerator.KeyGenerator()
        self.des=DESEncryptor.DESEncryptor()
        
    
    def run(self):
        
        while True:
            
            key=input()
            plain=input()
            count=int(input())
            
            subKeys=self.keygen.generateKeys(key)
            
            for i in range(count):
                
                cipher=self.des.encrypt(plain,subKeys)
                plain=cipher
                
            print(cipher[2:])
                