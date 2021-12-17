import time
from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By
from __test__.__admin__.__vm__ import *

class admin_vm2(admin_vm): #상속
    #def __init__(self, webDriver): 
    
    def test(self):
        print(self._vmName)
        #self.create()