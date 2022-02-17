
### Copy below function to your class ###


    def test(self):    
        printLog(printSquare('Test'))
        result = FAIL
        msg = ''

        try:

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'user')
            self.webDriver.findElement('name', 'user', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'password')
            self.webDriver.findElement('name', 'password', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1daj7gy-button')
            self.webDriver.findElement('css_selector', '.css-1daj7gy-button', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.sidemenu-item')
            self.webDriver.findElement('css_selector', '.sidemenu-item', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
            self.webDriver.findElement('link_text', 'Users', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.sidemenu-item')
            self.webDriver.findElement('css_selector', '.sidemenu-item', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
            self.webDriver.findElement('link_text', 'Users', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
            self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'name')
            self.webDriver.findElement('name', 'name', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'name')
            self.webDriver.findElement('name', 'name', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'email')
            self.webDriver.findElement('name', 'email', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'email')
            self.webDriver.findElement('name', 'email', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'login')
            self.webDriver.findElement('name', 'login', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'password')
            self.webDriver.findElement('name', 'password', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'password')
            self.webDriver.findElement('name', 'password', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
            self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'name')
            self.webDriver.findElement('name', 'name', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'name')
            self.webDriver.findElement('name', 'name', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'email')
            self.webDriver.findElement('name', 'email', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'email')
            self.webDriver.findElement('name', 'email', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'login')
            self.webDriver.findElement('name', 'login', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'login')
            self.webDriver.findElement('name', 'login', False)
            self.webDriver.sendKeys('') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
            self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)
   
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[TEST] " + msg)

        # 결과 출력
        printLog("[TEST] RESULT : " + result)
        self._testResult.append(['test' + DELIM + '' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('TEST',result, msg)