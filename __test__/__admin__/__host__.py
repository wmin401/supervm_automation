import time

from __common__.__parameter__ import *
from __common__.__module__ import *

from __common__.__ssh__ import ssh_connection
from __common__.__testlink__ import testlink

class admin_host:
    def __init__(self, webDriver):
        printLog("* 호스트 테스트 시작")
        self._hostResult = []
        self._hostName = 'hypervm171.tmax.dom'
        self._hostIP = '192.168.17.171'
        self._hostID = 'root'
        self._hostPW = 'asdf'
        self.webDriver = webDriver
        self.tl = testlink()

    def addHost(self, connect_ip, connect_id, connect_pw, host_ip, host_name):
        # /etc/hosts에 내용 추가
        # connect_ip : ssh 연결할 ip
        # host_ip : /etc/hosts에 추가할 ip
        # host_name : /etc/hosts에 추가할 fqdn
        ssh_ = ssh_connection(connect_ip, 22, connect_id, connect_pw)
        ssh_.activate()
        # /etc/hosts에 있는지 확인하고 내용 추가
        o, e = ssh_.commandExec('cat /etc/hosts')

        for i in o:
            # print(i)
            if self._hostName in i:
                exist = True
                break
            else:
                exist = False
        if exist == False:
            ssh_.commandExec('echo "%s %s" >> /etc/hosts'%(host_ip, host_name))
            ssh_.deactivate()

    def initialize(self):

        # node_host : 노드의 /etc/hosts에 추가 여부
        # master_host : 마스터 노드의 /etc/hosts에 추가 여부

        printLog("If you want to test host, you have to install packages before test")
        printLog("1. Install ProLinux 8.3")
        printLog("2. Add IP in /etc/hosts")
        printLog("3. Create hypervm repository")
        printLog("4. Disable virt module")
        printLog("5. Enable pki-deps postgresql:12 parfait modules")
        printLog("6. Install ovirt-hosted-engine-setup")


        # 새로 생성한 hosts에 추가
        self.addHost(self._hostIP, 'root', 'asdf', self._hostIP, self._hostName)
        self.addHost(self._hostIP, 'root', 'asdf', ENGINE_VM_IP, ENGINE_VM_FQDN)

        # ENGINE VM 에 추가
        self.addHost(ENGINE_VM_IP, 'root', 'asdf', self._hostIP, self._hostName)

        # admin node 에 추가
        self.addHost(ADMIN_HOST_IP, ADMIN_HOST_ID, ADMIN_HOST_PW, self._hostIP, self._hostName)

        ## 패키지 설치
        ssh_ = ssh_connection(self._hostIP, 22, self._hostID, self._hostPW)
        ssh_.activate()    
        # 레포지토리 파일 생성
        o, e = ssh_.commandExec('ls /etc/yum.repos.d/ |grep hypervm.repo')
        if 'hypervm.repo' in o[0]:
            pass
        else:
            ssh_.commandExec('touch /etc/yum.repos.d/hypervm.repo')
            ssh_.commandExec('echo "[hypervm.repo]" >> /etc/yum.repos.d/hypervm.repo')
            ssh_.commandExec('echo "name=hypervm-repo" >> /etc/yum.repos.d/hypervm.repo')
            ssh_.commandExec('echo "baseurl=http://172.21.7.2/supervm/22.0.0-rc2/prolinux/8/arch/x86_64/" >> /etc/yum.repos.d/hypervm.repo')
            ssh_.commandExec('echo "gpgcheck=0" >> /etc/yum.repos.d/hypervm.repo')
        # 설치
        o, e = ssh_.commandExec('sudo dnf module disable virt -y')
        o, e = ssh_.commandExec('sudo dnf module enable pki-deps postgresql:12 parfait -y')
        o, e = ssh_.commandExec('dnf install -y ovirt-hosted-engine-setup cockpit', 180)
        o, e = ssh_.commandExec('systemctl enable --now cockpit.socket', 180)
        ssh_.deactivate()

    def setup(self):
        time.sleep(1)
        printLog("[HOST SETUP] Compute - Hosts")
        self.webDriver.findElement('id','compute',True)
        time.sleep(1)
        self.webDriver.findElement('id','MenuView_hostsAnchor',True)
        time.sleep(3)
    
    def test(self):

        self.initialize()

        self.create()
        self.configuringHostSPM()
        self.moveToMaintenance()
        self.activateHost()   
        self.viewHostDevice()

        self.moveToMaintenance()
        self.reinstall()     

        self.moveToMaintenance()
        self.remove()


        
    def create(self):
        printLog(printSquare('Create Host'))
        
        try:
            self.setup()

            # 새로 만들기
            self.webDriver.findElement('id', 'ActionPanelView_New', True)
            time.sleep(1)
            self.webDriver.findElement('id', 'HostPopupView_name', True)
            self.webDriver.sendKeys(self._hostName)            
            self.webDriver.findElement('id', 'HostPopupView_host', True)
            self.webDriver.sendKeys(self._hostName)
            self.webDriver.findElement('id', 'HostPopupView_userPassword', True)
            self.webDriver.sendKeys(self._hostPW)
            self.webDriver.findElement('id', 'HostPopupView_rebootHostAfterInstall', True)
            a = self.webDriver.getAttribute('checked')

            # 호스트 엔진 선택
            lis = self.webDriver.findElement('css_selector_all', 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.wizard-pf-sidebar.dialog_noOverflow > ul > li')
            for li in lis:
                if '호스트 엔진' == li.get_attribute('textContent'):
                    li.click()
                    break
            time.sleep(1)

            hostEngine = self.webDriver.findElement('css_selector_all', '#dropdownMenu')
            hostEngine[2].click()
            selectDropdownMenu(self.webDriver, 'xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[6]/div/div[2]/div[2]/div/div[1]/div/div/div/ul', '배포')

            self.webDriver.findElement('id', 'HostPopupView_OnSaveFalse', True)
            time.sleep(1)
            self.webDriver.findElement('css_selector', '#DefaultConfirmationPopupView_OnSaveInternalNotFromApprove > button', True)
            time.sleep(2)

            result, msg = self.webDriver.isChangedStatus(self._hostName, 2, 7, ['Installing', 'Reboot'], ['Up'], 300)

            if result == FAIL:
                _status = self.webDriver.tableSearch(self._hostName, 2, False, False, True)
                if _status[7] == 'InstallFailed' or _status[7] == 'Maintenanace':
                    self.activateHost()

                result, msg = self.webDriver.isChangedStatus(self._hostName, 2, 7, ['Installing', 'Reboot'], ['Up'], 300)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST CREATE] MESSAGE : " + msg)
        printLog("[HOST CREATE] RESULT : " + result)
        self._hostResult.append(['host;create&cancel;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_CREATE',result, msg) # 모두 대문자

    def configuringHostSPM(self):
        printLog(printSquare('Configure Host SPM'))
        
        try:
            self.setup()

            # 생성한 호스트 클릭
            self.webDriver.tableSearch(self._hostName, 2, True)
            # 편집 클릭
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)
            time.sleep(2)

            # 호스트 엔진 선택
            lis = self.webDriver.findElement('css_selector_all', 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.wizard-pf-sidebar.dialog_noOverflow > ul > li')
            for li in lis:
                if 'SPM' == li.get_attribute('textContent'):
                    li.click()
                    break
            time.sleep(1)

            # 높음 선택
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[3]/div/div[2]/div[5]/div/span/input', True)

            # OK 클릭
            self.webDriver.findElement('id', 'HostPopupView_OnSaveFalse', True)
            time.sleep(1)
            self.webDriver.findElement('css_selector', '#DefaultConfirmationPopupView_OnSaveInternalNotFromApprove > button', True)
            time.sleep(2)

            # 호스트 이름 클릭
            self.webDriver.tableSearch(self._hostName, 2, False, True)
            time.sleep(2)

            self.webDriver.findElement('id', 'HostGeneralSubTabView_generalFormPanel_col0_row1_value')
            spmPriority = self.webDriver.getAttribute('textContent')

            if spmPriority == '높음':
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Faild to change SPM priority...'

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST CONFIGURE SPM] MESSAGE : " + msg)
        printLog("[HOST CONFIGURE SPM] RESULT : " + result)
        self._hostResult.append(['host;configure SPM;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_CONFIGURE_SPM',result, msg) # 모두 대문자

    def moveToMaintenance(self):

        printLog(printSquare('Move to Maintenance Mode'))
        
        try:
            self.setup()
            # 생성한 호스트 클릭
            time.sleep(1)
            self.webDriver.tableSearch(self._hostName, 2, True)

            # 관리
            self.webDriver.findElement('css_selector', '#ActionPanelView___ > button', True)
            selectDropdownMenu(self.webDriver, 'css_selector', '#ActionPanelView___ > ul', '유지보수')
            time.sleep(1)
            self.webDriver.findElement('css_selector', '#HostMaintenanceConfirmationPopupView_OnMaintenance > button', True)
            time.sleep(1)

            result, msg = self.webDriver.isChangedStatus(self._hostName, 2, 7, ['Up', 'Down', 'PreparingForMaintenance', 'Unassigned'], ['Maintenance'], 300)


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST MOVE TO MAINTENANCE] MESSAGE : " + msg)
        printLog("[HOST MOVE TO MAINTENANCE] RESULT : " + result)
        self._hostResult.append(['host;move to maintenance;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_MOVE_TO_MAINTENANCE',result, msg) # 모두 대문자

    def activateHost(self):

        printLog(printSquare('Activate host from Maintenance Mode'))
        
        try:
            self.setup()
            # 생성한 호스트 클릭
            self.webDriver.tableSearch(self._hostName, 2, True)

            # 관리
            self.webDriver.findElement('css_selector', '#ActionPanelView___ > button', True)
            selectDropdownMenu(self.webDriver, 'css_selector', '#ActionPanelView___ > ul', '활성')
            time.sleep(3)
            try:
                self.webDriver.findElement('css_selector', '#HostMaintenanceConfirmationPopupView_OnMaintenance > button', True)
            except:
                pass
            time.sleep(1)

            result, msg = self.webDriver.isChangedStatus(self._hostName, 2, 7, ['Unassigned', 'Maintenance', 'Down'], ['Up'], 600)


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST ACTIVATE] MESSAGE : " + msg)
        printLog("[HOST ACTIVATE] RESULT : " + result)
        self._hostResult.append(['host;activate;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_ACTIVATE',result, msg) # 모두 대문자

    def reinstall(self):
        printLog(printSquare('Reinstall host'))
        
        try:
            self.setup()
            # 생성한 호스트 클릭
            self.webDriver.tableSearch(self._hostName, 2, True)

            # 관리
            installBtn = self.webDriver.findElement('css_selector_all', '#ActionPanelView___')[1]
            installBtn.click()
            time.sleep(1)
            
            installDropdownMenu = installBtn.find_elements_by_tag_name('ul')
            for ul in installDropdownMenu:
                lis = ul.find_elements_by_tag_name('li')
                for li in lis:
                    if li.get_attribute('textContent') == '다시 설치':
                        li.click()
                        b = True
                        break
                if b == True:
                    break
            time.sleep(2)
            try:
                self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button', True)
            except:
                pass
            time.sleep(10)

            result, msg = self.webDriver.isChangedStatus(self._hostName, 2, 7, ['Installing', 'Maintenance', 'Down', 'Reboot'], ['Up'], 180)

            if result == FAIL:
                _status = self.webDriver.tableSearch(self._hostName, 2, False, False, True)
                if _status[7] == 'InstallFailed' or _status[7] == 'Maintenanace':
                    self.activateHost()
                
                result, msg = self.webDriver.isChangedStatus(self._hostName, 2, 7, ['Installing', 'Reboot'], ['Up'], 180)


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST REINSTALL] MESSAGE : " + msg)
        printLog("[HOST REINSTALL] RESULT : " + result)
        self._hostResult.append(['host;reinstall;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_REINSTALL',result, msg) # 모두 대문자
  
    def viewHostDevice(self):
        printLog(printSquare('View host devices'))
        
        try:
            self.setup()
            # 생성한 호스트 클릭
            self.webDriver.tableSearch(self._hostName, 2, rowClick = False, nameClick = True)
            time.sleep(1)

            try:
                self.webDriver.findElement('link_text', '호스트 장치', True)
            except:
                self.webDriver.findElement('link_text', 'Host Devices', True)
            time.sleep(0.5)

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST VIEW DEVICES] MESSAGE : " + msg)
        printLog("[HOST VIEW DEVICES] RESULT : " + result)
        self._hostResult.append(['host;view devices;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_VIEW_DEVICES',result, msg) # 모두 대문자

    def remove(self):
        
        printLog(printSquare('Host remove'))
        
        try:
            self.setup()
            # 생성한 호스트 클릭
            self.webDriver.tableSearch(self._hostName, 2, rowClick = True)
            time.sleep(1)
            # 편집 클릭
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)
            time.sleep(1)

            # 호스트 엔진 선택
            lis = self.webDriver.findElement('css_selector_all', 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.wizard-pf-sidebar.dialog_noOverflow > ul > li')
            for li in lis:
                if '호스트 엔진' == li.get_attribute('textContent'):
                    li.click()
                    break
            time.sleep(1)

            hostEngine = self.webDriver.findElement('css_selector_all', '#dropdownMenu')
            hostEngine[2].click()
            selectDropdownMenu(self.webDriver, 'xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[6]/div/div[2]/div[2]/div/div[1]/div/div/div/ul', '배포 취소')

            self.webDriver.findElement('id', 'HostPopupView_OnSaveFalse', True)
            time.sleep(1)
            self.webDriver.findElement('css_selector', '#DefaultConfirmationPopupView_OnSaveInternalNotFromApprove > button', True)
            time.sleep(2)

            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)
            time.sleep(1)
            self.webDriver.findElement('css_selector', '#RemoveConfirmationPopupView_OnRemove > button', True)

            isRemoved = self.webDriver.tableSearch(self._hostName, 2, False, False, True)       

            if isRemoved == False:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to remove host'


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[HOST REMOVE] MESSAGE : " + msg)
        printLog("[HOST REMOVE] RESULT : " + result)
        self._hostResult.append(['host;remove;' + result + ';' + msg])
        self.tl.junitBuilder('HOST_REMOVE',result, msg) # 모두 대문자
  