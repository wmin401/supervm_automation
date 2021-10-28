from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
import time

class admin_disk:
    def __init__(self,webDriver):
        printLog("* 디스크 테스트 시작")
        self._diskResult = []
        self._diskSize = '10'
        self._diskName = 'TEST'
        self.webDriver = webDriver
        
    def create(self):
        printLog('Create Disk')
        
        try:
            # 스토리지
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 디스크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_disksAnchor',True)
            
            #새로 만들기                  
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_New',True)

            # 크기 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id','VmDiskPopupWidget_size',True)
            self.webDriver.sendKeys(self._diskSize)
            
            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_alias')
            self.webDriver.findElement('id','VmDiskPopupWidget_alias',True)
            self.webDriver.sendKeys(self._diskName)

            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmDiskPopupView_OnSave > button',True)

            '''
            # 새로 만들기 취소 버튼
            webDriver.implicitlyWait(10)
            _cancelBtn = webDriver.findElement('id','VmDiskPopupView_Cancel',True)
            '''
            
            '''
            # 업로드
            time.sleep(1)
            webDriver.implicitlyWait(10)
            _uploadBtn = webDriver.findElement('id','ActionPanelView____',True)
            _startBtn = webDriver.findElement('css_selector','#ActionPanelView____ > ul > li:nth-child(1) > a',True)
            _connetctestBtn = webDriver.findElement('css_selector','body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.GHYIDY4CA4B > button',True)
            _uploadcancelBtn = webDriver.findElement('id','UploadImagePopupView_Cancel',True)
            result = PASS
            msg = ''
            '''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
    
    def remove(self):
        printLog('Create Disk')
        
        try:
            # 스토리지
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 디스크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_disksAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._diskName, 0, True)
            time.sleep(1)

            # 제거 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)

            # 디스크 삭제 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnRemoveDisk > button',True)
        
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)