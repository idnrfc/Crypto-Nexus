"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : ChatCommon.py
내용 : 그냥 공통적이고 주로 쓰이는 변수만 정리
"""


class ChatCommon:
    # 타입 지정을 위한 변수... 그냥 자주 쓰는거
    TYPE_OF_CAESAR = 0
    TYPE_OF_TRANSPOSITION = 1
    TYPE_OF_AFFINE = 2

    # 프로그램에서 지정한 형식의 메세지가 아닌 경우
    TYPE_OF_WRONG_MESSAGE = 0

    # 기타 변수들, 정규식, 시저 기본 문자열 등
    message_regularexpression = '\[(?P<type>[H]?[PM][AOS][GDC])\](?P<msg_all>(?P<hmac_value>[a-z0-9]*)[\s]?(?P<msg>.+))'
    caesar_letters = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    RECV_BUFFER = 1024
    is_response_HMSG = False
    hmac_auth_success = False
    stop = False
    PAG = None
    MAC = None
