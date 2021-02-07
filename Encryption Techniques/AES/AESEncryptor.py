import numpy as np

class AESEncryptor():
    
    
    def __init__(self):
        
        self.init_sbox()
        self.init_invsbox()
        self.init_mixcolums()
        self.init_invmixcolums()
        
        
        
        
    
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
        
        
    def init_invsbox(self):
        
        self.invsbox=np.array([
            ["52","09","6a","d5","30","36","a5","38","bf","40","a3","9e","81","f3","d7","fb"],
            ["7c","e3","39","82","9b","2f","ff","87","34","8e","43","44","c4","de","e9","cb"],
            ["54","7b","94","32","a6","c2","23","3d","ee","4c","95","0b","42","fa","c3","4e"],
            ["08","2e","a1","66","28","d9","24","b2","76","5b","a2","49","6d","8b","d1","25"],
            ["72","f8","f6","64","86","68","98","16","d4","a4","5c","cc","5d","65","b6","92"],
            ["6c","70","48","50","fd","ed","b9","da","5e","15","46","57","a7","8d","9d","84"],
            ["90","d8","ab","00","8c","bc","d3","0a","f7","e4","58","05","b8","b3","45","06"],
            ["d0","2c","1e","8f","ca","3f","0f","02","c1","af","bd","03","01","13","8a","6b"],
            ["3a","91","11","41","4f","67","dc","ea","97","f2","cf","ce","f0","b4","e6","73"],
            ["96","ac","74","22","e7","ad","35","85","e2","f9","37","e8","1c","75","df","6e"],
            ["47","f1","1a","71","1d","29","c5","89","6f","b7","62","0e","aa","18","be","1b"],
            ["fc","56","3e","4b","c6","d2","79","20","9a","db","c0","fe","78","cd","5a","f4"],
            ["1f","dd","a8","33","88","07","c7","31","b1","12","10","59","27","80","ec","5f"],
            ["60","51","7f","a9","19","b5","4a","0d","2d","e5","7a","9f","93","c9","9c","ef"],
            ["a0","e0","3b","4d","ae","2a","f5","b0","c8","eb","bb","3c","83","53","99","61"],
            ["17","2b","04","7e","ba","77","d6","26","e1","69","14","63","55","21","0c","7d"]
        ])
        
    
    
    def init_mixcolums(self):
        
        self.mixcols=np.array([
            ["02","03","01","01"],
            ["01","02","03","01"],
            ["01","01","02","03"],
            ["03","01","01","02"]
        ])
        
        
    def init_invmixcolums(self):
        
        self.invmixcols=np.array([
            ["0E","0B","0D","09"],
            ["09","0E","0B","0D"],
            ["0D","09","0E","0B"],
            ["0B","0D","09","0E"]
        ])
        
        
        
        
    def hexToBin(self,key,noOfBits):
        
        scale = 16 ## equals to hexadecimal
        num_of_bits = noOfBits

        binKey=bin(int(key, scale))[2:].zfill(num_of_bits)
        
        return (binKey)
    
    
    
    def binToHex(self,hx):
        
        return hex(int(hx,2))[2:].zfill(2)
    
    
    
    
    def convertToBinary(self,hxx):
        
        binn=[]
        
        for row in range(hxx.shape[0]):
            bn=[self.hexToBin(h,8) for h in hxx[row,:]]
            binn.append(bn)
            
        return np.array(binn)

        
    
    def xor(self,b1,b2):
        
        
        out=int(b1,2) ^ int(b2,2)
        out=bin(out)[2:].zfill(len(b1))
        
        return out
        
    
    def subByte(self,word,box):
        
        new_word=[]
        
        for byte in word:
            
            row=int(byte[0],16)
            col=int(byte[1],16)
            
            new_word.append(box[row,col])
            
        return new_word
    
    
    
    
    def shiftLeft(self,word,val):
        
        new_word=[word[np.mod(i+val,len(word))] for i in range(len(word))]
        
        return new_word
    
    
    
    def convertToString(self,state):
        
        s=""
        
        for col in range(state.shape[1]):
            for row in range(state.shape[0]):
                s+=str(state[row,col])
                
        return s
    
    
    
    def mix1(self,byte):
        
        return byte
    
    
    def mix2(self,byte):
        
        bit0=byte[0]
        shifted=byte[1:]+"0"
        new_byte=shifted
        
        
        if(bit0=="1"):
            
            new_byte=self.xor(new_byte,"00011011")
        
        return new_byte

    
    
    def addRoundKey(self,state,key):
        
        state_bin=self.convertToBinary(state)
        key_bin=self.convertToBinary(key)
        
        new_state=[]
        
        for row in range(state_bin.shape[0]):
            
            s=[self.binToHex(self.xor(state_bin[row,i],key_bin[row,i])) for i in range(len(state_bin[row,:]))]
            new_state.append(s)
            
        return np.array(new_state)
    
    
    
    def addSubByte(self,state):
        
        new_state=[]
        
        for row in range(state.shape[0]):
            
            word=self.subByte(state[row,:],self.sbox)
            new_state.append(word)
            
        return np.array(new_state)
    
    
    
    def invaddSubByte(self,state):
        
        new_state=[]
        
        for row in range(state.shape[0]):
            
            word=self.subByte(state[row,:],self.invsbox)
            new_state.append(word)
            
        return np.array(new_state)
    
    
    
    def shiftRows(self,state):
        
        new_state=[]
        
        for row in range(state.shape[0]):
            
            word=self.shiftLeft(state[row,:],row)
            new_state.append(word)
            
        return np.array(new_state)
    
    
    
    def invshiftRows(self,state):
        
        new_state=[]
        
        for row in range(state.shape[0]):
            
            word=self.shiftLeft(state[row,:],row*-1)
            new_state.append(word)
            
        return np.array(new_state)
    
    
    
    
    def mixColumns(self,state):
        
        state_bin=self.convertToBinary(state)
        new_state=[]
        
        for col in range(state.shape[1]):
            colm=[]
            for mixrow in range(self.mixcols.shape[0]):
                mixes=[]
                for mixcol in range(self.mixcols.shape[1]):
                
                    if(self.mixcols[mixrow,mixcol]=="01"):
                        mix=self.mix1(state_bin[mixcol,col])
                    elif(self.mixcols[mixrow,mixcol]=="02"):
                        mix=self.mix2(state_bin[mixcol,col])
                    elif(self.mixcols[mixrow,mixcol]=="03"):
                        mixf=self.mix1(state_bin[mixcol,col])
                        mixs=self.mix2(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                    
                    mixes.append(mix)
                    
                out=self.xor(self.xor(self.xor(mixes[0],mixes[1]),mixes[2]),mixes[3])
                colm.append(self.binToHex(out))
            new_state.append(colm)
            
        return np.transpose(np.array(new_state))
    
    
    
    def invmixColumns(self,state):
        
        state_bin=self.convertToBinary(state)
        new_state=[]
        
        for col in range(state.shape[1]):
            colm=[]
            for mixrow in range(self.invmixcols.shape[0]):
                mixes=[]
                for mixcol in range(self.invmixcols.shape[1]):
                
                    if(self.invmixcols[mixrow,mixcol]=="09"):
                        
                        mixf=self.mix2(self.mix2(self.mix2(state_bin[mixcol,col])))
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                    elif(self.invmixcols[mixrow,mixcol]=="0B"):
                        
                        mixf=self.mix2(self.mix2(state_bin[mixcol,col]))
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                        mixf=self.mix2(mix)
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                    elif(self.invmixcols[mixrow,mixcol]=="0D"):
                        
                        mixf=self.mix2(state_bin[mixcol,col])
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                        mixf=self.mix2(self.mix2(mix))
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                        
                    elif(self.invmixcols[mixrow,mixcol]=="0E"):
                        
                        mixf=self.mix2(state_bin[mixcol,col])
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                        mixf=self.mix2(mix)
                        mixs=self.mix1(state_bin[mixcol,col])
                        mix=self.xor(mixf,mixs)
                        
                        mix=self.mix2(mix)
                        
                    
                    mixes.append(mix)
                    
                out=self.xor(self.xor(self.xor(mixes[0],mixes[1]),mixes[2]),mixes[3])
                colm.append(self.binToHex(out))
            new_state.append(colm)
            
        return np.transpose(np.array(new_state))
    
    
    
    def encrypt(self,plain,roundKeys):
        
        new_state=self.addRoundKey(plain,roundKeys[0])
        
        for i in range(10):
            
            new_state=self.addSubByte(new_state)
            new_state=self.shiftRows(new_state)
            if i!=9:
                new_state=self.mixColumns(new_state)
            new_state=self.addRoundKey(new_state,roundKeys[i+1])
            
            
        return new_state
    
    
    
    
    def decrypt(self,cipher,roundKeys):
        
        new_state=self.addRoundKey(cipher,roundKeys[-1])
        
        for i in range(10):
            key=roundKeys[(roundKeys.shape[0]-1)-(i+1)]
            new_state=self.invaddSubByte(new_state)
            new_state=self.invshiftRows(new_state)
            if i!=9:
                new_state=self.invmixColumns(new_state)
                key=self.invmixColumns(key)
            new_state=self.addRoundKey(new_state,key)
            
            
        return new_state
    
            
        