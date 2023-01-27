#!/bin/bash

service cron start
tail -f /dev/null
/usr/bin/python3 /opt/cecil/webapp.py $1 $2