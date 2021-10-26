from __common__.__parameter__ import *
from selenium.webdriver.common.by import By
import time

class admin_cluster:
    def __init__(self, webDriver):
        print("* 클러스터 테스트 시작")
        self._clusterResult = []
        self._clusterName = 'auto_name'
        self.webDriver = webDriver
            
    def create(self):
        print('1) 클러스터 생성')
        
        try:
            # 컴퓨팅
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 호스트
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_clustersAnchor',True)

            # 새로 만들기
            self.webDriver.implicitlyWait(10)
            self.webDriver.explicitlyWait(10, By.ID, 'ClusterPopupView_nameEditor')
            self.webDriver.findElement('id','ActionPanelView_New',True)

            # 이름 입력
            #self.webDriver.implicitlyWait(30)
            self.webDriver.explicitlyWait(10, By.ID, 'ClusterPopupView_nameEditor')
            self.webDriver.findElement('id','ClusterPopupView_nameEditor',True)
            self.webDriver.sendKey(self._clusterName)    
            
            # 설명 입력
            self.webDriver.implicitlyWait(40)
            self.webDriver.findElement('id','ClusterPopupView_descriptionEditor',True)
            self.webDriver.sendKey('auto_description')    

            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_OnSave',True)
            
            # 나중에 설정 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','GuidePopupView_Cancel',True)
            
            # table 내부 전부 검색해서 입력한 이름이 있을경우 PASS
            _createCheck = self.webDriver.tableSearch(self._clusterName)
            
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new cluster..."


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'create' + DELIM + result + DELIM + msg])

    def remove(self):
        try:            
            # table 내부에 생성한 클러스터의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._clusterName, True)
            time.sleep(1)

            # 우측 추가 옵션 버튼 클릭
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button', True)
            
            # 삭제 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)
            
            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)
            
            # table 내부 전부 검색해서 입력한 이름이 있을경우 FAIL
            _removeCheck = self.webDriver.tableSearch(self._clusterName)
                
            if _removeCheck == True:
                result = FAIL
                msg = 'Failed to remove cluster'
            else:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'remove' + DELIM + result + DELIM + msg])
