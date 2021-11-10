# -*- encoding= utf-8 -*-
import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


## 변수명 snake_case
## 함수명 camelCase

class SuperVM_driver:

    def __init__(self, headless = False):
        self.BROWSER_NAME = BROWSER_NAME.lower()
        self.BROWSER_VERSION = str(BROWSER_VERSION)
        self.BROWSER_BIT = str(BROWSER_BIT)
        self.headless = headless

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        if self.headless == True:
            options.add_argument('--headless')
            #options.add_argument('window-size=1920x1080')
            options.add_argument('--no-sandbox')
            #options.add_argument("disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
        try:
            if self.BROWSER_NAME == 'firefox':
                print('driver/firefox/' + str(self.BROWSER_VERSION) + '/' + self.BROWSER_BIT + 'bit/geckodriver.exe')
                self.driver = webdriver.Chrome('driver/firefox/' + str(self.BROWSER_VERSION) + '/' + self.BROWSER_BIT + 'bit/geckodriver.exe',options=options)
            elif self.BROWSER_NAME == 'chrome':
                self.driver = webdriver.Chrome('driver/chrome/' + str(self.BROWSER_VERSION) + '/chromedriver.exe',options=options)
            printLog("* Your driver is " + self.BROWSER_NAME + ' and version is ' + self.BROWSER_VERSION)
        except Exception as e:
            printLog("No have any driver for " + self.BROWSER_NAME + " !!!")
            printLog(str(e))

    def getDriver(self):
        return self.driver
    
    def getDriverName(self):
        return self.BROWSER_NAME

    def implicitlyWait(self, sec):
        # driver 객체가 get(url)로 요청한 페이지 내용들이 모두 로딩이 완료될 때까지 int(초) 만큼 암묵적으로 기다리게 하는 것이다.
        self.driver.implicitly_wait(sec)

    def explicitlyWait(self, sec, element_type, element_type_value):
        # Explicitly wait은 명시적으로 어떤 조건이 성립했을 때까지 기다린다. 조건이 성립하지 않으면 timeout으로 설정된 시간만큼 최대한 기다리고, TimeoutException을 throw한다.

        try:
            element = WebDriverWait(self.driver, sec).until(
                EC.presence_of_element_located((element_type, element_type_value))                
            )
        except Exception as e:
            printLog(str(e))

        '''
        element_type 종류
        * By.ID, By.XPATH, By.CLASS_NAME, By.TAG_NAME, By.NAME, By.LINK_TEXT
        * 참고 : https://velog.io/@kjh03160/Selenium 
        '''

    def openURL(self, url):
        self.url = url
        try:
            self.driver.get(url)
        except AttributeError as e:
            raise(e)
        
        #self.driver.maximize_window()

    def findElement(self, element_type, path,  click = None):
        ## elem 초기화
        try:
            if element_type == 'xpath':
                self.element = self.driver.find_element_by_xpath(path)
            elif element_type == 'xpath_all':
                self.element = self.driver.find_elements_by_xpath(path)
            elif element_type == 'css_selector':
                self.element = self.driver.find_element_by_css_selector(path)
            elif element_type == 'css_selector_all':
                self.element = self.driver.find_elements_by_css_selector(path)
            elif element_type == 'name':
                self.element = self.driver.find_element_by_name(path)
            elif element_type == 'name_all':
                self.element = self.driver.find_elements_by_name(path)
            elif element_type == 'id':
                self.element = self.driver.find_element_by_id(path)
            elif element_type == 'id_all':
                self.element = self.driver.find_elements_by_id(path)
            elif element_type == 'tag_name':
                self.element = self.driver.find_element_by_tag_name(path)
            elif element_type == 'tag_name_all':
                self.element = self.driver.find_elements_by_tag_name(path)
            elif element_type == 'class_name':
                self.element = self.driver.find_element_by_class_name(path)
            elif element_type == 'class_name_all':
                self.element = self.driver.find_elements_by_class_name(path)
            else:
                printLog("You can use : xpath, css_selector, name, id, tag_name, class_name")
        except Exception as e:
            printLog("can't find element using " + element_type)
            raise(e)
            
        if click == True:
            self.implicitlyWait(5)
            self.element.click()
            
        return self.element

    def click(self):
        self.element.click()
    
    def sendKeys(self, *args):
        self.implicitlyWait(5)
        args = list(args)
        for i in args:
            self.element.send_keys(i)

    def clear(self):
        self.sendKeys(Keys.CONTROL + "a")
        self.sendKeys(Keys.DELETE)


    def getAttribute(self, attr):        
        return  self.element.get_attribute(attr)

    def quit(self):
        self.driver.close()
        self.driver.quit()


    def tableSearch(self, name, nameIdx, rowClick = False, nameClick = False): 
        # 최상위 테이블에서 검색
        # 테이블에 입력한 이름이 있을 경우 True / 없을 경우 False        
        # rowClick 매개변수의 값이 True일 경우 해당 row 클릭
        # nameClick True일 경우 이름 클릭
        printLog("* Start to search in first table!")
        time.sleep(1)   
        self.explicitlyWait(30, By.CSS_SELECTOR, 'tbody')

        table = self.driver.find_element_by_css_selector('tbody')
        self.explicitlyWait(30, By.TAG_NAME, 'tr')
        for tr in table.find_elements_by_tag_name("tr"):            
            self.explicitlyWait(30, By.TAG_NAME, 'td')
            td = tr.find_elements_by_tag_name("td")
            if name == td[nameIdx].text:                
                printLog('* Find name : ' + str(td[nameIdx].text))
                if rowClick == True:
                    tr.click()
                # if nameClick == True:
                if nameClick == True:
                    td[nameIdx].find_element_by_tag_name("a").click()
                return True
            #fp.write(s)

        return False

    
    def tableSearchAll(self, tableIdx, name, nameIdx, rowClick = False): 
        # 최상위 테이블에서 검색
        # 테이블에 입력한 이름이 있을 경우 True / 없을 경우 False
        # click 매개변수의 값이 True일 경우 해당 row 클릭
        time.sleep(1)   
        printLog("* Start to search in all table!")
        #tables = self.driver.find_elements_by_css_selector('table')
        
        tables = self.driver.find_elements_by_css_selector('tbody')
        self.explicitlyWait(30, By.TAG_NAME, 'tr')
        for tr in tables[tableIdx].find_elements_by_tag_name("tr"):            
            self.explicitlyWait(30, By.TAG_NAME, 'td')
            td = tr.find_elements_by_tag_name("td")
            if name == td[nameIdx].text:                
                printLog('* Find name : ' + str(td[nameIdx].text))
                if rowClick == True:
                    tr.click()
                return True
        return False