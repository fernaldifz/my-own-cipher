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

def LFSR(c, number = 8):
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

def reverseLFSR(c, number = 7):
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

def encrypt(key, text):
    #PRGA
    
    cipherText = PRGA(KSA(key), text)

    #LFSR

    # print(cipherText)

    shiftedText = ["" for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        shiftedText[i] = LFSR(cipherText[i], 8)

    shiftedCipherText = ["" for i in range(len(cipherText))]
    for i in range(len(cipherText)):
        shiftedCipherText[i] = chr(binaryToDecimal(shiftedText[i]))

    cipherResult = ""
    for i in range(len(cipherText)):
        cipherResult += shiftedCipherText[i]
    
    return cipherResult

def decrypt(key, cipherText):
    unshiftedText = ["" for i in range(len(cipherText))]
    arrayOFText = ["" for i in range(len(cipherText))]
    unshiftedTextString = ""

    for i in range(len(cipherText)):
        unshiftedText[i] = reverseLFSR(ord(cipherText[i]),7)
        arrayOFText[i] = chr(binaryToDecimal(unshiftedText[i]))
        unshiftedTextString += arrayOFText[i]
    
    arrayOfPlaintext = PRGA(KSA(key), unshiftedTextString)
    plaintext = ""

    for char in arrayOfPlaintext:
        plaintext += chr(char)

    return plaintext

def encryptFiles(key, Path):
    data = PRGAFiles(KSA(key), Path) #value 
    # print(data[:10])

    # shiftedText = ["" for i in range(len(data))]
    # shiftedCipherText = ["" for i in range(len(data))]
    for index, value in enumerate(data):
        data[index] = binaryToDecimal(LFSR(value))
    
    # print(data[:10])
    return data

def decryptFiles(key, Path):
    i = 0; j = 0
    file = open(Path, "rb")
    data = file.read()
    file.close()

    data = bytearray(data)

    # print(data[:10])

    unshiftedText = ["" for i in range(len(data))]
    for index, value in enumerate(data):
        unshiftedText[index] = reverseLFSR(value)
        data[index] = binaryToDecimal(unshiftedText[index])
    
    # print(data[:10])
    
    S = KSA(key)
    for index, value in enumerate(data):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t] #keystream
        data[index] = u ^ value

    return data

def PRGAFiles(S, Path):
    i = 0; j=0
    count = 0

    file = open(Path, "rb")
    data = file.read()
    file.close()

    data = bytearray(data) 
    # print(data[:10])
    for index, value in enumerate(data):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t] #keystream
        data[index] = u ^ value
    
    # print(data[:10])
    # print(len(data))
    # file = open("CC-" + Path, "wb")
    # file.write(data)
    # file.close()
    return data

# a = encrypt("halo", "aku adalah anak gembala yang punya 4 rumah dengan kode '431#$sT4'. ")
# b = decrypt("halo", encrypt("halo", "aku adalah anak gembala yang punya 4 rumah dengan kode '431#$sT4'. "))

# print(encryptFiles("Halo", "test_image.jpg")[:10])
# data = encryptFiles("Halo", "test_image.jpg")
# file = open("CC-" + "test_image.jpg", "wb")
# file.write(data)
# file.close()
# # print(data[:10])
# data = decryptFiles("Halo", "CC-test_image.jpg")
# file = open("CC-" + "test_image.jpg", "wb")
# file.write(data)
# file.close()
# print(data[:10])

                                                                                                                                                                                                                                                                                                                          