import subprocess
import csv
import pandas as pd

sinfo_command_CPU = 'sinfo --noheader --format="%P,%C" | awk -F\'[,/]{1}\' \'{print $1","$2","$3","$4","$5}\''
sinfo_command_GPU = "sinfo -p gpu --states=idle --noheader -o '%n %G' | awk '{split($2, gpus, \\\":\\\"); print $1, gpus[2]}' | awk '{s+=$2} END {print s}'"



def GetData():
    ssh_command =  f'ssh simlab "{sinfo_command_CPU}"'
    result = subprocess.run(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output = result.stdout.strip()

    data = []
    for line in output.splitlines():
        data.append(line.split(" "))

    df = pd.DataFrame(data, columns=["PARTITION", "CPUS_A", "CPUS_I", "CPUS_O", "CPUS_T"])

    for col in ["CPUS_A", "CPUS_I", "CPUS_O", "CPUS_T"]:
        df[col] = pd.to_numeric(df[col])

    return df



def GetGPU():
    ssh_command = f'ssh simlab "{sinfo_command_GPU}"'

    result = subprocess.run(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout.strip()

    return int(output)

