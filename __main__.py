
from __import__ import *

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
    tl = testlink() # 젠킨스 오류 방지용 샘플파일 생성하기 위해
    
    printLine()
    # 테스트 시작
    printLog('1. Open Browser')
    webDriver = SuperVM_driver(headless=IF_HEADLESS) ## 젠킨스에서는 헤드리스 모드 사용 금지
    webDriver.openURL('https://' + MASTER_FQDN + '/ovirt-engine')

    time.sleep(2)
    # 비공개 -> 안전하지 않음 이동(selenium에서는 보안인증이 처리가 되어있지 않음) 
    # CA 인증서 등록 안했을 경우 -> jenkins 에서는 CA 인증서 등록을 안했기 때문에 해당 기능 추가

    if SECURE == 'false':
        webDriver.explicitlyWait(10, By.ID, 'details-button')
        webDriver.findElement('id', 'details-button', True)

        webDriver.explicitlyWait(10, By.ID, 'proceed-link')
        webDriver.findElement('id', 'proceed-link', True)

    time.sleep(2)
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
    accessAdminPortal(webDriver)
    time.sleep(3)
        
    printLine()
    printLog("5. Start Test")
    
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
    
    if TEMPLATE_TEST == 'true':
        printLine()
        printLog("*** Template Test ***")
        _template = admin_template(webDriver)
        _template.test()
        
        _totalResult = saveResult(_template._templateResult, _totalResult)
        
    if VM_TEST == 'true':
        printLine()
        printLog("*** VM 1 Test ***")
        _vm = admin_vm(webDriver)
        _vm.test()

    if VM2_TEST == 'true':
        printLine()
        printLog("*** VM 2 Test ***")
        _vm2 = admin_vm2(webDriver)
        _vm2.test()
            
        _totalResult = saveResult(_vm2._vm2Result, _totalResult)

    if VM_PORTAL_TEST == 'true':
        webDriver.openURL(MASTER_FQDN)        
        accessVmPortal(webDriver)
        printLine()
        printLog("*** VM PORTAL Test ***")
        _portal_vm = vm_vm(webDriver)
        _portal_vm.test()
        
        _totalResult = saveResult(_portal_vm._vmPortalResult, _totalResult)
        
    printLog('6. Save Result')
    saveTotalResult(_totalResult)
    ## 테스트 이후 결과 종합하는거 필요

    time.sleep(2)
    printLog('7. Test finished')

if __name__ == '__main__':    
    
    main()