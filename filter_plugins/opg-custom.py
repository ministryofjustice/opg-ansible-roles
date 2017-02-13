from ansible import errors


def dict_to_list(dict_to_convert):
    if isinstance(dict_to_convert, dict):
        return [{k: v} for k, v in dict_to_convert.items()]
    else:
        raise errors.AnsibleFilterError('Supplied argument must be of type dict')


def generate_identifier(stackname, slice_length=10):
    """
    :param stackname:
    :param cutoff_length:
    :param slice_length:
    :return:
    """
    import hashlib

    stackname = hashlib.sha1(stackname).hexdigest()
    stackname = stackname[0:slice_length]

    return stackname


def unique_instance_stacks(instance_list, target):
    stack_names = []

    if 'instances' in instance_list:
        for instance in instance_list['instances']:
            if 'tags' in instance:
                if 'Stack' in instance['tags']:
                    if target != instance['tags']['Stack']:
                        stack_names.append(instance['tags']['Stack'])

    return list(set(stack_names))


def split_part(string, index, separator='-'):
    return string.split(separator)[index]


def make_efs_targets(source_list, extra_item):
    """
    create list suitable for use with EFS module target argument
    :param source_list:
    :param extra_item:
    :return:
    """
    if not isinstance(source_list, list):
        raise errors.AnsibleFilterError('First argument must be of type list')
    if not isinstance(extra_item, basestring):
        raise errors.AnsibleFilterError('Second argument must be of type string')
    if len(source_list) < 1 or len(extra_item) < 1:
        raise errors.AnsibleFilterError('Values passed cannot be zero length')
    new_list = []
    for list_item in source_list:
        new_list.append({'subnet_id': list_item, 'security_groups': [ extra_item ]})
    return new_list


class FilterModule(object):

    def filters(self):
        filter_list = {
            'dict_to_list': dict_to_list,
            'generate_identifier': generate_identifier,
            'unique_instance_stacks': unique_instance_stacks,
            'split_part': split_part,
            'make_efs_targets': make_efs_targets
        }
        return filter_list
