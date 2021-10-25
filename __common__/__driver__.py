# -*- encoding= utf-8 -*-
import time
from __common__.__parameter__ import *
from selenium import webdriver


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
            options.add_argument('headless')
            #options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
        try:
            if self.BROWSER_NAME == 'firefox':
                self.driver = webdriver.Chrome('__driver__/firefox/' + str(self.BROWSER_VERSION) + '/' + self.BROWSER_BIT + 'bit/chromedriver.exe',options=options)
            elif self.BROWSER_NAME == 'chrome':
                self.driver = webdriver.Chrome('__driver__/chrome/' + str(self.BROWSER_VERSION) + '/chromedriver.exe',options=options)
            print("* Your driver is " + self.BROWSER_NAME + ' and version is ' + self.BROWSER_VERSION)
        except Exception as e:
            print("No have any driver for " + self.BROWSER_NAME + " !!!")
            print(e)

    def getDriver(self):
        return self.driver
    
    def getDriverName(self):
        return self.BROWSER_NAME

    def waitUntilFindElement(self, sec):
        self.driver.implicitly_wait(sec)

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
            elif element_type == 'css_selector':
                self.element = self.driver.find_element_by_css_selector(path)
            elif element_type == 'name':
                self.element = self.driver.find_element_by_name(path)
            elif element_type == 'id':
                self.element = self.driver.find_element_by_id(path)
            elif element_type == 'tag_name':
                self.element = self.driver.find_element_by_tag_name(path)
            elif element_type == 'class_name':
                self.element = self.driver.find_element_by_class_name(path)
            else:
                print("You can use : xpath, css_selector, name, id, tag_name, class_name")
        except Exception as e:
            print("can't find element using " + element_type)
            raise(e)
            
        if click == True:
            self.waitUntilFindElement(5)
            self.element.click()
            
        return self.element

    def click(self):
        self.element.click()
    
    def sendKey(self, *args):
        self.waitUntilFindElement(5)
        args = list(args)
        for i in args:
            self.element.send_keys(i)

    def getAttribute(self, attr):        
        return  self.element.get_attribute(attr)

    def quit(self):
        self.driver.close()
        self.driver.quit()
