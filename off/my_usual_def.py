# coding: utf-8
import os
import re
import sys


def clear_screen():
    """ usual method to clear screen """

    os.system('cls')


def exit_script():
    """ usual method to exit """

    sys.exit()


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
    """ usual function to format string for terminal """

    return format_number(id) + ' - ' + format_string(field)


def is_category_fr(category):
    """ usual function to reject non fr languages """

    return all((not category.startswith(lg) for lg in ("en:", "es:", "pl:")))


def format_category(category):
    """ usual function to remove fr from categories known as fr """
    return category.replace('fr:', '')
