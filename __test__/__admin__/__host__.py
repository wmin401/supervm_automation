from time import sleep
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

class admin_host:
    def __init__(self, webDriver):
        printLog("* 호스트 테스트 시작")
        self._hostResult = []
        self._hostName = 'hypervm31.tmax.dom'
        self._hostIP = 'hypervm31.tmax.dom'
        self._hostPW = 'asdf'
        self.webDriver = webDriver
    
    def test(self):
        self.create()
        self.remove()
        
    def create(self):
        printLog("1) Create Host")
        
        try:
            # 컴퓨팅
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 호스트
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_hostsAnchor',True)

            # 새로 만들기
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_New')
            self.webDriver.findElement('id','ActionPanelView_New',True)

            time.sleep(1)
            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'HostPopupView_name')
            self.webDriver.findElement('id','HostPopupView_name',True)
            self.webDriver.sendKeys(self._hostName)

            # IP 입력
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','HostPopupView_host',True)
            self.webDriver.sendKeys(self._hostIP)

            # PW 입력
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','HostPopupView_userPassword',True)
            self.webDriver.sendKeys(self._hostPW)

            # 새 호스트 OK 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#HostPopupView_OnSaveFalse > button',True)

            # 전원 관리 설정 OK 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DefaultConfirmationPopupView_OnSaveInternalNotFromApprove',True)

            time.sleep(180)
            
            '''
            # 취소 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','HostPopupView_Cancel',True)

            '''
            _createCheck = self.webDriver.tableSearch(self._hostName, 2)

            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new host..."

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._hostResult.append(['host;create&cancel;' + result + ';' + msg])


    def remove(self):
        printLog("2) Remove Host")
        try:
            # 컴퓨팅
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 호스트
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_hostsAnchor',True)

            # table 내부에 생성한 호스트의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._hostName, 2, True)
            time.sleep(1)

            # 관리
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView___',True)

            # 유지보수
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#ActionPanelView___ > ul > li:nth-child(1) > a',True)

            # 호스트 유지관리 모드 OK 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','HostMaintenanceConfirmationPopupView_OnMaintenance',True)

            time.sleep(5)
            # 삭제 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)

            # 호스트 삭제 OK 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)

            time.sleep(5)

            _removeCheck = self.webDriver.tableSearch(self._hostName, 2)

            if _removeCheck == True:
                result = FAIL
                msg = 'Failed to remove new host...'
            else:
                result = PASS
                msg = ""
        
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._hostResult.append(['host;create&cancel;' + result + ';' + msg])