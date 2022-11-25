#!/bin/bash

# Move Files to location always accessible
mkdir /opt/cecil
cp -r /home/$1/cecil/* /opt/cecil/
mkdir /opt/cecil/TEMP

# Install Python modules if needed
pip3 install configparser
pip3 install requests
pip3 install regex
pip3 install psutil
pip3 install argparse
pip3 install logging
pip3 install logging-config
pip3 install os-sys
pip3 install typing 
pip3 install docker 
pip3 install lib-platform