
import datetime

from ansible.errors import AnsibleFilterError

def seconds_to_timestamp(a):
    try:
        return str(datetime.timedelta(seconds=int(a)))
    except:
        raise AnsibleFilterError("Input must be an integer, provider '{}'".format(a))

def create_ia_exclude_options(a):
    exclude_string = ""
    if isinstance(a, list):
        for exclude in a:
            exclude_string = exclude_string + "-e '{}'".format(exclude)
    return exclude_string

class FilterModule(object):
    def filters(self):
        return {
            'seconds_to_timestamp': seconds_to_timestamp,
            'create_ia_exclude_options': create_ia_exclude_options
        }