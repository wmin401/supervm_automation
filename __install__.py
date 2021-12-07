from __common__.__batch__ import *
from __common__.__module__ import secToHms
from __common__.__parameter__ import *
from __common__.__ssh__ import *

### To do list ###
# 사용자의 입력이 필요한 것들은 모두 변수로 입력받을 수 있도록 변경 가능. 현재는 테스트용으로 직접 입력했음
# 이후 코드가 완성되면 id, pw, ip 등은 모두 입력받을 수 있도록 변경될 예정

# 윈도우 노드 hosts에 내용 추가하는거 필요

class install():

    def __init__(self):
        self.ssh = ssh_connection(ENGINE_IP, 22, ENGINE_ID, ENGINE_PW)        
        self.ssh.activate()     

    def ifDeployed(self):    
        print("[DEPLOY] Check if SuperVM is deployed")
        print("[DEPLOY] hosted-engine --vm-status")
        o, e = self.ssh.commandExec('hosted-engine --vm-status')
        for i in o:
            print(i)
        for i in o:
            if 'good' in i:
                print('[DEPLOY] SuperVM is already deployed ')
                print('[DEPLOY] SuperVM installation will be finished')
                return True
        
        return False

    def setNode(self):        
        print("[SET NODE] Initialize windows node")
        # hosts 파일에 host fqdn 추가
        # 존재할경우 하지 않음
        o, e = batchCommand('for /f "delims=" %%i in (%s\system32\drivers\etc\hosts) do echo %%i'%(SYSTEM_ROOT))
        for i in o:
            if ENGINE_IP in i:
                print("[SET NODE] Windows hosts file alreday has ENGINE IP")
                print("[SET NODE] Need to check windows hosts file")
                return False
        print("[SET NODE] Add FQDN in %s\system32\drivers\etc\hosts"%(SYSTEM_ROOT))
        batchCommand('echo. >> %s\system32\drivers\etc\hosts'%(SYSTEM_ROOT))
        batchCommand('echo %s %s >> %s\system32\drivers\etc\hosts'%(ENGINE_IP, HOSTNAME, SYSTEM_ROOT))
        batchCommand('echo %s %s >> %s\system32\drivers\etc\hosts'%(MASTER_IP, SUPERVM_URL, SYSTEM_ROOT))

    def setup(self):
        result = FAIL
        print("[SETUP] Initialize engine")
        try:
            # hostname 변경
            self.ssh.commandExec('hostnamectl set-hostname %s'%(HOSTNAME))

            # hosts에 fqdn 추가
            o, e = self.ssh.commandExec('cat /etc/hosts')
            hosts = True
            # hosts에 입력한 ip가 있는지 확인 후 없을 때만 추가
            for i in o:
                if ENGINE_IP in i:
                    print('[SETUP] Engine VM IP is already using !!!')
                    print('[SETUP] Check /etc/hosts file in engine vm !!!')
                    hosts = False
                    break
            if hosts == True:
                print("[SETUP] Add hosts")
                self.ssh.commandExec('echo "%s %s" >> /etc/hosts'%(ENGINE_IP, HOSTNAME))
                self.ssh.commandExec('echo "%s %s" >> /etc/hosts'%(MASTER_IP, SUPERVM_URL))

            o, e = self.ssh.commandExec('ls /etc/yum.repos.d/supervm.repo')
            repo = True
            if  o != [] and 'supervm.repo' in o[0]:
                print('[SETUP] supervm.repo is already exists !!!')
                print('[SETUP] Check supervm.repo file !!!')
                repo = False            
            if repo == True:
                # supervm repository 생성
                print("[SETUP] Make /etc/yum.repos.d/supervm.repo")
                self.ssh.commandExec('echo "[supervm]" >> /etc/yum.repos.d/supervm.repo')
                self.ssh.commandExec('echo "name=supervm-repo" >> /etc/yum.repos.d/supervm.repo')
                self.ssh.commandExec('echo "baseurl=%s" >> /etc/yum.repos.d/supervm.repo'%(SUPERVM_REPO_URL))
                self.ssh.commandExec('echo "gpgcheck=0" >> /etc/yum.repos.d/supervm.repo')
                print("[SETUP] dnf update ")
                self.ssh.commandExec('dnf clean all')
                self.ssh.commandExec('dnf update -y')

            print("[SETUP] Install ovirt-hosted-engine-setup")
            self.ssh.commandExec('sudo dnf module disable virt -y', t=21600 )
            self.ssh.commandExec('sudo dnf module enable pki-deps postgresql:12 parfait -y', t=21600)
            self.ssh.commandExec('systemctl enable --now libvirtd cockpit.socket')
            self.ssh.commandExec('dnf install -y ovirt-hosted-engine-setup', t=21600)
            o, e = self.ssh.commandExec('rpm -q ovirt-hosted-engine-setup')
            if 'ovirt-hosted-engine-setup' in o[0] and 'not installed' not in o[0]:
                print("[SETUP] Successfully installed ovirt packages")
                result = PASS
            else:
                print("[SETUP] Failed install ovirt packages")
                result = FAIL
        except Exception as e:            
            result = FAIL
            print("[SETUP] ERROR : %s"%(str(e)))
        
    def answers(self):
        result = FAIL
        print("[ANSWERS] Make answers.conf file")
        try:
            o, e = self.ssh.commandExec('dnf -y install ovirt-hosted-engine-setup', t=3600)        
            o, e = self.ssh.commandExec('ls /etc/sysconfig/network-scripts/ |grep "ifcfg-e"')        
            self.NETWORK_NAME = o[0][6:] 
            print("[ANSWERS] NETWORK NAME = %s"%self.NETWORK_NAME)
            
            o, e = self.ssh.commandExec('python3.6 -c "from ovirt_hosted_engine_setup import util as ohostedutil; print(ohostedutil.randomMAC())"')        
            self.MAC_ADDRESS = o[0]
            print("[ANSWERS] MAC ADDRESS = %s"%self.MAC_ADDRESS)

            # answers.conf 파일 만들기
            o, e = self.ssh.commandExec('ls /root/answers.conf')
            if o != [] and 'answers.conf' in o[0]:
                self.ssh.commandExec('rm -rf /root/answers.conf')
                #print("* answers.conf file is already exists !!!")

            self.ssh.commandExec('echo "[environment:default]" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_CORE/deployProceed=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_CORE/screenProceed=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/adminPassword=str:asdf" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/clusterName=str:Default" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/datacenterName=str:Default" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/enableHcGlusterService=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/insecureSSL=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeIf=str:%s" >> /root/answers.conf'%(self.NETWORK_NAME))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeName=str:ovirtmgmt" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/fqdn=str:%s" >> /root/answers.conf'%(SUPERVM_URL))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/gateway=str:192.168.17.1" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/host_name=str:%s" >> /root/answers.conf'%(HOSTNAME))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test=str:ping" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_address=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_port=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/destEmail=str:root@localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpPort=str:25" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpServer=str:localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/sourceEmail=str:root@localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/LunID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/discardSupport=bool:False" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIDiscoverUser=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortal=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortalIPAddress=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortalPort=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSIPortalUser=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/iSCSITargetName=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/imgSizeGB=str:120" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/imgUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/lockspaceImageUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/lockspaceVolumeUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/metadataImageUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/metadataVolumeUUID=none:None" >> /root/answers.conf')

            # nfs / ceph 설정
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/domainType=str:%s" >> /root/answers.conf'%(DOMAIN_TYPE))
            if DOMAIN_TYPE == 'nfs':
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/nfsVersion=str:auto" >> /root/answers.conf')
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/mntOptions=str:" >> /root/answers.conf')
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainConnection=str:%s:%s" >> /root/answers.conf'%(NFS_IP, NFS_PATH))
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/vfsType=str:" >> /root/answers.conf')           
                
            elif DOMAIN_TYPE == 'posixfs':                
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/nfsVersion=none:None" >> /root/answers.conf')
                # secret key 받기
                o, e = self.ssh.commandExec('ceph auth get-key client.admin')
                self.SECRET_KEY = o[0]
                print("[ANSWRES] Secret key = %s"%self.SECRET_KEY)
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/mntOptions=str:name=admin,secret=%s" >> /root/answers.conf'%(self.SECRET_KEY))
                # get storageDomainConnection path
                o, e = self.ssh.commandExec('ceph fs subvolume info myfs tim1')
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
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainConnection=str:%s:%s" >> /root/answers.conf'%(self.STORAGEDOMAIN_URL, self.SUBVOLUME_PATH))
                print('[ANSWERS] Storage Domain Connection = %s:%s'%(self.STORAGEDOMAIN_URL, self.SUBVOLUME_PATH))     
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/vfsType=str:ceph" >> /root/answers.conf')           
                
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainName=str:hosted_storage" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/volUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/applyOpenScapProfile=bool:False" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/automateVMShutdown=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cdromUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudInitISO=str:generate" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitExecuteEngineSetup=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceDomainName=str:tmax.dom" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceHostName=str:%s" >> /root/answers.conf'%(SUPERVM_URL))
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitRootPwd=str:asdf" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMDNS=str:168.126.63.1" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMETCHOSTS=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMStaticCIDR=str:%s/24" >> /root/answers.conf'%(MASTER_IP))
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitVMTZ=str:Asia/Seoul" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/consoleUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/emulatedMachine=str:pc" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/nicUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/ovfArchive=str:" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/rootSshAccess=str:yes" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/rootSshPubkey=str:" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmCDRom=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmMACAddr=str:%s" >> /root/answers.conf'%(self.MAC_ADDRESS))
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmMemSizeMB=int:6144" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmVCpus=str:4" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/proLinuxRepoAddress=str:http://prolinux-repo.tmaxos.com/prolinux/8.2/os/x86_64" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/ovirtRepoAddress=str:%s" >> /root/answers.conf'%(SUPERVM_REPO_URL))

            o, e = self.ssh.commandExec('cat /root/answers.conf')
            print('[ANSWERS] cat /root/answers.conf')
            for i in o:
                print(i)
            result = PASS
        except Exception as e:            
            result = FAIL
            print("[ANSWERS] ERROR : %s"%(str(e)))

    def nfs(self):
        result = FAIL
        print("[NFS] Set nfs at %s"%(ENGINE_IP))
        try:
            o, e = self.ssh.commandExec('cat /etc/exports')
            nfs_ = True
            for i in o:
                if NFS_PATH in i:
                    print("[NFS] NFS folder already exist")
                    nfs_ = False
                    break
            if nfs_ == True:
                print("[NFS] Install nfs packages")
                self.ssh.commandExec('dnf install -y nfs-utils')
                print("[NFS] Start service for nfs")
                self.ssh.commandExec('systemctl start rpcbind')
                self.ssh.commandExec('systemctl start nfs-server')
                print("[NFS] Set nfs")
                self.ssh.commandExec('chkconfig rpcbind on')
                self.ssh.commandExec('chkconfig nfs-server on')
                self.ssh.commandExec('mkdir %s'%NFS_PATH)
                self.ssh.commandExec('echo "%s *(rw)" >> /etc/exports'%NFS_PATH)
                self.ssh.commandExec('exportfs -r')
                self.ssh.commandExec('systemctl restart nfs-server')
                self.ssh.commandExec('groupadd kvm -g 36')
                self.ssh.commandExec('useradd vdsm -u 36 -g 36')
                self.ssh.commandExec('chown -R 36:36 %s'%NFS_PATH)
                self.ssh.commandExec('chmod 777 %s'%NFS_PATH)
                o, e = self.ssh.commandExec('ls -al /nfs')
                print('[NFS] ls -al /nfs')
                for i in o:
                    print(i)
                print("[NFS] Add service to firewall")
                self.ssh.commandExec('firewall-cmd --permanent --add-service=nfs')
                self.ssh.commandExec('firewall-cmd --permanent --add-service=mountd')
                self.ssh.commandExec('firewall-cmd --permanent --add-service=rpc-bind')
                self.ssh.commandExec('firewall-cmd --reload')
            o, e = self.ssh.commandExec('firewall-cmd --list-all |grep services')
            if 'nfs' in o[0] and 'mountd' in o[0] and 'rpc-bind' in o[0]:
                print("[NFS] Successfully set nfs")
                result = PASS
            else:
                print("[NFS] Failed to set nfs")
                result = FAIL
        except Exception as e:
            print("[NFS] ERROR : %s"%(str(e)))

    def ceph(self, initialize = False):
        result = FAIL
        if initialize == True:
            print("[CEPH] Remove ceph-common and podman images")
            # 초기화 후 다시 설치            
            # ceph 삭제
            # ceph 도커 이미지 삭제
            o, e = self.ssh.commandExec('dnf -y remove ceph-common', t=3600)
            o, e = self.ssh.commandExec('podman rmi -f 557c 5b72 d324 0881 e5a6', t=3600)

        # sdb에다가 해야됨(추가해야됨)
        print("[CEPH] Set ceph to %s at %s"%(CEPH_DISK_PATH, CEPH_IP))
        try:
            print("[CEPH] Install ceph packages")
            o, e = self.ssh.commandExec('dnf -y install podman chrony lvm2 gdisk', t=3600)
            o, e = self.ssh.commandExec('systemctl start chronyd && systemctl status chronyd', t=3600)
            o, e = self.ssh.commandExec('curl --silent --remote-name --location https://github.com/ceph/ceph/raw/v15.2.10/src/cephadm/cephadm', t=3600)
            self.ssh.commandExec('chmod +x cephadm', t=3600)
            o, e = self.ssh.commandExec('dnf install -y ceph-common', t=3600)

            print("[CEPH] Set ceph")
            o, e = self.ssh.commandExec('./cephadm --image docker.io/ceph/ceph:v15.2.10 bootstrap --mon-ip %s --allow-fqdn-hostname'%(CEPH_IP), t=3600)
            o, e = self.ssh.commandExec('sgdisk --zap-all %s'%(CEPH_DISK_PATH), t=3600)
            o, e = self.ssh.commandExec('dd if=/dev/zero of=%s bs=1M count=100 oflag=direct,dsync'%(CEPH_DISK_PATH))
            o, e = self.ssh.commandExec('blkdiscard %s'%(CEPH_DISK_PATH), t=3600)

            o, e = self.ssh.commandExec('ls /dev/mapper/ceph-* | xargs -I% -- dmsetup remove %', t=3600)
            self.ssh.commandExec('rm -rf /dev/ceph-*', t=3600)

            o, e = self.ssh.commandExec('ceph orch device ls --refresh', t=3600)

            print("[CEPH] Make /root/osd_%s file"%(HOSTNAME))
            o, e = self.ssh.commandExec('ls /root/osd_%s.yaml'%(HOSTNAME))
            if o != [] and '/root/osd_%s.yaml'%HOSTNAME == o[0].replace('\n',''):
                self.ssh.commandExec('rm -rf /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('touch /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('echo "service_type: osd" >> /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('echo "service_id: osd_%s" >> /root/osd_%s.yaml'%(HOSTNAME, HOSTNAME))
            self.ssh.commandExec('echo "placement:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('echo " hosts:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('echo " - %s" >> /root/osd_%s.yaml'%(HOSTNAME, HOSTNAME))
            self.ssh.commandExec('echo "data_devices:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('echo " paths:" >> /root/osd_%s.yaml'%(HOSTNAME))
            self.ssh.commandExec('echo " - %s" >> /root/osd_%s.yaml'%(CEPH_DISK_PATH,HOSTNAME))
            o, e = self.ssh.commandExec('ceph orch apply osd -i /root/osd_%s.yaml'%HOSTNAME, t=3600)
            
            print("[CEPH] Config ceph")
            o, e = self.ssh.commandExec('ceph osd pool set device_health_metrics size 1', t=3600)
            o, e = self.ssh.commandExec('ceph osd pool create replicapool 32 32 replicated', t=3600)
            o, e = self.ssh.commandExec('ceph osd pool set replicapool size 1', t=3600)            
            o, e = self.ssh.commandExec('rbd pool init replicapool', t=3600)

            o, e = self.ssh.commandExec('ceph osd pool create myfs-metadata 32 32 replicated', t=3600)
            o, e = self.ssh.commandExec('ceph osd pool create myfs-data0 8 8 replicated', t=3600)
            o, e = self.ssh.commandExec('ceph osd pool set myfs-metadata size 1', t=3600)
            o, e = self.ssh.commandExec('ceph osd pool set myfs-data0 size 1', t=3600)

            o, e = self.ssh.commandExec('ceph orch apply mds myfs --placement="1 %s"'%HOSTNAME, t=3600)
            o, e = self.ssh.commandExec('ceph fs new myfs myfs-metadata myfs-data0', t=3600)

            o, e = self.ssh.commandExec('ceph fs subvolume create myfs tim1 --size 322122547200 --uid 36 --gid 36', t=3600)
            o, e = self.ssh.commandExec('ceph fs subvolume info myfs tim1', t=3600)
            print('[CEPH] ceph fs subvolume info myfs tim1')
            for i in o:
                print(i)
                i = i.split(":")
                #'    "state": "complete",'
                if 'state' in i[0]:
                    if 'complete' in i[1]:
                        result = PASS
                        break
                    else:
                        result  = FAIL
            if result == PASS:
                print('[CEPH] Successfully set ceph')
            else:
                print('[CEPH] Failed to set ceph')                   

        except Exception as e:
            result = FAIL
            print("[CEPH] ERROR : %s"%(str(e)))

    def deploy(self):
        result = FAIL
        print("[DEPLOY] Start deploy")   
        print("[DEPLOY] This task needs a lot of time. So you must need to wait")
        print("[DEPLOY] If you want to see the progress of installation, see /var/log/ovirt-hosted-engine-setup/ovirt-hosted-engine-setup-{date}.log file")   
        print("[DEPLOY] ex). tail -f /var/log/ovirt-hosted-engine-setup/ovirt-hosted-engine-setup-{date}.log")   

        try:
            self.ssh.commandExec('hosted-engine --deploy --config-append=answers.conf', t = 216000, pty = True)
            print("[DEPLOY] Deploy finished")

            if self.ifDeployed():
                result = PASS
                print("[DEPLOY] Successfully finished deploy")    
            else:
                result = FAIL
                print("[DEPLOY] Failed to deploy, check log file")

        except Exception as e:
            result = FAIL
            print("[DEPLOY] ERROR : %s"%(str(e)))
        # ssh 연결 해제
        self.ssh.deactivate()        
        time.sleep(5)

def main():

    if INSTALL_SUPERVM == 'true':
        install_time = time.time()
        try:
            a = install()
            # a.setNode() # 현재는 제외
            if not a.ifDeployed():
                a.setup()
                if DOMAIN_TYPE == 'nfs':
                    a.nfs()
                elif DOMAIN_TYPE == 'posixfs':
                    a.ceph(initialize=True)
                a.answers()
                a.deploy()
                h, m, s = secToHms(install_time, time.time())
                print("* DEPLOY TIME : %dh %dm %.2fs"%(h, m, s))
        except:
            print('[ERROR] Somthing wrong!')
            return
    else:
        print("* It didn't execute SuperVM installation")

if __name__ == "__main__":        

    main()

        