#-*- coding: utf-8 -*-

from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

class admin_vm3:
    def __init__(self, webDriver):
        self._vm3Result = [] # lowerCamelCase 로
        self.webDriver = webDriver
        self._vm3Name = 'auto_vm3_'+randomString() # 랜덤 이름
        self.tl = testlink()
          
    def test(self):
        self.create_restapi()


    def create_restapi(self):
        try:
            result = PASS
            msg = ''
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REST API VM CREATE] MESSAGE : " + msg)

        # 결과 저장
        printLog("[VM REST API VM CREATE] RESULT : " + result)
        self._vm3Result.append(['VM' + DELIM + 'rest api vm create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('VM_REST_API_VM_CREATE',result, msg)