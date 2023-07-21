import os

def return_vsphere_blank():
    location = os.getcwd() + "/blank_vsphere_config.csv" 
    return location

def return_vsphere_config():
    location = os.getcwd() + "/vsphere_config.csv"