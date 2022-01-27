
import requests, paramiko, time

class restAPI():

    def __init__(self, URL,verify, id_, pw):
        self.URL = URL
        self.verify=verify
        self.id_ = id_
        self.pw = pw

    def get(self, p=None, h={}):
        if p == None:
            p = ''
        res = requests.get(self.URL + p, headers = h,verify = self.verify, auth = (self.id_, self.pw))
        print(res.text)
    
    def post(self, p=None, h={}, d={}):
        if p == None:
            p = ''
        res = requests.post(self.URL + p, headers = h,  data = d, verify = self.verify, auth = (self.id_, self.pw))
        print(res.text)
        return res.text
        
    def delete(self,p=None, h={},d={}):
        if p == None:
            p = ''
        res = requests.delete(self.URL + p, headers = h,  data=d, verify = self.verify, auth = (self.id_, self.pw))
        print(res.text)
        
    def put(self,p=None, h={},d={}):
        if p == None:
            p = ''
        res = requests.put(self.URL + p, headers = h,  data=d, verify = self.verify, auth = (self.id_, self.pw))
        print(res.text) 


rest = restAPI('https://master165.tmax.com/ovirt-engine/api/','ca.crt', 'admin@internal', 'asdf') ## URL, 인증파일 위치, ID, PW

#
                  
# 가상 디스크 생성
storage_domain = '9eee8b81-5b06-40f9-aa91-f4a7b7746722' # 업로드할 스토리지 도메인의 id
a = rest.post('disks/',
          {'Accept':'application/xml',
           'Content-type':'data'},        
           '<disk>\
               <storage_domains>\
                   <storage_domain id="'+storage_domain+'"/>\
               </storage_domains>\
               <name>restapiDisk</name>\
               <description>restapiDisk</description>\
               <actual_size>1613774848</actual_size>\
               <content_type>data</content_type>\
               <provisioned_size>1613774848</provisioned_size>\
               <format>raw</format>\
               <storage_type>image</storage_type>\
               <sparse>true</sparse>\
          </disk>')

# 디스크 id 추출
b = a.split('\n')
c = b[1].split(' ')

disk_id = c[2][4:-2]
print('disk_id :', disk_id)

# 디스크 생성 중
print("making disk ...")
time.sleep(10)

# image transfer 생성
a = rest.post('imagetransfers/',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},          
          '<image_transfer>\
           <disk id="'+disk_id+'"/>\
           <direction>upload</direction>\
           </image_transfer>')
b = a.split('\n')

# transfer url 또는 proxy url 추출
for i in b:
    if 'transfer_url' in i:
        c = i
        break
transfer_url = c[c.find('https://'):c.find('</transfer_url>')]
print('transfer_url :', transfer_url)

for i in b:
    if 'proxy_url' in i:
        d = i
        break
proxy_url = d[d.find('https://'):d.find('</proxy_url>')]
print('proxy_url :', proxy_url)

# curl로 파일 업로드
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.17.40', username='root', password='asdf', port='22')
stdin, stdout, stderr = ssh.exec_command('curl --cacert ca.crt --upload-file ProLinux-8.1-minimal.iso -X PUT ' + proxy_url)

print("transfering image...")
time.sleep(60)

# image transfer id 추출
for i in b:
    if 'image_transfer' in i:
        e = i
        break
e = e.split(' ')
image_transfer_id = e[2][4:-2]
print('image_transfer_id :', image_transfer_id)

# 종료
rest.post('imagetransfers/' + image_transfer_id + '/finalize',
         {'Accept': 'application/xml' ,
          'Content-Type': 'application/xml'},         
          '<action />')
print('image transfering completed')
