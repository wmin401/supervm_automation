from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By


class admin_qos:
    def __init__(self, webDriver):
        self._qosResult = []
        self.webDriver = webDriver
        self._QoSName = 'auto_QoS'
        self._QoSDescription = 'automation QoS Test'
          
    def test(self):
        self.setup()
        # 스토리지 QoS
        self.frame('create', 0, 'storage', self.storageCreate)
        time.sleep(0.3)
        self.frame('remove', 0, 'storage', lambda: self.remove(0))
        # 가상머신 네트워크 QoS
        self.frame('create', 1, 'vm network', self.vmNetworkCreate)
        time.sleep(0.3)
        self.frame('remove', 1, 'vm network', lambda: self.remove(1))
        # 호스트 네트워크 QoS
        self.frame('create', 2, 'host network', self.hostNetworkCreate)
        time.sleep(0.3)
        self.frame('remove', 2, 'host network', lambda: self.remove(2))
        # CPU QoS
        self.frame('create', 3, 'CPU', self.CPUCreate)
        time.sleep(0.3)
        self.frame('remove', 3, 'CPU', lambda: self.remove(3))
  
    def setup(self):        
        try:
            # 컴퓨팅 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)            
            # Data Center 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_dataCentersAnchor',True)            
            # Default 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'MainDataCenterView_table_content_col2_row0')
            self.webDriver.findElement('id','MainDataCenterView_table_content_col2_row0', True) # Data Center 가장 위에 것으로 테스트
            # QoS 탭 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(5) > a')
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(5) > a',True)            
            # 새로 만들기 변수에 저장(0~3)
            self.webDriver.implicitlyWait(10)
            self.newBtns = self.webDriver.findElement('id_all','DetailActionPanelView_New') # 새로 만들기 버튼 리스트
            self.editBtns = self.webDriver.findElement('id_all','DetailActionPanelView_Edit') # 편집 버튼 리스트            
            self.removeBtns = self.webDriver.findElement('id_all','DetailActionPanelView_Remove') # 삭제 버튼 리스트            
        except Exception as e:
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)

    def done(self, action, tableIndex, menu):
        # 작업 완료 확인
        # 생성 또는 삭제 확인
        self.webDriver.implicitlyWait(10)
        _DoneCheck = self.webDriver.tableSearchAll(tableIndex, self._QoSName, 0)
        # 생성 확인
        if action == 'create':
            if _DoneCheck == True: # 검색하는 내용이 존재하면 생성된 것이니 PASS
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'failed to create '+ menu + ' QoS'
        # 삭제 확인
        elif action == 'remove':
            if _DoneCheck == True: # 검색하는 내용이 존재하면 삭제가 안된것이니 FAIL
                result = FAIL
                msg = 'failed to remove '+ menu + ' QoS'
            else:
                result = PASS
                msg = ''    
        return result, msg

    def frame(self, action, tableIndex, menu, testCase): ## 공통된 함수 하나로 합치기
        printLog('** %s %s QoS'%(action.capitalize(), menu))  
        try:
            # 테스트 실행
            testCase()
            # 작업 확인
            result, msg = self.done(action, tableIndex, menu)
        except Exception as e:
            # 예외처리
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        # 결과 저장
        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + '%s %s'%(menu, action) + DELIM + result + DELIM + msg])

    def storageCreate(self):
        # 새로 만들기 클릭
        self.newBtns[0].click() # 
        # QoS 이름 입력
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id', 'QosPopupView_nameEditor')
        self.webDriver.sendKeys(self._QoSName)
        # 설명 입력
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id', 'QosPopupView_descriptionEditor')
        self.webDriver.sendKeys(self._QoSDescription)
        # OK 버튼
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id', 'QosPopupView_OnSave', True)

    def vmNetworkCreate(self):
        # 새로 만들기 클릭
        self.newBtns[1].click() #  
        # QoS 이름 입력
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id', 'NetworkQoSPopupView_nameEditor')
        self.webDriver.sendKeys(self._QoSName)
        # OK 클릭
        self.webDriver.findElement('id', 'NetworkQoSPopupView_OnSave', True)

    def hostNetworkCreate(self):
        # 새로 만들기 클릭
        self.newBtns[2].click() # 
        # QoS 이름 입력
        self.webDriver.findElement('id','QosPopupView_nameEditor')
        self.webDriver.sendKeys(self._QoSName)
        # 설명 입력
        self.webDriver.findElement('id','QosPopupView_descriptionEditor')            
        self.webDriver.sendKeys(self._QoSDescription)
        # 가중 공유 입력 
        self.webDriver.findElement('id','HostNetworkQosWidget_outAverageLinkshare')
        self.webDriver.sendKeys(5)
        # 속도 제한 입력 
        self.webDriver.findElement('id','HostNetworkQosWidget_outAverageUpperlimit')
        self.webDriver.sendKeys(10)
        # 커밋 속도 입력 
        self.webDriver.findElement('id','HostNetworkQosWidget_outAverageRealtime')
        self.webDriver.sendKeys(10)
        # OK 버튼            
        self.webDriver.findElement('id', 'QosPopupView_OnSave', True)

    def CPUCreate(self):
        # 새로 만들기 클릭
        self.newBtns[3].click() # 
        # QoS 이름 입력
        self.webDriver.findElement('id','QosPopupView_nameEditor')
        self.webDriver.sendKeys(self._QoSName)
        # 설명 입력
        self.webDriver.findElement('id','QosPopupView_descriptionEditor')            
        self.webDriver.sendKeys(self._QoSDescription)
        # 제한 입력
        self.webDriver.findElement('id','CpuQosWidget_cpuLimitEditor')
        self.webDriver.sendKeys(10)
        # OK 버튼
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id', 'QosPopupView_OnSave', True)

    def remove(self, tableIndex):
        # 생성된 QoS 검색 및 선택
        self.webDriver.tableSearchAll(tableIndex, self._QoSName, 0, True)
        # 삭제 버튼 클릭
        self.removeBtns[tableIndex].click()
        # OK 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id', 'RemoveConfirmationPopupView_onRemove', True)