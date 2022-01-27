
### Copy below function to your class ###


    def create(self):    
        printLog(printSquare('Create'))
        result = FAIL
        msg = ''

        try:

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'route-add-vm-button')
            self.webDriver.findElement('id', 'route-add-vm-button', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-name-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-name-edit', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-name-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-name-edit', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-description-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-description-edit', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-description-edit')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-description-edit', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-cluster-edit-button-text')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-cluster-edit-button-text', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-cluster-edit-item-Default (Default)')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-cluster-edit-item-Default (Default)', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-provision-edit-button-text')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-provision-edit-button-text', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-provision-edit-item-템플릿')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-provision-edit-item-템플릿', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-template-edit-button-text')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-template-edit-button-text', True)

            # click
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizard-basic-template-edit-item-Blank')
            self.webDriver.findElement('id', 'create-vm-wizard-basic-template-edit-item-Blank', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn')
            self.webDriver.findElement('css_selector', '.btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-lg')
            self.webDriver.findElement('css_selector', '.btn-lg', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn')
            self.webDriver.findElement('css_selector', '.btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn-lg')
            self.webDriver.findElement('css_selector', '.btn-lg', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'tbody > .editing')
            self.webDriver.findElement('css_selector', 'tbody > .editing', True)

            # type
            self.webDriver.explicitlyWait(10, By.ID, 'create-vm-wizards-storage-undefined-size-edit')
            self.webDriver.findElement('id', 'create-vm-wizards-storage-undefined-size-edit', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn')
            self.webDriver.findElement('css_selector', '.btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn')
            self.webDriver.findElement('css_selector', '.btn', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.btn')
            self.webDriver.findElement('css_selector', '.btn', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[CREATE] " + msg)

        # 결과 출력
        printLog("[CREATE] RESULT : " + result)
        self._createResult.append(['create' + DELIM + '' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('CREATE',result, msg)