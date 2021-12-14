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
        self.create()
        time.sleep(0.3)
        self.update()
        time.sleep(0.3)
        self.remove()

    def setup(self):
        # 컴퓨팅 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute',True)

        # 템플릿 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','MenuView_templatesAnchor',True)
        
        time.sleep(2)

    def create(self):
        printLog('- Create Template')        
        try:
            result = FAIL
            msg = ''
            # 중지된 가상머신이 있어야한다.
            # 컴퓨팅 클릭
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
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_NewTemplate',True)

            # 템플릿 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmMakeTemplatePopupWidget_name')
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_name')
            self.webDriver.sendKeys(self._templateName)

            # 가상 머신 권한 복사 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmMakeTemplatePopupWidget_copyVmPermissions', True)            

            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','VmMakeTemplatePopupView_OnNewTemplate', True)
            time.sleep(3)
            # 템플릿 탭
            self.setup()

            # table 내부 전부 검색해서 입력한 이름이 있을경우 PASS
            _createCheck = self.webDriver.tableSearch(self._templateName, 1) # 템플릿 테이블에 숨겨진 열(0)이 하나 있어서 1부터 시작
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new template..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)
        printLog("* RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_CREATE', result, msg)

    def update(self):
        printLog('- Update Template')        
        try:
            result = FAIL
            msg = ''
            # 템플릿 탭
            self.setup()

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._templateName, 1, rowClick=True)    

            # 편집 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)
            
            # 설명에 임의의 문자열 입력 후 저장
            self.webDriver.explicitlyWait(10, By.ID, 'TemplateEditPopupWidget_description')
            self.webDriver.findElement('id', 'TemplateEditPopupWidget_description', True)
            des = randomString()
            self.webDriver.sendKeys(des)
            self.webDriver.findElement('id', 'TemplateEditPopupView_OnSave', True)
            time.sleep(1)

            # 설명에 추가되면 성공
            _updateCheck = self.webDriver.tableSearch(des, 9)        
            if _updateCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to update new template..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)
        printLog("* RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'update' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_UPDATE', result, msg)

    def remove(self):
        printLog('- Remove Template')        
        try:
            result = FAIL
            msg = ''
            # 템플릿 탭
            self.setup()

            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._templateName, 1, rowClick=True)    

            # 편집 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(0.5)
            
            # 설명에 추가되면 성공
            _removeCheck = self.webDriver.tableSearch(self._templateName, 1)        
            if _removeCheck == False:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to remove new template..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)
        printLog("* RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'remove' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_REMOVE', result, msg)