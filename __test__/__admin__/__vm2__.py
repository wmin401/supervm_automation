import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
from __common__.__ssh__ import ssh_connection
from __test__.__admin__.__vm__ import *

# vm - 선호도 그룹, 선호도 레이블
class admin_vm2(admin_vm): # 상속
    def __init__(self, webDriver): 
        self.webDriver = webDriver
        super().__init__(webDriver) ## admin_vm의 init값들을 모두 가져오기 위하여 사용        
        self._affinityGroupName = 'auto_affinity_group_%s'%randomString()
        self._affinityLabelName = 'auto_affinity_label_%s'%randomString()
        self._snapshotName = 'auto_snapshot_%s'%randomString()
        # printLog('VM 2 TEST includes Administrative tasks')
        
        self._vm2Result = []
        # self._vm2Name = 'for_automation' # 개별 테스트를 위해서 이렇게 값을 overriding
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
        
        # vm 생성
        self.vm2 = admin_vm(self.webDriver)
        self.vm2._vmName = self.vm2._vmName + '_2'
        self._vm2Name = self.vm2._vmName
        self.vm2.create()

        # 선호도 그룹
        self.affinityGroupCreate()
        self.affinityGroupUpdate()
        self.affinityGroupRemove()
        
        # 선호도 레이블
        self.affinityLabelCreate()
        self.affinityLabelUpdate()
        self.affinityLabelRemove()

        # 스냅샷
        self.snapshotCreate()
        self.restoreVMUsingSnapshot()
        self.vmCreateInSnapshot()
        self.snapshotRemove()

        # 내보내기
        self.exportToDomain()
        self.exportToHost()

        # # 가져오기
        self.importFromHost()

    def affinityGroupCreate(self):
        printLog(printSquare('Create Affinity Group'))
        result = FAIL
        msg = ''

        try:          
            self.setup()

            # 생성한 VM 이름 클릭
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)
            time.sleep(1)

            # 선호도 그룹 클릭
            try:
                self.webDriver.findElement('link_text', '선호도 그룹', True)
            except:
                self.webDriver.findElement('link_text', 'Affinity Groups', True)

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
            printLog("[VM AFFINITY GROUP CREATE] MESSAGE : " + msg)
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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)
            time.sleep(1)

            # 선호도 그룹 클릭
            try:
                self.webDriver.findElement('link_text', '선호도 그룹', True)
            except:
                self.webDriver.findElement('link_text', 'Affinity Groups', True)

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
            printLog("[VM AFFINITY GROUP UPDATE] MESSAGE : " + msg)
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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)
            time.sleep(1)

            # 선호도 그룹 클릭
            try:
                self.webDriver.findElement('link_text', '선호도 그룹', True)
            except:
                self.webDriver.findElement('link_text', 'Affinity Groups', True)

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
            printLog("[VM AFFINITY GROUP REMOVE] MESSAGE : " + msg)
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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)
            time.sleep(1)

            # 선호도 레이블 클릭
            try:
                self.webDriver.findElement('link_text', '선호도 레이블', True)
            except:
                self.webDriver.findElement('link_text', 'Affinity Labels', True)

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
            printLog("[VM AFFINITY LABEL CREATE] MESSAGE : " + msg)
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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)

            # 선호도 레이블 클릭
            try:
                self.webDriver.findElement('link_text', '선호도 레이블', True)
            except:
                self.webDriver.findElement('link_text', 'Affinity Labels', True)

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
            printLog("[VM AFFINITY LABEL UPDATE] MESSAGE : " + msg)
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
            try:
                self.webDriver.findElement('link_text', '선호도 레이블', True)
            except:
                self.webDriver.findElement('link_text', 'Affinity Labels', True)

            # 생성한 label의 이름 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Remove')
            self.webDriver.tableSearch(self._affinityLabelName + '_edited', 0, True)
            
            # 편집 버튼 클릭
            self.webDriver.findElement('id','DetailActionPanelView_Edit',True)
            time.sleep(1)
            
            # 팝업에서 VM - 클릭
            self.webDriver.findElement('css_selector', 'body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(4) > div:nth-child(1) > div > div > div > button:nth-child(2)', True)

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
            printLog("[VM AFFINITY LABEL REMOVE] MESSAGE : " + msg)
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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)

            # 스냅샷 클릭
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '스냅샷')
            self.webDriver.findElement('link_text', '스냅샷', True)
            time.sleep(1)

            # 생성 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)
            time.sleep(2)

            # 설명 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmSnapshotCreatePopupWidget_description')
            self.webDriver.findElement('id', 'VmSnapshotCreatePopupWidget_description', False)
            self.webDriver.sendKeys(self._snapshotName)

            # OK 클릭
            self.webDriver.findElement('id', 'VmSnapshotCreatePopupView_OnSave', True)
            time.sleep(10)

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
                    msg = 'Failed to create snapshot of %s'%self._vm2Name
                    if cnt == len(lis):
                        printLog("[VM SNAPSHOT CREATE] MESSAGE : " + msg)
                    continue
            
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM SNAPSHOT CREATE] MESSAGE : " + msg)

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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)

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
            printLog("[VM SNAPSHOT RESTORE VM] MESSAGE : " + msg)

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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)

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
            result, msg = self.webDriver.isChangedStatus('VM_for_%s'%self._snapshotName, 2, 13, ['이미지 잠김', 'Image locked', "Image Locked"], ['Down'], 300)

        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CREATE VM IN SNAPSHOT] MESSAGE : " + msg)

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
            self.webDriver.tableSearch(self._vm2Name, 2, False, True)

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
            printLog("[VM SNAPSHOT REMOVE] MESSAGE : " + msg)

        # 결과 출력
        printLog("[VM SNAPSHOT REMOVE] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'snapshot remove' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_SNAPSHOT_REMOVE',result, msg)
        
    def exportToDomain(self):
        # - 2-511 : 가상 머신을 데이터 도메인으로 내보내기 
          
        printLog(printSquare('Export vm to data domain'))
        result = FAIL
        msg = ''

        self._exportedVMName = self._vm2Name + '_exported'

        try:
            self.setup()

            # 생성한 VM 클릭
            self.webDriver.tableSearch(self._vm2Name, 2, True)

            # 내보내기 클릭
            self.webDriver.findElement('id', 'ActionPanelView_VmExport', True)
            time.sleep(2)

            self.webDriver.findElement('id', 'export-vm-name', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._exportedVMName)

            # 내보내기 버튼 클릭
            self.webDriver.findElement('xpath', '/html/body/div[4]/div/div/div/footer/button[1]', True)

            # 생성될 때 까지 대기
            st = time.time()
            while True:
                time.sleep(5)
                try:
                    if time.time() - st > 180:
                        result = FAIL
                        msg = 'Failed to data export(Timeout)'
                        printLog("[VM EXPORT TO DATA DOMAIN] MESSAGE : " + msg)
                        break

                    a = self.webDriver.tableSearch(self._exportedVMName, 2, False, False, True)
                    if a is not False:
                        result = PASS
                        msg = ''
                        break
                except:
                    continue

        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM EXPORT TO DATA DOMAIN] MESSAGE : " + msg)

        # 결과 출력
        printLog("[VM EXPORT TO DATA DOMAIN] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'export to data domain' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_EXPORT_TO_DATA_DOMAIN',result, msg)
        printLog("[VM EXPORT TO DATA DOMAIN] Wait 60 seconds ...")
        time.sleep(60)
        
    def exportToHost(self):
        # - 2-515 : 호스트에서 가상 머신 가져 오기
          
        printLog(printSquare('Export VM to host'))
        result = FAIL
        msg = ''

        try:
            self.setup()

            # 생성한 VM 클릭
            self.webDriver.tableSearch(self._vm2Name, 2, True)

            # 가져오기 클릭
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            time.sleep(1)
            self.webDriver.findElement('id', 'ActionPanelView_ExportOva', True)            
            time.sleep(5)

            # 호스트 선택
            self.webDriver.findElement('css_selector', '#ExportOvaWidget_proxy > div > button', True)
            self.selectDropdownMenu('css_selector', '#ExportOvaWidget_proxy > div > ul', ADMIN_HOSTNAME)

            # 경로 입력
            self.webDriver.findElement('id', 'ExportOvaWidget_path', True)
            self.webDriver.sendKeys('/root')

            # 이름 변경
            self.webDriver.findElement('id', 'ExportOvaWidget_name', True)
            self.webDriver.clear()
            self.webDriver.sendKeys('exported_%s.ova'%self._vm2Name)
            

            self.webDriver.findElement('css_selector', '#ExportOvaPopupView_OnExportOva > button', True)
            time.sleep(30)

            ssh_ = ssh_connection(ADMIN_HOST_IP, '22', ADMIN_HOST_ID, ADMIN_HOST_PW)
            ssh_.activate()

            # ssh 접속하여 ova 파일 생성되는지 확인
            st = time.time()
            printLog("[VM EXPORT TO HOST] Finding exported_%s.ova file ..."%self._vm2Name)
            while True:
                
                o, e = ssh_.commandExec('ls /root |grep %s'%self._vm2Name)
                if o == []:
                    continue

                elif o[0] == 'exported_%s.ova'%self._vm2Name:
                    result = PASS
                    msg = ''
                    break
                elif time.time() - st > 120:
                    result = FAIL
                    msg = 'Failed to export to host(timeout)'
                    printLog("[VM EXPORT TO HOST] MESSAGE : " + msg)

            ssh_.deactivate()

        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM EXPORT TO HOST] MESSAGE : " + msg)

        # 결과 출력
        printLog("[VM EXPORT TO HOST] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'export to host' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_EXPORT_TO_HOST',result, msg)
        printLog("[VM EXPORT TO HOST] Wait 30 seconds ...")
        time.sleep(30)
                
    def importFromHost(self):
        # - 2-515 : 호스트에서 가상 머신 가져 오기
          
        printLog(printSquare('Import VM from host'))
        result = FAIL
        msg = ''
        

        try:
            self.setup()

            # 생성한 VM 클릭
            self.webDriver.tableSearch(self._vm2Name, 2, True)

            # 가져오기 클릭
            self.webDriver.findElement('xpath', '/html/body/div[3]/div[4]/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[5]/button', True)
            time.sleep(0.3)
            self.webDriver.findElement('id', 'ActionPanelView_ImportVm', True)
            time.sleep(2)

            # 소스 메뉴 클릭
            sourceMenu = self.webDriver.findElement('css_selector_all', '#dropdownMenu')
            sourceMenu[1].click()
            time.sleep(.5)
            # 가상 어플라이언스 클릭
            self.selectDropdownMenu('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div/div/div/ul', '가상 어플라이언스 (OVA)')
            time.sleep(1)

            # 호스트 메뉴 클릭
            sourceMenu[6].click()
            # admin 호스트 클릭
            self.selectDropdownMenu('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div[1]/div/div[1]/div/div/div/ul', ADMIN_HOSTNAME)

            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div[2]/div[2]/div[1]/div/input', True)
            self.webDriver.sendKeys('/root')

            # 로드 클릭
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[5]/div[3]/div/div/button', True)
            time.sleep(15)

            # 가상머신 클릭
            vmTable = self.webDriver.findElement('css_selector_all', 'tbody')[1]
            for tr in vmTable.find_elements_by_tag_name('tr'):
                td = tr.find_elements_by_tag_name('td')
                if 'exported_%s.ova'%self._vm2Name in td[1].text:
                    td[0].click()
                    break

            # 화살표 버튼 클릭 후 OK
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[9]/div/div/div[4]/table/tbody/tr/td/table/tbody/tr[1]/td/div/div/img', True)
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[3]/div[1]/div[2]/button', True)

            time.sleep(3)

            copyVMTables = self.webDriver.findElement('css_selector_all', 'tbody')
            copyVMTable = copyVMTables[len(copyVMTables)-1]
            for tr in copyVMTable.find_elements_by_tag_name('tr'):
                td = tr.find_elements_by_tag_name('td')
                if self._vm2Name == td[1].text:
                    tr.click()
                    clicked = True
                    time.sleep(.5)
                    break

            if clicked == True:
                self.webDriver.findElement('xpath' ,'/html/body/div[5]/div/div/div/div[2]/div/div/table/tbody/tr[4]/td/div/div[2]/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/input')
                self.webDriver.clear()
                self.webDriver.sendKeys('from_host_%s'%self._vm2Name)
                
                self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[3]/div[1]/div[3]/button', True)
                time.sleep(2)

                isCreated = self.webDriver.tableSearch('from_host_%s'%self._vm2Name, 2, False, False, True)
                if isCreated == False:
                    result = FAIL
                    msg = 'Failed to import from host'
                    printLog("[VM IMPORT FROM HOST] MESSAGE : " + msg)
                else:
                    result = PASS
                    msg = ''

            else:
                result = FAIL
                msg = 'Failed to import from host'
                printLog("[VM IMPORT FROM HOST] MESSAGE : " + msg)


        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM IMPORT FROM HOST] MESSAGE : " + msg)


        # ova 파일 삭제        
        ssh_ = ssh_connection(ADMIN_HOST_IP, '22', ADMIN_HOST_ID, ADMIN_HOST_PW)
        ssh_.activate()
        ssh_.commandExec('rm -rf /root/exported_%s.ova'%self._vm2Name)
        ssh_.deactivate()


        # 결과 출력
        printLog("[VM IMPORT FROM HOST] RESULT : " + result)
        self._vm2Result.append(['vm' + DELIM + 'import from host' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('VM_IMPORT_FROM_HOST',result, msg)
        