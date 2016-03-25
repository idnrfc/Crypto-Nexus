"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoAffine.py
내용 : 아핀 사이퍼
"""
from CustomError import CustomError
from CryptoCommon import CryptoCommon
import array, random


class Affine(CryptoCommon):
    def __init__(self, sourceType=False, mode='encrypt', message='', letters='', key=0, fileAccessType=False, inputFile='', outputFile=''):
        self.mode = mode
        self.message = message
        self.letters = letters
        self.key = key
        self.keyA = 0
        self.keyB = 0
        self.sourceType = sourceType
        self.fileAccessType = fileAccessType
        self.inputFile = inputFile
        self.outputFile = outputFile

    # 텍스트인지 파일읹, 바이너리로 처리할 건지 따지는 함수
    def goEncryptOrDecrypt(self):
        # 키 입력 형태 검사
        self.check_key()
        # 명시적으로 키 변환
        self.key = int(self.key)

        self.keyA, self.keyB = self.getKeyParts(self.key)
        if not self.sourceType:
            if self.mode == 'encrypt':
                return self.encrypt()
            else:
                return self.decrypt()
        else:
             # 파일 갖고오기전에 체크
            if not self.checkFileReadble(self.inputFile):
                return False
            if self.mode == 'encrypt':
                self.message = self.loadFile(self.inputFile, self.fileAccessType)
                self.saveFile(self.outputFile, self.encrypt(), self.fileAccessType)
            else:
                self.message = self.loadFile(self.inputFile, self.fileAccessType)
                self.saveFile(self.outputFile, self.decrypt(), self.fileAccessType)

    def encrypt(self):

        self.check_keys(self.keyA, self.keyB, 'encrypt')
        if not self.fileAccessType:
            ciphertext = ''
        else:
            ciphertext = array.array('B')

        for symbol in self.message:
            if self.bringSymbol(symbol) in self.letters:
                # encrypt this symbol
                symIndex = self.letters.find(self.bringSymbol(symbol))
                if not self.fileAccessType:
                    ciphertext += self.letters[(symIndex * self.keyA + self.keyB) % len(self.letters)]
                else:
                    ciphertext.append(ord(self.letters[(symIndex * self.keyA + self.keyB) % len(self.letters)]))


            else:
                if not self.fileAccessType:
                    ciphertext += symbol
                else:
                    ciphertext.append(symbol)
        return ciphertext

    def decrypt(self):
        self.check_keys(self.keyA, self.keyB, 'decrypt')

        if not self.fileAccessType:
            plaintext = ''
        else:
            plaintext = array.array('B')

        modInverseOfKeyA = self.findModInverse(self.keyA, len(self.letters))

        for symbol in self.message:
            if self.bringSymbol(symbol) in self.letters:
                # decrypt this symbol
                symIndex = self.letters.find(self.bringSymbol(symbol))
                if not self.fileAccessType:
                    plaintext += self.letters[(symIndex - self.keyB) * modInverseOfKeyA % len(self.letters)]
                else:
                    plaintext.append(ord(self.letters[(symIndex - self.keyB) * modInverseOfKeyA % len(self.letters)]))

            else:
                if not self.fileAccessType:
                    plaintext += symbol
                else:
                    plaintext.append(symbol)
        return plaintext

    # 심볼을 fileAccessType에 맞게 다시 반환
    # fileAccessType가 False면 텍스트 타입, True면 바이너리 타입
    def bringSymbol(self, symbol):
        if not self.fileAccessType:
            return symbol
        return chr(symbol)

    def getKeyParts(self, key):
        keyA = key // len(self.letters)
        keyB = key % len(self.letters)
        return (keyA, keyB)


    def check_key(self):
        if not str(self.key).isnumeric():
            raise CustomError('키 오류', '키는 숫자여야합니다.')

    def check_keys(self, keyA, keyB, mode):
        if keyA == 1 and mode == 'encrypt':
            raise CustomError('키 오류', 'keyA가 1이면 암호문이 약해집니다.')
        if keyB == 0 and mode == 'encrypt':
            raise CustomError('키 오류', 'keyB가 0이면 암호문이 약해집니다.')
        if keyA < 0 or keyB < 0 or keyB > len(self.letters) - 1:
            raise CustomError('키 오류', 'keyA는 0보다 커야하고, keyB는 0과 ' + str(len(self.letters)-1) + '사이어야 합니다.')
        if self.gcd(keyA, len(self.letters)) != 1:
            raise CustomError('키 오류', 'keyA와 심볼셋 길이가 서로소가 아닙니다.')

    def getRandomKey(self):
        while True:
            keyA = random.randint(2, len(self.letters))
            keyB = random.randint(2, len(self.letters))
            if self.gcd(keyA, len(self.letters)) == 1:
                return keyA * len(self.letters) + keyB

    def gcd(self, a, b):
        # Return the GCD of a and b using Euclid's Algorithm
        while a != 0:
            a, b = b % a, a
        return b


    def findModInverse(self, a, m):
        # Returns the modular inverse of a % m, which is
        # the number x such that a*x % m = 1

        if self.gcd(a, m) != 1:
            return None # no mod inverse if a & m aren't relatively prime

        # Calculate using the Extended Euclidean Algorithm:
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3 # // is the integer division operator
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m

    def hack(self):
        pass

