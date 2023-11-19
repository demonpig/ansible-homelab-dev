
import datetime

from ansible.errors import AnsibleFilterError

def seconds_to_timestamp(a):
    try:
        return str(datetime.timedelta(seconds=int(a)))
    except:
        raise AnsibleFilterError("Input must be an integer, provider '{}'".format(a))

class FilterModule(object):
    def filters(self):
        return {
            'seconds_to_timestamp': seconds_to_timestamp
        }