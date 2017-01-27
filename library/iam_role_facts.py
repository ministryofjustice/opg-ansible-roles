#!/usr/bin/python

DOCUMENTATION = '''
---
module: iam_role_facts
short_description: Gather facts about IAM roles in AWS.
description:
  - Gather facts about IAM roles
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.

# Gather iam role facts
- iam_role_facts:
    description: Each element consists of a dict with all the information related to that iam role.
    type: list
    sample:

'''

import json
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

try:
    import boto3
    from botocore.exceptions import ClientError, ParamValidationError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


def main():

    argument_spec = ec2_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO3:
        module.fail_json(msg='boto3 required for this module')

    region, ec2_url, aws_connect_params = get_aws_connection_info(module, boto3=True)
    connection = boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=ec2_url, **aws_connect_params)

    try:
        response = connection.list_roles()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            return None
        else:
            module.fail_json(msg=e.message, **camel_dict_to_snake_dict(e.response))

    # TODO: If we have more that 100 iam roles the pagination may kick in.
    # Check response['IsTruncated'] and add code for pagination.

    module.exit_json(iam_roles=response['Roles'])


if __name__ == '__main__':
    main()
