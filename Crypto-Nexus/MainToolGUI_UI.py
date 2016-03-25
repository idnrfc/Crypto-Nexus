"""
개발환경 : PyQt5 x64, Python 3.4.3 x64, Windows 8.1 x64
파일 : MainToolGUI_UI.py
내용 : UI의 기본 구성을 위한 파이썬 코드로, 그냥 매우 길어서 분리해놨음...ㅡ,.ㅡ
"""


from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from _thread import *
import sys
import urllib.request


class MainToolGUI_UI():    

    # 타입 지정을 위한 변수... 그냥 자주 쓰는거
    TYPE_OF_CAESAR = 0
    TYPE_OF_TRANSPOSITION = 1
    TYPE_OF_AFFINE = 2
    TYPE_OF_SUBSTITUTION = 3
    TYPE_OF_VIGENERE = 4
    TYPE_OF_RSA = 5
    TYPE_OF_DES = 6
    TYPE_OF_TDES = 7
    
    MODE_OF_CRYPTO = 0
    MODE_OF_CHAT = 1

    CRPYTO_OTP_VALUE = ''

    # 프로그램 전체적인 구조는 메뉴와 메뉴에 따른 콘텐츠 레이아웃
    # 메뉴는 고정이고 콘텐츠는 바뀐다.
    app_menu_layout = QVBoxLayout()
    app_content_layout = QVBoxLayout()

    def __init__(self):

        # 조그마한 알림창, 재사용시 show를 한다.
        self.alert_window = QDialog()
        self.alert_window_layout = QVBoxLayout()
        self.alert_window_button = QPushButton('')
        self.alert_window_layout.addWidget(self.alert_window_button)
        self.alert_window.setLayout(self.alert_window_layout)
        self.alert_window_button.setMinimumSize(300,66)
        self.alert_window.setModal(True)
        self.alert_window.setWindowTitle('으아니! :p')
        self.alert_window.setWindowFlags(Qt.Tool)
        self.alert_window_button.clicked.connect(self.alert_window.close)



        # 프로그램 루트 윈도우 UI 세팅 1 - 정렬하기
        self.app_content_layout.setAlignment(Qt.AlignTop)
        self.app_menu_layout.setAlignment(Qt.AlignTop)
        self.ui_mode_crypto_attack_button_layout=None

        """
            일반 암/복호화 그룹박스 레이아웃
        """
        # 암/복호화 그룹박스 레이아웃
        self.mode_crypto_hbox_layout = QHBoxLayout()
        self.mode_crypto_hbox_layout.setAlignment(Qt.AlignLeft)
        self.mode_crypto_groupbox                = QGroupBox('일반')
        self.mode_crypto_groupbox.setLayout(self.mode_crypto_hbox_layout)
        self.mode_crypto_groupbox.setMinimumWidth(500)


        # 크립토 그룹박스에 들어갈 소메뉴들을 세팅한다.
        self.mode_crypto_radio_button_caesar        = QRadioButton('시저')
        self.mode_crypto_radio_button_transposition = QRadioButton('트랜스포지션')
        self.mode_crypto_radio_button_affine        = QRadioButton('아핀')
        self.mode_crypto_radio_button_substitution  = QRadioButton('서브스티튜션')
        self.mode_crypto_radio_button_vigenere      = QRadioButton('비제네르')
        #self.mode_crypto_radio_button_rsa           = QRadioButton('RSA')
        self.mode_crypto_radio_button_des           = QRadioButton('DES')
        self.mode_crypto_radio_button_tdes           = QRadioButton('Triple DES')
        self.mode_crypto_radio_button_caesar.setChecked(True)

        # 그룹박스 안에 사용할 버튼 넣기
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_caesar)
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_transposition)
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_affine)
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_substitution)
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_vigenere)
        #self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_rsa)
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_des)
        self.mode_crypto_hbox_layout.addWidget(self.mode_crypto_radio_button_tdes)

        # 각 모드 버튼마다 연결된 이벤트를 지정
        self.mode_crypto_radio_button_caesar.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_CAESAR))
        self.mode_crypto_radio_button_transposition.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_TRANSPOSITION))
        self.mode_crypto_radio_button_affine.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO,self.TYPE_OF_AFFINE))
        self.mode_crypto_radio_button_substitution.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_SUBSTITUTION))
        self.mode_crypto_radio_button_vigenere.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_VIGENERE))
        #self.mode_crypto_radio_button_rsa.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_RSA))
        self.mode_crypto_radio_button_des.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_DES))
        self.mode_crypto_radio_button_tdes.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CRYPTO, self.TYPE_OF_TDES))

        """
            채팅 암/복호화 그룹박스 레이아웃
        """
        self.mode_chat_hbox_layout = QHBoxLayout()
        self.mode_chat_hbox_layout.setAlignment(Qt.AlignHCenter)
        self.mode_chat_groupbox = QGroupBox('채팅')
        self.mode_chat_groupbox.setLayout(self.mode_chat_hbox_layout)
        self.mode_chat_groupbox.setMinimumWidth(50)


        # 채팅 그룹박스에 들어갈 소메뉴들을 세팅한다.
        self.mode_chat_radio_button_caesar        = QRadioButton('시저')

        # 그룹박스 안에 사용할 버튼 넣기
        self.mode_chat_hbox_layout.addWidget(self.mode_chat_radio_button_caesar)

        # 각 모드 버튼마다 연결된 이벤트를 지정
        self.mode_chat_radio_button_caesar.toggled.connect(partial(self.make_app_content_ui, self.MODE_OF_CHAT,self.TYPE_OF_CAESAR))


        """
            프로그램 모드 루트 그룹박스 레이아웃
        """
        self.app_mode_hbox_layout = QHBoxLayout()
        self.app_mode_hbox_layout.addWidget(self.mode_crypto_groupbox)
        self.app_mode_hbox_layout.addWidget(self.mode_chat_groupbox)

        self.app_mode_groupbox = QGroupBox('프로그램 모드')
        self.app_mode_groupbox.setMaximumHeight(150)
        self.app_mode_groupbox.setMaximumWidth(615)
        self.app_mode_groupbox.setLayout(self.app_mode_hbox_layout)

        # 프로그램 루트 윈도우 UI 세팅 2 - 마무리 세팅
        # 프로그램 초기 실행시에는 crypto ui(시저 사이퍼)를 먼저 선 보임
        self.current_ui_type = -1
        self.make_app_content_ui(self.MODE_OF_CRYPTO, self.TYPE_OF_CAESAR, True)

        self.app_menu_layout.addWidget(self.app_mode_groupbox)
        self.app_menu_layout.addLayout(self.app_content_layout)
        self.setLayout(self.app_menu_layout)
        self.setGeometry(150, 150, 900, 550)


    def make_crypto_ui_renew(self):
        """
            일반 암/복호화 모드 사용시 사용되는 콘텐츠 UI 다시 만들기
            일반적으로 글자나 버튼 길이 등등
        """

        # 일반과 공격 UI 전환을 위한 구성
        self.ui_mode_crypto_attack_radio_groupbox = QGroupBox('일반/공격')
        self.ui_mode_crypto_attack_radio_groupbox_layout = QHBoxLayout()
        self.ui_mode_crypto_attack_normal_radiobox = QRadioButton('일반')
        self.ui_mode_crypto_attack_attack_radiobox = QRadioButton('공격')
        self.ui_mode_crypto_attack_radio_groupbox_layout.addWidget(self.ui_mode_crypto_attack_normal_radiobox)
        self.ui_mode_crypto_attack_radio_groupbox.setLayout(self.ui_mode_crypto_attack_radio_groupbox_layout)
        self.ui_mode_crypto_attack_radio_groupbox_layout.addWidget(self.ui_mode_crypto_attack_attack_radiobox)



        # 텍스트/파일 종류 선택 그룹박스
        # 그냥 텍스트로 넣을건지 파일로 넣을건지 선택 가능하도록 조정
        self.ui_mode_crypto_input_method_groupbox_layout = QVBoxLayout()
        self.ui_mode_crypto_input_method_groupbox = QGroupBox('암/복호화 입력 종류')
        self.ui_mode_crypto_input_text_radiobutton = QRadioButton('텍스트')
        self.ui_mode_crypto_input_file_radiobutton = QRadioButton('파일')
        self.ui_mode_crypto_input_method_groupbox_layout.addWidget(self.ui_mode_crypto_input_text_radiobutton)
        self.ui_mode_crypto_input_method_groupbox_layout.addWidget(self.ui_mode_crypto_input_file_radiobutton)
        self.ui_mode_crypto_input_method_groupbox.setMaximumWidth(200)
        self.ui_mode_crypto_input_method_groupbox.setLayout(self.ui_mode_crypto_input_method_groupbox_layout)

        # 파일 접근 방법 그룹박스
        # 파일로 넣었을 때, 그냥 텍스트파일인지 바이너리파일인지 구분하도록 함
        self.ui_mode_crypto_file_accesstype_groupbox_layout = QVBoxLayout()
        self.ui_mode_crypto_file_accesstype_groupbox = QGroupBox('파일 암호화 접근 방법')
        self.ui_mode_crypto_file_type_text_radiobutton = QRadioButton('텍스트(Windows에서는 LF->CR+LF)')
        self.ui_mode_crypto_file_type_binary_radiobutton = QRadioButton('바이너리(zip, exe, ...)')
        self.ui_mode_crypto_file_accesstype_groupbox_layout.addWidget(self.ui_mode_crypto_file_type_text_radiobutton)
        self.ui_mode_crypto_file_accesstype_groupbox_layout.addWidget(self.ui_mode_crypto_file_type_binary_radiobutton)
        self.ui_mode_crypto_file_accesstype_groupbox.setMaximumWidth(400)
        self.ui_mode_crypto_file_accesstype_groupbox.setLayout(self.ui_mode_crypto_file_accesstype_groupbox_layout)

        # OTP 사용 여부 그룹박스
        # 복호화시에 OTP를 사용... OTP가 틀리면 복호화를 시도 못하게 함
        # OTP그림, 쓰레드를 사용해서 그림을 구글서버에서 가져온다
        # 구글 auth 앱을 설치해서 OTP 값을 스마트폰으로 확인 가능
        self.ui_mode_crypto_otp_groupbox_layout = QHBoxLayout()
        self.ui_mode_crypto_otp_option_layout = QVBoxLayout()
        self.ui_mode_crypto_otp_groupbox = QGroupBox('복호화시 OTP 2차인증')
        self.ui_mode_crypto_otp_yes_radiobutton = QRadioButton('사용')
        self.ui_mode_crypto_otp_no_radiobutton = QRadioButton('미사용')
        self.ui_mode_crypto_otp_input_textbox = QLineEdit()
        self.ui_mode_crypto_otp_input_textbox.setPlaceholderText('ex) OTP값')
        self.ui_mode_crypto_otp_option_layout.addWidget(self.ui_mode_crypto_otp_no_radiobutton)
        self.ui_mode_crypto_otp_option_layout.addWidget(self.ui_mode_crypto_otp_yes_radiobutton)
        self.ui_mode_crypto_otp_option_layout.addWidget(self.ui_mode_crypto_otp_input_textbox)

        self.ui_mode_crypto_otp_qrcode_layout = QHBoxLayout()
        self.ui_mode_crypto_otp_qrcode_image_button = QPushButton()
        self.ui_mode_crypto_otp_qrcode_image_button.setFixedSize(110, 110)
        self.ui_mode_crypto_otp_qrcode_option_layout = QVBoxLayout()

        self.ui_mode_crypto_otp_qrcode_new_create_button = QPushButton('새로 생성하기')
        self.ui_mode_crypto_otp_qrcode_nickname_layout = QHBoxLayout()
        self.ui_mode_crypto_otp_qrcode_nickname_label = QLabel('닉네임')
        self.ui_mode_crypto_otp_qrcode_nickname_textbox = QLineEdit()
        self.ui_mode_crypto_otp_qrcode_nickname_textbox.setText('NICK')
        self.ui_mode_crypto_otp_qrcode_nickname_layout.addWidget(self.ui_mode_crypto_otp_qrcode_nickname_label)
        self.ui_mode_crypto_otp_qrcode_nickname_layout.addWidget(self.ui_mode_crypto_otp_qrcode_nickname_textbox)
        self.ui_mode_crypto_otp_qrcode_key_layout = QHBoxLayout()
        self.ui_mode_crypto_otp_qrcode_key_label = QLabel('생성키')
        self.ui_mode_crypto_otp_qrcode_key_textbox = QLineEdit()
        self.ui_mode_crypto_otp_qrcode_key_textbox.setText('INTERNETSECURITY')
        self.ui_mode_crypto_otp_qrcode_key_layout.addWidget(self.ui_mode_crypto_otp_qrcode_key_label)
        self.ui_mode_crypto_otp_qrcode_key_layout.addWidget(self.ui_mode_crypto_otp_qrcode_key_textbox)

        self.ui_mode_crypto_otp_qrcode_option_layout.addWidget(self.ui_mode_crypto_otp_qrcode_new_create_button)
        self.ui_mode_crypto_otp_qrcode_option_layout.addLayout(self.ui_mode_crypto_otp_qrcode_nickname_layout)
        self.ui_mode_crypto_otp_qrcode_option_layout.addLayout(self.ui_mode_crypto_otp_qrcode_key_layout)

        self.ui_mode_crypto_otp_qrcode_layout.addWidget(self.ui_mode_crypto_otp_qrcode_image_button)
        self.ui_mode_crypto_otp_qrcode_layout.addLayout(self.ui_mode_crypto_otp_qrcode_option_layout)

        self.ui_mode_crypto_otp_groupbox_layout.addLayout(self.ui_mode_crypto_otp_option_layout)
        self.ui_mode_crypto_otp_groupbox_layout.addLayout(self.ui_mode_crypto_otp_qrcode_layout)
        self.ui_mode_crypto_otp_groupbox.setLayout(self.ui_mode_crypto_otp_groupbox_layout)




        # 프로그램 옵션에 대한 상위 레이아웃 구성
        # 옵션 3가지 구성(일반/공격, 문자열/파일, 텍스트타입/바이너리타입, OTP사용여부 및 OTP그림
        self.ui_mode_crypto_option_root_layout = QHBoxLayout()
        self.ui_mode_crypto_option_root_layout.setAlignment(Qt.AlignLeft)
        self.ui_mode_crypto_option_root_layout.addWidget(self.ui_mode_crypto_attack_radio_groupbox)
        self.ui_mode_crypto_option_root_layout.addWidget(self.ui_mode_crypto_input_method_groupbox)
        self.ui_mode_crypto_option_root_layout.addWidget(self.ui_mode_crypto_file_accesstype_groupbox)
        self.ui_mode_crypto_option_root_layout.addWidget(self.ui_mode_crypto_otp_groupbox)

        # 프로그램 입력값 및 컨트롤 구성 : 입력
        self.ui_mode_crypto_input_and_key_layout = QHBoxLayout()
        self.ui_mode_crypto_input_label = QLabel('입력')
        self.ui_mode_crypto_input_textbox = QLineEdit()
        self.ui_mode_crypto_input_textbox.setPlaceholderText('여기에 암/복호화할 암호문이나 평문을 입력하세요.')
        self.ui_mode_crypto_input_and_key_layout.addWidget(self.ui_mode_crypto_input_label)
        self.ui_mode_crypto_input_and_key_layout.addWidget(self.ui_mode_crypto_input_textbox)

        # 프로그램 입력값 및 컨트롤 구성 : 키
        self.ui_mode_crypto_key_label = QLabel('키')
        self.ui_mode_crypto_key_textbox = QLineEdit()
        self.ui_mode_crypto_key_textbox.setMaximumWidth(250)
        self.ui_mode_crypto_input_and_key_layout.addWidget(self.ui_mode_crypto_key_label)
        self.ui_mode_crypto_input_and_key_layout.addWidget(self.ui_mode_crypto_key_textbox)

        # 프로그램 입력값 및 컨트롤 구성 : 문자열
        self.ui_mode_crypto_letters_layout = QHBoxLayout()
        self.ui_mode_crypto_letters_label = QLabel('문자(심볼셋)')
        self.ui_mode_crypto_letters_textbox = QLineEdit()
        self.ui_mode_crypto_letters_textbox.setPlaceholderText('ex) ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        # 프로그램 입력값 및 컨트롤 구성 : 출력
        self.ui_mode_crypto_output_layout = QHBoxLayout()
        self.ui_mode_crypto_output_label = QLabel('결과')
        self.ui_mode_crypto_output_textbox = QLineEdit()
        self.ui_mode_crypto_output_textbox.setReadOnly(True)
        self.ui_mode_crypto_letters_layout.addWidget(self.ui_mode_crypto_letters_label)
        self.ui_mode_crypto_letters_layout.addWidget(self.ui_mode_crypto_letters_textbox)

        # 프로그램 입력값 및 컨트롤 구성 : 파일 입력
        self.ui_mode_crypto_file_input_layout = QHBoxLayout()
        self.ui_mode_crypto_inputfile_label = QLabel('파일 입력')
        self.ui_mode_crypto_inputfile_label.setMaximumWidth(60)
        self.ui_mode_crypto_inputfile_button = QPushButton('파일 찾아보기...')
        self.ui_mode_crypto_file_input_layout.addWidget(self.ui_mode_crypto_inputfile_label)
        self.ui_mode_crypto_file_input_layout.addWidget(self.ui_mode_crypto_inputfile_button)

        # 프로그램 입력값 및 컨트롤 구성 : 파일 출력
        self.ui_mode_crypto_file_output_layout = QHBoxLayout()
        self.ui_mode_crypto_outputfile_label = QLabel('파일 출력')
        self.ui_mode_crypto_outputfile_label.setMaximumWidth(60)
        self.ui_mode_crypto_outputfile_button = QPushButton('파일 찾아보기...')
        self.ui_mode_crypto_output_layout.addWidget(self.ui_mode_crypto_output_label)
        self.ui_mode_crypto_output_layout.addWidget(self.ui_mode_crypto_output_textbox)
        self.ui_mode_crypto_file_output_layout.addWidget(self.ui_mode_crypto_outputfile_label)
        self.ui_mode_crypto_file_output_layout.addWidget(self.ui_mode_crypto_outputfile_button)

        # 프로그램 입력값 및 컨트롤 구성 : 암/복호화 버튼 생성
        self.ui_mode_crypto_encrypt_button = QPushButton('암호화')
        self.ui_mode_crypto_decrypt_button = QPushButton('복호화')


        # 암호화된 문장을 공격할 때 쓰는 UI구성
        self.ui_mode_crypto_attack_root_layout = QHBoxLayout()
        self.ui_mode_crypto_attack_button_layout = QVBoxLayout()
        self.ui_mode_crypto_attack_dictionary_attack_groupbox = QGroupBox('사전 공격')
        self.ui_mode_crypto_attack_dictionary_attack_layout = QVBoxLayout()
        self.ui_mode_crypto_attack_log = QTextEdit()
        self.ui_mode_crypto_attack_log.setReadOnly(True)
        self.ui_mode_crypto_attack_bruteforce_button = QPushButton('브루트포스')
        self.ui_mode_crypto_attack_bruteforce_button.setMinimumHeight(80)
        self.ui_mode_crypto_attack_dictionary_attack_button = QPushButton('공격 시작')
        self.ui_mode_crypto_attack_dictionary_attack_button.setMinimumHeight(50)
        self.ui_mode_crypto_attack_dictionary_attack_next_button = QPushButton('다음')
        self.ui_mode_crypto_attack_dictionary_attack_stop_button = QPushButton('중지')

        self.ui_mode_crypto_attack_dictionary_attack_layout.addWidget(self.ui_mode_crypto_attack_dictionary_attack_button)
        self.ui_mode_crypto_attack_dictionary_attack_layout.addWidget(self.ui_mode_crypto_attack_dictionary_attack_next_button)
        self.ui_mode_crypto_attack_dictionary_attack_layout.addWidget(self.ui_mode_crypto_attack_dictionary_attack_stop_button)
        self.ui_mode_crypto_attack_dictionary_attack_groupbox.setLayout(self.ui_mode_crypto_attack_dictionary_attack_layout)
        self.ui_mode_crypto_attack_button_layout.addWidget(self.ui_mode_crypto_attack_bruteforce_button)
        self.ui_mode_crypto_attack_button_layout.addWidget(self.ui_mode_crypto_attack_dictionary_attack_groupbox)
        self.ui_mode_crypto_attack_root_layout.addWidget(self.ui_mode_crypto_attack_log)
        self.ui_mode_crypto_attack_root_layout.addLayout(self.ui_mode_crypto_attack_button_layout)

        # 앱 콘텐츠 UI에 최종 등록
        self.app_content_layout.addLayout(self.ui_mode_crypto_option_root_layout)
        self.app_content_layout.addLayout(self.ui_mode_crypto_input_and_key_layout)
        self.app_content_layout.addLayout(self.ui_mode_crypto_letters_layout)
        self.app_content_layout.addLayout(self.ui_mode_crypto_output_layout)
        self.app_content_layout.addLayout(self.ui_mode_crypto_file_input_layout)
        self.app_content_layout.addLayout(self.ui_mode_crypto_file_output_layout)
        self.app_content_layout.addWidget(self.ui_mode_crypto_encrypt_button)
        self.app_content_layout.addWidget(self.ui_mode_crypto_decrypt_button)
        self.app_content_layout.addLayout(self.ui_mode_crypto_attack_root_layout)

        """
            이벤트 핸들러 등록은 마지막에...
            나중에 쓰레드 좀 더 파고들면 에러 원인을 좀 더 다룰듯
        """
        # 일부러 뒤로 빼놓음 - 이벤트 연결시 해당 함수 안의 내용물 객체들이 먼저 생성 되어있어야함

        # 일반/공격, 텍스트/파일, 순수텍스트/바이너리, OTP사용/미사용 옵션 라디오버튼에 이벤트 지정
        self.ui_mode_crypto_attack_normal_radiobox.toggled.connect(partial(self.event_crypto_act_mode_changed, False))
        self.ui_mode_crypto_attack_attack_radiobox.toggled.connect(partial(self.event_crypto_act_mode_changed, True))
        self.ui_mode_crypto_input_text_radiobutton.toggled.connect(partial(self.crypto_input_method_changed, 0))
        self.ui_mode_crypto_input_file_radiobutton.toggled.connect(partial(self.crypto_input_method_changed, 1))
        self.ui_mode_crypto_file_type_text_radiobutton.toggled.connect(partial(self.crypto_file_access_method_changed, 0))
        self.ui_mode_crypto_file_type_binary_radiobutton.toggled.connect(partial(self.crypto_file_access_method_changed, 1))
        self.ui_mode_crypto_otp_yes_radiobutton.toggled.connect(partial(self.event_crypto_otp_usage, True))
        self.ui_mode_crypto_otp_no_radiobutton.toggled.connect(partial(self.event_crypto_otp_usage, False))

        # QR코드 이미지 버튼 클릭시 이벤트 지정(웹 브라우저로 띄우기)
        # 새로 생성하기 버튼 클릭시 이벤트 지정(다시 생성해서 버튼에 씌우기)
        self.ui_mode_crypto_otp_qrcode_image_button.clicked.connect(self.event_qrcode_button_clicked)
        self.ui_mode_crypto_otp_qrcode_new_create_button.clicked.connect(self.event_qrcode_new_create_button_clicked)

        # 파일을 사용자가 선택할 수 있도록 버튼 이벤트 등록, 0은 읽기, 1은 파일 저장 다이얼로그
        self.ui_mode_crypto_inputfile_button.clicked.connect(partial(self.file_io_clicked, 0))
        self.ui_mode_crypto_outputfile_button.clicked.connect(partial(self.file_io_clicked, 1))


        # 사전 공격 계속 진행과 중지버튼에 대한 이벤트 지정
        self.ui_mode_crypto_attack_dictionary_attack_next_button.clicked.connect(partial(self.event_dictionary_attack_next_or_stop_clicked, True))
        self.ui_mode_crypto_attack_dictionary_attack_stop_button.clicked.connect(partial(self.event_dictionary_attack_next_or_stop_clicked, False))

        # 초기 실행시 옵션 선택 사항(반드시 이벤트 등록 후) - 일반/텍스트/텍스트타입
        self.ui_mode_crypto_attack_normal_radiobox.setChecked(True)
        self.ui_mode_crypto_input_text_radiobutton.setChecked(True)
        self.ui_mode_crypto_file_type_text_radiobutton.setChecked(True)
        self.ui_mode_crypto_otp_no_radiobutton.setChecked(True)

    def make_qr_code_image(self, nickname, secret):

        # QR코드 가져오기 및 설정하기 시작
        try:
            qr_code = QIcon()
            self.ui_mode_crypto_otp_qrcode_image_button.setIcon(qr_code)
            self.ui_mode_crypto_otp_qrcode_new_create_button.setText('갖고 오는 중...')

            # qr코드 이미지를 구글에서 가져온다...
            # 입력 값은 닉네임과 시크릿키
            # 한글이 입력되어도 읽을 수 있게 URL 포맷으로 인코드 변환
            target = 'http://chart.apis.google.com/chart?cht=qr&chs=150x150&chl=otpauth://totp/'
            target = target + urllib.parse.quote(nickname) + '?secret=' + urllib.parse.quote(secret)

            image_data = urllib.request.urlopen(target).read()

            # 버튼에 이미지 등록을 하기 위해 QPixmap과 QIcon를 사용한다.. 이미지를 QIocn으로 등록
            image = QPixmap()
            image.loadFromData(image_data)
            qr_code.addPixmap(image)
            qr_code_size = QSize()
            qr_code_size.setHeight(150)
            qr_code_size.setWidth(150)

            # 시크릿 키를 qr코드 생성 후 쓰는 걸로 지정
            self.CRPYTO_OTP_VALUE = secret

            self.ui_mode_crypto_otp_qrcode_image_button.setIcon(qr_code)
            self.ui_mode_crypto_otp_qrcode_image_button.setIconSize(qr_code_size)
            self.ui_mode_crypto_otp_qrcode_new_create_button.setText('새로 생성하기')
        except:
            print('뭔가 오류.... 인터넷이 안 되나?', sys.exc_info())

    def make_chat_ui_renew(self):
        # 채팅 모드 옵션 UI
        # 서버/클라이언트 , 해쉬 메세지인증코드 지원여부
        self.ui_mode_chat_option_layout = QHBoxLayout()
        self.ui_mode_chat_type_groupbox = QGroupBox('서버/클라이언트')
        self.ui_mode_chat_type_groupbox_layout = QVBoxLayout()
        self.ui_mode_chat_type_server_radiobutton = QRadioButton('서버')
        self.ui_mode_chat_type_client_radiobutton = QRadioButton('클라이언트')
        self.ui_mode_chat_support_hmac_groupbox = QGroupBox('메세지인증코드(HMAC)')
        self.ui_mode_chat_support_hmac_groupbox_layout = QVBoxLayout()
        self.ui_mode_chat_support_hmac_no_radiobutton = QRadioButton('사용 안 함')
        self.ui_mode_chat_support_hmac_yes_radiobutton = QRadioButton('사용')

        self.ui_mode_chat_type_groupbox_layout.addWidget(self.ui_mode_chat_type_server_radiobutton)
        self.ui_mode_chat_type_groupbox_layout.addWidget(self.ui_mode_chat_type_client_radiobutton)
        self.ui_mode_chat_type_groupbox.setLayout(self.ui_mode_chat_type_groupbox_layout)
        self.ui_mode_chat_support_hmac_groupbox_layout.addWidget(self.ui_mode_chat_support_hmac_no_radiobutton)
        self.ui_mode_chat_support_hmac_groupbox_layout.addWidget(self.ui_mode_chat_support_hmac_yes_radiobutton)
        self.ui_mode_chat_support_hmac_groupbox.setLayout(self.ui_mode_chat_support_hmac_groupbox_layout)
        self.ui_mode_chat_option_layout.addWidget(self.ui_mode_chat_type_groupbox)
        self.ui_mode_chat_option_layout.addWidget(self.ui_mode_chat_support_hmac_groupbox)
        self.ui_mode_chat_support_hmac_yes_radiobutton.setChecked(True)


        # 서버 주소와 포트 번호를 지정하는 UI 설정
        self.ui_mode_chat_connection_layout = QHBoxLayout()
        self.ui_mode_chat_host_label = QLabel('호스트')
        self.ui_mode_chat_port_label = QLabel('포트')
        self.ui_mode_chat_host_text = QLineEdit()
        self.ui_mode_chat_port_text = QLineEdit()
        self.ui_mode_chat_connection_layout.addWidget(self.ui_mode_chat_host_label)
        self.ui_mode_chat_connection_layout.addWidget(self.ui_mode_chat_host_text)
        self.ui_mode_chat_connection_layout.addWidget(self.ui_mode_chat_port_label)
        self.ui_mode_chat_connection_layout.addWidget(self.ui_mode_chat_port_text)

        # 서버생성/서버닫기와 채팅접속/채팅종료 UI 설정
        self.ui_mode_chat_control_layout = QHBoxLayout()
        self.ui_mode_chat_make_server_button = QPushButton('서버 생성')
        self.ui_mode_chat_close_server_button = QPushButton('서버 닫기')
        self.ui_mode_chat_connect_chat_button = QPushButton('채팅 서버 접속')
        self.ui_mode_chat_discoonect_chat_button = QPushButton('채팅 종료')

        self.ui_mode_chat_control_layout.addWidget(self.ui_mode_chat_make_server_button)
        self.ui_mode_chat_control_layout.addWidget(self.ui_mode_chat_close_server_button)
        self.ui_mode_chat_control_layout.addWidget(self.ui_mode_chat_connect_chat_button)
        self.ui_mode_chat_control_layout.addWidget(self.ui_mode_chat_discoonect_chat_button)

        # 채팅 로그가 나오는 곳
        self.ui_mode_chat_chatlog_inputbox_layout = QHBoxLayout()
        self.ui_mode_chat_chatlog_box = QTextEdit()
        self.ui_mode_chat_chatlog_box.setReadOnly(True)
        self.ui_mode_chat_chatlog_inputbox = QLineEdit()
        self.ui_mode_chat_chatlog_send_button = QPushButton('전송')
        self.ui_mode_chat_chatlog_inputbox.setPlaceholderText('여기에 전송할 텍스트를 입력하세요.')
        self.ui_mode_chat_chatlog_inputbox_layout.addWidget(self.ui_mode_chat_chatlog_inputbox)
        self.ui_mode_chat_chatlog_inputbox_layout.addWidget(self.ui_mode_chat_chatlog_send_button)



        # 위에서 만들었던 것을 콘텐츠 UI에 등록하기
        self.app_content_layout.addLayout(self.ui_mode_chat_option_layout)
        self.app_content_layout.addLayout(self.ui_mode_chat_connection_layout)
        self.app_content_layout.addLayout(self.ui_mode_chat_control_layout)
        self.app_content_layout.addWidget(self.ui_mode_chat_chatlog_box)
        self.app_content_layout.addLayout(self.ui_mode_chat_chatlog_inputbox_layout)

        # 채팅 프로그램 옵션에 대한 라디오버튼 이벤트/ 서버 종료 및 클라이언트 종료/ 채팅 전송 및 키 눌림 이벤트 지정
        self.ui_mode_chat_type_server_radiobutton.toggled.connect(partial(self.event_chat_type_changed, True))
        self.ui_mode_chat_type_client_radiobutton.toggled.connect(partial(self.event_chat_type_changed, False))
        self.ui_mode_chat_close_server_button.clicked.connect(partial(self.event_chat_control_server, False))
        self.ui_mode_chat_discoonect_chat_button.clicked.connect(partial(self.event_chat_control_join))
        self.ui_mode_chat_chatlog_inputbox.returnPressed.connect(self.event_chat_send_button)
        self.ui_mode_chat_chatlog_send_button.clicked.connect(self.event_chat_send_button)

    def make_app_content_ui(self, crypto_or_chat, type_of_menu, enabled):
        # 암호화 방법이 바뀌면 선택된 것을 기준으로 실행
        if enabled:
            # 일반 암호와 채팅 암호 프로그램 구분
            # 기본적으로 UI는 유지하지만 다른 프로그램 사용하게 되면 지우고 다시 만들게 함
            if crypto_or_chat == self.MODE_OF_CRYPTO:
                if self.current_ui_type != self.MODE_OF_CRYPTO:
                    self.remove_app_content_ui(self.app_content_layout)
                    self.make_crypto_ui_renew()
                    start_new_thread(self.make_qr_code_image, (self.ui_mode_crypto_otp_qrcode_nickname_textbox.text(),
                                                               self.ui_mode_crypto_otp_qrcode_key_textbox.text()
                                                               )
                                     )
                self.make_app_content_crypto_ui(type_of_menu)
                self.current_ui_type = self.MODE_OF_CRYPTO

                # 일반 암/복호화 기능으로 이동 시에 채팅 기능의 라디오 버튼들을 다 해제한다.
                for i in range(0, self.mode_chat_hbox_layout.count()):
                    self.mode_chat_hbox_layout.itemAt(i).widget().setAutoExclusive(False)
                    self.mode_chat_hbox_layout.itemAt(i).widget().setChecked(False)
                    self.mode_chat_hbox_layout.itemAt(i).widget().setAutoExclusive(True)
            else:
                if self.current_ui_type != self.MODE_OF_CHAT:
                    self.remove_app_content_ui(self.app_content_layout)
                    self.make_chat_ui_renew()
                self.make_app_content_chat_ui(type_of_menu)
                self.current_ui_type = self.MODE_OF_CHAT
                # 채팅 기능으로 이동 시에 일반 암/복호화 기능의 라디오 버튼들을 다 해제한다.
                for i in range(0, self.mode_crypto_hbox_layout.count()):
                    self.mode_crypto_hbox_layout.itemAt(i).widget().setAutoExclusive(False)
                    self.mode_crypto_hbox_layout.itemAt(i).widget().setChecked(False)
                    self.mode_crypto_hbox_layout.itemAt(i).widget().setAutoExclusive(True)

    def make_app_content_crypto_ui(self, type_of_menu):
        print('[일반] 암호 프로그램 : ' + str(type_of_menu))

        try:
            # 재등록 하기 위해 연결 해제
            self.ui_mode_crypto_encrypt_button.clicked.disconnect()
            self.ui_mode_crypto_decrypt_button.clicked.disconnect()
            self.ui_mode_crypto_attack_bruteforce_button.clicked.disconnect()
            self.ui_mode_crypto_attack_dictionary_attack_button.clicked.disconnect()
        # 재연결 방법을 잘 모르겠다;;
        except TypeError:
            pass
        finally:
            # 어떤 메뉴인지 확인하고 메뉴에 맞게 암/복호화 종류 조정
            self.ui_mode_crypto_encrypt_button.clicked.connect(partial(self.determine_encrypt_or_decrypt, type_of_menu, 'encrypt'))
            self.ui_mode_crypto_decrypt_button.clicked.connect(partial(self.determine_encrypt_or_decrypt, type_of_menu, 'decrypt'))

            # 브루투포스 버튼과 사전 공격 버튼에 대한 이벤트 지정
            self.ui_mode_crypto_attack_bruteforce_button.clicked.connect(partial(self.bruteforce_or_dictionary_attack, type_of_menu, True))
            self.ui_mode_crypto_attack_dictionary_attack_button.clicked.connect(partial(self.bruteforce_or_dictionary_attack, type_of_menu, False))

        # 각 메뉴에 따른 추가 UI조작 및 기본 입력값들 제공
        self.test_sample()

        # 기본 세팅
        self.ui_mode_crypto_attack_dictionary_attack_groupbox.setTitle('사전 공격')
        self.ui_mode_crypto_attack_bruteforce_button.setText('브루트포스')
        self.ui_mode_crypto_attack_bruteforce_button.show()

        if type_of_menu == self.TYPE_OF_CAESAR:
            self.ui_mode_crypto_letters_label.setEnabled(True)
            self.ui_mode_crypto_letters_textbox.setEnabled(True)
        elif type_of_menu == self.TYPE_OF_TRANSPOSITION:
            self.ui_mode_crypto_letters_label.setEnabled(False)
            self.ui_mode_crypto_letters_textbox.setEnabled(False)
        elif type_of_menu == self.TYPE_OF_AFFINE:
            self.ui_mode_crypto_key_textbox.setText('2023')
            self.ui_mode_crypto_letters_label.setEnabled(True)
            self.ui_mode_crypto_letters_textbox.setEnabled(True)

        elif type_of_menu == self.TYPE_OF_SUBSTITUTION:
            self.ui_mode_crypto_key_textbox.setText('LFWOAYUISVKMNXPBDCRJTQEGHZ')
            self.ui_mode_crypto_letters_textbox.setText('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            self.ui_mode_crypto_letters_label.setEnabled(True)
            self.ui_mode_crypto_letters_textbox.setEnabled(True)
            self.ui_mode_crypto_attack_bruteforce_button.setText('패턴 공격')

        elif type_of_menu == self.TYPE_OF_VIGENERE:
            self.ui_mode_crypto_key_textbox.setText('PIZZA')
            self.ui_mode_crypto_letters_textbox.setText('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            self.ui_mode_crypto_letters_label.setEnabled(False)
            self.ui_mode_crypto_letters_textbox.setEnabled(False)
            self.ui_mode_crypto_attack_dictionary_attack_groupbox.setTitle('Kasiski 검사')
            self.ui_mode_crypto_attack_bruteforce_button.hide()

        elif type_of_menu == self.TYPE_OF_RSA:
            pass

        elif type_of_menu == self.TYPE_OF_DES:
            self.ui_mode_crypto_key_textbox.setText('12345678')
            self.ui_mode_crypto_letters_label.setEnabled(False)
            self.ui_mode_crypto_letters_textbox.setEnabled(False)
            self.ui_mode_crypto_attack_bruteforce_button.hide()

        elif type_of_menu == self.TYPE_OF_TDES:
            self.ui_mode_crypto_key_textbox.setText('123456781593570045685200')
            self.ui_mode_crypto_letters_label.setEnabled(False)
            self.ui_mode_crypto_letters_textbox.setEnabled(False)
            self.ui_mode_crypto_attack_bruteforce_button.hide()

    def make_app_content_chat_ui(self, type_of_menu):
        print('[채팅] 암호 프로그램 : ' + str(type_of_menu))
        # 기본 IP랑 포트 지정
        self.ui_mode_chat_host_text.setText('127.0.0.1')
        self.ui_mode_chat_port_text.setText('1818')

        # 클라이언트 접속으로 초기 설정
        self.ui_mode_chat_type_client_radiobutton.setChecked(True)

        try:
            # 생성 전에 중복 생성을 막기 위해 핸들링 모두 해지
            self.ui_mode_chat_make_server_button.clicked.disconnect()
            self.ui_mode_chat_connect_chat_button.clicked.disconnect()
        # 재연결 방법을 잘 모르겠다;;
        except TypeError:
            pass
        finally:
            self.ui_mode_chat_make_server_button.clicked.connect(partial(self.event_chat_control_server, True, type_of_menu))
            self.ui_mode_chat_connect_chat_button.clicked.connect(partial(self.event_chat_control_join, True, type_of_menu))

    def remove_app_content_ui(self, layout):
        # 다른 메뉴를 위해 기존 내용을 지우고 메뉴를 다시 만든다.
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.remove_app_content_ui(item.layout())

    # 샘플 집어넣는 함수, 빠른 테스트를 위해...
    def test_sample(self):
        self.ui_mode_crypto_input_textbox.setText('This is sample text for testing')
        self.ui_mode_crypto_key_textbox.setText(str(8))
        self.ui_mode_crypto_letters_textbox.setText(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')