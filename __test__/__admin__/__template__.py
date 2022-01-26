import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import testlink

from selenium.webdriver.common.by import By

from __test__.__admin__.__vm__ import *


class admin_template:
    def __init__(self, webDriver):
        self._templateResult = []
        self._templateName = 'auto_template_' + randomString()
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

        self.vm.remove()

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
        # 디스크가 있는 가상머신만 가능
        # 가상머신 생성하는 코드를 추가해야하나?

        printLog(printSquare('Create Template'))
        try:
            result = FAIL
            msg = ''
            # 중지된 가상머신이 있어야한다.
            # 컴퓨팅 클릭
            
            # 가상머신 생성
            self.vm = admin_vm(self.webDriver)
            self.vm.create()
            
            # 디스크 상태 확인
            self.vm.diskStatus()

            printLog("[CREATE TEMPLATE] Compute - Virtual Machines ")
            self.webDriver.findElement('id','compute',True)
            time.sleep(0.3)
            # 가상머신 클릭
            self.webDriver.findElement('id','MenuView_vmsAnchor', True)
            self.webDriver.tableSearch(self.vm._vmName, 2, rowClick=True)
            time.sleep(0.3)
            # 추가 옵션 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','.btn-group:nth-child(11) > .btn',True)
            
            # 템플릿 생성 클릭
            printLog("[CREATE TEMPLATE] Create template")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_NewTemplate',True)

            time.sleep(1)

            # 템플릿 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmMakeTemplatePopupWidget_name')
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_name')
            self.webDriver.sendKeys(self._templateName)
            printLog("[CREATE TEMPLATE] Template name : %s"%self._templateName)

            # 템플릿 디스크 별칭 변경
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_disksAllocation_disk0_diskAlias', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._templateName + '_Disk1')


            # 가상 머신 권한 복사 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_copyVmPermissions', True)            

            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmMakeTemplatePopupView_OnNewTemplate > button', True)
            time.sleep(3)
            # 템플릿 탭
            self.setup()

            printLog("[CREATE TEMPLATE] Check if created")
            printLog("[CREATE TEMPLATE] Wait until status will be OK")
       
            result, msg = self.webDriver.isChangedStatus(self._templateName, 1, 5, ['잠김', 'Locked'], ['OK'], 60)

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
            time.sleep(1)
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
            self.webDriver.findElement('css_selector', '#TemplateEditPopupView_OnSaveConfirm > button', True)
            time.sleep(2)

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
            if self.storage == 'Thin':
                # 씬 프로비저닝 클릭
                self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_provisioningThin')
                self.webDriver.findElement('id', 'VmPopupWidget_provisioningThin', True)
            elif self.storage == 'Copy':
                # 복제 클릭
                self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_provisioningClone')
                self.webDriver.findElement('id', 'VmPopupWidget_provisioningClone', True)
            
            # 디스크 별칭 변경
            self.webDriver.findElement('id', 'VmPopupWidget_disksAllocation_disk0_diskAlias', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._templateName + '_vm_%s_Disk1'%self.storage)
            
            # OK 클릭
            self.webDriver.findElement('css_selector', '#VmPopupView_OnSaveVm > button', True)
            time.sleep(5)
            
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
        # 가상머신 생성후 해당 가상머신의 디스크를 지우는 방식으로 변경    
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
            cnt = 0
            while True:
                time.sleep(1)
                tableValueList = self.webDriver.tableSearch(self._templateName + '_vm_%s_Disk1'%self.storage, 0, False, False,returnValueList=True)
                if '잠김' in tableValueList[10] or 'Locked' in tableValueList[10]:
                    if cnt == 0:
                        printLog("[COPY TEMPLATE DISK] Disk's status is still locked ...")
                        cnt = 1
                    continue
                elif 'OK' in tableValueList[10]:
                    break
            
            # 복사 클릭
            printLog("[COPY TEMPLATE DISK] Copy template disk")
            self.webDriver.tableSearch(self._templateName + '_vm_%s_Disk1'%self.storage, 0, rowClick=True)
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Copy')
            self.webDriver.findElement('id', 'ActionPanelView_Copy', True)
            time.sleep(2)

            # 별칭 변경
            self._templateCopyDisk = 'copy_' + self._templateName + '_vm_%s_Disk1'%self.storage
            printLog("[COPY TEMPLATE DISK] Change copy disk's name")
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div/div/div[3]/div/div/div[2]/div[1]/div/input')
            self.webDriver.clear()
            self.webDriver.sendKeys(self._templateCopyDisk)

            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button', True)
            printLog("[COPY TEMPLATE DISK] Wait 30 seconds until disk is OK")
            time.sleep(30)
           
            # 디스크가 추가되고 잠금상태에서 OK가 되면 성공
            printLog("[COPY TEMPLATE DISK] Check if created")
            printLog("[COPY TEMPLATE DISK] Wait until changed copy disk was created")

            result, msg = self.webDriver.isChangedStatus(self._templateCopyDisk, 0, 10, ['잠김', 'Locked'], ['OK'], 180)

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
            st = time.time()
            cnt = 0
            while True:
                tdLst = []
                time.sleep(1)
                print(self._templateVMname)        
                try:        
                    table = self.webDriver.getDriver().find_element_by_css_selector('tbody')
                    self.webDriver.explicitlyWait(30, By.TAG_NAME, 'tr')
                    for tr in table.find_elements_by_tag_name("tr"):          
                        td = tr.find_elements_by_tag_name("td")                      
                        if self._templateVMname == td[2].text:                
                            if cnt == 0:
                                printLog('[TABLE SEARCH] Find : ' + str(td[2].text))
                                cnt = 1
                            for i in range(len(td)):
                                try:
                                    tdLst.append(td[i].text)
                                except:
                                    tdLst.append('')
                    if tdLst != [] and ('이미지 잠김' in tdLst[13] or 'Image Locked' in tdLst[13]):
                        printLog("[REMOVE VM] VM's status is still locked ...")
                        continue
                    if tdLst != [] and 'Down' in tdLst[13]:
                        printLog("[REMOVE VM] VM's status is down")
                        break
                    if time.time() - st > 120:
                        printLog("[REMOVE VM] Timeout ...")
                        break
                except:
                    continue

            printLog("[REMOVE VM] Remove vm")
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Remove')
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(1)    

        except Exception as e:
            msg = str(e).replace("\n",'')
            printLog("[REMOVE VM] MESSAGE : " + msg)       

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
            try:
                self.webDriver.findElement('link_text', '권한', True)
            except:
                self.webDriver.findElement('link_text', 'role', True)
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
            self.webDriver.findElement('css_selector', '#PermissionsPopupView_OnAdd > button', True)
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
            try:
                self.webDriver.findElement('link_text', '권한', True)
            except:
                self.webDriver.findElement('link_text', 'role', True)
            # 생성한 권한 찾아서 클릭
            self.webDriver.tableSearch(self.role, 4, rowClick=True)
            # 제거 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)
            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('css_selector', '#RemoveConfirmationPopupView_OnRemove > button', True)
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
            self.webDriver.findElement('css_selector', '#RemoveConfirmationPopupView_OnRemove > button', True)
            time.sleep(7)
            
            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[REMOVE TEMPLATE] MESSAGE : " + msg)
        printLog("[REMOVE TEMPLATE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'remove' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_REMOVE', result, msg)
