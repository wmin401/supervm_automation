import time

# SuperVM 접근 가능한 url
# SUPERVM_URL = 'https://10.0.0.7/ovirt-engine/'
SUPERVM_URL = 'https://master165.tmax.com/ovirt-engine/'

## 브라우저 정보
BROWSER_NAME = 'chrome'
BROWSER_VERSION = 95
BROWSER_BIT = 32 ## 32비트 또는 64비트 ## firefox만 사용

## 로그인 정보
USER_ID = 'admin'
USER_PW = 'asdf'

# 접속할 포털
PORTAL_TYPE = 'admin'

# 테스트 실행여부
CLUSTER_TEST = 'false'
DATA_CENTER_TEST = 'false'
DISK_TEST = 'false'
HOST_TEST = 'false'
DOMAIN_TEST = 'false'
QOS_TEST = 'false'

VM_TEST = 'false'

# 결과 저장용
now = time.localtime()
RESULT_PATH = 'results'
RESULT_FILE = 'SuperVM_Result_%04d%02d%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday)
TMP_RESULT_FILE = 'tmp_SuperVM_Result_%04d%02d%02d_%02d%02d%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
LOG_FILE = RESULT_PATH + '/log/SuperVM_Automation_log_%04d%02d%02d_%02d%02d%02d.log'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
DELIM = ';'
PASS = 'PASS'
FAIL = 'FAIL'
BLOCK = 'BLOCK'