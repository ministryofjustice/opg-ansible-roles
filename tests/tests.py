import unittest
import sys
import os

testdir = os.path.dirname(__file__)
srcdir = '../filter_plugins'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import ec2_custom

from ansible import errors

class sg_rules(unittest.TestCase):

    def setUp(self):
        self.sg_rules_cidr_many_host_many_port = {
            'ports': '11,12',
            'proto': 'tcp',
            'src': [
                '1.2.3.4',
                '4.5.6.7'
            ]
        }
        self.sg_rules_sg_many_host_many_port = {
            'ports': '11,12',
            'proto': 'tcp',
            'src': [
                'sg-1234abc',
                'sg-abcd123'
            ]
        }
        self.sg_ruleset_dict_cidr = [
            {
                'ports': '11,12',
                'proto': 'tcp',
                'src': [
                    '10.1.2.0/24',
                    '10.2.3.4/32'
                ]
            },
            {
                'ports': '11,12',
                'proto': 'usdp',
                'src': [
                    '10.1.2.0/24',
                    '10.2.3.4/32'
                ]
            }
            ]
        self.sg_ruleset_dict_sg = [
            {
                'ports': '11,12',
                'proto': 'tcp',
                'src': [
                    'sg-1234abc',
                    'sg-abcd123'
                ]
            },
            {
                'ports': '11,12',
                'proto': 'tcp',
                'src': [
                    'sg-1234abc',
                    'sg-abcd123'
                ]
            }
            ]
        self.sg_results_var = [
                {
                    "_ansible_item_result": True,
                    "_ansible_no_log": False,
                    "changed": False,
                    "item": {
                        "Name": "jumphost",
                        "description": "External access to jumphost",
                        "ruleset": [
                            {
                                "ports": "22",
                                "proto": "tcp",
                                "src": [
                                    "81.134.202.29/32",
                                    "52.30.28.165/32"
                                ]
                            }
                        ]
                    },
                    "skip_reason": "Conditional check failed",
                    "skipped": True
                },
                {
                    "_ansible_item_result": True,
                    "_ansible_no_log": False,
                    "changed": False,
                    "group_id": "sg-4631a921",
                    "invocation": {
                        "module_args": {
                            "aws_access_key": None,
                            "aws_secret_key": None,
                            "description": "elb monitoring security group for devops-dev",
                            "ec2_url": None,
                            "name": "elb-monitoring-devops-dev",
                            "profile": None,
                            "purge_rules": True,
                            "purge_rules_egress": True,
                            "region": None,
                            "rules": [
                                {
                                    "cidr_ip": "81.134.202.29/32",
                                    "from_port": 443,
                                    "proto": "tcp",
                                    "to_port": 443
                                }
                            ],
                            "rules_egress": None,
                            "security_token": None,
                            "state": "present",
                            "validate_certs": True,
                            "vpc_id": "vpc-b98557dd"
                        },
                        "module_name": "ec2_group"
                    },
                    "item": {
                        "Name": "elb-monitoring",
                        "description": "External monitoring",
                        "ruleset": [
                            {
                                "ports": "443",
                                "proto": "tcp",
                                "src": [
                                    "81.134.202.29/32"
                                ]
                            }
                        ]
                    }
                },
                {
                    "_ansible_item_result": True,
                    "_ansible_no_log": False,
                    "changed": False,
                    "item": {
                        "Name": "salt-master",
                        "description": "Minion access to salt-master",
                        "ruleset": [
                            {
                                "ports": "4505,4506",
                                "proto": "tcp"
                            }
                        ]
                    },
                    "skip_reason": "Conditional check failed",
                    "skipped": True
                },
                {
                    "_ansible_item_result": True,
                    "_ansible_no_log": False,
                    "changed": False,
                    "item": {
                        "Name": "monitoring",
                        "description": "monitoring security group",
                        "ruleset": [
                            {
                                "ports": "6379,9200,2003,2514,8003,5671",
                                "proto": "tcp"
                            },
                            {
                                "ports": "2003,2514,8125",
                                "proto": "udp"
                            }
                        ]
                    },
                    "skip_reason": "Conditional check failed",
                    "skipped": True
                }
            ]



    def test_make_rules_cidr(self):
        result = ec2_custom.make_rules(
            self.sg_rules_cidr_many_host_many_port.get('src'),
            self.sg_rules_cidr_many_host_many_port.get('ports'),
            self.sg_rules_cidr_many_host_many_port.get('proto')
        )
        self.assertIsInstance(result, list)


    def test_make_rules_sg(self):
        result = ec2_custom.make_rules(
            self.sg_rules_sg_many_host_many_port.get('src'),
            self.sg_rules_sg_many_host_many_port.get('ports'),
            self.sg_rules_sg_many_host_many_port.get('proto'),
            True
        )
        self.assertIsInstance(result, list)


    def test_make_rules_no_hosts(self):
        with self.assertRaises(errors.AnsibleFilterError) as rules:
            result = ec2_custom.make_rules(
            None,
            self.sg_rules_sg_many_host_many_port.get('ports'),
            self.sg_rules_sg_many_host_many_port.get('proto'),
            True
            )
        self.assertIsInstance(rules.exception, errors.AnsibleFilterError)


    def test_make_rules_no_ports(self):
        with self.assertRaises(errors.AnsibleFilterError) as rules:
            result = ec2_custom.make_rules(
                self.sg_rules_sg_many_host_many_port.get('src'),
                None,
                self.sg_rules_sg_many_host_many_port.get('proto'),
                True
            )
        self.assertIsInstance(rules.exception, errors.AnsibleFilterError)


    def test_make_rules_no_proto(self):
        with self.assertRaises(errors.AnsibleFilterError) as rules:
            ec2_custom.make_rules(
                self.sg_rules_sg_many_host_many_port.get('src'),
                self.sg_rules_sg_many_host_many_port.get('port'),
                None,
                True
            )
        self.assertIsInstance(rules.exception, errors.AnsibleFilterError)


    def test_rules_from_dict_cidr(self):
        result = ec2_custom.rules_from_dict(
            self.sg_ruleset_dict_cidr
        )
        self.assertIsInstance(result, list)
        self.assertIn('cidr_ip', result[0].keys())

    def test_rules_from_dict_sg(self):
        result = ec2_custom.rules_from_dict(
            self.sg_ruleset_dict_sg
        )
        self.assertIsInstance(result, list)
        self.assertIn('group_id', result[0].keys())


    def test_get_dict_from_results_var(self):
        result = ec2_custom.get_sg_result(self.sg_results_var)
        self.assertIsInstance(result, dict)


    def test_get_id_from_results_var(self):
        result = ec2_custom.get_sg_id_result(self.sg_results_var)
        self.assertIsInstance(result, str)



if __name__ == '__main__':
    unittest.main()

