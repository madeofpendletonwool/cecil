import argparse, sys
import os
import subprocess
import paramiko

parser=argparse.ArgumentParser()

parser.add_argument("--host_ssh_ip", help="ip of host that will run pipe")
parser.add_argument("--host_ssh_user", help="username to ssh into host machine that will run the pipe")
parser.add_argument("--host_ssh_pass", help="password to user on host machine")
parser.add_argument("--alert_url", help="ntfy url that information should be delivered to. This would be your url used for alerts.")
parser.add_argument("--monitor_url", help="ntfy url that information should be delivered to. This would be your url to monitor. Not an immediate issue essentially.")
parser.add_argument("--docker_monitor_active", help="true or false - Should we run the docker monitor?")
parser.add_argument("--linux_health_active", help="true or false - Should we run the linux health scan?")
parser.add_argument("--dynamic_ip_updater", help="true or false. Should be run the dynamic IP Scanner")
parser.add_argument("--docker_monitor_cron", help="cron timer of how often the docker monitor should be run")
parser.add_argument("--linux_health_cron", help="cron timer of how often the linux health scan should run")
parser.add_argument("--dynamic_ip_cron", help="cron timer of how often the dyanmic IP updater should run")

args=parser.parse_args()

# print(f"Args: {args}\nCommand Line: {sys.argv}\nfoo: {args.foo}")
# print(f"Dict format: {vars(args)}")

args_passed = vars(args)


# Create an SSH client using paramiko
ssh = paramiko.SSHClient()
# Automatically add host keys for known hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to the remote host
ssh.connect(hostname=args_passed['host_ssh_ip'], username=args_passed['host_ssh_user'], password=args_passed['host_ssh_pass'])
# Run a command on the remote host
stdin, stdout, stderr = ssh.exec_command('mkdir -p /opt/cecil && mkfifo /opt/cecil/pipe && while true; do eval "$(cat /opt/cecil/pipe)"; done')
stdin.close()
# Wait for the command to complete
stdout.channel.recv_exit_status()
# Close the connection
ssh.close()

#Setup pipe so it always runs on boot
setup_pipe = f"echo 'crontab -l 2>/dev/null; echo \"@reboot /usr/bin/bash /opt/cecil/execpipe.sh\" | crontab -' > /hostpipe/pipe"
os.system(setup_pipe)

#Check if Docker Monitor should run and setup
if args_passed['docker_monitor_active'] == 'true':
    setup_docker_mon = f"crontab -l 2>/dev/null; echo '{args_passed['docker_monitor_cron']} /usr/bin/bash /opt/cecil/monitor-docker/run.sh {args_passed['alert_url']}' > /hostpipe/pipe | crontab -"
    os.system(setup_docker_mon)

#Check if Linux Health Scan should run and setup
if args_passed['linux_health_active'] == 'true':
    setup_linux_health = f"crontab -l 2>/dev/null; echo '{args_passed['linux_health_cron']} /usr/bin/python3 /opt/cecil/linux-health/server-health-check.py {args_passed['monitor_url']}' > /hostpipe/pipe | crontab -"
    os.system(setup_linux_health)

#Check if Dynamic IP Scan should run and setup
if args_passed['dynamic_ip_updater'] == 'true':
    setup_dynamic_ip = f"crontab -l 2>/dev/null; echo '{args_passed['dynamic_ip_cron']} /usr/bin/python3 'echo /opt/cecil/DynamicIP-Updater/checkpublicip.py {args_passed['monitor_url']}' > /hostpipe/pipe | crontab -"
    os.system(setup_dynamic_ip)

# 
# crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && \
# crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && \
# crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && \
