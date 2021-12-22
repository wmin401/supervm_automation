    def qosCreate(self):    
        printLog(printSquare('Qos Create'))
        result = FAIL
        msg = ''

        try:

            self.webDriver.explicitlyWait(10, By.ID, 'WelcomePage_webadmin')
            self.webDriver.findElement('id', 'WelcomePage_webadmin', True)

            self.webDriver.explicitlyWait(10, By.ID, 'username')
            self.webDriver.findElement('id', 'username', True)

            self.webDriver.explicitlyWait(10, By.ID, 'username')
            self.webDriver.findElement('id', 'username', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            self.webDriver.explicitlyWait(10, By.ID, 'password')
            self.webDriver.findElement('id', 'password', True)

            self.webDriver.explicitlyWait(10, By.ID, 'password')
            self.webDriver.findElement('id', 'password', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.pf-c-button')
            self.webDriver.findElement('css_selector', '.pf-c-button', True)

            self.webDriver.explicitlyWait(10, By.ID, 'compute')
            self.webDriver.findElement('id', 'compute', True)

            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_dataCentersAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_dataCentersAnchor > .list-group-item-value', True)

            self.webDriver.explicitlyWait(10, By.ID, 'MainDataCenterView_table_content_col2_row0')
            self.webDriver.findElement('id', 'MainDataCenterView_table_content_col2_row0', True)

            self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'QoS')
            self.webDriver.findElement('link_text', 'QoS', True)

            self.webDriver.explicitlyWait(10, By.ID, 'DetailActionPanelView_New')
            self.webDriver.findElement('id', 'DetailActionPanelView_New', True)

            self.webDriver.explicitlyWait(10, By.ID, 'QosPopupView_nameEditor')
            self.webDriver.findElement('id', 'QosPopupView_nameEditor', True)

            self.webDriver.explicitlyWait(10, By.ID, 'QosPopupView_nameEditor')
            self.webDriver.findElement('id', 'QosPopupView_nameEditor', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            self.webDriver.explicitlyWait(10, By.ID, 'QosPopupView_descriptionEditor')
            self.webDriver.findElement('id', 'QosPopupView_descriptionEditor', True)

            self.webDriver.explicitlyWait(10, By.ID, 'QosPopupView_descriptionEditor')
            self.webDriver.findElement('id', 'QosPopupView_descriptionEditor', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[QOS CREATE] " + msg)
            printLog("[QOS CREATE] RESULT : " + result)

        self._qosResult.append(['qos' + DELIM + 'create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('QOS_CREATE',result, msg)