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
        self._snapshotName = 'auto_snapshot_%s'%randomString()
        printLog('VM 2 TEST includes affinity groups, affinity labels, snapshot')
        
        self._vm2Result = []
        self._vmName = 'for_automation' # 개별 테스트를 위해서 이렇게 값을 overriding
        self._clusterName = 'Default' # Default 로 고정 

        
    
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
        
        # # 선호도 레이블
        # self.affinityLabelCreate()
        # self.affinityLabelUpdate()
        # self.affinityLabelRemove()

        # 스냅샷
        self.snapshotCreate()
        self.restoreVMUsingSnapshot()
        self.vmCreateInSnapshot()
        self.snapshotRemove()

    def affinityGroupCreate(self):
        printLog(printSquare('Create Affinity Group'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 선호도 그룹 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '선호도 그룹')
            self.webDriver.findElement('link_text', '선호도 그룹', True)

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
            time.sleep(2)

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
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '선호도 그룹')
            self.webDriver.findElement('link_text', '선호도 그룹', True)

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
            time.sleep(2)
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
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '선호도 그룹')
            self.webDriver.findElement('link_text', '선호도 그룹', True)

            # 생성한 그룹 클릭
            self.webDriver.tableSearch(self._affinityGroupName, 1, True)
            printLog("[VM AFFINITY GROUP REMOVE] Name : %s"%self._affinityGroupName)

            # Remove 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)

            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(2)

            try:
                result, msg = self.check(exist=False, value=self._affinityGroupName, idx=1)
            except:
                result = PASS
                msg = ''


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
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '선호도 레이블')
            self.webDriver.findElement('link_text', '선호도 레이블', True)

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
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '선호도 레이블')
            self.webDriver.findElement('link_text', '선호도 레이블', True)

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

            # 클러스터 이름 클릭
            self.webDriver.tableSearch(self._clusterName, 1, False, True)

            # Affinity Labels 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '선호도 레이블')
            self.webDriver.findElement('link_text', '선호도 레이블', True)

            # 생성한 label의 이름 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.tableSearch(self._affinityLabelName + '_edited', 0, True)
            
            # 편집 버튼 클릭
            self.webDriver.findElement('id','DetailActionPanelView_Edit',True)
            
            # 팝업에서 VM - 클릭
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[4]/div[1]/div/div/div/button[1]')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[4]/div[1]/div/div/div/button[1]', True)

            # OK 클릭
            self.webDriver.findElement('id','AffinityLabelPopupView_OnSave',True)
            time.sleep(0.5)

            # 삭제 클릭
            self.webDriver.findElement('id','DetailActionPanelView_Remove',True)

            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)    
            time.sleep(0.5)

            try:
                result, msg = self.check(exist=False, value=self._affinityLabelName + '_edited', idx=0)
            except:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM AFFINITY LABEL REMOVE] " + msg)
        printLog("[VM AFFINITY LABEL REMOVE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'affinity label remove' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('VM_AFFINITY_LABEL_REMOVE',result, msg) # 모두 대문자

    def snapshotCreate(self):    
        printLog(printSquare('Create Snapshot'))
        result = FAIL
        msg = ''

        try:
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 스냅샷 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '스냅샷')
            self.webDriver.findElement('link_text', '스냅샷', True)
            time.sleep(1)

            # 생성 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)
            time.sleep(0.5)

            # 설명 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmSnapshotCreatePopupWidget_description')
            self.webDriver.findElement('id', 'VmSnapshotCreatePopupWidget_description', False)
            self.webDriver.sendKeys(self._snapshotName)

            # OK 클릭
            self.webDriver.findElement('id', 'VmSnapshotCreatePopupView_OnSave', True)
            time.sleep(5)

            # 확인 방법 li 태그를 모두 확인하면서 text Content에 내가 입력한 값이 포함되어있으면 성공
            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            lis = ul.find_elements_by_tag_name('li')
            cnt = 0
            for li in lis:
                cnt += 1
                if self._snapshotName in li.text: 
                    result = PASS
                    printLog("[VM SNAPSHOT CREATE] Snapshot Name : %s"%self._snapshotName)
                    msg = ''
                    break
                else:
                    result = FAIL
                    msg = 'Failed to create snapshot of %s'%self._vmName
                    if cnt == len(lis):
                        printLog("[VM SNAPSHOT CREATE] " + msg)
                    continue
            
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM SNAPSHOT CREATE] " + msg)

        # 결과 출력
        printLog("[VM SNAPSHOT CREATE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'snapshot create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_SNAPSHOT_CREATE',result, msg)
        
        printLog("[VM SNAPSHOT CREATE] Wait 30 seconds for unlock snapshot")
        time.sleep(30)

    def restoreVMUsingSnapshot(self):
        printLog(printSquare('Restore VM using Snapshot'))
        result = FAIL
        msg = ''

        try:
            self.setup()
                # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 스냅샷 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '스냅샷')
            self.webDriver.findElement('link_text', '스냅샷', True)
            time.sleep(1)
            	
            # 생성된 스냅샷 선택
            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            lis = ul.find_elements_by_tag_name('li')
            isClicked = False
            for li in lis:
                try:
                    if self._snapshotName in li.text: 
                        printLog("[VM SNAPSHOT REMOVE] Snapshot Name : %s"%self._snapshotName)
                        li.click()
                        isClicked = True
                        break
                except:
                    continue
            if isClicked == False:
                result = FAIL
                msg = 'Failed to remove snapshot(Not found)'

            # 미리보기 드롭다운 메뉴에서 사용자 지정 선택
            self.webDriver.findElement('css_selector', '#DetailActionPanelView_Preview > button.btn.btn-default.dropdown-toggle', True)
            self.webDriver.findElement('css_selector', '#DetailActionPanelView_Preview > ul > li', True)
            time.sleep(1)

            # OK 클릭
            self.webDriver.findElement('id', 'VmSnapshotCustomPreviewPopupView_OnCustomPreview', True)
            time.sleep(5)
            
            # Active VM 이 Active VM before the preview로 변경되면 성공
            
            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            lis = ul.find_elements_by_tag_name('li')
            isClicked = False
            for li in lis:
                try:
                    if 'Active VM before the preview' in li.text: 
                        li.click()
                        result = PASS
                        msg = ''                        
                        break
                    else:                        
                        result = FAIL
                        msg = 'Failed to restore ...'
                except:
                    continue


        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM SNAPSHOT RESTORE VM] " + msg)

        # 결과 출력
        printLog("[VM SNAPSHOT RESTORE VM] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'restore using snapshot' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_RESTORE_USING_SNAPSHOT',result, msg)
        time.sleep(30)

        # 테스트 이후 되돌리기 클릭
        self.webDriver.findElement('id', 'DetailActionPanelView_Undo', True)
        printLog("[VM SNAPSHOT RESTORE VM] Going back to before restore...")
        time.sleep(30)

    def vmCreateInSnapshot(self):        
        printLog(printSquare('Create VM in snapshot'))
        result = FAIL
        msg = ''

        try:
            self.setup()
            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 스냅샷 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '스냅샷')
            self.webDriver.findElement('link_text', '스냅샷', True)
            time.sleep(1)
            	
            # 생성된 스냅샷 선택
            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            lis = ul.find_elements_by_tag_name('li')
            isClicked = False
            for li in lis:
                try:
                    if self._snapshotName in li.text: 
                        printLog("[VM SNAPSHOT REMOVE] Snapshot Name : %s"%self._snapshotName)
                        li.click()
                        isClicked = True
                        break
                except:
                    continue
            if isClicked == False:
                result = FAIL
                msg = 'Failed to remove snapshot(Not found)'

            # 복제 클릭
            self.webDriver.findElement('id', 'DetailActionPanelView_CloneVM', True)

            # 이름 입력 후 생성
            self.webDriver.explicitlyWait(10, By.ID, 'VmClonePopupWidget_name')
            self.webDriver.findElement('id', 'VmClonePopupWidget_name')
            self.webDriver.sendKeys('VM_for_%s'%self._snapshotName)
            # OK 클릭
            self.webDriver.findElement('id', 'VmClonePopupView_OnCloneVM', True)
            
            # 컴퓨팅 - 가상머신
            self.setup()
            # 가상머신 목록 확인
            result, msg = self.webDriver.isChangedStatus('VM_for_%s'%self._snapshotName, 2, 13, ['이미지 잠김', 'Image locked', "Image Locked"], ['Down'])

        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CREATE VM IN SNAPSHOT] " + msg)

        # 결과 출력
        printLog("[VM CREATE VM IN SNAPSHOT] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'create vm in snapshot' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_CREATE_IN_SNAPSHOT',result, msg)

    def snapshotRemove(self):    
        printLog(printSquare('Remove Snapshot'))
        result = FAIL
        msg = ''

        try:
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vmName, 2, False, True)

            # 스냅샷 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '스냅샷')
            self.webDriver.findElement('link_text', '스냅샷', True)
            time.sleep(2)
        
            #
            ul = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
            lis = ul.find_elements_by_tag_name('li')
            isClicked = False
            for li in lis:
                try:
                    if self._snapshotName in li.text: 
                        printLog("[VM SNAPSHOT REMOVE] Snapshot Name : %s"%self._snapshotName)
                        li.click()
                        isClicked = True
                        break
                except:
                    continue
            if isClicked == False:
                result = FAIL
                msg = 'Failed to remove snapshot(Not found)'

            # 삭제 버튼 클릭
            self.webDriver.findElement('id', 'DetailActionPanelView_Remove', True)
            time.sleep(0.5)

            # OK 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id', 'RemoveConfirmationPopupView_OnRemove', True)
            time.sleep(1)

            # 삭제 확인
            isRemoved = False
            st = time.time()
            printLog("[VM SNAPSHOT REMOVE] %s is removing ..."%self._snapshotName)
            while not isRemoved:
                cnt = 0
                snapshotTable = self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/ul')
                time.sleep(1)
                snapshotList = snapshotTable.find_elements_by_tag_name('li')
                for snapshot in snapshotList:
                    try:
                        if self._snapshotName in snapshot.text:
                            result = FAIL
                        else:
                            cnt += 1
                            # print('*** ', cnt, len(snapshotList))
                            if cnt == len(snapshotList):
                                # 삭제됨
                                isRemoved = True
                                result = PASS
                                msg = ''
                                break
                    except:
                        continue
                if time.time() - st > 120: # 2분 경과하면 timeout으로 나감      
                    result = FAIL
                    msg = 'Failed to remove snapshot(timeout)'
                
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM SNAPSHOT REMOVE] " + msg)

        # 결과 출력
        printLog("[VM SNAPSHOT REMOVE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'snapshot remove' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_SNAPSHOT_REMOVE',result, msg)
        