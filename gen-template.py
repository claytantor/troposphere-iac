#!/usr/bin/env python
# coding: utf-8

import logging
import argparse
import importlib

from tropiac.utils import make_cloudformation_client, load_config, get_log_level

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True,
                       help='the name of the stack to create.')
    parser.add_argument('--config', type=str, required=True,
                       help='the name of the configuration section to use.')
    parser.add_argument('--log', type=str, default="INFO", required=False,
                       help='which log level. DEBUG, INFO, WARNING, CRITICAL')

    args = parser.parse_args()

    # init LOGGER
    stack = importlib.import_module('tropiac.stacks.{0}'.format(args.name))
    cfg = stack.get_config()
    template = stack.make_template(cfg[args.config])

    print(template.to_json())


if __name__ == '__main__':
    main()
