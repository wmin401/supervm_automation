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
            self.webDriver.sendKey('auto_descrition')    

            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_OnSave',True)
            
            # 나중에 설정 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','GuidePopupView_Cancel',True)
            
            
            # tbody내부 전부 검색해서 입력한 이름이 있을경우 PASS
            a = self.webDriver.tableSearch(self._clusterName)
            
            time.sleep(1)

            if a == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Not created"


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._clusterResult.append(['cluster;create;' + result + ';' + msg])

    def remove(self):
        try:
            self.webDriver.tableSearch(self._clusterName, True)
            time.sleep(1)

            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button')
            self.webDriver.click()

            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)
            
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)
            
            a = self.webDriver.tableSearch(self._clusterName)
                
            time.sleep(1)

            if a == True:
                result = FAIL
                msg = 'Not removed'
            else:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._clusterResult.append(['cluster;remove;' + result + ';' + msg])
