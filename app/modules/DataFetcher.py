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
        Fetch GPU data in a single SSH command.
        """
        try:
            combined_command = (
                'sinfo --noheader -p gpu -o "%n %G" && squeue -t RUNNING -o "%P %N"'
            )
            result, err = executeSSH(self.data.username, self.data.password, combined_command)

            if err:
                raise ValueError(f"Error executing SSH command: {err}")

            if not result:
                raise ValueError("No output from GPU data command")

            # Split sinfo and squeue results
            sinfo_lines = []
            squeue_lines = []
            gpu_section = True

            for line in result.splitlines():
                if line.startswith("PARTITION"):  # Start of squeue output
                    gpu_section = False
                    continue
                if gpu_section:
                    sinfo_lines.append(line)
                else:
                    squeue_lines.append(line)

            # Extract GPU nodes from sinfo output
            gpu_nodes = set()
            for line in sinfo_lines:
                parts = line.split()
                if len(parts) == 2 and "gpu:" in parts[1]:
                    node = parts[0]
                    gpu_nodes.add(node)

            # Extract allocated nodes from squeue output
            allocated_nodes = set()
            other_partition_nodes = set()
            for line in squeue_lines:
                parts = line.split()
                if len(parts) >= 2:
                    partition = parts[0]
                    node = parts[1]
                    if partition == "gpu":
                        allocated_nodes.add(node)
                    else:
                        other_partition_nodes.add(node)

            # Compute available GPU nodes
            available_nodes = gpu_nodes - allocated_nodes - other_partition_nodes

            # Create DataFrame
            data = {
                "Partition": ["gpu"] * len(available_nodes),
                "Available GPU Nodes": list(available_nodes),
                "Available GPU Count": [1] * len(available_nodes),
            }

            return pd.DataFrame(data)

        except Exception as e:
            print(f"Error fetching GPU data: {e}")
            return pd.DataFrame()
