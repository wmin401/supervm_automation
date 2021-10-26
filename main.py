# 공통 파일
from __common__.__driver__ import *
from __common__.__parameter__ import *
from __common__.__login__ import *
from __common__.__portal__ import *
from __common__.__csv__ import *

# 테스트 파일
from __test__.__admin__.__host__ import *
from __test__.__admin__.__cluster__ import *
from __test__.__admin__.__data_center__ import *
from __test__.__admin__.__disk__ import *
from __test__.__admin__.__domain__ import *
from __test__.__vm__.__vm__ import *

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
    
    printLine()
    # 테스트 시작
    print('1. Open Browser')
    webDriver = SuperVM_driver(headless=False)
    webDriver.openURL(SUPERVM_URL)

    printLine()
    print("2. Print SuperVM Version")
    ## supervm version 출력
    webDriver.implicitlyWait(5)
    _supervmVersionElem = webDriver.findElement('css_selector','body > main > section > div.pf-l-split > div.pf-l-split__item.obrand_welcomePageVersionText')
    _supervmVersion = _supervmVersionElem.get_attribute('textContent')
    print('SuperVM Ver : ' + _supervmVersion[_supervmVersion.find('4'):_supervmVersion.find('prolinux8')+9])
    

    printLine()
    print('3. Login')
    portalLogin(webDriver)

    printLine()
    print("4. Access Portal")
    if PORTAL_TYPE == 'admin':
        accessAdminPortal(webDriver)
        
    elif PORTAL_TYPE == 'vm':
        accessVmPortal(webDriver)

    printLine()
    print("5. Start Test")

    if PORTAL_TYPE == 'admin':        
        if CLUSTER_TEST == 'true':        
            printLine()
            print("*** Cluster Test ***")
            _cluster = admin_cluster(webDriver)
            _cluster.create()
            _cluster.update()
            _cluster.remove()
            
            _totalResult = saveResult(_cluster._clusterResult, _totalResult)        

        if DATA_CENTER_TEST == 'true':
            printLine()
            print("*** Data Center Test ***")
            _data_center = admin_data_center()
            _data_center.create(webDriver)
            
            _totalResult = saveResult(_data_center._data_centerResult, _totalResult)        

        if DISK_TEST == 'true':
            printLine()
            print("*** Disk Test ***")
            _disk = admin_disk()
            _disk.create(webDriver)
            
            _totalResult = saveResult(_disk._diskResult, _totalResult)        
        
        if DOMAIN_TEST == 'true':
            printLine()
            print("*** Domain Test ***")
            _domain = admin_domain()
            _domain.create(webDriver)
            
            _totalResult = saveResult(_domain._domainResult, _totalResult)        

        if HOST_TEST == 'true':
            printLine()
            print("*** Host Test ***")
            _host = admin_host()
            _host.create(webDriver)
            
            _totalResult = saveResult(_host._hostResult, _totalResult)

    elif PORTAL_TYPE == 'vm':
        printLine()
        print("5.1 VM Create")
        test_vm_vm = vm_vm()
        test_vm_vm.create()

    saveTotalResult(_totalResult)
    ## 테스트 이후 결과 종합하는거 필요

    time.sleep(1)

if __name__ == '__main__':    
    
    main()