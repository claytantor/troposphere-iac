#!/usr/bin/env python
from __future__ import print_function

import fileinput
from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2
import yaml
import logging
import argparse

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)



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



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True,
                       help='the name of the vars section to use.')
    parser.add_argument('--log', type=str, default="INFO", required=False,
                       help='which log level. DEBUG, INFO, WARNING, CRITICAL')

    args = parser.parse_args()

    # init LOGGER
    logging.basicConfig(level=get_log_level(args.log), format=LOG_FORMAT)

    with open("vars.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    print(cfg[args.name])

    temlate = make_template(cfg[args.name])
    print(template.to_json())

if __name__ == "__main__": main()
