import argparse, sys
import os
import subprocess
import paramiko
import threading

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

args_passed = vars(args)

# Check if the entry already exists in the crontab
entry_exists_dock = os.system("crontab -l | grep '/opt/cecil/monitor-docker/cronstart.py'")

#Check if Docker Monitor should run and setup
if args_passed['docker_monitor_active'] == 'true' and entry_exists_dock != 0:
    setup_docker_mon = f"crontab -l 2>/dev/null; echo '{args_passed['docker_monitor_cron']} /usr/bin/python3 /opt/cecil/monitor-docker/monitor.py --host_ssh_ip=$HOST_SSH_IP --host_ssh_user=$HOST_SSH_USER --host_ssh_pass=$HOST_SSH_PASS --alert_url=$ALERT_URL' | crontab -"
    os.system(setup_docker_mon)

# Check if the entry already exists in the crontab
entry_exists_healthcheck = os.system("crontab -l | grep '/opt/cecil/linux-health/server-health-check.py'")

#Check if Linux Health Scan should run and setup
if args_passed['linux_health_active'] == 'true' and entry_exists_healthcheck != 0:
    setup_healthcheck = f"crontab -l 2>/dev/null; echo '{args_passed['linux_health_cron']} /usr/bin/python3 /opt/cecil/linux-health/server_health_check.py --host_ssh_ip=$HOST_SSH_IP --host_ssh_user=$HOST_SSH_USER --host_ssh_pass=$HOST_SSH_PASS --monitor_url=$MONITOR_URL' | crontab -"
    os.system(setup_healthcheck)

# Check if the entry already exists in the crontab
entry_exists_ip_updater = os.system("crontab -l | grep '/opt/cecil/DynamicIP-Updater/server-health-check.py'")

#Check if Dynamic IP Updater should run and setup
if args_passed['dynamic_ip_updater'] == 'true' and entry_exists_ip_updater != 0:
    setup_dynamic_ip = f"crontab -l 2>/dev/null; echo '{args_passed['dynamic_ip_cron']} /usr/bin/python3 /opt/cecil/DynamicIP-Updater/checkpublicip.py --host_ssh_ip=$HOST_SSH_IP --host_ssh_user=$HOST_SSH_USER --host_ssh_pass=$HOST_SSH_PASS --alert_url=$ALERT_URL' | crontab -"
    os.system(setup_dynamic_ip)
