# Self Generate AWS Credentials

## Introduction

We recently moved our AWS accounts from BIG-IP APM to Azure AD for SAML authentication. In the new model users have the ability to generate just in time programmatic access for themselves (detailed documentatation [here](https://f5.service-now.com/kb_view.do?sysparm_article=KB51164 "AWS Account Access via Azure AD")).

### How It Works

Under the hood when users perform a login call from their terminal, AWS CLI creates a new session for users against their F5 credentials. Once your credentials are validated, AWS CLI creates a token that is time bound and places this on your local machine, and thereafter each CLI call sends this token to validate who you are and your permissions. This works seamlessly for most cases, no credentials are ever stored on your local machine hence reducing the risk of accidental exposure.

### Problem

However, most automation tools/sdks like Terraform, Ansible, Boto3 are not yet compatible with this approach. These tools instead need a pair for Access Key and Secret Access Key, and as we learned earlier the CLI generates only a token. 

## Solution

The current project solves the above problem by converting your session token into a pair of access key/secret access key. The credentials are then stored in on your local machine and just like the initial token they are time bound.

The high level process looks like this

`F5 Credentials --> Local Device Token --> Local Access Key/Secret Access Key`

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

1. [Python3](https://www.python.org/downloads/ "python installation")
1. [Pip](https://pip.pypa.io/en/stable/installing/ "pip installation")
1. [AWSCLI v2.0](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html "AWSCLI")
1. Access to F5 AWS account. If you don't have access, request access [here](https://f5.service-now.com/sp?id=sc_cat_item&sys_id=aa2d8279dbbd6300b2c774dfaa96198e "Access to a cloud account")

```
$ python3 --version
Python 3.7.5

$ pip --version
pip 20.0.2 from /usr/local/lib/python3.7/dist-packages/pip (python 3.7)

$ aws --version
aws-cli/2.0.0 Python/3.7.3 Linux/5.3.0-59-generic botocore/2.0.0dev4
```

### Installation

1. Clone the project onto your local machine

```bash
git clone https://prashant-pandey@dev.azure.com/prashant-pandey/TS/_git/TS
```

2. Navigate to the current directory and use the package manager pip to install the dependencies

```bash
$ cd TS/generate-aws-credentials

$ pip install -r requirements.txt
Defaulting to user installation because normal site-packages is not writeable
....
Installing collected packages: jmespath, urllib3, six, python-dateutil, botocore, boto3
Successfully installed boto3-1.14.4 botocore-1.17.4 jmespath-0.10.0 python-dateutil-2.8.1 six-1.15.0 urllib3-1.25.9
```

## Usage

1. Run clear-cache.py to clean out the cache on your local machine.

```
ls
clear-cache.py  generate-aws-credentials.py  log

$ python3 clear-cache.py
Success! Cache cleared 
```

2. Generate AWSCLI token by providing your F5 credentials.

```
$ aws sso login --profile <PROFILE_NAME>
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://device.sso.us-east-1.amazonaws.com/

Then enter the code:

HKWF-CNHF
Successully logged into Start URL: https://d-90670ec0cd.awsapps.com/start
```

3. Generate credentials for the token created above.

```
$ python3 generate-aws-credentials.py
2020-06-24 13:38:33,117|INFO|generate-aws-credentials.read_token_from_aws_cache:23|access token acquired from aws cache
2020-06-24 13:38:40,934|INFO|generate-aws-credentials.generate_credentials:41|temporary credentials generated
2020-06-24 13:38:40,937|INFO|generate-aws-credentials.check_if_profile_exists:69|credentials file ready to be re-written
2020-06-24 13:38:40,937|INFO|generate-aws-credentials.write_credentials_file:79|~/.aws/credentials file written

```

4. Validate the credentials.

```
$ cat ~/.aws/credentials 

[<PROFILE_NAME>]
aws_access_key_id = <REDACTED>
aws_secret_access_key = <REDACTED>
aws_session_token = <REDACTED>
```

## Authors

[Prashant Pandey](mailto:p.pandey@f5.com "Email Prashant Pandey") - *Initial Work*

## License

This project is licensed under the MIT License - see the LICENSE.md file for details