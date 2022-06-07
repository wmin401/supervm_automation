from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

'''

    작성자 : Infra QA 김정현
'''

class admin_logical_network: # 모두 소문자
    def __init__(self, webDriver):
        self._logicalNetworkResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        # self._sampleName = 'auto_sample_'+randomString() # 필요할 경우 사용
        self.tl = testlink()

    def test(self):
        printLog("")
    
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
