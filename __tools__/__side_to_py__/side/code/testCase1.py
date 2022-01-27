
### Copy below function to your class ###


    def testCase1(self):    
        printLog(printSquare('Test Case1'))
        result = FAIL
        msg = ''

        try:

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'sso-dropdown-toggle')
            self.webDriver.findElement('id', 'sso-dropdown-toggle', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '로그인')
            self.webDriver.findElement('link_text', '로그인', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'username')
            self.webDriver.findElement('id', 'username', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'password')
            self.webDriver.findElement('id', 'password', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.pf-c-button')
            self.webDriver.findElement('css_selector', '.pf-c-button', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'WelcomePage_webadmin')
            self.webDriver.findElement('id', 'WelcomePage_webadmin', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#compute > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#compute > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'gwt-uid-286')
            self.webDriver.findElement('id', 'gwt-uid-286', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.toolbar-pf-actions > .form-group')
            self.webDriver.findElement('css_selector', '.toolbar-pf-actions > .form-group', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'ActionPanelView_Edit')
            self.webDriver.findElement('id', 'ActionPanelView_Edit', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_description')
            self.webDriver.findElement('id', 'VmPopupWidget_description', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmPopupWidget_description')
            self.webDriver.findElement('id', 'VmPopupWidget_description', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[TEST CASE1] " + msg)

        # 결과 출력
        printLog("[TEST CASE1] RESULT : " + result)
        self._testResult.append(['test' + DELIM + 'case1' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('TEST_CASE1',result, msg)