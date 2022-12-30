#!/bin/bash 


set -f
set -o noglob
DOCKERCRON=$(echo $DOCKER_MONITOR_CRON | xargs)
LINUXCRON=$(echo $LINUX_HEALTH_CRON | xargs)
DYNAMICCRON=&(echo $DYNAMIC_IP_CRON | xargs)