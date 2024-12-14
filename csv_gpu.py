import subprocess
from collections import defaultdict
import csv


def get_allocated_nodes():
    # Command output given by you:
    # squeue -t RUNNING -o "%P %N %G"
    squeue_cmd = 'squeue -t RUNNING -o "%P %N %G"'
    result = subprocess.run(squeue_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    allocated = defaultdict(set)
    if result.returncode != 0 or not result.stdout.strip():
        print("Error retrieving squeue information.")
        return allocated

    lines = result.stdout.strip().splitlines()
    # Assuming the first line is header: "PARTITION NODELIST GROUP"
    # We skip it.
    if lines and lines[0].upper().startswith("PARTITION"):
        lines = lines[1:]

    # Each line: PARTITION NODELIST GROUP
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            partition = parts[0]
            node = parts[1]
            allocated[partition].add(node)

    return allocated


def get_gpu_nodes():
    # Command output given by you:
    # sinfo --noheader -o "%P %n %G"
    sinfo_cmd = 'sinfo --noheader -o "%P %n %G"'
    result = subprocess.run(sinfo_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    gpu_nodes = defaultdict(set)
    if result.returncode != 0 or not result.stdout.strip():
        print("Error retrieving sinfo information.")
        return gpu_nodes

    lines = result.stdout.strip().splitlines()

    # Each line: PARTITION NODE GRES
    # We consider only nodes that have 'gpu:' in the GRES field
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            partition, node, gres = parts
            if "gpu:" in gres:
                gpu_nodes[partition].add(node)

    return gpu_nodes


def write_output_to_csv(output_file="gpu_availability.csv"):

    allocated_nodes = get_allocated_nodes()


    gpu_nodes = get_gpu_nodes()

    csv_rows = [["Partition", "Available GPU Nodes", "Available GPU Count"]]  # Header row

    print("Partition - Available GPU Nodes:")
    for partition, gpu_node_set in gpu_nodes.items():

        allocated_set = allocated_nodes.get(partition, set())

        available_nodes = gpu_node_set - allocated_set

        print(f"{partition}: {available_nodes}")
        print(f"{partition} Available GPU Count: {len(available_nodes)}")
 
        csv_rows.append([partition, ", ".join(available_nodes), len(available_nodes)])


    with open(output_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_rows)

    print(f"Output written to {output_file}")


if __name__ == "__main__":
    write_output_to_csv()

