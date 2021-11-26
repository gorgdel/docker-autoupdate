import re
import subprocess
import requests
import time
import os
from distutils.version import LooseVersion


def clearConsole():
    command = 'clear'
    os.system(command)

# Pull vaultwarden Version
url = 'https://github.com/dani-garcia/vaultwarden/releases/latest'
r = requests.get(url)
vw_github_version = r.url.split('/')[-1]


# Pull Current Version for vaultwarden
with open('vaultwarden-update') as vaultwarden:
    v_file_content = vaultwarden.read()
    v_file_match = re.search(r'(dockerversion=([0-9.]*))', v_file_content)
    v_file_version = v_file_match.group(2)

while True:
    if LooseVersion(vw_github_version) == LooseVersion(v_file_version):
        print("vaultwarden is up to date")
        print('File Version:',v_file_version)
        print('Github Version:',vw_github_version)

        url = 'https://github.com/vaultwarden/vaultwarden/releases/latest'
        r = requests.get(url)
        vw_github_version = r.url.split('/')[-1]
        with open('vaultwarden-update') as vaultwarden:
            v_file_content = vaultwarden.read()
            v_file_match = re.search(r'(dockerversion=([0-9.]*))', v_file_content)
            v_file_version = v_file_match.group(2)
            time.sleep(2)

    else:
        print('vaultwarden requires an update')
        print('Updating From:',v_file_version)
        print('Latest Version:',vw_github_version)
        with open('vaultwarden-update') as vaultwarden:
            v_file_content = vaultwarden.read()
            v_file_match = re.search(r'(dockerversion=([0-9.]*))', v_file_content)
            v_file_version = v_file_match.group(2)
            time.sleep(5)
            break

# Check who is higher
if LooseVersion(vw_github_version) > LooseVersion(v_file_version):
    # print(f'github version ({github_version}) > file version ({file_version})')
    with open('vaultwarden-update', 'w') as vaultwarden:
        p_new_file_content = v_file_content.replace(v_file_match.group(1), f'dockerversion={vw_github_version}')
        vaultwarden.write(p_new_file_content)
        vaultwarden.close()
        print('Updating vaultwarden')
        time.sleep(1)

        cmd = 'bash vaultwarden-update'
    subprocess.run([cmd], shell=True)

    print('Updated')
    print('vaultwarden Has Been Updated From', v_file_version, 'To', vw_github_version)
    time.sleep(3)
