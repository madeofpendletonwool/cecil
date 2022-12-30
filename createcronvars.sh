#!/bin/bash 


set -f
set -o noglob
export DOCKERCRON=$(echo $DOCKER_MONITOR_CRON | xargs)
export LINUXCRON=$(echo $LINUX_HEALTH_CRON | xargs)
export DYNAMICCRON=&(echo $DYNAMIC_IP_CRON | xargs)