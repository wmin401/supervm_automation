import os
import time

SYSTEM_ROOT = os.getenv('SystemRoot')

IN_JENKINS = os.getenv('IN_JENKINS')

######## 현재 젠킨스 테스트 중
if IN_JENKINS == 'true':    
    INSTALL_SUPERVM = os.getenv('INSTALL_SUPERVM')
    ADMIN_HOSTNAME = os.getenv('ADMIN_HOSTNAME')
    SUPERVM_REPO_URL = os.getenv('SUPERVM_REPO_URL')
    ENGINE_VM_FQDN = os.getenv('ENGINE_VM_FQDN')
    ENGINE_VM_IP = os.getenv('ENGINE_VM_IP')
    ADMIN_HOST_IP = os.getenv('ADMIN_HOST_IP')
    ADMIN_GATEWAY = os.getenv('ADMIN_GATEWAY')
    ADMIN_HOST_ID = os.getenv('ADMIN_HOST_ID')
    ADMIN_HOST_PW = os.getenv('ADMIN_HOST_PW')
    ENGINE_VM_MEMORY = os.getenv('ENGINE_VM_MEMORY')

    DOMAIN_TYPE = os.getenv('DOMAIN_TYPE')
    NFS_PATH = os.getenv('NFS_PATH')
    NFS_IP = os.getenv('NFS_IP')
    CEPH_IP = os.getenv('CEPH_IP')
    CEPH_DISK_PATH = os.getenv('CEPH_DISK_PATH')

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
    TEMPLATE_TEST = os.getenv('TEMPLATE_TEST')
    VM_TEST = os.getenv('VM_TEST')
    VM2_TEST = os.getenv('VM2_TEST')
    POOLS_TEST = os.getenv('POOLS_TEST')
    EXTERNAL_PROVIDER_TEST = os.getenv('EXTERNAL_PROVIDER_TEST')
    QUOTA_TEST = os.getenv('QUOTA_TEST')

    VM_PORTAL_TEST = os.getenv('VM_PORTAL_TEST')

    # entry point para1

    BUILD_ID = os.getenv('BUILD_ID')

    MONITORING_TEST = os.getenv('MONITORING_TEST')
    
else: # 로컬
    ENGINE_VM_FQDN = 'master165.tmax.com'
    
    ## 설치 자동화 매개변수 ##
    INSTALL_SUPERVM = 'false'
    ADMIN_HOSTNAME = 'hypervm41.tmax.dom'
    SUPERVM_REPO_URL = 'http://172.21.7.2/supervm/22.0.0-rc0/prolinux/8/arch/x86_64/'
    
    ENGINE_VM_IP = '192.168.17.165'
    ADMIN_HOST_IP = '192.168.17.41'
    ADMIN_GATEWAY = '192.168.17.1'
    ADMIN_HOST_ID = 'root'
    ADMIN_HOST_PW = 'asdf'
    ENGINE_VM_MEMORY = '4096'

    DOMAIN_TYPE = 'nfs' #posixfs
    NFS_PATH = '/nfs'
    NFS_IP = ADMIN_HOST_IP
    CEPH_IP = ADMIN_HOST_IP
    CEPH_DISK_PATH = '/dev/sdb'

    ## 테스트 자동화 매개변수 ##
    SECURE = 'false'
    ## 브라우저 정보
    BROWSER_NAME = 'chrome'
    BROWSER_VERSION = 'ver98'
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
    QOS_TEST = 'false'
    TEMPLATE_TEST = 'false'
    VM_TEST = 'false'
    VM2_TEST = 'false'
    POOLS_TEST = 'false'
    EXTERNAL_PROVIDER_TEST = 'false'
    QUOTA_TEST = 'false'
    
    VM_PORTAL_TEST = 'false'
        
    # entry point para2
    
    BUILD_ID = 'local'

    MONITORING_TEST = 'true'

#############################

# 결과 저장용
now = time.localtime()
RESULT_PATH = 'results'
RESULT_FILE = 'SuperVM_Result_%04d%02d%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday)
TMP_RESULT_FILE = 'tmp_SuperVM_Result_%04d%02d%02d_%02d%02d%02d.csv'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
LOG_FILE = RESULT_PATH + '/log/SuperVM_Automation_log_%04d%02d%02d_%02d%02d%02d.log'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
INSTALL_LOG_FILE = RESULT_PATH + '/log/SuperVM_Automation_log_install_%04d%02d%02d_%02d%02d%02d.log'%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
DELIM = ';'
PASS = 'PASS'
STOP = 'STOP'
SKIP = 'SKIP'
FAIL = 'FAIL'
BLOCK = 'BLOCK'