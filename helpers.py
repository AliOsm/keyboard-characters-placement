import sys
import time
import random

PX = 37.7952755906

def cm2px(cm):
    if type(cm) is float or type(cm) is int:
        return round(cm * PX)
    elif type(cm) is tuple:
        return tuple([round(item * PX) for item in cm])
    elif type(cm) is list:
        return [round(item * PX) for item in cm]

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_current_time():
    return time.asctime(time.localtime(time.time()))

def info_log(message):
    print('info: %s] %s' % (get_current_time(), message))

def warning_log(message):
    print('warning: %s] %s' % (get_current_time(), message))

def error_log(message, is_exit):
    print('error: %s] %s' % (get_current_time(), message), file=sys.stderr)
    if is_exit:
        sys.exit(1)
