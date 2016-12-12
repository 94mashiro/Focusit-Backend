import time
import datetime

def stringToDateTime(str):
    timestamp = time.mktime(time.strptime(str, '%Y-%m-%dT%H:%M:%S'))
    return datetime.datetime.utcfromtimestamp(timestamp)
