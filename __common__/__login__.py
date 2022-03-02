from __common__.__parameter__ import *
from selenium.webdriver.common.by import By

def portalLogin(webDriver):

    webDriver.explicitlyWait(10, By.ID, 'sso-dropdown-toggle')
    _loginDropdown = webDriver.findElement('id','sso-dropdown-toggle', True)
    
    webDriver.implicitlyWait(10)
    _loginMenu = webDriver.findElement('css_selector','body > header > div > div > ul > li > a', True)    

    _userID = webDriver.findElement('id','username')
    webDriver.implicitlyWait(10)
    _userID.send_keys(USER_ID)

    _userPW = webDriver.findElement('id','password')
    webDriver.implicitlyWait(10)
    _userPW.send_keys(USER_PW)

    _profile = webDriver.findElement('id', 'profile', True)
    _options = _profile.find_elements_by_tag_name('option')
    for opt in _options:
        if opt.text == 'internal':
            opt.click()

    webDriver.implicitlyWait(10)
    _loginBtn = webDriver.findElement('css_selector','#loginForm > div.pf-c-form__group.pf-m-action > button',True)

