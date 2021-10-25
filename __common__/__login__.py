from __common__.__parameter__ import *

def portalLogin(webDriver):

    webDriver.waitUntilFindElement(10)
    _loginDropdown = webDriver.findElement('id','sso-dropdown-toggle', True)
    
    webDriver.waitUntilFindElement(10)
    _loginMenu = webDriver.findElement('css_selector','body > header > div > div > ul > li > a', True)    

    _userID = webDriver.findElement('id','username')
    webDriver.waitUntilFindElement(10)
    _userID.send_keys(USER_ID)

    _userPW = webDriver.findElement('id','password')
    webDriver.waitUntilFindElement(10)
    _userPW.send_keys(USER_PW)

    webDriver.waitUntilFindElement(10)
    _loginBtn = webDriver.findElement('css_selector','#loginForm > div.pf-c-form__group.pf-m-action > button',True)

