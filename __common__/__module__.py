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


# 출력되는 내용을 로그에 똑같이 기록하기 위해 만든 함수
# debug일 경우엔 앞에 DEBUG가 붙는다
# install은 install 로그파일에 출력된다.
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

# 8개의 문자열을 임의로 생성해준다.(숫자+영문대소문자)
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
    # element의 type과 ul 태그의 경로를 매개변수로 입력받고, 클릭하고자 하는 메뉴를 매개변수로 입력받는다.
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