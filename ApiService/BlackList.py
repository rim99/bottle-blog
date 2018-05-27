#! /bin/env/python3

from Cache import TimedItem

TIME_OUT = 1 # one second
MAX_REQUEST_PER_PERIOD = 5
_req_frequency_record = dict()

def canRequest(ip_address):
    if ip_address in _black_list:
        return False
    counterIncrement(_req_frequency_record, MAX_REQUEST_PER_PERIOD, ip_address)
    return True


_black_list = set()
def counterIncrement(record, limit, ip_address):
    count = None
    if ip_address in record.keys():
        countBox = record[ip_address]
        count = countBox.get()
        if count is not None:
            count += 1
            if count < limit:
                countBox.update(count)
            else:
                # when request too much frequest,
                # the ip will put into black list
                _black_list.add(ip_address)
                try:
                    del record[ip_address]
                except:
                    pass
                finally:
                    return False
    if count is None:
        record[ip_address] = TimedItem(0, TIME_OUT)
