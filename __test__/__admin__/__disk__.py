from __common__.__parameter__ import *
import time

class admin_disk:
    def __init__(self):
        print("* 디스크 추가 테스트 시작")
        self._diskResult = []
        
    def create(self, webDriver):
        print('1) disk 생성 취소')
        
        try:
            # 스토리지
            webDriver.implicitlyWait(10)
            _storageBtn = webDriver.findElement('id','MenuView_storageTab',True)

            # 디스크
            webDriver.implicitlyWait(10)
            _diskBtn = webDriver.findElement('id','MenuView_disksAnchor',True)
            '''
            # 새로 만들기                  
            time.sleep(1)
            webDriver.implicitlyWait(10)
            _newBtn = webDriver.findElement('id','ActionPanelView_New',True)

            # 새로 만들기 취소 버튼
            webDriver.implicitlyWait(10)
            _cancelBtn = webDriver.findElement('id','VmDiskPopupView_Cancel',True)
            '''

            # 업로드
            time.sleep(1)
            webDriver.implicitlyWait(10)
            _uploadBtn = webDriver.findElement('id','ActionPanelView____',True)
            _startBtn = webDriver.findElement('css_selector','#ActionPanelView____ > ul > li:nth-child(1) > a',True)
            _connetctestBtn = webDriver.findElement('css_selector','body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.GHYIDY4CA4B > button',True)
            _uploadcancelBtn = webDriver.findElement('id','UploadImagePopupView_Cancel',True)
            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._diskResult.append(['disk' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])