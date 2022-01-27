## OVIRT 매뉴얼 16.4.3
## URL, 인증파일, 계정 정보 수정 후 각 번호에 맞는 테스트 코드를 주석해제하여 실행

## 가상머신의 id를 제외한 모든 id는 자동으로 입력되도록 설정


import requests

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
        #print(res.text)
        return res.text
        
    def delete(self,p=None, h=None, d=None):
        res = requests.delete(self.URL + p, headers = h,  data = d, verify = self.verify, auth = (self.id_, self.pw))
        #print(res.text)
        return res.text
    
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

