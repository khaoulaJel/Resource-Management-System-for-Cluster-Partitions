import paramiko

host = "simlab-cluster.um6p.ma"

class SSHConnectionManager:
    _instance = None
    def __init__(self, host):
        self.host = host
        self.client = None

    def connect(self, username, password):
        if self.client is None or not self._is_client_active():
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self.client.connect(hostname=self.host, username=username, password=password)
            except Exception as e:
                self.client = None
                raise Exception(f"SSH connection failed: {e}")

    def execute(self, command):
        if self.client is None or not self._is_client_active():
            raise Exception("SSH client is not connected or is inactive.")
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode().strip(), stderr.read().decode().strip()
        except Exception as e:
            raise Exception(f"Error executing command: {e}")

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def _is_client_active(self):
        if self.client and self.client.get_transport() and self.client.get_transport().is_active():
            return True
        return False
    
    @staticmethod
    def getInstance():
        if not SSHConnectionManager._instance:
            SSHConnectionManager._instance = SSHConnectionManager(host)
        return SSHConnectionManager._instance



def verifyUm6pEmail(email):
    if "@" not in email:
        return False
    
    if email.split("@")[1] == "um6p.ma":
        return True
    return False

def getUserName(email):
    return email.split("@")[0]

def verifyAuth(email, password):
    if not verifyUm6pEmail(email):
        return False
    
    command = "echo 20"
    stdout, stderr = executeSSH(getUserName(email), password, command)
    if stdout != "authfailed" and stderr != "authfailed":
        return True
    
    return False

def executeSSH(username, password, command):
    ssh_manager = SSHConnectionManager.getInstance()
    try:
        ssh_manager.connect(username, password) # For Safety 
        return ssh_manager.execute(command)
    except Exception as e:
        print(f"Error executing SSH command: {e}")
        return None, str(e)


