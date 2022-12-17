from pathlib import Path
import os
from requests import get
import requests
import yaml
import sys

#Define ntfy topic
ntfytopic = sys.argv[1]

#Check to make sure folder Structure exists
ntfy_folder_create = os.path.expanduser('~')
path = f'{ntfy_folder_create}/ntfy'
# Check whether the specified path exists or not
ipconfig = os.path.expanduser('~') + '/ntfy/checkpublicip.yaml'
isExist = os.path.exists(path)
if isExist == False:
    os.makedirs(path)

ipconfigcheck = os.path.exists(os.path.expanduser('~') + '/ntfy/checkpublicip.yaml')
if ipconfigcheck == False:
    Path(f'{ipconfig}').touch()
    with open(ipconfig, 'a') as f:
        line1 = '---'
        linenew = '\n'
        line2 = 'ipaddress:'
        line3 = f'  - Current_IP: 0.0.0.0'
        f.writelines([line1, linenew, line2, linenew, line3])

# Pull Current Known Public IP from config file that's always updated
home_folder = os.path.expanduser('~')
with open(f'{home_folder}/ntfy/checkpublicip.yaml') as f:
    Current_IP_File = yaml.load(f, Loader=yaml.FullLoader)

Current_IP = Current_IP_File['ipaddress'][0]['Current_IP']

# Get Actual Current IP from the internet
ip = get('https://ifconfig.me').text

# If the Values are diffent, update yaml file, notify, and restart Dynu to quickly update services dependant on up to date IP
if Current_IP != ip:
    os.remove(ipconfig)
    Path(f'{ipconfig}').touch()
    with open(ipconfig, 'a') as f:
        line1 = '---'
        linenew = '\n'
        line2 = 'ipaddress:'
        line3 = f'  - Current_IP: {ip}'

        f.writelines([line1, linenew, line2, linenew, line3])
    # Post curl Notification
    requests.post(ntfytopic, data=f"Public IP Changed! It's now {ip} 😀".encode(encoding='utf-8'))

    #Restart Dynu Service
    os.system("echo password | sudo -S systemctl restart dynuiuc.service")