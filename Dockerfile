 
FROM ubuntu:latest

LABEL maintainer="Collin Pendleton <collinp@collinpendleton.com>"

ARG DEBIAN_FRONTEND=noninteractive

# Create location where cecil code is stored
# RUN mkdir /cecil
# Make sure the package repository is up to date. Also install needed packages via apt
RUN apt update && \
    apt -qy upgrade && \
    apt install -qy python3 && \
    apt install -qy git && \
    apt install -qy software-properties-common && \
    apt install -qy python3-pip && \
    apt install -qy curl && \
    apt install -qy cron && \
    apt install -qy supervisor && \
    apt install python3-pip
# Install needed python packages via pip
ADD ./requirements.txt /
RUN pip install -r ./requirements.txt
# Put cecil Files in place
# Create structure for cecil
RUN git clone https://github.com/madeofpendletonwool/cecil.git /opt/cecil && \
    mkdir -p /opt/cecil/TEMP && \
    chmod -R 755 /opt
# Begin cecil Setup
ENTRYPOINT   /bin/bash -c "set -f && \
             ./createcronvars.sh && \
             /usr/bin/python3 /opt/cecil/cecilcontained.py \
             --host_ssh_ip=$HOST_SSH_IP \
             --host_ssh_user=$HOST_SSH_USER \
             --host_ssh_pass=$HOST_SSH_PASS \
             --alert_url=$ALERT_URL \
             --monitor_url=$MONITOR_URL \
             --docker_monitor_active=$DOCKER_MONITOR_ACTIVE \
             --linux_health_active=$LINUX_HEALTH_ACTIVE \
             --dynamic_ip_updater=$DYNAMIC_IP_UPDATER \
             --docker_monitor_cron='$DOCKERCRON' \
             --linux_health_cron='$LINUXCRON' \
             --dynamic_ip_cron='$DYNAMICCRON' && \
             set +f && \
             service cron start && \
             tail -f '/dev/null'"
