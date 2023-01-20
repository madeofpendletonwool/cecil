import argparse, sys
import os
import paramiko

parser=argparse.ArgumentParser()

parser.add_argument("--alert_url", help="ntfy url that information should be delivered to. This would be your url used for alerts.")
args=parser.parse_args()

args_passed = vars(args)

# Import the paramiko library
import paramiko

# Create an SSH client
ssh = paramiko.SSHClient()

# Automatically add host keys for known hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the remote host
ssh.connect(hostname=args_passed['host_ssh_ip'], username=args_passed['host_ssh_user'], password=args_passed['host_ssh_pass'])

# Run the command on the remote host
stdin, stdout, stderr = ssh.exec_command(f'/opt/cecil/monitor-docker/run.sh {args_passed['alert_url']}')

# Wait for the command to complete
stdout.channel.recv_exit_status()

# Close the connection
ssh.close()