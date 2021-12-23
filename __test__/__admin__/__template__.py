import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import testlink

from selenium.webdriver.common.by import By


class admin_template:
    def __init__(self, webDriver):
        self._templateResult = []
        self.rs = randomString()
        self._templateName = 'auto_template_' + self.rs
        self.webDriver = webDriver

        self.tl = testlink()
            
    def test(self):

        self.setup()
        
        self.create()
        time.sleep(0.3)
        self.update()
        time.sleep(0.3)
        self.createVM(storage='Thin')        
        time.sleep(0.3)
        self.copyTemplateDisk()
        time.sleep(0.3)
        self.removeVM()
        time.sleep(0.3)
        self.createVM(storage='Copy')
        time.sleep(0.3)
        self.removeVM()
        time.sleep(0.3)
        self.addRole()
        time.sleep(0.3)
        self.removeRole()
        time.sleep(0.3)
        self.remove()

    def setup(self):
        # 컴퓨팅 클릭
        printLog("[SETUP] Compute - Template ")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute',True)

        # 템플릿 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_templatesAnchor')
        self.webDriver.findElement('id','MenuView_templatesAnchor',True)
        
        time.sleep(2)

    def create(self):
        printLog(printSquare('Create Template'))
        try:
            result = FAIL
            msg = ''
            # 중지된 가상머신이 있어야한다.
            # 컴퓨팅 클릭
            printLog("[CREATE TEMPLATE] Compute - Virtual Machines ")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)
            # 가상머신 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_vmsAnchor',True)
            self.webDriver.tableSearch('Down', 13, rowClick=True)
            time.sleep(0.3)
            # 추가 옵션 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button',True)
            
            # 템플릿 생성 클릭
            printLog("[CREATE TEMPLATE] Create template")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_NewTemplate',True)

            # 템플릿 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmMakeTemplatePopupWidget_name')
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_name')
            self.webDriver.sendKeys(self._templateName)
            printLog("[CREATE TEMPLATE] Template name : %s"%self._templateName)

            # 가상 머신 권한 복사 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_copyVmPermissions', True)            

            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmMakeTemplatePopupView_OnNewTemplate', True)
            time.sleep(3)
            # 템플릿 탭
            self.setup()

            printLog("[CREATE TEMPLATE] Check if created")
            printLog("[CREATE TEMPLATE] Wait until status will be OK")
            # table 내부 전부 검색해서 입력한 이름이 있을경우 PASS
            # _createCheck = self.webDriver.tableSearch(self._templateName, 1) # 템플릿 테이블에 숨겨진 열(0)이 하나 있어서 1부터 시작
            st = time.time()
            while True:
                time.sleep(1)
                tableValueList = self.webDriver.tableSearch(self._templateName, 1, rowClick=False, nameClick=False, returnValueList=True)        
                if '잠김' in tableValueList[5] or 'Locked' in tableValueList[5]:
                    printLog("[CREATE VM] Template's status is still locked ...")
                    continue
                elif 'OK' in tableValueList[5]:
                    result = PASS
                    msg = ''
                    break
                ed = time.time()
                if ed-st >= 60:
                    printLog("[CREATE VM] Failed status changed : Timeout")
                    result = FAIL
                    msg = "Failed to create new template..."
                    break

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[CREATE TEMPLATE] MESSAGE : " + msg)
        printLog("[CREATE TEMPLATE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_CREATE', result, msg)

    def update(self):
        printLog(printSquare('Update Template'))
        try:
            result = FAIL
            msg = ''
            # 템플릿 탭
            self.setup()

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._templateName, 1, rowClick=True)    

            # 편집 클릭
            printLog("[UPDATE TEMPLATE] Update template")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)
            
            # 설명에 임의의 문자열 입력 후 저장
            self.webDriver.explicitlyWait(10, By.ID, 'TemplateEditPopupWidget_description')
            self.webDriver.findElement('id', 'TemplateEditPopupWidget_description', True)
            des = randomString()
            self.webDriver.sendKeys(des)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'TemplateEditPopupView_OnSave', True)
            time.sleep(1)

            # 설명에 추가되면 성공
            _updateCheck = self.webDriver.tableSearch(des, 9)
            printLog("[UPDATE TEMPLATE] Check if updated")
            if _updateCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to update new template..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[UPDATE TEMPLATE] MESSAGE : " + msg)
        printLog("[UPDATE TEMPLATE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'update' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_UPDATE', result, msg)

    # 2-533 : 리소스에 관리자 또는 사용자 역할 할당
    def addRole(self):
        printLog(printSquare('Add role'))
        try:
            result = FAIL
            msg = ''
            # 템플릿 탭
            self.setup()
            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            self.webDriver.tableSearch(self._templateName, 1, rowClick=False, nameClick=True)    
            time.sleep(0.3)
            # 권한 탭 클릭
            printLog("[ADD ROLE] Add role")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(6)', True)
            # 추가 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)
            # 모두 라디오 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'PermissionsPopupView_everyoneRadio', True)
            # 드롭다운 메뉴 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'PermissionsPopupView_role', True)
            # 첫번째 역할 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector', '#PermissionsPopupView_role > div > ul > li:nth-child(1)')
            self.role = self.webDriver.getAttribute('textContent')
            self.webDriver.click()
            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'PermissionsPopupView_OnAdd', True)
            time.sleep(2)
            # 생성 확인
            printLog("[ADD ROLE] Check if added")
            _addCheck = self.webDriver.tableSearch(self.role, 4)        
            if _addCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to add new role..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[ADD ROLE] MESSAGE : " + msg)
        printLog("[ADD ROLE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'add role' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_ADD_ROLE', result, msg)

    # 2-534 : 리소스에서 관리자 또는 사용자 역할 제거
    def removeRole(self):
        printLog(printSquare('Remove role'))
        try:
            result = FAIL
            msg = ''
            # 템플릿 탭
            self.setup()
            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            self.webDriver.tableSearch(self._templateName, 1, rowClick=False, nameClick=True)    
            time.sleep(0.3)
            # 권한 탭 클릭
            printLog("[REMOVE ROLE] Remove role")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(6)', True)
            # 생성한 권한 찾아서 클릭
            self.webDriver.tableSearch(self.role, 4, rowClick=True)
            # 제거 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)
            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(2)
            _removeCheck = self.webDriver.tableSearch(self.role, 4)
            printLog("[REMOVE ROLE] Check if removed")
            if _removeCheck == False:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to remove new role..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[REMOVE ROLE] MESSAGE : " + msg)
        printLog("[REMOVE ROLE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'remove role' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_REMOVE_ROLE', result, msg)

    def createVM(self, storage='Thin'):
        self.storage=storage
        printLog(printSquare('Create vm %s using template'%self.storage))
        try:
            result = FAIL
            msg = ''

            self.setup()

            # 새 가상머신
            time.sleep(1)
            printLog("[CREATE VM] New virtual machine")
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_CreateVM')
            self.webDriver.tableSearch(self._templateName, 1, rowClick=True)
            self.webDriver.findElement('id','ActionPanelView_CreateVM',True)
            time.sleep(1)

            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_name')
            self.webDriver.findElement('id', 'VmPopupWidget_name')
            self.webDriver.sendKeys(self._templateName + '_vm_%s'%self.storage)

            # 고급 옵션이 숨겨져 있을 경우 보이게 하기
            self.webDriver.findElement('id', 'VmPopupView_OnAdvanced')
            advanced = self.webDriver.getAttribute('textContent')
            if advanced == '고급 옵션 표시' or advanced == 'Show Advnaced Options':
                self.webDriver.click()
                time.sleep(0.3)
            # 리소스 할당 클릭
            self.webDriver.findElement('css_selector', '#VmPopupWidget > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(8)', True)
            time.sleep(0.3)
            if self.storage == 'hin':
                # 씬 프로비저닝 클릭
                self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_provisioningThin')
                self.webDriver.findElement('id', 'VmPopupWidget_provisioningThin', True)
            elif self.storage == 'Copy':
                # 복제 클릭
                self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_provisioningClone')
                self.webDriver.findElement('id', 'VmPopupWidget_provisioningClone', True)
            
            # 디스크 할당
            self.webDriver.findElement('id', 'VmPopupWidget_disksAllocation_disk0_diskAlias', True)
            self.webDriver.clear()
            self._diskName = self._templateName + '_vm_%s_disk'%self.storage
            self.webDriver.sendKeys(self._diskName)
            time.sleep(0.5)

            # OK 클릭
            self.webDriver.findElement('id', 'VmPopupView_OnSaveVm', True)
            time.sleep(2)
            
            # 컴퓨팅 - 가상머신
            printLog("[CREATE VM] Compute - Virtual Machine")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_vmsAnchor',True)
            time.sleep(2)
            printLog("[CREATE VM] Check if created")
            _createCheck = self.webDriver.tableSearch(self._templateName + '_vm_%s'%self.storage, 2, rowClick=True)        
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create vm using template..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[CREATE VM] MESSAGE : " + msg)
        printLog("[CREATE VM] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'create vm %s'%(self.storage) + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_CREATE_VM_%s'%(self.storage.upper()), result, msg)

    def copyTemplateDisk(self):        
        printLog(printSquare('Copy template disk'))
        try:
            result = FAIL
            msg = ''
            # 컴퓨팅 - 스토리지
            printLog("[COPY TEMPLATE DISK] Storage - Disks")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)
            time.sleep(0.5)
            self.webDriver.explicitlyWait(10, By.ID, 'MenuView_disksAnchor')
            self.webDriver.findElement('id','MenuView_disksAnchor',True)
            time.sleep(1)
            
            # 생성된 템플릿 디스크 선택
            printLog("[COPY TEMPLATE DISK] Wait until disk's status will be OK")
            # self.webDriver.tableSearch(self._templateName + '_vm_Thin_disk', 0, rowClick=True)    
            while True:
                time.sleep(1)
                tableValueList = self.webDriver.tableSearch(self._templateName + '_vm_Thin_disk', 0, False, False,returnValueList=True)
                if '잠김' in tableValueList[11] or 'Locked' in tableValueList[11]:
                    printLog("[COPY TEMPLATE DISK] Disk's status is still locked ...")
                    continue
                elif 'OK' in tableValueList[11]:
                    break
            
            # 복사 클릭
            printLog("[COPY TEMPLATE DISK] Copy template disk")
            self.webDriver.tableSearch(self._templateName + '_vm_Thin_disk', 0, rowClick=True)
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Copy')
            self.webDriver.findElement('id', 'ActionPanelView_Copy', True)
            time.sleep(1)

            # 별칭 변경
            printLog("[COPY TEMPLATE DISK] Change copy disk's name")
            self.webDriver.findElement('css_selector', 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div > div.GHYIDY4CMRB > div > div > div:nth-child(2) > div > div > input')            
            self.webDriver.clear()
            self.webDriver.sendKeys(self._diskName + '_copy')

            self.webDriver.findElement('css_selector', 'body > div.popup-content.ui-draggable > div > div > div > div.modal-footer.wizard-pf-footer.footerPosition > div.GHYIDY4CMOB > div:nth-child(2) > button', True)
            time.sleep(1)

            
            # 디스크가 추가되고 잠금상태에서 OK가 되면 성공
            printLog("[COPY TEMPLATE DISK] Check if created")
            printLog("[COPY TEMPLATE DISK] Wait until changed copy disk was created")
            while True:
                tableValueList = self.webDriver.tableSearch(self._diskName + '_copy', 0, False, False, returnValueList=True)    
                if '잠김' in tableValueList[11] or 'Locked' in tableValueList[11]:
                    result = FAIL
                    msg = 'Failed copy template'
                    printLog("[COPY TEMPLATE DISK] Disk's status is still locked ...")
                    continue
                if 'OK' in tableValueList[11]:
                    result = PASS
                    msg = ''
                    break
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[COPY TEMPLATE DISK] MESSAGE : " + msg)
        printLog("[COPY TEMPLATE DISK] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'copy disk' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_COPY_DISK', result, msg)

    def removeVM(self):
        # 성공 후 삭제 필요
        # 다른 테스트에 사용되기 떄문
        # 컴퓨팅 - 가상머신
        msg = ''
        try:
            printLog("[REMOVE VM] Compute - Virtual Machines")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_vmsAnchor',True)
            time.sleep(2)
            self._templateVMname = self._templateName + '_vm_%s'%self.storage
            while True:
                tdLst = []
                time.sleep(1)
                print(self._templateVMname)                
                table = self.webDriver.getDriver().find_element_by_css_selector('tbody')
                self.webDriver.explicitlyWait(30, By.TAG_NAME, 'tr')
                for tr in table.find_elements_by_tag_name("tr"):          
                    td = tr.find_elements_by_tag_name("td")                      
                    if self._templateVMname == td[2].text:                
                        printLog('[TABLE SEARCH] Find : ' + str(td[2].text))
                        for i in range(len(td)):
                            tdLst.append(td[i].text)
                if tdLst != [] and ('이미지 잠김' in tdLst[13] or 'Image Locked' in tdLst[13]):
                    msg = 'Failed remove VM'
                    printLog("[REMOVE VM] VM's status is still locked ...")
                    continue
                if tdLst != [] and 'Down' in tdLst[13]:
                    printLog("[REMOVE VM] VM's status is down")
                    break

            printLog("[REMOVE VM] Remove vm")
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right', True)                
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Remove')
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(1)    

        except Exception as e:
            msg = str(e).replace("\n",'')
            printLog("[REMOVE VM] MESSAGE : " + msg)       

    def remove(self):
        printLog(printSquare('Remove Template'))
        try:
            result = FAIL
            msg = ''
            # 템플릿 탭
            self.setup()

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(1)
            self.webDriver.tableSearch(self._templateName, 1, rowClick=True)    

            # 편집 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(2)
            
            
            printLog("[REMOVE TEMPLATE] Check if removed")
            while True:
                try:
                    tableValueList = self.webDriver.tableSearch(self._templateName, 1, False, False, returnValueList = True)        
                    if '잠김' in tableValueList[5] or 'Locked' in tableValueList[5]:
                        printLog("[REMOVE TEMPLATE] Template's status is still locked ...")
                        result = FAIL
                        msg = "Failed to remove new template..."
                except:
                    printLog("[REMOVE TEMPLATE] Template removed")
                    result = PASS
                    msg = ''
                    break

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[REMOVE TEMPLATE] MESSAGE : " + msg)
        printLog("[REMOVE TEMPLATE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'remove' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_REMOVE', result, msg)
