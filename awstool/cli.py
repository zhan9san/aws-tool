# -*- coding: utf-8 -*-
import argparse
from awstool import APP_DESCRIPTION, APP_NAME, APP_VERSION

from awstool.configure import set_configure
from awstool.credential import generate_credentials


def main():
    parser = argparse.ArgumentParser(prog=APP_NAME, description=APP_DESCRIPTION)
    parser.add_argument('-v', '--version', action='version',
                        version='{} {}'.format(APP_NAME, APP_VERSION))

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_configure = subparsers.add_parser('configure', help='configure help')
    parser_configure.set_defaults(func=set_configure)

    parser_credential = subparsers.add_parser('credential', help='credential help')
    parser_credential.add_argument('--generate-account', help='Generate aws accounts', action='store_true')
    parser_credential.set_defaults(func=generate_credentials)

    args = parser.parse_args()
    args.func(args)
