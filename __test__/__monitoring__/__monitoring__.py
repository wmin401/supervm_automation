from calendar import c
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

        self.monitoringLogin()
        self.monitoringCreate()
        self.monitoringDelete()


    # def createAccount(self):    
    #     printLog(printSquare('Test'))
    #     result = FAIL
    #     msg = ''


    def monitoringLogin(self):
        printLog(printSquare('Grafana Login'))
        result = FAIL
        msg = ''

        try:
              # click Grafana Login
            self.webDriver.explicitlyWait(10, By.NAME, 'user')
            self.webDriver.findElement('name', 'user', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'user')
            self.webDriver.findElement('name', 'user', True)
            self.webDriver.sendKeys('admin') # You have to change this you want to write

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'password')
            self.webDriver.findElement('name', 'password', True)
            self.webDriver.sendKeys('asdf') # You have to change this you want to write

            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > div > div > react-container > div > div > div.css-9h8xxw > div > div.css-lcb2lo > form > button' )
            self.webDriver.findElement('css_selector', 'body > grafana-app > div > div > react-container > div > div > div.css-9h8xxw > div > div.css-lcb2lo > form > button', True)

            result = PASS
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[MONITORING_LOGIN] " + msg)

        printLog("[MONITORING_LOGIN] RESULT : " + result)
        self._monitoringResult.append(['monitoring' + DELIM + 'login' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('MONITORING_LOGIN',result, msg)

    def monitoringCreate(self):
        printLog(printSquare('Grafana Create'))
        result = FAIL
        msg = ''

        try:
            # click 사이드 탭에서 User 선택
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > a > span > div > svg')
            self.webDriver.findElement('css_selector', 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > a > span > div > svg', True)

            # click User 생성
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > ul > li:nth-child(2) > a')
            self.webDriver.findElement('css_selector', 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > ul > li:nth-child(2) > a', True)

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
            self.webDriver.findElement('name', 'name', True)
            self.webDriver.sendKeys('test2') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'email')
            self.webDriver.findElement('name', 'email', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'email')
            self.webDriver.findElement('name', 'email', True)
            self.webDriver.sendKeys('test2@gmail.com') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'login')
            self.webDriver.findElement('name', 'login', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'login')
            self.webDriver.findElement('name', 'login', True)
            self.webDriver.sendKeys('test2') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.NAME, 'password')
            self.webDriver.findElement('name', 'password', True)

            # type
            self.webDriver.explicitlyWait(10, By.NAME, 'password')
            self.webDriver.findElement('name', 'password', True)
            self.webDriver.sendKeys('asdf') # You have to change this you want to write

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > form > button')
            self.webDriver.findElement('css_selector', 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > form > button', True)

            result = PASS
        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[MONITORING_CREATE] " + msg)

        printLog("[MONITORING_CREATE] RESULT : " + result)
        self._monitoringResult.append(['monitoring' + DELIM + 'create' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('MONITORING_CREATE',result, msg)

    def monitoringDelete(self):
        printLog(printSquare('Grafana Delete'))
        result = FAIL
        msg = ''

        try:
            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(6) > a > span > div')
            self.webDriver.findElement('css_selector', 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(6) > a > span > div', True)

            # click
            self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
            self.webDriver.findElement('link_text', 'Users', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > div.css-66nrdr-vertical-group > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(7) > button')
            self.webDriver.findElement('css_selector', 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > div.css-66nrdr-vertical-group > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(7) > button', True)

            # click
            self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div > div > div.css-1fnwz84 > div.css-46jqiz > div > div.css-1rmaa0w-horizontal-group > div:nth-child(1) > button')
            self.webDriver.findElement('css_selector', 'body > div > div > div.css-1fnwz84 > div.css-46jqiz > div > div.css-1rmaa0w-horizontal-group > div:nth-child(1) > button', True)
            
            result = PASS

        except Exception as e:   
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[MONITORING_DELETE] " + msg)

        printLog("[MONITORING_DELETE] RESULT : " + result)
        self._monitoringResult.append(['monitoring' + DELIM + 'delete' + DELIM + result + DELIM + msg])        
        self.tl.junitBuilder('MONITORING_DELETE',result, msg)

    # def monitoringPortal(self):    
    #     printLog(printSquare('Monitoring Portal'))
    #     result = FAIL
    #     msg = ''

    #     try:

    #         # click Grafana Login
    #         self.webDriver.explicitlyWait(10, By.NAME, 'user')
    #         self.webDriver.findElement('name', 'user', True)

    #         # type
    #         self.webDriver.explicitlyWait(10, By.NAME, 'user')
    #         self.webDriver.findElement('name', 'user', True)
    #         self.webDriver.sendKeys('admin') # You have to change this you want to write

    #         # type
    #         self.webDriver.explicitlyWait(10, By.NAME, 'password')
    #         self.webDriver.findElement('name', 'password', True)
    #         self.webDriver.sendKeys('asdf') # You have to change this you want to write

    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > div > div > react-container > div > div > div.css-9h8xxw > div > div.css-lcb2lo > form > button' )
    #         self.webDriver.findElement('css_selector', 'body > grafana-app > div > div > react-container > div > div > div.css-9h8xxw > div > div.css-lcb2lo > form > button', True)

    #         # click 사이드 탭에서 User 선택
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > a > span > div > svg')
    #         self.webDriver.findElement('css_selector', 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > a > span > div > svg', True)

    #         # click User 생성
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > ul > li:nth-child(2) > a')
    #         self.webDriver.findElement('css_selector', 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(7) > ul > li:nth-child(2) > a', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
    #         self.webDriver.findElement('link_text', 'Users', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, '.css-1mhnkuh')
    #         self.webDriver.findElement('css_selector', '.css-1mhnkuh', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.NAME, 'name')
    #         self.webDriver.findElement('name', 'name', True)

    #         # type
    #         self.webDriver.explicitlyWait(10, By.NAME, 'name')
    #         self.webDriver.findElement('name', 'name', True)
    #         self.webDriver.sendKeys('test2') # You have to change this you want to write

    #         # click
    #         self.webDriver.explicitlyWait(10, By.NAME, 'email')
    #         self.webDriver.findElement('name', 'email', True)

    #         # type
    #         self.webDriver.explicitlyWait(10, By.NAME, 'email')
    #         self.webDriver.findElement('name', 'email', True)
    #         self.webDriver.sendKeys('test2@gmail.com') # You have to change this you want to write

    #         # click
    #         self.webDriver.explicitlyWait(10, By.NAME, 'login')
    #         self.webDriver.findElement('name', 'login', True)

    #         # type
    #         self.webDriver.explicitlyWait(10, By.NAME, 'login')
    #         self.webDriver.findElement('name', 'login', True)
    #         self.webDriver.sendKeys('test2') # You have to change this you want to write

    #         # click
    #         self.webDriver.explicitlyWait(10, By.NAME, 'password')
    #         self.webDriver.findElement('name', 'password', True)

    #         # type
    #         self.webDriver.explicitlyWait(10, By.NAME, 'password')
    #         self.webDriver.findElement('name', 'password', True)
    #         self.webDriver.sendKeys('asdf') # You have to change this you want to write

    #         # click
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > form > button')
    #         self.webDriver.findElement('css_selector', 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > form > button', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(6) > a > span > div')
    #         self.webDriver.findElement('css_selector', 'body > grafana-app > sidemenu > div.sidemenu__top > div:nth-child(6) > a > span > div', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.LINK_TEXT, 'Users')
    #         self.webDriver.findElement('link_text', 'Users', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > div.css-66nrdr-vertical-group > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(7) > button')
    #         self.webDriver.findElement('css_selector', 'body > grafana-app > div > div > react-container > div > div > div.scrollbar-view > div > div.page-container.page-body > div.css-66nrdr-vertical-group > div:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(7) > button', True)

    #         # click
    #         self.webDriver.explicitlyWait(10, By.CSS_SELECTOR, 'body > div > div > div.css-1fnwz84 > div.css-46jqiz > div > div.css-1rmaa0w-horizontal-group > div:nth-child(1) > button')
    #         self.webDriver.findElement('css_selector', 'body > div > div > div.css-1fnwz84 > div.css-46jqiz > div > div.css-1rmaa0w-horizontal-group > div:nth-child(1) > button', True)
    #         result = PASS
    #     except Exception as e:   
    #         result = FAIL
    #         msg = str(e).replace("\n",'')
    #         msg = msg[:msg.find('Element <')]
    #         printLog("[MONITORING PORTAL] " + msg)

    #     # 결과 출력
    #     printLog("[MONITORING PORTAL] RESULT : " + result)
    #     self._monitoringResult.append(['monitoring' + DELIM + 'portal' + DELIM + result + DELIM + msg])        
    #     self.tl.junitBuilder('MONITORING_PORTAL',result, msg)