from datetime import datetime, time
from email.utils import parseaddr
from hashlib import sha512
from random import randint
from re import compile, match

from settings import HASHING_TIMES
import subprocess
from getpass import getpass
from termcolor import colored
from .constants import QWERTY, MAPPER


def get_hashed_pass_and_salt(password):
    salt = ''.join(chr(randint(32, 126)) for i in range(16))
    password += salt
    for i in range(HASHING_TIMES):
        password = sha512(password.encode()).hexdigest()

    return password, salt


def get_hash(password, salt):
    password += salt
    for i in range(HASHING_TIMES):
        password = sha512(password.encode()).hexdigest()

    return password


def validate_email(email):
    if '@' not in parseaddr(email)[1]:
        raise ValueError('invalid email address')


def validate_password(password):
    if len(password) > 7:
        has_capital_letter = compile('[A-Z]')
        has_special_symbol = compile(r'[\W\S\D]')

        if not match(has_capital_letter, password):
            raise ValueError('password must contain a capital letter')

        if not match(has_special_symbol, password):
            raise ValueError('password must contain a special symbol')
    else:
        raise ValueError('password must be min 8 characters long')


def get_datetime_object(date):
    y, m, d = date.split('-')
    return datetime(int(y), int(m), int(d))


def get_time_object(str_time):
    h, m = str_time.split(':')
    return time(int(h), int(m))


def clear_screen():
    subprocess.call('clear')


def system_input(text, secret=False):
    if secret:
        inputing = getpass
    else:
        inputing = input
    return inputing(colored(f'{text}: ', 'green'))


def calculate_words_per_minute(words, time, sep='_'):
    return int(round(words / time * 60))


def calculate_position_of_finger_in_board_by_symbol(symbol):
    symbol = symbol.upper()
    for row in QWERTY:
        if row.__contains__(symbol):
            return MAPPER[row.index(symbol) - 1]
