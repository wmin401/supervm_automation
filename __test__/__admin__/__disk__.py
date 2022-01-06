from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
import time

from __common__.__testlink__ import *

class admin_disk:
    def __init__(self,webDriver):
        printLog("* 디스크 테스트 시작")
        self._diskResult = []
        self._diskSize = '10'
        self._diskName = 'TEST'
        self._vmName1 = 'TEST1'
        self._vmName2 = 'TEST2'
        self.webDriver = webDriver
        self.tl = testlink()

    def test(self):
        #self.create()
        #self.diskMove()
        #self.diskChangeinterface()
        #self.vmCreate()
        self.diskCopy()
        #self.remove()
        
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

            time.sleep(20)

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
            _createCheck = self.webDriver.tableSearch(self._diskName, 0)            
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new disk..."

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("* RESULT : " + result)
        self._diskResult.append(['disk' + DELIM + 'create' + DELIM + result + DELIM + msg])
    
    def remove(self):
        printLog('remove Disk')
        
        try:
            # 스토리지
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 디스크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_disksAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._diskName, 0, True)
            time.sleep(5)

            # 제거 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)

            # 디스크 삭제 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemoveDisk',True)

            time.sleep(2)

            _removeCheck = self.webDriver.tableSearch(self._diskName, 0)            
            if _removeCheck == True:
                result = FAIL
                msg = ''
            else:
                result = PASS
                msg = "Failed to create new disk..."

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("* RESULT : " + result)
        self._diskResult.append(['disk' + DELIM + 'remove' + DELIM + result + DELIM + msg])

    def diskMove(self):    
        printLog(printSquare('Disk Move'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MenuView_storageTab')
            self.webDriver.findElement('id', 'MenuView_storageTab', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_disksAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_disksAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._diskName,0,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Move')
            self.webDriver.findElement('id', 'ActionPanelView_Move', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[DISK MOVE] " + msg)

        # 결과 출력
        printLog("[DISK MOVE] RESULT : " + result)
        self._diskResult.append(['disk' + DELIM + 'move' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('DISK_MOVE',result, msg)

    def diskChangeinterface(self):    
        printLog(printSquare('Disk Changeinterface'))
        result = FAIL
        msg = ''

        try:
            self.vmCreate()
            time.sleep(5)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MainVirtualMachineView_table_content_col2_row1')
            self.webDriver.findElement('id', 'MainVirtualMachineView_table_content_col2_row1', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '디스크')
            self.webDriver.findElement('link_text', '디스크', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Edit')
            self.webDriver.findElement('id', 'DetailActionPanelView_Edit', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmDiskPopupWidget_interface .filter-option')
            self.webDriver.findElement('css_selector', '#VmDiskPopupWidget_interface .filter-option', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'SATA')
            self.webDriver.findElement('link_text', 'SATA', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(5)

            self.vmRemove()
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[DISK CHANGEINTERFACE] " + msg)

        # 결과 출력
        printLog("[DISK CHANGEINTERFACE] RESULT : " + result)
        self._diskResult.append(['disk' + DELIM + 'changeinterface' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('DISK_CHANGEINTERFACE',result, msg)

    def diskCopy(self):    
        printLog(printSquare('Disk Copy'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MenuView_storageTab')
            self.webDriver.findElement('id', 'MenuView_storageTab', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_disksAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_disksAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_New')
            self.webDriver.findElement('id', 'ActionPanelView_New', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_size', False)
            self.webDriver.sendKeys('10') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_alias')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_alias', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_alias')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_alias', False)
            self.webDriver.sendKeys(self._diskName) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(10)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._diskName,0,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Copy')
            self.webDriver.findElement('id', 'ActionPanelView_Copy', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'WelcomePage_webadmin')
            self.webDriver.findElement('id', 'WelcomePage_webadmin', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[DISK COPY] " + msg)

        # 결과 출력
        printLog("[DISK COPY] RESULT : " + result)
        self._diskResult.append(['disk' + DELIM + 'copy' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('DISK_COPY',result, msg)

    def vmCreate(self):    
        printLog(printSquare('Vm Create'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_NewVm')
            self.webDriver.findElement('id', 'ActionPanelView_NewVm', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_name')
            self.webDriver.findElement('id', 'VmPopupWidget_name', False)
            self.webDriver.sendKeys(self._vmName1) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmPopupWidget_instanceImages__createEdit > .btn')
            self.webDriver.findElement('css_selector', '#VmPopupWidget_instanceImages__createEdit > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_size', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_size', False)
            self.webDriver.sendKeys('10') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmDiskPopupView_OnSave > .btn')
            self.webDriver.findElement('css_selector', '#VmDiskPopupView_OnSave > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(10)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CREATE] " + msg)
            printLog("[VM CREATE] RESULT : " + result)

    def vmRemove(self):    
        printLog(printSquare('Vm Remove'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._vmName1,2,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button')
            self.webDriver.findElement('css_selector', 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '삭제')
            self.webDriver.findElement('link_text', '삭제', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
           
            time.sleep(10)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REMOVE] " + msg)
            printLog("[VM REMOVE] RESULT : " + result)