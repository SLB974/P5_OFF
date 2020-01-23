# coding: utf-8
import os
import re
import sys


def clear_screen():
    """default method to clear screen."""

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def exit_script():
    """default method to exit."""

    sys.exit()


def format_number(value):
    """default function to format headline number."""

    if value < 10:
        return ' ' + str(value)
    else:
        return str(value)


def format_string(value):
    """default function to remove return inside string."""

    regex = re.compile(r'[\n]')
    return regex.sub(" ", value)


def format_for_screen(id, field):
    """default function to format string for terminal."""

    return format_number(id) + ' - ' + format_string(field)


def is_category_fr(category):
    """dafault function to reject non fr languages."""

    return all((not category.startswith(lg) for lg in ("en:", "es:", "pl:")))


def format_category(category):
    """default function to remove fr from categories known as fr."""
    return category.replace('fr:', '')
