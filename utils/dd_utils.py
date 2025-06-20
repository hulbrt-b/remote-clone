from utils.ssh import run_ssh_command

def check_disk_size(remote_host):
    result = run_ssh_command(remote_host, "lsblk -b /dev/sda --output SIZE -n | head -1")
    if result["success"]:
        return int(result["stdout"])
    else:
        raise RuntimeError(f"SSH Error: {result['stderr']}")
