#!/bin/bash

service cron start
echo "Current Variables set:"
echo "CLIENT_ID: $CLIENT_ID"
echo "CLIENT_SECRET: $CLIENT_SECRET"
echo "AUTH_URL: $AUTH_URL"
echo "CONFIG PATH: $CONFIG_PATH"
echo "ENCRYPTION_KEY: $ENCRYPTION_KEY"
cp -r /opt/ceciltemp/* /opt/cecil
/usr/bin/python3 /opt/cecil/webapp.py "$CONFIG_PATH" "$CLIENT_ID" "$CLIENT_SECRET" "$AUTH_URL"