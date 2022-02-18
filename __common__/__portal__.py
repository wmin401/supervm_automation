from __common__.__parameter__ import *
from __common__.__module__ import *

def accessAdminPortal(webDriver):
    printLog("* Portal : Admin Portal")
    webDriver.implicitlyWait(10)
    _adminPortal = webDriver.findElement('id','WelcomePage_webadmin',True)

def accessVmPortal(webDriver):
    printLog("* Portal : VM Portal")
    webDriver.implicitlyWait(10)
    time.sleep(1)
    _vmPortal = webDriver.findElement('id','WelcomePage_userportal_webui',True)


def accessMonitoringPortal(webDriver):
    printLog("* Portal : Monitoring Portal")
    webDriver.implicitlyWait(10)
    time.sleep(1)
    _MonitoringPortal = webDriver.findElement('id','WelcomePage_monitoringportal_webui',True)
