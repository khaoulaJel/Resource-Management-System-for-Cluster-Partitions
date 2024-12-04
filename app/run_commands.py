import subprocess
import subprocess

def run_sinfo_command(format_string="%P|%C|%G"):
    """Fetch partition data using sinfo."""
        result = subprocess.run(
            ['sinfo', f'--format={format_string}'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

def run_squeue_command(partition=None):
    """Fetch job data using squeue."""
    command = ['squeue']
    if partition:
        command.extend(['-p', partition])
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()

