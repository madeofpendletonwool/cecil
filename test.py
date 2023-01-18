from dell_idrac_scan.test_idrac import test_idrac
import os
import time
import signal

current_path = os.path.dirname(os.path.abspath(__file__))

ip = 'sdf'
user = 'sdf'
password = 'sdf'


test_idrac(ip, user, password)


with open(current_path + '/dell_idrac_scan/idractest.txt', 'r') as file:
    data = file.read()

print(data)