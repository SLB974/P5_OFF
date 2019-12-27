# coding: utf-8
import os
import re
import sys


def clear_screen():
    """ usual method to clear screen """

    os.system('cls')


def format_number(value):
    """ usual function format headline number """

    if value < 10:
        return ' ' + str(value)
    else:
        return str(value)


def format_string(value):
    """ usual function remove return inside string """

    regex = re.compile(r'[\n]')
    return regex.sub(" ", value)


def format_for_screen(id, field):

    return format_number(id) + ' - ' + format_string(field)


def exit_script():
    """ usual method to exit """

    sys.exit()
