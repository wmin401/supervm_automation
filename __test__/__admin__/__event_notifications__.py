from __common__.__parameter__ import *
from __common__.__module__ import *
from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

'''
    작성자 : Infra QA 김정현
'''

class admin_event_notifications: # 모두 소문자
    def __init__(self, webDriver):
        self._eventNotificationsResult = [] # lowerCamelCase 로
        self.webDriver = webDriver
        self._adminAccount = "admin"
        # self._sampleName = 'auto_sample_'+randomString() # 필요할 경우 사용
        self.tl = testlink()
    def test(self):
        self.setup()
        self.enableNotifications()
        time.sleep(0.3)

    def setup(self):
        # 이벤트 알림 설정 창 접근

        # 관리 클릭
        printLog("[SETUP] Administration - Users ")
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('xpath','/html/body/div[3]/div[3]/div/ul/li[5]/a/span[2]',True)

        # 사용자 클릭
        self.webDriver.explicitlyWait(10, By.ID, 'MenuView_usersAnchor')
        self.webDriver.findElement('id','MenuView_usersAnchor',True)

        # admin 계정 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.tableSearch(self._adminAccount, 4, nameClick=True) # hidden td를 1개 포함하고 있어 원래 index + 1로  감안해서 실행

        # 이벤트 공지 탭 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('xpath','/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div[1]/ul/li[5]/a', True)

        # 이벤트 관리 버튼 클릭
        self.webDriver.implicitlyWait(10)
        self.webDriver.findElement('id','DetailActionPanelView_ManageEvents',True)

        time.sleep(2)
        
    def enableNotifications(self):
        printLog(printSquare('[ENABLE NOTIFICATIONS] Enable Notifications'))
        try:
            result = ''
            msg = ''

            # 초기 상태 확인
            self.webDriver.implicitlyWait(10)
            _checkboxElement = self.webDriver.findElement('id', 'ManageEventsPopupView_tree_root0', False)
            _isSelected = _checkboxElement.is_selected()
            
            # 체크 / 체크 해제
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id', 'ManageEventsPopupView_tree_root0', True)

            # OK 버튼 클릭
            self.webDriver.implicitlyWait(10)
            self.webDriver.findElement('id','ManageEventsPopupView_OnSave', True)

            # 반영 확인
            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    # 이벤트 관리 버튼 클릭
                    self.webDriver.implicitlyWait(10)
                    self.webDriver.findElement('id','DetailActionPanelView_ManageEvents',True)

                    self.webDriver.implicitlyWait(10)
                    _checkboxElement = self.webDriver.findElement('id', 'ManageEventsPopupView_tree_root0', False)
                    _confirmSelected = _checkboxElement.is_selected()
                    
                    if _isSelected != _confirmSelected:
                        result = PASS
                        # OK 버튼 클릭
                        self.webDriver.implicitlyWait(10)
                        self.webDriver.findElement('id','ManageEventsPopupView_OnSave', True)
                        break
                    else:
                        printLog("[ENABLE NOTIFICATIONS] Enable notifications status is still applying...")
                        
                        # 취소 버튼 클릭
                        self.webDriver.implicitlyWait(10)
                        self.webDriver.findElement('id','ManageEventsPopupView_Cancel', True)
                        _endTime = time.time()
                        if _endTime - _startTime >= 60:
                            printLog("[ENABLE NOTIFICATIONS] Failed status changed : Timeout")
                            result = FAIL
                            msg = "Failed to enable notifications..."
                            break
                        else:
                            continue
                except:
                    continue

        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[ENABLE NOTIFICATIONS] MESSAGE : " + msg)
        printLog("[ENABLE NOTIFICATIONS] RESULT : " + result)
        self._eventNotificationsResult.append(['enable' + DELIM + 'notifications' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('ENABLE_NOTIFICATIONS', result, msg)