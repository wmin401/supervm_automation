# -*- coding: utf-8 -*-
from random import weibullvariate
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
        self.create() # 가상머신 생성 코드 문제로 인해 보류
        self.detail()
        self.update()
        self.remove()

    def create(self):
        self.tl.junitBuilder('VM_PORTAL_LOGIN', PASS, '') # VM 포털 로그인 
        
        printLog(printSquare('Create VM in Portal'))
        result = FAIL
        msg = ''


        try:
            time.sleep(1)
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'route-add-vm-button')
            self.webDriver.findElement('id', 'route-add-vm-button', True)
            time.sleep(0.5)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-name-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-name-edit', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-name-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-name-edit', False)
            self.webDriver.sendKeys(self._vmName)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-description-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-description-edit', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-description-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-description-edit', False)
            self.webDriver.sendKeys('automated creation')

            # 클러스터 click
            self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-cluster-edit-button-toggle').click()")
            time.sleep(0.1)

            # 메뉴 중 Default 클릭
            self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-cluster-edit-item-Default (Default)').click()")
            time.sleep(0.1)
            
            # 프로비저닝 소스 클릭
            self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-provision-edit-button-toggle').click()")
            time.sleep(0.1)

            # 메뉴 중 템플릿 클릭
            try:
                self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-provision-edit-item-템플릿').click()")
            except:
                self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-provision-edit-item-Template').click()")            
            time.sleep(0.1)

            # 템플릿 클릭
            self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-template-edit-button-toggle').click()")
            time.sleep(0.1)

            # Blank 클릭
            self.webDriver.executeScript("document.getElementById('create-vm-wizard-basic-template-edit-item-Blank').click()")
            time.sleep(0.1)

            # click
            self.webDriver.findElement('xpath', '/html/body/div[2]/div[2]/div/div/div/div[3]/button[3]', True)
            time.sleep(0.1)

            # click            
            self.webDriver.findElement('css_selector', '#create-vm-wizards-net > div > div.blank-slate-pf-main-action > button', True)
            time.sleep(0.1)

            # click
            self.webDriver.findElement('css_selector', '#create-vm-wizards-net > div.src-components-CreateVmWizard-steps-style__nic-table--1korfGa-KL > div > button.btn.btn-primary', True)
            time.sleep(0.1)

            # click
            self.webDriver.findElement('xpath', '/html/body/div[2]/div[2]/div/div/div/div[3]/button[3]', True)
            time.sleep(0.1)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#create-vm-wizards-storage > div > div.blank-slate-pf-main-action > button')
            self.webDriver.findElement('css_selector', '#create-vm-wizards-storage > div > div.blank-slate-pf-main-action > button', True)
            time.sleep(0.1)

            # type
            
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizards-storage-undefined-size-edit')
            self.webDriver.findElement('id', 'create-vm-wizards-storage-undefined-size-edit', True)
            self.webDriver.sendKeys('1')
            time.sleep(0.3)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#create-vm-wizards-storage > div.src-components-CreateVmWizard-steps-style__disk-table--2onYAmcpqP > div > button.btn.btn-primary')
            self.webDriver.findElement('css_selector', '#create-vm-wizards-storage > div.src-components-CreateVmWizard-steps-style__disk-table--2onYAmcpqP > div > button.btn.btn-primary', True)
            time.sleep(0.3)

            # click
            self.webDriver.findElement('xpath', '/html/body/div[2]/div[2]/div/div/div/div[3]/button[3]', True)
            time.sleep(0.1)

            # click
            self.webDriver.findElement('xpath', '/html/body/div[2]/div[2]/div/div/div/div[3]/button[3]', True)
            time.sleep(5)
   
            self.webDriver.findElement('css_selector','#create-vm-wizard-review-review-progress-success > div.src-components-CreateVmWizard-steps-style__review-text--2hWB4OczhF')
            if 'SUCCESS' in self.webDriver.getAttribute('textContent') or '성공' in self.webDriver.getAttribute('textContent'):
                result = PASS
                msg = self.webDriver.getAttribute('textContent')
                printLog("[PORTAL VM CREATE] VM NAME : %s"%self._vmName)

            self.webDriver.findElement('xpath', '/html/body/div[2]/div[2]/div/div/div/div[3]/button[3]', True)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[PORTAL VM CREATE] RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_CREATE', result, msg)

    def detail(self):

        printLog(printSquare('Detail VM in Portal'))
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
        
        printLog("[PORTAL VM DETAIL] RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm detail' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_DETAIL', result, msg)
        # 처음화면으로 돌아가기
        self.webDriver.findElement('id','breadcrumb-link-0', True) 

    def update(self):        
        printLog(printSquare('Update VM in Portal'))
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
            printLog("[PORTAL VM UPDATE] Change VM's CPU 1 to 2")
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
        printLog("[PORTAL VM UPDATE] RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm update' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_UPDATE', result, msg)
        
        # 초기화면 돌아가기
        self.webDriver.findElement('id','breadcrumb-link-0', True) 

    def remove(self):
        printLog('[PORTAL VM REMOVE] Wait 15 seconds until the disk is unlocked.')
        time.sleep(15)

        printLog(printSquare('Remove VM in Portal'))
        result = FAIL
        msg = ''

        try: 
            # 생성한 VM 이름 클릭
            self.webDriver.findElement('id','vm-' + self._vmName + '-name', True)   
            time.sleep(0.3)    
            # 삭제 버튼 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'vmaction-' + self._vmName + '-actions-button-remove-title')
            self.webDriver.findElement('id', 'vmaction-' + self._vmName + '-actions-button-remove-title', True)
            # 디스크 유지 클릭
            self.webDriver.findElement('css_selector', '#vmaction-' + self._vmName + '-actions-preservedisks > div > label > input', True)
            # 삭제 버튼 클릭
            self.webDriver.findElement('xpath', '/html/body/div[2]/div[2]/div/div/div[3]/button[2]', True)
            
            result = PASS
            msg = ''
            
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[PORTAL VM REMOVE] RESULT : " + result)
        self._vmPortalResult.append(['vm portal' + DELIM + 'vm remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_PORTAL_VM_REMOVE', result, msg)