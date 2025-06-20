import subprocess

def run_ssh_command(host: str, command: str, user: str = "root", timeout: int = 300):
    """
    Executes a command on a remote host via SSH.

    Args:
        host (str): The remote host (IP or hostname).
        command (str): The command to run on the remote host.
        user (str): SSH username.
        timeout (int): Optional timeout for the command (seconds).

    Returns:
        dict: {
            'success': bool,
            'stdout': str,
            'stderr': str,
            'exit_code': int
        }
    """
    ssh_cmd = [
        "ssh",
        f"{user}@{host}",
        command
    ]

    try:
        result = subprocess.run(
            ssh_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds.",
            "exit_code": -1
        }

    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "exit_code": -2
        }

