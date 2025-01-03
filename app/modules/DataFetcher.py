from collections import defaultdict
import pandas as pd
from modules.Commander import executeSSH

class DataFetcher:
    CPUCommand = 'sinfo --noheader --format="%P,%C" | awk -F\'[,/]{1}\' \'{print $1","$2","$3","$4","$5}\''
    GPUCommand = 'sinfo --noheader -p gpu -o "%n %G" && squeue -t RUNNING -o "%P %N"'

    def __init__(self, user):
        self.data = user

    def getCPUData(self):
        """
        Fetch and process CPU data.
        """
        try:
            output, err = executeSSH(self.data.username, self.data.password, self.CPUCommand)

            if err:
                raise ValueError(f"Error executing SSH command: {err}")

            if not output:
                raise ValueError("No output from CPU command")

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
        """
        Fetch and process GPU data with separate commands for better reliability.
        """

        try:
            allocated_nodes = self.get_allocated_nodes()  # Allocated nodes in the 'gpu' partition
            gpu_nodes = self.get_gpu_nodes()  # All GPU nodes in the 'gpu' partition
            other_partition_nodes = self.get_other_partition_allocations()  # Nodes allocated by other partitions

            available_nodes = gpu_nodes - allocated_nodes - other_partition_nodes

            data = {
                "Partition": ["gpu"] * len(available_nodes),
                "Available GPU Nodes": list(available_nodes),
                "Available GPU Count": [1] * len(available_nodes),
            }

            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching GPU data: {e}")
            return pd.DataFrame()

    def get_allocated_nodes(self):
        """
        Fetch nodes that are currently running GPU jobs using squeue.
        Focus only on the 'gpu' partition.
        """
        squeue_cmd = 'squeue -t RUNNING -o "%P %N" | grep "^gpu"'
        try:
            result, err = executeSSH(self.data.username, self.data.password, squeue_cmd)

            if err:
                raise ValueError(f"Error executing SSH command: {err}")

            allocated_nodes = set()

            for line in result.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    node = parts[1]  # Extract the node name
                    allocated_nodes.add(node)

            return allocated_nodes
        except Exception as e:
            print(f"Error in get_allocated_nodes: {e}")
            return set()

    def get_gpu_nodes(self):
        """
        Fetch all nodes in the 'gpu' partition that have GPUs using sinfo.
        """
        sinfo_cmd = 'sinfo --noheader -p gpu -o "%n %G"'
        try:
            result, err = executeSSH(self.data.username, self.data.password, sinfo_cmd)

            if err:
                raise ValueError(f"Error executing SSH command: {err}")

            gpu_nodes = set()

            for line in result.splitlines():
                parts = line.split()
                if len(parts) == 2 and "gpu:" in parts[1]:
                    node = parts[0]  # Extract node name
                    gpu_nodes.add(node)

            return gpu_nodes
        except Exception as e:
            print(f"Error in get_gpu_nodes: {e}")
            return set()

    def get_other_partition_allocations(self):
        """
        Fetch nodes allocated by partitions other than 'gpu'.
        """
        squeue_cmd = 'squeue -t RUNNING -o "%P %N"'
        try:
            result, err = executeSSH(self.data.username, self.data.password, squeue_cmd)

            if err:
                raise ValueError(f"Error executing SSH command: {err}")

            non_gpu_allocated_nodes = set()

            for line in result.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    partition = parts[0]
                    node = parts[1]
                    if partition != "gpu":  # Exclude 'gpu' partition
                        non_gpu_allocated_nodes.add(node)

            return non_gpu_allocated_nodes
        except Exception as e:
            print(f"Error in get_other_partition_allocations: {e}")
            return set()
