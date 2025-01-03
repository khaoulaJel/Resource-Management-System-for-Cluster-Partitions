from collections import defaultdict
import pandas as pd
from modules.Commander import executeSSH


class DataFetcher:
    CPUCommand = 'sinfo --noheader --format="%P,%C" | awk -F\'[,/]{1}\' \'{print $1","$2","$3","$4","$5}\''
    GPUCommand = '''
        sinfo --noheader -p gpu -o "%n %G";
        squeue -t RUNNING -o "%P %N" | grep "^gpu"
    '''

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
        try:
            output, err = executeSSH(self.data.username, self.data.password, self.GPUCommand)
            if err:
                raise ValueError(f"Error executing SSH command: {err}")

            gpu_nodes, allocated_nodes = self._parse_combined_gpu_output(output)
            available_nodes = gpu_nodes - allocated_nodes

            data = {
                "Partition": ["gpu"] * len(available_nodes),
                "Available GPU Nodes": list(available_nodes),
                "Available GPU Count": [len(available_nodes)] * len(available_nodes),
            }

            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error retrieving GPU data: {e}")
            return pd.DataFrame(columns=["Partition", "Available GPU Nodes", "Available GPU Count"])


    def _parse_combined_gpu_output(self, output):
        try:
            lines = output.splitlines()
            gpu_nodes = set()
            allocated_nodes = set()

            for line in lines:
                if "gpu:" in line:  # sinfo output
                    parts = line.split()
                    if len(parts) == 2:
                        gpu_nodes.add(parts[0])
                elif line.startswith("gpu"):  # squeue output
                    parts = line.split()
                    if len(parts) >= 2:
                        allocated_nodes.add(parts[1])

            return gpu_nodes, allocated_nodes
        except Exception as e:
            print(f"Error parsing GPU output: {e}")
            return set(), set()
