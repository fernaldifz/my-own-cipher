def KSA(key):
    #inisiasi
    S = [i for i in range(256)]
    
    #permutasi
    j = 0
    for i in range(0,256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256 
        S[i], S[j] = S[j], S[i]

    return S

def PRGA(S, Text):
    i = 0; j=0
    count = 0
    result = ''

    #Setiap keystream "u" langsung di XOR dengan plaintext
    for count in range(len(Text)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t] #keystream
        c = u ^ ord(Text[count])
        result += chr(c)
    return result

print(PRGA(KSA("halo"), "senang sekali"))