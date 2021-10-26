from __common__.__parameter__ import *
from selenium.webdriver.common.by import By


class admin_host:
    def __init__(self, webDriver):
        print("* 호스트 테스트 시작")
        self._hostResult = []
        self._hostName = 'supervm41.tmax.dom'
        self._hostIP = 'supervm41.tmax.dom'
        self._hostPW = 'asdf'
        self.webDriver = webDriver
        
    def create(self):
        print('1) 호스트 생성 취소')
        
        try:
            # 컴퓨팅
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 호스트
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_hostsAnchor',True)

            # 새로 만들기
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_New',True)

            # 이름 입력
            self.webDriver.findElement('id','HostPopupView_name',True)
            self.webDriver.sendKey(self._hostName)

            # IP 입력
            self.webDriver.findElement('id','HostPopupView_host',True)
            self.webDriver.sendKey(self._hostIP)

            # PW 입력
            self.webDriver.findElement('id','HostPopupView_userPassword',True)
            self.webDriver.sendKey(self._hostPW)

            # OK 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#HostPopupView_OnSaveFalse > button',True)
            
            '''
            # 취소 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','HostPopupView_Cancel',True)
            '''

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._hostResult.append(['host;create&cancel;' + result + ';' + msg])