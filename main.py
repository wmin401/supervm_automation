# 공통 파일
from __common__.__driver__ import *
from __common__.__parameter__ import *
from __common__.__login__ import *
from __common__.__portal__ import *
from __common__.__csv__ import *

# 테스트 파일
from __admin__.__host__ import *
from __admin__.__cluster__ import *
from __admin__.__data_center__ import *
from __admin__.__disk__ import *
from __admin__.__domain__ import *
from __vm__.__vm__ import *

## 테스트 메인 파일
## 여기서 각 파일들을 불러와서 테스트 진행

def saveResult(res, lst):
    for i in res:
        lst.append(i)
        saveRealTimeResult(i[0])
    return lst

def main():

    # 테스트 초기 세팅
    initResult()
    _totalResult = []

    # 테스트 시작
    print('1. 브라우저 열기')
    webDriver = SuperVM_driver(headless=False)
    webDriver.openURL(SUPERVM_URL)

    print("2. SuperVM 버전 출력")
    ## supervm version 출력
    webDriver.implicitlyWait(5)
    _supervmVersionElem = webDriver.findElement('css_selector','body > main > section > div.pf-l-split > div.pf-l-split__item.obrand_welcomePageVersionText')
    _supervmVersion = _supervmVersionElem.get_attribute('textContent')
    print('SuperVM Ver : ' + _supervmVersion[_supervmVersion.find('4'):_supervmVersion.find('prolinux8')+9])
    

    print('3. 로그인')
    portalLogin(webDriver)

    print("4. 포털접근")
    if PORTAL_TYPE == 'admin':
        accessAdminPortal(webDriver)
        
    elif PORTAL_TYPE == 'vm':
        accessVmPortal(webDriver)

    print("5. 기능 테스트 시작")

    if PORTAL_TYPE == 'admin':
        if HOST_TEST == 'true':
            print("5.1 host")
            _host = admin_host()
            _host.create(webDriver)
            
            _totalResult = saveResult(_host._hostResult, _totalResult)

        if CLUSTER_TEST == 'true':
            print("5.2 cluster")
            _cluster = admin_cluster(webDriver)
            _cluster.create()
            _cluster.remove()
            
            _totalResult = saveResult(_cluster._clusterResult, _totalResult)        
        
        if DISK_TEST == 'true':
            print("5.3 disk")
            _disk = admin_disk()
            _disk.create(webDriver)
            
            _totalResult = saveResult(_disk._diskResult, _totalResult)        
        
        if DOMAIN_TEST == 'true':
            print("5.4 domain")
            _domain = admin_domain()
            _domain.create(webDriver)
            
            _totalResult = saveResult(_domain._domainResult, _totalResult)        

        if DATA_CENTER_TEST == 'true':
            print("5.5 data_center")
            _data_center = admin_data_center()
            _data_center.create(webDriver)
            
            _totalResult = saveResult(_data_center._data_centerResult, _totalResult)        
            
    elif PORTAL_TYPE == 'vm':
        print("5.1 VM 생성")
        test_vm_vm = vm_vm()
        test_vm_vm.create()

    saveTotalResult(_totalResult)
    ## 테스트 이후 결과 종합하는거 필요

    time.sleep(1)

if __name__ == '__main__':    
    
    main()