import os
import shutil
from xml.etree.ElementTree import Element, SubElement #, Comment, tostring
from xml.etree.ElementTree import ElementTree
from __common__.__parameter__ import *


class testlink:
    def __init__(self):      
        print("* Start the connection with the Testlink ! ")
        self.junitsFolder = 'junit_xml/build_' + str(BUILD_ID)
        if not os.path.isdir(RESULT_PATH + '/'+ self.junitsFolder):
            os.makedirs(RESULT_PATH + '/'+ self.junitsFolder)

        self.junitBuilder('SAMPLE', PASS, 'Sample junit xml file for jenkins')

    def junitBuilder(self, *args):
        ## 젠킨스 에서만 생성되도록 변경
        if IN_JENKINS == 'true':
            args = list(args)   
            testsuite = Element('testsuite')
            testcase = SubElement(testsuite, 'testcase')
            testcase.set('classname', args[0])
            testcase.set('name', args[0])
            testcase.set('status',args[1].lower()+'ed')
            if args[1] == FAIL:
                failure = SubElement(testcase, 'failure')
                failure.text = args[2]
            else: ## pass or blocked
                testcase.text = args[2]

            ## block인 경우엔 testNG 파일이 필요한 상태
            tree = ElementTree(testsuite)
            filePath = RESULT_PATH + '/' + self.junitsFolder + '/junit-'+str(args[0])+'.xml'
            try:
                tree.write(filePath,encoding="utf-8", xml_declaration=True)
                print("* junit file is successfully created!")
            except Exception as e:            
                print("*** Junit Build Exception : %s"%(e))
                return

### 연동 방법
## 테스트링크
# 1) 테스트케이스의 커스텀필드(SuperVM_Automation)에 클래스 이름을 입력
# 2) 테스트케이스의 Execution type을 Automated로 변경
## 소스 코드
# 1) testlink 클래스 생성(self.tl = testlink())
# 2) junitBuilder 함수에 입력한 클래스 이름을 매개변수로 생성 
# 생성된 junit파일이 테스트링크로 연결됨(junit 내부의 클래스이름과 테스트링크의 클래스이름이 일치하여야 한다.)