import os
import string
import random

from __common__.__parameter__ import *

## 시작시간과 종료시간을 입력받으면 시, 분, 초로 보여주는 함수
def secToHms(start, end): # 시작시간, 끝나는 시간
    sec = end - start
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return h,m,s

def printLog(text, debug=False, install=False):
    print(text)

    tt = str(type(text))
    if 'list' in tt:
        t = '['
        cc = 0
        for i in text:
            if cc == 0:
                t += "'" + i + "'"
            else:
                t += ", '" + i + "'"
            cc += 1
        t += ']'
    else:
        t = text

    if t is not None and debug == True:
        t = '[DEBUG]' + str(t)

    if install == True:
        with open(INSTALL_LOG_FILE, 'a', encoding='utf-8') as logFile:
            logFile.write(t+'\n')
    else:
        with open(LOG_FILE, 'a', encoding='utf-8') as logFile:
            logFile.write(t+'\n')


## 원하는 경로에 폴더를 생성해줌
## 하위 경로 입력시, 폴더가 존재하지 않으면 같이 생성
def makeFolder(path_):
    if os.path.isdir(path_):
        print("* " + path_ + ' folder is already existed!')
        return
    else:
        print("* " + path_ + ' folder made!')
        os.makedirs(path_)

def printLine():
    print('---------------------------------------------------------')

def randomString(length=8):
    string_ = ''
    for i in range(length):
        string_ += str(random.choice(string.ascii_letters))
    return string_

def makeUpMsg(msg_list):
    ## 입력받은 메시지 리스트에서 \n과 , 삭제
    returnMsg = []
    for i in msg_list:
        i = i.replace('\n','')
        #i = i.replace(',', ' ')
        returnMsg.append(i)
    return returnMsg

def printSquare(msg):
    m = '''=========================================================
 %s
========================================================='''%msg.capitalize()
    return m


def selectDropdownMenu(webDriver, type_, ulTagPath, name):
    # 드롭다운 메뉴에서 원하는거 클릭하고 싶을때 사용    
    time.sleep(1)
    printLog("[SELECT DROPDOWN MENU] Selecting menu")
    if type_ == 'css_selector':
        lis = webDriver.findElement(type_ + '_all', ulTagPath + ' > li')
    elif type_ == 'xpath':
        lis = webDriver.findElement(type_ + '_all', ulTagPath + '/li')
    else:
        printLog("[SELECT DROPDOWN MENU] Undefined type")
        return

    for li in lis:
        if name == li.get_attribute('textContent'):
            printLog("[SELECT DROPDOWN MENU] Select %s"%(str(li.get_attribute('textContent'))))
            li.click()
            break
    time.sleep(1)


import pywinauto
def openFileDialog(title_, filePath, fileName):
    app = pywinauto.Application().connect(title=title_)
    dialog = app.top_window()
    dialog.Edit.type_keys(filePath + '\\' + fileName)
    dialog['&OpenButton'].click()      
