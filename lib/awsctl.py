#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# Author: Fabien Loudet

import boto3
from botocore.exceptions import ClientError


class ec2ctl:
  ec2 = None

  def __init__(self, region_name):
    self.ec2 = boto3.client('ec2', region_name=region_name)

  def getInstanceIdFromName(self, instance_name):

    if(self.ec2):

      response = self.ec2.describe_instances(
          Filters=[
              {
                  'Name': 'tag:Name',
                  'Values': [
                      instance_name,
                  ]
              },
          ],
          MaxResults=10
      )
      try:
        instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]
      except IndexError:
        instance_id = None
      return instance_id

    else:
      print("Error: API client not initialized")

  def getInstancePublicIp(self, instance_id):

    if(self.ec2):

      response = self.ec2.describe_instances(
          InstanceIds=[instance_id]
      )

      try:
        instance_public_ip_address = (response["Reservations"][0]
                                              ["Instances"][0]
                                              ["PublicIpAddress"])
      except KeyError:
        instance_public_ip_address = None
      return instance_public_ip_address

    else:
      print("Error: API client not initialized")

  def getInstanceState(self, instance_id):

    if(self.ec2):

      response = self.ec2.describe_instances(
          InstanceIds=[instance_id]
      )

      return response["Reservations"][0]["Instances"][0]["State"]["Name"]

    else:
      print("Error: API client not initialized")

  def stopInstance(self, instance_id):

    if(self.ec2):

      try:
        self.ec2.stop_instances(InstanceIds=[instance_id])

      except ClientError as e:
        print(e)

    else:
      print("Error: API client not initialized")

  def startInstance(self, instance_id):

    if(self.ec2):

      try:
        self.ec2.start_instances(InstanceIds=[instance_id])

      except ClientError as e:
        print(e)

    else:
      print("Error: API client not initialized")
