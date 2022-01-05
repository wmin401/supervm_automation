import time

from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__csv__ import *
from __common__.__testlink__ import *

from selenium.webdriver.common.by import By

'''
    Cloud Service 팀 내 vSphere 환경 기준 작성

    작성자 : CQA2 김정현
'''

class admin_external_provider:
    def __init__(self, webDriver):
        self._externalProviderResult = []
        self.webDriver = webDriver
        self._externalProviderName = 'auto_external_provider_'+randomString()
        self._externalProviderDescription = 'auto_external_provider_'+randomString()
        self._type = '' # 환경에 따라 수정 필요
        self._superVmDatacenter = '' # 환경에 따라 수정 필요
        self._vCenterIp = '' # 환경에 따라 수정 필요
        self._esxiIp = '' # 환경에 따라 수정 필요
        self._externalProviderDatacenter = '' # 환경에 따라 수정 필요
        self._proxyHost = '' # 환경에 따라 수정 필요
        self._userName = '' # 환경에 따라 수정 필요
        self._userPassword = '' # 환경에 따라 수정 필요
        self._editedExternalProviderDescription = 'auto_external_provider_edited_'+randomString()
        self.tl = testlink()

    def test(self):
        self.setup()
        self.create()
        time.sleep(3) # 생성 대기 필요
        self.edit()
        time.sleep(3) # 수정 대기 필요
        self.delete()

    def setup(self):
        # 외부 공급자 메뉴 접근

        # 관리 클릭
        printLog("[SETUP] Administration - Provider")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('xpath','/html/body/div[3]/div[3]/div/ul/li[5]/a/span[2]',True)
        time.sleep(2)

        # 공급자 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_providersAnchor')
        self.webDriver.findElement('id','MenuView_providersAnchor',True)

        time.sleep(2)

    def create(self):
        printLog(printSquare('Create External Provider'))
        result = FAIL
        msg = ''

        try:
            # 추가 버튼 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Add')
            self.webDriver.findElement('id', 'ActionPanelView_Add', True)

            # 외부 공급자 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'ProviderPopupView_nameEditor')
            self.webDriver.findElement('id', 'ProviderPopupView_nameEditor', False)
            self.webDriver.sendKeys(self._externalProviderName)

            # 외부 공급자 설명 입력
            self.webDriver.explicitlyWait(10, By.ID, 'ProviderPopupView_descriptionEditor')
            self.webDriver.findElement('id', 'ProviderPopupView_descriptionEditor', False)
            self.webDriver.sendKeys(self._externalProviderDescription) # You have to change this you want to write

            # 유형 - VMware 선택
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#ProviderPopupView_typeEditor .filter-option')
            self.webDriver.findElement('css_selector', '#ProviderPopupView_typeEditor .filter-option', True)
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, self._type)
            self.webDriver.findElement('link_text', self._type, True)

            # SuperVM 데이터 센터 - Default 선택
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#ProviderPopupView_datacenterEditor .filter-option')
            self.webDriver.findElement('css_selector', '#ProviderPopupView_datacenterEditor .filter-option', True)
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, self._superVmDatacenter)
            self.webDriver.findElement('link_text', self._superVmDatacenter, True)

            # vCenter IP 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmwarePropertiesWidget_vCenter')
            self.webDriver.findElement('id', 'VmwarePropertiesWidget_vCenter', False)
            self.webDriver.sendKeys(self._vCenterIp)

            # ESXi IP 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmwarePropertiesWidget_esx')
            self.webDriver.findElement('id', 'VmwarePropertiesWidget_esx', False)
            self.webDriver.sendKeys(self._esxiIp)

            # 외부 공급자 데이터 센터 입력
            self.webDriver.explicitlyWait(10, By.ID, 'VmwarePropertiesWidget_vmwareDatacenter')
            self.webDriver.findElement('id', 'VmwarePropertiesWidget_vmwareDatacenter', False)
            self.webDriver.sendKeys(self._externalProviderDatacenter)

            # 서버 SSL 인증서 확인 여부 체크 해제
            self.webDriver.explicitlyWait(10, By.ID, 'VmwarePropertiesWidget_verifySSLEditor')
            self.webDriver.findElement('id', 'VmwarePropertiesWidget_verifySSLEditor', True)

            # 프록시 호스트 선택
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmwarePropertiesWidget_proxyHost .filter-option')
            self.webDriver.findElement('css_selector', '#VmwarePropertiesWidget_proxyHost .filter-option', True)
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, self._proxyHost)
            self.webDriver.findElement('link_text', self._proxyHost, True)

            # 사용자 이름 입력
            self.webDriver.explicitlyWait(10, By.ID, 'ProviderPopupView_usernameEditor')
            self.webDriver.findElement('id', 'ProviderPopupView_usernameEditor', False)
            self.webDriver.sendKeys(self._userName)

            # 암호 입력
            self.webDriver.explicitlyWait(10, By.ID, 'ProviderPopupView_passwordEditor')
            self.webDriver.findElement('id', 'ProviderPopupView_passwordEditor', False)
            self.webDriver.sendKeys(self._userPassword)

            # OK 버튼 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            # 외부 공급자 이름으로 검색했을 때 확인되면 성공
            _createCheck = self.webDriver.tableSearch(self._externalProviderName, 0)
            printLog("[CREATE EXTERNAL PROVIDER] Check if created")
            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new external provider..."

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CREATE EXTERNAL PROVIDER] " + msg)
        printLog("[CREATE EXTERNAL PROVIDER] RESULT : " + result)

        self._externalProviderResult.append(['external' + DELIM + 'provider' + DELIM + 'create' + DELIM + result + DELIM + msg])
        self.tl.junitBuilder('CREATE_EXTERNAL_PROVIDER',result, msg)

    def edit(self):
        printLog(printSquare('Edit External Provider'))
        result = FAIL
        msg = ''

        try:
            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._externalProviderName, 0, rowClick=True)

            # 편집 버튼 클릭
            time.sleep(1)
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Edit')
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # 설명 수정
            self.webDriver.explicitlyWait(10, By.ID, 'ProviderPopupView_descriptionEditor')
            self.webDriver.findElement('id', 'ProviderPopupView_descriptionEditor', False)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._editedExternalProviderDescription)

            # OK 버튼 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            # 설명으로 검색했을 때 확인되면 성공
            _editCheck = self.webDriver.tableSearch(self._editedExternalProviderDescription, 2)
            printLog("[EDIT EXTERNAL PROVIDER] Check if edited")
            if _editCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to edit new external provider..."

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[EDIT EXTERNAL PROVIDER] " + msg)
        printLog("[EDIT EXTERNAL PROVIDER] RESULT : " + result)

        self._externalProviderResult.append(['edit' + DELIM + 'external' + DELIM + 'provider' + DELIM + result + DELIM + msg])
        self.tl.junitBuilder('EDIT_EXTERNAL_PROVIDER',result, msg)

    def delete(self):
        printLog(printSquare('Delete External Provider'))
        result = FAIL
        msg = ''

        try:
            # table 내부 전부 검색해서 입력한 이름이 있을경우 클릭
            time.sleep(0.5)
            self.webDriver.tableSearch(self._externalProviderName, 0, rowClick=True)

            # 삭제 버튼 클릭
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Remove')
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

            # OK 버튼 클릭
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            # 설명으로 검색했을 때 없으면 성공
            # _deleteCheck = self.webDriver.tableSearch(self._externalProviderName, 0)
            # printLog("[DELETE EXTERNAL PROVIDER] Check if deleted")
            # if _deleteCheck == False:
            #     result = PASS
            #     msg = ''
            # else:
            #     result = FAIL
            #     msg = "Failed to delete new external provider..."

            printLog("[DELETE EXTERNAL PROVIDER] Check if deleted")
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    _deleteCheck = self.webDriver.tableSearch(self._externalProviderName, 0)
                    if _deleteCheck == False:
                        result = PASS
                        msg = ''
                        break
                    else:
                        printLog("[DELETE EXTERNAL PROVIDER] Pools status is still deleted ...")
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[DELETE EXTERNAL PROVIDER] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to new external provider..."
                            break
                        else:
                            continue
                except:
                    continue
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[DELETE EXTERNAL PROVIDER] " + msg)
        printLog("[DELETE EXTERNAL PROVIDER] RESULT : " + result)

        self._externalProviderResult.append(['delete' + DELIM + 'external' + DELIM + 'provider' + DELIM + result + DELIM + msg])
        self.tl.junitBuilder('DELETE_EXTERNAL_PROVIDER',result, msg)
