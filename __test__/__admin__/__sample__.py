from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *


class admin_sample:
    def __init__(self, webDriver):
        self._sampleResult = []
        self.webDriver = webDriver
        # self._sampleName = 'auto_sample_'+randomString()
        self.tl = testlink()
          
    def sample_test_case1(self):
        print("샘플파일")
        print("이 코드는 필수로 사용되어야함")
        try:
            result = PASS
            msg = ''
        except Exception as e:
            # 예외처리
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        # 결과 저장
        printLog("* RESULT : " + result)
        self._sampleResult.append(['Sample' + DELIM + 'test case 1' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('SAMPLE_TEST_CASE_1',result, msg)

