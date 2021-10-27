from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By


class admin_qos:
    def __init__(self, webDriver):
        self._qosResult = []
        self.webDriver = webDriver
            
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
            self.removeBtns = self.webDriver.findElement('id_all','DetailActionPanelView_New') # 삭제 버튼 리스트
            
        except Exception as e:
            msg = str(e).replace("\n",'')
            printLog("* MESSAGE : " + msg)

    def scenario1(self):
        self.storageCreate()
        self.storageRemove()
        self.VMNetwrkCreate()
        self.VMNetwrkRemove()
        self.HostNetworkCreate()
        self.HostNetworkRemove()
        self.CPUCreate()
        self.CPURemove()

    def storageCreate(self):
        printLog('1) Create QoS Storage')
        try:        
            self.newBtns[0].click() # 

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'storage create' + DELIM + result + DELIM + msg])

        #QosPopupView_Cancel > button

    def storageRemove(self):
        printLog('2) Remove QoS Storage')        
        try:
            self.removeBtns[0].click() # 

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'storage remove' + DELIM + result + DELIM + msg])

    def VMNetwrkCreate(self):
        printLog('3) Create QoS VM Network')
        try:
            self.newBtns[1].click() #           

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'vm network create' + DELIM + result + DELIM + msg])

    def VMNetwrkRemove(self):
        printLog('4) Remove QoS VM Network')
        try:
            self.removeBtns[1].click()         

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'vm network remove' + DELIM + result + DELIM + msg])

    def HostNetworkCreate(self):
        printLog('5) Create QoS Host Network')
        try:
            self.newBtns[2].click() # 

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'host network create' + DELIM + result + DELIM + msg])

    def HostNetworkRemove(self):
        printLog('6) Remove QoS Host Network')
        try:
            self.removeBtns[2].click()            

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
            self.removeBtns[3].click()           

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._qosResult.append(['QoS' + DELIM + 'cpu remove' + DELIM + result + DELIM + msg])
