#!/usr/bin/env python
""" MFW Status Report """
# -*- coding: utf-8 -*- 

#----------------------------------------------------------------------------------------
# server-health-check
# Version: 0.7
# 
# WebSite:
# https://github.com/madeofpendletonwool/
# 
# Collin Pendleton <collinp@collinpendleton.com>
# --------------------------------------------------------------------- #
# Import General modules
import sys
import os
# import datetime
# import time
import platform
import requests

# --------------------------------------------------------------------- #
# Arg Vars
request_url = sys.argv[1]
# --------------------------------------------------------------------- #
# Add local lib path
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname) + "/modules/")

# Import MFW Lib General
from mfw_lib_general import get_network_ip
from mfw_lib_general import get_timestamp
from mfw_lib_general import get_hostname
from mfw_lib_general import get_osversion
from mfw_lib_general import get_external_ip

# Import MFW Status
from mfw_lib_status import get_uptime
from mfw_lib_status import get_cpuload
from mfw_lib_status import get_memfree
from mfw_lib_status import get_memfreeGB
from mfw_lib_status import get_memtotal
from mfw_lib_status import get_uptime
from mfw_lib_status import get_processcount
from mfw_lib_status import get_processmax
from mfw_lib_status import get_swapused
from mfw_lib_status import get_swaptotal
from mfw_lib_status import get_swappercent
from mfw_lib_status import get_diskused
from mfw_lib_status import get_disktotal
from mfw_lib_status import get_diskpercent
from mfw_lib_status import get_updatesavailable

# --------------------------------------------------------------------- #
def gather_info():
    """ gather_info """
    msg_desc = "Generated date = " + get_timestamp() + "\n"
    msg_desc += "hostname =" + get_hostname() + "\n"
    msg_desc += "Ip = " + get_network_ip() + "\n"
    msg_desc += "Ip External = " + get_external_ip() + "\n"
    msg_desc += "System = " + platform.system() + "\n"
    msg_desc += "Operating System = " + get_osversion() + "\n"
    msg_desc += "Kernel = " + platform.release() + "\n"
    msg_desc += "CPU Load = " + get_cpuload() +  "\n"
    msg_desc += "Memory = Used: " + get_memfreeGB() + " GB - " + get_memfree() + "%," + " Total: " + get_memtotal() + "GB" + "\n"
    msg_desc += "Swap = Used: " + get_swapused() + " GB - " + get_swappercent() + "%" + ", Total: " + get_swaptotal() + " GB \n"
    msg_desc += "Root = Used: " + get_diskused() + " GB - " + get_diskpercent() + "%" + ", Total: " + get_disktotal() + " GB \n"
    msg_desc += "Processes = " + get_processcount() + " running processes of " + get_processmax() + " maximum processes \n"
    msg_desc += "Last Reboot = " + get_uptime() + "\n"
    msg_desc += "Number of Available Updates = " + get_updatesavailable()
    send_notification(msg_desc)
# --------------------------------------------------------------------- #
def send_notification(msg_desc):
    send_data = f'''
    New Health Script Posted!
    {msg_desc} 
    Good Morning! Have a great day! 😀
    '''
    requests.post(request_url, data=send_data.encode(encoding='utf-8'))



# --------------------------------------------------------------------- #
# Main

gather_info()


# --------------------------------------------------------------------- #
