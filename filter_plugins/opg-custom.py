from ansible import errors


def dict_to_list(dict_to_convert):
    if isinstance(dict_to_convert, dict):
        return [{k: v} for k, v in dict_to_convert.items()]
    else:
        raise errors.AnsibleFilterError('Supplied argument must be of type dict')


def generate_identifier(stackname, slice_length=10):
    '''
    :param stackname:
    :param cutoff_length:
    :param slice_length:
    :return:
    '''
    import hashlib

    stackname = hashlib.sha1(stackname).hexdigest()
    stackname = stackname[0:slice_length]

    return stackname


class FilterModule(object):

    def filters(self):
        filter_list = {
            'dict_to_list': dict_to_list,
            'generate_identifier': generate_identifier
        }
        return filter_list
