# -*- coding: utf-8 -*-
import configparser
import re
from bs4 import BeautifulSoup

from awstool.config import account_config_file


def get_saml_account(div):
    saml_account_div = div.find("div", {"class": "saml-account-name"})
    saml_account_content = saml_account_div.contents[0]
    m = re.search('Account: ([^ ]+)', saml_account_content)
    saml_account = m.group(1)
    return saml_account


def get_saml_roles(div):
    saml_roles = []
    # saml_roles_inputs = div.find("input", {"type": "radio", "name": "roleIndex"})
    saml_roles_inputs = div.find_all("input", {"type": "radio", "name": "roleIndex"})
    for saml_role in saml_roles_inputs:
        saml_roles.append(saml_role.attrs.get("value"))
    return saml_roles


def generate_account(session, saml_assertion):

    saml_accounts = []
    payload = {
        'SAMLResponse': saml_assertion
    }
    response = session.post('https://signin.aws.amazon.com/saml', data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    saml_account_divs = soup.findAll("div", {"class": "saml-account", "id": None})
    # print("saml_account_divs: {0}".format(saml_account_divs))
    for saml_account_div in saml_account_divs:
        saml_account = get_saml_account(saml_account_div)
        saml_roles = get_saml_roles(saml_account_div)

        for saml_role in saml_roles:
            principal_arn_prefix, group_name = saml_role.split('role/')
            group_name = group_name.lower().replace('_', '-')
            saml_account_tuple = (
                saml_account + '-' + group_name,
                saml_role,
                principal_arn_prefix + 'saml-provider/customer-saml'
            )
            saml_accounts.append(saml_account_tuple)

    # print("saml_accounts: {0}".format(saml_accounts))
    account_config = configparser.ConfigParser()
    # account_config.read(account_config_file)
    for account in saml_accounts:
        if not account_config.has_section(account[0]):
            account_config.add_section(account[0])
        account_config.set(account[0], 'role_arn', account[1])
        account_config.set(account[0], 'principal_arn', account[2])

    with open(account_config_file, 'w+') as configfile:
        account_config.write(configfile)
