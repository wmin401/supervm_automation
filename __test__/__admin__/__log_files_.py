-from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

'''
    샘플파일
    아래 코드는 필수로 사용되어야함
    주석은 삭제해도됨(# 로 입력된 부분이나, 이 주석)
    모든 sample 로 입력 되어있는 부분을 변경하여아함(대소문자 구분하여)
    출력은 본인이 원하는 곳에 추가하여 사용(보통은 디버그용)
    코드 작성은 작성자가 원하는대로 가능(함수를 나눠도 되고 하나로 해도 되고)


    작성자 : CQA2 이동일
'''

class admin_log_files: # 모두 소문자
    def __init__(self, webDriver):
        self._sampleResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        # self._sampleName = 'auto_sample_'+randomString() # 필요할 경우 사용
        self.tl = testlink()

    def sample_test_case1(self):

        try:
            result = PASS
            msg = ''
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[SAMPLE TEST] MESSAGE : " + msg)

        # 결과 저장
        printLog("[SAMPLE TEST] RESULT : " + result)
        self._sampleResult.append(['Sample' + DELIM + 'test case 1' + DELIM + result + DELIM + msg]) # 대소문자 상관없음

        self.tl.junitBuilder('SAMPLE_TEST_CASE_1',result, msg) # 모두 대문자
