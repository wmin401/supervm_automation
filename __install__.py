from __common__.__module__ import secToHms
from __common__.__parameter__ import *
from __common__.__ssh__ import *

### To do list ###
# 1. deploy check?
# 2. 



class install():

    def __init__(self):
        self.ENGINE_NUM = ENGINE_IP.split('.')[3] # ***.***.***.***
        self.MASTER_NUM = MASTER_IP.split('.')[3]
        self.HOSTNAME = 'supervm%s.tmax.dom'%self.ENGINE_NUM
        self.FQDN = 'master%s.tmax.dom'%self.MASTER_NUM
        self.STORAGE_TYPE = 'ceph'
        # engine vm에 ssh연결
        self.ssh = ssh_connection(ENGINE_IP, 22, ENGINE_ID, ENGINE_PW)        
        self.ssh.activate() 

    def setup(self):
        print("[SETUP] Initialize engine")
        try:
            # hostname 변경
            self.ssh.commandExec('hostnamectl set-hostname %s'%(self.HOSTNAME))

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
                self.ssh.commandExec('echo "%s %s" >> /etc/hosts'%(ENGINE_IP, self.HOSTNAME))
                self.ssh.commandExec('echo "%s %s" >> /etc/hosts'%(MASTER_IP, self.FQDN))

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
            else:
                print("[SETUP] Failed install ovirt packages")
        except Exception as e:            
            print("[SETUP] ERROR : %s"%(str(e)))
        
    def answers(self):
        print("[ANSWERS] Make answers.conf file")
        try:
            o, e = self.ssh.commandExec('ls /etc/sysconfig/network-scripts/ |grep "ifcfg-e"')        
            self.networkName = o[0][6:] 
            print("[ANSWERS] NETWORK NAME = %s"%self.networkName)
            
            o, e = self.ssh.commandExec('python3.6 -c "from ovirt_hosted_engine_setup import util as ohostedutil; print(ohostedutil.randomMAC())"')        
            self.macAddress = o[0]
            print("[ANSWERS] MAC ADDRESS = %s"%self.macAddress)

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
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeIf=str:%s" >> /root/answers.conf'%(self.networkName))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeName=str:ovirtmgmt" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/fqdn=str:%s" >> /root/answers.conf'%(self.FQDN))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/gateway=str:192.168.17.1" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/host_name=str:%s" >> /root/answers.conf'%(self.HOSTNAME))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test=str:ping" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_address=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_port=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/destEmail=str:root@localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpPort=str:25" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpServer=str:localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/sourceEmail=str:root@localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/LunID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/discardSupport=bool:False" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/domainType=str:%s" >> /root/answers.conf'%(self.STORAGE_TYPE))
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
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/mntOptions=str:" >> /root/answers.conf')
            if self.STORAGE_TYPE == 'nfs':
                self.ssh.commandExec('echo "OVEHOSTED_STORAGE/nfsVersion=str:auto" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainConnection=str:%s:/%s" >> /root/answers.conf'%(ENGINE_IP, self.STORAGE_TYPE))
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainName=str:hosted_storage" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/vfsType=str:" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/volUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/applyOpenScapProfile=bool:False" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/automateVMShutdown=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cdromUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudInitISO=str:generate" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitExecuteEngineSetup=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceDomainName=str:tmax.dom" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceHostName=str:%s" >> /root/answers.conf'%(self.FQDN))
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
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmMACAddr=str:%s" >> /root/answers.conf'%(self.macAddress))
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmMemSizeMB=int:6144" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/vmVCpus=str:4" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/proLinuxRepoAddress=str:http://prolinux-repo.tmaxos.com/prolinux/8.2/os/x86_64" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/ovirtRepoAddress=str:%s" >> /root/answers.conf'%(SUPERVM_REPO_URL))
        except Exception as e:            
            print("[ANSWERS] ERROR : %s"%(str(e)))

    def nfs(self):
        print("[NFS] Set nfs at %s"%(ENGINE_IP))
        try:
            o, e = self.ssh.commandExec('cat /etc/exports')
            nfs_ = True
            for i in o:
                if '/nfs' in i:
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
                self.ssh.commandExec('mkdir /nfs')
                self.ssh.commandExec('echo "/nfs *(rw)" >> /etc/exports')
                self.ssh.commandExec('exportfs -r')
                self.ssh.commandExec('systemctl restart nfs-server')
                self.ssh.commandExec('groupadd kvm -g 36')
                self.ssh.commandExec('useradd vdsm -u 36 -g 36')
                self.ssh.commandExec('chown -R 36:36 /nfs')
                self.ssh.commandExec('chmod 777 /nfs')
                print("[NFS] Add service to firewall")
                self.ssh.commandExec('firewall-cmd --permanent --add-service=nfs')
                self.ssh.commandExec('firewall-cmd --permanent --add-service=mountd')
                self.ssh.commandExec('firewall-cmd --permanent --add-service=rpc-bind')
                self.ssh.commandExec('firewall-cmd --reload')
            o, e = self.ssh.commandExec('firewall-cmd --list-all |grep services')
            if 'nfs' in o[0] and 'mountd' in o[0] and 'rpc-bind' in o[0]:
                print("[NFS] Successfully set nfs")
        except Exception as e:
            print("[NFS] ERROR : %s"%(str(e)))

    def ceph(self):
        # sdb에다가 해야됨(추가해야됨)
        CEPH_IP = ENGINE_IP
        CEPH_DISK_PATH = '/dev/sdb'
        print("[CEPH] Set ceph to %s at %s"%(CEPH_DISK_PATH, CEPH_IP))
        try:
            print("[CEPH] Install ceph packages")
            o, e = self.ssh.commandExec('dnf -y install podman chrony lvm2 gdisk')
            o, e = self.ssh.commandExec('systemctl start chronyd && systemctl status chronyd')
            o, e = self.ssh.commandExec('curl --silent --remote-name --location https://github.com/ceph/ceph/raw/v15.2.10/src/cephadm/cephadm')
            self.ssh.commandExec('chmod +x cephadm')
            o, e = self.ssh.commandExec('dnf install -y ceph-common')

            print("[CEPH] Set ceph")
            o, e = self.ssh.commandExec('./cephadm --image docker.io/ceph/ceph:v15.2.10 bootstrap --mon-ip %s --allow-fqdn-hostname'%(CEPH_IP))
            o, e = self.ssh.commandExec('sgdisk --zap-all %s'%(CEPH_DISK_PATH))
            o, e = self.ssh.commandExec('dd if=/dev/zero of=%s bs=1M count=100 oflag=direct,dsync'%(CEPH_DISK_PATH))
            o, e = self.ssh.commandExec('blkdiscard %s'%(CEPH_DISK_PATH))

            # o, e = self.ssh.commandExec('ls /dev/mapper/ceph-* | xargs -I% -- dmsetup remove %')
            # self.ssh.commandExec('rm -rf /dev/ceph-*')

            # o, e = self.ssh.commandExec('ceph orch device ls --refresh')

            # print("[CEPH] Make /root/osd_%s file"%(self.HOSTNAME))
            # o, e = self.ssh.commandExec('ls /root/osd_%s.yaml'%(self.HOSTNAME))
            # if o != [] and '/root/osd_%s.yaml'%self.HOSTNAME == o[0].replace('\n',''):
            #     self.ssh.commandExec('rm -rf /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('touch /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('echo "service_type: osd" >> /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('echo "service_id: osd_%s" >> /root/osd_%s.yaml'%(self.HOSTNAME, self.HOSTNAME))
            # self.ssh.commandExec('echo "placement:" >> /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('echo " hosts:" >> /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('echo " - %s" >> /root/osd_%s.yaml'%(self.HOSTNAME, self.HOSTNAME))
            # self.ssh.commandExec('echo "data_devices:" >> /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('echo " paths:" >> /root/osd_%s.yaml'%(self.HOSTNAME))
            # self.ssh.commandExec('echo " - %s" >> /root/osd_%s.yaml'%(CEPH_DISK_PATH,self.HOSTNAME))
            # o, e = self.ssh.commandExec('ceph orch apply osd -i /root/osd_%s.yaml'%self.HOSTNAME)
            
            # print("[CEPH] Config ceph")
            # o, e = self.ssh.commandExec('ceph osd pool set device_health_metrics size 1')
            # o, e = self.ssh.commandExec('ceph osd pool create replicapool 32 32 replicated')
            # o, e = self.ssh.commandExec('ceph osd pool set replicapool size 1')
            
            # o, e = self.ssh.commandExec('rbd pool init replicapool')

            # o, e = self.ssh.commandExec('ceph osd pool create myfs-metadata 32 32 replicated')
            # o, e = self.ssh.commandExec('ceph osd pool create myfs-data0 8 8 replicated')
            # o, e = self.ssh.commandExec('ceph osd pool set myfs-metadata size 1')
            # o, e = self.ssh.commandExec('ceph osd pool set myfs-data0 size 1')

            # o, e = self.ssh.commandExec('ceph orch apply mds myfs --placement="1 %s"'%self.HOSTNAME)

            # o, e = self.ssh.commandExec('ceph fs new myfs myfs-metadata myfs-data0')
            # o, e = self.ssh.commandExec('ceph fs subvolume create myfs tim1 --size 322122547200 --uid 36 --gid 36')
            # o, e = self.ssh.commandExec('ceph fs subvolume info myfs tim1')
            # for i in o:
            #     print(i)
        except Exception as e:
            print("[CEPH] ERROR : %s"%(str(e)))

    def deploy(self):
        print("[DEPLOY] Start deploy")   
        print("[DEPLOY] This task needs a lot of time. So you must need to wait")
        print("[DEPLOY] If you want to see the progress of installation, see /var/log/ovirt-hosted-engine-setup/ovirt-hosted-engine-setup-{date}.log file")   
        print("[DEPLOY] ex). tail -f /var/log/ovirt-hosted-engine-setup/ovirt-hosted-engine-setup-{date}.log")   

        try:
            o, e = self.ssh.commandExec('hosted-engine --deploy --config-append=answers.conf', t = 216000, pty = True)

            for i in range(len(o)):
                if '' in o[len(o)-1]:
                    result = PASS
                else:
                    result = FAIL
            print("[DEPLOY] Deploy finished")
            if result == PASS:
                print("[DEPLOY] Successfully finished deploy")    
            else:
                print("[DEPLOY] Failed to deploy, check log file")
        except Exception as e:
            print("[DEPLOY] ERROR : %s"%(str(e)))
        # ssh 연결 해제
        self.ssh.deactivate()        
        time.sleep(5)

def main():

    if INSTALL_SUPERVM == 'true':
        install_time = time.time()
        a = install()
        #a.setup()
        #a.answers()
        if a.STORAGE_TYPE == 'nfs':
            a.nfs()
        elif a.STORAGE_TYPE == 'ceph':
            a.ceph()
        #a.deploy()
        h, m, s = secToHms(install_time, time.time())
        print("* DEPLOY TIME : %dh %dm %.2fs"%(h, m, s))
    else:
        print("* It didn't execute installation")


if __name__ == "__main__":        

    main()

        