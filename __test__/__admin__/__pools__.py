import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import *

from selenium.webdriver.common.by import By

from __test__.__admin__.__template__ import *

'''
    작성자 : CQA2 김정현
'''

class admin_pools:
    def __init__(self, webDriver):
        self._poolsResult = []
        self.webDriver = webDriver
        self._poolsName = 'auto_pools_'+ randomString()
        self._poolsDescription = randomString()
        self.tl = testlink()
        self._template_instance = admin_template(webDriver) # template class 사용

    def test(self):
        # self._template_instance.create() # 템플릿 생성
        # time.sleep(0.3)
        self.setup()
        self.create()
        time.sleep(10) # 풀 내 가상 머신 생성 시간 대기 필요
        self.edit()
        time.sleep(0.3)
        self.delete()
        time.sleep(0.3)

    def setup(self):
        # 풀 메뉴 접근

        # 컴퓨팅 클릭
        printLog("[SETUP] Compute - Pools ")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute',True)

        # 풀 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_poolsAnchor')
        self.webDriver.findElement('id','MenuView_poolsAnchor',True)

        time.sleep(2)

    def create(self):
        printLog(printSquare('Create Pools'))
        try:
            result = FAIL
            msg = ''
            # 풀 새로 만들기 버튼 클릭
            printLog("[CREATE POOLS] Create pools")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_New',True)

            # 풀 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'PoolNewPopupWidget_name')
            self.webDriver.findElement('id','PoolNewPopupWidget_name')
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.sendKeys(self._poolsName)
            printLog("[CREATE POOLS] Pools name : %s"%self._poolsName)

            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','PoolNewPopupView_OnSave', True)
            time.sleep(3)

            printLog("[CREATE POOLS] Check if created")
            printLog("[CREATE POOLS] Wait until status will be OK")
            # table 내부 전부 검색해서 입력한 이름이 있을경우 PASS
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    tableValueList = self.webDriver.tableSearch(self._poolsName, 0, rowClick=False, nameClick=False, returnValueList=True)
                    if self._poolsName in tableValueList[0]:
                        result = PASS
                        msg = ''
                        break
                    elif self._poolsName not in tableValueList[0]:
                        printLog("[CREATE POOLS] Pools status is still created ...")
                        continue
                    _endTime = time.time()
                    if _endTime - _startTime >= 60:
                        printLog("[CREATE POOLS] Failed status changed : Timeout")
                        result = FAIL
                        msg = "Failed to create new pools..."
                        break
                except:
                    continue

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[CREATE POOLS] MESSAGE : " + msg)
        printLog("[CREATE POOLS] RESULT : " + result)
        self._poolsResult.append(['pools' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('POOLS_CREATE', result, msg)

    def edit(self):
        printLog(printSquare('Edit Pools'))
        try:
            result = FAIL
            msg = ''

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._poolsName, 0, rowClick=True)    

            # 편집 클릭
            printLog("[EDIT POOLS] Edit pools")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)
            
            # 설명에 임의의 문자열 입력 후 저장
            self.webDriver.explicitlyWait(10, By.ID, 'PoolEditPopupWidget_description')
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.findElement('id', 'PoolEditPopupWidget_description', True)
            
            self.webDriver.sendKeys(self._poolsDescription)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'PoolEditPopupView_OnSave', True)
            time.sleep(1)

            # 설명에 추가되면 성공
            _updateCheck = self.webDriver.tableSearch(self._poolsDescription, 5)
            printLog("[EDIT POOLS] Check if edited")
            if _updateCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to edit new pools..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[EDIT POOLS] MESSAGE : " + msg)
        printLog("[EDIT POOLS] RESULT : " + result)
        self._poolsResult.append(['pools' + DELIM + 'edit' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('EDIT_POOLS', result, msg)

    def delete(self):
        printLog(printSquare('Delete Pools'))
        try:
            result = FAIL
            msg = ''

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._poolsName, 0, rowClick=True)    

            # 삭제 클릭
            printLog("[DELETE POOLS] Delete pools")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)
            
            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(3) # 테이블 업데이트까지 대기 필요

            # 삭제되면 성공
            _deleteCheck = self.webDriver.tableSearch(self._poolsName, 0)
            printLog("[DELETE POOLS] Check if deleted")
            if _deleteCheck == False:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to delete new pools..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[DELETE POOLS] MESSAGE : " + msg)
        printLog("[DELETE POOLS] RESULT : " + result)
        self._poolsResult.append(['pools' + DELIM + 'delete' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DELETE_POOLS', result, msg)