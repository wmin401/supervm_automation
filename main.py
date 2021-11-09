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
from __test__.__admin__.__qos__ import *
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
    printLog('1. Open Browser')
    webDriver = SuperVM_driver(headless=False)
    webDriver.openURL(SUPERVM_URL)

    printLine()
    printLog("2. Print SuperVM Version")
    # supervm version 출력
    webDriver.implicitlyWait(5)
    _supervmVersionElem = webDriver.findElement('css_selector','body > main > section > div.pf-l-split > div.pf-l-split__item.obrand_welcomePageVersionText')
    _supervmVersion = _supervmVersionElem.get_attribute('textContent')
    printLog('* SuperVM Ver : ' + _supervmVersion[_supervmVersion.find('4'):_supervmVersion.find('prolinux8')+9])
    

    printLine()
    printLog('3. Login')
    portalLogin(webDriver)

    printLine()
    printLog("4. Access Portal")
    if PORTAL_TYPE == 'admin':
        accessAdminPortal(webDriver)
        
    elif PORTAL_TYPE == 'vm':
        accessVmPortal(webDriver)

    printLine()
    printLog("5. Start Test")

    if PORTAL_TYPE == 'admin':        
        if CLUSTER_TEST == 'true':        
            printLine()
            printLog("*** Cluster Test ***")
            _cluster = admin_cluster(webDriver)
            _cluster.test()
            
            _totalResult = saveResult(_cluster._clusterResult, _totalResult)        

        if DATA_CENTER_TEST == 'true':
            printLine()
            printLog("*** Data Center Test ***")
            _data_center = admin_data_center(webDriver)
            _data_center.test()
            
            _totalResult = saveResult(_data_center._data_centerResult, _totalResult)        

        if DISK_TEST == 'true':
            printLine()
            printLog("*** Disk Test ***")
            _disk = admin_disk(webDriver)
            _disk.test()
            
            _totalResult = saveResult(_disk._diskResult, _totalResult)

        if HOST_TEST == 'true':
            printLine()
            printLog("*** Host Test ***")
            _host = admin_host(webDriver)
            _host.test()
            
            _totalResult = saveResult(_host._hostResult, _totalResult)            
        
        if DOMAIN_TEST == 'true':
            printLine()
            printLog("*** Domain Test ***")
            _domain = admin_domain(webDriver)
            _domain.test()
            
            _totalResult = saveResult(_domain._domainResult, _totalResult)        
            
        if QOS_TEST == 'true':
            printLine()
            printLog("*** QoS Test ***")
            _qos = admin_qos(webDriver)
            _qos.test()
            
            _totalResult = saveResult(_qos._qosResult, _totalResult)
        
        if VM_TEST == 'true':
            printLine()
            printLog("*** VM Test ***")
            _vm = vm_vm(webDriver)
            _vm.create()
            
            _totalResult = saveResult(_vm._vmResult, _totalResult)


    elif PORTAL_TYPE == 'vm':
        printLine()
        printLog("5.1 VM Create")
        test_vm_vm = vm_vm()
        test_vm_vm.create()

    saveTotalResult(_totalResult)
    ## 테스트 이후 결과 종합하는거 필요

    time.sleep(5)

if __name__ == '__main__':    
    
    main()