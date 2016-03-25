"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoTransposition.py
내용 : 트랜스포지션 사이퍼
"""
from CustomError import CustomError
from CryptoCommon import CryptoCommon
import math, array


class Transposition(CryptoCommon):
    def __init__(self, sourceType=False, mode='encrypt', message='', key=0, fileAccessType=False, inputFile='', outputFile=''):
        self.mode = mode
        self.message = message
        self.key = key
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

    def check_key(self):
        if not str(self.key).isnumeric():
            raise CustomError('키 오류', '키는 숫자여야합니다.')

    def encrypt(self):
        translated = [''] * self.key

        for col in range(self.key):
            pointer = col
            while pointer < len(self.message):
                if not self.fileAccessType:
                    translated[col] += self.message[pointer]
                else:
                    translated[col] += chr(self.message[pointer])
                pointer += self.key

        # 바이너리모드라면 좀 특별하게 형식을 바꿔주고 저장한다.
        # 간단하게 말하면 원래 translated의 모든 내용을 ord()해서 아스키로 바꾸고 다시 바이트 형식으로
        if not self.fileAccessType:
            return ''.join(translated)
        else:
            return_array= array.array('B')
            return_array.fromlist(list(map(ord, ''.join(translated))))
            return return_array

    def decrypt(self):

        numOfColumns = math.ceil(len(self.message) / self.key)
        numOfRows = self.key
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(self.message)

        translated = [''] * numOfColumns
        col = 0
        row = 0

        for symbol in self.message:
            if not self.fileAccessType:
                translated[col] += symbol
            else:
                translated[col] += chr(symbol)

            col += 1
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                col = 0
                row += 1

        # 바이너리모드라면 좀 특별하게 형식을 바꿔주고 저장한다.
        # 간단하게 말하면 원래 translated의 모든 내용을 ord()해서 아스키로 바꾸고 다시 바이트 형식으로
        if not self.fileAccessType:
            return ''.join(translated)
        else:
            return_array= array.array('B')
            return_array.fromlist(list(map(ord, ''.join(translated))))
            return return_array

    def hack(self):
        pass
