# -*- coding: utf-8 -*-
import configparser
from getpass import getpass

from awstool.config import user_config_file, sso_section


def set_configure(args):

    user_config = configparser.ConfigParser()
    user_config.read(user_config_file)

    idp_domain = input("Enter your Identity Source Domain(like sso.example.com):")
    username = input("Enter your Identity User(like user@example.com):")
    password = getpass("Enter your Identity Password:")

    if not user_config.has_section(sso_section):
        user_config.add_section(sso_section)

    user_config.set(sso_section, 'idp_domain', idp_domain)
    user_config.set(sso_section, 'username', username)
    user_config.set(sso_section, 'password', password)

    with open(user_config_file, 'w+') as configfile:
        user_config.write(configfile)
