"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoCaesar.py
내용 : 시저 사이퍼를 위한 행동, 암복호화을 제공
"""

from CustomError import CustomError
from CryptoCommon import CryptoCommon
import array


class Caesar(CryptoCommon):
    def __init__(self, sourceType=False, mode='encrypt', message='', letters='', key=0, fileAccessType=False, inputFile='', outputFile=''):
        self.message = message
        self.letters = letters
        self.key = key
        self.mode = mode
        self.sourceType = sourceType
        self.fileAccessType = fileAccessType
        self.inputFile = inputFile
        self.outputFile = outputFile

    # 텍스트인지 파일읹, 바이너리로 처리할 건지 따지는 함수
    def goEncryptOrDecrypt(self):
        # 키 간단하게 검사
        self.check_key()

        # 명시적으로 키 변환
        self.key = int(self.key)

        if not self.sourceType:
            return self.encryptAndDecrypt()
        else:
            # 파일 갖고오기전에 체크
            if not self.checkFileReadble(self.inputFile):
                return False

            self.message = self.loadFile(self.inputFile, self.fileAccessType)
            self.saveFile(self.outputFile, self.encryptAndDecrypt(), self.fileAccessType)

    def check_key(self):
        if not str(self.key).isnumeric():
            raise CustomError('키 오류', '키는 숫자여야합니다.')

    def encryptAndDecrypt(self):
        # fileAcceessType이 바이너리이면 바이트 배열로 줘야 자 ㄹ 됨...
        if not self.fileAccessType:
            translated = ''
        else:
            translated = array.array('B')

        for symbol in self.message:
            if self.bringSymbol(symbol) in self.letters:
                num = self.letters.find(self.bringSymbol(symbol))
                if self.mode == 'encrypt':
                    num = num + self.key
                elif self.mode == 'decrypt':
                    num = num - self.key
                num = num % len(self.letters)

                if not self.fileAccessType:
                    translated = translated + self.letters[num]
                else:
                    translated.append(ord(self.letters[num]))
            else:
                if not self.fileAccessType:
                    translated = translated + symbol
                else:
                    translated.append(symbol)
        return translated

    # 심볼을 fileAccessType에 맞게 다시 반환
    # fileAccessType가 False면 텍스트 타입, True면 바이너리 타입
    def bringSymbol(self, symbol):
        if not self.fileAccessType:
            return symbol
        return chr(symbol)



