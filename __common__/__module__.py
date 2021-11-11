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

def printLog(text):
    print(text)

    with open(LOG_FILE, 'a', encoding='utf-8') as logFile:
        logFile.write(text+'\n')

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


def randomString(num=8):
    stinrg_ = ''
    for i in range(num):
        stinrg_ += str(random.choice(string.ascii_letters))