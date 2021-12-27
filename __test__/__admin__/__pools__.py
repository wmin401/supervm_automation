import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import *

from selenium.webdriver.common.by import By

from __test__.__admin__ import *

'''
    작성자 : CQA2 김정현
'''

class admin_pools:
    def __init__(self, webDriver):
        self._poolsResult = []
        self.webDriver = webDriver
        self._templateName = 'auto_sample_'+ randomString()
        self.tl = testlink()
        # class import 부분이 안되고 있음
        # _admin_template_instance = admin_template(webDriver)

    def test(self):
        # _admin_template_instance.setup()
        # _admin_template_instance.create()
        self.template_setup() # 템플릿 메뉴 접근 확인
        self.template_create() # 템플릿 생성
        time.sleep(0.3)

    def template_setup(self):
        # 템플릿 메뉴 접근

        # 컴퓨팅 클릭
        printLog("[TEMPLATE_CREATE] Compute - Template ")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute',True)

        # 템플릿 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_templatesAnchor')
        self.webDriver.findElement('id','MenuView_templatesAnchor',True)

        time.sleep(2)

    def template_create(self):
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
            self.template_setup()

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
        self._poolsResult.append(['template' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('TEMPLATE_CREATE', result, msg)
