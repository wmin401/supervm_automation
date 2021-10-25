from __common__.__parameter__ import *

def access_admin_portal(webDriver):
    print("* Portal : Admin Portal")
    webDriver.waitUntilFindElement(10)
    adminPortal = webDriver.findElement('id','WelcomePage_webadmin',True)

def access_vm_portal(webDriver):
    print("* Portal : VM Portal")
    webDriver.waitUntilFindElement(10)
    vmPortal = webDriver.findElement('id','WelcomePage_userportal_webui',True)
