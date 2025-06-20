import subprocess

def run_dd_clone(source, destination):
    try:
        cmd = f"ssh user@{source} 'dd if=/dev/sda | pv -n' | dd of={destination}"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return {'status': 'SUCCESS' if process.returncode == 0 else 'FAILURE', 'output': stderr.decode()}
    except Exception as e:
        return {'status': 'FAILURE', 'output': str(e)}

