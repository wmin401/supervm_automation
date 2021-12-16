import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import testlink
class admin_vm:
    def __init__(self, webDriver):
        printLog("* 관리자 포털 vm 테스트 시작")
        self._vmResult = []
        self._vmName = 'auto_vm_%s'%randomString()
        self._diskName = '%s_Disk1'%self._vmName
        self._diskSize = '10'
        self.webDriver = webDriver

        self.tl = testlink()

    def test(self):
        self.create()
        self.copy()
        self.remove()

    def setup(self):
        # 컴퓨팅
        time.sleep(2)
        printLog("[VM SETUP] Compute - Virtual Machines")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute', True)

        # 가상머신
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','MenuView_vmsAnchor',True)
        time.sleep(2)


    def create(self):
        printLog(printSquare('Create VM'))
        result = FAIL
        msg = ''

        try:            
            self.setup()

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
            
            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmDiskPopupView_OnSave',True)
            time.sleep(0.5)

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

            time.sleep(1)

            _createCheck = self.webDriver.tableSearch(self._vmName, 2)            
            if _createCheck == True:
                result = PASS
                printLog("VM NAME : %s"%self._vmName)
                printLog("VM DISK NAME : %s_disk"%self._vmName)
                printLog("VM DISK SIZE : %s"%self._diskSize)
            else:
                result = FAIL
                msg = "Failed to create new vm..."
                printLog("[VM CREATE] MESSAGE : " + msg)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM CREATE] RESULT : " + result)
        self._vmResult.append(['admin' + DELIM + 'vm create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_CREATE',result, msg) # 모두 대문자

    def copy(self):
        printLog(printSquare('Copy VM'))
        result = FAIL
        msg = ''

        try:            

            # 디스크 잠겼는지 확인 필요
            time.sleep(2)
            printLog("[VM COPY] Storage - Disks")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)
            time.sleep(0.5)
            self.webDriver.explicitlyWait(10, By.ID, 'MenuView_disksAnchor')
            self.webDriver.findElement('id','MenuView_disksAnchor',True)
            time.sleep(1)

            st = time.time()
            while True:
                tableValueList = self.webDriver.tableSearch(self._diskName, 0, False, False, True)
                if 'OK' in tableValueList[11]:
                    break
                elif '잠김' in tableValueList[11] or 'Locked' in tableValueList[11]:
                    printLog("[VM REMOVE] Disk's status is still locked...")
                    if time.time() - st > 120:
                        result = FAIL
                        msg = 'Disk is locked...'
                        printLog("[REMOVE VM] RESULT : " + result)
                        printLog("[REMOVE VM] MESSAGE : " + msg)
                        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
                        return

            self.setup()

            printLog("[VM COPY] VM Copy")

            self.webDriver.tableSearch(self._vmName, 2, True)            
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button', True)
            time.sleep(0.3)
            self.webDriver.findElement('id', 'ActionPanelView_CloneVm', True)
        
            time.sleep(1)
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_name')
            self.webDriver.findElement('id', 'VmPopupWidget_name', True)
            self.webDriver.sendKeys('%s_copy'%self._vmName)

            self.webDriver.findElement('id', 'VmPopupView_OnSave', True)

            
            st = time.time()
            while True:
                time.sleep(1)
                try:
                    _createCheck = self.webDriver.tableSearch('%s_copy'%self._vmName, 2)
                    if _createCheck == True:
                        result = PASS
                        try:
                            self.webDriver.findElement('css_selector', 'body > div.popup-content.ui-draggable > div > div > div > div.modal-header.ui-draggable-handle > button', True)
                            break
                        except:
                            pass
                    else:                 
                        result = FAIL
                        msg = "Failed to copy vm..."
                        printLog("[VM COPY] MESSAGE : " + msg)
                    if time.time() - st > 360: #최대 5분                        
                        break
                except:
                    result = FAIL
                    msg = "Failed to copy vm..."
                    printLog("[VM COPY] MESSAGE : " + msg)
                    break


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM COPY] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'vm copy' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_COPY',result, msg) # 모두 대문자

    def remove(self):
        printLog(printSquare('Remove VM'))
        result = FAIL
        msg = ''

        try:            

            # 디스크 잠겼는지 확인 필요
            time.sleep(2)
            printLog("[VM REMOVE] Storage - Disks")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)
            time.sleep(0.5)
            self.webDriver.explicitlyWait(10, By.ID, 'MenuView_disksAnchor')
            self.webDriver.findElement('id','MenuView_disksAnchor',True)
            time.sleep(1)

            st = time.time()
            while True:
                tableValueList = self.webDriver.tableSearch(self._diskName, 0, False, False, True)
                if 'OK' in tableValueList[11]:
                    break
                elif '잠김' in tableValueList[11] or 'Locked' in tableValueList[11]:
                    printLog("[VM REMOVE] Disk's status is still locked...")
                    if time.time() - st > 120:
                        result = FAIL
                        msg = 'Disk is locked...'
                        printLog("[REMOVE VM] RESULT : " + result)
                        printLog("[REMOVE VM] MESSAGE : " + msg)
                        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
                        return

            self.setup()

            st = time.time()
            while True:
                tableValueList = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
                if 'Down' in tableValueList[13]:
                    break
                elif '이미지 잠김' in tableValueList[13] or 'Image Locked' in tableValueList[13]:
                    printLog("[VM REMOVE] VM'status is still locked...")
                    if time.time() - st > 60:
                        result = FAIL
                        msg = 'VM Image locked...'
                        printLog("[VM CREATE] RESULT : " + result)
                        printLog("[VM CREATE] MESSAGE : " + msg)
                        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
                        return

            self.webDriver.tableSearch(self._vmName, 2, True)            
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button', True)
            time.sleep(0.3)
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)

            
            time.sleep(2)
            
            st = time.time()
            while True:
                time.sleep(1)
                try:
                    tableValueList = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
                    if tableValueList == False:
                        printLog("[VM REMOVE] VM removed")
                        result = PASS
                        break

                    printLog("[VM REMOVE] VM still existed...")
                    result = FAIL
                    msg = "Failed to remove new vm..."
                    printLog("[VM REMOVE] MESSAGE : " + msg)
                    if time.time() - st > 60:
                        break
                except:
                    result = PASS
                    break

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM REMOVE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'vm remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
