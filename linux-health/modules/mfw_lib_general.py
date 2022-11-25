#!/usr/bin/env python
""" MFW Common Lib """
# -*- coding: utf-8 -*- 

#----------------------------------------------------------------------------------------
# server-health-check
# Version: 0.7
# 
# WebSite:
# https://github.com/madeofpendletonwool/docker-server-health
# 
# Collin Pendleton <collinp@collinpendleton.com>
#----------------------------------------------------------------------------------------

# --------------------------------------------------------------------- #
import time
import datetime
import socket
import subprocess
# Import Ini Reader
import configparser
import io
# Request
import requests
import os

# --------------------------------------------------------------------- #
# get_network_ip

def get_network_ip():
    """ get_network_ip """
    socket_tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        #s.connect(('10.255.255.255', 1))
        socket_tmp.connect(("8.8.8.8", 80))
        ip_local = socket_tmp.getsockname()[0]
    except:
        # If no internet access, return loopback address
        ip_local = '127.0.0.1'
    finally:
        socket_tmp.close()
    return ip_local.rstrip('\n')

# --------------------------------------------------------------------- #
# get_timestamp

def get_timestamp():
    """ get_timestamp """
    today = datetime.datetime.fromtimestamp(time.time())
    today2 = today.strftime('%Y/%m/%d %H:%M')
    return today2.rstrip('\n')

# --------------------------------------------------------------------- #
# get_hostname

def get_hostname():
    """ get_hostname """
    output = str(socket.gethostname())
    return output

# --------------------------------------------------------------------- #
# get_osversion

def get_osversion():
    """ get_osversion """
    ## call command ##
    with open('/etc/os-release') as fi:
        for ln in fi:
            if ln.startswith("PRETTY_NAME="):
                output = ln
                output = output.strip()[12:]

                return output



# --------------------------------------------------------------------- #
# get_external_ip

def get_external_ip():
    """ get_external_ip """
    output = ip = requests.get('https://api.ipify.org').text
    return output


# --------------------------------------------------------------------- #
