#!/bin/bash

service cron start
/usr/bin/python3 /opt/cecil/webapp.py "$CLIENT_ID" "CLIENT_SECRET"