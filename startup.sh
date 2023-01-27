#!/bin/bash

service cron start
echo "Current Variables set:"
echo "CLIENT_ID: $CLIENT_ID"
echo "CLIENT_SECRET: $CLIENT_SECRET"
cp -r /opt/ceciltemp/* /opt/cecil
/usr/bin/python3 /opt/cecil/webapp.py "$CLIENT_ID" "CLIENT_SECRET"