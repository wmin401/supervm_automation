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
    def __init__(self, headless = 'False'):
        self.BROWSER_NAME = BROWSER_NAME.lower()
        self.BROWSER_VERSION = str(BROWSER_VERSION)
        self.BROWSER_BIT = str(BROWSER_BIT)
        self.headless = headless

        options = webdriver.ChromeOptions()
        # 브라우저 최대화
        options.add_argument("--start-maximized")

        ## 헤드리스 기능 적용 여부
        if self.headless == 'true':
            options.add_argument('--headless')
            options.add_argument('window-size=1920,1080')
            # options.add_argument('--no-sandbox')
            options.add_argument("disable-gpu")
            # options.add_argument("--disable-dev-shm-usage")
            options.add_argument('ignore-certificate-errors')
        try:
            # if self.BROWSER_NAME == 'firefox':
            #     #print('driver/firefox/' + str(self.BROWSER_VERSION) + '/' + self.BROWSER_BIT + 'bit/geckodriver.exe')
            #     #self.driver = webdriver.('driver/firefox/' + str(self.BROWSER_VERSION) + '/' + self.BROWSER_BIT + 'bit/geckodriver.exe',options=options)
            #     self.driver = webdriver.Firefox(executable_path='driver/firefox/' + str(self.BROWSER_VERSION) + '/' + self.BROWSER_BIT + 'bit/geckodriver.exe')
            if self.BROWSER_NAME == 'chrome':
                self.driver = webdriver.Chrome('driver/chrome/' + str(self.BROWSER_VERSION) + '/chromedriver.exe',options=options)
            printLog("* Your driver is " + self.BROWSER_NAME + ' and version is ' + self.BROWSER_VERSION[3:])
        except Exception as e:
            printLog("No have any driver for " + self.BROWSER_NAME + " !!!")
            printLog(str(e))

    # 드라이버 자체의 기능을 사용하고 싶을 때 사용
    def getDriver(self):
        return self.driver

    # 현재 드라이버의 이름 출력(크롬인지 파폭인지)
    def getDriverName(self):
        return self.BROWSER_NAME

    def implicitlyWait(self, sec):
        # driver 객체가 get(url)로 요청한 페이지 내용들이 모두 로딩이 완료될 때까지 int(초) 만큼 암묵적으로 기다리게 하는 것이다.
        self.driver.implicitly_wait(sec)

    def explicitlyWait(self, sec, element_type, element_type_value):
        # Explicitly wait은 명시적으로 어떤 조건이 성립했을 때까지 기다린다.
        # 조건이 성립하지 않으면 timeout으로 설정된 시간만큼 최대한 기다리고, TimeoutException을 throw한다.

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

    # 드라이버로 url열기
    def openURL(self, url):
        self.url = url
        try:
            self.driver.get(url)
        except AttributeError as e:
            raise(e)

        #self.driver.maximize_window()

    def findElement(self, element_type, path,  click = False):
        ## element를 찾는 방식을 하나의 함수로 관리하기 위해서 만든 함수
        ## 클릭도 동시에 가능하도록 하기 위해 매개변수로 클릭을 추가했다.
        ## findElement로 element를 찾았을 때, 해당 element는 self.element에 저장되어있다.

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
            elif element_type == 'link_text':
                self.element = self.driver.find_element_by_link_text(path)
            elif element_type == 'link_text_all':
                self.element = self.driver.find_elements_by_link_text(path)
            else:
                printLog("You can use : [xpath, css_selector, name, id, tag_name, class_name, link_text] + _all")
        except Exception as e:
            printLog("* can't find element using " + element_type)
            raise(e)

        if click == True:
            self.element.click()

        return self.element

    # findElement로 찾은 element 클릭
    def click(self):
        self.element.click()

    # findElement로 찾은 element 에 key값 전송
    def sendKeys(self, *args):
        self.implicitlyWait(5)
        args = list(args)
        for i in args:
            self.element.send_keys(i)

    # findElement로 찾은 element가 input일때 값이 있으면 삭제한다.
    def clear(self):
        self.sendKeys(Keys.CONTROL + "a")
        self.sendKeys(Keys.DELETE)

    # element의 attribute를 가져온다.
    def getAttribute(self, attr):
        return  self.element.get_attribute(attr)

    # 자바스크립트의 명령어를 사용하고 싶을 때 사용한다. 
    def executeScript(self, script):
        self.driver.execute_script(script)
    
    # 드라이버 종료
    def quit(self):
        self.driver.close()
        self.driver.quit()

    def tableSearch(self, name, nameIdx, rowClick = False, nameClick = False, returnValueList = False):
        # 최상위 테이블에서 검색
        # 테이블에 입력한 이름이 있을 경우 True / 없을 경우 False
        # rowClick : True일 경우 해당 row 클릭 -> 현재는 해당 부분 문제로 인해 사용 불가
        # nameClick : True일 경우 이름 클릭
        # returnValueList : True일 경우 해당하는 행을 리스트로 반환해줌
        time.sleep(2)


        # 현재 페이지에 table이 하나만 있을 경우에 사용 가능하다.
        # HyperVM의 페이지는 보통 table이 하나만 있기에 사용 가능
        # tbody의 tr태그, tr태그 내부의 td태그를 검색하여 원하는 값이 있는 행을 찾는 기능



        printLog('[TABLE SEARCH] ' + str(self.driver.current_url), debug=True)

        try:
            self.explicitlyWait(10, By.CSS_SELECTOR, 'tbody')
            table = self.driver.find_element_by_css_selector('tbody')
            for tr in table.find_elements_by_tag_name("tr"):
                self.explicitlyWait(10, By.TAG_NAME, 'td')
                td = tr.find_elements_by_tag_name("td")
                if name == td[nameIdx].text:
                    if returnValueList == True:
                        tdLst = []
                        for i in range(len(td)):
                            try:
                                tdLst.append(td[i].text)
                            except:
                                tdLst.append('')
                        printLog('[TABLE SEARCH] TABLE : ' + str(tdLst))
                        return tdLst
                    if rowClick == True:    
                        printLog('[TABLE SEARCH] Search : ' + str(td[nameIdx].text))     
                        time.sleep(1) 
                        # tr.click() ## 여기서 자꾸 호스트를 클릭해버리네?
                        td[nameIdx].click()
                    if nameClick == True:
                        ## 찾은 내용을 클릭하는 함수(a태그가 있어야만 가능하다)
                        ## 이름을 클릭할 때 사용한다.
                        printLog('[TABLE SEARCH] Search : ' + str(td[nameIdx].text))    
                        td[nameIdx].find_element_by_tag_name("a").click() 
                        self.implicitlyWait(10)
                        time.sleep(1)
                        printLog('[TABLE SEARCH] Name Click : ' + str(self.driver.current_url), debug=True) 
                    return True
        except Exception as e:
            printLog('[TABLE SEARCH] EXCEPTION : ' + str(e))
            return False

        return False

    def tableSearchAll(self, tableIdx, name, nameIdx, rowClick = False):
        # 최상위 테이블에서 검색
        # 테이블에 입력한 이름이 있을 경우 True / 없을 경우 False
        # click 매개변수의 값이 True일 경우 해당 row 클릭
        time.sleep(1)
        # printLog("[TABLE SEARCH ALL] Searching all table ...")
        #tables = self.driver.find_elements_by_css_selector('table')

        ## 페이지에 table이 여러개 있을 떄 사용 가능하다.
        ## 매개변수로 table의 순서를 입력하여 원하는 tbody를 선택할 수 있다. 
        ## 현재 HyperVM은 QoS에서 적용 중이다.

        tables = self.driver.find_elements_by_css_selector('tbody')
        self.explicitlyWait(30, By.TAG_NAME, 'tr')
        for tr in tables[tableIdx].find_elements_by_tag_name("tr"):
            self.explicitlyWait(30, By.TAG_NAME, 'td')
            td = tr.find_elements_by_tag_name("td")
            if name == td[nameIdx].text:
                if rowClick == True:
                    printLog('[TABLE SEARCH ALL] : ' + str(td[nameIdx].text))
                    tr.click()
                return True
        return False

    
    def isChangedStatus(self, name, nameIdx, statusIdx, failLst, passLst, t=60):
        # 1초마다 상태 변경이 되었는지 확인하는 함수
        printLog("[STATUS CHECK] Check status changed")
        st = time.time()
        before = ''
        while True:
            ed = time.time()
            if ed-st >= t:
                printLog("[%s STATUS] Failed status changed : %ss Timeout"%(name,t))
                return FAIL, 'Timeout'
            time.sleep(1)
            try:
                tableValueList = self.tableSearch(name, nameIdx, rowClick=False, nameClick=False, returnValueList=True)    
                # printLog(tableValueList, debug=True)    
                current = tableValueList[statusIdx]
                ## 현재 상태와 기존의 상태를 비교하여 
                ## passLst에 포함된 문자열이 나오지 않으면 실패로 간주하며, timeout이 될 때 까지 계속 확인한다.
                ## failLst는 현재 상태를 비교하여 출력을 위한 변수이다.
                for failStr in failLst:
                    if failStr in tableValueList[statusIdx]:
                        if current != before:
                            printLog("[%s STATUS] %s"%(name, tableValueList[statusIdx]))
                            before = current

                for passStr in passLst:
                    if passStr == tableValueList[statusIdx]:
                        printLog("[%s STATUS] %s"%(name, tableValueList[statusIdx]))
                        return PASS, ''
            except Exception as e: 
                printLog('[STATUS CHECK] %s'%(str(e)))
                continue

    def turnOffAlert(self):
        printLog("[TURN OFF NOTIFICATION] Turn off notification")

        # notification 팝업을 보여지게 한다.
        # notificaion 컨테이너의 css값을 강제로 변경하여, 보여지게 만듦
        self.executeScript("notiPanel = document.getElementsByClassName('notif_notificationsPanel')")
        self.executeScript("notiPanel[0].style.display = 'inline-block'")
        self.executeScript("notiContainer = document.getElementsByClassName('notif_buttonContainer')")
        self.executeScript("notiContainer[0].style.display = 'inline-block'")

        # 알림 해제
        self.findElement('xpath','/html/body/div[3]/div[2]/div/div[1]/div[2]/a', True)
        time.sleep(0.5)
        self.findElement('xpath','/html/body/div[3]/div[2]/div/div[1]/div[2]/ul/li[3]/a', True)

        # noti 팝업 다시 안보여지게 수정        
        self.executeScript("notiPanel[0].style.display = 'none'")
        self.executeScript("notiContainer[0].style.display = 'none'")