#!/bin/bash

crontab -l | grep -v "/opt/cecil/dynamic_ip_scan/checkpublicip.py" | crontab -
