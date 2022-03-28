#-*- coding: utf-8 -*-

from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
from __common__.__ssh__ import ssh_connection

from __common__.__testlink__ import *
from __common__.__restAPI__ import *

class admin_vm3:
    def __init__(self, webDriver):
        self._vm3Result = [] # lowerCamelCase 로
        self.webDriver = webDriver
        self._vm3Name = 'auto_vm3_'+randomString() # 랜덤 이름
        self.tl = testlink()

        self.rest = restAPI('https://master166.tmax.com/ovirt-engine/api/','__tools__/__rest_api__/master166_ca.crt', 'admin@internal', 'asdf')

    def get_property_value_from_xml(self, xml_, tag, prop):
        # 전체 태그 입력시, 원하는 태그의 속성을 추출
        xml_ = xml_.split('\n')
        tag_name = ''
        for i in xml_:
            if '<'+tag+' ' in i:
                tag_name = i
                break
        print('tag :', tag_name)
        if tag_name == '':
            print("No tag")
            return
        else:
            propIdx = tag_name.find(prop)
            prop_ = tag_name[propIdx+len(prop)+2:]
            a = prop_.find('"')
            propValue = prop_[:a]
            print(tag,prop,':',propValue)
            
            return propValue

    def setup(self):
        # 컴퓨팅
        time.sleep(1)
        printLog("[VM SETUP] Compute - Virtual Machines")
        self.webDriver.findElement('id','compute', True)
        time.sleep(1)

        # 가상머신
        self.webDriver.findElement('id','MenuView_vmsAnchor',True)
        self.webDriver.implicitlyWait(10)
        time.sleep(3)

    def test(self):
        self.createRestAPI()

    def createRestAPI(self):
        try:
            result = FAIL
            msg = ''

            self.rest.post('vms/',
            {'Accept':'application/xml',
             'Content-type':'application/xml'},
             '''<vm>
  <name>%s</name>
  <description>VM creation from rest api automation</description>
  <cluster>
    <name>Default</name>
  </cluster>
  <template>
    <name>Blank</name>
  </template>
  <memory>536870912</memory>
  <os>
    <boot>
      <devices>
        <device>hd</device>
      </devices>
    </boot>
  </os>
</vm>'''%self._vm3Name)

            self.setup()

            time.sleep(10)

            _createCheck = self.webDriver.tableSearch(self._vm3Name, 2, False, False, True)
            if _createCheck[2] == self._vm3Name:
                result = PASS
                msg = ''

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            msg = msg[:msg.find('Element <')]
            printLog("[VM REST API VM CREATE] MESSAGE : " + msg)

        # 결과 저장
        printLog("[VM REST API VM CREATE] RESULT : " + result)
        self._vm3Result.append(['VM' + DELIM + 'rest api vm create' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('VM_REST_API_VM_CREATE',result, msg)