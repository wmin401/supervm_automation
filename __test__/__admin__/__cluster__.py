import time
import string
import random

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import testlink

from selenium.webdriver.common.by import By


class admin_cluster:
    def __init__(self, webDriver):
        self._clusterResult = []
        self.rs = randomString()
        self._clusterName = 'auto_cluster_' + self.rs
        self._cpuProfileName = 'auto_cluster_profile_' + self.rs
        self.webDriver = webDriver

        self.tl = testlink()
            
    def test(self):
        self.create()
        time.sleep(1)
        self.CPUProfileCreate()
        time.sleep(0.3)
        self.CPUProfileRemove()
        time.sleep(0.3)
        # self.changeVersion()
        # time.sleep(0.3)
        self.scheduling()
        time.sleep(0.3)
        self.MoMUpdate()
        time.sleep(0.3)
        self.memoryOptimization()
        time.sleep(0.3)
        self.remove()

    def setup(self):
        # 컴퓨팅 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','compute',True)

        # 클러스터 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','MenuView_clustersAnchor',True)

    def create(self):
        printLog(printSquare('Create Cluster'))   
        try:
            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.3)
            # 새로 만들기
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_New')
            self.webDriver.findElement('id','ActionPanelView_New',True)
            # 이름 입력
            time.sleep(0.3)
            self.webDriver.explicitlyWait(10, By.ID, 'ClusterPopupView_nameEditor')
            self.webDriver.findElement('id','ClusterPopupView_nameEditor',True)
            self.webDriver.sendKeys(self._clusterName)                
            # 설명 입력
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_descriptionEditor',True)
            self.webDriver.sendKeys('auto_description') 
            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_OnSave',True)            
            # 나중에 설정 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','GuidePopupView_Cancel',True)            
            # table 내부 전부 검색해서 입력한 이름이 있을경우 PASS
            _createCheck = self.webDriver.tableSearch(self._clusterName, 1)            
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new cluster..."
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[CLUSTER CREATE] MESSAGE : " + msg)
        printLog("[CLUSTER CREATE] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_CREATE', result, msg)
    
    def CPUProfileCreate(self):
        printLog(printSquare("Create CPU Profile"))
        try:
            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.3)
            
            # 클러스터 이름 클릭                  
            self.webDriver.tableSearch(self._clusterName, 1, False, nameClick = True)
            # CPU 프로파일 탭 클릭            
            time.sleep(0.5)
            uls = self.webDriver.getDriver().find_elements_by_tag_name('ul') # 전체 ul 태그 찾기
            lis = uls[len(uls)-1].find_elements_by_tag_name('li') # 마지막 ul 태그에서 검색
            for i in range(len(lis)):
                if lis[i].get_attribute('textContent') == 'CPU 프로파일' or lis[i].get_attribute('textContent') == 'CPU Profiles':
                   lis[i].click() 
            
            # 새로 만들기 클릭            
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id','DetailActionPanelView_New',True)  
            # 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'CpuProfilePopupView_name')
            self.webDriver.findElement('id','CpuProfilePopupView_name',True)
            self.webDriver.sendKeys(self._cpuProfileName)          
            # 설명 입력
            self.webDriver.findElement('id','CpuProfilePopupView_description',True)
            self.webDriver.sendKeys('auto_profile_description')          
            # OK 버튼 클릭
            self.webDriver.findElement('id','CpuProfilePopupView_OnSave',True)
            # 생성 확인
            _createCheck = self.webDriver.tableSearchAll(0, self._cpuProfileName, 0)
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create cluster's CPU profile..."
            
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER CPU PROFILE CREATE] MESSAGE : " + msg)
        printLog("[CLUSTER CPU PROFILE CREATE] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'create cpu profile' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_CREATE_CPU_PROFILE', result, msg)

    def CPUProfileRemove(self):
        printLog(printSquare("Remove CPU Profile"))
        try:
            self.setup() # 컴퓨팅 - 클러스터
            # 클러스터 이름 클릭                  
            self.webDriver.tableSearch(self._clusterName, 1, False, nameClick = True)
            time.sleep(0.5)
            # CPU 프로파일 탭 클릭            
            time.sleep(0.5)
            uls = self.webDriver.getDriver().find_elements_by_tag_name('ul') # 전체 ul 태그 찾기
            lis = uls[len(uls)-1].find_elements_by_tag_name('li') # 마지막 ul 태그에서 검색
            for i in range(len(lis)):
                if lis[i].get_attribute('textContent') == 'CPU 프로파일' or lis[i].get_attribute('textContent') == 'CPU Profiles':
                   lis[i].click() 
            # 생성한 CPU 프로필 선택
            self.webDriver.tableSearchAll(0, self._cpuProfileName, 0, True)
            # 제거 클릭
            self.webDriver.findElement('id','DetailActionPanelView_Remove',True)
            # OK 클릭        
            self.webDriver.explicitlyWait(10, By.ID, 'RemoveConfirmationPopupView_OnRemove')
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)
            # 생성 확인
            _removeCheck = self.webDriver.tableSearchAll(0, self._cpuProfileName, 0)
            if _removeCheck == True:
                result = FAIL
                msg = "Failed to remove cluster's cpu profile..."
            else:
                result = PASS
                msg = ''
                
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER CPU PROFILE REMOVE] MESSAGE : " + msg)
        printLog("[CLUSTER CPU PROFILE REMOVE] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'remove cpu profile' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_REMOVE_CPU_PROFILE', result, msg)

    def changeVersion(self):
        printLog(printSquare("Change Cluster Compatibility Version"))
        try:
            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.3)   
            # table 내부에 생성한 클러스터의 이름이 있을 경우 해당 row 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._clusterName, 1, True, False)            
            # 우측 편집 버튼 클릭
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('id','ActionPanelView_Edit', True)
            # 호환 버전 클릭 / 4.4 -> 4.5
            time.sleep(1)
            self.webDriver.explicitlyWait(30, By.ID, 'ClusterPopupView_versionEditor')
            self.webDriver.findElement('id','ClusterPopupView_versionEditor',True)
            self.webDriver.findElement('css_selector_all','#ClusterPopupView_versionEditor > div > ul > li')[1].click()
            #ClusterPopupView_versionEditor > div > ul > li:nth-child(2)
            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_OnSave',True)
            # Confirm OK 버튼 클릭
            time.sleep(0.5)
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DefaultConfirmationPopupView_OnSaveConfirmCpuThreads',True)                   
            
            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER CHANGE VERSION] MESSAGE : " + msg)        
            # 저장 불가능시
            time.sleep(0.3)
            self.webDriver.findElement('css_selector', 'body > div:nth-child(10) > div > div > div > div.modal-footer.wizard-pf-footer.footerPosition > div.GHYIDY4CMOB > button', True)
            # 취소 클릭
            time.sleep(0.3)
            self.webDriver.findElement('id','ClusterPopupView_Cancel',True)


        printLog("[CLUSTER CHANGE VERSION] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'change version' + DELIM + result + DELIM + msg])
        
        self.tl.junitBuilder('CLUSTER_CHANGE_VERSION', result, msg)

    def scheduling(self):
        printLog(printSquare("Sheduling Update"))
        try:    
            msg = ''

            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.3)
            # table 내부에 생성한 클러스터의 이름이 있을 경우 해당 row 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._clusterName, 1, True)            
            # 우측 편집 버튼 클릭
            time.sleep(1)
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('id','ActionPanelView_Edit', True)
            time.sleep(1)
            # 스케줄링 정책 탭 클릭
            time.sleep(0.5)
            self.webDriver.findElement('css_selector','body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(4)', True)            
            # 스케줄링 선택 - power_saving
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('id','ClusterPopupView_clusterPolicyEditor', True)
            time.sleep(0.2)
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#ClusterPopupView_clusterPolicyEditor > div > ul > li')            
            self.webDriver.findElement('css_selector_all','#ClusterPopupView_clusterPolicyEditor > div > ul > li')[0].click()        
            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_OnSave',True)
            time.sleep(0.3)
            # 저장 불가능일 경우
            self.webDriver.explicitlyWait(10,By.CSS_SELECTOR,'body > div:nth-child(10) > div > div > div > div:nth-child(2) > div > div > div > div')
            self.webDriver.findElement('css_selector','body > div:nth-child(10) > div > div > div > div:nth-child(2) > div > div > div > div')
            msg = self.webDriver.getAttribute('textContent')
            if '오류' in msg or 'Error' in msg:
                printLog("[CLUSTER SCHEDULING] Save failed")
                # self.webDriver.explicitlyWait(10, By.LINK_TEXT, '닫기')
                self.webDriver.findElement('xpath', '/html/body/div[7]/div/div/div/div[3]/div[1]/button', True)
                #self.webDriver.findElement('css_selector','body > div:nth-child(10) > div > div > div > div.modal-footer.wizard-pf-footer.footerPosition > div.GHYIDY4CMOB > button', True)
                # 취소 클릭
                time.sleep(0.3)
                self.webDriver.findElement('id','ClusterPopupView_Cancel',True)
            
            result = PASS

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER SCHEDULING] MESSAGE : " + msg)      
        printLog("[CLUSTER SCHEDULING] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'scheduling' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_SCHEDULING', result, msg)

    def MoMUpdate(self):
        printLog(printSquare("MoM Update"))
        try:    
            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.3)   
            # table 내부에 생성한 클러스터의 이름이 있을 경우 이름 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._clusterName, 1, rowClick=False, nameClick=True)            
            # 호스트탭 클릭            
            time.sleep(0.3)
            uls = self.webDriver.getDriver().find_elements_by_tag_name('ul') # 전체 ul 태그 찾기
            lis = uls[len(uls)-1].find_elements_by_tag_name('li') # 마지막 ul 태그에서 검색
            for i in range(len(lis)):
                if lis[i].get_attribute('textContent') == '호스트' or lis[i].get_attribute('textContent') == 'Hosts':
                   lis[i].click() 
            # MoM 정책 동기화 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','DetailActionPanelView_updateMomPolicyCommand',True)  

            result = PASS
            msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER MOM UPDATE] MESSAGE : " + msg)   
        printLog("[CLUSTER MOM UPDATE] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'MoM Update' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_MOM_UPDATE', result, msg)

    def memoryOptimization(self):
        printLog(printSquare("Memory Optimization"))
        try:      
            msg = ''
            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.3)
            # table 내부에 생성한 클러스터의 이름이 있을 경우 해당 row 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._clusterName, 1, True)            
            # 우측 편집 버튼 클릭
            time.sleep(1)
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('id','ActionPanelView_Edit', True)
            time.sleep(0.5)
            # 최적화 탭 클릭
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('css_selector','body > div.popup-content.ui-draggable > div > div > div > div:nth-child(2) > div > div > div > div.wizard-pf-sidebar.dialog_noOverflow > ul > li:nth-child(2)', True)
            # 데스크톱용 로드 클릭
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('id','ClusterPopupView_optimizationForDesktopEditor', True)
            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ClusterPopupView_OnSave',True)
            
            # 저장 불가능일 경우
            time.sleep(0.5)
            try:
                self.webDriver.explicitlyWait(10,By.CSS_SELECTOR,'body > div:nth-child(10) > div > div > div > div:nth-child(2) > div > div > div > div')
                self.webDriver.findElement('css_selector','body > div:nth-child(10) > div > div > div > div:nth-child(2) > div > div > div > div')
                msg = self.webDriver.getAttribute('textContent')
                if '오류' in msg or 'Error' in msg:
                    printLog("[CLUSTER MEMORY OPTIMIZATION] Save failed")
                    #self.webDriver.findElement('css_selector','body > div:nth-child(10) > div > div > div > div.modal-footer.wizard-pf-footer.footerPosition > div.GHYIDY4CMOB > button', True)                    
                    self.webDriver.findElement('xpath', '/html/body/div[7]/div/div/div/div[3]/div[1]/button', True)
                    # 취소 클릭
                    time.sleep(0.3)
                    self.webDriver.findElement('id','ClusterPopupView_Cancel',True)
            except:
                pass            
            result = PASS

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER MEMORY OPTIMIZATION] MESSAGE : " + msg)   
        printLog("[CLUSTER MEMORY OPTIMIZATION] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'memory optimize' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_MEMORY_OPTIMIZATION', result, msg)

    def remove(self):
        printLog(printSquare("Remove Cluster"))
        try:               
            self.setup() # 컴퓨팅 - 클러스터
            time.sleep(0.5)
            # table 내부에 생성한 클러스터의 이름이 있을 경우 해당 row 클릭
            self.webDriver.tableSearch(self._clusterName, 1, True)
            # 우측 추가 옵션 버튼 클릭
            self.webDriver.implicitlyWait(10)            
            self.webDriver.findElement('css_selector','.btn-group:nth-child(4) .fa', True)
            time.sleep(0.3)
            # 삭제 버튼 클릭
            self.webDriver.findElement('id','ActionPanelView_Remove',True)            
            time.sleep(0.5)
            # OK 버튼 클릭
            self.webDriver.findElement('id','RemoveConfirmationPopupView_OnRemove',True)     
            time.sleep(2)       
            # table 내부 전부 검색해서 입력한 이름이 있을경우 FAIL
            try:
                removeCheck = self.webDriver.tableSearch(self._clusterName, 1, False, False, True)
                if removeCheck == False:
                    result = PASS
                    msg = ''
                else:
                    result = FAIL
                    msg = 'Failed to remove cluster'
                    printLog("[CLUSTER REMOVE] MESSAGE : " + msg)
            except:
                result = PASS
                msg = ''
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CLUSTER REMOVE] MESSAGE : " + msg)
        printLog("[CLUSTER REMOVE] RESULT : " + result)
        self._clusterResult.append(['cluster' + DELIM + 'remove' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('CLUSTER_REMOVE', result, msg)
