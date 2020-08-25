# -*- coding: utf-8 -*-
from os.path import expanduser, join

base_dir = join(expanduser("~"), '.aws')
sso_section = 'SSO'

user_config_name = 'user'
user_config_file = join(base_dir, user_config_name)

account_config_name = 'account'
account_config_file = join(base_dir, account_config_name)

aws_config_name = 'credentials'
aws_config_file = join(base_dir, aws_config_name)

outputformat = 'yaml'

flag_max_session_duration = True
