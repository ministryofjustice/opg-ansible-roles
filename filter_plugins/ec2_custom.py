from ansible import errors


def get_zone_id(zone_data, zone_name):
    # print "{}".format(zone_data.get('HostedZones'))
    for x in zone_data.get('HostedZones'):
        if zone_name in x.get('Name'):
            zid = x.get('Id').split('/')
            return zid[2]
    return None


def validate_ruleset(ports, proto):
    '''
    check for emtpy values
    :param ports: should be list
    :param proto: should be list
    :raise: ansible error on failure
    '''
    if proto is None or len(proto) < 0:
        raise errors.AnsibleFilterError('proto is empty or missing')
    if ports is None or len(ports) < 0:
        raise errors.AnsibleFilterError('ports is empty or missing')


def rules_from_dict(rules, src_list=None):
    '''
    rules:
      - ports: '22'
          proto: tcp
          src: (optional)

     ec2_group:
       rules: "{{ rules | rules_from_dict() }}"

    :param rules: list of rule
    :param src_list: src group/cidr list
    :return: list of rules
    '''

    if isinstance(rules, list):
        rule_list = []
        if len(rules) > 0:
            for rule in rules:
                if 'src' in rule.keys():
                    src_list = rule.get('src')
                if isinstance(src_list, list) and len(src_list) > 0:
                    rule_list += make_rules(src_list, rule['ports'], rule['proto'], ('sg' in src_list[0]))
                else:
                    raise errors.AnsibleFilterError('src host or security group list empty or not a list')
            return rule_list
        else:
            raise errors.AnsibleFilterError('Rules list is empty')
    else:
        raise errors.AnsibleFilterError('Rules data must be a list')


def make_rules(hosts, ports, proto, group=False):
    '''
    inspiration: https://gist.github.com/viesti/1febe79938c09cc29501

    :param hosts: list
    :param ports: comma separated string
    :param proto: string
    :param group: bool default false
    :return: rules as list of dicts
    '''
    if isinstance(hosts, list) and len(hosts) > 0:
        validate_ruleset(ports, proto)
        if group:
            return [{'proto': proto,
                     'from_port': port,
                     'to_port': port,
                     'group_id': sg} for sg in hosts for port in map(int, ports.split(','))]
        return [{'proto': proto,
                 'from_port': port,
                 'to_port': port,
                 'cidr_ip': host} for host in hosts for port in map(int, ports.split(','))]
    else:
        raise errors.AnsibleFilterError('list of hosts or security groups must be a list')


def get_sg_result(result_list):
    if isinstance(result_list, list) and len(result_list) > 0:
        for result in result_list:
            if result.get('group_id'):
                return result
    else:
        raise errors.AnsibleFilterError('results list is empty or not a list')


def get_sg_id_result(result_list):
    if isinstance(result_list, list) and len(result_list) > 0:
        for result in result_list:
            if result.get('group_id'):
                return result.get('group_id')
    else:
        raise errors.AnsibleFilterError('results list is empty or not a list')


def get_launch_configs(launch_configs, stack_name):
    import json
    configs = []
    launch_configs = json.loads(launch_configs)

    if 'LaunchConfigurations' in launch_configs:
        for launch_config in launch_configs['LaunchConfigurations']:
            if stack_name in launch_config['LaunchConfigurationName']:
                configs.append(launch_config['LaunchConfigurationName'])

    return configs


class FilterModule(object):
    def filters(self):
        filter_list = {
            'make_rules': make_rules,
            'rules_from_dict': rules_from_dict,
            'get_sg_result': get_sg_result,
            'get_sg_id_result': get_sg_id_result,
            'get_zone_id': get_zone_id,
            'get_launch_configs': get_launch_configs
        }
        return filter_list
