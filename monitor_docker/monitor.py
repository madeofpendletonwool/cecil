import argparse
import logging
import logging.config
import sys
import requests
from requests import get
from typing import List
from io import StringIO
import io
import docker
import socket
import paramiko
import subprocess
# --------------------------------------------------------------------- #
# Define needed vars

parser=argparse.ArgumentParser()

parser.add_argument("--host_ssh_ip", help="ip of host that will run pipe")
parser.add_argument("--host_ssh_user", help="username to ssh into host machine that will run the pipe")
parser.add_argument("--host_ssh_pass", help="password to user on host machine")
parser.add_argument("--alert_url", help="ntfy url that information should be delivered to. This would be your url used for alerts.")

args=parser.parse_args()

args_passed = vars(args)


# --------------------------------------------------------------------- #
# get_hostname

def get_hostname():
    """ get_hostname """
    hostname = str(socket.gethostname())
    return hostname
hostname = get_hostname()
    

# --------------------------------------------------------------------- #
#Setup Paramiko
# Create an SSH client
ssh = paramiko.SSHClient()

# Automatically add host keys for known hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the remote host
ssh.connect(hostname=args_passed['host_ssh_ip'], username=args_passed['host_ssh_user'], password=args_passed['host_ssh_pass'])

# --------------------------------------------------------------------- #


#Get Container Names

# Run the command to get the names of the running containers
stdin, stdout, stderr = ssh.exec_command("docker ps -a --format '{{.Names}}'")

# Get the output of the command
output = stdout.read()

# Split the output by newline to get a list of container names
container_names = output.decode().split("\n")
print(container_names)

# Run Health Check

requests_url = args_passed['alert_url'].replace("'", "")

def main(container_name: str):
    
    hostname = get_hostname()
    try:
        client: docker.DockerClient = docker.from_env()

        containers: List[docker.models.containers.Container] = client.containers.list(
            all=True,
            filters={'name': container_name}
        )

        for container in containers:
            res = client.api.inspect_container(container.id)

            # if the container is running, check the health status (if it exists)
            if container.status == 'running':
                if 'Health' in res['State'] and res['State']['Health']['Status'] == 'unhealthy':
                    last_log = res['State']['Health']['Log'][-1]['Output'].strip()
                    requests.post(requests_url, data=(f'container {container.name} on {hostname} is unhealthy, last log entry: {last_log}'))
            elif container.status != 'running':
                requests.post(requests_url, data=(f'container {container.name} on {hostname} has status {container.status}'))


        if len(containers) == 0:
            requests.post(requests_url, data=(f'no container(s) with name {container.name} found on {hostname}'))
    except docker.errors.NotFound:
        requests.post(requests_url, data=(f'Container {container.name} on {hostname} not found'))
        
    except docker.errors.DockerException as exc:
        requests.post(requests_url, data=(f'Docker host on {hostname} seems to be down: {exc}'))

if __name__ == '__main__':
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            '': {
                'level': 'INFO',
            },
        }
    })

    for container_name in container_names:
        # Execute the main function on the remote host
        stdin, stdout, stderr = ssh.exec_command(f"python main.py {container_name}")