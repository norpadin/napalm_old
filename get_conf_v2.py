#!/usr/bin/env python3
#-*- coding: utf-8 -*-

__author__ = "Norberto Padin"
__email__ = "norberto.padin@bvstv.com"
__webpage__ = "https://github.com/norpadin"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2023, all rights reserved."
__license__ = "MIT License."



from napalm import get_network_driver
import csv
import ping3

# Use the appropriate network driver to connect to the device:
driver = get_network_driver('ios')

# Function to check reachability using ping
def check_reachability(ip):
    try:
        response_time = ping3.ping(ip, timeout=2)
        if response_time is not None:
            return True
        else:
            return False
    except:
        return False


# Function to connect to the device and retrieve information
def retrieve_device_info(ip, username, password):
    # Create an SSH client
    print(ip, username, password)
    try:
        # Connect:
        device = driver(
            hostname=ip,
            username=username,
            password=password,
            optional_args={"port": 22},
        )

        device.open()

        facts = device.get_facts()
        return True, facts['hostname'], facts['model'], facts['os_version']
    except:
        return False, None, None, None


# Read IP addresses from the first CSV file
ip_addresses = []
with open('ip_addresses.csv', 'r') as ip_file:
    csv_reader = csv.reader(ip_file)
    for row in csv_reader:
        ip_addresses.append(row[0])


# Read username-password pairs from the second CSV file
credentials = []
with open('credentials.csv', 'r') as cred_file:
    csv_reader = csv.reader(cred_file)
    for row in csv_reader:
        credentials.append((row[0], row[1]))


# Iterate over each IP address
for ip in ip_addresses:
    if check_reachability(ip):
        # Iterate over each set of credentials
        for username, password in credentials:
            reachability, hostname, device_type, ios_version = retrieve_device_info(ip, username, password)
            if reachability:
                print("IP:", ip)
                print("Reachability: TRUE")
                print("Hostname:", hostname)
                print("Device Type:", device_type)
                print("IOS Version:", ios_version)
                print()
                # Exit the loop once successful connection is established
                break
        else:
            # Executed if no successful connection is established for any credentials
            print("IP:", ip)
            print("Wrong username or password")
            print()
    else:
        # Executed if ping to the IP address fails
        print("IP:", ip)
        print("No reachability")
        print()
