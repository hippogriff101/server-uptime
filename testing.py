import platform
import subprocess

def ping_host(ip):
    count_flag = '-n' if platform.system() == 'Windows' else '-c'
    result = subprocess.run(
        ['ping', count_flag, '4', ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0

ip_address = '8.8.8.8'
if ping_host(ip_address):
    print(f"{ip_address} is reachable")
else:
    print(f"{ip_address} is not reachable")