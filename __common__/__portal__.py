from __common__.__parameter__ import *

def accessAdminPortal(webDriver):
    print("* Portal : Admin Portal")
    webDriver.waitUntilFindElement(10)
    _adminPortal = webDriver.findElement('id','WelcomePage_webadmin',True)

def accessVmPortal(webDriver):
    print("* Portal : VM Portal")
    webDriver.waitUntilFindElement(10)
    _vmPortal = webDriver.findElement('id','WelcomePage_userportal_webui',True)
