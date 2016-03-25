"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoVigenere.py
내용 : 비제네르 사이퍼
"""
from CustomError import CustomError
from CryptoCommon import CryptoCommon
import CryptoVigenereKasiskiHackExtra
import array


class Vigenere(CryptoCommon):
    def __init__(self, sourceType=False, mode='encrypt', message='', letters='', key=0, fileAccessType=False, inputFile='', outputFile=''):
        self.mode = mode
        self.message = message
        self.letters = letters
        self.key = key
        self.sourceType = sourceType
        self.fileAccessType = fileAccessType
        self.inputFile = inputFile
        self.outputFile = outputFile

    # 텍스트인지 파일읹, 바이너리로 처리할 건지 따지는 함수
    def goEncryptOrDecrypt(self):
        # 키 입력 형태 검사
        self.check_key()

        if not self.sourceType:
            return self.translateMessage(self.key, self.message)
        else:
             # 파일 갖고오기전에 체크
            if not self.checkFileReadble(self.inputFile):
                return False
            if self.mode == 'encrypt':
                self.message = self.loadFile(self.inputFile, self.fileAccessType)
                self.saveFile(self.outputFile, self.translateMessage(self.key, self.message), self.fileAccessType)
            else:
                self.message = self.loadFile(self.inputFile, self.fileAccessType)
                self.saveFile(self.outputFile, self.translateMessage(self.key, self.message), self.fileAccessType)

    def translateMessage(self, key, message):


        keyIndex = 0
        key = key.upper()
        mode = self.mode
        letters = self.letters


        if not self.fileAccessType:
            translated = []
        else:
            translated = array.array('B')

        for symbol in message: # loop through each character in message
            num = letters.find(self.bringSymbol(symbol).upper())
            if num != -1: # -1 means symbol.upper() was not found in LETTERS
                if mode == 'encrypt':
                    num += letters.find(key[keyIndex]) # add if encrypting
                elif mode == 'decrypt':
                    num -= letters.find(key[keyIndex]) # subtract if decrypting

                num %= len(letters) # handle the potential wrap-around

                if not self.fileAccessType:
                    # add the encrypted/decrypted symbol to the end of translated.
                    if symbol.isupper():
                        translated.append(letters[num])
                    elif symbol.islower():
                        translated.append(letters[num].lower())
                else:
                    if self.bringSymbol(symbol).isupper():
                        translated.append(ord(letters[num]))
                    elif self.bringSymbol(symbol).islower():
                        translated.append(ord(letters[num].lower()))

                keyIndex += 1 # move to the next letter in the key
                if keyIndex == len(key):
                    keyIndex = 0
            else:
                # The symbol was not in LETTERS, so add it to translated as is.
                translated.append(symbol)
        if not self.fileAccessType:
            return ''.join(translated)
        else:
            return translated


    # 심볼을 fileAccessType에 맞게 다시 반환
    # fileAccessType가 False면 텍스트 타입, True면 바이너리 타입
    def bringSymbol(self, symbol):
        if not self.fileAccessType:
            return symbol
        return chr(symbol)

    def check_key(self):
        for c in self.key:
            if not c in self.letters:
                raise CustomError('키 오류', '문자(심볼셋)에 키의 문자들이 들어가 있어야 합니다.')

    def go_kasiski_examination(self):
        return CryptoVigenereKasiskiHackExtra.kasiskiExamination(self.message)

    def get_kaiski_freq_score_list(self, key_length):
        return CryptoVigenereKasiskiHackExtra.make_freq_score_list(self.message, key_length, self)

    def get_kasiski_NUM_MOST_FREQ_LETTERS(self):
        return CryptoVigenereKasiskiHackExtra.NUM_MOST_FREQ_LETTERS

    def get_kasiski_proper_casing(self, decrypted_text):
        origCase = []
        for i in range(len(self.message)):
            if self.message[i].isupper():
                origCase.append(decrypted_text[i].upper())
            else:
                origCase.append(decrypted_text[i].lower())
        return ''.join(origCase)
