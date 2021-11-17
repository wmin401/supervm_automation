import os
import time

IN_JENKINS = os.getenv('IN_JENKINS')

######## 현재 젠킨스 테스트 중
if IN_JENKINS == 'true':    
    SUPERVM_URL = os.getenv('SUPERVM_URL')
    SECURE = os.getenv('SECURE')    
    BROWSER_NAME = os.getenv('BROWSER_NAME')
    BROWSER_VERSION = os.getenv('BROWSER_VERSION')
    BROWSER_BIT = os.getenv('BROWSER_BIT')
    IF_HEADLESS = os.getenv('IF_HEADLESS')
    USER_ID = os.getenv('USER_ID')
    USER_PW = os.getenv('USER_PW')
    CLUSTER_TEST = os.getenv('CLUSTER_TEST')
    DATA_CENTER_TEST = os.getenv('DATA_CENTER_TEST')
    DISK_TEST = os.getenv('DISK_TEST')
    DOMAIN_TEST = os.getenv('DOMAIN_TEST')
    HOST_TEST = os.getenv('HOST_TEST')
    QOS_TEST = os.getenv('QOS_TEST')
    VM_TEST = os.getenv('VM_TEST')
    VM_PORTAL_TEST = os.getenv('VM_PORTAL_TEST')

    BUILD_NUMBER = os.getenv('BUILD_NUMBER')
    print(BUILD_NUMBER)
    
else: # 로컬
    SUPERVM_URL = 'https://master165.tmax.com/ovirt-engine/'

    SECURE = 'false'
    ## 브라우저 정보
    BROWSER_NAME = 'chrome'
    BROWSER_VERSION = 'ver95'
    BROWSER_BIT = 32 ## 32비트 또는 64비트 ## firefox만 사용

    IF_HEADLESS = 'false' # 헤드리스 사용 여부(사용 금지)
        
    ## 로그인 정보
    USER_ID = 'admin'
    USER_PW = 'asdf'

    # 테스트 실행여부
    CLUSTER_TEST = 'false'
    DATA_CENTER_TEST = 'false'
    DISK_TEST = 'false'
    DOMAIN_TEST = 'false'
    HOST_TEST = 'false'
    QOS_TEST = 'true'
    VM_TEST = 'false'
    VM_PORTAL_TEST = 'false'

    TESTLINK_BUILD_NAME = 'local'

#############################

# 결과 저장용
now = time.localtime()
RESULT_PATH = 'results'
RESULT_FILE = 'SuperVM_Result_%04d%02d%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday)
TMP_RESULT_FILE = 'tmp_SuperVM_Result_%04d%02d%02d_%02d%02d%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
LOG_FILE = RESULT_PATH + '/log/SuperVM_Automation_log_%04d%02d%02d_%02d%02d%02d.log'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
DELIM = ';'
PASS = 'PASS'
STOP = 'STOP'
SKIP = 'SKIP'
FAIL = 'FAIL'
BLOCK = 'BLOCK'