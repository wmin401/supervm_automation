# 1) ProLinux에 ssh 연결
# 2) 해당 ProLinux에 디플로이 설정
# 3) 
# 실행할때 매개변수로 linux ip 랑 master ip 입력받음
# 사용 예시 - sh deploy_automation.sh 161 165 # 여기서 이제 진킨스 변수로 다시 입력받음
ENGINE_NO=$1
MASTER_NO=$2

echo $ENGINE_NO
echo $MASTER_NO

# echo "192.168.17.${LINUX_IP} hypervm${LINUX_IP}.tmax.dom
# 192.168.17.${MASTER_IP} master${MASTER_IP}.tmax.dom" >> /etc/hosts

# touch /etc/yum.repos.d/supervm.repo
# echo "[supervm]
# name=supervm-repo
# baseurl=http://172.21.7.114/ovirt/4.4/supervm-21.0.0-rc0/el8/x86_64/
# gpgcheck=0" >> /etc/yum.repos.d/supervm.repo

# sudo dnf module disable virt -y
# sudo dnf module enable pki-deps postgresql:12 parfait -y
# dnf install -y ovirt-hosted-engine-setup git
# git clone https://github.com/tmax-cloud/install-ovirt
# cd install-ovirt/
# tar -xvf ovirt4.4.3_posixfs_scripts.tar && cd ovirt4.4.3_posixfs_scripts
# ./deploy.sh


# ## nfs 설정
# dnf install -y nfs-utils

# systemctl start rpcbind
# systemctl start nfs-server


# chkconfig rpcbind on
# chkconfig nfs-server on

# mkdir /nfs

# echo "/nfs *(rw)" >> /etc/exports

# exportfs -r

# systemctl restart nfs-server

# groupadd kvm -g 36
# useradd vdsm -u 36 -g 36

# chown -R 36:36 /nfs
# chmod 777 /nfs

# firewall-cmd --permanent --add-service=nfs
# firewall-cmd --permanent --add-service=mountd
# firewall-cmd --permanent --add-service=rpc-bind
# firewall-cmd --reload
# firewall-cmd --list-all



# # 네트워크 이름
# IFCFG_NAME=$(ls /etc/sysconfig/network-scripts/ |grep "ifcfg-e")
# NETWORK_NAME=${IFCFG_NAME:6}


# # 맥 주소
# MAC_ADDR=$(python3.6 -c "from ovirt_hosted_engine_setup import util as ohostedutil; print(ohostedutil.randomMAC())")
# echo "[environment:default]
# OVEHOSTED_CORE/deployProceed=bool:True
# OVEHOSTED_CORE/screenProceed=none:None
# OVEHOSTED_ENGINE/adminPassword=str:asdf
# OVEHOSTED_ENGINE/clusterName=str:Default
# OVEHOSTED_ENGINE/datacenterName=str:Default
# OVEHOSTED_ENGINE/enableHcGlusterService=none:None
# OVEHOSTED_ENGINE/insecureSSL=none:None
# OVEHOSTED_NETWORK/bridgeIf=str:${NETWORK_NAME}
# OVEHOSTED_NETWORK/bridgeName=str:ovirtmgmt
# OVEHOSTED_NETWORK/fqdn=str:master${MASTER_IP}.tmax.dom
# OVEHOSTED_NETWORK/gateway=str:192.168.17.1
# OVEHOSTED_NETWORK/host_name=str:hypervm${HOST_IP}.tmax.dom
# OVEHOSTED_NETWORK/network_test=str:ping
# OVEHOSTED_NETWORK/network_test_tcp_address=none:None
# OVEHOSTED_NETWORK/network_test_tcp_port=none:None
# OVEHOSTED_NOTIF/destEmail=str:root@localhost
# OVEHOSTED_NOTIF/smtpPort=str:25
# OVEHOSTED_NOTIF/smtpServer=str:localhost
# OVEHOSTED_NOTIF/sourceEmail=str:root@localhost
# OVEHOSTED_STORAGE/LunID=none:None
# OVEHOSTED_STORAGE/discardSupport=bool:False
# OVEHOSTED_STORAGE/domainType=str:nfs
# OVEHOSTED_STORAGE/iSCSIDiscoverUser=none:None
# OVEHOSTED_STORAGE/iSCSIPortal=none:None
# OVEHOSTED_STORAGE/iSCSIPortalIPAddress=none:None
# OVEHOSTED_STORAGE/iSCSIPortalPort=none:None
# OVEHOSTED_STORAGE/iSCSIPortalUser=none:None
# OVEHOSTED_STORAGE/iSCSITargetName=none:None
# OVEHOSTED_STORAGE/imgSizeGB=str:120
# OVEHOSTED_STORAGE/imgUUID=none:None
# OVEHOSTED_STORAGE/lockspaceImageUUID=none:None
# OVEHOSTED_STORAGE/lockspaceVolumeUUID=none:None
# OVEHOSTED_STORAGE/metadataImageUUID=none:None
# OVEHOSTED_STORAGE/metadataVolumeUUID=none:None
# OVEHOSTED_STORAGE/mntOptions=str:
# OVEHOSTED_STORAGE/nfsVersion=none:None
# OVEHOSTED_STORAGE/storageDomainConnection=str:192.168.17.${HOST_IP}:/nfs
# OVEHOSTED_STORAGE/storageDomainName=str:hosted_storage
# OVEHOSTED_STORAGE/vfsType=str:
# OVEHOSTED_STORAGE/volUUID=none:None
# OVEHOSTED_VM/applyOpenScapProfile=bool:False
# OVEHOSTED_VM/automateVMShutdown=bool:True
# OVEHOSTED_VM/cdromUUID=none:None
# OVEHOSTED_VM/cloudInitISO=str:generate
# OVEHOSTED_VM/cloudinitExecuteEngineSetup=bool:True
# OVEHOSTED_VM/cloudinitInstanceDomainName=str:tmax.dom
# OVEHOSTED_VM/cloudinitInstanceHostName=str:master${MASTER_IP}.tmax.dom
# OVEHOSTED_VM/cloudinitRootPwd=str:asdf
# OVEHOSTED_VM/cloudinitVMDNS=str:168.126.63.1
# OVEHOSTED_VM/cloudinitVMETCHOSTS=bool:True
# OVEHOSTED_VM/cloudinitVMStaticCIDR=str:192.168.17.${MASTER_IP}/24
# OVEHOSTED_VM/cloudinitVMTZ=str:Asia/Seoul
# OVEHOSTED_VM/consoleUUID=none:None
# OVEHOSTED_VM/emulatedMachine=str:pc
# OVEHOSTED_VM/nicUUID=none:None
# OVEHOSTED_VM/ovfArchive=str:
# OVEHOSTED_VM/rootSshAccess=str:yes
# OVEHOSTED_VM/rootSshPubkey=str:
# OVEHOSTED_VM/vmCDRom=none:None
# OVEHOSTED_VM/vmMACAddr=str:${MAC_ADDR}
# OVEHOSTED_VM/vmMemSizeMB=int:6144
# OVEHOSTED_VM/vmVCpus=str:4
# OVEHOSTED_VM/proLinuxRepoAddress=str:http://prolinux-repo.tmaxos.com/prolinux/8/os/x86_64
# OVEHOSTED_VM/ovirtRepoAddress=str:http://prolinux-repo.tmaxos.com/ovirt/4.4/el8/x86_64" >> /root/answers.conf

