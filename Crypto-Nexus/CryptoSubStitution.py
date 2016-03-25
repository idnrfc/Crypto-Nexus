"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoSubStitution.py
내용 : 서브스티튜션 사이퍼
"""
from CustomError import CustomError
from CryptoCommon import CryptoCommon

import array, random



class SubStitution(CryptoCommon):
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
            return self.translateMessage()
        else:
             # 파일 갖고오기전에 체크
            if not self.checkFileReadble(self.inputFile):
                return False
            if self.mode == 'encrypt':
                self.message = self.loadFile(self.inputFile, self.fileAccessType)
                self.saveFile(self.outputFile, self.translateMessage(), self.fileAccessType)
            else:
                self.message = self.loadFile(self.inputFile, self.fileAccessType)
                self.saveFile(self.outputFile, self.translateMessage(), self.fileAccessType)



    def translateMessage(self):

        key= self.key
        message = self.message
        mode = self.mode
        charsA = self.letters
        charsB = key


        if not self.fileAccessType:
            translated = ''
        else:
            translated = array.array('B')

        if mode == 'decrypt':
            # For decrypting, we can use the same code as encrypting. We
            # just need to swap where the key and LETTERS strings are used.
            charsA, charsB = charsB, charsA

            # loop through each symbol in the message
        for symbol in message:
            if self.bringSymbol(symbol).upper() in charsA:
                symIndex = charsA.find(self.bringSymbol(symbol).upper())
                if not self.fileAccessType:
                    if symbol.isupper():
                        translated += charsB[symIndex].upper()
                    else:
                        translated += charsB[symIndex].lower()
                else:
                    if self.bringSymbol(symbol).isupper():
                        translated.append(ord(charsB[symIndex].upper()))
                    else:
                        translated.append(ord(charsB[symIndex].lower()))

            else:
                if not self.fileAccessType:
                    # symbol is not in LETTERS, just add it
                    translated += symbol
                else:
                    translated.append(symbol)

        return translated

    # 심볼을 fileAccessType에 맞게 다시 반환
    # fileAccessType가 False면 텍스트 타입, True면 바이너리 타입
    def bringSymbol(self, symbol):
        if not self.fileAccessType:
            return symbol
        return chr(symbol)

    def getRandomKey(self):
        key = list(self.letters)
        random.shuffle(key)
        return ''.join(key)

    def check_key(self):
        keyList = list(self.key)
        lettersList = list(self.letters)
        keyList.sort()
        lettersList.sort()
        if keyList != lettersList:
            raise CustomError('키 오류', '키와 문자(심볼셋)이 매치되질 않습니다.')

    # 패턴 공격 실시, 사전 파일에서 패턴 파일을 생성 후 공격
    def pattern_hack(self):
        import CryptoSubStitutionHackExtra
        CryptoSubStitutionHackExtra.LETTERS = self.letters
        letter_mapping = CryptoSubStitutionHackExtra.hackSimpleSub(self.message)
        self.key, self.message = CryptoSubStitutionHackExtra.decryptWithCipherletterMapping(self.message, letter_mapping)
        letter_mapping = CryptoSubStitutionHackExtra.getPrettyLetterMapping(letter_mapping)

        return letter_mapping
