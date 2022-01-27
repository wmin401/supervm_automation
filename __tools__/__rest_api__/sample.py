import __restAPI__

rest = __restAPI__.restAPI('https://master165.tmax.com/ovirt-engine/api/','master165_ca.crt', 'admin@internal', 'asdf') ## URL, 인증파일 위치, ID, PW

a = rest.get('disks')

print(a)

