from __common__.__parameter__ import *
import time

class admin_cluster:
    def __init__(self):
        print("* 클러스터 테스트 시작")
        self._clusterResult = []
        
    def create(self, webDriver):
        print('1) 클러스터 생성 취소')
        
        try:
            # 컴퓨팅
            webDriver.waitUntilFindElement(10)
            _computeBtn = webDriver.findElement('id','compute',True)

            # 호스트
            webDriver.waitUntilFindElement(10)
            _clusterBtn = webDriver.findElement('id','MenuView_clustersAnchor',True)

            # 새로 만들기
            time.sleep(1)
            webDriver.waitUntilFindElement(10)
            _newBtn = webDriver.findElement('id','ActionPanelView_New',True)
            
            # 취소 버튼
            webDriver.waitUntilFindElement(10)
            _cancelBtn = webDriver.findElement('id','ClusterPopupView_Cancel',True)

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            print("* MESSAGE : " + msg)

        print("* RESULT : " + result)
        self._clusterResult.append(['cluster;create&cancel;' + result + ';' + msg])