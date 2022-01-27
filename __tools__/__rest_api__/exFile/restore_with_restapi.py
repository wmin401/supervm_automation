## OVIRT 매뉴얼 16.4.3
## URL, 인증파일, 계정 정보 수정 후 각 번호에 맞는 테스트 코드를 주석해제하여 실행

## 가상머신의 id를 제외한 모든 id는 자동으로 입력되도록 설정



import requests, time

class restAPI():

    def __init__(self, URL,verify, id_, pw):
        self.URL = URL
        self.verify=verify
        self.id_ = id_
        self.pw = pw

    def get(self, p=None, h=None):
        res = requests.get(self.URL + p, headers = h,verify = self.verify, auth = (self.id_, self.pw))
        #print(res.text)
        return res.text
    
    def post(self, p=None, h=None, d=None):
        res = requests.post(self.URL + p, headers = h,  data = d, verify = self.verify, auth = (self.id_, self.pw))
        print(res.text)
        return res.text
        
    def delete(self,p=None, h=None, d=None):
        res = requests.delete(self.URL + p, headers = h,  data = d, verify = self.verify, auth = (self.id_, self.pw))
        #print(res.text)
        return res.text

rest = restAPI('https://master162.tmax.dom/ovirt-engine/api/','ca.crt', 'admin@internal', 'asdf')
## URL, 인증파일 위치, ID, PW

## post 의 매개변수는 url, headers, data 순서
## * url은 클래스 생성시 입력한 url 이후부터), headers, data는 json 형
## get, delete 의 매개변수는 url, headers 순서


def get_property_value_from_xml(xml, tag, prop):
    # 전체 태그 입력시, 원하는 태그의 속성을 추출
    xml = xml.split('\n')
    tag_name = ''
    for i in xml:
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


backup_vm_id = '07c09d35-8800-4aa6-ba58-605ce4b0ecb7' ## 백업 전용 가상머신 id
floating_disk_id = 'c74a4efe-127d-455c-9c73-777d8d656e76' # 플로팅 디스크 id


#TC 2
# 디스크를 백업 가상머신에 연결
rest.post('vms/' + backup_vm_id + '/diskattachments/',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},
         '<disk_attachment> \
    <active>true</active> \
    <interface>virtio_scsi</interface>\
    <disk id="' + floating_disk_id + '"/>\
    </disk_attachment>')

#TC 3
#연결한 디스크에 백업진행


#TC 4
# 디스크를 가상머신에서 분리
rest.delete('vms/' + backup_vm_id + '/diskattachments/' + floating_disk_id,
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},
         '<action><detach>true</detach></action>')

#TC 5
# 가상머신 구성 데이터를 사용하여 새 가상머신 생성(16.4.2의 2에서 생성되는 ovf 데이터
cluster_id = '9ed8e340-107a-11ec-b9e7-00163e290953'
make_vm = rest.post('vms/',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},
         '<vm>\
    <cluster id = "' + cluster_id + '">\
        <name>Default</name>\
    </cluster>\
    <name>restapiVM</name>\
    <original_template href="/ovirt-engine/api/templates/00000000-0000-0000-0000-000000000000" id="00000000-0000-0000-0000-000000000000"/>\
    <template href="/ovirt-engine/api/templates/00000000-0000-0000-0000-000000000000" id="00000000-0000-0000-0000-000000000000"/>\
</vm>')
new_vm_id = get_property_value_from_xml(make_vm, 'vm', 'id')

#TC 6
rest.post('vms/' + new_vm_id + '/diskattachments/',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},
         '<disk_attachment> \
    <active>true</active> \
    <interface>virtio_scsi</interface>\
    <disk id="' + floating_disk_id + '"/>\
    </disk_attachment>')
