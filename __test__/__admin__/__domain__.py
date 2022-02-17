from asyncio import sleep
from re import T
from typing import Tuple
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

        self.dataCenterName = 'Default'

        self._domainNFSName = 'NFS-4'
        self._domainNFSPath = '10.0.0.4:/nfs'

        self._domainCEPHName = 'posix-31'
        self._domainCEPHPath = '192.168.17.31:6789:/volumes/_nogroup/tim1/e326d8ed-5092-4249-86cb-cdc8ad22394b'
        self._domainCEPHvfsType = 'ceph'
        self._domainCEPHAuth = 'name=admin,secret=AQDHR4JhTcz2CxAAG1TIoppqJclaMWyDYO1v0A=='

        self._domainGLUSTERName = 'gluster-5'
        self._domainGLUSTERPath = '10.0.0.5:/data'

        self._domainISCSIName = 'iSCSI-5'
        self._domainISCSIPath = '10.0.0.5'

        self._domainLOCALName = 'Local'
        self._domainLOCALPath = '/data'

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

        self.create('ceph')
        self.maintenance('ceph')
        self.active('ceph')
        self.maintenance('ceph')
        self.detach('ceph')
        self.attach('ceph')
        self.maintenance('ceph')
        self.detach('ceph')
        self.remove('ceph')
        self.create('ceph')
        self.maintenance('ceph')
        self.destroy('ceph')

        self.create('gluster')
        self.maintenance('gluster')
        self.active('gluster')
        self.maintenance('gluster')
        self.detach('gluster')
        self.attach('gluster')
        self.maintenance('gluster')
        self.detach('gluster')
        self.remove('gluster')
        self.create('gluster')
        self.maintenance('gluster')
        self.destroy('gluster')

        #self.create('iscsi')
        self.maintenance('iscsi')
        self.active('iscsi')
        self.maintenance('iscsi')
        self.detach('iscsi')
        self.attach('iscsi')
        self.maintenance('iscsi')
        self.detach('iscsi')
        self.remove('iscsi')
        #self.create('iscsi')
        self.maintenance('iscsi')
        self.destroy('iscsi')

        #self.create('local')
        self.create('local')
        self.maintenance('local')
        self.active('local')
        self.maintenance('local')
        self.detach('local')
        self.maintenance('local')
        self.detach('local')
        #self.create('local')
        self.maintenance('local')
        #self.destroy('local')
        self.maintenance('local')
        self.detach('local')
        self.create('local')
        self.maintenance('local')
        self.destroy('local')
        
    def create(self, storageType):
        printLog('Create Domain')
        
        try:
            # 스토리지
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            # 새로운 도메인 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ActionPanelView_NewDomain',True)

            time.sleep(1)

            # 스토리지 유형 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','StoragePopupView_availableStorageTypeItems',True)

            if(storageType == 'NFS' or storageType =='nfs'):
                # NFS 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_availableStorageTypeItems > div > ul > li:nth-child(1)',True)

                # 이름 입력
                self.webDriver.explicitlyWait(10,By.ID,'StoragePopupView_name')
                self.webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.sendKeys(self._domainNFSName)

                # 경로 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','NfsStorageView_path',True)
                self.webDriver.sendKeys(self._domainNFSPath)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(50)

                _createCheck = self.webDriver.tableSearch(self._domainNFSName,2)

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
                self.webDriver.explicitlyWait(10,By.ID,'StoragePopupView_name')
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

                # 마운트 옵션 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','PosixStorageView_mountOptions',True)
                self.webDriver.sendKeys(self._domainCEPHAuth)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(50)

                _createCheck = self.webDriver.tableSearch(self._domainCEPHName,2)

                if _createCheck == True:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = "Failed to create new CEPH domain..."

            elif(storageType == 'GLUSTER' or storageType == 'gluster'):
                # GlusterFS 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_availableStorageTypeItems > div > ul > li:nth-child(3)',True)

                # 이름 입력
                self.webDriver.explicitlyWait(10,By.ID,'StoragePopupView_name')
                self.webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.sendKeys(self._domainGLUSTERName)

                # 경로 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','GlusterStorageView_path',True)
                self.webDriver.sendKeys(self._domainGLUSTERPath)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(50)

                _createCheck = self.webDriver.tableSearch(self._domainGLUSTERName,2)

                if _createCheck == True:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = "Failed to create new GLUSTER domain..."
                
            '''
                '''
            elif(storageType == 'ISCSI' or storageType == 'iscsi'):
                # iSCSI 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_availableStorageTypeItems > div > ul > li:nth-child(4)',True)

                # 이름 입력
                self.webDriver.explicitlyWait(10,By.ID,'StoragePopupView_name')
                self.webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.sendKeys(self._domainISCSIName)

                # 경로 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','GlusterStorageView_path',True)
                self.webDriver.sendKeys(self._domainISCSIPath)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(50)

                _createCheck = self.webDriver.tableSearch(self._domainISCSIName,2)

                if _createCheck == True:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = "Failed to create new GLUSTER domain..."
            '''
                '''

            elif(storageType == 'LOCAL' or storageType == 'local'):

                # 데이터 센터 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','StoragePopupView_dataCenter',True)

                # 로컬 스토리지 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/div/ul/li[2]/a',True)

                time.sleep(2)

                # 스토리지 유형 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','StoragePopupView_availableStorageTypeItems',True)

                # 로컬 스토리지 선택
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[2]/div/div/div/div[3]/div[1]/div/div[1]/div/div/div/ul/li[4]',True)

                # 이름 입력
                self.webDriver.explicitlyWait(10,By.ID,'StoragePopupView_name')
                self.webDriver.findElement('id','StoragePopupView_name',True)
                self.webDriver.sendKeys(self._domainLOCALName)

                # 경로 입력
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','LocalStorageView_localPathEditor',True)
                self.webDriver.sendKeys(self._domainLOCALPath)

                # 새로운 도메인 OK 버튼
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#StoragePopupView_OnSave > button',True)

                time.sleep(50)

                _createCheck = self.webDriver.tableSearch(self._domainLOCALName,2)

                if _createCheck == True:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = "Failed to create new LOCAL domain..."
            
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)

        printLog("* RESULT : " + result)
        self._domainResult.append(['domain' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DOMAIN_CREATE',result,msg)

    def maintenance(self,storageType):
        printLog('Domain maintenance mode')
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            if(storageType == 'NFS' or storageType == 'nfs'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,False,True)
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,False,True)

            elif(storageType == 'GLUSTER' or storageType == 'gluster'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainGLUSTERName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainGLUSTERName,2,False,True)
            
            elif(storageType == 'ISCSI' or storageType == 'iscsi'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainISCSIName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainISCSIName,2,False,True)
            
            elif(storageType == 'LOCAL' or storageType == 'local'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainLOCALName,2,True,False)
                time.sleep(1)
                
                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainLOCALName,2,False,True)


            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

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
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            if(storageType == 'NFS' or storageType == 'nfs'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 연결 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Attach',True)

                # 데이터 센터에 연결 OK 클릭
                time.sleep(1)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button',True)

                time.sleep(60)

                _attachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _attachCheck == False:
                    result = FAIL
                    msg = 'Failed to attach NFS domain...'
                else:
                    result = PASS
                    msg = ''
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 연결 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Attach',True)

                # 데이터 센터에 연결 OK 클릭
                time.sleep(1)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button',True)

                time.sleep(60)

                _attachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _attachCheck == False:
                    result = FAIL
                    msg = 'Failed to attach CEPH domain...'
                else:
                    result = PASS
                    msg = ''

            elif(storageType == 'GLUSTER' or storageType == 'gluster'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainGLUSTERName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainGLUSTERName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 연결 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Attach',True)

                # 데이터 센터에 연결 OK 클릭
                time.sleep(1)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button',True)

                time.sleep(60)

                _attachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _attachCheck == False:
                    result = FAIL
                    msg = 'Failed to attach Gluster domain...'
                else:
                    result = PASS
                    msg = ''
            
            elif(storageType == 'ISCSI' or storageType == 'iscsi'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainISCSIName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainISCSIName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 연결 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Attach',True)

                # 데이터 센터에 연결 OK 클릭
                time.sleep(1)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('xpath','/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button',True)

                time.sleep(60)

                _attachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _attachCheck == False:
                    result = FAIL
                    msg = 'Failed to attach iSCSI domain...'
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

        self.tl.junitBuilder('DOMAIN_DETACH',result,msg)
    
    def detach(self, storageType):
        printLog('Detach Domain')
        
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            if(storageType == 'NFS' or storageType == 'nfs'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 분리 클릭
                time.sleep(3)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Detach',True)

                # 스토리지 분리 OK 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnDetach > button',True)

                time.sleep(30)

                _detachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _detachCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to detach NFS domain...'

            elif(storageType == 'CEPH' or storageType == 'ceph'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 분리 클릭
                time.sleep(3)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Detach',True)

                # 스토리지 분리 OK 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnDetach > button',True)

                time.sleep(30)

                _detachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _detachCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to detach CEPH domain...'
            
            elif(storageType == 'GLUSTER' or storageType == 'gluster'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainGLUSTERName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainGLUSTERName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 분리 클릭
                time.sleep(3)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Detach',True)

                # 스토리지 분리 OK 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnDetach > button',True)

                time.sleep(30)

                _detachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _detachCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to detach Gluster domain...'

            elif(storageType == 'ISCSI' or storageType == 'iscsi'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainISCSIName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainISCSIName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 분리 클릭
                time.sleep(3)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Detach',True)

                # 스토리지 분리 OK 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnDetach > button',True)

                time.sleep(30)

                _detachCheck = self.webDriver.tableSearch(self.dataCenterName,1,False,False,True)

                if _detachCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to detach iSCSI domain...'

            elif(storageType == 'LOCAL' or storageType == 'local'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainLOCALName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainLOCALName,2,False,True)

                # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

                # 분리 클릭
                time.sleep(3)
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','DetailActionPanelView_Detach',True)

                # 도메인을 포멧합니다. 스토리지 컨텐츠가 손실됩니다! 체크
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('id','RemoveConfirmationPopupView_force',True)

                # 스토리지 분리 OK 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','#RemoveConfirmationPopupView_OnDetach > button',True)

                time.sleep(30)

                _detachCheck = self.webDriver.tableSearch(self.dataCenterName,2) # 로컬스토리지의 경우 분리 시 도메인 목록에서 즉시 제거됨

                if _detachCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to detach iSCSI domain...'

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("* MESSAGE : " + msg)
        
        printLog("* RESULT : " + result)
        self._domainResult.append(['domain' + DELIM + 'create&cancel' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('DOMAIN_DETACH',result,msg)

    def active(self,storageType):
        printLog('Active Domain')
        try:
            time.sleep(1)
            # 스토리지
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            if(storageType == 'NFS' or storageType == 'nfs'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainNFSName,2,False,True)
            
            elif(storageType == 'CEPH' or storageType == 'ceph'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainCEPHName,2,False,True)
            
            elif(storageType == 'GLUSTER' or storageType == 'gluster'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainGLUSTERName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainGLUSTERName,2,False,True)
            
            elif(storageType == 'ISCSI' or storageType == 'iscsi'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainISCSIName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainISCSIName,2,False,True)

            elif(storageType == 'LOCAL' or storageType == 'local'):
                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainLOCALName,2,True,False)
                time.sleep(1)

                # 도메인 이름 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.tableSearch(self._domainLOCALName,2,False,True)

            # 도메인 이름 클릭 후 데이터 센터 탭으로 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(2) > a',True)

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
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            if(storageType == 'NFS' or storageType == 'nfs'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
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

                time.sleep(30)
                        
                _removeCheck = self.webDriver.tableSearch(self._domainNFSName,2)
            
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

                time.sleep(30)
                        
                _removeCheck = self.webDriver.tableSearch(self._domainCEPHName,2)
            
            elif(storageType == 'GLUSTER' or storageType == 'gluster'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainGLUSTERName,2,True,False)
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

                time.sleep(30)
                        
                _removeCheck = self.webDriver.tableSearch(self._domainGLUSTERName,2)
            
            elif(storageType == 'ISCSI' or storageType == 'iscsi'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainISCSIName,2,True,False)
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

                time.sleep(50)
                        
                _removeCheck = self.webDriver.tableSearch(self._domainISCSIName,2)
            
            if _removeCheck == True:
                result = FAIL
                msg = 'Failed to remove new domain...'
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
            self.webDriver.findElement('id','MenuView_storageTab',True)

            # 도메인
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_domainsAnchor',True)

            if(storageType == 'NFS' or storageType == 'nfs'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainNFSName,2,True,False)
                time.sleep(1)

                # 더보기 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button',True)

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
                        
                _destroyCheck = self.webDriver.tableSearch(self._domainNFSName,2)

                if _destroyCheck == True:
                    result = FAIL
                    msg = 'Failed to destroy NFS domain...'
                else:
                    result = PASS
                    msg = ''

            elif(storageType == 'CEPH' or storageType == 'ceph'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainCEPHName,2,True,False)
                time.sleep(1)

                # 더보기 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button',True)

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
                        
                _destroyCheck = self.webDriver.tableSearch(self._domainCEPHName,2)

                if _destroyCheck == True:
                    result = FAIL
                    msg = 'Failed to destroy CEPH domain...'
                else:
                    result = PASS
                    msg = ''

            elif(storageType == 'GLUSTER' or storageType == 'gluster'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainGLUSTERName,2,True,False)
                time.sleep(1)

                # 더보기 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button',True)

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
                        
                _destroyCheck = self.webDriver.tableSearch(self._domainGLUSTERName,2)

                if _destroyCheck == True:
                    result = FAIL
                    msg = 'Failed to destroy GLUSTER domain...'
                else:
                    result = PASS
                    msg = ''
            
            elif(storageType == 'ISCSI' or storageType == 'iscsi'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainISCSIName,2,True,False)
                time.sleep(1)

                # 더보기 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button',True)

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
                        
                _destroyCheck = self.webDriver.tableSearch(self._domainISCSIName,2)

                if _destroyCheck == True:
                    result = FAIL
                    msg = 'Failed to destroy iSCSI domain...'
                else:
                    result = PASS
                    msg = ''
            
            elif(storageType == 'LOCAL' or storageType == 'local'):

                # table 내부에 생성한 도메인의 이름이 있을 경우 해당 row 클릭
                self.webDriver.tableSearch(self._domainLOCALName,2,True,False)
                time.sleep(1)

                # 더보기 클릭
                self.webDriver.implicitlyWait(10)
                self.webDriver.findElement('css_selector','body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div > button',True)

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
                        
                _destroyCheck = self.webDriver.tableSearch(self._domainLOCALName,2)

            if _destroyCheck == True:
                result = FAIL
                msg = 'Failed to destroy new domain...'
                msg = 'Failed to destroy Local domain...'
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

    '''
    def iSCSICreate(self):    
        printLog(printSquare('I S C S I Create'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MenuView_storageTab')
            self.webDriver.findElement('id', 'MenuView_storageTab', True)

            time.sleep(1)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_domainsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_domainsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_NewDomain')
            self.webDriver.findElement('id', 'ActionPanelView_NewDomain', True)

            time.sleep(1)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#StoragePopupView_availableStorageTypeItems .filter-option')
            self.webDriver.findElement('css_selector', '#StoragePopupView_availableStorageTypeItems .filter-option', True)

            time.sleep(1)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'iSCSI')
            self.webDriver.findElement('link_text', 'iSCSI', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'StoragePopupView_name')
            self.webDriver.findElement('id', 'StoragePopupView_name', False)
            self.webDriver.sendKeys(self._domainISCSIName) # You have to change this you want to write

            time.sleep(3)

            
            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[1]/td/div/div/table[1]/tbody/tr/td/div')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[1]/td/div/div/table[1]/tbody/tr/td/div', True)
            

            # type
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[1]/td/div/div/table[2]/tbody/tr/td/div/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td/div/div[1]/input')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[1]/td/div/div/table[2]/tbody/tr/td/div/table[1]/tbody/tr/td[1]/table/tbody/tr[1]/td/div/div[1]/input', True)
            self.webDriver.sendKeys(self._domainISCSIPath) # You have to change this you want to write

            time.sleep(3)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.GB10KEXCO3C > .btn')
            self.webDriver.findElement('css_selector', '.GB10KEXCO3C > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.fa-arrow-right')
            self.webDriver.findElement('css_selector', '.fa-arrow-right', True)

            time.sleep(10)

            # + 버튼 click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[2]/td/div/div/div[2]/div/div/div[2]/div')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[2]/td/div/div/div[2]/div/div/div[2]/div', True)

            time.sleep(3)

            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[2]/td/div/div/div[2]/div/div/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[8]/div/span/button')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[2]/td/div/div/div[2]/div/div/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[8]/div/span/button', True)

            time.sleep(1)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.modal-footer')
            self.webDriver.findElement('css_selector', '.modal-footer', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(20)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[I S C S I CREATE] " + msg)

        # 결과 출력
        printLog("[I S C S I CREATE] RESULT : " + result)
        #self._iResult.append(['i' + DELIM + 's c s i create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('I_S_C_S_I_CREATE',result, msg)
        '''