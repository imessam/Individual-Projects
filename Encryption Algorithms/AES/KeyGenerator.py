import numpy as np

class KeyGenerator():
    
    def __init__(self):
        
        self.init_sbox()
        self.init_rcons()
        
        
    def init_sbox(self):
        
        self.sbox=np.array([
            ["63","7c","77","7b","f2","6b","6f","c5","30","01","67","2b","fe","d7","ab","76"],
            ["ca","82","c9","7d","fa","59","47","f0","ad","d4","a2","af","9c","a4","72","c0"],
            ["b7","fd","93","26","36","3f","f7","cc","34","a5","e5","f1","71","d8","31","15"],
            ["04","c7","23","c3","18","96","05","9a","07","12","80","e2","eb","27","b2","75"],
            ["09","83","2c","1a","1b","6e","5a","a0","52","3b","d6","b3","29","e3","2f","84"],
            ["53","d1","00","ed","20","fc","b1","5b","6a","cb","be","39","4a","4c","58","cf"],
            ["d0","ef","aa","fb","43","4d","33","85","45","f9","02","7f","50","3c","9f","a8"],
            ["51","a3","40","8f","92","9d","38","f5","bc","b6","da","21","10","ff","f3","d2"],
            ["cd","0c","13","ec","5f","97","44","17","c4","a7","7e","3d","64","5d","19","73"],
            ["60","81","4f","dc","22","2a","90","88","46","ee","b8","14","de","5e","0b","db"],
            ["e0","32","3a","0a","49","06","24","5c","c2","d3","ac","62","91","95","e4","79"],
            ["e7","c8","37","6d","8d","d5","4e","a9","6c","56","f4","ea","65","7a","ae","08"],
            ["ba","78","25","2e","1c","a6","b4","c6","e8","dd","74","1f","4b","bd","8b","8a"],
            ["70","3e","b5","66","48","03","f6","0e","61","35","57","b9","86","c1","1d","9e"],
            ["e1","f8","98","11","69","d9","8e","94","9b","1e","87","e9","ce","55","28","df"],
            ["8c","a1","89","0d","bf","e6","42","68","41","99","2d","0f","b0","54","bb","16"]
        ])
        
        
        
    def init_rcons(self):
        
        self.rcon=np.array([
            ["01","00","00","00"],
            ["02","00","00","00"],
            ["04","00","00","00"],
            ["08","00","00","00"],
            ["10","00","00","00"],
            ["20","00","00","00"],
            ["40","00","00","00"],
            ["80","00","00","00"],
            ["1b","00","00","00"],
            ["36","00","00","00"]
        ])
        
        
        
    def hexToBin(self,key,noOfBits):
        
        scale = 16 ## equals to hexadecimal
        num_of_bits = noOfBits

        binKey=bin(int(key, scale))[2:].zfill(num_of_bits)
        
        return (binKey)
    
    
    
    def binToHex(self,hx):
        
        return hex(int(hx,2))[2:].zfill(2)
    
    
    def xor(self,b1,b2):
        
        
        out=int(b1,2) ^ int(b2,2)
        out=bin(out)[2:].zfill(len(b1))
        
        return out
    
    
    def subByte(self,word):
        
        new_word=[]
        
        for byte in word:
            
            row=int(byte[0],16)
            col=int(byte[1],16)
            
            new_word.append(self.sbox[row,col])
            
        return new_word
    
    
    def shiftRight(self,word):
        
        new_word=word.tolist()
        new_word.append(new_word[0])
        new_word.pop(0)
        
        return new_word
    
    
    def generateW0(self,w0,w3,rcon):
        
        
        w3=self.shiftRight(w3)
        w3=self.subByte(w3)
        w0_bin=[self.hexToBin(w,8) for w in w0]
        w3_bin=[self.hexToBin(w,8) for w in w3]
        rcon_bin=[self.hexToBin(r,8) for r in rcon]
        
        z=[self.xor(w3_bin[i],rcon_bin[i]) for i in range(len(w3_bin))]
        w0_new=[self.binToHex(self.xor(w0_bin[i],z[i])) for i in range(len(w0_bin))]

        return w0_new
    
    
    
    def generateNextKey(self,key,rcon):
        
        next_key=[]
        word=[] 
        w0=key[:,0]
        w3=key[:,3]
        
        word=self.generateW0(w0,w3,rcon)
        next_key.append(word)
        
        for i in range(key.shape[0]-1):
            
            word_bin=[self.hexToBin(w,8) for w in word]
            key_bin=[self.hexToBin(w,8) for w in key[:,i+1]]
            word=[self.binToHex(self.xor(word_bin[i],key_bin[i])) for i in range(len(word_bin))]
            next_key.append(word)
            
        return np.transpose(np.array(next_key))
    
    
    
    def generateRoundKeys(self,firstKey):
        
        roundKeys=[]
        prev_key=firstKey
        roundKeys.append(firstKey)
        
        for i in range(10):
            
            next_key=self.generateNextKey(prev_key,self.rcon[i,:])
            roundKeys.append(next_key)
            prev_key=next_key
            
        return np.array(roundKeys)   