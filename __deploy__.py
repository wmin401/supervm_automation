import sys
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(sys.argv[1], username=sys.argv[3], password=sys.argv[4], port=sys.argv[2])
#ssh.connect('192.168.17.161',username='root', password='asdf', port='22')

stdin, stdout, stderr = ssh.exec_command('dos2unix /root/deploy_automation.sh', timeout=10)        
output = stdout.readlines()
for i in output:
    print(i.replace('\n',''))
stdin, stdout, stderr = ssh.exec_command('sh /root/deploy_automation.sh %s %s'%(sys.argv[5],sys.argv[6]))        
output = stdout.readlines()
for i in output:
    print(i.replace('\n',''))


ssh.close()