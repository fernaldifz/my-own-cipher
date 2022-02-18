from pydoc import plain
import time
import sys
import RC4Modified
from os import curdir, environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QTabWidget, QWidget, QMessageBox, QPushButton, QFileDialog, QVBoxLayout

class RC4Encryption(QDialog):
    def __init__(self):
        super(RC4Encryption, self).__init__()
        loadUi("RC4Enc.ui", self)
        self.decrypt.clicked.connect(self.gotoRC4Decrypt)
        self.encrypt.clicked.connect(self.encrypting)
        self.savecipher.clicked.connect(self.saveCipher)
        self.selectfile.clicked.connect(self.openFileToEncrypt)

    def encrypting(self):
        self.file.setText("")
        plaintext = self.plaintext.toPlainText()
        key = self.key.toPlainText()
        cipher = RC4Modified.encrypt(key, plaintext)
        self.ciphertext.setText(cipher)

    def gotoRC4Decrypt(self):
        RC4Dec = RC4Decryption()
        widget.addWidget(RC4Dec)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def saveCipher(self):
        if len(self.ciphertext.toPlainText()) != 0:
            option=QFileDialog.Options()
            option|=QFileDialog.DontUseNativeDialog

            file=QFileDialog.getSaveFileName(widget,"Save File Window Title","default.txt","All Files (*)",options=option)
            file = open(file[0], "w",encoding="utf-8")
            file.write(self.ciphertext.toPlainText())
            file.close()

    def openFileToEncrypt(self):
        if len(self.key.toPlainText()) != 0:
            self.warning.setText("")
            option=QFileDialog.Options()
            file=QFileDialog.getOpenFileName(widget,"Open Single File","Default File","All Files(*)",options=option)
            path = file[0]
            data = RC4Modified.encryptFiles(self.key.toPlainText(), path)
            file=QFileDialog.getSaveFileName(widget,"Save File Window Title","default.txt","All Files (*)",options=option)
            file = open(file[0], "wb")
            file.write(data)
            file.close()
            self.file.setText("file \n has been \n encrypted!")
            
        else:
            self.warning.setText("decide the \nkey first!")
       

class RC4Decryption(QDialog):
    def __init__(self):
        super(RC4Decryption, self).__init__()
        loadUi("RC4Dec.ui", self)
        self.encrypt.clicked.connect(self.gotoRC4Encrypt)
        self.decrypt.clicked.connect(self.decrypting)
        self.selectfile.clicked.connect(self.openFileToDecrypt)

    def gotoRC4Encrypt(self):
        RC4Enc = RC4Encryption()
        widget.addWidget(RC4Enc)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def decrypting(self):
        self.file.setText("")
        ciphertext = self.ciphertext.toPlainText()
        key = self.key.toPlainText()
        plaintext = RC4Modified.decrypt(key, ciphertext)
        self.plaintext.setText(plaintext)

    def openFileToDecrypt(self):
        if len(self.key.toPlainText()) != 0:
            self.warning.setText("")
            option=QFileDialog.Options()
            file=QFileDialog.getOpenFileName(widget,"Open Single File","Default File","All Files(*)",options=option)
            path = file[0]
            data = RC4Modified.decryptFiles(self.key.toPlainText(), path)
            file=QFileDialog.getSaveFileName(widget,"Save File Window Title","default.txt","All Files (*)",options=option)
            file = open(file[0], "wb")
            file.write(data)
            file.close()
            self.file.setText("file \n has been \n decrypted!")
            
        else:
            self.warning.setText("decide the \nkey first!")

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def run():
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

suppress_qt_warnings()
app = QApplication(sys.argv)
menu = RC4Encryption()
widget = QtWidgets.QStackedWidget()
widget.addWidget(menu)
widget.setFixedHeight(512)
widget.setFixedWidth(720)