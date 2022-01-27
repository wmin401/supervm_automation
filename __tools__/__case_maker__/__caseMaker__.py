import tkinter as tk

testName = 'default'

root = tk.Tk()
root.geometry("300x100")
root.title("Page Maker")

# 파일 입력 후 create 클릭
# __test__/__admin__/__이름__.py 로 파일 생성됨
# __import__.py 에 생성한 파일 추가됨
# __common__/__parameter__.py 에 변수 추가됨
# __main__.py 에 테스트 추가됨


def pageMaker():
    global testName
    testName=nameEntry.get()

    # 파일생성
    s = '''#-*- coding: utf-8 -*-

from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

class admin_%s:
    def __init__(self, webDriver):
        self._%sResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        self._%sName = 'auto_%s_'+randomString() # 랜덤 이름
        self.tl = testlink()
          
    def test(self):
        self.case1()


    def case1(self):
        try:
            result = PASS
            msg = ''
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[%s TEST] MESSAGE : " + msg)

        # 결과 저장
        printLog("[%s TEST] RESULT : " + result)
        self._%sResult.append(['%s' + DELIM + 'test' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('%s_TEST',result, msg)'''%(testName.lower(), testName.lower(), testName.lower(), testName.lower(), testName.upper(), testName.upper(), testName.lower(), testName.capitalize(), testName.upper())

    with open('../__test__/__admin__/__%s__.py'%testName.lower(),'w', encoding='utf-8') as f:
        f.write(s)
    print("[PAGE MAKER] ../__test__/__admin__/__%s__.py file was created")

    # import 추가    
    fp = open('../__import__.py','r', encoding='utf-8')
    fl = []
    for i in fp:
        fl.append(i.replace('\n',''))
    for i in range(len(fl)):
        if 'entry point import' in fl[i]:
            importCode = 'from __test__.__admin__.__%s__ import *'%(testName.lower())
            fl.insert(i+1, importCode)
    fp = open('../__import__.py','w', encoding='utf-8')
    for i in fl:
        fp.write(i+'\n')
    fp.close()
    print("[PAGE MAKER] Import code was Added in __import__.py")

    # 변수 추가
    fp = open('../__common__/__parameter__.py','r', encoding='utf-8')
    fl = []
    for i in fp:
        fl.append(i.replace('\n',''))
    for i in range(len(fl)):
        if 'entry point para1' in fl[i]:
            fl.insert(i+1, "    %s_TEST = os.getenv('%s_TEST')"%(testName.upper(),testName.upper()))
        elif 'entry point para2' in fl[i]:
            fl.insert(i+1, "    %s_TEST = 'true'"%(testName.upper()))
    fp = open('../__common__/__parameter__.py','w', encoding='utf-8')
    for i in fl:
        fp.write(i+'\n')
    fp.close()
    print("[PAGE MAKER] Variable was Added in ../__common__/__parameter__.py")
    print("[PAGE MAKER] You have to add variable in jenkins")
    print("[PAGE MAKER] http://192.168.105.140:8088/view/ProLinux/job/supervm_automation/configure")
    
    # main 추가    
    fp = open('../__main__.py','r', encoding='utf-8')
    fl = []
    for i in fp:
        fl.append(i.replace('\n',''))
    for i in range(len(fl)):
        if 'entry point main' in fl[i]:
            mainCode = '''    if %s_TEST == 'true':
        printLine()
        printLog(printSquare("*** %s Test ***"))
        _%s = admin_%s(webDriver)
        _%s.test()
            
        _totalResult = saveResult(_%s._%sResult, _totalResult)
'''%(testName.upper(), testName.capitalize(), testName.lower(), testName.lower(), testName.lower(), testName.lower(), testName.lower())
            fl.insert(i+1, mainCode)
    fp = open('../__main__.py','w', encoding='utf-8')
    for i in fl:
        fp.write(i+'\n')
    fp.close()
    print("[PAGE MAKER] Main test code was added in __main__.py")
    print("[PAGE MAKER] You have to add variable in jenkins")
    
    root.destroy()

nameEntry=tk.Entry(root)
nameEntry.pack()
btnRead=tk.Button(root, height=1, width=10, text="Create", command=pageMaker)

btnRead.pack()

root.mainloop()