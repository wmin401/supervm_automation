from __common__.__driver__ import *
from __common__.__parameter__ import *
from __common__.__login__ import *
from __common__.__portal__ import *

from __admin__.__host__ import *
from __vm__.__vm__ import *


## 테스트 메인 파일
## 여기서 각 파일들을 불러와서 테스트 진행


def main():

    print('1. 브라우저 열기')
    webDriver = SuperVM_driver()
    webDriver.openURL(SUPERVM_URL)

    # ## supervm version 출력
    # webDriver.waitUntilFindElement(5)
    # supervm_version_elem = webDriver.findElement('class_name','pf-l-split__item obrand_welcomePageVersionText')
    # supervm_version = supervm_version_elem.get_attribute('textContent')
    # print(supervm_version[supervm_version.find('4'):supervm_version.find('prolinux8')+9])
    

    print('2. 로그인')
    portalLogin(webDriver)
    ## 비공개 일 때
    ## 공개 일 때

    print("3. 포털접근")
    if PORTAL_TYPE == 'admin':
        accessAdminPortal(webDriver)
        
    elif PORTAL_TYPE == 'vm':
        accessVmPortal(webDriver)

    print("4. 테스트 시작")

    if PORTAL_TYPE == 'admin':
        if HOST_TEST == 'true':
            print("4.1 호스트")
            _host = admin_host()
            _host.create(webDriver)

    elif PORTAL_TYPE == 'vm':
        print("4.1 VM 생성")
        test_vm_vm = vm_vm()
        test_vm_vm.create()

    time.sleep(10)

if __name__ == '__main__':    
    
    main()