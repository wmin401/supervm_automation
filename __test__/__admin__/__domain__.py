from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
import time

class admin_domain:
    def __init__(self, webDriver):
        printLog("* 도메인 테스트 시작")
        self._domainResult = []
        self._domainName = 'NFS-31'
        self._domainPath = '192.168.17.31:/nfs'
        self.webDriver = webDriver
        
    def create(self):
        printLog('Create Domain ')
        
        try:
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # 새로운 도메인 클릭
            #time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_NewDomain',True)
            #_newBtn = webDriver.findElement('id','ActionPanelView_NewDomain',True)

            time.sleep(1)

            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'StoragePopupView_name')
            #_newBtn = webDriver.findElement('id','StoragePopupView_name',True)
            self.webDriver.findElement('id','StoragePopupView_name',True)
            self.webDriver.sendKeys(self._domainName)

            # 경로 입력
            self.webDriver.implicitlyWait(10)
            #_newBtn = webDriver.findElement('id','ActionPanelView_NewDomain',True)
            self.webDriver.findElement('id','NfsStorageView_path',True)
            self.webDriver.sendKeys(self._domainPath)

            # 새로운 도메인 OK 버튼
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

            time.sleep(120)
            
            '''
            # 취소 버튼
            webDriver.implicitlyWait(10)
            _cancelBtn = webDriver.findElement('css_selector','#StoragePopupView_Cancel > button',True)
            '''
            _createCheck = self.webDriver.tableSearch(self._domainName, 2)

            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new domain..."


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._domainResult.append(['domain' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])

    def maintenance(self):
        printLog('Domain maintenance mode')
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._domainName, 2, True)
            time.sleep(1)

            # 도메인 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)

            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

            # 유지보수 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DetailActionPanelView_Maintenance',True)

            # 스토리지 도메인 관리 창 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnMaintenance',True)

            time.sleep(40)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

    def attach(self):
        printLog('attach Domain')
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._domainName, 2, True)
            time.sleep(1)

            # 도메인 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)

            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

            # 연결 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DetailActionPanelView_Attach',True)

            # 데이터 센터에 연결 OK 클릭
            time.sleep(1)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button',True)

            time.sleep(60)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
    
    def detach(self):
        printLog('Detach Domain')
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._domainName, 2, True)
            time.sleep(1)

            # 도메인 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)

            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

            # 분리 클릭
            time.sleep(3)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DetailActionPanelView_Detach',True)

            # 스토리지 분리 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnDetach > button',True)

            time.sleep(30)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

    def active(self):
        printLog('active Domain')
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._domainName, 2, True)
            time.sleep(1)

            # 도메인 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)

            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

            # 활성 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DetailActionPanelView_Activate',True)

            time.sleep(10)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
         
    def remove(self):
        printLog('Remove Domain ')
        
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._domainName, 2, True)
            time.sleep(1)

            # 삭제 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_Remove',True)

            # 스토리지 삭제창의 포멧 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','StorageRemovePopupView_format',True)

            # 스토리지 삭제 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#StorageRemovePopupView_OnRemove > button',True)

            time.sleep(10)
                    
            _createCheck = self.webDriver.tableSearch(self._domainName, 2)

            if _createCheck == True:
                result = FAIL
                msg = 'Failed to create new domain...'
            else:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._domainResult.append(['domain' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])


    def destroy(self):
        printLog('Destroy Domain ')
        
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            #_storageBtn = webDriver.findElement('id','MenuView_storageTab',True)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            #_domainBtn = webDriver.findElement('id','MenuView_domainsAnchor',True)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._domainName, 2, True)
            time.sleep(1)

            # 더보기 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button',True)

            # 파괴 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#ActionPanelView_Destroy > a',True)

            # 작업 승인 체크
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ForceRemoveConfirmationPopupView_latch',True)

            # 스토리지 도메인 삭제 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ForceRemoveConfirmationPopupView_OnDestroy',True)

            time.sleep(5)
                    
            _createCheck = self.webDriver.tableSearch(self._domainName, 2)

            if _createCheck == True:
                result = FAIL
                msg = 'Failed to create new domain...'
            else:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._domainResult.append(['domain' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])