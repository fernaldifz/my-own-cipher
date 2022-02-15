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
    result = [0 for i in range(len(Text))]

    #Setiap keystream "u" langsung di XOR dengan plaintext
    for count in range(len(Text)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t] #keystream
        c = u ^ ord(Text[count])
        result[count] = c

    return result

def LFSR(c, number):
    binary = str(bin(c)[2:])
    if(len(binary) < 8):
        x = ""
        for i in range(8 - len(binary)):
            x += "0"
        binary = x + binary

    firstHalf = binary[:4]
    secondHalf = binary[4:8]
    for i in range(number):
        new = XOR(int(firstHalf[0]), int(firstHalf[3]))
        firstHalf = str(new) + firstHalf[:3]
    
    for i in range(number):
        new = XOR(int(secondHalf[0]), int(secondHalf[3]))
        secondHalf = str(new) + secondHalf[:3]
    binary = firstHalf + secondHalf

    return binary

def XOR(bil1, bil2):
    if(bil1 == 1 and bil2 == 1) or (bil1 == 0 and bil2 == 0):
        return 0
    else:
        return 1

def binaryToDecimal(binary):
    decimal = 0
    for i in range(len(binary)):
        decimal += int(binary[i]) * 2**(len(binary)-i-1)
    return decimal

def RC4(key, Text):
    print(PRGA(KSA("halo"), "senang"))
    cipherText = PRGA(KSA("halo"), "senang")

    shiftedCipherText = [0 for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        print(chr(cipherText[i]))
        shiftedBinary = LFSR(cipherText[i], 8)
        decimal = binaryToDecimal(shiftedBinary)
        shiftedCipherText[i] = chr(decimal)
    
    print(shiftedCipherText)

    unshiftedCipherText = [0 for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        shiftedBinary = LFSR(cipherText[i], 15)
        decimal = binaryToDecimal(shiftedBinary)
        unshiftedCipherText[i] = chr(decimal)
    
    print(unshiftedCipherText)
    #print(PRGA(KSA(unshiftedCipherText), "senang"))

RC4("halo", "senang")