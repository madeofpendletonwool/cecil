#!/bin/bash

set -f
crontab -l 2>/dev/null; echo '*/10 * * * * /usr/bin/python3 /opt/cecil/DynamicIP-Updater/checkpublicip.py $1' | crontab -
set +f