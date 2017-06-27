#!/usr/bin/python

DOCUMENTATION = '''
---
module: ec2_vpc_nat_gateway_facts
short_description: Retrieve information about a nat gateway
description:
  - Retrieve information about an Nat Gateway. Inspired by https://github.com/ansible/ansible-modules-extras/pull/1687
author: Tim McArthur
requirements:
  - Requires the Boto module
options:
  subnet_id:
    description:
      - The subnet_id to check for.
    required: true
    default: null
    aliases: []
extends_documentation_fragment: aws
'''

EXAMPLES = '''
  - name: Retrieve details for the Nat gateway
    ec2_vpc_nat_gateway_facts: subnet_id="subnet-12345"
    register: nat_gw_data
  - debug: var=nat_gw_data
'''

try:
    import boto3
    import botocore
    HAS_BOTO_3 = True
except ImportError:
    HAS_BOTO_3 = False
from distutils.version import LooseVersion

if LooseVersion(botocore.__version__) < LooseVersion("1.3.14"):
    HAS_SUFFICIENT_BOTOCORE = False
else:
    HAS_SUFFICIENT_BOTOCORE = True


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            subnet_id=dict(required=True),
        )
    )
    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
    try:
        if not HAS_BOTO_3:
            module.fail_json(msg='boto3 and botocore are required.')
        if not HAS_SUFFICIENT_BOTOCORE:
            module.fail_json(msg='botocore version 1.3.14 or above is required.')
        ec2_client = boto3_conn(module,
                                conn_type='client',
                                resource='ec2',
                                region=region,
                                endpoint=ec2_url,
                                **aws_connect_kwargs)

        subnet_id = module.params['subnet_id']

        results = ec2_client.describe_nat_gateways(Filter=[
                {
                    'Name': 'subnet-id',
                    'Values': [subnet_id]
                },
                {
                    'Name': 'state',
                    'Values': ['available']
                }
            ])
        module.exit_json(**results)
    except boto.exception.BotoServerError as e:
        module.fail_json(msg=e.body)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()
