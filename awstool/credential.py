# -*- coding: utf-8 -*-
import configparser
import re
from getpass import getpass
import boto3
import requests

from awstool.account import generate_account
from awstool.config import account_config_file, aws_config_file, outputformat, flag_max_session_duration, \
    user_config_file, sso_section


def get_asseration():
    user_config = configparser.ConfigParser()
    user_config.read(user_config_file)

    idpentryurl = 'https://' + user_config[sso_section][
        'idp_domain'] + '/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices'
    username = user_config[sso_section]['username']
    password = user_config[sso_section]['password']

    session = requests.Session()
    response = session.get(idpentryurl)
    m = re.search('action="([^"]+)"', response.text)
    idpauthformsubmiturl = "https://" + user_config[sso_section]['idp_domain'] + m.group(1)
    payload = {
        'UserName': username,
        'Password': password,
        'AuthMethod': 'FormsAuthentication'
    }

    response = session.post(idpauthformsubmiturl, data=payload)

    # Get context of MFA payload
    response = session.get(idpauthformsubmiturl)
    m = re.search('context" type="hidden" name="Context" value="([^"]+)"', response.text)
    context = m.group(1)
    payload = {
        'AuthMethod': 'SecurIDv2Authentication',
        'Context': context,
        'InitStatus': 'true'
    }

    response = session.post(idpauthformsubmiturl, data=payload)
    m = re.search('context" type="hidden" name="Context" value="([^"]+)"', response.text)
    context = m.group(1)

    passcode = getpass("Enter your RSA SecurID passcode:")

    payload = {
        'AuthMethod': 'SecurIDv2Authentication',
        'Context': context,
        'Passcode': passcode
    }

    response = session.post(idpauthformsubmiturl, data=payload)
    m = re.search('input type="hidden" name="SAMLResponse" value="([^"]+)"', response.text)
    assertion = m.group(1)
    if assertion == '':
        print('Response did not contain a valid SAML assertion')
        return None
    return session, assertion


def generate_credential(account, saml_assertion):
    regions = ['ca-central-1', 'us-east-1', 'us-west-2']

    for region in regions:
        pattern = '^' + region
        m = re.search(pattern, account)
        if m:
            region = m.group(0)
            break
    else:
        # set default region
        region = 'us-east-1'

    account_config = configparser.ConfigParser()
    account_config.read(account_config_file)

    role_arn = account_config[account]['role_arn']
    principal_arn = account_config[account]['principal_arn']
    # Use the assertion to get an AWS STS token using Assume Role with SAML
    client = boto3.client('sts', region_name=region)
    response = client.assume_role_with_saml(
        RoleArn=role_arn,
        PrincipalArn=principal_arn,
        SAMLAssertion=saml_assertion,
    )

    # https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html
    if flag_max_session_duration:
        # print("Try to get MaxSessionDuration for {0}".format(account))
        client_iam = boto3.client('iam', region_name=region,
                                  aws_access_key_id=response['Credentials']['AccessKeyId'],
                                  aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                  aws_session_token=response['Credentials']['SessionToken'])
        role_name = role_arn.split('role/')[1]
        try:
            response_iam = client_iam.get_role(RoleName=role_name)
            max_session_duration = response_iam['Role']['MaxSessionDuration']
            response = client.assume_role_with_saml(
                RoleArn=role_arn,
                PrincipalArn=principal_arn,
                SAMLAssertion=saml_assertion,
                DurationSeconds=max_session_duration
            )
        except Exception:
            print("Failed to get MaxSessionDuration for {0}. Use default 3600".format(account))

    # Read in the existing config file
    aws_config = configparser.RawConfigParser()
    aws_config.read(aws_config_file)

    # Put the credentials into a saml specific section instead of clobbering
    # the default credentials
    if not aws_config.has_section(account):
        aws_config.add_section(account)

    aws_config.set(account, 'output', outputformat)
    aws_config.set(account, 'region', region)
    aws_config.set(account, 'aws_access_key_id', response['Credentials']['AccessKeyId'])
    aws_config.set(account, 'aws_secret_access_key', response['Credentials']['SecretAccessKey'])
    aws_config.set(account, 'aws_session_token', response['Credentials']['SessionToken'])

    # Write the updated config file
    with open(aws_config_file, 'w+') as configfile:
        aws_config.write(configfile)

    # Give the user some basic info as to what has just happened
    print('-'*40)
    print('Key in {0} under {1} profile.'.format(aws_config_file, account))
    print('Expire at {0}.'.format(response['Credentials']['Expiration']))
    print('CLI(e.g. aws --profile {0} ec2 describe-instances --max-items 2).'.format(account))


def generate_credentials(args):
    flag_generate_account = args.generate_account
    print("flag_generate_account: {}".format(flag_generate_account))
    session, assertion = get_asseration()
    if flag_generate_account:
        generate_account(session, assertion)

    accounts = configparser.ConfigParser()
    accounts.read(account_config_file)
    for account in accounts.sections():
        generate_credential(account, assertion)
