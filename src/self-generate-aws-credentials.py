import json
import os
import boto3
from log import loggerSetup
import logging
from input_parameters import input

loggerSetup.configure()
logger = logging.getLogger(__name__)
cred_file_path = os.path.expanduser('~/.aws/') + 'credentials'

# Read aws cache for authentication token
def read_token_from_aws_cache():
    dir = os.path.expanduser('~/.aws/sso/cache')
    json_files = [pos_json for pos_json in os.listdir(dir) if pos_json.endswith('.json')]

    for json_file in json_files:
        path = dir + '/' + json_file
        with open(path) as file:
            data = json.load(file)
            if 'accessToken' in data:
                accessToken = data['accessToken']

    logger.info('access token acquired from aws cache')
    return accessToken

# Using the token from read_token_from_aws_cache, we generate temporary credentials
def generate_credentials(accountId,roleName,accessToken,profile):
    credentials = []
    
    client = boto3.client('sso', region_name='us-east-1')
    response = client.get_role_credentials(
        roleName=roleName,
        accountId=accountId,
        accessToken=accessToken
    )
    credentials.append('[' + profile + ']')
    credentials.append('aws_access_key_id = ' + response['roleCredentials']['accessKeyId'])
    credentials.append('aws_secret_access_key = ' + response['roleCredentials']['secretAccessKey'])
    credentials.append('aws_session_token = ' + response['roleCredentials']['sessionToken'])

    logger.info('temporary credentials generated')
    return credentials

# Read aws credentials file on local machine
def read_credentials_file(cred_file_path):
    with open(cred_file_path, "r") as file:
        data = file.read()
        file.close()
    cred_file = list(data.split('\n'))

    logger.debug('Current -> '+json.dumps(cred_file, indent=4))

    logger.info('~/.aws/credentials file read')
    return cred_file

# After reading the credential file, check if the aws profile already exists, if yes -> override, if no -> write
def check_if_profile_exists(cred_file,credentials,profile):
    index = [i for i, string in enumerate(cred_file) if profile in string]

    if not index:
        for i in range(0, len(credentials)):
            cred_file.append(credentials[i])
    else:
        for i in range(0, len(credentials)):
            cred_file[index[0]+i] = credentials[i]

    logger.debug('New -> '+json.dumps(cred_file, indent=4))

    logger.info('credentials file ready to be re-written')
    return cred_file

# Write aws credentials to file on local machine
def write_credentials_file(cred_file_path,cred_file):
    with open(cred_file_path, "w") as file:
        for item in cred_file:
            file.write(item+'\n')
        file.close()

    logger.info('~/.aws/credentials file written')

def main():
    user_input = input()
    accessToken = read_token_from_aws_cache()
    credentials = generate_credentials(user_input['accountId'],user_input['roleName'],accessToken,user_input['profile'])
    current_cred_file = read_credentials_file(cred_file_path)
    new_cred_file = check_if_profile_exists(current_cred_file,credentials,user_input['profile'])
    write_credentials_file(cred_file_path,new_cred_file)

if __name__ == "__main__":
    main()