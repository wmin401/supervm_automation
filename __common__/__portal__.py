from __common__.__parameter__ import *
from __common__.__module__ import *


## 관리 포털에 접속
def accessAdminPortal(webDriver):
    printLog("* Portal : Admin Portal")
    webDriver.implicitlyWait(10)
    _adminPortal = webDriver.findElement('id','WelcomePage_webadmin',True)

## 가상 머신 포털에 접속
def accessVmPortal(webDriver):
    printLog("* Portal : VM Portal")
    webDriver.implicitlyWait(10)
    time.sleep(1)
    _vmPortal = webDriver.findElement('id','WelcomePage_userportal_webui',True)

## 모니터링 포털에 접속
def accessMonitoringPortal(webDriver):
    printLog("* Portal : Monitoring Portal")
    webDriver.implicitlyWait(10)
    time.sleep(1)
    _MonitoringPortal = webDriver.findElement('id','WelcomePage_monitoring_grafana',True)
