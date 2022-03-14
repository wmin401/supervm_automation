from re import T
import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import testlink
class admin_vm:
    def __init__(self, webDriver):
        # printLog('VM 1 TEST includes CRUD')
        self._vmResult = []
        self._vmName = 'auto_vm_%s'%randomString()
        # self._vmName = 'for_automation'
        self._diskName = '%s_Disk1'%self._vmName
        # self._diskName = 'auto_vm_HnpZbEOS_Disk1'
        self._diskSize = '5'        
        self._networkInterfaceName = 'auto_nic_%s'%randomString()

        self.webDriver = webDriver
        printLog("iso 파일이 디스크에 추가되어있어야지 가상머신 생성 가능")

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
        cnt = 0
        while True:
            time.sleep(1)
            try:
                tableValueList = self.webDriver.tableSearch(self._diskName, 0, False, False, True)
                if 'OK' in tableValueList[10]:
                    printLog("[DISK STATUS] Disk's status is OK")
                    status = True
                    break
                elif '잠김' in tableValueList[10] or 'Locked' in tableValueList[10]:                    
                    if cnt == 0:
                        printLog("[DISK STATUS] Disk's status is still locked...")                    
                        cnt = 1
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

    def advancedOption(self):
        # 고급 옵션 표시 클릭 (열려있으면 누르지 않음)
        self.webDriver.findElement('css_selector','#VmPopupView_OnAdvanced > button')
        advancedOption = self.webDriver.getAttribute('textContent')
        if advancedOption == '고급 옵션 숨기기' or advancedOption == 'Hide Advanced Options':
            pass
        elif advancedOption == '고급 옵션 표시' or advancedOption == 'Show Advanced Options':
            self.webDriver.click()
        time.sleep(1)

    def test(self):
        # VM 생성 - 2
        time.sleep(5)
        self.create()
        # self.createWindows()

        # # 가상 디스크 - 4
        # self.addVirtualDisk()
        # self.attachDisk()
        # # self.virtualDiskHotPlugging()
        # self.removeVirtualDisk()

        # # 네트워크 인터페이스 - 4
        # self.addNetworkInterface()
        # self.updateNetworkInterface()
        # self.networkInterfaceHotPlugging()
        # self.deleteNetworkInterface()

        # # # # 업데이트 - 1
        # self.update()

        # # # 복사 - 1 
        # self.copy()

        # 실행 - 1
        self.run()

        # 호스트 - 2
        # self.pinToMultipleHosts()
        # self.ViewingPinnedToHost()

        # # 가상 메모리 - 2
        # self.virtualMemoryHotPlugging()
        # # self.virtualMemoryHotUnplugging()

        # # vcpu - 1
        # self.hotPluggingVCPU()

        # # cd변경 - 1
        self.changeCD()

        # 종료 및 정지 - 4
        self.reboot()
        # self.pause()
        # self.shutdown()
        # self.remove()

    def setup(self):
        # 컴퓨팅
        time.sleep(1)
        printLog("[VM SETUP] Compute - Virtual Machines")
        self.webDriver.findElement('id','compute', True)
        time.sleep(1)

        # 가상머신
        self.webDriver.findElement('id','MenuView_vmsAnchor',True)
        self.webDriver.implicitlyWait(10)
        time.sleep(3)

    def create(self):
        printLog(printSquare('Create VM'))
        result = FAIL
        msg = ''

        try:            
            self.setup()

            # 새로 만들기
            # printLog('New VM Button', True)
            self.webDriver.findElement('id','ActionPanelView_NewVm',True)
            time.sleep(2)

            # 이름 입력
            # printLog('Input Name', True)
            self.webDriver.findElement('id','VmPopupWidget_name',True)
            self.webDriver.sendKeys(self._vmName)

            # 디스크 생성 클릭
            # printLog('Create disk', True)
            self.webDriver.findElement('id','VmPopupWidget_instanceImages__createEdit',True)
            time.sleep(1)

            # 크기 입력
            # printLog('Input size', True)
            self.webDriver.findElement('id','VmDiskPopupWidget_size',True)
            self.webDriver.sendKeys(self._diskSize)
            
            # OK 버튼 클릭
            # printLog('Click OK', True)
            self.webDriver.findElement('id','VmDiskPopupView_OnSave',True)
            time.sleep(2)

            # 고급 옵션 표시 클릭 (열려있으면 누르지 않음)
            # printLog('Open Advanced options', True)
            self.webDriver.findElement('css_selector','#VmPopupView_OnAdvanced > button')
            advancedOption = self.webDriver.getAttribute('textContent')
            if advancedOption == '고급 옵션 숨기기' or advancedOption == 'Hide Advanced Options':
                pass
            elif advancedOption == '고급 옵션 표시' or advancedOption == 'Show Advanced Options':
                self.webDriver.click()
            time.sleep(1)

            # 부트 옵션 클릭
            # printLog('Boot options', True)
            self.webDriver.findElement('css_selector','#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(9) > a',True)

            # 첫 번째 장치 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_firstBootDevice',True)
            
            # 첫 번째 장치 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmPopupWidget_firstBootDevice > div > ul > li:nth-child(2)',True)
            
            # CD/DVD 연결 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_cdAttached',True)

            # OK 클릭
            # printLog('OK 클릭', True)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmPopupView_OnSave > button',True)
            
            # printLog('Table 검색', True)
            time.sleep(15)
            _createCheck = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
            if _createCheck == False:
                result = FAIL
                msg = "Failed to create new vm..."
                printLog("[VM CREATE] MESSAGE : " + msg)

            else:
                result = PASS
                printLog("VM NAME : %s"%self._vmName)
                printLog("VM DISK NAME : %s_disk"%self._vmName)
                printLog("VM DISK SIZE : %s GiB"%self._diskSize)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CREATE] MESSAGE : " + msg)
        printLog("[VM CREATE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_CREATE',result, msg) # 모두 대문자

    def createWindows(self):
        printLog(printSquare('Create windows VM'))
        result = FAIL
        msg = ''

        try:            
            self.setup()

            # 새로 만들기
            self.webDriver.findElement('id','ActionPanelView_NewVm',True)
            time.sleep(2)

            # 이름 입력
            self.webDriver.findElement('id','VmPopupWidget_name',True)
            self.windowsVMName = 'auto_vm_windows_%s'%randomString()
            self.webDriver.sendKeys(self.windowsVMName)

            # 운영 시스템 변경
            self.webDriver.findElement('css_selector','#VmPopupWidget_osType > div > button', True)
            lis = self.webDriver.findElement('css_selector_all', '#VmPopupWidget_osType > div > ul > li')
            for li in lis:
                if 'Windows 10' == li.get_attribute('textContent'):
                    li.click()
                    break

            # 디스크 생성 클릭
            self.webDriver.findElement('id','VmPopupWidget_instanceImages__createEdit',True)
            time.sleep(1)

            # 크기 입력
            self.webDriver.findElement('id','VmDiskPopupWidget_size',True)
            self.webDriver.sendKeys(self._diskSize)
            
            # OK 버튼 클릭
            self.webDriver.findElement('id','VmDiskPopupView_OnSave',True)
            time.sleep(2)

            self.advancedOption()

            # 부트 옵션 클릭
            self.webDriver.findElement('css_selector','#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(9) > a',True)

            # 첫 번째 장치 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_firstBootDevice',True)
            
            # 첫 번째 장치 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmPopupWidget_firstBootDevice > div > ul > li:nth-child(2)',True)
            
            # CD/DVD 연결 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmPopupWidget_cdAttached',True)
            time.sleep(.3)

            # windows.iso 클릭            
            self.webDriver.findElement('css_selector', '#VmPopupWidget_cdImage > div > button', True)
            lis = self.webDriver.findElement('css_selector_all', '#VmPopupWidget_cdImage > div > ul > li')
            for li in lis:
                if 'Windows10.iso' == li.get_attribute('textContent'):
                    li.click()

            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmPopupView_OnSave > button',True)
            time.sleep(15)

            # 생성 확인
            _createCheck = self.webDriver.tableSearch(self.windowsVMName, 2, False, False, True)
            if _createCheck == False:
                result = FAIL
                msg = "Failed to create new vm..."
                printLog("[VM CREATE WINDOWS] MESSAGE : " + msg)

            else:
                result = PASS
                printLog("VM NAME : %s"%self.windowsVMName)
                printLog("VM DISK NAME : %s_disk"%self.windowsVMName)
                printLog("VM DISK SIZE : %s GiB"%self._diskSize)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CREATE WINDOWS] MESSAGE : " + msg)
        printLog("[VM CREATE WINDOWS] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'create windows' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_CREATE_WINDOWS',result, msg) # 모두 대문자

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
            time.sleep(3)        

            # 설명 변경            
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_description')
            self.webDriver.findElement('id', 'VmPopupWidget_description')
            self.webDriver.clear()
            self.webDriver.sendKeys('updated by automation')

            # OK 클릭
            self.webDriver.findElement('id', 'VmPopupView_OnSave', True)
            time.sleep(2)

            # VM 이름 클릭
            des = self.webDriver.tableSearch(self._vmName, 2, False, False, True)

            if 'updated by automation' in des[15]:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to update vm'
                printLog("[VM UPDATE] MESSAGE : " + msg)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM UPDATE] MESSAGE : " + msg)
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
            self.webDriver.findElement('id', 'VmPopupWidget_name', True)
            self.webDriver.sendKeys('copy_%s'%self._vmName)

            self.webDriver.findElement('id', 'VmPopupWidget_description', True)
            self.webDriver.clear()
            self.webDriver.sendKeys('copied by automation')

            self.webDriver.findElement('id', 'VmPopupView_OnSave', True)

            time.sleep(60)

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
                        printLog("[VM COPY] MESSAGE : " + msg)                  
                        break
                except Exception as e:
                    result = FAIL
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[VM COPY] MESSAGE : " + msg)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM COPY] MESSAGE : " + msg)
        printLog("[VM COPY] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'copy' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_COPY',result, msg) # 모두 대문자

        printLog("[VM COPY] Wait until vm's status will be ok")

        time.sleep(60)

    def run(self):

        printLog(printSquare('Run VM'))
        time.sleep(2)

        # 스케줄링 정책이 power_saving 이면 됨
        # cc = admin_cluster(self.webDriver)
        # cc.scheduling()

        result = FAIL
        msg = ''

        try:        
            if not self.diskStatus():
                result = FAIL
                msg = 'Disk is locked(timeout)...'
                printLog("[VM RUN] MESSAGE : " + msg)
                self.tl.junitBuilder('VM_RUN',result, msg) # 모두 대문자

            self.setup()

            # 생성한 vm 클릭
            self.webDriver.tableSearch(self._vmName, 2, True)            
            self.webDriver.findElement('css_selector','#ActionPanelView_Run > button',True)   

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
                            printLog("[VM RUN] MESSAGE : " + msg)
                            cnt += 1
                        continue
                    ed = time.time()
                    if ed - st > 300:
                        result = FAIL
                        msg = 'Failed to run vm ...'
                        printLog("[VM SHUTDOWN] MESSAGE : " + msg)
                        break

                except Exception as e:
                    result = FAIL
                    msg = str(e).replace("\n",'')
                    msg = msg[:msg.find('Element <')]
                    printLog("[VM RUN] MESSAGE : " + msg)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM RUN] MESSAGE : " + msg)
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
            if 'Down' in isRun[13]: # 실행중이지 않을 경우 종료
                result = FAIL
                msg = 'VM is not running ...'
                printLog("[VM SHUTDOWN] MESSAGE : " + msg)
                printLog("[VM SHUTDOWN] RESULT : " + result)
                self._vmResult.append(['vm' + DELIM + 'shutdown' + DELIM + result + DELIM + msg])        
                self.tl.junitBuilder('VM_SHUTDOWN',result, msg) # 모두 대문자
                return
            # 선택
            self.webDriver.tableSearch(self._vmName, 2, True)
            self.webDriver.findElement('css_selector','#ActionPanelView_Shutdown > button:nth-child(1)',True)
            time.sleep(3)
                # OK 클릭
            try:
                self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnShutdown > button',True)
            except:
                pass

            time.sleep(2)
            printLog("[STATUS CHECK] Check status changed")
            st = time.time()
            before = ''
            t = 300
            while True:
                ed = time.time()
                if result == PASS:
                    break
                if ed-st >= t:
                    printLog("[%s STATUS] Failed status changed : %ss Timeout"%(self._vmName,t))
                    result, msg = FAIL, 'Timeout'
                    break
                time.sleep(1)
                tableValueList = []
                try:
                    listUp = False
                    table = self.webDriver.findElement('css_selector', 'tbody')
                    for tr in table.find_elements_by_tag_name("tr"):
                        if listUp == True:
                            break
                        td = tr.find_elements_by_tag_name("td")
                        if self._vmName == td[2].text:
                            tableValueList = []
                            for i in range(len(td)):
                                try:
                                    tableValueList.append(td[i].text)
                                except:
                                    tableValueList.append('')
                            printLog('[TABLE SEARCH] TABLE : ' + str(tableValueList))
                            listUp = True
                            break
                    printLog(tableValueList, debug=True)    
                    current = tableValueList[13]
                    for failStr in ['Up', '전원을 끄는 중']:
                        if failStr in tableValueList[13]:
                            if current != before:
                                printLog("[%s STATUS] %s"%(self._vmName, tableValueList[13]))
                                before = current

                    for passStr in ['Down']:
                        if passStr == tableValueList[13]:
                            printLog("[%s STATUS] %s"%(self._vmName, tableValueList[13]))
                            result, msg = PASS, ''
                            break
                except Exception as e: 
                    printLog('[STATUS CHECK EXCEPTION] %s'%(str(e)))
                    continue
            

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM SHUTDOWN] MESSAGE : " + msg)
        printLog("[VM SHUTDOWN] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'shutdown' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_SHUTDOWN',result, msg) # 모두 대문자

    def reboot(self, save = True):
        printLog(printSquare('Reboot VM'))
        result = FAIL
        msg = ''

        try:        
            self.setup()
            printLog(self.webDriver.getDriver().current_url, debug=True)

            # 생성한 vm 클릭
            isRun = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
            if 'Down' in isRun[13]: # 실행중이지 않을 경우 종료
                result = FAIL
                msg = 'VM is not running ...'
                printLog("[VM REBOOT] MESSAGE : " + msg)
                printLog("[VM REBOOT] RESULT : " + result)
                self._vmResult.append(['vm' + DELIM + 'shutdown' + DELIM + result + DELIM + msg])        
                self.tl.junitBuilder('VM_SHUTDOWN',result, msg) # 모두 대문자
                return
            printLog(self.webDriver.getDriver().current_url, debug=True)

            # 선택
            self.webDriver.tableSearch(self._vmName, 2, True)
            # 재부팅 클릭
            self.webDriver.findElement('id','ActionPanelView_Reboot', True)
            time.sleep(1)
            printLog(self.webDriver.getDriver().current_url, debug=True)
            # OK 클릭
            self.webDriver.findElement('css_selector','#DefaultConfirmationPopupView_OnReboot > button', True)
            # 결과 확인
            result, msg = self.webDriver.isChangedStatus(self._vmName, 2, 13, ['다시 시작 중', 'Rebooting'], ['Up', '실행 중'], 180)

            printLog(self.webDriver.getDriver().current_url, debug=True)
        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REBOOT] MESSAGE : " + msg)
        
        if save == True:
            printLog("[VM REBOOT] RESULT : " + result)
            self._vmResult.append(['vm' + DELIM + 'reboot' + DELIM + result + DELIM + msg])
            
            self.tl.junitBuilder('VM_REBOOT',result, msg) # 모두 대문자

    def remove(self):
        printLog(printSquare('Remove VM'))
        result = FAIL
        msg = ''

        try:       
            if not self.diskStatus():
                result = FAIL
                msg = 'Disk is locked...'
                printLog("[REMOVE VM] RESULT : " + result)
                printLog("[REMOVE VM] MESSAGE : " + msg)
                self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자
                return

            self.setup()

            cnt = 0
            while True:
                time.sleep(1)
                self.webDriver.tableSearch(self._vmName, 2, True)            
                # self.webDriver.tableSearch('auto_vm_HnpZbEOS', 2, True)            
                self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
                time.sleep(0.3)
                self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

                self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#RemoveConfirmationPopupView_OnRemove > button')
                self.webDriver.findElement('css_selector', '#RemoveConfirmationPopupView_OnRemove > button', True)

                time.sleep(2)
                    
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
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REMOVE] MESSAGE : " + msg)
        printLog("[VM REMOVE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_REMOVE',result, msg) # 모두 대문자

        time.sleep(5)

    def addNetworkInterface(self):

        printLog(printSquare('Add Network Interface'))
        result = FAIL
        msg = ''


        try:       
            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 네트워크 인터페이스 클릭
            time.sleep(2)
            try:
                self.webDriver.findElement('link_text', '네트워크 인터페이스', True)
            except:
                self.webDriver.findElement('link_text', 'Network Interfaces', True)
            time.sleep(1)

            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)
            time.sleep(2)

            self.webDriver.findElement('id', 'NetworkInterfacePopupWidget_name', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._networkInterfaceName)

            self.webDriver.findElement('css_selector', '#VmInterfacePopupView_OnSave > button', True)
            time.sleep(5)

            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            for li in ul.find_elements_by_tag_name('li'):
                nidList = li.find_element_by_css_selector('div.list-view-pf-main-info > div.list-view-pf-body > div:nth-child(1) > div.list-group-item-heading')
                if self._networkInterfaceName in nidList.text:
                    result = PASS
                    msg = ''
                    break
                else:
                    result = FAIL
                    msg = 'Failed to add network interface'
                    printLog("[VM ADD NETWORK INTERFACE] MESSAGE : " + msg)
            
        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM ADD NETWORK INTERFACE] MESSAGE : " + msg)
        printLog("[VM ADD NETWORK INTERFACE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'add network interface' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_ADD_NETWORK_INTERFACE',result, msg) # 모두 대문자

    def updateNetworkInterface(self):

        printLog(printSquare('Update Network Interface'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 네트워크 인터페이스 클릭
            time.sleep(0.5)
            try:
                self.webDriver.findElement('link_text', '네트워크 인터페이스', True)
            except:
                self.webDriver.findElement('link_text', 'Network Interfaces', True)
            time.sleep(0.5)

            self.webDriver.findElement('id', 'DetailActionPanelView_Edit', True)
            time.sleep(0.5)
            
            # 이름 변경
            self.webDriver.findElement('id', 'NetworkInterfacePopupWidget_name', True)
            self.webDriver.clear()
            self.webDriver.sendKeys('updated_' + self._networkInterfaceName)

            # OK 클릭
            self.webDriver.findElement('css_selector', '#VmInterfacePopupView_OnSave > button', True)
            time.sleep(2)

            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            for li in ul.find_elements_by_tag_name('li'):
                nidList = li.find_element_by_css_selector('div.list-view-pf-main-info > div.list-view-pf-body > div:nth-child(1) > div.list-group-item-heading')
                if 'updated_' + self._networkInterfaceName in nidList.text:
                    result = PASS
                    msg = ''
                    break
                else:
                    result = FAIL
                    msg = 'Failed to add network interface'
                    printLog("[VM UPDATE NETWORK INTERFACE] MESSAGE : " + msg)
            
        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM UPDATE NETWORK INTERFACE] MESSAGE : " + msg)
        printLog("[VM UPDATE NETWORK INTERFACE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'update network interface' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_UPDATE_NETWORK_INTERFACE',result, msg) # 모두 대문자

    def networkInterfaceHotPlugging(self):

        printLog(printSquare('Network Interface Hot plugging'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 네트워크 인터페이스 클릭
            time.sleep(0.5)
            try:
                self.webDriver.findElement('link_text', '네트워크 인터페이스', True)
            except:
                self.webDriver.findElement('link_text', 'Network Interfaces', True)
            time.sleep(0.5)

            self.webDriver.findElement('id', 'DetailActionPanelView_Edit', True)
            time.sleep(0.5)

            # Down 클릭
            # 분리 클릭
            linkState = self.webDriver.findElement('name_all', 'linkState')
            linkState[1].click()
            cardStatus = self.webDriver.findElement('name_all', 'cardStatus')
            cardStatus[1].click()

            # OK 클릭
            self.webDriver.findElement('css_selector', '#VmInterfacePopupView_OnSave > button', True)
            time.sleep(1)
            
            # OK 클릭
            self.webDriver.findElement('css_selector', '#DefaultConfirmationPopupView_ON_APPROVE > button', True)
            time.sleep(1)

            # 상태 확인
            # 왼쪽 화살표 클릭
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul/li/div[1]/div/span[1]', True)
            time.sleep(0.5)
            networkStatus = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul/li/div[4]/div/div[1]/dl')
            nicStatus = networkStatus.get_attribute('textContent')
            if ('분리' in nicStatus and '정지' in nicStatus) or ('Unplugged' in nicStatus and 'Down' in nicStatus):
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed hot plugging...'
            
        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM NETWORK INTERFACE HOT PLUGGING] MESSAGE : " + msg)
        printLog("[VM NETWORK INTERFACE HOT PLUGGING] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'network interface hot plugging' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_NETWORK_INTERFACE_HOT_PLUGGING',result, msg) # 모두 대문자

    def deleteNetworkInterface(self):

        printLog(printSquare('Delete network interface'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 네트워크 인터페이스 클릭
            time.sleep(0.5)
            try:
                self.webDriver.findElement('link_text', '네트워크 인터페이스', True)
            except:
                self.webDriver.findElement('link_text', 'Network Interfaces', True)
            time.sleep(0.5)

            # 제거 클릭
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)
            time.sleep(0.5)

            self.webDriver.findElement('css_selector', '#RemoveConfirmationPopupView_OnRemove > button', True)
            time.sleep(2)

            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            for li in ul.find_elements_by_tag_name('li'):
                try:
                    nidList = li.find_element_by_css_selector('div.list-view-pf-main-info > div.list-view-pf-body > div:nth-child(1) > div.list-group-item-heading')
                    if self._networkInterfaceName in nidList.text:
                        result = FAIL
                        msg = 'Failed to delete network interface'
                        break
                    else:
                        result = PASS
                        msg = ''
                except:                    
                    result = PASS
                    msg = ''
                    break

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM DELETE NETWORK INTERFACE] MESSAGE : " + msg)
        printLog("[VM DELETE NETWORK INTERFACE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'delete network interface' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_DELETE_NETWORK_INTERFACE',result, msg) # 모두 대문자

    def addVirtualDisk(self):
        
        printLog(printSquare('Add Virtual Disk'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 디스크탭 클릭
            time.sleep(0.5)
            try:
                self.webDriver.findElement('link_text', '디스크', True)
            except:
                self.webDriver.findElement('link_text', 'Disks', True)
            time.sleep(0.5)

            # 새로 만들기클릭
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)
            time.sleep(1)

            self.webDriver.findElement('id', 'VmDiskPopupWidget_size')
            self.webDriver.sendKeys('5')

            self.webDriver.findElement('id', 'VmDiskPopupWidget_alias')
            self.webDriver.clear()
            self.webDriver.sendKeys('added_' + self._diskName)

            self.webDriver.findElement('css_selector', '#VmDiskPopupView_OnSave > button', True)

            result, msg = self.webDriver.isChangedStatus('added_' + self._diskName, 1, 18, ['잠김', 'locked', 'Locked'], ['OK'], 300)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM ADD VIRTUAL DISKS] MESSAGE : " + msg)
        printLog("[VM ADD VIRTUAL DISKS] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'add virtual disks' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_ADD_VIRTUAL_DISKS',result, msg) # 모두 대문자

    def attachDisk(self):
        # 가상 머신에 기존 디스크 연결
        
        printLog(printSquare('Attach Virtual Disk to VM'))
        result = FAIL
        msg = ''

        self._unAttachedDiskName = 'unAttached_disk_' + randomString()

        try:       
            # 스토리지 - 디스크
            printLog("[VM SETUP] Storage - Disks")
            self.webDriver.findElement('id','MenuView_storageTab', True)
            time.sleep(1)
            self.webDriver.findElement('id','MenuView_disksAnchor',True)
            time.sleep(2)
            # 새로 만들기 클릭
            self.webDriver.findElement('id','ActionPanelView_New',True)

            self.webDriver.findElement('id','VmDiskPopupWidget_size')
            self.webDriver.sendKeys('5')
            self.webDriver.findElement('id','VmDiskPopupWidget_alias')
            self.webDriver.sendKeys(self._unAttachedDiskName)
            printLog("[VM SETUP] Disk : %s"%self._unAttachedDiskName)

            self.webDriver.findElement('css_selector', '#VmDiskPopupView_OnSave > button', True)
            time.sleep(5)


            self.webDriver.isChangedStatus(self._unAttachedDiskName, 0, 10, ['잠김', 'Locked', 'locked'], ['OK'], 300)            

            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 디스크탭 클릭
            time.sleep(0.5)
            try:
                self.webDriver.findElement('link_text', '디스크', True)
            except:
                self.webDriver.findElement('link_text', 'Disks', True)
            time.sleep(0.5)

            # 연결 클릭
            self.webDriver.findElement('id', 'DetailActionPanelView_Attach', True)
            time.sleep(3)
        
            table = self.webDriver.findElement('css_selector_all', 'tbody')
            for tr in table[1].find_elements_by_tag_name("tr"):
                td = tr.find_elements_by_tag_name("td")
                if self._unAttachedDiskName == td[1].text:
                    printLog('[TABLE SEARCH] Search : ' + str(td[1].text))
                    td[0].find_element_by_css_selector('div > input').click()
                    break

            # OK 클릭
            self.webDriver.findElement('css_selector', '#VmDiskAttachPopupView_OnSave > button', True)
            time.sleep(1)

            result, msg = self.webDriver.isChangedStatus(self._unAttachedDiskName, 1, 18, ['잠김', 'Locked', 'locked'], ['OK'])

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM ATTACH VIRTUAL DISKS] MESSAGE : " + msg)
        printLog("[VM ATTACH VIRTUAL DISKS] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'attach virtual disks' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_ATTACH_VIRTUAL_DISKS',result, msg) # 모두 대문자

    def virtualDiskHotPlugging(self):
        # - 2-455 : 가상 디스크 핫 플러깅
        # 결과 확인 코드에서 오류발생
        
        printLog(printSquare('Virtual Disk Hot Plugging'))
        result = FAIL
        msg = ''
        try:       
            self.setup()

            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 디스크탭 클릭
            time.sleep(2)
            try:
                self.webDriver.findElement('link_text', '디스크', True)
            except:
                self.webDriver.findElement('link_text', 'Disks', True)
            time.sleep(2)

            # 추가한 가상 디스크 선택
            self.webDriver.tableSearch(self._unAttachedDiskName, 1, rowClick=True)

            # 추가 옵션 버튼 클릭
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/button', True)
            time.sleep(1)
            self.webDriver.findElement('id', 'DetailActionPanelView_Unplug', True)
            time.sleep(1)
            # OK 클릭
            self.webDriver.findElement('css_selector', '#DefaultConfirmationPopupView_OnUnplug > button', True)            
            time.sleep(3)
            
            # 스토리지 - 디스크
            printLog("[VM SETUP] Storage - Disks")
            self.webDriver.findElement('id','MenuView_storageTab', True)
            time.sleep(1)
            self.webDriver.findElement('id','MenuView_disksAnchor',True)
            time.sleep(3)

            self.webDriver.tableSearch(self._unAttachedDiskName, 0, rowClick = False, nameClick = True)
            time.sleep(3)

            try:
                printLog(5, debug=True)
                self.webDriver.findElement('link_text', '가상 머신', True)
            except:
                self.webDriver.findElement('link_text', 'Virtual Machines', True)
            time.sleep(2)

            printLog(5, debug=True)
            result, msg = self.webDriver.isChangedStatus(self._vmName, 1, 9, ['Up'], ['Down'])

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM VIRTUAL DISK HOT PLUGGING] MESSAGE : " + msg)
        printLog("[VM VIRTUAL DISK HOT PLUGGING] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'virtual disk hot plugging' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_VIRTUAL_DISK_HOT_PLUGGING',result, msg) # 모두 대문자

    def removeVirtualDisk(self):
        # - 2-456 : 가상 머신에서 가상 디스크 제거
        
        printLog(printSquare('Remove Virtual Disk to VM'))
        result = FAIL
        msg = ''
        try:       
            self.setup()
            # 가상머신 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 디스크탭 클릭
            time.sleep(0.5)
            try:
                self.webDriver.findElement('link_text', '디스크', True)
            except:
                self.webDriver.findElement('link_text', 'Disks', True)
            time.sleep(0.5)

            # 추가한 가상 디스크 선택
            self.webDriver.tableSearch(self._unAttachedDiskName, 1, rowClick=True)

            # 제거 버튼 클릭
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)
            # 완전 제거 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_latch')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_latch', True)

            # OK 클릭
            self.webDriver.findElement('css_selector', '#RemoveConfirmationPopupView_OnRemoveDisk > button', True)
            time.sleep(5)

            # 결과 확인
            try:
                removeCheck = self.webDriver.tableSearch(self._unAttachedDiskName, 1, False, False, True)
                if removeCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to remove disk'
                    printLog("[VM REMOVE VIRTUAL DISKS] MESSAGE : " + msg)
            except:
                result = PASS
                msg = ''
            


        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REMOVE VIRTUAL DISKS] MESSAGE : " + msg)
        printLog("[VM REMOVE VIRTUAL DISKS] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'remove virtual disks' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_REMOVE_VIRTUAL_DISKS',result, msg) # 모두 대문자

    def virtualMemoryHotPlugging(self):         
        printLog(printSquare('Virtual memory hot plugging'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 클릭
            self.webDriver.tableSearch(self._vmName, 2, True)
            printLog(1, debug=True)

            # 편집 클릭
            self.webDriver.findElement('id','ActionPanelView_Edit',True)
            time.sleep(2)
            printLog('edit popup', debug=True)
            # 시스템 탭 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(2)')
            self.webDriver.findElement('css_selector', '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(2)', True)
            time.sleep(1)
            # 메모리 사이즈 변경
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_memSize')
            self.webDriver.findElement('id', 'VmPopupWidget_memSize')
            self.webDriver.clear()
            self._updateSize = '2048'
            self.webDriver.sendKeys(self._updateSize)
            printLog('changed memory size', debug=True)

            # OK 클릭
            self.webDriver.findElement('css_selector', '#VmPopupView_OnSave > button', True)
            time.sleep(2)

            try:
                self.webDriver.findElement('css_selector', '#VmNextRunConfigurationPopupView_updateExistingVm > button', True)
                time.sleep(3)
            except:
                pass
            printLog('OK double check', debug=True)

            ##############  
            # VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            time.sleep(3)
            printLog('vm name clicked', debug=True)


            self.webDriver.explicitlyWait(10, By.ID, 'SubTabVirtualMachineGeneralView_form_col1_row0_value')
            self.webDriver.findElement('id', 'SubTabVirtualMachineGeneralView_form_col1_row0_value')
            _memorySize = self.webDriver.getAttribute('textContent')
            ##############

            printLog('read memory check', debug=True)

            if self._updateSize in _memorySize:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to update memory size'
                printLog("[VM VIRTUAL MEMORY HOT PLUGGING] " + msg)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM VIRTUAL MEMORY HOT PLUGGING] " + msg)
        printLog("[VM VIRTUAL MEMORY HOT PLUGGING] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'virtual memory hot plugging' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_VIRTUAL_MEMORY_HOT_PLUGGING',result, msg) # 모두 대문자

    def virtualMemoryHotUnplugging(self):        
        printLog(printSquare('Virtual memory hot unplugging'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 이름 클릭            

            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 가상 머신 장치 클릭
            time.sleep(2)
            try:
                self.webDriver.findElement('link_text', '가상 머신 장치', True)
            except:
                self.webDriver.findElement('link_text', 'Vm Devices', True)
            time.sleep(1)

            idx = -1
            table = self.webDriver.findElement('css_selector', 'tbody')
            trs = table.find_elements_by_tag_name('tr')
            for tr in trs:
                idx += 1
                try:
                    td = tr.find_elements_by_tag_name('td')
                    if 'memory' in td[1].text:
                        td[7].find_element_by_css_selector('button').click()
                        time.sleep(3)
                        break
                except:
                    continue
            self.webDriver.findElement('css_selector', '#DefaultConfirmationPopupView_memoryHotUnplug > button', True)
            time.sleep(20)

            self.setup()

            self.webDriver.tableSearch(self._vmName, 2, False, True)
            time.sleep(3)

            self.webDriver.explicitlyWait(10, By.ID, 'SubTabVirtualMachineGeneralView_form_col1_row0_value')
            self.webDriver.findElement('id', 'SubTabVirtualMachineGeneralView_form_col1_row0_value')
            _memorySize = self.webDriver.getAttribute('textContent')

            if '1024' in _memorySize:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to hot unplug memory size'
                printLog("[VM VIRTUAL MEMORY HOT UNPLUGGING] " + msg)
            
        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM VIRTUAL MEMORY HOT UNPLUGGING] MESSAGE : " + msg)
        printLog("[VM VIRTUAL MEMORY HOT UNPLUGGING] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'virtual memory hot unplugging' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_VIRTUAL_MEMORY_HOT_UNPLUGGING',result, msg) # 모두 대문자

    def hotPluggingVCPU(self):
        printLog(printSquare('hot plugging vcpu'))
        result = FAIL
        msg = ''

        try:       
            self.setup()
            # 가상머신 클릭            
            self.webDriver.tableSearch(self._vmName, 2, True)
            # 편집 클릭
            self.webDriver.findElement('id','ActionPanelView_Edit',True)
            time.sleep(3)

            # 시스템 탭 클릭
            self.webDriver.findElement('css_selector', '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(2)', True)
            time.sleep(1)

            # 총 가상 cpu 변경
            self.webDriver.findElement('id', 'VmPopupWidget_totalCPUCores')
            self.webDriver.clear()
            self.webDriver.sendKeys('2')

            # OK 클릭
            self.webDriver.findElement('id', 'VmPopupView_OnSave', True)
            time.sleep(2)

            ##############
            # OK 클릭
            self.webDriver.findElement('css_selector', '#VmNextRunConfigurationPopupView_updateExistingVm > button', True)
            time.sleep(5)

            # VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            time.sleep(3)
            ##############
            self.webDriver.findElement('id', 'SubTabVirtualMachineGeneralView_form_col1_row4_value')
            _cpuNum = self.webDriver.getAttribute('textContent')

            if '2 (2:1:1)' in _cpuNum:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to hot plugging vCPU'
                printLog("[VM HOT PLUGGING VCPU] MESSAGE : " + msg)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM HOT PLUGGING VCPU] MESSAGE : " + msg)
        printLog("[VM HOT PLUGGING VCPU] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'hot plugging vcpu' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_HOT_PLUGGING_VCPU',result, msg) # 모두 대문자

    def pinToMultipleHosts(self):
        printLog(printSquare('Pinning VM to Multiple hosts'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            h = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
            self._specificHost = h[4]
            printLog("VM HOST : %s"%self._specificHost)
            # 생성한 vm 클릭
            self.webDriver.tableSearch(self._vmName, 2, True)

            # 편집 클릭
            self.webDriver.findElement('id','ActionPanelView_Edit',True)
            time.sleep(2)
            self.advancedOption()
            
            time.sleep(1)

            # 특정 호스트 선택
            lis = self.webDriver.findElement('css_selector_all', '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li')
            for li in lis:
                if '호스트' == li.get_attribute('textContent') or 'Hosts' == li.get_attribute('textContent'):
                    li.click()
                    break
            time.sleep(1)
            self.webDriver.findElement('id', 'VmPopupWidget_specificHost', True)

            # # 호스트 선택
            # self.webDriver.findElement('css_selector', '#VmPopupWidget_defaultHost > div > Button', True)
            # lis = self.webDriver.findElement('css_selector_all', '#VmPopupWidget_defaultHost > div > ul > li')
            # for li in lis:
            #     if self._specificHost == li.get_attribute('textContent'):
            #         li.click()
            #         break

            # 고가용성 선택
            for li in lis:
                if '고가용성' == li.get_attribute('textContent') or 'Hosts' == li.get_attribute('textContent'):
                    li.click()
                    break
            time.sleep(1)
            self.webDriver.findElement('id', 'VmPopupWidget_isHighlyAvailable', True)
            time.sleep(1)
            
            self.webDriver.findElement('css_selector', '#VmPopupWidget_lease > div > button', True)
            time.sleep(1)
            
            lis = self.webDriver.findElement('css_selector_all', '#VmPopupWidget_lease > div > ul > li')
            for li in lis:
                if '가상 머신 임대 없음' == li.get_attribute('textContent') or 'No VM Lease' == li.get_attribute('textContent'):
                    li.click()

            # OK
            self.webDriver.findElement('css_selector', '#VmPopupView_OnSave > button', True)
            time.sleep(2)
            self.webDriver.findElement('css_selector', '#VmNextRunConfigurationPopupView_updateExistingVm > button', True)
            time.sleep(3)

            # 재부팅
            self.reboot(save = False)

            # 적용 확인
            self.setup()
            self.webDriver.tableSearch(self._vmName, 2, rowClick = False, nameClick = True)
            time.sleep(1)
                    
            self.webDriver.explicitlyWait(10, By.ID, 'SubTabVirtualMachineGeneralView_form_col1_row7_value')
            self.webDriver.findElement('id', 'SubTabVirtualMachineGeneralView_form_col1_row7_value')
            _highAvailability = self.webDriver.getAttribute('textContent')

            if '예' in _highAvailability or 'Yes' in _highAvailability:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to pin multiple hosts'
                printLog("[VM PIN MULTIPLE HOSTS] MESSAGE : " + msg)

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM PIN MULTIPLE HOSTS] MESSAGE : " + msg)
        printLog("[VM PIN MULTIPLE HOSTS] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'pinning multiple hosts' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PIN_MULTIPLE_HOSTS',result, msg) # 모두 대문자

    def ViewingPinnedToHost(self):
        
        printLog(printSquare('Viewing VM pinned to hosts'))
        result = FAIL
        msg = ''
        # self._vmName = 'auto_vm_VFdPlSqp'
        # self._specificHost = ADMIN_HOSTNAME

        try:          
            # 컴퓨팅 - 호스트
            time.sleep(2)
            printLog("[VM SETUP] Compute - Hosts")
            self.webDriver.findElement('id','compute', True)
            time.sleep(1)
            self.webDriver.findElement('id','MenuView_hostsAnchor',True)
            time.sleep(4)

            self.webDriver.tableSearch(self._specificHost, 2, rowClick = False, nameClick = True)
            time.sleep(2)
            try:
                self.webDriver.findElement('link_text', '가상머신', True)
            except:
                self.webDriver.findElement('link_text', 'Virtual Machines', True)
            time.sleep(2)

            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div[1]/div/div/div/div/div[2]/label[2]', True)

            try:
                isPinned = self.webDriver.tableSearch(self._vmName, 1, rowClick = False, nameClick = False, returnValueList = True)
                if isPinned is not False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to view...'
                    printLog("[VM VIEWING PINNED HOSTS] MESSAGE : " + msg)
            except IndexError as e:
                msg = str(e).replace("\n",'')
                msg = msg[:msg.find('Element <')]
                printLog("[VM VIEWING PINNED HOSTS] MESSAGE : " + msg)
                result = PASS

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM VIEWING PINNED HOSTS] MESSAGE : " + msg)
        printLog("[VM VIEWING PINNED HOSTS] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'viewing pinned hosts' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_VIEWING_PINNED_HOSTS',result, msg) # 모두 대문자

    def changeCD(self):        
        printLog(printSquare('Change CD for VM'))
        result = FAIL
        msg = ''

        try:          
            self.setup()
            self._cdName = 'Windows10.iso'

            # 생성한 vm 클릭
            self.webDriver.tableSearch(self._vmName, 2, True)

            # 꺼내기 생략
            # # 추가 옵션 - CD 변경 클릭
            # self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            # self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_ChangeCD')
            # self.webDriver.findElement('id', 'ActionPanelView_ChangeCD', True)

            # # 꺼내기 선택
            # self.webDriver.findElement('css_selector', '#VmChangeCDPopupWidget_isoImage > div > button', True)
            # selectDropdownMenu(self.webDriver, 'css_selector', '#VmChangeCDPopupWidget_isoImage > div > ul', '[꺼내기]')
            # self.webDriver.findElement('css_selector', '#VmChangeCDPopupView_OnChangeCD > button', True)
            # time.sleep(.5)

            # 추가 옵션 - CD 변경 클릭
            printLog(self.webDriver.getDriver().current_url, debug=True)
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            time.sleep(2)
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_ChangeCD')
            self.webDriver.findElement('id', 'ActionPanelView_ChangeCD', True)
            printLog(self.webDriver.getDriver().current_url, debug=True)
            # Windows10.iso 선택
            self.webDriver.findElement('css_selector', '#VmChangeCDPopupWidget_isoImage > div > button', True)
            selectDropdownMenu(self.webDriver, 'css_selector', '#VmChangeCDPopupWidget_isoImage > div > ul', self._cdName)
            self.webDriver.findElement('css_selector', '#VmChangeCDPopupView_OnChangeCD > button', True)
            time.sleep(2)
            printLog(self.webDriver.getDriver().current_url, debug=True)
            try:
                self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[3]/div[1]/button', True)
                result = FAIL
                msg = 'Unexpected exception'
                printLog("[VM CHANGE CD] MESSAGE : " + msg)
                printLog("[VM CHANGE CD] RESULT : " + result)
                self._vmResult.append(['vm' + DELIM + 'change cd' + DELIM + result + DELIM + msg])
                
                self.tl.junitBuilder('VM_CHANGE_CD',result, msg)
                return
            except:
                pass                
            # 추가 옵션 - CD 변경 클릭
            printLog(self.webDriver.getDriver().current_url, debug=True)
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            time.sleep(.5)
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_ChangeCD')
            self.webDriver.findElement('id', 'ActionPanelView_ChangeCD', True)
            self.webDriver.findElement('css_selector', '#VmChangeCDPopupWidget_isoImage > div > button')
            cd = self.webDriver.getAttribute('textContent')
            if cd == self._cdName:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to change cd'
                printLog("[VM CHANGE CD] MESSAGE : " + msg)
            # 확인 후 취소 클릭            
            self.webDriver.findElement('css_selector', '#VmChangeCDPopupView_Cancel > button', True)
            
        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CHANGE CD] MESSAGE : " + msg)
        printLog("[VM CHANGE CD] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'change cd' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_CHANGE_CD',result, msg) # 모두 대문자

    def pause(self):
        printLog(printSquare('Pause VM'))
        result = FAIL
        msg = ''

        try:        
            self.setup()

            # VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)
            # 일시중지 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Pause')
            self.webDriver.findElement('id','ActionPanelView_Pause', True)
            printLog("[VM PAUSE] Wait until status will change")    
            time.sleep(90)

            self.setup()

            # 결과 확인
            isPaused = self.webDriver.tableSearch(self._vmName, 2, False, False, True)
            printLog(isPaused, debug=True)
            if isPaused[13] == '일시중지됨' or isPaused[13] == 'Suspended':
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to change status to pause'

        except Exception as e:
            result = FAIL
            printLog(str(e))
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM PAUSE] MESSAGE : " + msg)        
            
        printLog("[VM PAUSE] RESULT : " + result)
        self._vmResult.append(['vm' + DELIM + 'pause' + DELIM + result + DELIM + msg])            
        self.tl.junitBuilder('VM_PAUSE',result, msg) # 모두 대문자