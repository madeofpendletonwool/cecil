 
#! /usr/bin/env python
#
# dell_hw_health.py, python script using Redfish API to get system hardware
# health based on GetSystemHWInventoryREDFISH.py by Texas Roemer
# <Texas_Roemer@Dell.com>
#
# _author_ = Lorenzo Gaggini  <lorenzo.gaggini@dada.eu>,
# Texas Roemer <Texas_Roemer@Dell.com>
# _version_ = 1.0
#
# Copyright (c) 2018, Dell, Inc., 2019, Lorenzo Gaggini
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
import requests
import sys
import re
# import argparse
from datetime import datetime
import logging
import os
import time
import signal

current_path = os.path.dirname(os.path.abspath(__file__))

class Timeout():
  """Timeout class using ALARM signal"""
  class Timeout(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    signal.alarm(0) # disable alarm

  def raise_timeout(self, *args):
    raise Timeout.Timeout()



def test_idrac(ip, user, password):


    requests.packages.urllib3.disable_warnings()

    logger = logging.getLogger('dell_hw_health')
    logging.basicConfig()

    ENDPOINT = '/redfish/v1/Systems/System.Embedded.1'


    def check_supported_idrac_version():
        try:
            with Timeout(10):
                response = requests.get('https://%s%s' % (idrac_ip, ENDPOINT),
                                        verify=False,
                                        auth=(idrac_username, idrac_password))
        except:
            # print("No response at this IP :'(")
            return_code = "No response at this IP :'("
            return return_code
        if response.status_code != 200:
            # msg = 'WARNING, iDRAC version installed does not support ' +\
            #     'this feature using Redfish API'
            print('Either the iDrac does not support Refish API or the credentials are wrong. Could be too old :/')
            return 'Either the iDrac does not support Refish API or the credentials are wrong. Could be too old :/'
            # logger.warning(msg)
        else:
            pass


    def get_system_information():
        global serverSN
        global HostName
        response = requests.get('https://%s%s' % (idrac_ip, ENDPOINT),
                                verify=False,
                                auth=(idrac_username, idrac_password))
        data = response.json()
        if response.status_code != 200:
            logger.error('FAIL, get command failed, error is: %s' % data)
            print('iDrac not responding. Check IP, user, and pass, then try again.')
            return 'iDrac not responding. Check IP, user, and pass, then try again.'

            sys.exit(2)
        serverSN = data[u'SerialNumber']
        HostName = data[u'HostName']
        return HostName



    idrac_ip = ip
    idrac_username = user
    idrac_password = password



    errormsg = check_supported_idrac_version()

    if errormsg != "No response at this IP :'(":
        if errormsg != 'Either the iDrac does not support Refish API or the credentials are wrong. Could be too old :/':
            HostName = get_system_information()

            try:
                print(f'Host at {idrac_ip} responded! Hit save to remember credentials!')
                return f'Host at {idrac_ip} responded! Hit save to remember credentials!'
                with open(current_path + '/idractest.txt', 'w') as f:
                    f.write(str(errormsg))

            except:
                print('iDrac not responding. Check IP, user, and pass, then try again.')
                return 'iDrac not responding. Check IP, user, and pass, then try again.'
                with open(current_path + '/idractest.txt', 'w') as f:
                    f.write(str(errormsg))
        else:
            with open(current_path + '/idractest.txt', 'w') as f:
                f.write(str(errormsg))

    else: 
        # print(errormsg)
        print(current_path + '/idractest.txt')
        with open(current_path + '/idractest.txt', 'w') as f:
            f.write(str(errormsg))
        return errormsg

if __name__ == "__main__":
    test_value = test_idrac('192.168.2.75', 'root', 'pass')
    print(test_value)