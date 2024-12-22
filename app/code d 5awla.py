import subprocess
from collections import defaultdict

def get_allocated_nodes():

    squeue_cmd = 'squeue -t RUNNING -o "%P %N" | grep "^gpu"'
    result = subprocess.run(squeue_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    allocated_nodes = set()
    if result.returncode != 0 or not result.stdout.strip():
        print("Error retrieving allocated GPU nodes.")
        return allocated_nodes

    for line in result.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            node = parts[1] 
            allocated_nodes.add(node)

    return allocated_nodes

def get_gpu_nodes():

    sinfo_cmd = 'sinfo --noheader -p gpu -o "%n %G"'
    result = subprocess.run(sinfo_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    gpu_nodes = set()
    if result.returncode != 0 or not result.stdout.strip():
        print("Error retrieving GPU nodes.")
        return gpu_nodes

    for line in result.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) == 2 and "gpu:" in parts[1]:
            node = parts[0]  # Extract node name
            gpu_nodes.add(node)

    return gpu_nodes

if __name__ == "__main__":
    allocated_nodes = get_allocated_nodes()
    gpu_nodes = get_gpu_nodes()

    available_nodes = gpu_nodes - allocated_nodes

    print("GPU Partition - Node Status:")
    print(f"Total GPU Nodes: {len(gpu_nodes)}")
    print(f"Allocated Nodes: {len(allocated_nodes)}")
    print(f"Available Nodes: {len(available_nodes)}")
    print(f"Available GPU Nodes: {available_nodes}")
