"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoCommon.py
내용 : 암호에서 자주 쓰이는 변수들을 지원할 예정
"""
import os


class CryptoCommon:
    common_long_keyspace = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

    def __init__(self):
        self.message = ''
        self.key = 0
        self.mode = ''
        self.letters = ''
        self.sourceType = False
        self.inputFile = ''
        self.outputFile = ''
        self.fileAccessType = False

    # 파일 저장
    # 파일 저장 방식이 바이너리라면 바이너리방식으로 저장....
    # 나중에 바이너리방식으로 통이할 것
    def saveFile(self, filename, content, fileAccessType):
        try:
            if not fileAccessType:
                file = open(filename, mode='w', encoding='utf-8')
            else:
                file = open(filename, mode='wb')
        except:
            return False
        file.write(content)
        file.close()

    def loadFile(self, filename, fileAccessType):
        try:
            if not fileAccessType:
                file = open(filename, mode='r', encoding='utf-8')
            else:
                file = open(filename, mode='rb')
        except:
            return False
        content = file.read()
        file.close()
        return content

    def checkFileReadble(self, filename):
        if os.access(filename, os.R_OK):
            return True
        return False



