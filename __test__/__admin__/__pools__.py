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
        self._prestartVmsCountInPool = '1'
        self._addVmsCountInPool = '1'
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
        self.prestartVmsInPools()
        time.sleep(0.3)
        self.addVmsInPools()
        time.sleep(10) # 풀 내 가상 머신 생성 시간 대기 필요
        self.detachVmsInPools()
        time.sleep(10) # 풀 내 가상 머신 생성 시간 대기 필요
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
            time.sleep(3) # element 뜰 때까지 대기 필요

            # 설명에 추가되면 성공
            _editCheck = self.webDriver.tableSearch(self._poolsDescription, 5)
            printLog("[EDIT POOLS] Check if edited")
            if _editCheck == True:
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

    def prestartVmsInPools(self):
        printLog(printSquare('Prestart Vms In Pools'))
        try:
            result = FAIL
            msg = ''

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._poolsName, 0, rowClick=True)

            # 편집 클릭
            printLog("[PRESTART VMS IN POOLS] Edit pools")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # 사전 시작할 가상 머신 갯수에 대한 문자열 입력 후 저장
            self.webDriver.explicitlyWait(10, By.ID, 'PoolEditPopupWidget_editPrestartedVms')
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.findElement('id', 'PoolEditPopupWidget_editPrestartedVms', True)

            self.webDriver.sendKeys(self._prestartVmsCountInPool)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'PoolEditPopupView_OnSave', True)
            time.sleep(3)

            # 실행중인 가상머신에 0 -> self._prestartVmsCountInPool되면 성공
            printLog("[PRESTART VMS IN POOLS] Check if edited")
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    tableValueList = self.webDriver.tableSearch(self._poolsName, 0, rowClick=False, nameClick=False, returnValueList=True)
                    if self._prestartVmsCountInPool in tableValueList[3]:
                        result = PASS
                        msg = ''
                        break
                    elif self._prestartVmsCountInPool not in tableValueList[3]:
                        printLog("[PRESTART VMS IN POOLS] Prestart vms in pools status is still created ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[PRESTART VMS IN POOLS] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to prestart vms in new pools..."
                            break
                        else:
                            continue
                except:
                    continue
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[PRESTART VMS IN POOLS] MESSAGE : " + msg)
        printLog("[PRESTART VMS IN POOLS] RESULT : " + result)
        self._poolsResult.append(['prestart' + DELIM + 'vms' + DELIM + 'in' + DELIM + 'pools' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('PRESTART_VMS_IN_POOLS', result, msg)

    def addVmsInPools(self):
        printLog(printSquare('Add Vms In Pools'))
        try:
            result = FAIL
            msg = ''

            # 할당된 가상머신 갯수 저장
            time.sleep(0.5)
            _poolsInfo = self.webDriver.tableSearch(self._poolsName, 0, rowClick=False, nameClick=False, returnValueList=True)
            _presentAssignedVms = int(_poolsInfo[2])

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._poolsName, 0, rowClick=True)

            # 편집 클릭
            printLog("[ADD VMS IN POOLS] Edit pools")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # 추가할 가상 머신 갯수에 대한 문자열 입력 후 저장
            self.webDriver.explicitlyWait(10, By.ID, 'PoolEditPopupWidget_increaseNumOfVms')
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.findElement('id', 'PoolEditPopupWidget_increaseNumOfVms', True)

            self.webDriver.sendKeys(self._addVmsCountInPool)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'PoolEditPopupView_OnSave', True)
            time.sleep(3)

            # 할당된 가상머신에 기존 갯수 -> 기존 갯수 + self._addVmsCountInPool되면 성공
            printLog("[ADD VMS IN POOLS] Check if edited")
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    tableValueList = self.webDriver.tableSearch(self._poolsName, 0, rowClick=False, nameClick=False, returnValueList=True)
                    _afterAssignedVms = int(tableValueList[2])
                    _addCount = int(self._addVmsCountInPool)
                    if _presentAssignedVms + _addCount == _afterAssignedVms:
                        result = PASS
                        msg = ''
                        break
                    else:
                        printLog("[ADD VMS IN POOLS] Add vms In pools status is still added ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[ADD VMS IN POOLS] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to add vms in new pools..."
                            break
                        else:
                            continue
                except:
                    continue
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[[ADD VMS IN POOLS] MESSAGE : " + msg)
        printLog("[[ADD VMS IN POOLS] RESULT : " + result)
        self._poolsResult.append(['add' + DELIM + 'vms' + DELIM + 'in' + DELIM + 'pools' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('ADD_VMS_IN_POOLS', result, msg)

    def detachVmsInPools(self):
        printLog(printSquare('Detach Vms In Pools'))
        try:
            result = FAIL
            msg = ''

            # table 내부 전부 검색해서 입력한 이름이 있을 경우 이름 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._poolsName, 0, nameClick=True)

            # 가상머신 탭 클릭
            self.webDriver.implicitlyWait(10)
            time.sleep(3) # element 뜰 때까지 대기 필요
            self.webDriver.findElement('link_text', '가상머신', True) # css_selector 변경

            # Down 상태인 가상 머신 클릭
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    _downCheck = self.webDriver.tableSearch('Down', 6, rowClick=True)
                    if _downCheck == False: # 아직 Down이 되지 않았을 경우, 1분간 시도
                        printLog("[DETACH VMS IN POOLS] Down vms in pools status is still prepared ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[DETACH VMS IN POOLS] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to click down vms in new pools..."
                            break
                        else:
                            continue
                    else :
                        break
                except:
                    continue

            # 분리할 가상머신 클릭
            # self.webDriver.tableSearch('Down', 6, rowClick=True) 
            # tableValueList = self.webDriver.tableSearch(self._poolsName + '-1', 0, rowClick=False, nameClick=False, returnValueList=True)

            # 분리 버튼 클릭
            printLog("[DETACH VMS IN POOLS] Detach vms")
            self.webDriver.explicitlyWait(10, By.ID, ' DetailActionPanelView_Detach')
            self.webDriver.findElement('id', 'DetailActionPanelView_Detach', True)

            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnDetach')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnDetach', True)

            printLog("[DETACH VMS IN POOLS]] Check if detached")

            # 가상머신 탭 내에서 VM이 사라진 것으로 체크
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    _deleteCheck = self.webDriver.tableSearch(self._poolsName + '-1', 0) # 가상머신 이름으로 검색
                    if _deleteCheck == False:
                        result = PASS
                        msg = ''
                        break
                    else:
                        printLog("[DETACH VMS IN POOLS] Detach vms in pools status is still deleted ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[DETACH VMS IN POOLS] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to detach vms in new pools..."
                            break
                        else:
                            continue
                except:
                    continue
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[[DETACH VMS IN POOLS] MESSAGE : " + msg)
        printLog("[[DETACH VMS IN POOLS] RESULT : " + result)
        self._poolsResult.append(['detach' + DELIM + 'vms' + DELIM + 'in' + DELIM + 'pools' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DETACH_VMS_IN_POOLS', result, msg)


    def delete(self):
        printLog(printSquare('Delete Pools'))
        
        # 풀 메뉴 재진입
        self.setup()

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

            printLog("[DELETE POOLS] Check if deleted")
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    _deleteCheck = self.webDriver.tableSearch(self._poolsName, 0)
                    if _deleteCheck == False:
                        result = PASS
                        msg = ''
                        break
                    else:
                        printLog("[DELETE POOL] Pools status is still deleted ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[DELETE POOL] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to delete new pools..."
                            break
                        else:
                            continue
                except:
                    continue
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[DELETE POOLS] MESSAGE : " + msg)
        printLog("[DELETE POOLS] RESULT : " + result)
        self._poolsResult.append(['pools' + DELIM + 'delete' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DELETE_POOLS', result, msg)