from run_commands import run_sinfo_command, run_squeue_command
from data_processing import process_partition_data, process_job_data

# Test partition data processing
partition_data = run_sinfo_command()
df_partitions = process_partition_data(partition_data)
print(df_partitions)

# Test job data processing
job_data = run_squeue_command("gpu")
df_jobs = process_job_data(job_data)
print(df_jobs)

