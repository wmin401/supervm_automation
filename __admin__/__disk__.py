from __common__.__parameter__ import *
import time

class admin_disk:
    def __init__(self):
        print("* 디스크추가 테스트 시작")
        self._diskResult = []
        
    def create(self, webDriver):
        print('1) disk 생성 취소')
        
        try:
            # 스토리지
            webDriver.waitUntilFindElement(10)
            _storageBtn = webDriver.findElement('id','MenuView_storageTab',True)

            # 디스크
            webDriver.waitUntilFindElement(10)
            _diskBtn = webDriver.findElement('id','MenuView_disksAnchor',True)

            # 새로 만들기
            time.sleep(1)
            webDriver.waitUntilFindElement(10)
            _newBtn = webDriver.findElement('id','ActionPanelView_New',True)
            
            # 취소 버튼
            webDriver.waitUntilFindElement(10)
            _cancelBtn = webDriver.findElement('id','VmDiskPopupView_Cancel',True)

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._diskResult.append(['disk;create&cancel;' + result + ';' + msg])