from __common__.__batch__ import *
from __common__.__csv__ import initResult
from __common__.__module__ import *
from __common__.__parameter__ import *
from __common__.__ssh__ import *

### To do list ###
# 사용자의 입력이 필요한 것들은 모두 변수로 입력받을 수 있도록 변경 가능. 현재는 테스트용으로 직접 입력했음
# 이후 코드가 완성되면 id, pw, ip 등은 모두 입력받을 수 있도록 변경될 예정

# 윈도우 노드 hosts에 내용 추가하는거 필요

class install():

    def __init__(self):
        self._ssh = ssh_connection(ADMIN_HOST_IP, 22, ADMIN_HOST_ID, ADMIN_HOST_PW)        
        self._ssh.activate()     

    def ifDeployed(self):    
        printLog("[DEPLOY] Check if SuperVM is deployed")
        printLog("[DEPLOY] hosted-engine --vm-status")
        o, e = self._ssh.commandExec('hosted-engine --vm-status')
        for i in o:
            printLog(i)
        for i in o:
            if 'good' in i:
                printLog(i)
                printLog('[DEPLOY] SuperVM is deployed ')
                return True
        
        printLog("[DEPLOY] SuperVM didn't deploy")
        return False

    def setup(self):
        _result = FAIL
        printLog("[SETUP] Initialize engine")
        try:
            # hostname 변경
            self._ssh.commandExec('hostnamectl set-hostname %s'%(HOSTNAME))

            # hosts에 fqdn 추가
            o, e = self._ssh.commandExec('cat /etc/hosts')
            _hosts = True
            # hosts에 입력한 ip가 있는지 확인 후 없을 때만 추가
            for i in o:
                if ADMIN_HOST_IP in i:
                    printLog('[SETUP] Engine VM IP is already using !!!')
                    printLog('[SETUP] Check /etc/hosts file in engine vm !!!')
                    _hosts = False
                    break
            if _hosts == True:
                printLog("[SETUP] Add hosts")
                self._ssh.commandExec('echo "%s %s" >> /etc/hosts'%(ADMIN_HOST_IP, HOSTNAME))
                self._ssh.commandExec('echo "%s %s" >> /etc/hosts'%(ENGINE_VM_IP, ENGINE_VM_FQDN))

            o, e = self._ssh.commandExec('ls /etc/yum.repos.d/supervm.repo')
            _repo = True
            if  o != [] and 'supervm.repo' in o[0]:
                printLog('[SETUP] supervm.repo is already exists !!!')
                printLog('[SETUP] Check supervm.repo file !!!')
                _repo = False            
            if _repo == True:
                # supervm repository 생성
                printLog("[SETUP] Make /etc/yum.repos.d/supervm.repo")
                self._ssh.commandExec('echo "[supervm]" >> /etc/yum.repos.d/supervm.repo')
                self._ssh.commandExec('echo "name=supervm-repo" >> /etc/yum.repos.d/supervm.repo')
                self._ssh.commandExec('echo "baseurl=%s" >> /etc/yum.repos.d/supervm.repo'%(SUPERVM_REPO_URL))
                self._ssh.commandExec('echo "gpgcheck=0" >> /etc/yum.repos.d/supervm.repo')
                printLog("[SETUP] dnf update ")
                self._ssh.commandExec('dnf clean all')
                self._ssh.commandExec('dnf update -y')

            printLog("[SETUP] Install ovirt-hosted-engine-setup")
            self._ssh.commandExec('sudo dnf module disable virt -y', t=21600 )
            self._ssh.commandExec('sudo dnf module enable pki-deps postgresql:12 parfait -y', t=21600)
            self._ssh.commandExec('systemctl enable --now libvirtd cockpit.socket')
            self._ssh.commandExec('dnf install -y ovirt-hosted-engine-setup', t=21600)
            o, e = self._ssh.commandExec('rpm -q ovirt-hosted-engine-setup')
            if 'ovirt-hosted-engine-setup' in o[0] and 'not installed' not in o[0]:
                printLog("[SETUP] Successfully installed ovirt packages")
                _result = PASS
            else:
                printLog("[SETUP] Failed install ovirt packages")
                _result = FAIL
        except Exception as e:            
            _result = FAIL
            printLog("[SETUP] ERROR : %s"%(str(e)))
           
    def nfs(self):
        _result = FAIL
        printLog("[NFS] Set nfs at %s"%(ADMIN_HOST_IP))
        try:
            o, e = self._ssh.commandExec('cat /etc/exports')
            _nfs = True
            for i in o:
                if NFS_PATH in i:
                    printLog("[NFS] NFS folder already exist")
                    _nfs = False
                    break
            if _nfs == True:
                printLog("[NFS] Install nfs packages")
                self._ssh.commandExec('dnf install -y nfs-utils')
                printLog("[NFS] Start service for nfs")
                self._ssh.commandExec('systemctl start rpcbind')
                self._ssh.commandExec('systemctl start nfs-server')
                printLog("[NFS] Set nfs")
                self._ssh.commandExec('chkconfig rpcbind on')
                self._ssh.commandExec('chkconfig nfs-server on')
                self._ssh.commandExec('mkdir %s'%NFS_PATH)
                self._ssh.commandExec('echo "%s *(rw)" >> /etc/exports'%NFS_PATH)
                self._ssh.commandExec('exportfs -r')
                self._ssh.commandExec('systemctl restart nfs-server')
                self._ssh.commandExec('groupadd kvm -g 36')
                self._ssh.commandExec('useradd vdsm -u 36 -g 36')
                self._ssh.commandExec('chown -R 36:36 %s'%NFS_PATH)
                self._ssh.commandExec('chmod 777 %s'%NFS_PATH)
                o, e = self._ssh.commandExec('ls -al /nfs')
                printLog('[NFS] ls -al /nfs')
                for i in o:
                    printLog(i)
                printLog("[NFS] Add service to firewall")
                self._ssh.commandExec('firewall-cmd --permanent --add-service=nfs')
                self._ssh.commandExec('firewall-cmd --permanent --add-service=mountd')
                self._ssh.commandExec('firewall-cmd --permanent --add-service=rpc-bind')
                self._ssh.commandExec('firewall-cmd --reload')
            o, e = self._ssh.commandExec('firewall-cmd --list-all |grep services')
            if 'nfs' in o[0] and 'mountd' in o[0] and 'rpc-bind' in o[0]:
                printLog("[NFS] Successfully set nfs")
                _result = PASS
            else:
                printLog("[NFS] Failed to set nfs")
                _result = FAIL
        except Exception as e:
            printLog("[NFS] ERROR : %s"%(str(e)))

    def ceph(self, initialize = False):
        _result = FAIL
        if initialize == True:
            printLog("[CEPH] Remove ceph-common and podman images")
            # 초기화 후 다시 설치            
            # ceph 삭제
            # ceph 도커 이미지 삭제
            o, e = self._ssh.commandExec('dnf -y remove ceph-common', t=3600)
            o, e = self._ssh.commandExec('podman rmi -f 557c 5b72 d324 0881 e5a6', t=3600)

        # sdb에다가 해야됨(추가해야됨)
        printLog("[CEPH] Set ceph to %s at %s"%(CEPH_DISK_PATH, CEPH_IP))
        try:
            printLog("[CEPH] Install ceph packages")
            o, e = self._ssh.commandExec('dnf -y install podman chrony lvm2 gdisk', t=3600)
            o, e = self._ssh.commandExec('systemctl start chronyd && systemctl status chronyd', t=3600)
            o, e = self._ssh.commandExec('curl --silent --remote-name --location https://github.com/ceph/ceph/raw/v15.2.10/src/cephadm/cephadm', t=3600)
            self._ssh.commandExec('chmod +x cephadm', t=3600)
            o, e = self._ssh.commandExec('dnf install -y ceph-common', t=3600)

            printLog("[CEPH] Set ceph")
            o, e = self._ssh.commandExec('./cephadm --image docker.io/ceph/ceph:v15.2.10 bootstrap --mon-ip %s --allow-fqdn-hostname'%(CEPH_IP), t=3600)
            o, e = self._ssh.commandExec('sgdisk --zap-all %s'%(CEPH_DISK_PATH), t=3600)
            o, e = self._ssh.commandExec('dd if=/dev/zero of=%s bs=1M count=100 oflag=direct,dsync'%(CEPH_DISK_PATH))
            o, e = self._ssh.commandExec('blkdiscard %s'%(CEPH_DISK_PATH), t=3600)

            o, e = self._ssh.commandExec('ls /dev/mapper/ceph-* | xargs -I% -- dmsetup remove %', t=3600)
            self._ssh.commandExec('rm -rf /dev/ceph-*', t=3600)

            o, e = self._ssh.commandExec('ceph orch device ls --refresh', t=3600)

            printLog("[CEPH] Make /root/osd_%s file"%(HOSTNAME))
            o, e = self._ssh.commandExec('ls /root/osd_%s.yaml'%(HOSTNAME))
            if o != [] and '/root/osd_%s.yaml'%HOSTNAME == o[0].replace('\n',''):
                self._ssh.commandExec('rm -rf /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('touch /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('echo "service_type: osd" >> /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('echo "service_id: osd_%s" >> /root/osd_%s.yaml'%(HOSTNAME, HOSTNAME))
            self._ssh.commandExec('echo "placement:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('echo " hosts:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('echo " - %s" >> /root/osd_%s.yaml'%(HOSTNAME, HOSTNAME))
            self._ssh.commandExec('echo "data_devices:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('echo " paths:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self._ssh.commandExec('echo " - %s" >> /root/osd_%s.yaml'%(CEPH_DISK_PATH,HOSTNAME))
            o, e = self._ssh.commandExec('ceph orch apply osd -i /root/osd_%s.yaml'%HOSTNAME, t=3600)
            
            printLog("[CEPH] Config ceph")
            o, e = self._ssh.commandExec('ceph osd pool set device_health_metrics size 1', t=3600)
            o, e = self._ssh.commandExec('ceph osd pool create replicapool 32 32 replicated', t=3600)
            o, e = self._ssh.commandExec('ceph osd pool set replicapool size 1', t=3600)            
            o, e = self._ssh.commandExec('rbd pool init replicapool', t=3600)

            o, e = self._ssh.commandExec('ceph osd pool create myfs-metadata 32 32 replicated', t=3600)
            o, e = self._ssh.commandExec('ceph osd pool create myfs-data0 8 8 replicated', t=3600)
            o, e = self._ssh.commandExec('ceph osd pool set myfs-metadata size 1', t=3600)
            o, e = self._ssh.commandExec('ceph osd pool set myfs-data0 size 1', t=3600)

            o, e = self._ssh.commandExec('ceph orch apply mds myfs --placement="1 %s"'%HOSTNAME, t=3600)
            o, e = self._ssh.commandExec('ceph fs new myfs myfs-metadata myfs-data0', t=3600)

            o, e = self._ssh.commandExec('ceph fs subvolume create myfs tim1 --size 322122547200 --uid 36 --gid 36', t=3600)
            o, e = self._ssh.commandExec('ceph fs subvolume info myfs tim1', t=3600)
            printLog('[CEPH] ceph fs subvolume info myfs tim1')
            for i in o:
                printLog(i)
                i = i.split(":")
                #'    "state": "complete",'
                if 'state' in i[0]:
                    if 'complete' in i[1]:
                        _result = PASS
                        break
                    else:
                        _result  = FAIL
            if _result == PASS:
                printLog('[CEPH] Successfully set ceph')
            else:
                printLog('[CEPH] Failed to set ceph')                   

        except Exception as e:
            _result = FAIL
            printLog("[CEPH] ERROR : %s"%(str(e)))

    def answers(self):
        _result = FAIL
        printLog("[ANSWERS] Make answers.conf file")
        try:
            # answers.conf 파일 만들기
            o, e = self._ssh.commandExec('ls /root/answers.conf')
            if o != [] and 'answers.conf' in o[0]:
                self._ssh.commandExec('rm -rf /root/answers.conf')
                #printLog("* answers.conf file is already exists !!!")

            self._ssh.commandExec('echo "[environment:default]" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_CORE/deployProceed=bool:True" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_CORE/screenProceed=bool:True" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_ENGINE/adminPassword=str:asdf" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_ENGINE/clusterName=str:Default" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_ENGINE/datacenterName=str:Default" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_ENGINE/enableHcGlusterService=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_ENGINE/insecureSSL=none:None" >> /root/answers.conf')
            o, e = self._ssh.commandExec('dnf -y install ovirt-hosted-engine-setup', t=3600)        
            o, e = self._ssh.commandExec('ls /etc/sysconfig/network-scripts/ |grep "ifcfg-e"')        
            _networkName = o[0][6:] 
            printLog("[ANSWERS] NETWORK NAME = %s"%_networkName)
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeIf=str:%s" >> /root/answers.conf'%(_networkName))
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeName=str:ovirtmgmt" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/fqdn=str:%s" >> /root/answers.conf'%(ENGINE_VM_FQDN))
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/gateway=str:192.168.17.1" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/host_name=str:%s" >> /root/answers.conf'%(HOSTNAME))
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test=str:ping" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_address=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_port=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NOTIF/destEmail=str:root@localhost" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpPort=str:25" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpServer=str:localhost" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_NOTIF/sourceEmail=str:root@localhost" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/LunID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/discardSupport=bool:False" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIDiscoverUser=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortal=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortalIPAddress=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortalPort=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortalUser=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSITargetName=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/imgSizeGB=str:120" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/imgUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/lockspaceImageUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/lockspaceVolumeUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/metadataImageUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/metadataVolumeUUID=none:None" >> /root/answers.conf')

            # nfs / ceph 설정
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/domainType=str:%s" >> /root/answers.conf'%(DOMAIN_TYPE))
            if DOMAIN_TYPE == 'nfs':
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/nfsVersion=str:auto" >> /root/answers.conf')
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/mntOptions=str:" >> /root/answers.conf')
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainConnection=str:%s:%s" >> /root/answers.conf'%(NFS_IP, NFS_PATH))
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/vfsType=str:" >> /root/answers.conf')           
                
            elif DOMAIN_TYPE == 'posixfs':                
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/nfsVersion=none:None" >> /root/answers.conf')
                # secret key 받기
                o, e = self._ssh.commandExec('ceph auth get-key client.admin')
                _secretKey = o[0]
                printLog("[ANSWRES] Secret key = %s"%_secretKey)
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/mntOptions=str:name=admin,secret=%s" >> /root/answers.conf'%(_secretKey))
                # get storageDomainConnection path
                o, e = self._ssh.commandExec('ceph fs subvolume info myfs tim1')
                cnt = -1
                for i in o:
                    cnt += 1
                    i = i.split(":")
                    if 'mon_addr' in i[0]:
                        # 현재 위치에서 다음 인덱스에 값이 있기 때문에 +1
                        '''
                        "mon_addrs": [
                            "192.168.17.163:6789"
                        '''
                        idx = cnt + 1
                        self.STORAGEDOMAIN_URL = o[idx][o[idx].find('"')+1:o[idx].find('"', o[idx].find('"')+1)]
                        # ex. 192.168.17.163:6789
                    elif 'path' in i[0]:
                        # "path": "/volumes/_nogroup/tim1/c21023fe-c818-4559-9489-bcb407cb8072",    "pool_namespace": "",
                        idx = cnt
                        self.SUBVOLUME_PATH = i[1][i[1].find('"')+1:i[1].find('"', i[1].find('"')+1)]
                        # ex. /volumes/_nogroup/tim1/c21023fe-c818-4559-9489-bcb407cb8072
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainConnection=str:%s:%s" >> /root/answers.conf'%(self.STORAGEDOMAIN_URL, self.SUBVOLUME_PATH))
                printLog('[ANSWERS] Storage Domain Connection = %s:%s'%(self.STORAGEDOMAIN_URL, self.SUBVOLUME_PATH))     
                self._ssh.commandExec('echo "OVEHOSTED_STORAGE/vfsType=str:ceph" >> /root/answers.conf')           
                
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainName=str:hosted_storage" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_STORAGE/volUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/applyOpenScapProfile=bool:False" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/automateVMShutdown=bool:True" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cdromUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudInitISO=str:generate" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitExecuteEngineSetup=bool:True" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceHostName=str:%s" >> /root/answers.conf'%(ENGINE_VM_FQDN))
            _domainName = ENGINE_VM_FQDN.split('.')[1] + '.' + ENGINE_VM_FQDN.split('.')[2]
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceDomainName=str:%s" >> /root/answers.conf'%(_domainName))
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitRootPwd=str:asdf" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMDNS=str:168.126.63.1" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMETCHOSTS=bool:True" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMStaticCIDR=str:%s/24" >> /root/answers.conf'%(ENGINE_VM_IP))
            self._ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMTZ=str:Asia/Seoul" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/consoleUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/emulatedMachine=str:pc" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/nicUUID=none:None" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/ovfArchive=str:" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/rootSshAccess=str:yes" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/rootSshPubkey=str:" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/vmCDRom=none:None" >> /root/answers.conf')                        
            o, e = self._ssh.commandExec('python3.6 -c "from ovirt_hosted_engine_setup import util as ohostedutil; print(ohostedutil.randomMAC())"')        
            _macAddress = o[0]
            printLog("[ANSWERS] MAC ADDRESS = %s"%_macAddress)
            self._ssh.commandExec('echo "OVEHOSTED_VM/vmMACAddr=str:%s" >> /root/answers.conf'%(_macAddress))
            self._ssh.commandExec('echo "OVEHOSTED_VM/vmMemSizeMB=int:6144" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/vmVCpus=str:4" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/proLinuxRepoAddress=str:http://prolinux-repo.tmaxos.com/prolinux/8.2/os/x86_64" >> /root/answers.conf')
            self._ssh.commandExec('echo "OVEHOSTED_VM/ovirtRepoAddress=str:%s" >> /root/answers.conf'%(SUPERVM_REPO_URL))

            o, e = self._ssh.commandExec('cat /root/answers.conf')
            printLog('[ANSWERS] cat /root/answers.conf')
            for i in o:
                printLog(i)
            _result = PASS
        except Exception as e:            
            _result = FAIL
            printLog("[ANSWERS] ERROR : %s"%(str(e)))

    def deploy(self):
        _result = FAIL
        printLog("[DEPLOY] Start deploy")   
        printLog("[DEPLOY] This task needs a lot of time. So you must need to wait")
        printLog("[DEPLOY] If you want to see the progress of installation, see /var/log/ovirt-hosted-engine-setup/ovirt-hosted-engine-setup-{date}.log file in %s"%ADMIN_HOST_IP)   
        printLog("[DEPLOY] ex). tail -f /var/log/ovirt-hosted-engine-setup/ovirt-hosted-engine-setup-{date}.log")   

        try:
            self._ssh.commandExec('hosted-engine --deploy --config-append=answers.conf', t = 216000, pty = True)
            printLog("[DEPLOY] Deploy finished")
            time.sleep(10)
            if self.ifDeployed():
                _result = PASS
                printLog("[DEPLOY] Successfully finished deploy")    
            else:
                _result = FAIL
                printLog("[DEPLOY] Failed to deploy, check log file")

        except Exception as e:
            _result = FAIL
            printLog("[DEPLOY] ERROR : %s"%(str(e)))
        # ssh 연결 해제
        self._ssh.deactivate()        
        time.sleep(5)

    def cleanup(self): 
        # deploy 실패시 자동 실행(1안)
        # deploy 이전에 실행(2안)
        printLog("[CLEANUP] Start cleanup using ovirt-hosted-engine-cleanup")   
        o, e = self._ssh.commandExec('ovirt-hosted-engine-cleanup -q', t=216000) # -q : 사용자 입력없이 실행되는 옵션
        for i in o:
            print(i)
        



def main():

    initResult()

    if INSTALL_SUPERVM == 'true':
        install_time = time.time()
        try:
            supervm = install()
            # a.setNode() # 현재는 제외
            if not supervm.ifDeployed():
                supervm.setup()
                if DOMAIN_TYPE == 'nfs':
                    supervm.nfs()
                elif DOMAIN_TYPE == 'posixfs':
                    supervm.ceph(initialize=False) ## 아직 기능이 확실하지 않음
                supervm.answers()
                supervm.deploy()
                h, m, s = secToHms(install_time, time.time())
                printLog("* DEPLOY TIME : %dh %dm %.2fs"%(h, m, s))
        except:
            printLog('[ERROR] Somthing wrong!')
            return
    else:
        printLog("* It didn't execute SuperVM installation")

if __name__ == "__main__":        

    main()