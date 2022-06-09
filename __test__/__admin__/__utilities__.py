from __common__.__parameter__ import *
from __common__.__module__ import *
from __common__.__ssh__ import *

from selenium.webdriver.common.by import By

from __common__.__testlink__ import *

'''
    작성자 : Infra QA 김정현
'''

class admin_utilities: # 모두 소문자
    def __init__(self):
        self._utilitiesResult = [] # lowerCamelCase 로
        self._engineConfigOutput = 'AffinityRulesEnforcementManagerEnabled'
        self._engineConfigKeyName = 'IsIncrementalBackupSupported'
        self._engineConfigKeyValue = 'true'
        self._engineConfigVersion = '4.2'
        self._engineUpStatus = 'active'
        self.tl = testlink()

    def test(self):
        self.engine_configuration_tool()

    def engine_configuration_tool(self):
        printLog(printSquare('Engine Configuration Tool'))
        try:
            result = ''
            msg = ''
            ssh = ssh_connection('192.168.17.165', 22, 'root', 'asdf')
            ssh.activate()

            printLog("[ENGINE CONFIGURATION TOOL] List option")
            _list_option_output, _list_option_error = ssh.commandExec('engine-config --list')
            if self._engineConfigOutput not in _list_option_output[0]:
                result = FAIL
                msg = _list_option_error
            else:
                printLog("[ENGINE CONFIGURATION TOOL] List option - OK")

            printLog("[ENGINE CONFIGURATION TOOL] All option")
            _all_option_output, _all_option_error = ssh.commandExec('engine-config --all')
            if self._engineConfigOutput not in _all_option_output[0]:
                result = FAIL
                msg = _all_option_error
            else:
                printLog("[ENGINE CONFIGURATION TOOL] All option - OK")

            printLog("[ENGINE CONFIGURATION TOOL] Get option")
            _get_option_output, _get_option_error = ssh.commandExec('engine-config --get ' + self._engineConfigOutput)
            if self._engineConfigOutput not in _get_option_output[0]:
                result = FAIL
                msg = _get_option_error
            else:
                printLog("[ENGINE CONFIGURATION TOOL] Get option - OK")

            printLog("[ENGINE CONFIGURATION TOOL] Set option")
            ssh.commandExec('engine-config --set ' +  self._engineConfigKeyName + '=' + self._engineConfigKeyValue + ' --cver=' + self._engineConfigVersion)
            _set_option_output, _set_option_error = ssh.commandExec('engine-config --get ' + self._engineConfigKeyName)
            if self._engineConfigKeyValue not in _set_option_output[0]:
                result = FAIL
                msg = _set_option_error
            else:
                printLog("[ENGINE CONFIGURATION TOOL] Set option - OK")

            printLog("[ENGINE CONFIGURATION TOOL] Check applying")
            ssh.commandExec('systemctl restart ovirt-engine.service')

            _startTime = time.time()
            while True:
                time.sleep(1)
                try:
                    _endTime = time.time()
                    if _endTime - _startTime >= 60:
                        printLog("[ENGINE CONFIGURATION TOOL] Failed status changed : Timeout")
                        result = FAIL
                        msg = "Failed to apply by engine config tool..."
                        break

                    _status_check_output, _status_check_error = ssh.commandExec('systemctl status ovirt-engine.service')
                    if self._engineUpStatus not in _status_check_output[2]:
                        printLog("[ENGINE CONFIGURATION TOOL] Engine status is still not up...")
                        continue

                    _get_option_output, _get_option_error = ssh.commandExec('engine-config --get ' + self._engineConfigKeyName)
                    if self._engineConfigKeyValue not in _get_option_output[0]:
                        printLog("[ENGINE CONFIGURATION TOOL] Engine config is still not applying...")
                        continue
                    else:
                        printLog("[ENGINE CONFIGURATION TOOL] Check applying - OK")
                        break
                except:
                    continue

            if result != FAIL:
                result = PASS

            ssh.deactivate()
        except Exception as e:
            result = FAIL
            msg = str(e).replace("\n",'')
            printLog("[ENGINE CONFIGURATION TOOL] MESSAGE : " + msg)
        printLog("[ENGINE CONFIGURATION TOOL] RESULT : " + result)
        self._utilitiesResult.append(['engine' + DELIM + 'configuration' + DELIM + 'tool' + DELIM + result + DELIM + msg])

        self.tl.junitBuilder('ENGINE_CONFIGURATION_TOOL', result, msg)
