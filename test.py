#!/usr/bin/env python3

import argparse, sys
import os
import subprocess
import paramiko

#Setup pipe so it always runs on boot
bashCommand = f"touch /home/collinp/python1"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

#Check if Docker Monitor should run and setup

bashCommand = f"touch /home/collinp/python2"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
print(bashCommand)
output, error = process.communicate()

# #Check if Linux Health Scan should run and setup
# if args_passed['linux_health_active'] == 'true':
#     bashCommand = f"crontab -l 2>/dev/null; echo '{args_passed['linux_health_cron']} /usr/bin/python3 'echo /opt/cecil/linux-health/server-health-check.py {args_passed['monitor_url']} > /opt/cecil/pipe' | crontab -"
#     process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#     output, error = process.communicate()

# #Check if Dynamic IP Scan should run and setup
# if args_passed['dynamic_ip_updater'] == 'true':
#     bashCommand = f"crontab -l 2>/dev/null; echo '{args_passed['dynamic_ip_cron']} /usr/bin/python3 'echo /opt/cecil/DynamicIP-Updater/checkpublicip.py {args_passed['monitor_url']} > /opt/cecil/pipe' | crontab -"
#     process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#     output, error = process.communicate()

# 
# crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && \
# crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && \
# crontab -l 2>/dev/null; echo '$RUNTIMER /usr/bin/bash /camm/cammtask.sh' | crontab - && \