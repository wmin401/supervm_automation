from operator import truediv
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
import time
from __common__.__testlink__ import *

class admin_data_center:
    def __init__(self, webDriver):
        printLog("* 데이터 센터 테스트 시작")
        self._data_centerResult = []
        self._data_centerName = 'TEST'
        self.webDriver = webDriver
        self.domainName = 'nfs-231'
        self.tl = testlink()
        
    def test(self):
        #self.create()
        #self.edit_changeStorageType()
        #self.edit_changeStorageCompatibleVersion()
        #time.sleep(2)
        #self.datacenterForceRemove()
        #self.remove()
        self.datacenterDetachDomain()
        
    def create(self):
        printLog('Create data_center')
        
        try:
            # 컴퓨팅
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 데이터 센터
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_dataCentersAnchor',True)

            # 새로 만들기
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_New',True)

            time.sleep(1)
            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'DataCenterPopupView_nameEditor')
            self.webDriver.findElement('id','DataCenterPopupView_nameEditor',True)
            self.webDriver.sendKeys(self._data_centerName)
            
            '''
            # 호환 버전 4.4로 변경
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_versionEditor',True)
            self.webDriver.findElement('css_selector','#DataCenterPopupView_versionEditor > div > ul > li:nth-child(3)',True)
            '''
            # 새로운 데이터 센터 OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_OnSave',True)

            # 데이터 센터 - 가이드 나중에 설정 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','GuidePopupView_Cancel',True)

            '''
            # 취소 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_Cancel',True)
            '''
            _createCheck = self.webDriver.tableSearch(self._data_centerName,2)
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = 'Failed to create new Data Center...'

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        printLog("* RESULT : " + result)
        self._data_centerResult.append(['data center' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DATA_CENTER_CREATE', result, msg)

    def remove(self):
        printLog('Remove data_center')
        
        try:
            # 컴퓨팅
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 데이터 센터
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_dataCentersAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._data_centerName, 2, True)
            
            time.sleep(1)

            # 삭제 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)

            # 새로운 데이터 센터 OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)

            time.sleep(1)

            _removeCheck = self.webDriver.tableSearch(self._data_centerName,2)
            if _removeCheck == True:
                result = FAIL
                msg = 'Failed to create new Data Center...'
            else:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        printLog("* RESULT : " + result)
        self._data_centerResult.append(['data center' + DELIM + 'remove' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DATA_CENTER_REMOVE', result, msg)

    def edit_changeStorageType(self):
        printLog('Edit type data_center')
        
        try:
            # 컴퓨팅
            time.sleep(2)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 데이터 센터
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_dataCentersAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._data_centerName, 2, True)
            time.sleep(1)

            # 편집 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Edit',True)

            # 스토리지 유형 클릭
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_storagePoolTypeEditor',True)
            self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/ul/li[2]',True)
            
            # 새로운 데이터 센터 OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_OnSave',True)

            '''
            _removeCheck = self.webDriver.tableSearch(self._data_centerName,2)
            if _removeCheck == True:
                result = FAIL
                msg = 'Failed to create new Data Center...'
            else:
                result = PASS
                msg = ''
            '''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        #self.tl.junitBuilder('DATA_CENTER_EDIT_TYPE', result, msg)

    def edit_changeStorageCompatibleVersion(self):
        printLog('Edit version data_center')
        
        try:
            # 컴퓨팅
            time.sleep(2)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute',True)

            # 데이터 센터
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_dataCentersAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._data_centerName, 2, True)
            time.sleep(1)

            # 편집 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Edit',True)

            # 스토리지 유형 클릭
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_versionEditor',True)
            self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[2]/div/div/div/div[4]/div/div[1]/div/div/div/ul/li[2]',True)
            
            # 새로운 데이터 센터 OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DataCenterPopupView_OnSave',True)

            # 데이터 센터의 호환 버전을 변경 OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DefaultConfirmationPopupView_OnSaveInternal',True)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        
        #self.tl.junitBuilder('DATA_CENTER_EDIT_VERSION', result, msg)

    def datacenterForceRemove(self):    
        printLog(printSquare('Datacenter Force Remove'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_dataCentersAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_dataCentersAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._data_centerName,2,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button')
            self.webDriver.findElement('css_selector', 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '강제 제거')
            self.webDriver.findElement('link_text', '강제 제거', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ForceRemoveConfirmationPopupView_latch')
            self.webDriver.findElement('id', 'ForceRemoveConfirmationPopupView_latch', True)

            time.sleep(3)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[DATACENTER FORCE REMOVE] " + msg)

        # 결과 출력
        printLog("[DATACENTER FORCE REMOVE] RESULT : " + result)
        self._data_centerResult.append(['datacenter' + DELIM + 'force remove' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('DATACENTER_FORCE_REMOVE',result, msg)

    def datacenterDetachDomain(self):    
        printLog(printSquare('Datacenter Detach Domain'))
        result = FAIL
        msg = ''

        try:
            # 컴퓨팅 click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # 데이터 센터 click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_dataCentersAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_dataCentersAnchor > .list-group-item-value', True)

            time.sleep(2)

            # 데이터 센터 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._data_centerName,2,False,True)

            time.sleep(2)

            # 분리할 스토리지 도메인 선택
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self.domainName,2,True)

            # 유지보수 click
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Maintenance')
            self.webDriver.findElement('id', 'DetailActionPanelView_Maintenance', True)

            # OK click
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnMaintenance')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnMaintenance', True)

            time.sleep(40)

            # 상단 데이터 센터 click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(1) > div > div.detailMainBreadcrumbs > div > ol > li:nth-child(2) > a')
            self.webDriver.findElement('css_selector', 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(1) > div > div.detailMainBreadcrumbs > div > ol > li:nth-child(2) > a', True)

            # 데이터 센터 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._data_centerName,2,False,True)

            # 분리할 스토리지 도메인 선택
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self.domainName,2,True)

            # 분리 click
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Detach')
            self.webDriver.findElement('id', 'DetailActionPanelView_Detach', True)

            # OK click
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnDetach')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnDetach', True)

            time.sleep(30)

            _detachCheck = self.webDriver.tableSearch(self.domainName,2)
            
            if _detachCheck == False:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to detach domain..."
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[DATACENTER DETACH DOMAIN] " + msg)

        # 결과 출력
        printLog("[DATACENTER DETACH DOMAIN] RESULT : " + result)
        self._data_centerResult.append(['datacenter' + DELIM + 'detach remove' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('DATACENTER_DETACH_DOMAIN',result, msg)