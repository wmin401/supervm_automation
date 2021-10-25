from __common__.__driver__ import *
from __common__.__parameter__ import *
from __common__.__login__ import *
from __common__.__portal__ import *

from __admin__.__host__ import *
from __vm__.__create__ import vm_create


## 테스트 메인 파일
## 여기서 각 파일들을 불러와서 테스트 진행

def main():

    print('1. 브라우저 열기')
    webDriver = SuperVM_driver()
    webDriver.openURL(SUPERVM_URL)

    print('2. 로그인')
    portal_login(webDriver)
    ## 비공개 일 때
    ## 공개 일 때

    print("3. 포털접근")
    if PORTAL_TYPE == 'admin':
        access_admin_portal(webDriver)
        
    elif PORTAL_TYPE == 'vm':
        access_vm_portal(webDriver)

    print("4. 테스트 시작")

    if PORTAL_TYPE == 'admin':
        print("4.1 호스트")
        host_create()
    elif PORTAL_TYPE == 'vm':
        print("4.1 VM 생성")
        vm_create()

    time.sleep(10)

if __name__ == '__main__':    
    
    main()