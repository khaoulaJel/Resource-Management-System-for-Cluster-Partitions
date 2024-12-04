import subprocess
import subprocess

def run_sinfo_command(format_string="%P|%C|%G"):
    """Fetch partition data using sinfo."""
    try:
        result = subprocess.run(
            ['sinfo', f'--format={format_string}'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running sinfo: {e}")
        return ""
    except FileNotFoundError:
        print("sinfo command not found. Ensure SLURM is installed.")
        return ""

def run_squeue_command(partition=None):
    """Fetch job data using squeue."""
    command = ['squeue']
    if partition:
        command.extend(['-p', partition])
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running squeue: {e}")
        return ""
    except FileNotFoundError:
        print("squeue command not found. Ensure SLURM is installed.")
        return ""

