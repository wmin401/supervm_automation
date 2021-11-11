import os
import shutil
from xml.etree.ElementTree import Element, SubElement #, Comment, tostring
from xml.etree.ElementTree import ElementTree
from __common__.__parameter__ import *


class testlink:
    def __init__(self):      
        print("* Start the connection with the Testlink ! ")
        self.junitsFolder = 'junit_xml'
        if not os.path.isdir(RESULT_PATH + '/'+ self.junitsFolder):
            os.makedirs(RESULT_PATH + '/'+ self.junitsFolder)

    def junitBuilder(self, *args):
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
        filePath = RESULT_PATH + '/' + self.junitsFolder+ '/junit-'+str(args[0])+'.xml'
        try:
            tree.write(filePath,encoding="utf-8", xml_declaration=True)
            print("* junit file is successfully created!")
        except Exception as e:            
            print("*** Junit Build Exception : %s"%(e))
            return


# junit-커스텀필드명.xml 파일 
'''
<?xml version='1.0' encoding='utf-8'?>
<testsuite><testcase classname="첫번째 매개변수" name="첫번째 매개변수" status="두번째 매개변수" />세번째 매개변수</testsuite>
'''
# 테스트링크의 커스텀필드(SupverVM_Automation)와 classname이 일치하여야함)
# 입력 예시
# self.tl.junitBuilder('CLUSTER_REMOVE', result, msg) #클래스이름, 결과, 메세지
