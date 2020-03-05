#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Stop/Start an AWS EC2 instance for Public IP renewal
# This script assumes that:
# * The instance has a Name tag (--instance parameter)
#
# Author: Fabien Loudet

import argparse
import json
import os
import sys
import time
from colorama import Fore
from colorama import Style
from lib.awsctl import ec2ctl

# Parse arguments from command line
parser = argparse.ArgumentParser(description='Restarts an AWS EC2 instance and grab its new Public IP')
parser.add_argument('--config', '-c', type=str, help='AWS credentials file', required=True)
parser.add_argument('--instance', '-i', type=str, help='Name of the instance to restart', required=True)
parser.add_argument('--region', '-r', type=str, help='AWS Region', required=True)

args = parser.parse_args()

aws_shared_credentials_file = args.config
region_name = args.region
target_instance = args.instance

if os.path.isfile(aws_shared_credentials_file):
  os.environ['AWS_SHARED_CREDENTIALS_FILE'] = aws_shared_credentials_file
else:
  print("Unable to find '" + aws_shared_credentials_file + "'.")
  sys.exit(1)

# Initialize API client
ec2client = ec2ctl(region_name)

instance_id = ec2client.getInstanceIdFromName(target_instance)

if instance_id is None:
  print('Unable to find an instance with the Name ' + target_instance + ' on region ' + region_name)
  sys.exit(1)

print(" * InstanceId : " + instance_id)

instance_public_ip = ec2client.getInstancePublicIp(instance_id)

if instance_public_ip is None:
  instance_public_ip = Fore.RED + 'N/A' + Style.RESET_ALL

print(" * InstancePublicIpAddress : " + instance_public_ip)

instance_state = ec2client.getInstanceState(instance_id)

print(" * Instance State : " + instance_state)

if instance_state != 'running':
  print("Instance '" + target_instance + "' is not in a running state, aborting.")
else:
  print("Stopping '" + target_instance + "'.", end='', flush=True)
  ec2client.stopInstance(instance_id)

timeout = 30
while instance_state != 'stopped' and timeout >= 0:
  instance_state = ec2client.getInstanceState(instance_id)
  print('.', end='', flush=True)
  timeout -= 1
  time.sleep(1)
print('\n')

if instance_state != 'stopped':
  print(Fore.RED + "Instance '" + target_instance + "' is still not in a stopped state, aborting." + Style.RESET_ALL)
  sys.exit(1)
else:
  print("'" + target_instance + "' has been successfully stopped")
  print("Starting instance '" + target_instance + "'.", end='', flush=True)
  ec2client.startInstance(instance_id)

timeout = 30
while instance_state != 'running' and timeout >= 0:
  instance_state = ec2client.getInstanceState(instance_id)
  print('.', end='', flush=True)
  timeout -= 1
  time.sleep(1)
print('\n')

if instance_state != 'running':
  print(Fore.RED + "Instance '" + target_instance + "' is still not in a running state, please check." + Style.RESET_ALL)
  sys.exit(1)
else:
  print("'" + target_instance + "' has been successfully started")

instance_public_ip = ec2client.getInstancePublicIp(instance_id)

if instance_public_ip is None:
  instance_public_ip = Fore.RED + 'N/A' + Style.RESET_ALL
else:
  instance_public_ip = Fore.GREEN + instance_public_ip + Style.RESET_ALL

print(" * InstancePublicIpAddress : " + instance_public_ip)

