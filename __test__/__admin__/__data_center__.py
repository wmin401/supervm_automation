from __common__.__parameter__ import *
import time

class admin_data_center:
    def __init__(self):
        print("* 데이터 센터 추가 테스트 시작")
        self._data_centerResult = []
        
    def create(self, webDriver):
        print('1) data_center 생성 취소')
        
        try:
            # 스토리지
            webDriver.implicitlyWait(10)
            _storageBtn = webDriver.findElement('id','MenuView_storageTab',True)

            # 데이터 센터
            webDriver.implicitlyWait(10)
            _data_centerBtn = webDriver.findElement('id','MenuView_dataCentersStorageAnchor',True)

            # 새로 만들기
            time.sleep(1)
            webDriver.implicitlyWait(10)
            _newBtn = webDriver.findElement('id','ActionPanelView_New',True)
            
            # 취소 버튼
            webDriver.implicitlyWait(10)
            _cancelBtn = webDriver.findElement('id','DataCenterPopupView_Cancel',True)

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._data_centerResult.append(['data_center' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])