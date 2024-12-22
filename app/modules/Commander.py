import paramiko

host = "simlab-cluster.um6p.ma"

def verifyUm6pEmail(email):
    if "@" not in email:
        return False
    
    if email.split("@")[1] == "um6p.ma":
        return True
    return False


def getUserName(email):
    return email.split("@")[0]


def executeSSH(username, password, command):
    try: 
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=host, username=username, password=password)
            stdin, stdout, stderr = client.exec_command(command)
            return stdout.read().decode().strip(), stderr.read().decode().strip()
        finally:
            client.close()
    except Exception as AuthenticationException:
        return "authfailed", "authfailed"

def verifyAuth(email, password):
    if not verifyUm6pEmail(email):
        return False
    
    command = "echo 20"
    stdout, stderr = executeSSH(getUserName(email), password, command)
    if stdout != "authfailed" and stderr != "authfailed":
        return True
    
    return False