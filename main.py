def KSA(key):
    #inisiasi
    S = [i for i in range(256)]
    
    #permutasi
    j = 0
    for i in range(0,256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256 
        S[i], S[j] = S[j], S[i]

    return S

def PRGA(S):
    pass

# print(KSA("aku dan kamu"))
