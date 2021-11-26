import re
import subprocess
import requests
import time
import os
from distutils.version import LooseVersion


def clearConsole():
    command = 'clear'
    os.system(command)

# Pull Portainer Version
url = 'https://github.com/portainer/portainer/releases/latest'
r = requests.get(url)
pgithub_version = r.url.split('/')[-1]


# Pull Current Version for Portainer
with open('portainer-update') as portainer:
    p_file_content = portainer.read()
    p_file_match = re.search(r'(dockerversion=([0-9.]*))', p_file_content)
    p_file_version = p_file_match.group(2)

while True:
    if LooseVersion(pgithub_version) == LooseVersion(p_file_version):
        print("Portainer is up to date")
        print('File Version:',p_file_version)
        print('Github Version:',pgithub_version)

        url = 'https://github.com/portainer/portainer/releases/latest'
        r = requests.get(url)
        pgithub_version = r.url.split('/')[-1]
        with open('portainer-update') as portainer:
            p_file_content = portainer.read()
            p_file_match = re.search(r'(dockerversion=([0-9.]*))', p_file_content)
            p_file_version = p_file_match.group(2)
            time.sleep(2)

    else:
        print('Portainer requires an update')
        print('Updating From:',p_file_version)
        print('Latest Version:',pgithub_version)
        with open('portainer-update') as portainer:
            p_file_content = portainer.read()
            p_file_match = re.search(r'(dockerversion=([0-9.]*))', p_file_content)
            p_file_version = p_file_match.group(2)
            time.sleep(5)
            break

# Check who is higher
if LooseVersion(pgithub_version) > LooseVersion(p_file_version):
    # print(f'github version ({github_version}) > file version ({file_version})')
    with open('portainer-update', 'w') as portainer:
        p_new_file_content = p_file_content.replace(p_file_match.group(1), f'dockerversion={pgithub_version}')
        portainer.write(p_new_file_content)
        portainer.close()
        print('Updating Portainer')
        time.sleep(1)

        cmd = 'bash portainer-update'
    subprocess.run([cmd], shell=True)

    print('Updated')
    print('Portainer Has Been Updated From', p_file_version, 'To', pgithub_version)
    time.sleep(3)
