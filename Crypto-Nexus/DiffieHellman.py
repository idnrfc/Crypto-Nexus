"""
개발환경 : PyQt5 x64, Python 3.4.3 x64
파일 : DiffieHellman.py
내용 : 디피 헬만 키 교환을 위해 만든 함수들...특히 소수
"""

import sys
import random
import math


# 소수인지 확인
# 짝수는 제외, 1과 2를 제외한 자연수로 검사 실시(3 ~ number-1)


def check_prime(number):
    for i in range(3, int(math.sqrt(number) + 1)):
        if number % i == 0:
            return False
    return True


def make_random_prime_and_g(min=151, max=1000000):
    """
        랜덤한 안전 소수 구해보기
        min에서 max까지 min기준으로 x번째 소피제르맹 소수(이걸로 안전소수 리턴)
        min을 반드시 홀수로
    """

    # 20번째 소수 찾자(최소값으로부터 기준)
    count = 0
    count_match = random.randint(1, 100)

    # 짝수를 피하고 홀수만 101, 101+2.....
    for prime in range(min, max, 2):
        if check_prime(prime):
            # 소피 제르맹 소수 확인 2p+1도 소수인가?
            if check_prime(prime*2+1):
                count += 1
                if count == count_match:
                    print(str(min) + '으로부터 ' + str(count) + '번째 소피 제르맹 소수 : ' + str(prime) \
                          + ', 안전소수(2p+1) : ' + str(prime*2+1))
                    return [prime*2+1, random.randint(1, (prime*2))]
                else:
                    pass
                    # print('카운트 매치 X')
            else:
                pass
                # print('안전 소수 X : ', prime)
        else:
            pass
            # print('소수 X')
    print('소수 못 찾음')
    sys.exit(-1)


def make_own_private_key():
    min = 3
    max = 50
    return random.randint(min, max)


