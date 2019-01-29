from dateutil.parser import parse


def is_blank(val):
    return val == ""


def is_datetime(val):
    try:
        parse(val)
        return True
    except ValueError:
        return False
