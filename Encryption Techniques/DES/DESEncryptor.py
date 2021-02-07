import numpy as np

class DESEncryptor():
    
    def __init__(self):
        
        self.init_initialPermut()
        self.init_expansionTable()
        self.init_finalPermut()
        self.init_sboxes()
        self.init_revPerm()
        
        
     
    
    def init_initialPermut(self):
        
        permut=[
                [58,50,42,34,26,18,10,2],
                [60,52,44,36,28,20,12,4],
                [62,54,46,38,30,22,14,6],
                [64,56,48,40,32,24,16,8],
                [57,49,41,33,25,17, 9,1],
                [59,51,43,35,27,19,11,3],
                [61,53,45,37,29,21,13,5],
                [63,55,47,39,31,23,15,7]
                                    ]
        self.initialPermut=np.array(permut)
        
        
        
        
        
    def init_expansionTable(self):
        
        expan=[
            [32,1,2,3,4,5],
            [4,5,6,7,8,9],
            [8,9,10,11,12,13],
            [12,13,14,15,16,17],
            [16,17,18,19,20,21],
            [20,21,22,23,24,25],
            [24,25,26,27,28,29],
            [28,29,30,31,32,1]
        ]
        
        self.expTable=np.array(expan)
        
        
        
    def init_finalPermut(self):
        
        permut=[
            [16,7,20,21],
            [29,12,28,17],
            [1,15,23,26],
            [5,18,31,10],
            [2,8,24,14],
            [32,27,3,9],
            [19,13,30,6],
            [22,11,4,25]
        ]
        
        self.finalPermute=np.array(permut)
        
        
        
        
    
    def init_sboxes(self):
                
        s1=np.array([
                    [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
                    [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
                    [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
                    [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
        ])
        
        s2=np.array([
            [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
            [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
            [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
            [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
        ])
        
        s3=np.array([
            [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
            [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
            [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
            [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
        ])
        
        s4=np.array([
            [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
            [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
            [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
            [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
        ])
        
        s5=np.array([
            [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
            [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
            [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
            [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
        ])
        
        s6=np.array([
            [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
            [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
            [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
            [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
        ])
        
        s7=np.array([
            [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
            [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
        ])
        
        s8=np.array([
            [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
            [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
            [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
            [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
        ])
        
        self.sboxes=np.array([s1,s2,s3,s4,s5,s6,s7,s8])
        
        
        
        
    def init_revPerm(self):
        
        self.revPerm=np.array([
            [40,8,48,16,56,24,64,32],
            [39,7,47,15,55,23,63,31],
            [38,6,46,14,54,22,62,30],
            [37,5,45,13,53,21,61,29],
            [36,4,44,12,52,20,60,28],
            [35,3,43,11,51,19,59,27],
            [34,2,42,10,50,18,58,26],
            [33,1,41,9,49,17,57,25]
        ])
        
        
        
    def hexToBin(self,msg,noOfBits):
        
        scale = 16 ## equals to hexadecimal
        num_of_bits = noOfBits

        msg=bin(int(msg, scale))[2:].zfill(num_of_bits)
        
        return (msg)
        
        
        
    def permute(self,message,table):
        
        new_message=""
        
        for row in range(table.shape[0]):
            for col in range(table.shape[1]):
                
                new_message+=(message[table[row,col]-1])
                
        return new_message
    
    
    
    def initPermute(self,message):
        
        new_message=self.permute(message,self.initialPermut)
        
        return new_message
    
    
    def splitMessage(self,message):
        
        mid=int(len(message)/2)
                
        L0=message[0:mid]
        R0=message[mid:]
        
        return L0,R0
    
    def expand(self,message):
        
        new_message=self.permute(message,self.expTable)
        
        return new_message
    
    
    
    def splitBits(self,message):
        
        bits=""
        new_message=[]
        
        for i in range(len(message)):
            
            if i%6==0:
                if i !=0:
                    new_message.append(bits)
                    bits=""
                    
            bits+=message[i]
            
        new_message.append(bits)
            
        return np.array(new_message)
    
    
    
    
    def sboxing(self,message):
        
        new_message=""
        
        for i in range(len(message)):
            
            s=self.sboxes[i]
            
            bit0=message[i][0]
            bit5=message[i][5]
            
            row=int(bit0+bit5,2)
            col=int(message[i][1:5],2)
            
            new_bits=bin(s[row,col])[2:].zfill(4)
            new_message+=(new_bits)
            
        return new_message
    
    
    def finalPerm(self,message):
        
        new_message=self.permute(message,self.finalPermute)
        
        return new_message
            
            
    def xor(self,b1,b2):
        
        out=int(b1,2) ^ int(b2,2)
        out=bin(out)[2:].zfill(len(b1))
        
        return out
    
    
    
    def function(self,R,key):
        
        R_next=self.expand(R)
        out=self.xor(R_next,key)
        bits=self.splitBits(out)
        sbits=self.sboxing(bits)
        fOut=self.finalPerm(sbits)
        
        return fOut
    
    
    
    def encrypt(self,message,keys):
        
        
        message=self.hexToBin(message,64)
        msg=self.initPermute(message)
        L_prev,R_prev=self.splitMessage(msg)
        
        
        
        for i in range(16):
            
            L=R_prev
            f=self.function(R_prev,keys[i])
            R=self.xor(f,L_prev)
            R_prev=R
            L_prev=L
            
        RL=R+L
        cipher=self.permute(RL,self.revPerm)
            
        return hex(int(cipher,2))
    
    
    def decrypt(self,cipher,keys):
        
        
        cipher=self.hexToBin(cipher,64)
        ciph=self.initPermute(cipher)
        L_prev,R_prev=self.splitMessage(ciph)
        
        
        
        for i in range(16):
            
            L=R_prev
            f=self.function(R_prev,keys[(15-i)])
            R=self.xor(f,L_prev)
            R_prev=R
            L_prev=L
            
        RL=R+L
        plain=self.permute(RL,self.revPerm)
            
        return hex(int(plain,2))
    