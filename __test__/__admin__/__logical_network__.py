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
        self._networksDescription = randomString()
        self.tl = testlink()

    def test(self):
        self.setup()
        self.create()
        time.sleep(0.3)
        self.edit()
        time.sleep(0.3)
        self.delete()

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
    
    def edit(self):
        printLog(printSquare('Edit Networks'))
        try:
            result = FAIL
            msg = ''

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(3)
            self.webDriver.tableSearch(self._networksName, 0, nameClick=True)

            # 편집 클릭
            printLog("[EDIT NETWORKS] Edit networks")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)
            
            # 설명에 임의의 문자열 입력 후 저장
            self.webDriver.explicitlyWait(10, By.ID, 'AbstractNetworkPopupView_descriptionEditor')
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.findElement('id', 'AbstractNetworkPopupView_descriptionEditor', True)
            
            self.webDriver.sendKeys(self._networksDescription)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'AbstractNetworkPopupView_OnSave', True)
            time.sleep(3) # element 뜰 때까지 대기 필요

            # 메뉴 재접근
            self.setup()

            # 설명에 추가되면 성공
            _editCheck = self.webDriver.tableSearch(self._networksDescription, 3)
            printLog("[EDIT NETWORKS] Check if edited")
            if _editCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to edit new networks..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[EDIT NETWORKS] MESSAGE : " + msg)
        printLog("[EDIT NETWORKS] RESULT : " + result)
        self._logicalNetworkResult.append(['networks' + DELIM + 'edit' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('EDIT_NETWORKS', result, msg)

    def delete(self):
        printLog(printSquare('Delete Pools'))
        
        # 풀 메뉴 재진입
        self.setup()

        try:
            result = FAIL
            msg = ''

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._networksName, 0, nameClick=True)    

            # 삭제 클릭
            printLog("[DELETE NETWORKS] Delete networks")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)
            
            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_onRemove', True)
            time.sleep(3) # 테이블 업데이트까지 대기 필요

            # 삭제되면 성공
            printLog("[DELETE NETWORKS] Check if deleted")
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    _deleteCheck = self.webDriver.tableSearch(self._networksName, 0)
                    if _deleteCheck == False:
                        result = PASS
                        msg = ''
                        break
                    else:
                        printLog("[DELETE NETWORKS] Pools status is still deleted ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[DELETE NETWORKS] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to delete new networks..."
                            break
                        else:
                            continue
                except:
                    continue
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[DELETE NETWORKS] MESSAGE : " + msg)
        printLog("[DELETE NETWORKS] RESULT : " + result)
        self._logicalNetworkResult.append(['networks' + DELIM + 'delete' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DELETE_NETWORKS', result, msg)