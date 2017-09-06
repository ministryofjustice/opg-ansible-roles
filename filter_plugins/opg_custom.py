from ansible import errors


def dict_to_list(dict_to_convert):
    """
    :param dict_to_convert:
    :return:
    """
    if isinstance(dict_to_convert, dict):
        return [{k: v} for k, v in dict_to_convert.items()]
    else:
        raise errors.AnsibleFilterError('Supplied argument must be of type dict')


def list_intersect(first, second):
    """
    Returns elements found in first that are in second
    :param first:
    :param second:
    :return:
    """
    second = set(second)
    return [item for item in first if item in second]


def merge_custom_app_data(src=[{}], destination=[{}]):
    """
    :param src:
    :param destination:
    :return [{}]:
    Merges two lists
    """

    src_names = []
    dest_names = []

    for elem in src:
        if 'name' in elem:
            src_names.append(elem['name'])

    for elem in destination:
        if 'name' in elem:
            dest_names.append(elem['name'])

    intersects = list_intersect(src_names, dest_names)

    if intersects:
        raise errors.AnsibleFilterError(
            'Keys {} are duplicated in source and destination lists'.
                format(list(set(intersects)))
        )

    result = src
    result += destination
    return result


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
    """
    :param instance_list:
    :param target:
    :return:
    """
    stack_names = []

    if 'instances' in instance_list:
        for instance in instance_list['instances']:
            if 'tags' in instance:
                if 'Stack' in instance['tags']:
                    if target != instance['tags']['Stack']:
                        stack_names.append(instance['tags']['Stack'])

    return list(set(stack_names))


def split_part(string, index, separator='-'):
    """
    :param string:
    :param index:
    :param separator:
    :return:
    """
    return string.split(separator)[index]


def find_rds_instance(rds_list, db_name):
    """
    :param rds_list:
    :param db_name:
    :return:
    """
    db_info = None

    for db_instance in rds_list:
        if db_name == db_instance['db_name']:
            db_info = db_instance

    return db_info


def merge_config_dictionaries(*dicts):
    """
    Merges n dictionaries of configuration data
    :param list<dicts>:
    :return dict:
    """
    res_dict = {}

    if isinstance(dicts, list):
        if len(dicts) == 1 and isinstance(dicts[0], dict):
            return dicts[0]
        else:
            for dictionary in dicts:
                if isinstance(dictionary, dict):
                    res_dict.update(dictionary)

    return res_dict

class FilterModule(object):

    def filters(self):
        filter_list = {
            'dict_to_list': dict_to_list,
            'generate_identifier': generate_identifier,
            'unique_instance_stacks': unique_instance_stacks,
            'split_part': split_part,
            'merge_custom_app_data': merge_custom_app_data,
            'find_rds_instance': find_rds_instance,
            'merge_config_dictionaries': merge_config_dictionaries
        }
        return filter_list
