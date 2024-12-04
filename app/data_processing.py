import pandas as pd

def process_partition_data(partition_data):
    columns = ['Partition', 'AvailableCPUs', 'AvailableGPUs']
    data = []
    for line in partition_data.split('\n')[1:]:
        if line.strip():
            parts = line.split('|')
            partition = parts[0]
            cpus = parts[1]
            gpus = parts[2] if len(parts) > 2 else "0"
            data.append([partition, cpus, gpus])
    
    df = pd.DataFrame(data, columns=columns)
    df[['Allocated', 'Idle', 'Other', 'Total']] = df['AvailableCPUs'].str.split('/', expand=True)
    return df.drop(columns=['AvailableCPUs'])


def process_job_data(job_data):
    lines = job_data.split('\n')
    header = lines[0].split()  # Extract column headers
    jobs = [dict(zip(header, line.split())) for line in lines[1:] if line]
    return pd.DataFrame(jobs)

