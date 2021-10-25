from __common__.__parameter__ import *


class admin_host:
    def __init__(self):
        print("* 호스트 테스트 시작")
        
    def create(self, webDriver):
        print('1) 호스트 생성 취소')
        
        try:
            # 컴퓨팅
            webDriver.waitUntilFindElement(10)
            _computeBtn = webDriver.findElement('id','compute',True)

            # 호스트
            webDriver.waitUntilFindElement(10)
            _hostBtn = webDriver.findElement('id','MenuView_hostsAnchor',True)

            # 새로 만들기
            webDriver.waitUntilFindElement(10)
            _newBtn = webDriver.findElement('id','ActionPanelView_New',True)
            
            # 취소 버튼
            webDriver.waitUntilFindElement(10)
            _cancelBtn = webDriver.findElement('id','HostPopupView_Cancel',True)

            result = PASS
        except Exception as e:
            result = FAIL
            msg = e
            print("* MESSAGE : " + str(e).replace("\n",''))

        print("* RESULT : " + result)