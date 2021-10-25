from __common__.__driver__ import *
from __common__.__parameter__ import *
from __common__.__login__ import *
from __common__.__portal__ import *

from __admin__.__host__ import *
from __admin__.__cluster__ import *
from __vm__.__vm__ import *


## 테스트 메인 파일
## 여기서 각 파일들을 불러와서 테스트 진행


def main():

    _totalResult = []

    print('1. 브라우저 열기')
    webDriver = SuperVM_driver()
    webDriver.openURL(SUPERVM_URL)

    print("2. SuperVM 버전 출력")
    ## supervm version 출력
    webDriver.waitUntilFindElement(5)
    _supervmVersionElem = webDriver.findElement('css_selector','body > main > section > div.pf-l-split > div.pf-l-split__item.obrand_welcomePageVersionText')
    _supervmVersion = _supervmVersionElem.get_attribute('textContent')
    print('SuperVM Ver : ' + _supervmVersion[_supervmVersion.find('4'):_supervmVersion.find('prolinux8')+9])
    

    print('3. 로그인')
    portalLogin(webDriver)
    ## 비공개 일 때
    ## 공개 일 때

    print("4. 포털접근")
    if PORTAL_TYPE == 'admin':
        accessAdminPortal(webDriver)
        
    elif PORTAL_TYPE == 'vm':
        accessVmPortal(webDriver)

    print("5. 테스트 시작")

    if PORTAL_TYPE == 'admin':
        if HOST_TEST == 'true':
            print("5.1 host")
            _host = admin_host()
            _host.create(webDriver)
            
            for i in _host._hostResult:
                _totalResult.append(i)

        if CLUSTER_TEST == 'true':
            print("5.2 cluster")
            _cluster = admin_cluster()
            _cluster.create(webDriver)
            
            for i in _cluster._clusterResult:
                _totalResult.append(i)

    elif PORTAL_TYPE == 'vm':
        print("5.1 VM 생성")
        test_vm_vm = vm_vm()
        test_vm_vm.create()

    for i in _totalResult:
        print(i)
    ## 테스트 이후 결과 종합하는거 필요

    time.sleep(1)

if __name__ == '__main__':    
    
    main()