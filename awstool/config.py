# -*- coding: utf-8 -*-
import os
from os.path import expanduser, join

home = expanduser("~")
sso_section = 'SSO'
user_config_name = '.aws/user'
user_config_file = join(home, user_config_name)

account_config_name = '.aws/account'
account_config_file = join(home, account_config_name)

aws_config_name = '.aws/credentials'
aws_config_file = join(home, aws_config_name)

outputformat = 'yaml'

flag_max_session_duration = True
