#-*- coding: utf-8 -*-

from time import sleep
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

class admin_quota:
    def __init__(self, webDriver):
        self._quotaResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        self._quotaName = 'TEST'
        self._changeName = 'change-name'
        self._memByte = '100'
        self._cpuByte = '100'
        self._storageByte = '200'
        self._memByte2 = '250'
        self._cpuByte2 = '250'
        self._storageByte2 = '150'
        self._vmName = 'TEST'
        self.tl = testlink()
          
    def test(self):
        self.quotaChange()
        self.quotaCreate()
        self.quotaTovm()
        self.quotaTodisk()
        self.quotaToconsumer()
        self.quotaEdit()
        self.quotaSettingcpu()
        self.quotaRemove()


    def quotaChange(self):    
        printLog(printSquare('Quota Change'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_dataCentersAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_dataCentersAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Edit')
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#DataCenterPopupView_quotaEnforceTypeEditor .filter-option')
            self.webDriver.findElement('css_selector', '#DataCenterPopupView_quotaEnforceTypeEditor .filter-option', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '강제 적용')
            self.webDriver.findElement('link_text', '강제 적용', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.list-group-item')
            self.webDriver.findElement('css_selector', '.list-group-item', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_quotasAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_quotasAnchor > .list-group-item-value', True)

            time.sleep(2)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA CHANGE] " + msg)
        printLog("[QUOTA CHANGE] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'change' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_CHANGE',result, msg)

    

    def quotaCreate(self):    
        printLog(printSquare('Quota Create'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '관리')
            self.webDriver.findElement('link_text', '관리', True)
            
            time.sleep(1)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_quotasAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_quotasAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Create')
            self.webDriver.findElement('id', 'ActionPanelView_Create', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'QuotaPopupView_nameEditor')
            self.webDriver.findElement('id', 'QuotaPopupView_nameEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'QuotaPopupView_nameEditor')
            self.webDriver.findElement('id', 'QuotaPopupView_nameEditor', False)
            self.webDriver.sendKeys(self._quotaName) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[7]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[5]/div/button')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[7]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[5]/div/button', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_specificMemRadioButtonEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_specificMemRadioButtonEditor', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_memValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_memValueEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_memValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_memValueEditor', False)
            self.webDriver.sendKeys(self._memByte) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_specificCpuRadioButtonEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_specificCpuRadioButtonEditor', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_cpuValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_cpuValueEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_cpuValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_cpuValueEditor', False)
            self.webDriver.sendKeys(self._cpuByte) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#EditQuotaClusterPopupView_OnEditClusterQuota > .btn')
            self.webDriver.findElement('css_selector', '#EditQuotaClusterPopupView_OnEditClusterQuota > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[11]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[4]/div/button')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[11]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[4]/div/button', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_specificStorageRadioButtonEditor')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_specificStorageRadioButtonEditor', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_storageValueEditor')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_storageValueEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_storageValueEditor')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_storageValueEditor', False)
            self.webDriver.sendKeys(self._storageByte) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_OnEditStorageQuota')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_OnEditStorageQuota', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'QuotaPopupView_OnCreateQuota')
            self.webDriver.findElement('id', 'QuotaPopupView_OnCreateQuota', True)

            time.sleep(2)

            _createCheck = self.webDriver.tableSearch(self._quotaName, 1)

            if _createCheck == True:
                result = PASS
                msg = ''
            else:
                result = FAIL
                msg = "Failed to create new quota..."

        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        
        printLog("[QUOTA CREATE] " + msg)
        printLog("[QUOTA CREATE] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_CREATE',result, msg)

    def quotaTovm(self):    
        printLog(printSquare('Quota to VM'))
        result = FAIL
        msg = ''

        try:
            self.vmCreate()
            time.sleep(5)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)
         
            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._vmName,2,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Edit')
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmPopupWidget_quota .combobox')
            self.webDriver.findElement('css_selector', '#VmPopupWidget_quota .combobox', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('css_selector','#VmPopupWidget_quota > div > input',True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._quotaName)

            time.sleep(1)         

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(2)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA TOVM] " + msg)
        printLog("[QUOTA TOVM] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'tovm' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_TOVM',result, msg)
    
    def quotaTodisk(self):    
        printLog(printSquare('Quota to Disk'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MainVirtualMachineView_table_content_col2_row1')
            self.webDriver.findElement('id', 'MainVirtualMachineView_table_content_col2_row1', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '디스크')
            self.webDriver.findElement('link_text', '디스크', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Edit')
            self.webDriver.findElement('id', 'DetailActionPanelView_Edit', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmDiskPopupWidget_quota .filter-option')
            self.webDriver.findElement('css_selector', '#VmDiskPopupWidget_quota .filter-option', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmDiskPopupWidget_quota > div > ul > li:nth-child(2)')
            self.webDriver.findElement('css_selector', '#VmDiskPopupWidget_quota > div > ul > li:nth-child(2)', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(3)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA TODISK] " + msg)
        printLog("[QUOTA TODISK] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'todisk' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_TODISK',result, msg)
    
    def quotaToconsumer(self):    
        printLog(printSquare('Quota Toconsumer'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '관리')
            self.webDriver.findElement('link_text', '관리', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_quotasAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_quotasAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MainQuotaView_table_content_col1_row1')
            self.webDriver.findElement('id', 'MainQuotaView_table_content_col1_row1', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '소비자')
            self.webDriver.findElement('link_text', '소비자', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_Add')
            self.webDriver.findElement('id', 'DetailActionPanelView_Add', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'PermissionsPopupView_searchString')
            self.webDriver.findElement('id', 'PermissionsPopupView_searchString', False)
            self.webDriver.sendKeys('admin') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#PermissionsPopupView_searchButton > .btn')
            self.webDriver.findElement('css_selector', '#PermissionsPopupView_searchButton > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[3]/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[1]/div/input')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[3]/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[1]/div/input', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(2)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA TOCONSUMER] " + msg)
        printLog("[QUOTA TOCONSUMER] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'toconsumer' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_TOCONSUMER',result, msg)


    def quotaEdit(self):    
        printLog(printSquare('Quota Edit'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.list-group-item')
            self.webDriver.findElement('css_selector', '.list-group-item', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '관리')
            self.webDriver.findElement('link_text', '관리', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_quotasAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_quotasAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._quotaName,1,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Edit')
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'QuotaPopupView_nameEditor')
            self.webDriver.findElement('id', 'QuotaPopupView_nameEditor', False)
            self.webDriver.clear()
            self.webDriver.sendKeys('change-name') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[7]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[5]/div/button')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[7]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[5]/div/button', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_specificMemRadioButtonEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_specificMemRadioButtonEditor', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_memValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_memValueEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_memValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_memValueEditor', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._memByte2) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_specificCpuRadioButtonEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_specificCpuRadioButtonEditor', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_cpuValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_cpuValueEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaClusterPopupView_cpuValueEditor')
            self.webDriver.findElement('id', 'EditQuotaClusterPopupView_cpuValueEditor', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._cpuByte2) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#EditQuotaClusterPopupView_OnEditClusterQuota > .btn')
            self.webDriver.findElement('css_selector', '#EditQuotaClusterPopupView_OnEditClusterQuota > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[11]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[4]/div/button')
            self.webDriver.findElement('xpath', '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[11]/div/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr/td[4]/div/button', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_specificStorageRadioButtonEditor')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_specificStorageRadioButtonEditor', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_storageValueEditor')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_storageValueEditor', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_storageValueEditor')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_storageValueEditor', True)
            self.webDriver.clear()
            self.webDriver.sendKeys(self._storageByte2) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'EditQuotaStoragePopupView_OnEditStorageQuota')
            self.webDriver.findElement('id', 'EditQuotaStoragePopupView_OnEditStorageQuota', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.popup-content')
            self.webDriver.findElement('css_selector', '.popup-content', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(2)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA EDIT] " + msg)
        printLog("[QUOTA EDIT] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'edit' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_EDIT',result, msg)

    def quotaSettingcpu(self):    
        printLog(printSquare('Quota Settingcpu'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._vmName,2,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Edit')
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupView_OnAdvanced')
            self.webDriver.findElement('id', 'VmPopupView_OnAdvanced', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '리소스 할당')
            self.webDriver.findElement('link_text', '리소스 할당', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmPopupWidget_cpuSharesAmountSelection .filter-option')
            self.webDriver.findElement('css_selector', '#VmPopupWidget_cpuSharesAmountSelection .filter-option', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '높음')
            self.webDriver.findElement('link_text', '높음', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(2)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA SETTINGCPU] " + msg)
        printLog("[QUOTA SETTINGCPU] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'settingcpu' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_SETTINGCPU',result, msg)

    def quotaRemove(self):    
        printLog(printSquare('Quota Remove'))
        result = FAIL
        msg = ''

        try:
            self.vmRemove()
            time.sleep(5)
            
            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '관리')
            self.webDriver.findElement('link_text', '관리', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_quotasAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_quotasAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._changeName,1,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Remove')
            self.webDriver.findElement('id', 'ActionPanelView_Remove', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
        
            time.sleep(2)

            _removeCheck = self.webDriver.tableSearch(self._changeName, 1)

            if _removeCheck == True:
                result = FAIL
                msg = 'Failed to remove new quota...'
            else:
                result = PASS
                msg = ''
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
        printLog("[QUOTA REMOVE] " + msg)
        printLog("[QUOTA REMOVE] RESULT : " + result)

        self._quotaResult.append(['quota' + DELIM + 'remove' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QUOTA_REMOVE',result, msg)

    def vmCreate(self):    
        printLog(printSquare('Vm Create'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_NewVm')
            self.webDriver.findElement('id', 'ActionPanelView_NewVm', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_name')
            self.webDriver.findElement('id', 'VmPopupWidget_name', False)
            self.webDriver.sendKeys(self._vmName) # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmPopupWidget_instanceImages__createEdit > .btn')
            self.webDriver.findElement('css_selector', '#VmPopupWidget_instanceImages__createEdit > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_size', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmDiskPopupWidget_size')
            self.webDriver.findElement('id', 'VmDiskPopupWidget_size', False)
            self.webDriver.sendKeys('10') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#VmDiskPopupView_OnSave > .btn')
            self.webDriver.findElement('css_selector', '#VmDiskPopupView_OnSave > .btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            time.sleep(10)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM CREATE] " + msg)
            printLog("[VM CREATE] RESULT : " + result)


    def vmRemove(self):    
        printLog(printSquare('Vm Remove'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            self.webDriver.implicitlyWait(10)
            self.webDriver.tableSearch(self._vmName,2,True,False)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button')
            self.webDriver.findElement('css_selector', 'body > div.GB10KEXCJUB > div.container-pf-nav-pf-vertical > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.toolbar-pf-actions > div:nth-child(2) > div.btn-group.dropdown-kebab-pf.dropdown.pull-right > button', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '삭제')
            self.webDriver.findElement('link_text', '삭제', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
           
            time.sleep(10)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REMOVE] " + msg)
            printLog("[VM REMOVE] RESULT : " + result)