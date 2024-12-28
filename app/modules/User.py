import pandas as pd
from modules.Commander import executeSSH, getUserName
from modules.GPUData import getGPUAvail

class User:
    
    class DataFetcher:
        CPUCommand = 'sinfo --noheader --format="%P,%C" | awk -F\'[,/]{1}\' \'{print $1","$2","$3","$4","$5}\''
        def __init__(self, user):
            self.data = user 

        def getCPUData(self):

            try:
                output, err = executeSSH(self.data.username, self.data.password, self.CPUCommand)

                if err:
                    raise ValueError(f"Error executing SSH command: {err}")
                
                data = []
                for line in output.splitlines():
                    data.append(line.split(","))

                df = pd.DataFrame(data, columns=["PARTITION", "CPUS_A", "CPUS_I", "CPUS_O", "CPUS_T"])

                for col in ["CPUS_A", "CPUS_I", "CPUS_O", "CPUS_T"]:
                    df[col] = pd.to_numeric(df[col])

                return df
            except ValueError as e:
                print(f"ValueError: {e}")
                return pd.DataFrame()
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                return pd.DataFrame()
        
    
        def getGPUData(self):
            return getGPUAvail(self.data.username, self.data.password)


    def __init__(self, username, password):
        self.username = getUserName(username)
        self.password = password
        self.dataFetcher = User.DataFetcher(self)


    def __repr__(self):
        return self.username
    

    def to_dict(self):
        return {"username": self.username, "password": self.password}


    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"])
    

    @staticmethod
    def getLoggedUser(usr):
        return User.from_dict(usr)

    