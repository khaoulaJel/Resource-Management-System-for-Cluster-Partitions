from run_commands import run_sinfo_command, run_squeue_command

print("Testing sinfo command...")
print(run_sinfo_command())

print("Testing squeue command...")
print(run_squeue_command("gpu"))

