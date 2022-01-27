
### Copy below function to your class ###


    def templateCreate(self):    
        printLog(printSquare('Template Create'))
        result = FAIL
        msg = ''

        try:

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#compute > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#compute > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_vmsAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_vmsAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#gwt-uid-278 > div')
            self.webDriver.findElement('css_selector', '#gwt-uid-278 > div', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-group')
            self.webDriver.findElement('css_selector', '.btn-group', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, '템플릿 생성')
            self.webDriver.findElement('link_text', '템플릿 생성', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'VmMakeTemplatePopupWidget_name')
            self.webDriver.findElement('id', 'VmMakeTemplatePopupWidget_name', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'VmMakeTemplatePopupWidget_name')
            self.webDriver.findElement('id', 'VmMakeTemplatePopupWidget_name', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-primary')
            self.webDriver.findElement('css_selector', '.btn-primary', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#compute > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#compute > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '#MenuView_templatesAnchor > .list-group-item-value')
            self.webDriver.findElement('css_selector', '#MenuView_templatesAnchor > .list-group-item-value', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'MainTemplateView_table_content_col1_row1')
            self.webDriver.findElement('id', 'MainTemplateView_table_content_col1_row1', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[TEMPLATE CREATE] " + msg)

        # 결과 출력
        printLog("[TEMPLATE CREATE] RESULT : " + result)
        self._templateResult.append(['template' + DELIM + 'create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('TEMPLATE_CREATE',result, msg)