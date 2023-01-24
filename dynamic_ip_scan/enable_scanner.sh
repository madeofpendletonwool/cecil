#!/bin/bash

set -f
crontab -l 2>/dev/null; echo '{args_passed['dynamic_ip_cron']} /usr/bin/python3 /opt/cecil/DynamicIP-Updater/checkpublicip.py --host_ssh_ip=$HOST_SSH_IP --host_ssh_user=$HOST_SSH_USER --host_ssh_pass=$HOST_SSH_PASS --alert_url=$ALERT_URL' | crontab -
set +f