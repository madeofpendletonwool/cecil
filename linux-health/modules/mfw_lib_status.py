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
# Include modules
import subprocess
import re
import psutil
import os
import time
import datetime

# --------------------------------------------------------------------- #
# get_cpuload

def get_cpuload():
    """ get_cpuload """
    ## call command ##
    output = str(psutil.cpu_percent(8))

    return output


# --------------------------------------------------------------------- #
# get_memfreeb

def get_memfree():
    """ get_memfreeb """
    output = str(psutil.virtual_memory()[2])
    return output

# --------------------------------------------------------------------- #


# get_memfreeGB

def get_memfreeGB():
    """ get_memfreeb """
    memfree = psutil.virtual_memory()[3]/1000000000
    memround = round(memfree, 2)
    output = str(memround)
    return output

# --------------------------------------------------------------------- #

def get_memtotal():
    """ get_memtotalb """
    ## call command ##
    memtotal = psutil.virtual_memory().total/1000000000
    memtround = round(memtotal, 2)
    output = str(memtround)
    return output

# --------------------------------------------------------------------- #
# get_uptimeminutes

def get_uptime():
    """ get_uptimeminutes """
    output = str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))

    return output


# --------------------------------------------------------------------- #
# get_processcount

def get_processcount():
    """ get_processcount """
    ## call command ##
    output = os.popen('ps -Afl | wc -l').read()
    return output.strip('\n')

# --------------------------------------------------------------------- #
# get_processcount

def get_updatesavailable():
    # Check Update System Type
    """ get_osversion """
    ## call command ##
    with open('/etc/os-release') as fi:
        for ln in fi:
            if ln.startswith("ID_LIKE="):
                out_like = ln
                version = out_like.strip()[8:]
    
    if version == "debian":            

        # Get updates available Debian
        output = os.popen('/usr/lib/update-notifier/apt-check --human-readable').read()
    elif version == "arch":
        os.system('pacman -Sy > /dev/null')
        output = os.popen('pacman -Qu | wc -l').read()

    return output

# --------------------------------------------------------------------- #
# get_processmax

def get_processmax():
    """ get_processmax """
    ## call command ##
    output = os.popen('ulimit -u').read()
    return output.strip('\n')

# --------------------------------------------------------------------- #
# get_swapfreeb

def get_swapused():
    """ get_swapfreeb """
    ## call command ##
    swapused = psutil.swap_memory().used/1000000000
    swapround = round(swapused, 2)
    output = str(swapround)
    return output


# --------------------------------------------------------------------- #
# get_swapfreeb

def get_swappercent():
    """ get_swapfreeb """
    ## call command ##
    output = str(psutil.swap_memory().percent)
    return output


# --------------------------------------------------------------------- #
# get_swaptotalb

def get_swaptotal():
    """ get_swaptotalb """
    ## call command ##
    swaptotal = psutil.swap_memory().total/1000000000
    swaptround = round(swaptotal, 2)
    output = str(swaptround)
    return output

# --------------------------------------------------------------------- #
# get_rootusedb

def get_diskused():
    """ get_rootusedb """
    ## call command ##
    diskused = psutil.disk_usage('/').used/1000000000
    diskround = round(diskused, 2)
    output = str(diskround)
    return output

# --------------------------------------------------------------------- #
# get_roottotalb

def get_disktotal():
    """ get_rootusedb """
    ## call command ##
    disktotal = psutil.disk_usage('/').total/1000000000
    disktround = round(disktotal, 2)
    output = str(disktround)
    return output

# --------------------------------------------------------------------- #
# get_roottotalb

def get_diskpercent():
    """ get_rootusedb """
    ## call command ##
    output = str(psutil.disk_usage('/').percent)
    return output