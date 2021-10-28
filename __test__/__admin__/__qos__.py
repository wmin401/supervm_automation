from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By


class admin_qos:
    def __init__(self, webDriver):
        self._qosResult = []
        self.webDriver = webDriver
        self._QoSName = 'auto_QoS'
        self._QoSDescription = 'automation QoS Test'
            
    def initialize(self):        
        try:
            # 컴퓨팅
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)
            
            # Data Center
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_dataCentersAnchor',True)
            
            # Default Click
            self.webDriver.explicitlyWait(10, By.ID, 'MainDataCenterView_table_content_col2_row0')
            self.webDriver.findElement('id','MainDataCenterView_table_content_col2_row0', True) # Data Center 가장 위에 것으로 테스트

            # QoS 탭 Click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(5) > a')
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(5) > a',True)
            
            # 새로 만들기 
            self.webDriver.implicitlyWait(10)
            self.newBtns = self.webDriver.findElement('id_all','DetailActionPanelView_New') # 새로 만들기 버튼 리스트
            self.editBtns = self.webDriver.findElement('id_all','DetailActionPanelView_Edit') # 편집 버튼 리스트            
            self.removeBtns = self.webDriver.findElement('id_all','DetailActionPanelView_Remove') # 삭제 버튼 리스트
            
        except Exception as e:
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)

    def ifDone(self, action, tableIndex, menu):
        self.webDriver.implicitlyWait(10)
        _DoneCheck = self.webDriver.tableSearchAll(tableIndex, self._QoSName, 0)

        if action == 'create':
            if _DoneCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'failed to create '+ menu + ' QoS'

        elif action == 'remove':
            if _DoneCheck == True:
                result = FAIL
                msg = 'failed to create '+ menu + ' QoS'
            else:
                result = PASS
                msg = ''
    
        return result, msg

    def scenario1(self):
        self.storageCreate()
        time.sleep(0.3)
        self.storageRemove()
        self.vmNetworkCreate()
        time.sleep(0.3)
        self.vmNetworkRemove()        
        self.hostNetworkCreate()
        time.sleep(0.3)
        self.hostNetworkRemove()
        self.CPUCreate()
        time.sleep(0.3)
        self.CPURemove()

    def storageCreate(self):
        printLog('1) Create Storage QoS')
        try:        
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
            # 생성 확인
            result, msg = self.ifDone('create', 0, 'Storage')

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'storage create' + DELIM + result + DELIM + msg])

    def storageRemove(self):
        printLog('2) Remove Storage QoS')        
        try:          
            # 생성되어있는 QoS 탐색 및 클릭  
            self.webDriver.tableSearchAll(0, self._QoSName, 0, True)
            # 삭제 버튼 클릭
            self.removeBtns[0].click()
            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_onRemove', True)
            # 삭제 확인
            result, msg = self.ifDone('remove', 0, 'Storage')
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'storage remove' + DELIM + result + DELIM + msg])

    def vmNetworkCreate(self):
        printLog('3) Create M Network QoS')
        try:
            # 새로 만들기 클릭
            self.newBtns[1].click() #  
            # QoS 이름 입력
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'NetworkQoSPopupView_nameEditor')
            self.webDriver.sendKeys(self._QoSName)
            # OK 클릭
            self.webDriver.findElement('id', 'NetworkQoSPopupView_OnSave', True)
            # 생성 확인            
            result, msg = self.ifDone('create', 1, 'VM Network')
            
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'vm network create' + DELIM + result + DELIM + msg])

    def vmNetworkRemove(self):
        printLog('4) Remove VM Network QoS')
        try:
            # 생성된 QoS 탐색 및 클릭
            self.webDriver.tableSearchAll(1, self._QoSName, 0, True)
            # 삭제 버튼 클릭
            self.removeBtns[1].click()         
            # OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_onRemove', True)
            # 삭제 확인
            result, msg = self.ifDone('remove', 1, 'VM Network')

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'vm network remove' + DELIM + result + DELIM + msg])

    def hostNetworkCreate(self):
        printLog('5) Create QoS Host Network')
        try:
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
            # 생성 확인
            result, msg = self.ifDone('create', 2, 'Host Network')

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        printLog("* RESULT : " + result)

        self._qosResult.append(['QoS' + DELIM + 'host network create' + DELIM + result + DELIM + msg])

    def hostNetworkRemove(self):
        printLog('6) Remove QoS Host Network')
        try:
            # 생성된 QoS 탐색 및 클릭
            self.webDriver.tableSearchAll(2, self._QoSName, 0, True)
            # 삭제 버튼 클릭
            self.removeBtns[2].click()        
            # OK 클릭
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_onRemove', True)
            # 삭제 확인
            result, msg = self.ifDone('remove', 2, 'Host Network')

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'host network remove' + DELIM + result + DELIM + msg])

    def CPUCreate(self):
        printLog('7) Create QoS CPU')        
        try:
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
            # 생성 확인
            result, msg = self.ifDone('create', 3, 'CPU')

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'cpu create' + DELIM + result + DELIM + msg])

    def CPURemove(self):
        printLog('8) Remove QoS CPU')
        try:
            # 생성된 QoS 탐색 및 클릭
            self.webDriver.tableSearchAll(3, self._QoSName, 0, True)
            # 삭제 클릭
            self.removeBtns[3].click()        
            # OK 클릭
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_onRemove', True)
            # 삭제 확인
            result, msg = self.ifDone('remove', 3, 'CPU')

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'cpu remove' + DELIM + result + DELIM + msg])
