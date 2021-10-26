from __common__.__parameter__ import *


class admin_host:
    def __init__(self):
        print("* 호스트 테스트 시작")
        self._hostResult = []
        
    def create(self, webDriver):
        print('1) 호스트 생성 취소')
        
        try:
            # 컴퓨팅
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','compute',True)

            # 호스트
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','MenuView_hostsAnchor',True)

            # 새로 만들기
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','ActionPanelView_New',True)
            
            # 취소 버튼
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','HostPopupView_Cancel',True)

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._hostResult.append(['host;create&cancel;' + result + ';' + msg])