def SubNibble(func,byte):
    first,second=byte[:4],byte[4:]
    first=func[first]
    second=func[second]
    return first+second

def RotateNibble(byte):
    first,second=byte[:4],byte[4:]
    first,second=second,first
    return first+second

def Exor(a,b):
    t1=list(map(int,list(a)))
    t2=list(map(int,list(b)))
    
    ans=[str(x^y) for x,y in zip(t1,t2)]
    return "".join(ans)

S_box={
    
    "0000":"1001",
    "0001":"0100",
    "0010":"1010",
    "0011":"1011",
    "0100":"1101",
    "0101":"0001",
    "0110":"1000",
    "0111":"0101",
    "1000":"0110",
    "1001":"0010",
    "1010":"0000",
    "1011":"0011",
    "1100":"1100",
    "1101":"1110",
    "1110":"1111",
    "1111":"0111",   
}

key_list=list(S_box.keys())
value_list=list(S_box.values())

Inverse_S_box={}
for i in range(len(key_list)):
    Inverse_S_box[value_list[i]]=key_list[i]


def mult(p1, p2):
    p = 0
    while p2:
        if p2 & 0b1:
            p ^= p1
        p1 <<= 1
        if p1 & 0b10000:
            p1 ^= 0b11
        p2 >>= 1
    return p & 0b1111


def binary_to_int(nibble):
    res=0
    p=len(nibble)-1
    num=list(map(int,list(nibble)))
    for i in num:
        res+=((2**p)*i)
        p-=1
    return res

def int_to_binary(num):
    ans=[]
    while num>0:
        ans.append(str(num%2))
        num=int(num/2)
    while(len(ans)!=4):
        ans.append('0')
    ans.reverse()
    return "".join(ans)

def convert_sentence_to_stream(sentence):
    stream = []
    for letter in sentence:
        ascii_val = ord(letter)
        bin_val = bin(ascii_val)[2:]
        bin_val = '0'*(16-len(list(bin_val))) + bin_val
        stream.append(bin_val)

    print(stream,end="")
    return stream

def convert_stream_to_sentence(stream):
    ascii_list = []
    for binary in stream:

        ascii_list.append(chr(int(binary,2)))
    return ''.join(ascii_list)

def print_fun(s):
    i=0
    ans=""
    while i<len(s):
        ans+=s[i:i+4]+" "
        i+=4
    return ans

def generate_key(key):
    w0=key[:8]
    w1=key[8:]
    w2=""
    w3=""
    w4=""
    w5=""

    w2=Exor(Exor("10000000",SubNibble(S_box,RotateNibble(w1))),w0)
    w3=Exor(w2,w1)
    w4=Exor(Exor("00110000",SubNibble(S_box,RotateNibble(w3))),w2)
    w5=Exor(w4,w3)
    
    Key0=w0+w1
    Key1=w2+w3
    Key2=w4+w5
    
    print()
    print("Key 0 : {}".format(print_fun(Key0)))
    print("Key 1 : {}".format(print_fun(Key1)))
    print("Key 2 : {}".format(print_fun(Key2)))
    
    return Key0,Key1,Key2

class Encrypt:
    def __init__(self,text,Key0,Key1,Key2):
        self.text=text                
        self.Key0=Key0
        self.Key1=Key1
        self.Key2=Key2
        self.encrypt=text
        self.keys=[self.Key0,self.Key1,self.Key2]
        
    def mix_columns(self,word):
        m=[[1,4],[4,1]]
        s=[[word[:4],word[4:8]],[word[8:12],word[12:]]]

        ans=[[0,0],[0,0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    ans[i][j]^=mult(m[i][k],binary_to_int(s[k][j]))
                ans[i][j]=int_to_binary(ans[i][j])
        res=""
        for i in range(2):
            for j in range(2):
                res+=ans[j][i]

        return res

    
    def Functions(self):

        rounds=0
        while rounds <=2:
            
            if rounds==1 or rounds==2:
                self.encrypt=SubNibble(S_box,self.encrypt[:8])+SubNibble(S_box,self.encrypt[8:])
                print("Substitute Nibbles : {}".format(print_fun(self.encrypt)))
  
            if rounds==1 or rounds==2:
                self.encrypt=self.encrypt[:4]+self.encrypt[12:]+self.encrypt[8:12]+self.encrypt[4:8]
                print("Shift Row : {}".format(print_fun(self.encrypt)))

            if rounds==1:
                self.encrypt=self.mix_columns(self.encrypt)
                print("Mix Columns : {}".format(print_fun(self.encrypt)))

            self.encrypt=Exor(self.encrypt,self.keys[rounds])
            print("Add Round Key : {}".format(print_fun(self.encrypt)))
            
            rounds+=1
            
        
    def encrypt_text(self):
        self.Functions()
        return self.encrypt
    
class Decrypt:
    def __init__(self,ciphertext,Key0,Key1,Key2):
        self.ciphertext=ciphertext                
        self.Key0=Key0
        self.Key1=Key1
        self.Key2=Key2
        self.text=ciphertext
        self.keys=[self.Key0,self.Key1,self.Key2]
        
    def inverse_mix_columns(self,word):
        m=[[9,2],[2,9]]
        s=[[word[:4],word[8:12]],[word[4:8],word[12:]]]

        ans=[[0,0],[0,0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    ans[i][j]^=mult(m[i][k],binary_to_int(s[k][j]))
                ans[i][j]=int_to_binary(ans[i][j])
        res=""
        for i in range(2):
            for j in range(2):
                res+=ans[i][j]

        return res

    
    def Functions(self):
        rounds=2
        while rounds >=0:

            self.ciphertext=Exor(self.ciphertext,self.keys[rounds])
            print("Add Round Key : {}".format(print_fun(self.ciphertext)))           

            if rounds==1:
                self.ciphertext=self.inverse_mix_columns(self.ciphertext)
                print("Mix Columns : {}".format(print_fun(self.ciphertext)))

            if rounds==1 or rounds==2:
                self.ciphertext=self.ciphertext[:4]+self.ciphertext[12:]+self.ciphertext[8:12]+self.ciphertext[4:8]
                print("Shift Row : {}".format(print_fun(self.ciphertext)))

            if rounds==1 or rounds==2:
                self.ciphertext=SubNibble(Inverse_S_box,self.ciphertext[:8])+SubNibble(Inverse_S_box,self.ciphertext[8:])
                print("Substitute Nibbles : {}".format(print_fun(self.ciphertext)))

            rounds-=1
            
            
        
    def decrypt_text(self):
        self.Functions()
        return self.ciphertext
    
if __name__=='__main__':
        
    org_text=input("Enter plain text : ")
    
    key=input("Enter key : ")
    #key="0100101011110101"

    stream=convert_sentence_to_stream(org_text)
    #stream=['1101011100101000']
    
    Key0,Key1,Key2=generate_key(key=key)
    
    ciphertext=[]
    print()
    print('***** Encryption *****')
    print()
    for block in stream:
        encrypt=Encrypt(text=block,Key0=Key0,Key1=Key1,Key2=Key2)
        ciphertext.append(encrypt.encrypt_text())
    
    print('Ciphertext : {}'.format(''.join(ciphertext)))    
    print()
    print('***** Decryption *****')
    print()
    
    final_text=[]
    for block in ciphertext:
        decrypt=Decrypt(ciphertext=block,Key0=Key0,Key1=Key1,Key2=Key2)
        final_text.append(decrypt.decrypt_text())

    ans=convert_stream_to_sentence(final_text)
    if ans==org_text:
        print()
        print('Original text  : {}'.format(org_text))
        print('Decrypted text : {}'.format(ans))




