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
        self._networksName = 'auto_networks_'+randomString()
        self.tl = testlink()

    def test(self):
        self.setup()
        self.create()

    def setup(self):
        # 논리 네트워크 메뉴 접근

        # 네트워크 클릭
        printLog("[SETUP] Network - Networks")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('xpath','/html/body/div[3]/div[3]/div/ul/li[3]/a/span[2]',True)

        # 네트워크 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_networksAnchor')
        self.webDriver.findElement('id','MenuView_networksAnchor',True)

        time.sleep(2)

    def create(self):
        printLog(printSquare('Create Networks'))
        try:
            result = FAIL
            msg = ''
            # 네트워크 새로 만들기 버튼 클릭
            printLog("[CREATE NETWORKS] Create networks")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_New',True)

            # 네트워크 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'AbstractNetworkPopupView_nameEditor')
            self.webDriver.findElement('id','AbstractNetworkPopupView_nameEditor')
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.sendKeys(self._networksName)
            printLog("[CREATE NETWORKS] Networks name : %s"%self._networksName)

            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','AbstractNetworkPopupView_OnSave', True)
            time.sleep(3)

            printLog("[CREATE NETWORKS] Check if created")
            printLog("[CREATE NETWORKS] Wait until status will be OK")
            # table 내부 전부 검색해서 입력한 이름이 있을경우 PASS
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    tableValueList = self.webDriver.tableSearch(self._networksName, 0, rowClick=False, nameClick=False, returnValueList=True)
                    if self._networksName in tableValueList[0]:
                        result = PASS
                        msg = ''
                        break
                    elif self._networksName not in tableValueList[0]:
                        printLog("[CREATE NETWORKS] Networks status is still created ...")
                        continue
                    _endTime = time.time()
                    if _endTime - _startTime >= 60:
                        printLog("[CREATE NETWORKS] Failed status changed : Timeout")
                        result = FAIL
                        msg = "Failed to create new networks..."
                        break
                except:
                    continue

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[CREATE NETWORKS] MESSAGE : " + msg)
        printLog("[CREATE NETWORKS] RESULT : " + result)
        self._logicalNetworkResult.append(['networks' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('NETWORKS_CREATE', result, msg)

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
