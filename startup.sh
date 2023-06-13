#!/bin/bash

service cron start
echo "Current Variables set:"
echo "CLIENT_ID: $CLIENT_ID"
echo "CLIENT_SECRET: $CLIENT_SECRET"
echo "AUTH_URL: $AUTH_URL"
echo "CONFIG PATH: $CONFIG_PATH"
echo "ENCRYPTION_KEY: $ENCRYPTION_KEY"
echo "USERNAME: $USERNAME"
echo "PASSWORD: $PASSWORD"
cp -r /opt/ceciltemp/* /opt/cecil
/usr/bin/python3 /opt/cecil/webapp.py --config_path "$CONFIG_PATH" --client_id "$CLIENT_ID" --client_secret "$CLIENT_SECRET" --auth_url "$AUTH_URL" --encryption_key "$ENCRYPTION_KEY" --username "$USERNAME" --password "$PASSWORD"
