 
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
RUN pip install -r requirements.txt
# Put cecil Files in place
RUN 
# Create structure for cecil
RUN mkdir mkdir -p /opt/cecil/TEMP && \
    git clone https://github.com/madeofpendletonwool/cecil.git /opt/cecil && \
    chmod -R 755 /opt
# Begin cecil Setup
ENTRYPOINT [ /bin/bash -c \
             "/usr/bin/bash /opt/cecil/cecilcontained.py \
             --host_ssh_ip=$HOST_SSH_IP \
             --host_ssh_user=$HOST_SSH_USER \
             --host_ssh_pass=$HOST_SSH_PASS \
             --alert_url=$alert_url \
             --monitor_url=$MONITOR_URL \
             --docker_monitor_active=$DOCKER_MONITOR_ACTIVE \
             --linux_health_active=$LINUX_HEALTH_ACTIVE \
             --dynamic_ip_updater=$DYNAMIC_IP_UPDATER \
             --docker_monitor_cron=$DOCKER_MONITOR_CRON \
             --linux_health_cron=$LINUX_HEALTH_CRON \
             --dynamic_ip_cron=$DYNAMIC_IP_CRON \
             service cron start && \
             tail -f /dev/null" ]
