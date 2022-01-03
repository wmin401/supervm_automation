import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import *

from selenium.webdriver.common.by import By

'''
    작성자 : CQA2 김정현
'''

class admin_external_provider: # 모두 소문자
    def __init__(self, webDriver):
        self._externalProviderResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        # self._sampleName = 'auto_sample_'+randomString() # 필요할 경우 사용
        self.tl = testlink()

    def test(self):
        self.setup()

    def setup(self):
        # 외부 공급자 메뉴 접근

        # 관리 클릭
        printLog("[SETUP] Administration - Provider")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('xpath','/html/body/div[3]/div[3]/div/ul/li[5]/a/span[2]',True)

        # time.sleep(3) # element 뜰 때까지 대기 필요
        # self.webDriver.explicitlyWait(10, By.LINK_TEXT, '관리')
        # _driver = self.webDriver.getDriver()

        # _element = _driver.find_element_by_xpath('')
        # _driver.execute_script("arguments[0].click();", _element)
        time.sleep(2)

        # _element = _driver.find_element_by_css_selector('body > div.GHYIDY4CHUB > div:nth-child(3) > div > ul > li.list-group-item.secondary-nav-item-pf.active > a')    
        # self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div:nth-child(3) > div > ul > li.list-group-item.secondary-nav-item-pf.active',True)

        # 공급자 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_providersAnchor')
        self.webDriver.findElement('id','MenuView_providersAnchor',True)

        time.sleep(2)

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
