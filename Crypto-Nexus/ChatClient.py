"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : ChatClient.py
내용 : 채팅 클라이언트를 위한 코드, 디피헬만 키교환 및 HMAC을 지원하는 수/송신
"""

from socket import *
from _thread import *
import re
import DiffieHellman
import hmac

from ChatCommon import ChatCommon
from CryptoCaesar import Caesar
from CryptoTransposition import Transposition


class ChatClient(ChatCommon):

    def __init__(self, server_ip, server_port, type_of_crypto, support_hmac):
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.client_connection = None
        self.__PRIVATE_key = 0
        self.__SECRET_key = 0
        self.type_of_crypto = type_of_crypto
        self.support_hmac = support_hmac
        if self.type_of_crypto == self.TYPE_OF_CAESAR:
            self.crypto_actor = Caesar(letters=self.caesar_letters)
        elif self.type_of_crypto == self.TYPE_OF_TRANSPOSITION:
            self.crypto_actor = Transposition()

    # 디피 헬만 키 교환하기 위해 사용되는 함수
    # p,g 값을 디피헬만 모듈에서 만들게하고 내 개인키를 정함
    # p,g값과 개인키로 만든 g^개인키 값을 공유
    def make_key_exchange(self):
        self.PAG = DiffieHellman.make_random_prime_and_g()
        self.__PRIVATE_key = DiffieHellman.make_own_private_key()

        # 값 계산 p, g, (g^개인키) mod p
        p = self.PAG[0]
        g = self.PAG[1]
        sharekey = (g ** self.__PRIVATE_key) % p

        self.client_connection.send(('[PAG]' + str(p) + ' ' + str(self.PAG[1])).encode('utf-8'))
        self.client_connection.send(('[MOD]' + str(sharekey)).encode('utf-8'))

    # 수신된 메세지에 대하여 종류별 작업
    # HMAC은 간단하게 hmac 내장 모듈 사용
    # 메세지는 "[종류]내용"의 형식이며 구분은 정규식으로 판단
    # 초기 디피헬만 키 교환을 위해 p,g값과 서로의 개인키를 이용한 연산 값을 교환후 최종적으로 시크릿키를 생성
    # 리턴 값은 (원하는메세지여부, 내용)으로 완전 잘못된 메세지라면 (False, TYPE_OF_WRONG_MESSAGE) 튜플을 리턴
    def message_check(self, msg):
        message = re.search(self.message_regularexpression, msg)
        type = message.group('type')
        if type == 'PAG':
            self.PAG = list(map(int, message.group('msg_all').split()))
        elif type == 'MOD':
            print(self.PAG, self.__PRIVATE_key, message.group('msg_all'))
            self.__SECRET_key = (int(message.group('msg_all')) ** self.__PRIVATE_key) % self.PAG[0]
            self.crypto_actor.key = self.__SECRET_key

            # 메세지 인증 코드를 지원하게 한다면 객체 생성
            if self.support_hmac:
                self.MAC = hmac.new(bytes(str(self.__SECRET_key), encoding='utf-8'), None, 'SHA512')

            print('공유된 시크릿키 : ' + str(self.__SECRET_key))
        elif type == 'MSG':
            return True, message.group('msg_all')
        elif type == 'HMSG':
            self.is_response_HMSG = True
            if self.support_hmac:
                hmac_value = message.group('hmac_value')
                self.MAC.update(message.group('msg').encode('utf-8'))
                if hmac_value == self.MAC.hexdigest():
                    self.hmac_auth_success = True
                    return True, message.group('msg')
                else:
                    return False, message.group('msg')
            else:
                return True, message.group('msg')

        return False, self.TYPE_OF_WRONG_MESSAGE

    def run_client(self, ui_mode_chat_chatlog_box):
        try:
            self.client_connection = socket(AF_INET, SOCK_STREAM)
            self.client_connection.connect((self.server_ip, self.server_port))
            ui_mode_chat_chatlog_box.append('서버에 접속 중...')
        except ConnectionRefusedError:
            ui_mode_chat_chatlog_box.append('서버 접속 불가')
            return

        ui_mode_chat_chatlog_box.append('서버에 접속하였습니다.' + self.server_ip + ' : ' + str(self.server_port))
        self.make_key_exchange()
        # 반드시 연결이 수립된 후 진행되어야 할 쓰레드
        # 수신 쓰레드 새로 생성
        start_new_thread(self.recvthread, (ui_mode_chat_chatlog_box, ))

    def stop_client(self):
        print('클라이언트 중지')
        self.stop = True

    def send_chat(self, message, ui_mode_chat_chatlog_box):
        original_message = message

        # 메세지를 보내는 것이므로 암호화 모드
        self.crypto_actor.mode = 'encrypt'
        self.crypto_actor.message = message
        message = self.crypto_actor.goEncryptOrDecrypt()
        if self.support_hmac:
            self.MAC.update(message.encode('utf-8'))
            hmac_value = self.MAC.hexdigest()

            ui_mode_chat_chatlog_box.append('나 : ' + original_message + ' (보낸 메세지인증코드-> ' + hmac_value + ')')
            message = '[HMSG]' + hmac_value + ' ' + message
        else:
            ui_mode_chat_chatlog_box.append('나 : ' + original_message)
            message = '[MSG]' + message

        print(message)
        original_message = ''

        self.client_connection.send(message.encode('utf-8'))

    def recvthread(self, ui_mode_chat_chatlog_box):
        while True:
            try:
                buf = self.client_connection.recv(self.RECV_BUFFER)
                if (not buf) | self.stop:
                    break
                buf = buf.decode('utf-8')
                buf = self.message_check(buf)

                # 원하는 메세지가 아닐 경우 => False로 나오게 되어있음
                if buf == (False, self.TYPE_OF_WRONG_MESSAGE):
                    continue

                print('[채팅클라이언트] : (받은 메세지) ' + buf[1])

                self.crypto_actor.mode = 'decrypt'
                self.crypto_actor.message = buf[1]
                translated = self.crypto_actor.goEncryptOrDecrypt()

                print('[채팅클라이언트] : (해독 메세지) ' + translated)

                # 챗로그 표시 내용
                # MAC 지원시에 앞서 message_check에서 검사 후 인증완료 메세지 및 인증코드 같이 보여줌
                log_base = '상대방 : ' + translated + ' (원본-> ' + buf[1] + ')'

                if self.support_hmac:
                    if self.is_response_HMSG:
                        log_extra = '[HMAC-메세지인증완료]'
                        if not self.hmac_auth_success:
                            log_extra = '[HMAC-메세지인증실패]'
                        log_extra = log_extra + '(메세지인증코드-> ' + self.MAC.hexdigest() + ')'
                    else:
                        log_extra = '[HMAC-인증코드가 오지 않음(인증실패)]'
                else:
                    if self.is_response_HMSG:
                        log_extra = '[일반채팅-인증코드가 왔지만 현재 내가 인증사용모드가 아님]'
                    else:
                        log_extra = '[일반채팅-인증을 사용하지 않음]'


                ui_mode_chat_chatlog_box.append(log_base + log_extra)
            except ConnectionAbortedError:
                ui_mode_chat_chatlog_box.append('연결 종료.')
                break
        self.client_connection.close()

