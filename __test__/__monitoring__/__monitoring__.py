from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

class monitoring_monitoring: # 모두 소문자
    def __init__(self, webDriver):
        printLog("* 모니터링 테스트 시작")
        self._monitoringResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        # self._sampleName = 'auto_sample_'+randomString() # 필요할 경우 사용
        self.tl = testlink()

    def test(self):

        self.createAccount()


    def createAccount(self):    
        printLog(printSquare('Test'))
        result = FAIL
        msg = ''

        # try:

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'user')
        #     self.webDriver.findElement('name', 'user', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'password')
        #     self.webDriver.findElement('name', 'password', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1daj7gy-button')
        #     self.webDriver.findElement('css_selector', '.css-1daj7gy-button', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.sidemenu-item')
        #     self.webDriver.findElement('css_selector', '.sidemenu-item', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
        #     self.webDriver.findElement('link_text', 'Users', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.sidemenu-item')
        #     self.webDriver.findElement('css_selector', '.sidemenu-item', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
        #     self.webDriver.findElement('link_text', 'Users', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
        #     self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.NAME, 'name')
        #     self.webDriver.findElement('name', 'name', True)

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'name')
        #     self.webDriver.findElement('name', 'name', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.NAME, 'email')
        #     self.webDriver.findElement('name', 'email', True)

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'email')
        #     self.webDriver.findElement('name', 'email', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'login')
        #     self.webDriver.findElement('name', 'login', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.NAME, 'password')
        #     self.webDriver.findElement('name', 'password', True)

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'password')
        #     self.webDriver.findElement('name', 'password', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
        #     self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)

        #     # click
        #     self.webDriver.explicitlyWait(10, By.NAME, 'name')
        #     self.webDriver.findElement('name', 'name', True)

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'name')
        #     self.webDriver.findElement('name', 'name', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.NAME, 'email')
        #     self.webDriver.findElement('name', 'email', True)

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'email')
        #     self.webDriver.findElement('name', 'email', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.NAME, 'login')
        #     self.webDriver.findElement('name', 'login', True)

        #     # type
        #     self.webDriver.explicitlyWait(10, By.NAME, 'login')
        #     self.webDriver.findElement('name', 'login', False)
        #     self.webDriver.sendKeys('') # You have to change this you want to write

        #     # click
        #     self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
        #     self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)
   
        # except Exception as e:   
        #     result = FAIL
        #     msg = str(e).replace("\n",'')
        #     msg = msg[:msg.find('Element <')]
        #     printLog("[TEST] " + msg)

        # # 결과 출력
        # printLog("[TEST] RESULT : " + result)
        # self._testResult.append(['monitoring' + DELIM + 'create account' + DELIM + result + DELIM + msg])        
        # self.tl.junitBuilder('TEST',result, msg)
