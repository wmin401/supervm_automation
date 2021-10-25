from __common__.__parameter__ import *
from selenium.webdriver.common.by import By
import time

class admin_cluster:
    def __init__(self):
        print("* 클러스터 테스트 시작")
        self._clusterResult = []
        
    def create(self, webDriver):
        print('1) 클러스터 생성')
        
        try:
            # 컴퓨팅
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','compute',True)

            # 호스트
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','MenuView_clustersAnchor',True)

            # 새로 만들기
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','ActionPanelView_New',True)

            # 이름 입력
            #webDriver.implicitlyWait(30)
            webDriver.explicitlyWait(10, By.ID, 'ClusterPopupView_nameEditor')
            webDriver.findElement('id','ClusterPopupView_nameEditor',True)
            webDriver.sendKey('auto_name')    
            
            # 설명 입력
            webDriver.implicitlyWait(40)
            webDriver.findElement('id','ClusterPopupView_descriptionEditor',True)
            webDriver.sendKey('auto_descrition')    

            # OK 버튼 클릭
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','ClusterPopupView_OnSave',True)
            
            # 나중에 설정 버튼 클릭
            webDriver.implicitlyWait(10)
            webDriver.findElement('id','GuidePopupView_Cancel',True)
            

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._clusterResult.append(['cluster;create;' + result + ';' + msg])