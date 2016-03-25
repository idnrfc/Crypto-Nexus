"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : ChatServer.py
내용 : 채팅 서버 역할, 디피헬만 키교환방식과 HMAC을 지원하는 수/송신
"""

from socket import *
from _thread import *
import re
import DiffieHellman
import hmac

from ChatCommon import ChatCommon
from CryptoCaesar import Caesar
from CryptoTransposition import Transposition


class ChatServer(ChatCommon):

    def __init__(self, server_ip, server_port, type_of_crypto, support_hmac):
        self.server_ip = server_ip
        self.server_port = int(server_port)
        self.server_connection=None
        self.server_socket = None
        self.__PRIVATE_key = 0
        self.__SECRET_key = 0
        self.type_of_crypto = type_of_crypto
        self.support_hmac = support_hmac
        
        if self.type_of_crypto == self.TYPE_OF_CAESAR:
            self.crypto_actor = Caesar(letters=self.caesar_letters)
        elif self.type_of_crypto == self.TYPE_OF_TRANSPOSITION:
            self.crypto_actor = Transposition()

    # 수신된 메세지에 대하여 종류별 작업
    # HMAC은 간단하게 hmac 내장 모듈 사용
    # 메세지는 "[종류]내용"의 형식이며 구분은 정규식으로 판단
    def message_check(self, msg):
        message = re.search(self.message_regularexpression, msg)
        type = message.group('type')
        if type == 'PAG':
            self.PAG = list(map(int, message.group('msg_all').split()))
        elif type == 'MOD':
            print(self.PAG, self.__PRIVATE_key, message.group('msg_all'))
            self.server_socket.send(('[MOD]' + str((self.PAG[1] ** self.__PRIVATE_key) % self.PAG[0])).encode('utf-8'))
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

    def run_server(self, ui_mode_chat_chatlog_box):
        print('서버 생성, 1:1 클라이언트 연결 기다리는 중...')
        self.server_connection = socket(AF_INET, SOCK_STREAM)
        self.server_connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.server_connection.bind((self.server_ip, self.server_port))
        self.server_connection.listen(5)
        self.server_socket, addr = self.server_connection.accept()

        self.__PRIVATE_key = DiffieHellman.make_own_private_key()
        # 반드시 소켓이 수립된 후 진행되어야 할 쓰레드
        # 수신 쓰레드 새로 생성
        start_new_thread(self.recvthread, (ui_mode_chat_chatlog_box, ))

    def stop_server(self):
        print('서버 중지')
        self.stop = True

    def send_chat(self, message, ui_mode_chat_chatlog_box):
        original_message = message

        self.crypto_actor.message = message
        self.crypto_actor.mode = 'encrypt'
        message = self.crypto_actor.goEncryptOrDecrypt()
        if self.support_hmac:
            self.MAC.update(message.encode('utf-8'))
            hmac_value = self.MAC.hexdigest()
            ui_mode_chat_chatlog_box.append('나 : ' + original_message + ' (보낸 메세지인증코드-> ' + hmac_value + ')')
            message = '[HMSG]' + hmac_value + ' ' + message

        else:
            ui_mode_chat_chatlog_box.append('나 : ' + original_message)
            message = '[MSG]' + message

        original_message = ''

        self.server_socket.send(message.encode('utf-8'))

    def recvthread(self, ui_mode_chat_chatlog_box):
        while True:
            try:
                buf = self.server_socket.recv(self.RECV_BUFFER)
                if (not buf) | self.stop:
                    break
                buf = buf.decode('utf-8')

                buf = self.message_check(buf)

                # 원하는 메세지가 아닐 경우 => False로 나오게 되어있음
                if buf == (False, self.TYPE_OF_WRONG_MESSAGE):
                    continue

                print('[채팅서버] : (받은 메세지) ' + buf[1])

                self.crypto_actor.mode = 'decrypt'
                self.crypto_actor.message = buf[1]
                translated = self.crypto_actor.goEncryptOrDecrypt()

                print('[채팅서버] : (해독 메세지) ' + translated)

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
            except ConnectionResetError:
                ui_mode_chat_chatlog_box.append('상대방의 연결이 끊어졌습니다.')
                break

        self.server_connection.close()
        self.server_socket.close()

