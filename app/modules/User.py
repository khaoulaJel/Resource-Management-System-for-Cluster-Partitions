import pandas as pd
from modules.Commander import executeSSH, getUserName

path = "C:\\Users\\UM6P\\Desktop\\Learning\\S1 - CI\\HPC\\Resource-Management-System-for-Cluster-Partitions\\app\\modules\\gpu_availability.csv"

class User:
    
    class DataFetcher:
        CPUCommand = 'sinfo --noheader --format="%P,%C" | awk -F\'[,/]{1}\' \'{print $1","$2","$3","$4","$5}\''
        GPUCommand = ""

        def __init__(self, user):
            self.data = user 

        def getCPUData(self):
            output, err = executeSSH(self.data.username, self.data.password, self.CPUCommand)
            data = []
            for line in output.splitlines():
                data.append(line.split(","))

            df = pd.DataFrame(data, columns=["PARTITION", "CPUS_A", "CPUS_I", "CPUS_O", "CPUS_T"])

            for col in ["CPUS_A", "CPUS_I", "CPUS_O", "CPUS_T"]:
                df[col] = pd.to_numeric(df[col])

            return df
        
    
        def getGPUData(self):
            try:
                df = pd.read_csv(path)

                df["Available GPU Nodes"] = df["Available GPU Nodes"].fillna("")
                return df
            except Exception as e:
                print(f"Error loading GPU data: {e}")
                return pd.DataFrame(columns=["Partition", "Available GPU Nodes", "Available GPU Count"])



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

    