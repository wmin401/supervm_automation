import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
from __test__.__admin__.__vm__ import *

# vm - 선호도 그룹, 선호도 레이블
class admin_vm2(admin_vm): # 상속
    def __init__(self, webDriver): 
        self.webDriver = webDriver
        super().__init__(webDriver) ## admin_vm의 init값들을 모두 가져오기 위하여 사용        
        self._affinityGroupName = 'auto_affinity_group_%s'%randomString()
        self._affinityLabelName = 'auto_affinity_label_%s'%randomString()
        printLog('VM 2 TEST includes affinity groups, affinity labels')
        
        self._vm2Result = []
        self._vmName = 'HostedEngine' # 개별 테스트를 위해서 이렇게 값을 변경
    
    def check(self, exist, value, idx):
        _check = self.webDriver.tableSearch(value, idx)
        if exist == True:
            if _check == True:
                return PASS, ''
            else:
                return FAIL, 'check failed ...'
        else:
            if _check == True:
                return FAIL, 'check failed ...'
            else:
                return PASS, ''

    def test(self):
        # 선호도 그룹
        # self.affinityGroupCreate()
        # self.affinityGroupUpdate()
        # self.affinityGroupRemove()
        
        # 선호도 레이블
        self.affinityLabelCreate()
        self.affinityLabelUpdate()
        self.affinityLabelRemove()

    def affinityGroupCreate(self):
        printLog(printSquare('Create Affinity Group'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 선호도 그룹 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(9)')
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(9)', True)

            # New 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)

            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'AffinityGroupPopupView_name')
            self.webDriver.findElement('id', 'AffinityGroupPopupView_name')
            self.webDriver.sendKeys(self._affinityGroupName)
            printLog("[VM AFFINITY GROUP CREATE] Name : %s"%self._affinityGroupName)

            # OK 클릭
            self.webDriver.findElement('id', 'AffinityGroupPopupView_OnSave', True)
            time.sleep(0.5)

            # 생성 확인
            result, msg = self.check(exist=True, value=self._affinityGroupName, idx=1)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY GROUP CREATE] " + msg)
        printLog("[VM AFFINITY GROUP CREATE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity group create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_GROUP_CREATE',result, msg) # 모두 대문자

    def affinityGroupUpdate(self):
        printLog(printSquare('Update Affinity Group'))
        result = FAIL
        msg = ''
 
        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 선호도 그룹 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(9)')
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(9)', True)

            # 생성한 그룹 클릭
            self.webDriver.tableSearch(self._affinityGroupName, 1, True)

            # Edit 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Edit')
            self.webDriver.findElement('id', 'DetailActionPanelView_Edit', True)
            
            # Description 입력            
            self.webDriver.explicitlyWait(10, By.ID, 'AffinityGroupPopupView_description')
            self.webDriver.findElement('id', 'AffinityGroupPopupView_description')
            self.webDriver.sendKeys('Update_affinity_group')
            printLog("[VM AFFINITY GROUP UPDATE] Description : Update_affinity_group")
            # OK 클릭
            self.webDriver.findElement('id', 'AffinityGroupPopupView_OnSave', True)
            time.sleep(0.5)
            # 변경 확인
            result, msg = self.check(exist=True, value='Update_affinity_group', idx=2)


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY GROUP UPDATE] " + msg)
        printLog("[VM AFFINITY GROUP UPDATE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity group update' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_GROUP_UPDATE',result, msg) # 모두 대문자

    def affinityGroupRemove(self):
        printLog(printSquare('Remove Affinity Group'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 선호도 그룹 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(9)')
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(9)', True)

            # 생성한 그룹 클릭
            self.webDriver.tableSearch(self._affinityGroupName, 1, True)
            printLog("[VM AFFINITY GROUP REMOVE] Name : %s"%self._affinityGroupName)

            # Remove 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)

            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)

            result, msg = self.check(exist=False, value=self._affinityGroupName, idx=1)


        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY GROUP REMOVE] " + msg)
        printLog("[VM AFFINITY GROUP REMOVE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity group remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_GROUP_REMOVE',result, msg) # 모두 대문자

    def affinityLabelCreate(self):
        printLog(printSquare('Create Affinity Label'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 선호도 레이블 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(10)')
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(10)', True)

            # New 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)

            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'AffinityLabelPopupView_name')
            self.webDriver.findElement('id', 'AffinityLabelPopupView_name')
            self.webDriver.sendKeys(self._affinityLabelName)
            printLog("[VM AFFINITY LABEL CREATE] Name : %s"%self._affinityLabelName)
            

            # OK 클릭
            self.webDriver.findElement('id', 'AffinityLabelPopupView_OnSave', True)
            time.sleep(0.5)

            # 생성 확인
            result, msg = self.check(exist=True, value=self._affinityLabelName, idx=0)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY LABEL CREATE] " + msg)
        printLog("[VM AFFINITY LABEL CREATE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity label create' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_LABEL_CREATE',result, msg) # 모두 대문자

    def affinityLabelUpdate(self):
        printLog(printSquare('Update Affinity Label'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 선호도 레이블 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(10)')
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(10)', True)

            # 생성한 레이블 클릭
            self.webDriver.tableSearch(self._affinityLabelName, 0, True)

            # Edit 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Edit')
            self.webDriver.findElement('id', 'DetailActionPanelView_Edit', True)

            # 이름 수정
            self.webDriver.explicitlyWait(10, By.ID, 'AffinityLabelPopupView_name')
            self.webDriver.findElement('id', 'AffinityLabelPopupView_name')
            self.webDriver.clear()
            self.webDriver.sendKeys(self._affinityLabelName + '_edited')
            printLog("[VM AFFINITY LABEL CREATE] Name : %s_edited"%self._affinityLabelName)

            # OK 클릭
            self.webDriver.findElement('id', 'AffinityLabelPopupView_OnSave', True)
            time.sleep(0.5)

            # 생성 확인
            result, msg = self.check(exist=True, value=self._affinityLabelName + '_edited', idx=0)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY LABEL UPDATE] " + msg)
        printLog("[VM AFFINITY LABEL UPDATE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity label update' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_LABEL_UPDATE',result, msg) # 모두 대문자

    def affinityLabelRemove(self):
        printLog(printSquare('Remove Affinity Label'))
        result = FAIL
        msg = ''

        try:          
            # 컴퓨팅
            time.sleep(2)
            printLog("[VM AFFINITY LABEL REMOVE] Compute - Cluster")
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','compute', True)

            # 클러스터
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','MenuView_clustersAnchor',True)
            time.sleep(2)

            # Default 클릭
            self.webDriver.tableSearch('Default', 1, False, True)

            # Affinity Labels 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(8)')
            self.webDriver.findElement('css_selector', 'body > div.GHYIDY4CHUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(8)', True)

            # 생성한 label 선택
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.tableSearch(self._affinityLabelName + '_edited', 0, True)

            # Edit 에서 VM 제거 필요
            self.webDriver.findElement('id','DetailActionPanelView_Edit',True)
            # 팝업에서 VM - 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div > div > button:nth-child(2)')
            self.webDriver.findElement('css_selector', 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div > div > button:nth-child(2)', True)
            
            # OK 클릭
            self.webDriver.findElement('id','AffinityLabelPopupView_OnSave',True)
            time.sleep(0.5)

            # Delete 클릭
            self.webDriver.findElement('id','DetailActionPanelView_Remove',True)

            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)    
            time.sleep(0.5)

            result, msg = self.check(exist=False, value=self._affinityLabelName + '_edited', idx=0)

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY LABEL REMOVE] " + msg)
        printLog("[VM AFFINITY LABEL REMOVE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity label remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_LABEL_REMOVE',result, msg) # 모두 대문자
