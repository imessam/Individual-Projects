import numpy as np

class KeyGenerator():
    
    def __init__(self):
        
        self.init_permut1()
        self.init_permut2()
        self.init_shiftTable()
        
    def init_permut1(self):
        
        permut1=[
                [57,49,41,33,25,17,9],
                [1,58,50,42,34,26,18],
                [10,2,59,51,43,35,27],
                [19,11,3,60,52,44,36],
                [63,55,47,39,31,23,15],
                [7,62,54,46,38,30,22],
                [14,6,61,53,45,37,29],
                [21,13,5,28,20,12,4]
                                    ]
        self.permut1=np.array(permut1)
        
        
        
        
    def init_permut2(self):
        
        permut2=[
            [14,17,11,24,1,5],
            [3,28,15,6,21,10],
            [23,19,12,4,26,8],
            [16,7,27,20,13,2],
            [41,52,31,37,47,55],
            [30,40,51,45,33,48],
            [44,49,39,56,34,53],
            [46,42,50,36,29,32]
        ]
        self.permut2=np.array(permut2)
        
        
        
    def init_shiftTable(self):
        
        self.shiftTable=[1,1,2,2
                         ,2,2
                         ,2,2
                         ,1,2
                         ,2,2
                         ,2,2
                         ,2,1]
        
        
        
        
    def hexToBin(self,key,noOfBits):
        
        scale = 16 ## equals to hexadecimal
        num_of_bits = noOfBits

        binKey=bin(int(key, scale))[2:].zfill(num_of_bits)
        return (binKey)
    
    
    
    def permute(self,key,table):
        
        new_key=""
        
        for row in range(table.shape[0]):
            for col in range(table.shape[1]):
                
                new_key+=(key[table[row,col]-1])
                
        return new_key
    
    
    def shiftLeft(self,key,value):
        
        new_key=[key[np.mod(i+value,len(key))] for i in range(len(key))]
        
        return new_key
        
        
    
    def firstPermute(self,key):
        
        new_key=self.permute(key,self.permut1)
        
        return new_key
    
    
    def splitKey(self,key):
        
        mid=int(len(key)/2)
                
        c0=key[0:mid]
        d0=key[mid:]
        
        return c0,d0
    
    
    def shiftLeftKeys(self,c0,d0):
        
        row=[c0,d0]
        keys=[]
        
        for shift in self.shiftTable:
            
            c=self.shiftLeft(row[0],shift)
            d=self.shiftLeft(row[1],shift)
            row=[c,d]
            keys.append(row)
            
        return np.array(keys)
    
    
    def concatenateKeys(self,keys):
        
        new_keys=[]
        
        for row in range(keys.shape[0]):
            
            c=keys[row,0,:].tolist()
            d=keys[row,1,:].tolist()
            c.extend(d)
            new_keys.append(c)
            
        return np.array(new_keys)
            
    
    def secondPermute(self,keys):
        
        new_keys=[]
        
        for row in range(keys.shape[0]):
            
            new_key=self.permute(keys[row,:].tolist(),self.permut2)
            new_keys.append(new_key)
            
        return np.array(new_keys)
    
    def printKeys(self,keys):
        
        print("Sub Keys : ")
        
        for row in range(keys.shape[0]):
            
            print(f"K{row+1}")
            key=keys[row]
            p=""
            
            for i in range(len(key)):
                if i%6==0:
                    p+="  "
                p+=key[i]
                
            print(p)
    
    
    def generateKeys(self,hexKey):
        
        key=self.hexToBin(hexKey,64)
        key=self.firstPermute(key)
        c0,d0=self.splitKey(key)
        keys=self.shiftLeftKeys(c0,d0)
        keys=self.concatenateKeys(keys)
        subKeys=self.secondPermute(keys)
        #self.printKeys(subKeys)
        
        return subKeys
        
        