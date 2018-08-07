#!/usr/bin/env python
# coding: utf-8

import os
import json
import logging
import argparse
import boto3
import botocore
import urllib2
import botocore
import sys
import time
import signal
import fileinput

from urlparse import urlparse, parse_qs
from utils import make_cloudformation_client, load_config, get_log_level

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

# Parameters=[
#     {
#         'ParameterKey': 'string',
#         'ParameterValue': 'string',
#         'UsePreviousValue': False
#     },
# ],
def make_kv_from_args(params_as_querystring, name_prefix="", use_previous=None):

    nvs = parse_qs(params_as_querystring)

    #{'i': ['main'], 'enc': [' Hello '], 'mode': ['front'], 'sid': ['12ab']}
    kv_pairs = []
    for key in nvs:
        # print "key: %s , value: %s" % (key, nvs[key])
        kv = {
            "{0}Key".format(name_prefix):key,
            "{0}Value".format(name_prefix):nvs[key][0],
        }
        if use_previous != None:
            kv['UsePreviousValue'] = use_previous

        kv_pairs.append(kv)

    return kv_pairs

def json_from_stdin(fileinput):
    new_log=''
    for line in fileinput.input():
        new_log += line

    return new_log

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True,
                       help='the name of the stack to create.')

    parser.add_argument('--params', type=str, required=True,
                       help='the key value pairs for the parameters of the stack.')
    # parser.add_argument('--topicarn', type=str, required=True,
    #                    help='the SNS topic arn for notifications to be sent to.')
    parser.add_argument('--log', type=str, default="INFO", required=False,
                       help='which log level. DEBUG, INFO, WARNING, CRITICAL')
    parser.add_argument('--tags', type=str, required=False,
                       help='the tags to attach to the stack.')
    parser.add_argument('--config', type=str, required=False,
                       help='the config file used for the application.')

    args = parser.parse_args()

    # init LOGGER
    logging.basicConfig(level=get_log_level(args.log), format=LOG_FORMAT)

    #load the client using app config or default
    client = make_cloudformation_client(args.config)

    try:
        # setup the model
        template_object = json_from_stdin(fileinput)

        params = make_kv_from_args(args.params, "Parameter", False)
        tags = make_kv_from_args(args.tags)

        response = client.create_stack(
            StackName=args.name,
            TemplateBody=json.dumps(template_object),
            Parameters=params,
            DisableRollback=False,
            TimeoutInMinutes=2,
            # NotificationARNs=[args.topicarn],
            Tags=tags
        )

        # we expect a response, if its missing on non 200 then show response
        if 'ResponseMetadata' in response and \
            response['ResponseMetadata']['HTTPStatusCode'] < 300:
            logging.info("succeed. response: {0}".format(json.dumps(response)))
        else:
            logging.critical("There was an Unexpected error. response: {0}".format(json.dumps(response)))

    except ValueError as e:
        logging.critical("Value error caught: {0}".format(e))
    except botocore.exceptions.ClientError as e:
        logging.critical("Boto client error caught: {0}".format(e))
    except:
        # catch any failure
        logging.critical("Unexpected error: {0}".format(sys.exc_info()[0]))

if __name__ == '__main__':
    main()
