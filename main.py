import codecs
import binascii
import re

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
    binary = str(bin(int(c))[2:])
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
    print("ini hasil enkripsi sebelum LFSR dan sesudah PRGA", PRGA(KSA(key), Text))
    cipherText = PRGA(KSA(key), Text)

    shiftedText = ["" for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        shiftedText[i] = LFSR(cipherText[i], 8)
    
    shiftedCipherText = ["" for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        shiftedCipherText[i] = chr(binaryToDecimal(shiftedText[i]))

    print("ini hasil enkripsi setelah LFSR dan sesudah PRGA: ", shiftedCipherText)

    cipherTextResult = ""
    for i in range(len(cipherText)):
        cipherTextResult += shiftedCipherText[i]
    
    print("ini hasil akhir enkripsi setelah segalanya: ", cipherTextResult)
    
    unshiftedText = ["" for i in range(len(cipherText))]

    for i in range(len(cipherText)):
        unshiftedText[i] = LFSR(binaryToDecimal(shiftedText[i]), 7)
    
    unshiftedCipherText = ["" for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        unshiftedCipherText[i] = chr(binaryToDecimal(unshiftedText[i]))
    
    print("ini hasil dekripsi setelah LFSR dan sebelum PRGA: ", unshiftedCipherText)

    cipherText2 = ""

    for i in range(len(cipherText)):
        cipherText2 += unshiftedCipherText[i]
    
    plainTextNumber = PRGA(KSA(key), cipherText2)
    print("ini hasil dekripsi setelah LFSR dan setelah PRGA: ", plainTextNumber)

    plainTextResult = ""
    for i in range(len(plainTextNumber)):
        plainTextResult += chr(plainTextNumber[i])
    
    print("ini hasil akhir dekripsinya setelah segalanya:", plainTextResult)

def RC4EncFile(filename, key):
    file = open(filename, "rb")
    data = file.read()
    file.close()
    
    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ len(key)
        
    file = open("CC-" + filename, "wb")
    file.write(data)
    file.close()

def RC4DecFile(filename, key):
    file = open(filename, "rb")
    data = file.read()
    file.close()
    
    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ len(key)
        
    
    file = open(filename, "wb")
    file.write(data)
    file.close()

data = RC4EncFile("file/test_image.jpg", "halo")
# RC4("halo", "aku adalah anak gembala yang punya 4 rumah dengan kode '431#$sT4'. ")