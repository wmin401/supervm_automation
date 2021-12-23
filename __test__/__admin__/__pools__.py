import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import *

from selenium.webdriver.common.by import By

from __test__.__admin__.__template__ import *

'''
    작성자 : CQA2 김정현
'''

class admin_pools:
    def __init__(self, webDriver):
        self._poolsResult = []
        self.webDriver = webDriver
        # self._templateName = 'auto_sample_'+ randomString()
        self.tl = testlink()
    def sample_test_case1(self):

        try:
            result = PASS
            msg = ''
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[SAMPLE TEST] MESSAGE : " + msg)

        self._admin_template = admin_template(webDriver)

    def test(self):
        self._admin_template.setup()
        self._admin_template.create()
        time.sleep(0.3)
        # time.sleep(0.3)
        # self.update()
        # time.sleep(0.3)
        # self.createVM(storage='Thin')
        # time.sleep(0.3)

    def template_setup(self):
        # 템플릿 생성
        printLog("[TEMPLATE_CREATE] Compute - Template ")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute',True)

        # 템플릿 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_templatesAnchor')
        self.webDriver.findElement('id','MenuView_templatesAnchor',True)

        time.sleep(2)

