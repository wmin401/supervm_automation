from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
from __common__.__testlink__ import *
import time

class admin_domain:
    def __init__(self, webDriver):
        printLog("* 도메인 테스트 시작")
        self.webDriver = webDriver
        self.tl = testlink()
        self._domainResult = []
        self._domainNFSName = 'NFS-31'
        self._domainNFSPath = '192.168.17.31:/nfs'

        self._domainCEPHName = 'posix-31'
        self._domainCEPHPath = '192.168.17.31:6789:/volumes/_nogroup/tim1/e326d8ed-5092-4249-86cb-cdc8ad22394b'
        self._domainCEPHvfsType = 'ceph'
        self._domainCEPHAuth = 'name=admin,secret=AQDHR4JhTcz2CxAAG1TIoppqJclaMWyDYO1v0A=='

    def test(self):
        self.create('nfs')
        self.maintenance('nfs')
        self.active('nfs')
        self.maintenance('nfs')
        self.detach('nfs')
        self.attach('nfs')
        self.maintenance('nfs')
        self.detach('nfs')
        self.remove('nfs')
        self.create('nfs')
        self.maintenance('nfs')
        self.destroy('nfs')

        #self.create('ceph')
        #self.maintenance('ceph')
        #self.active('ceph')
        #self.maintenance('ceph')
        #self.detach('ceph')
        #self.attach('ceph')
        #self.maintenance('ceph')
        #self.detach('ceph')
        #self.remove('ceph')
        #self.create('ceph')
        #self.maintenance('ceph')
        #self.destroy('ceph')
        
    def create(self, storageType):
        printLog('Create Domain')
        
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

            # 스토리지 유형 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','StoragePopupView_availableStorageTypeItems',True)

            if(storageType == 'NFS' or storageType =='nfs'):
                # NFS 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_availableStorageTypeItems > div > ul > li:nth-child(1)',True)

                # 이름 입력
                self.webDriver.explicitlyWait(10, By.ID, 'StoragePopupView_name')
                #_newBtn = webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.sendKeys(self._domainNFSName)

                # 경로 입력
                self.webDriver.implicitlyWait(10)
                #_newBtn = webDriver.findElement('id','ActionPanelView_NewDomain',True)
                self.webDriver.findElement('id','NfsStorageView_path',True)
                self.webDriver.sendKeys(self._domainNFSPath)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(40)

                _createCheck = self.webDriver.tableSearch(self._domainNFSName, 2)

                if _createCheck == True:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = "Failed to create new NFS domain..."

            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # ceph 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_availableStorageTypeItems > div > ul > li:nth-child(2)',True)

                # 이름 입력
                self.webDriver.explicitlyWait(10, By.ID, 'StoragePopupView_name')
                self.webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.sendKeys(self._domainCEPHName)

                # 경로 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','PosixStorageView_path',True)
                self.webDriver.sendKeys(self._domainCEPHPath)

                # VFS 유형 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','PosixStorageView_vfsType',True)
                self.webDriver.sendKeys(self._domainCEPHvfsType)

                # VFS 유형 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','PosixStorageView_mountOptions',True)
                self.webDriver.sendKeys(self._domainCEPHAuth)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(40)
      
                '''
                # 취소 버튼
                webDriver.implicitlyWait(10)
                _cancelBtn = webDriver.findElement('css_selector','#StoragePopupView_Cancel > button',True)
                '''
                _createCheck = self.webDriver.tableSearch(self._domainCEPHName, 2)

                if _createCheck == True:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = "Failed to create new CEPH domain..."
            
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._domainResult.append(['domain' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DOMAIN_CREATE', result, msg)

    def maintenance(self,storageType):
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

            if(storageType == 'NFS' or storageType == 'nfs'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,True,True)
            
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,True,True)


            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

            # 유지보수 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DetailActionPanelView_Maintenance',True)

            # 스토리지 도메인 관리 창 OK 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnMaintenance',True)

            time.sleep(60)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

    def attach(self, storageType):
        printLog('Attach Domain')
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

            if(storageType == 'NFS' or storageType == 'nfs'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,True,True)
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,True,True)

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
    
    def detach(self, storageType):
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

            if(storageType == 'NFS' or storageType == 'nfs'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                #self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)
                self.webDriver.tableSearch(self._domainNFSName,2,True,True)

            elif(storageType == 'CEPH' or storageType == 'ceph'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                #self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)
                self.webDriver.tableSearch(self._domainCEPHName,2,True,True)

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

    def active(self,storageType):
        printLog('Active Domain')
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

            if(storageType == 'NFS' or storageType == 'nfs'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                #self.webDriver.findElement('css_selector','#MainStorageView_table_content_col2_row1',True)
                self.webDriver.tableSearch(self._domainNFSName,2,True,True)
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,True,True)

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
         
    def remove(self, storageType):
        printLog('Remove Domain')
        
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

            if(storageType == 'NFS' or storageType == 'nfs'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
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
                    
            _createCheck = self.webDriver.tableSearch(self._domainNFSName, 2)

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

        self.tl.junitBuilder('DOMAIN_REMOVE', result, msg)


    def destroy(self, storageType):
        printLog('Destroy Domain')
        
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

            if(storageType == 'NFS' or storageType == 'nfs'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

            elif(storageType == 'CEPH' or storageType == 'ceph'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
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
                    
            _removeCheck = self.webDriver.tableSearch(self._domainNFSName, 2)

            if _removeCheck == True:
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

        self.tl.junitBuilder('DOMAIN_DESTROY', result, msg)