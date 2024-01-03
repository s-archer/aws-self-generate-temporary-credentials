import argparse

def valid_accountId(account_id):
    if len(account_id) == 12:
        for character in account_id:
            if not character.isdigit():
                raise argparse.ArgumentTypeError('Invalid input - You provided a string that contains a non-numeric character. AWS Account number is a 12 digit number. Example: 123456789876')
        return account_id
    else:
        raise argparse.ArgumentTypeError('Invalid input - You provided a string that does not meet the expected length (12)')


def valid_role(role_name):
    roles = ['Admin','Users','Readonly']
    if not role_name in roles:
        raise argparse.ArgumentTypeError('Invalid input - You provided a role name that does not meet the expected value. Possible values: Admin, Users, Readonly')
    else:
        return role_name


def input():
    parser = argparse.ArgumentParser(
        description='Generates temporary AWS credentials for an access token')
    parser.add_argument('--account-id', action='store', required=True,
                        type=valid_accountId,
                        help='AWS account number for which you want programmatic access. AWS Account number is a 12 digit number. Example: 123456789876')
    parser.add_argument('--role-name', action='store', required=True,
                        type=valid_role,
                        help='Name of the SAML role for which you want programmatic access. Check the AWS single sign-on page to identify which role you have access to. Possible values: Admin, Users, Readonly')
    parser.add_argument('--profile', action='store', required=True,
                        help='Named profile. More info here: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html')    
    args = parser.parse_args()
    return {
        'accountId': args.account_id,
        'roleName': args.role_name,
        'profile': args.profile        
    }