#!/bin/bash

service cron start
tail -f /dev/null
/usr/bin/python3 /opt/cecil/cecilcontained.py --host_ssh_ip=$HOST_SSH_IP --host_ssh_user=$HOST_SSH_USER --host_ssh_pass=$HOST_SSH_PASS --alert_url=$ALERT_URL --monitor_url=$MONITOR_URL --docker_monitor_active=$DOCKER_MONITOR_ACTIVE --linux_health_active=$LINUX_HEALTH_ACTIVE --docker_monitor_cron="$DOCKER_MONITOR_CRON" --linux_health_cron="$LINUX_HEALTH_CRON" --dynamic_ip_cron="$DYNAMIC_IP_CRON"