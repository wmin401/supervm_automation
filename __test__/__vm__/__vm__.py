from time import sleep
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
class vm_vm:
    def __init__(self, webDriver):
        printLog("* vm 포털 vm 테스트 시작")
        self._vmResult = []
        self._vmName = 'TEST'
        self._diskSize = '10'
        #self._diskName = 'TEST'
        self.webDriver = webDriver

    def create(self):
        printLog('Create VM')

        try:
            # 컴퓨팅
            time.sleep(3)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 가상머신
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_vmsAnchor',True)

            # 새로 만들기
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_NewVm')
            self.webDriver.findElement('id','ActionPanelView_NewVm',True)

            time.sleep(1)

            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_name')
            self.webDriver.findElement('id','VmPopupWidget_name',True)
            self.webDriver.sendKeys(self._vmName)

            # 디스크 생성 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_instanceImages__createEdit',True)

            time.sleep(1)

            # 크기 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id','VmDiskPopupWidget_size',True)
            self.webDriver.sendKeys(self._diskSize)
            
            '''
            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_alias')
            self.webDriver.findElement('id','VmDiskPopupWidget_alias',True)
            self.webDriver.sendKeys(self._diskName)
            '''

            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmDiskPopupView_OnSave',True)

            # 고급 옵션 표시 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupView_OnAdvanced',True)

            # 부트 옵션 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[2]/div/div/div/div[1]/ul/li[9]/a',True)

            # 첫 번째 장치 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_firstBootDevice',True)

            # 첫 번째 장치 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmPopupWidget_firstBootDevice > div > ul > li:nth-child(2)',True)

            # CD/DVD 연결 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_cdAttached',True)

            # CD/DVD 연결 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupView_OnSave',True)

            _createCheck = self.webDriver.tableSearch(self._vmName, 2)            
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new vm..."

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("* RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'create' + DELIM + result + DELIM + msg])