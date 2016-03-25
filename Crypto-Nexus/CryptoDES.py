"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CryptoDES.py
내용 : DES,Triple-DES 모듈을 사용해서 본 GUI환경에 맞게 살짝 수정한 내용
참조 : pyDES.py
        http://www.cppblog.com/AutomateProgram/archive/2013/01/06/197017.html
        http://twhiteman.netfirms.com/des.html
"""
from CustomError import CustomError
from CryptoCommon import CryptoCommon
import pyDes
import base64


class CryptoDES(CryptoCommon):
    def __init__(self, sourceType=False, mode='encrypt', message='', key='12345678', fileAccessType=False, \
                 inputFile='', outputFile='', isTriple = False):
        self.message = message
        self.key = key
        self.mode = mode
        self.sourceType = sourceType
        self.fileAccessType = fileAccessType
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.iv=''
        self.isTriple = isTriple

    # 텍스트인지 파일읹, 바이너리로 처리할 건지 따지는 함수
    def goEncryptOrDecrypt(self):
        self.check_key()

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
        if self.isTriple:
            if not ((len(self.key) == 16) | (len(self.key) == 24)):
                raise CustomError('키 오류', '트리플 DES의 키의 길이는 16이거나 24이어야합니다.')
        else:
            if (not len(self.key) == 8):
                raise CustomError('키 오류', 'DES의 키의 길이는 8이어야합니다.')


    def encrypt(self):
        if not self.fileAccessType:
            if not type(self.message) == bytes:
                self.message = self.message.encode('utf-8')

        data = self.message

        if self.isTriple:
            k = pyDes.triple_des(self.key, pyDes.ECB, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        else:
            k = pyDes.des(self.key, pyDes.ECB, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)

        d = k.encrypt(data)
        d = base64.encodestring(d)

        if not self.fileAccessType:
            return ''.join(map(chr, d))
        return d

    def decrypt(self):
        if not self.fileAccessType:
            if not type(self.message) == bytes:
                self.message = self.message.encode('utf-8')

        data = self.message

        if self.isTriple:
            k = pyDes.triple_des(self.key, pyDes.ECB, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        else:
            k = pyDes.des(self.key, pyDes.ECB, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)

        data = base64.decodestring(data)
        d = k.decrypt(data)

        if not self.fileAccessType:
            return d.decode('utf-8')
        return d


 
