from collections import defaultdict
import pandas as pd
from modules.Commander import executeSSH, getUserName



def get_allocated_nodes(username, password):


    try:
        squeue_cmd = 'squeue -t RUNNING -o "%P %N" | grep "^gpu"'
        result, err = executeSSH(username, password, squeue_cmd)

        if err:
            raise ValueError(f"Error executing SSH command: {err}")

        allocated_nodes = set()

        for line in result.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                node = parts[1]
                allocated_nodes.add(node)

        return allocated_nodes
    
    except ValueError as e:
        print(f"ValueError: {e}")
        return set()
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return set()

def get_gpu_nodes(username, password):
    try:
        sinfo_cmd = 'sinfo --noheader -p gpu -o "%n %G"'
        result, err = executeSSH(username, password, sinfo_cmd)

        if err:
            raise ValueError(f"Error executing SSH command: {err}")

        gpu_nodes = set()

        for line in result.splitlines():
            parts = line.split()
            if len(parts) == 2 and "gpu:" in parts[1]:
                node = parts[0]
                gpu_nodes.add(node)

        return gpu_nodes
    
    except ValueError as e:
        print(f"ValueError: {e}")
        return set()
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return set()
   

def getGPUAvail(username, password):
    try:

        allocated_nodes = get_allocated_nodes(username, password)
        gpu_nodes = get_gpu_nodes(username, password)

        available_nodes = gpu_nodes - allocated_nodes

        data = {
            "Partition": ["gpu"] * len(available_nodes), 
            "Available GPU Nodes": list(available_nodes),
            "Available GPU Count": [len(available_nodes)] * len(available_nodes)
        }

        df = pd.DataFrame(data)

        return df
    except Exception as e:
        print(f"Error retrieving GPU data: {e}")
        return pd.DataFrame(columns=["Partition", "Available GPU Nodes", "Available GPU Count"])
    
