"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : MainToolGUI.py
내용 : 메인, 애플리케이션의 시작, 조작, UI, 잡다한 내용...
"""


from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal

from MainToolGUI_UI import MainToolGUI_UI
from CustomError import CustomError
from ChatServer import ChatServer
from ChatClient import ChatClient
from CryptoCaesar import Caesar
from CryptoTransposition import Transposition
from CryptoAffine import Affine
from CryptoSubStitution import SubStitution
from CryptoVigenere import Vigenere
from CryptoDES import CryptoDES

from _thread import *
import threading
import detectEnglish
import re
import sys
import pyotp
import binascii
import webbrowser
import time
import itertools

PROGRAM_TITLE   = 'Crypto Nexus'
PROGRAM_VERSION = '0.1.3'

"""
    UI 작성의 대부분을 MainToolGUI_UI에 따로 둔다. 이제 뭔가 뭔지 모르겠
"""


class MainToolGUI(QWidget, MainToolGUI_UI):

    # 현재 사용하는 UI 타입, 변하면 다시 지우고 만든다.
    # 'crypto'랑 'chat' 타입
    current_ui_type = 'crypto'

    # 앱에 텍스트를 쓸건지 아니면 파일로 넣을건지
    # False : 앱 내 텍스트, True : 파일
    crypto_method = False

    # 파일로 입/출력 넣을 시에, 파일 넣는 방법
    # False : 텍스트, True : 바이너리
    crypto_file_access_method = False

    # 복호화시 OTP 사용 여부
    crypto_otp_use = False

    # 채팅 객체에 쓰일 녀석들을 미리 만들어둔다.
    chat_connection = None

    # 사전 공격시 필요한 쓰레드에 필요한 신호를 위한 이벤트를 만든다.
    dictionary_attack_log_update_signal = pyqtSignal(str)
    dictionary_thread_event = threading.Event()
    do_more_dictionary_attack = False
    stop_dictionary_attack = False

    def __init__(self):
        super().__init__()


        self.setWindowTitle(PROGRAM_TITLE + PROGRAM_VERSION)
        self.show()

    def check_otp_matching(self, otp_value):

        totp = pyotp.TOTP(self.CRPYTO_OTP_VALUE)
        print("QR코드생성키 : %s, 입력한 OTP : %s, 생성된 OTP키 : %s, 현재 시간 : %s" %
              (self.CRPYTO_OTP_VALUE, otp_value, totp.now(), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
              )
        if otp_value == totp.now():
            return True
        return False

    def determine_encrypt_or_decrypt(self, typeOfMenu, mode):
        print(typeOfMenu)

        # 복호화시 OTP를 사용하는데, 매칭이 안 되면 경고 띄우고 리턴
        if (mode == 'decrypt') & self.crypto_otp_use:
            if not self.check_otp_matching(self.ui_mode_crypto_otp_input_textbox.text()):
                self.alert_window_button.setText('OTP 값이 틀림!\n컴퓨터 시간과 OTP인증기의 시간을 동기화 해보세요.')
                self.alert_window.show()
                return


        cryptoRun = None
        message = self.ui_mode_crypto_input_textbox.text()
        key = self.ui_mode_crypto_key_textbox.text()
        letters = self.ui_mode_crypto_letters_textbox.text()
        sourceType = self.crypto_method
        fileAccessType = self.crypto_file_access_method
        inputFileName = self.ui_mode_crypto_inputfile_button.text()
        outputFileName = self.ui_mode_crypto_outputfile_button.text()

        try:
            if typeOfMenu == self.TYPE_OF_CAESAR:
                # 암호화 객체 초기 설정
                cryptoRun = Caesar(sourceType, mode, message, letters, key, fileAccessType, inputFileName, outputFileName)

                # sourceType이 0이면 파일이 아니다라는 것
                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())

                # 파일로 넣었을 때
                #  텍스트/바이너리 인지 체크 후 실행
                else:
                    cryptoRun.goEncryptOrDecrypt()
            elif typeOfMenu == self.TYPE_OF_TRANSPOSITION:
                cryptoRun = Transposition(sourceType, mode, message, key, fileAccessType, inputFileName, outputFileName)
                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())
                else:
                    cryptoRun.goEncryptOrDecrypt()

            elif typeOfMenu == self.TYPE_OF_AFFINE:
                cryptoRun = Affine(sourceType, mode, message, letters, key, fileAccessType, inputFileName, outputFileName)
                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())
                else:
                    cryptoRun.goEncryptOrDecrypt()


            elif typeOfMenu == self.TYPE_OF_SUBSTITUTION:
                cryptoRun = SubStitution(sourceType, mode, message, letters, key, fileAccessType, inputFileName, outputFileName)
                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())
                else:
                    cryptoRun.goEncryptOrDecrypt()

            elif typeOfMenu == self.TYPE_OF_VIGENERE:
                cryptoRun = Vigenere(sourceType, mode, message, letters, key, fileAccessType, inputFileName, outputFileName)
                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())
                else:
                    cryptoRun.goEncryptOrDecrypt()

            elif typeOfMenu == self.TYPE_OF_RSA:
                pass
            elif typeOfMenu == self.TYPE_OF_DES:

                cryptoRun = CryptoDES(sourceType, mode, message=message, key=key, fileAccessType=fileAccessType,inputFile=inputFileName,outputFile=outputFileName)

                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())
                else:
                    cryptoRun.goEncryptOrDecrypt()
            elif typeOfMenu == self.TYPE_OF_TDES:

                cryptoRun = CryptoDES(sourceType, mode, message=message, key=key, fileAccessType=fileAccessType,inputFile=inputFileName,outputFile=outputFileName, isTriple=True)

                if not sourceType:
                    self.ui_mode_crypto_output_textbox.setText(cryptoRun.goEncryptOrDecrypt())
                else:
                    cryptoRun.goEncryptOrDecrypt()

            cryptoRun = None
        except UnicodeDecodeError:
            # 파일 암/복호화 실패?
            self.alert_window_button.setText('파일 처리 실패\n\n' + str(sys.exc_info()[0]) + '\n' \
                                             + str(sys.exc_info()[1]) + '\n\n' + '바이너리 모드 권장')
            self.alert_window.show()
        except binascii.Error:
            # 가능성 : DES 입력값의 형식이 올바르지 않음
            self.alert_window_button.setText('DES 처리 실패\n\n' + str(sys.exc_info()[0]) + '\n' \
                                             + str(sys.exc_info()[1]) + '\n\n' + '복호화시에 입력값 형식이 올바른가?')
            self.alert_window.show()
        except CustomError as e:
            # 커스텀 예외 상황에 대한 알림메세지, 주로 키 오류
            self.alert_window_button.setText('에러\n\n' + str(sys.exc_info()[0]) + '\n' \
                                             + e.title + '\n' + e.msg)
            self.alert_window.show()
        except:
            # 만일의 경우 에러가 뜬다면 그냥 알림메세지로...
            self.alert_window_button.setText(str(sys.exc_info()))
            self.alert_window.show()
        finally:
            return

    def bruteforce_or_dictionary_attack(self, type_of_menu, is_brute_force):
        message = self.ui_mode_crypto_input_textbox.text()
        letters = self.ui_mode_crypto_letters_textbox.text()
        sourceType = self.crypto_method
        fileAccessType = self.crypto_file_access_method
        inputFileName = self.ui_mode_crypto_inputfile_button.text()

        # 로그창 초기화
        self.ui_mode_crypto_attack_log.setText('')

        # 공격 시작
        try:
            self.dictionary_attack_log_update_signal.disconnect()
        except TypeError:
                pass
        finally:
            # 브루트포스와 사전 공격의 내용이 수시로 업데이트될 UI 위젯 이벤트 지정)
            self.dictionary_attack_log_update_signal.connect(self.signal_dictionary_attack_log_update)

            # 추후에 파일도 지원할 것인지 고민..
            if type_of_menu == self.TYPE_OF_CAESAR:
                attack_run = Caesar(sourceType=sourceType, mode='decrypt', message=message, letters=letters, fileAccessType=fileAccessType, inputFile=inputFileName)
                if is_brute_force:
                    start_new_thread(self.start_bruteforce_attack, (attack_run, len(attack_run.letters)))
                else:
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    len(attack_run.letters)))
            elif type_of_menu == self.TYPE_OF_TRANSPOSITION:
                attack_run = Transposition(sourceType=sourceType, mode='decrypt', message=message, fileAccessType=fileAccessType, inputFile=inputFileName)
                if is_brute_force:
                    start_new_thread(self.start_bruteforce_attack, (attack_run, len(attack_run.message)))
                else:
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    len(attack_run.message)))
            elif type_of_menu == self.TYPE_OF_AFFINE:
                attack_run = Affine(sourceType=sourceType, mode='decrypt', letters=letters, message=message, fileAccessType=fileAccessType, inputFile=inputFileName)
                if is_brute_force:
                    start_new_thread(self.start_bruteforce_attack, (attack_run, len(attack_run.letters) ** 2))
                else:
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    len(attack_run.letters) ** 2))
            elif type_of_menu == self.TYPE_OF_SUBSTITUTION:
                attack_run = SubStitution(sourceType=sourceType, mode='decrypt', letters=letters, message=message, fileAccessType=fileAccessType, inputFile=inputFileName)

                # 서브스티튜션은 예외적으로 브루트포스 대신에 패턴공격 실시
                if is_brute_force:
                    letter_mapping = attack_run.pattern_hack()
                    key, hacked_message = attack_run.key, attack_run.translateMessage()

                    self.dictionary_attack_log_update_signal.emit('패턴 ->\n' + letter_mapping)
                    self.dictionary_attack_log_update_signal.emit('추정 키 : %s\n추정 메세지: %s' % (key, hacked_message))
                else:
                    # 서브스티튜션 키랜덤+사전공격
                    # 서브스티튜션의 모든 키 조합은 너무나도 많은 자원과 시간이 소모된다.
                    # 키 = 랜덤, 횟수 =  999999 제한
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    999999))
            elif type_of_menu == self.TYPE_OF_VIGENERE:
                attack_run = Vigenere(sourceType=sourceType, mode='decrypt', letters=letters, message=message, fileAccessType=fileAccessType, inputFile=inputFileName)

                # 비제네르 사전 공격 : Kasiski 검사
                if not is_brute_force:
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    1))

            elif type_of_menu == self.TYPE_OF_DES:
                attack_run = CryptoDES(sourceType=sourceType, mode='decrypt', message=message, fileAccessType=fileAccessType,inputFile=inputFileName)

                if not is_brute_force:
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    len(attack_run.common_long_keyspace) ** 8))
            elif type_of_menu == self.TYPE_OF_TDES:
                attack_run = CryptoDES(sourceType=sourceType, mode='decrypt', message=message, fileAccessType=fileAccessType,inputFile=inputFileName,isTriple = True)

                if not is_brute_force:
                    start_new_thread(self.start_dictionary_attack, (attack_run,
                                                                    self.dictionary_thread_event,
                                                                    len(attack_run.common_long_keyspace) ** 16))

    def start_bruteforce_attack(self, attack_run, max_try):
        # 브루트포스 진행 시에는 버튼 잠시 비활성화 후 끝나면 활성화
        self.ui_mode_crypto_attack_bruteforce_button.setEnabled(False)
        self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(False)

        for i in range(1, max_try):

            attack_run.key = i

            # 암호화 종류마다 조금 다른 출력 포맷 제공
            if isinstance(attack_run, Affine):
                attack_run.keyA, attack_run.keyB = attack_run.getKeyParts(attack_run.key)
                key_message = '키 : %s (keyA: %s, keyB: %s)' % (attack_run.key, attack_run.keyA, attack_run.keyB)
                if attack_run.gcd(attack_run.keyA, len(attack_run.letters)) != 1:
                    continue
                temp_message = attack_run.decrypt()
            else:
                temp_message = attack_run.goEncryptOrDecrypt()
                key_message = '키 : ' + str(attack_run.key)

            self.dictionary_attack_log_update_signal.emit(key_message + ' -> ' + temp_message)

        self.ui_mode_crypto_attack_bruteforce_button.setEnabled(True)
        self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(True)

    def start_dictionary_attack(self, attack_run, thread_event, max_try):
        self.ui_mode_crypto_attack_bruteforce_button.setEnabled(False)
        self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(False)
        self.ui_mode_crypto_attack_dictionary_attack_next_button.setEnabled(True)
        self.ui_mode_crypto_attack_dictionary_attack_stop_button.setEnabled(True)
        self.ui_mode_crypto_attack_radio_groupbox.setEnabled(False)
        self.app_mode_groupbox.setEnabled(False)

        # 의미있는 문장 갯수
        count = 0

        # 실행 범위의 조정
        for_limit = range(1, max_try)


        # 공격하기 전의 사전 검사 또는 설정 실시
        # DES 실시할 때 쓰는 저장소
        # 랜덤키가 아닌 순차적 키를 위함임
        if isinstance(attack_run, CryptoDES):
            len_letters = len(attack_run.common_long_keyspace)
            pointer_cycle = []
            key_size = 8

            # 초기 키 설정
            attack_run.key = ' ' * 8
            if attack_run.isTriple:
                attack_run.key = ' ' * 16
                key_size = 16
            for i in range(0, key_size, 1):
                pointer_cycle.append(len_letters ** i)
            pointer = [0] * key_size

        # 비제네르 공격하기전 공격해볼만한 키를 조사(Kasiski Examination)
        elif isinstance(attack_run, Vigenere):
            vigenere_keys = attack_run.go_kasiski_examination()
            keyLengthStr = ''
            for keyLength in vigenere_keys:
                keyLengthStr += '%s ' % (keyLength)

            # 키를 조사한 값을 토대로 공격할지 말지 판단
            if keyLengthStr != '':
                self.dictionary_attack_log_update_signal.emit(\
                    'Kasiski 검사의 결과로 공격해볼만한 키의 길이는 (%s) 입니다.' % keyLengthStr)
                for_limit = vigenere_keys
            else:
                self.dictionary_attack_log_update_signal.emit('Kasiski 검사 결과 공격해볼만한 키가 나오지 않았습니다')

        temp_message = ' '

        for i in for_limit:

            # 키 공격을 시간 간격을 두고 실행한다.
            # 나중에 쓰레드 좀 더 공부해야...
            time.sleep(0.001)



            # 공격 중간에도 멈출 수 있도록 선택권 부여
            if self.stop_dictionary_attack:
                self.stop_dictionary_attack = False
                thread_event.clear()
                break

            # 암호화 종류마다 조금 다른 출력 포맷 제공
            if isinstance(attack_run, Affine):
                attack_run.key = i
                attack_run.keyA, attack_run.keyB = attack_run.getKeyParts(attack_run.key)
                key_message = '키 : %s (keyA: %s, keyB: %s)' % (attack_run.key, attack_run.keyA, attack_run.keyB)
                if attack_run.gcd(attack_run.keyA, len(attack_run.letters)) != 1:
                    continue
                temp_message = attack_run.decrypt()
            elif isinstance(attack_run, SubStitution):
                attack_run.key = attack_run.getRandomKey()
                temp_message = attack_run.goEncryptOrDecrypt()
                key_message = '키 : {' + str(attack_run.key)
            elif isinstance(attack_run, CryptoDES):
                # DES의 키 16개까지 도달, 24 길이 키 공격 전환(Triple-DES 키 사용법 중 하나)
                if attack_run.key == '~' * 16:
                    pointer_cycle.clear()
                    for i in range(0, 24, 1):
                        pointer_cycle.append(len_letters ** i)
                    pointer = [0] * 24


                # 가능한 모든 경우의 키를 고려해서 만든 알고리즘
                # ex) 8자리의 문자열 중 각 자리마다 가리키는 pointer를 생성 후, 일정 조건이 되면 다음 문자로 바뀜
                # ex) 00000000 ~ ZZZZZZZZ
                for pc in range(len(pointer)):
                    pointer[pc] = (i // pointer_cycle[pc]) % len_letters

                # 공격에 사용할 키를 만드는 과정
                # 키는 특수문자+숫자+영문 등등 모두 포함한 문자를 모두 사용하여 조합
                attack_run.key = ''
                for pc in range(len(pointer)):
                    attack_run.key = attack_run.common_long_keyspace[pointer[pc]] + attack_run.key


                # 만들어진 키로 DES 복호화를 시도해본다.
                # 키에도 제한이 있어서 잘못된 형태의 키라면 복호화 실패가 된다.
                try:
                    temp_message = attack_run.goEncryptOrDecrypt()
                except (binascii.Error,ValueError,AttributeError):
                    pass
                finally:
                    key_message = '키(공백포함) : {' + str(attack_run.key)
                if len(temp_message.strip()) == 0:
                    temp_message = '(복호화 실패, 키가 안 맞거나 입력이 암호문 포맷(DES)이 아님)'

            elif isinstance(attack_run, Vigenere):
                self.dictionary_attack_log_update_signal.emit(\
                    '키 길이 %s로 시도합니다. %s의 가능한 경우가 있습니다.' % \
                    (i, attack_run.get_kasiski_NUM_MOST_FREQ_LETTERS() ** i))

                freq_score_list = attack_run.get_kaiski_freq_score_list(i)

                # 빈도수 조사 후 각 키 자릿수마다 빈도점수가 높은 문자들을 공개
                for index in range(len(freq_score_list)):
                    high_score_freqs = ''
                    for freqScore in freq_score_list[index]:
                        high_score_freqs += freqScore[0] + ' '
                    self.dictionary_attack_log_update_signal.emit('키 %s번째 자리 후보: %s' % (index + 1, high_score_freqs))

                # 본격적인 공격시작
                # i => 키의 길이
                for indexes in itertools.product(range(attack_run.get_kasiski_NUM_MOST_FREQ_LETTERS()), repeat=i):
                    time.sleep(0.001)
                    # Kasiski 특성상... 반복문 처리 공격 중간에도 멈출 수 있도록 선택권 부여
                    if self.stop_dictionary_attack:
                        # 여기서는 self.stop_dictionary_attack = False를 하지 않는다. 중첩 for 반복문 이기 때문.. 상위도 중지
                        break

                    possibleKey = ''
                    for length in range(i):
                        possibleKey += freq_score_list[length][indexes[length]][0]

                    temp_message = attack_run.translateMessage(possibleKey, attack_run.message.upper())

                    temp_message = attack_run.get_kasiski_proper_casing(temp_message)
                    self.dictionary_attack_log_update_signal.emit('키 공격 시도 : {%s} -> %s' % (possibleKey, temp_message))

                    # 영문 문장인지 검사 후 사용자에게 (다음, 중지) 선택권 제공
                    if detectEnglish.isEnglish(temp_message):
                        count += 1
                        self.dictionary_attack_log_update_signal.emit(\
                             '영문 문장으로 판단 되었습니다. 이것이 맞습니까? 맞다면 중지를, 계속 시도하려면 다음을 눌러주세요.\n')
                        thread_event.wait()

                        # (다음, 중지) 중 어떤 것을 선택하였는가? 중지면 검사 중지
                        if self.do_more_dictionary_attack:
                            thread_event.clear()
                            continue
                        # 선택 기다림의 초기화
                        thread_event.clear()
                        self.dictionary_attack_log_update_signal.emit('\n 마지막으로 고른 메세지는 키 : ' + \
                                                                      str(possibleKey) + ' -> ' + temp_message + '입니다.')
                        break

            else:
                attack_run.key = i
                temp_message = attack_run.goEncryptOrDecrypt()
                key_message = '키 : {' + str(attack_run.key)


            if not isinstance(attack_run, Vigenere):
                self.dictionary_attack_log_update_signal.emit(key_message + '} -> ' + temp_message)

                # 영문 문장인지 검사 후 사용자에게 (다음, 중지) 선택권 제공
                if detectEnglish.isEnglish(temp_message):
                    count += 1
                    self.dictionary_attack_log_update_signal.emit(\
                         '영문 문장으로 판단 되었습니다. 이것이 맞습니까? 맞다면 중지를, 계속 시도하려면 다음을 눌러주세요.\n')
                    thread_event.wait()

                    # (다음, 중지) 중 어떤 것을 선택하였는가? 중지면 검사 중지
                    if self.do_more_dictionary_attack:
                        thread_event.clear()
                        continue
                    # 선택 기다림의 초기화
                    thread_event.clear()
                    self.dictionary_attack_log_update_signal.emit('\n 마지막으로 고른 메세지는 키 : ' + \
                                                                  str(attack_run.key) + ' -> ' + temp_message + '입니다.')
                    break

        if count == 0:
            self.dictionary_attack_log_update_signal.emit('끝날 때까지 의미있는 문장을 하나도 찾지 못했습니다.')
        self.ui_mode_crypto_attack_bruteforce_button.setEnabled(True)
        self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(True)
        self.ui_mode_crypto_attack_dictionary_attack_next_button.setEnabled(False)
        self.ui_mode_crypto_attack_dictionary_attack_stop_button.setEnabled(False)
        self.ui_mode_crypto_attack_radio_groupbox.setEnabled(True)
        self.app_mode_groupbox.setEnabled(True)
        self.stop_dictionary_attack = False # 함수 종료시에 다시 초기화

    def signal_dictionary_attack_log_update(self, data):
        self.ui_mode_crypto_attack_log.append(data)

    def event_dictionary_attack_next_or_stop_clicked(self, is_next):
        if is_next:
            self.do_more_dictionary_attack = True
        else:
            self.do_more_dictionary_attack = False
            self.stop_dictionary_attack = True
            self.ui_mode_crypto_attack_bruteforce_button.setEnabled(True)
            self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(True)
            self.ui_mode_crypto_attack_dictionary_attack_next_button.setEnabled(False)
            self.ui_mode_crypto_attack_dictionary_attack_stop_button.setEnabled(False)
        self.dictionary_thread_event.set()

    def event_qrcode_button_clicked(self):
        # qr코드 이미지를 웹으로 띄운다.
        # 입력 값은 닉네임과 시크릿키
        nickname = self.ui_mode_crypto_otp_qrcode_nickname_textbox.text()
        secret = self.ui_mode_crypto_otp_qrcode_key_textbox.text()
        target = 'http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl=otpauth://totp/'
        target = target + nickname + '?secret=' + secret

        webbrowser.open(target)

    def event_qrcode_new_create_button_clicked(self):
        # 입력값에 대하여 간단한 검사
        nickname = self.ui_mode_crypto_otp_qrcode_nickname_textbox.text()
        secret = self.ui_mode_crypto_otp_qrcode_key_textbox.text()

        # 시크릿값 정규식으로 검사
        # Base 32 -> a~z, A~Z, 2~7
        # 기본 16으로 최소 길이 제한
        regular = re.fullmatch('[a-zA-Z2-7]{16}', secret)
        if regular == None:
            self.alert_window_button.setText('생성 불가, \n키 값은 반드시 알파벳이나 숫자 2~7로 조합해서 16자 필요')
            self.alert_window.show()
            return
        start_new_thread(self.make_qr_code_image, (nickname, secret))

    def event_crypto_otp_usage(self, use_otp, enabled):
        # OTP 사용/미사용 버튼에 따른 스위치
        if enabled:
            self.crypto_otp_use = use_otp
            self.ui_mode_crypto_otp_input_textbox.setEnabled(use_otp)
            self.ui_mode_crypto_otp_qrcode_image_button.setEnabled(use_otp)
            self.ui_mode_crypto_otp_qrcode_new_create_button.setEnabled(use_otp)
            self.ui_mode_crypto_otp_qrcode_nickname_textbox.setEnabled(use_otp)
            self.ui_mode_crypto_otp_qrcode_key_textbox.setEnabled(use_otp)

    def event_crypto_act_mode_changed(self, is_attack_mode):
        # 공격모드와 일반모드시에는 UI의 활성화 부분이 조금 달라짐
        if is_attack_mode:
            self.ui_mode_crypto_input_text_radiobutton.setChecked(True)
            self.ui_mode_crypto_input_method_groupbox.setEnabled(False)
            self.ui_mode_crypto_encrypt_button.setEnabled(False)
            self.ui_mode_crypto_decrypt_button.setEnabled(False)
            self.ui_mode_crypto_output_textbox.setEnabled(False)
            self.ui_mode_crypto_outputfile_button.setEnabled(False)
            self.ui_mode_crypto_attack_bruteforce_button.setEnabled(True)
            self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(True)
            self.ui_mode_crypto_key_textbox.setEnabled(False)
        else:
            self.ui_mode_crypto_input_method_groupbox.setEnabled(True)
            self.ui_mode_crypto_encrypt_button.setEnabled(True)
            self.ui_mode_crypto_decrypt_button.setEnabled(True)
            self.ui_mode_crypto_output_textbox.setEnabled(True)
            self.ui_mode_crypto_outputfile_button.setEnabled((not is_attack_mode) & self.ui_mode_crypto_input_file_radiobutton.isChecked())
            self.ui_mode_crypto_attack_bruteforce_button.setEnabled(False)
            self.ui_mode_crypto_attack_dictionary_attack_button.setEnabled(False)
            self.ui_mode_crypto_attack_dictionary_attack_next_button.setEnabled(False)
            self.ui_mode_crypto_attack_dictionary_attack_stop_button.setEnabled(False)
            self.ui_mode_crypto_key_textbox.setEnabled(True)

    def file_io_clicked(self, typeOfFileIo):
        if typeOfFileIo == 0:
            self.button_input_file_dialog = QFileDialog()
            self.ui_mode_crypto_inputfile_button.setText(self.button_input_file_dialog.getOpenFileName()[0])
        else:
            self.button_output_file_dialog = QFileDialog()
            self.ui_mode_crypto_outputfile_button.setText(self.button_output_file_dialog.getSaveFileName()[0])

    def crypto_input_method_changed(self, typeOfInputMethod, enabled):
        if enabled and typeOfInputMethod == 0:
            self.ui_mode_crypto_output_textbox.setEnabled(True)
            self.ui_mode_crypto_input_textbox.setEnabled(True)
            self.ui_mode_crypto_inputfile_button.setEnabled(False)
            self.ui_mode_crypto_outputfile_button.setEnabled(False)
            self.crypto_method = False
            self.ui_mode_crypto_file_type_text_radiobutton.setChecked(True)
            self.ui_mode_crypto_file_accesstype_groupbox.setEnabled(False)

        elif enabled and typeOfInputMethod:
            self.ui_mode_crypto_output_textbox.setEnabled(False)
            self.ui_mode_crypto_input_textbox.setEnabled(False)
            self.ui_mode_crypto_inputfile_button.setEnabled(True)
            self.ui_mode_crypto_outputfile_button.setEnabled(True)
            self.crypto_method = True
            self.ui_mode_crypto_file_type_text_radiobutton.setChecked(True)
            self.ui_mode_crypto_file_accesstype_groupbox.setEnabled(True)

    def crypto_file_access_method_changed(self, type_of_method, enabled):
        if enabled and type_of_method == 0:
            self.crypto_file_access_method = False
        if enabled and type_of_method == 1:
            self.crypto_file_access_method = True

    def event_chat_type_changed(self, chat_server_hosting, enabled):
        if enabled:
            # 서버 호스팅이냐 클라이언트 접속이냐 구분, chat_server_hosting이 True면 서버 호스팅
            self.ui_mode_chat_make_server_button.setEnabled(chat_server_hosting)
            self.ui_mode_chat_close_server_button.setEnabled(chat_server_hosting)
            self.ui_mode_chat_connect_chat_button.setEnabled(not chat_server_hosting)
            self.ui_mode_chat_discoonect_chat_button.setEnabled(not chat_server_hosting)

    def event_chat_control_server(self, server_make_switch, type_of_crypto=None):
        # server_make_switch는 서버 생성 버튼과 서버 중지 버튼을 눌렀을 때의 변화
        # 서버 생성
        if server_make_switch:
            server_ip = self.ui_mode_chat_host_text.text()
            server_port = self.ui_mode_chat_port_text.text()
            support_hmac = self.ui_mode_chat_support_hmac_yes_radiobutton.isChecked()
            self.chat_connection = ChatServer(server_ip, server_port, type_of_crypto, support_hmac)
            try:
                start_new_thread(self.chat_connection.run_server, (self.ui_mode_chat_chatlog_box,))
            except:
                print ("뭔가 에러 : ", sys.exc_info())
            self.ui_mode_chat_chatlog_box.append(
                    '서버 생성이 되었습니다. : (' + server_ip + ', ' + server_port + ')')
            self.ui_mode_chat_make_server_button.setEnabled(False)
            self.ui_mode_chat_close_server_button.setEnabled(True)
            self.ui_mode_chat_type_groupbox.setEnabled(False)
            self.ui_mode_chat_support_hmac_groupbox.setEnabled(False)

        # 서버 중지
        else:
            try:
                self.chat_connection.stop_server()
                #self.chat_connection = None
                self.ui_mode_chat_chatlog_box.append('서버가 중지 되었습니다.')
            except:
                print ("뭔가 에러 : ", sys.exc_info())
            self.ui_mode_chat_make_server_button.setEnabled(True)
            self.ui_mode_chat_close_server_button.setEnabled(False)
            self.ui_mode_chat_type_groupbox.setEnabled(True)
            self.ui_mode_chat_support_hmac_groupbox.setEnabled(True)

    def event_chat_control_join(self, join_server_switch, type_of_crypto=None):
        # join_server_switch : 클라이언트가 서버에 접속/해제 할 때 전환
        # True : 접속,  False: 해제

        if join_server_switch:
            server_ip = self.ui_mode_chat_host_text.text()
            server_port = self.ui_mode_chat_port_text.text()
            support_hmac = self.ui_mode_chat_support_hmac_yes_radiobutton.isChecked()
            self.chat_connection = ChatClient(server_ip, server_port, type_of_crypto, support_hmac)
            try:
                start_new_thread(self.chat_connection.run_client, (self.ui_mode_chat_chatlog_box,))
            except:
                print ("뭔가 에러 : ", sys.exc_info())
            self.ui_mode_chat_connect_chat_button.setEnabled(False)
            self.ui_mode_chat_discoonect_chat_button.setEnabled(True)
            self.ui_mode_chat_type_groupbox.setEnabled(False)
            self.ui_mode_chat_support_hmac_groupbox.setEnabled(False)
        else:
            try:
                self.chat_connection.stop_client()
                self.chat_connection.client_connection.close()
                #self.chat_connection = None
                self.ui_mode_chat_chatlog_box.append('연결을 해제하였습니다.')
            except:
                print ("뭔가 에러 : ", sys.exc_info())
            self.ui_mode_chat_connect_chat_button.setEnabled(True)
            self.ui_mode_chat_discoonect_chat_button.setEnabled(False)
            self.ui_mode_chat_type_groupbox.setEnabled(True)
            self.ui_mode_chat_support_hmac_groupbox.setEnabled(True)

    def event_chat_send_button(self):
        if self.chat_connection is not None:
            self.chat_connection.send_chat(self.ui_mode_chat_chatlog_inputbox.text(), self.ui_mode_chat_chatlog_box)

            self.ui_mode_chat_chatlog_inputbox.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    WindowGo = MainToolGUI()
    sys.exit(app.exec_())
