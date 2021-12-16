import paramiko
from __common__.__module__ import makeUpMsg

class ssh_connection():
    def __init__(self, HOST_IP, HOST_PORT, HOST_ID, HOST_PW):
        self.HOST_IP = str(HOST_IP)
        self.HOST_PORT = str(HOST_PORT)
        self.HOST_ID = str(HOST_ID)
        self.HOST_PW = str(HOST_PW)

    def activate(self): ## ssh 연결 활성화
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.HOST_IP, username=self.HOST_ID, password=self.HOST_PW, port=self.HOST_PORT)
            print("* Successfully connected")
            print("**********************************************************")
            print("[CONNECTION INFORMATION]")
            print("HOST IP = %s"%self.HOST_IP)
            print("HOST PORT = %s"%self.HOST_PORT)
            print("HOST ID = %s"%self.HOST_ID)
            print("HOST PW = %s"%self.HOST_PW)
            print("**********************************************************")
            # stdin, stdout, stderr = self.ssh.exec_command('rpm --query prolinux-release')
        except Exception as e:
            print("**********************************************************")
            print("* SSH Connection Exception : %s"%str(e))
            print("**********************************************************")

    def commandExec(self, e, t=30, pty = False): # exection, timeout
        # default timeout = 30sec
        try:
            if pty == True:
                stdin, stdout, stderr = self.ssh.exec_command(e, get_pty = pty, timeout=t)        
            else:
                stdin, stdout, stderr = self.ssh.exec_command(e, timeout=t)        
            output = makeUpMsg(stdout.readlines())
        except Exception as e:
            output = [str(e)]
        try:
            error = makeUpMsg(stderr.readlines())
        except Exception as e:
            error = [str(e)]

        return output, error

    def deactivate(self):
        try:
            self.ssh.close()
            print("* Successfully disconnected")
        except Exception as e:
            print('* Failed ssh disconnection, still connecting ssh')

