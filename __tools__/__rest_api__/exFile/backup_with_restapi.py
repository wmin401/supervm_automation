## OVIRT 매뉴얼 16.4.2
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
        print(res.text)
        return res.text
    
    def post(self, p=None, h=None, d=None):
        res = requests.post(self.URL + p, headers = h,  data = d, verify = self.verify, auth = (self.id_, self.pw))
        #print(res.text)
        return res.text
        
    def delete(self,p=None, h=None):
        res = requests.delete(self.URL + p, headers = h,  verify = self.verify, auth = (self.id_, self.pw))
        #print(res.text)
        return res.text
rest = restAPI('https://master162.tmax.dom/ovirt-engine/api/','ca.crt', 'admin@internal', 'asdf')
## URL, 인증파일 위치, ID, PW

## post 의 매개변수는 url, headers, data 순서
## * url은 클래스 생성시 입력한 url 이후부터), headers, data는 json 형
## get, delete 의 매개변수는 url, headers 순서


def get_property_value_from_xml(xml_, tag, prop):
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


origin_vm_id = '460b481f-6fed-44a7-afa2-c2c67f8256e0' ## vm id는 백업할 가상머신의 id
backup_vm_id = '07c09d35-8800-4aa6-ba58-605ce4b0ecb7' ## 백업 전용 가상머신 id

'''
#TC 1
# 스냅샷 생성
make_snapshot = rest.post('vms/' + origin_vm_id + '/snapshots',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},
          "<snapshot><description>BACKUP</description></snapshot>")
print("making snapshot...")
time.sleep(30)
snapshot_id = get_property_value_from_xml(make_snapshot, 'snapshot', 'id') ## 생성한 스냅샷 id를 반환

'''
#TC 2
# ovf 데이터 가져오기
snapshot_id = 'a5261141-97c6-4897-ac61-2df07d46abcc'
rest.get('vms/' + origin_vm_id + '/snapshots/' + snapshot_id,
         {'All-Content':'true',
          'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'})


'''
#TC 3
# 스냅샷의 디스크 id 가져오기
#snapshot_id = 'b9b2c368-5838-4842-9bfc-6ab4372654ee' ##각자 실행할때는 id를 수동으로
get_disk_id = rest.get('vms/' + origin_vm_id + '/snapshots/' + snapshot_id + '/disks',
                       {'Accept': 'application/xml' ,
                        'Content-Type': 'application/xml'})

disk_id = get_property_value_from_xml(get_disk_id, 'disk','id')

time.sleep(5)

#TC 4
## 백업 vm 은 같은 클러스터 내에 있는 백업이 가능한 도메인을 이용하여 가상머신을 생성하여야함
rest.post('vms/' + backup_vm_id + '/diskattachments/',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},
         '<disk_attachment>\
	<active>true</active>\
	<interface>virtio_scsi</interface>\
	<disk id="' + disk_id + '">\
	<snapshot id="' + snapshot_id + '"/>\
	</disk>\
</disk_attachment>')

time.sleep(5)

#TC 6
# 가이드 상에는 snapshot id 를 사용하라고 나와있으나, 디스크를 삭제해야하기 때문에 디스크로 하니까 됨
#deleted_disk_id = '203bfe4f-96ba-4d00-958b-a75ee24a988c'
#backup_vm_id = '75fee71c-88eb-488f-b69f-2cf4cd5871fc' 
rest.delete('vms/' + backup_vm_id + '/diskattachments/' + disk_id,
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'})

time.sleep(5)
#TC 7
rest.delete('vms/' + origin_vm_id + '/snapshots/' + snapshot_id,
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'})

time.sleep(5)
'''
