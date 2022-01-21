import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import testlink
from __test__.__admin__.__cluster__ import admin_cluster
class admin_vm:
    def __init__(self, webDriver):
        printLog('VM 1 TEST includes create, update, copy, run, shutdown, remove')
        self._vmResult = []
        self._vmName = 'auto_vm_%s'%randomString()
        self._diskName = '%s_Disk1'%self._vmName
        # self._diskName = 'auto_vm_HnpZbEOS_Disk1'
        self._diskSize = '5'
        self.webDriver = webDriver

        self.tl = testlink()

    def diskStatus(self):
        status = False

        # 디스크 잠겼는지 확인 필요
        time.sleep(1)
        printLog("[DISK STATUS] Storage - Disks")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','MenuView_storageTab',True)
        time.sleep(0.5)
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_disksAnchor')
        self.webDriver.findElement('id','MenuView_disksAnchor',True)
        time.sleep(1)

        st = time.time()
        while True:
            time.sleep(1)
            try:
                tableValueList = self.webDriver.tableSearch(self._diskName, 0, False, False, True)
                printLog(tableValueList)
                if 'OK' in tableValueList[10]:
                    printLog("[DISK STATUS] Disk's status is OK")
                    status = True
                    break
                elif '잠김' in tableValueList[10] or 'Locked' in tableValueList[10]:                    
                    printLog("[DISK STATUS] Disk's status is still locked...")                    
                    status = False
                    
                ed = time.time()
                if ed - st > 120:
                    printLog("[DISK STATUS] Disk is locked(timeout)...")
                    status = False
                    break
            except Exception as e:
                status = False
                msg = str(e).replace("\n",'')
                msg = msg[:msg.find('Element <')]
                printLog("[DISK STATUS] " + msg)
                continue
        return status

    def test(self):
        self.create()
        self.update()
        self.copy()
        self.run()
        self.shutdown()
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

            time.sleep(5)
            _createCheck = self.webDriver.tableSearch(self._vmName, 2)            
            if _createCheck == True:
                result = PASS
                printLog("VM NAME : %s"%self._vmName)
                printLog("VM DISK NAME : %s_disk"%self._vmName)
                printLog("VM DISK SIZE : %s GiB"%self._diskSize)
            else:
                result = FAIL
                msg = "Failed to create new vm..."
                printLog("[VM CREATE] " + msg)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM CREATE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_CREATE',result, msg) # 모두 대문자

    def update(self):
        printLog(printSquare('Update VM'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 vm 클릭
            self.webDriver.tableSearch(self._vmName, 2, True)

            # 편집 클릭
            self.webDriver.findElement('id','ActionPanelView_Edit',True)

            # 시스템 탭 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(2)')
            self.webDriver.findElement('css_selector', '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(2)', True)

            # 메모리 사이즈 변경
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_memSize')
            self.webDriver.findElement('id', 'VmPopupWidget_memSize')
            self.webDriver.clear()
            self._updateSize = '2048'
            self.webDriver.sendKeys(self._updateSize)

            # OK 클릭
            self.webDriver.findElement('id', 'VmPopupView_OnSave', True)
            time.sleep(2)

            # VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            self.webDriver.explicitlyWait(10, By.ID, 'SubTabVirtualMachineGeneralView_form_col1_row0_value')
            self.webDriver.findElement('id', 'SubTabVirtualMachineGeneralView_form_col1_row0_value')
            _updated = self.webDriver.getAttribute('textContent')

            if self._updateSize in _updated:
                result = PASS
            else:
                result = FAIL
                msg = 'Failed to update memory size'

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM UPDATE] " + msg)
        printLog("[VM UPDATE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'update' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_UPDATE',result, msg) # 모두 대문자

    def copy(self):
        printLog(printSquare('Copy VM'))
        result = FAIL
        msg = ''

        try:            
            # 디스크 상태 확인
            if not self.diskStatus():
                result = FAIL
                msg = 'Disk is locked(timeout)...'
                self.tl.junitBuilder('VM_DISK_COPY',result, msg) # 모두 대문자
                return

            self.setup()

            printLog("[VM COPY] VM Copy")

            self.webDriver.tableSearch(self._vmName, 2, True)            
            
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            time.sleep(0.3)
            self.webDriver.findElement('id', 'ActionPanelView_CloneVm', True)
        
            time.sleep(1)
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_name')
            self.webDriver.findElement('id', 'VmPopupWidget_name', True)
            self.webDriver.sendKeys('copy_%s'%self._vmName)

            self.webDriver.findElement('id', 'VmPopupView_OnSave', True)

            st = time.time()
            while True:
                time.sleep(1)
                try:
                    _createCheck = self.webDriver.tableSearch('copy_%s'%self._vmName, 2)
                    if _createCheck == True:
                        result = PASS
                        try:
                            printLog("[VM COPY] VM is copied")
                            break
                        except:
                            pass
                    else:                 
                        printLog("[VM COPY] VM copy does not exist ...")
                        result = FAIL
                    if time.time() - st > 360: #최대 5분      
                        result = FAIL
                        msg = "Failed to copy vm..."
                        printLog("[VM COPY] " + msg)                  
                        break
                except Exception as e:
                    result = FAIL
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[VM COPY] " + msg)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM COPY] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'copy' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_COPY',result, msg) # 모두 대문자

    def run(self):
        printLog(printSquare('Run VM'))

        # 스케줄링 정책이 power_saving 이면 됨
        # cc = admin_cluster(self.webDriver)
        # cc.scheduling()

        result = FAIL
        msg = ''

        try:        
            if not self.diskStatus():
                result = FAIL
                msg = 'Disk is locked(timeout)...'
                self.tl.junitBuilder('VM_RUN',result, msg) # 모두 대문자
                return

            self.setup()

            # 생성한 vm 클릭
            self.webDriver.tableSearch(self._vmName, 2, True)

            # Run 클릭
            self.webDriver.findElement('id','ActionPanelView_Run',True)
            
            st=time.time()
            cnt = 0
            while True:
                try:
                    time.sleep(1)
                    row = self.webDriver.tableSearch(self._vmName, 2, False, False, True)

                    if 'Up' in row[13] or '실행 중' in row[13]: # 실행완료
                        printLog("[VM RUN] Succefully run vm")
                        result = PASS
                        msg = ''
                        break
                        
                    elif 'Powering Up' in row[13] or '전원을 켜는 중' in row[13]: #
                        result = FAIL
                        msg = 'VM is still powering up ...'
                        if cnt < 1:
                            printLog("[VM RUN] Status : " + row[13])
                            printLog("[VM RUN] Message : " + msg)
                            cnt += 1
                        continue
                    ed = time.time()
                    if ed - st > 120:
                        result = FAIL
                        msg = 'Failed to run vm ...'
                        printLog("[VM SHUTDOWN] Message : " + msg)
                        break

                except Exception as e:
                    result = FAIL
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[VM RUN] Message : " + msg)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM RUN] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'run' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_RUN',result, msg) # 모두 대문자

    def shutdown(self):
        printLog(printSquare('Shutdown VM'))
        result = FAIL
        msg = ''

        try:        
            self.setup()

            # 생성한 vm 클릭
            isRun = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
            # isRun = self.webDriver.tableSearch('auto_vm_HnpZbEOS', 2, False, False, True)
            if 'Down' in isRun[13]: # 실행중이지 않을 경우 종료
                result = FAIL
                msg = 'VM is not running ...'
                printLog("[VM SHUTDOWN] MESSAGE : " + msg)
                printLog("[VM SHUTDOWN] RESULT : " + result)
                self._vmResult.append(['vm' + DELIM + 'shutdown' + DELIM + result + DELIM + msg])        
                self.tl.junitBuilder('VM_SHUTDOWN',result, msg) # 모두 대문자
                return

            # 선택
            # self.webDriver.tableSearch('auto_vm_HnpZbEOS', 2, True)
            self.webDriver.tableSearch(self._vmName, 2, True)
            # 종료 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Shutdown')
            self.webDriver.findElement('id','ActionPanelView_Shutdown',True)
            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnShutdown')
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnShutdown',True)


            st = time.time()
            cnt = 0
            while True:
                try:                          
                    time.sleep(1)
                    row = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
                    # row = self.webDriver.tableSearch('auto_vm_HnpZbEOS', 2, False, False, True)

                    if 'Down' in row[13]: # 
                        result = PASS
                        msg = ''
                        break
                        
                    elif 'Powering Down' in row[13] or '전원을 끄는 중' in row[13]: #
                        result = FAIL
                        msg = 'VM is still shutting down ...'
                        cnt += 1
                        if cnt < 1:
                            printLog("[VM SHHTDOWN] Status : " + row[13])
                            printLog("[VM SHUTDOWN] Message : " + msg)
                        continue
                    ed = time.time()
                    more = 0
                    # 30초마다 종료버튼 클릭
                    if int(ed - st)%30 == 0 and more == 0: 
                        more = 1
                        self.webDriver.tableSearch(self._vmName, 2, True)
                        # 종료 클릭
                        self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Shutdown')
                        self.webDriver.findElement('id','ActionPanelView_Shutdown',True)
                        # OK 클릭
                        self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnShutdown')
                        self.webDriver.findElement('id','RemoveConfirmationPopupView_OnShutdown',True)

                    elif ed - st > 120:
                        result = FAIL
                        msg = 'Failed to shutdown vm ...'
                        printLog("[VM SHUTDOWN] Message : " + msg)
                        break

                except Exception as e:
                    result = FAIL
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[VM SHUTDOWN] Message : " + msg)
                    continue

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[VM SHUTDOWN] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'shutdown' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_SHUTDOWN',result, msg) # 모두 대문자

    def remove(self):
        printLog(printSquare('Remove VM'))
        result = FAIL
        msg = ''

        try:       
            if not self.diskStatus():
                result = FAIL
                msg = 'Disk is locked...'
                printLog("[REMOVE VM] RESULT : " + result)
                printLog("[REMOVE VM] " + msg)
                self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
                return

            self.setup()

            # 이미지 잠긴 상태
            st = time.time()
            while True:
                tableValueList = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
                # tableValueList = self.webDriver.tableSearch('auto_vm_HnpZbEOS_Disk1', 2, False, False, True)
                
                if 'Down' in tableValueList[13]:
                    break
                elif '이미지 잠김' in tableValueList[13] or 'Image Locked' in tableValueList[13]:
                    ed = time.time()  
                    printLog("[TABLE SEARCH] VM'status is still locked...%ds"%(int(ed-st)))
                    if ed - st > 60:
                        result = FAIL
                        msg = 'VM Image locked...'
                        printLog("[VM CREATE] RESULT : " + result)
                        printLog("[VM CREATE] " + msg)
                        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
                        return
            cnt = 0
            while True:
                time.sleep(1)
                self.webDriver.tableSearch(self._vmName, 2, True)            
                # self.webDriver.tableSearch('auto_vm_HnpZbEOS', 2, True)            
                self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
                time.sleep(0.3)
                self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

                self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
                self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
                    
                try:
                    cnt += 1
                    time.sleep(0.5)
                    self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[3]/div[1]/button', True)
                    printLog("[REMOVE EXCEPTION] Remove fail. try again ... %d times"%cnt)
                    continue
                except Exception as e:
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[TABLE SEARCH] " + msg)
                    break
            
            time.sleep(2)
            
            st = time.time()
            while True:
                time.sleep(1)
                try:
                    tableValueList = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
                    if tableValueList == False:
                        printLog("[TABLE SEARCH] VM removed")
                        result = PASS
                        msg = ''
                        break
                    result = FAIL
                    ed = time.time()  
                    printLog("[TABLE SEARCH] VM still existed...%ds"%(int(ed-st)))
                    if ed - st > 60:
                        msg = "Failed to remove new vm..."
                        printLog("[TABLE SEARCH] " + msg)
                        break
                except Exception as e:
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[TABLE SEARCH] " + msg)
                    continue

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REMOVE] " + msg)
        printLog("[VM REMOVE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
