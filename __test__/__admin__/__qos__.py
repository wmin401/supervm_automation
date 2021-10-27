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

    def storageCreate(self):
        printLog('1) Create QoS Storage')
        self.newBtns[0].click() # 
        time.sleep(1)
        self.webDriver.findElement('id','QosPopupView_Cancel', True)

        #QosPopupView_Cancel > button

    def storageRemove(self):
        printLog('2) Remove QoS Storage')        
        self.removeBtns[0].click() # 

    def VMNetwrkCreate(self):
        printLog('3) Create QoS VM Network')
        self.newBtns[1].click() # 
        time.sleep(1)
        self.webDriver.findElement('id','NetworkQoSPopupView_Cancel', True)

    def VMNetwrkRemove(self):
        printLog('4) Remove QoS VM Network')
        self.removeBtns[1].click()

    def HostNetworkCreate(self):
        printLog('5) Create QoS Host Network')
        self.newBtns[2].click() # 
        time.sleep(1)
        self.webDriver.findElement('id','QosPopupView_Cancel', True)

    def HostNetworkRemove(self):
        printLog('6) Remove QoS Host Network')
        self.removeBtns[2].click()

    def CPUCreate(self):
        printLog('7) Create QoS CPU')        
        self.newBtns[3].click() # 
        time.sleep(1)
        self.webDriver.findElement('id','QosPopupView_Cancel', True)

    def CPURemove(self):
        printLog('8) Remove QoS CPU')
        self.removeBtns[3].click()