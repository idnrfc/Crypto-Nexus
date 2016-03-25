"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : CustomError.py
내용 : 많은 예기치 못한 상황들을 위해 만든 커스텀 에러 Exception
"""

class CustomError(Exception):
    def __init__(self, title, msg):
        self.title = title
        self.msg = msg
