from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__testlink__ import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
class vm_vm:
    def __init__(self, webDriver):
        self.webDriver = webDriver
        self._vmPortalResult = []
        self._vmName = 'auto_vm_%s'%randomString()
        self._vmCPUs = 2

        self.tl = testlink()

    def test(self):
        # self.create() # 가상머신 생성 코드 문제로 인해 보류
        self.detail()
        self.update()
        self.remove()

    def create(self):
        self.tl.junitBuilder('VM_PORTAL_LOGIN', PASS, '') # VM 포털 로그인 
        
        printLog('- Create VM')
        result = FAIL
        msg = ''


        try:
            # 가상 머신 생성 버튼 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'route-add-vm-button')
            self.webDriver.findElement('id','route-add-vm-button', True)
            # 이름 입력            
            self.webDriver.findElement('id','create-vm-wizard-basic-name-edit')
            self.webDriver.sendKeys(self._vmName)
            # 클러스터 클릭 및 Default 선택
            self.webDriver.findElement('id','create-vm-wizard-basic-cluster-edit-button-toggle', True)
            self.webDriver.findElement('css_selector','#create-vm-wizard-basic-cluster-edit > div > ul > li:nth-child(1)')
            a = self.webDriver.getAttribute('textContent')
            
            

            # 프로비저닝 소스 클릭 및 템플릿 선택
            self.webDriver.findElement('id','create-vm-wizard-basic-provision-edit-button-toggle', True)
            try:
                # 한글일 경우
                self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-provision-edit-item-템플릿')
                self.webDriver.findElement('id','create-vm-wizard-basic-provision-edit-item-템플릿', True)
            except: 
                # 영문일 경우
                self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-provision-edit-item-Template')
                self.webDriver.findElement('id','create-vm-wizard-basic-provision-edit-item-Template', True)                
            # 템플릿 클릭 및 Blank 선택
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-template-edit-button-text')
            self.webDriver.findElement('id','create-vm-wizard-basic-template-edit-button-text', True)
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-template-edit-item-Blank')
            self.webDriver.findElement('id','create-vm-wizard-basic-template-edit-item-Blank', True)
            # 다음 클릭
            self.webDriver.findElement('css_selector', '.btn:nth-child(3)', True)
            # NIC 생성
            self.webDriver.findElement('css_selector', '#create-vm-wizards-net > div > div.blank-slate-pf-main-action > button', True)
            self.webDriver.findElement('css_selector', '#create-vm-wizards-net > div._2w_sbU1I-QKEdNDpIvRpri > div > button.btn.btn-primary', True)
            # 다음 클릭
            self.webDriver.findElement('css_selector', 'body > div:nth-child(3) > div.fade.in.modal > div > div > div > div.wizard-pf-footer.modal-footer > button.btn.btn-primary', True)
            # 디스크 생성
            self.webDriver.findElement('css_selector', '#create-vm-wizards-storage > div > div.blank-slate-pf-main-action > button', True)
            self.webDriver.findElement('css_selector', '#create-vm-wizards-storage > div._5dFBDOu9x8heSWkSiAvka > div > button.btn.btn-primary', True)
            # 다음 클릭
            self.webDriver.findElement('css_selector', 'body > div:nth-child(3) > div.fade.in.modal > div > div > div > div.wizard-pf-footer.modal-footer > button.btn.btn-primary', True)
            # 가상 머신 생성 클릭
            self.webDriver.findElement('css_selector', 'body > div:nth-child(3) > div.fade.in.modal > div > div > div > div.wizard-pf-footer.modal-footer > button.btn.btn-primary', True)
            # 생성 확인
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-review-review-progress-success')            
            self.webDriver.findElement('id','create-vm-wizard-review-review-progress-success')
            #print(self.webDriver.getAttribute('textContent'))

            time.sleep(2)
            if 'SUCCESS' in self.webDriver.getAttribute('textContent') or '성공' in self.webDriver.getAttribute('textContent'):
                result = PASS
                msg = self.webDriver.getAttribute('textContent')
                printLog("* VM NAME : %s"%self._vmName)

            self.webDriver.findElement('css_selector', 'body > div:nth-child(3) > div.fade.in.modal > div > div > div > div.wizard-pf-footer.modal-footer > button:nth-child(3)', True)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("* RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_CREATE', result, msg)

    def detail(self):

        printLog('- Detail VM')
        result = FAIL
        msg = ''

        try: 
            # 생성한 VM 이름 클릭
            self.webDriver.findElement('id','vm-' + self._vmName + '-name', True)
            # 세부 정보의 이름이 보이면 성공
            self.webDriver.explicitlyWait(10, By.ID, 'vmdetail-overview-name')
            self.webDriver.findElement('id', 'vmdetail-overview-name')
            if self._vmName in self.webDriver.getAttribute('textContent'):
                result = PASS
                msg = ''                
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        
        printLog("* RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm detail' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_DETAIL', result, msg)
        # 처음화면으로 돌아가기
        self.webDriver.findElement('id','breadcrumb-link-0', True) 

    def update(self):        
        printLog('- Update VM')
        result = FAIL
        msg = ''

        try: 
            # 생성한 VM 이름 클릭
            self.webDriver.findElement('id','vm-' + self._vmName + '-name', True)                        
            # 상세정보 편집 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'vmdetail-details-button-edit')
            self.webDriver.findElement('id','vmdetail-details-button-edit', True)

            self.webDriver.findElement('id','vmdetail-details-cpus-edit')

            self.webDriver.clear()
            self.webDriver.sendKeys(Keys.CONTROL + "a")
            self.webDriver.sendKeys(self._vmCPUs)
            self.webDriver.findElement('id','vmdetail-details-button-save', True)
            time.sleep(1)

            self.webDriver.findElement('id','vmdetail-details-cpus')
            if str(self._vmCPUs) == self.webDriver.getAttribute('textContent'):
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("* RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm update' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_UPDATE', result, msg)
        
        # 초기화면 돌아가기
        self.webDriver.findElement('id','breadcrumb-link-0', True) 

    def remove(self):
        printLog('* Wait 30 seconds')
        time.sleep(30)

        printLog('- Remove VM')
        result = FAIL
        msg = ''

        try: 
            # 생성한 VM 이름 클릭
            self.webDriver.findElement('id','vm-' + self._vmName + '-name', True)       
            # 삭제 버튼 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'vmaction-' + self._vmName + '-actions-button-remove-title')
            self.webDriver.findElement('id', 'vmaction-' + self._vmName + '-actions-button-remove-title', True)
            # 디스크 유지 클릭
            self.webDriver.findElement('css_selector', '#vmaction-' + self._vmName + '-actions-preservedisks > div > label > input', True)
            # 삭제 버튼 클릭
            self.webDriver.findElement('css_selector', 'body > div:nth-child(3) > div.fade.message-dialog-pf.in.modal > div > div > div.modal-footer > button.btn.btn-danger', True)
            # 삭제 확인
            time.sleep(10)
            try:
                self.webDriver.findElement('id','vm-' + self._vmName + '-name')
                msg = 'Remove failed'
            except Exception as e:
                msg = str(e).replace("\n",'')
                msg = msg[:msg.find('Element <')]
                if "no such element" in msg.lower():
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
            
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("* RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_REMOVE', result, msg)