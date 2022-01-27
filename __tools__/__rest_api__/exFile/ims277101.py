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
        print(res.text)
        return res.text
        
    def delete(self,p=None, h=None, d=None):
        res = requests.delete(self.URL + p, headers = h,  data = d, verify = self.verify, auth = (self.id_, self.pw))
        #print(res.text)
        return res.text

rest = restAPI('https://192.168.17.165/ovirt-engine/api/','ca.crt', 'admin@internal', 'asdf') ## URL, 인증파일 위치, ID, PW

a = rest.get('disks')

print(a)

