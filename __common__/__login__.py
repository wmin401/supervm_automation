from __common__.__parameter__ import *

def portal_login(webDriver):

    webDriver.waitUntilFindElement(10)
    loingDropdown = webDriver.findElement('id','sso-dropdown-toggle', True)
    
    webDriver.waitUntilFindElement(10)
    loginMenu = webDriver.findElement('css_selector','body > header > div > div > ul > li > a', True)    

    userID = webDriver.findElement('id','username')
    webDriver.waitUntilFindElement(10)
    userID.send_keys(USER_ID)

    userPW = webDriver.findElement('id','password')
    webDriver.waitUntilFindElement(10)
    userPW.send_keys(USER_PW)

    webDriver.waitUntilFindElement(10)
    loginBtn = webDriver.findElement('css_selector','#loginForm > div.pf-c-form__group.pf-m-action > button',True)

