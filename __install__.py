from __common__.__parameter__ import *
from __common__.__ssh__ import *


class install():

    def __init__(self):
        self.ENGINE_NUM = ENGINE_IP.split('.')[3] # ***.***.***.***
        self.MASTER_NUM = MASTER_IP.split('.')[3]
        # engine vm에 ssh연결
        self.ssh = ssh_connection(ENGINE_IP, 22, ENGINE_ID, ENGINE_PW)

    def setup(self):
        
        self.ssh.activate() 

        # hostname 변경
        self.ssh.commandExec('hostnamectl set-hostname hypervm%s.tmax.dom'%self.ENGINE_NUM)

        # hosts에 fqdn 추가
        o, e = self.ssh.commandExec('cat /etc/hosts')
        hosts = True
        # hosts에 입력한 ip가 있는지 확인 후 없을 때만 추가
        for i in o:
            if ENGINE_IP in i:
                print('* Engine VM IP is already using !!!')
                print('* Check /etc/hosts file in engine vm !!!')
                hosts = False
                break
        if hosts == True:
            print(" Add hosts")
            self.ssh.commandExec('echo "%s hypervm%s.tmax.dom" >> /etc/hosts'%(ENGINE_IP, self.ENGINE_NUM))
            self.ssh.commandExec('echo "%s master%s.tmax.dom" >> /etc/hosts'%(MASTER_IP, self.MASTER_NUM))

        o, e = self.ssh.commandExec('ls /etc/yum.repos.d/supervm.repo')
        repo = True
        if  o != [] and 'supervm.repo' in o[0]:
            print('* supervm.repo is already exists !!!')
            print('* Check supervm.repo file !!!')
            repo = False            
        if repo == True:
            # supervm repository 생성
            print("* Make /etc/yum.repos.d/supervm.repo")
            self.ssh.commandExec('echo "[supervm]" >> /etc/yum.repos.d/supervm.repo')
            self.ssh.commandExec('echo "name=supervm-repo" >> /etc/yum.repos.d/supervm.repo')
            self.ssh.commandExec('echo "baseurl=%s" >> /etc/yum.repos.d/supervm.repo'%(SUPERVM_REPO_URL))
            self.ssh.commandExec('echo "gpgcheck=0" >> /etc/yum.repos.d/supervm.repo')
            self.ssh.commandExec('dnf clean all')
            self.ssh.commandExec('dnf update -y')

        print("* Package install")
        o, e = self.ssh.commandExec('sudo dnf module disable virt -y')
        o, e = self.ssh.commandExec('sudo dnf module enable pki-deps postgresql:12 parfait -y')
        o, e = self.ssh.commandExec('dnf install -y ovirt-hosted-engine-setup')

    def answers(self):
        print("* Make answers.conf file")
        o, e = self.ssh.commandExec('ls /etc/sysconfig/network-scripts/ |grep "ifcfg-e"')        
        self.networkName = o[0][6:] 
        
        o, e = self.ssh.commandExec('python3.6 -c "from ovirt_hosted_engine_setup import util as ohostedutil; print(ohostedutil.randomMAC())"')        
        self.macAddress = o[0]

        # answers.conf 파일 만들기
        o, e = self.ssh.commandExec('ls /root/answers.conf')
        if o != [] and 'answers.conf' in o[0]:
            print("* answers.conf file is already exists !!!")
        else:
            self.ssh.commandExec('echo "[environment:default]" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_CORE/deployProceed=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_CORE/screenProceed=none:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/adminPassword=str:asdf" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/clusterName=str:Default" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/datacenterName=str:Default" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/enableHcGlusterService=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_ENGINE/insecureSSL=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeIf=str:%s" >> /root/answers.conf'%(self.networkName))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/bridgeName=str:ovirtmgmt" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/fqdn=str:master%s.tmax.dom" >> /root/answers.conf'%(self.MASTER_NUM))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/gateway=str:192.168.17.1" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/host_name=str:hypervm%s.tmax.dom" >> /root/answers.conf'%(self.ENGINE_NUM))
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test=str:ping" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_address=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NETWORK/network_test_tcp_port=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/destEmail=str:root@localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpPort=str:25" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/smtpServer=str:localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_NOTIF/sourceEmail=str:root@localhost" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/LunID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/discardSupport=bool:False" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/domainType=str:nfs" >> /root/answers.conf')
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
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/nfsVersion=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainConnection=str:%s:/nfs" >> /root/answers.conf'%(ENGINE_IP))
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/storageDomainName=str:hosted_storage" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/vfsType=str:" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_STORAGE/volUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/applyOpenScapProfile=bool:False" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/automateVMShutdown=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cdromUUID=none:None" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudInitISO=str:generate" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitExecuteEngineSetup=bool:True" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceDomainName=str:tmax.dom" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/cloudinitInstanceHostName=str:master%s.tmax.dom" >> /root/answers.conf'%(self.MASTER_NUM))
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
            self.ssh.commandExec('echo "OVEHOSTED_VM/proLinuxRepoAddress=str:http://prolinux-repo.tmaxos.com/prolinux/8/os/x86_64" >> /root/answers.conf')
            self.ssh.commandExec('echo "OVEHOSTED_VM/ovirtRepoAddress=str:%s" >> /root/answers.conf'%(SUPERVM_REPO_URL))

    def nfs(self):
        print("* Set nfs at %s"%(ENGINE_IP))
        o, e = self.ssh.commandExec('cat /etc/exports')
        nfs_ = True
        for i in o:
            if '/nfs' in i:
                nfs_ = False
                break
        if nfs_ == True:
            self.ssh.commandExec('dnf install -y nfs-utils')
            self.ssh.commandExec('systemctl start rpcbind')
            self.ssh.commandExec('systemctl start nfs-server')
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
            self.ssh.commandExec('firewall-cmd --permanent --add-service=nfs')
            self.ssh.commandExec('firewall-cmd --permanent --add-service=mountd')
            self.ssh.commandExec('firewall-cmd --permanent --add-service=rpc-bind')
            self.ssh.commandExec('firewall-cmd --reload')
            self.ssh.commandExec('firewall-cmd --list-all')

        self.ssh.deactivate()

    def deploy(self):
        print("* Start deploy")       
        self.ssh.commandExec('hosted-engine --deploy --config-append=answers.conf >> $s'%(DEPLOY_LOG_FILE))
        
        # ssh 연결 해제
        self.ssh.deactivate()

def main():

    a = install()
    a.setup()
    a.nfs()
    a.deploy()

if __name__ == "__main__":        

    main()

        