from ansible import errors


def dict_to_list(dict_to_convert):
    if isinstance(dict_to_convert, dict):
        return [{k: v} for k, v in dict_to_convert.items()]
    else:
        raise errors.AnsibleFilterError('Supplied argument must be of type dict')


class FilterModule(object):

    def filters(self):
        filter_list = {
            'dict_to_list': dict_to_list,
        }
        return filter_list
