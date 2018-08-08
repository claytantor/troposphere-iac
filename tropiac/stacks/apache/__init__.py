#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
from __future__ import print_function

import fileinput
from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2
import yaml
import logging
import argparse
import sys, os

def get_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open("{0}/config.yaml".format(dir_path), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    return cfg

def make_template(cfg):

    template = Template()

    # needs to be passed during the boto create stack call
    keyname_param = template.add_parameter(Parameter(
        "KeyName",
        Description="Name of an existing EC2 KeyPair to enable SSH "
                    "access to the instance",
        Type="String",
    ))

    template.add_mapping('RegionMap', cfg['RegionMap'])

    ec2_instance = template.add_resource(ec2.Instance(
        "Ec2Instance",
        ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
        InstanceType=cfg['InstanceType'],
        KeyName=Ref(keyname_param),
        SecurityGroups=cfg['SecurityGroups'],
        UserData=Base64("80")
    ))

    template.add_output([
        Output(
            "InstanceId",
            Description="InstanceId of the newly created EC2 instance",
            Value=Ref(ec2_instance),
        ),
        Output(
            "AZ",
            Description="Availability Zone of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "AvailabilityZone"),
        ),
        Output(
            "PublicIP",
            Description="Public IP address of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "PublicIp"),
        ),
        Output(
            "PrivateIP",
            Description="Private IP address of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "PrivateIp"),
        ),
        Output(
            "PublicDNS",
            Description="Public DNSName of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "PublicDnsName"),
        ),
        Output(
            "PrivateDNS",
            Description="Private DNSName of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "PrivateDnsName"),
        ),
    ])

    return template
