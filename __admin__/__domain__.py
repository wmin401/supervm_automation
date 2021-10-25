from __common__.__parameter__ import *
import time

class admin_domain:
    def __init__(self):
        print("* 도메인 추가 테스트 시작")
        self._domainResult = []
        
    def create(self, webDriver):
        print('1) domain 생성 취소')
        
        try:
            # 스토리지
            webDriver.implicitlyWait(10)
            _storageBtn = webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            webDriver.implicitlyWait(10)
            _domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)

            # 새로 만들기
            time.sleep(1)
            webDriver.implicitlyWait(10)
            _newBtn = webDriver.findElement('id','ActionPanelView_NewDomain',True)
            
            # 취소 버튼
            webDriver.implicitlyWait(10)
            _cancelBtn = webDriver.findElement('css_selector','#StoragePopupView_Cancel > button',True)

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._domainResult.append(['domain;create&cancel;' + result + ';' + msg])