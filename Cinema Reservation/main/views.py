from getpass import getpass
import subprocess

from .models import User
from views_constants import *
from .utils import validate_email, validate_password, clear_screen, system_input

from tabulate import tabulate
from termcolor import colored

from .constants import (LEFT_HAND, KEYBOARD, RIGHT_HAND, ALL_TUTORIALS_FINISHED_TEXT,
                        TUTORIAL_WELCOME_TEXT, SPEEDTEST_WELCOME_TEXT)
import os
import time
from .help_library import get_character


def welcome(welcome_text):
    clear_screen()
    print(colored(welcome_text.center(os.get_terminal_size().columns), 'blue'))
    print('\n\n')


def print_hands_with_console():
    strings = [LEFT_HAND, KEYBOARD, RIGHT_HAND]
    print(*['    '.join(x).center(os.get_terminal_size().columns) for x in zip(*[[x.ljust(len(max(s.split('\n'), key=len))) for x in s.split('\n')] for s in strings])], sep='\n')


def print_screen(text, title):
    welcome(title)
    print(text.center(os.get_terminal_size().columns))
    print('\n\n')
    print_hands_with_console()


class UserViews:
    def console_read_command_view(self):
        command = input('> ')
        return command

#     def guest_user_help_view(self):
#         print('\nlist of commands:\n')
#         print(colored('exit\nhelp\n', COLOR_IN_EXIT))
#         print(colored('''login
# signup''', COMMAND_COLOR))

    def error_view(self, error):
        print(error)

    def welcome_user(self, user):
        print(f'Hello, {user.username}')

    def logged_user_help_view(self):
        print('\nlist of commands:\n')
        print(colored('exit\nhelp\n', COLOR_IN_EXIT))
        print(colored('''make reservation
show movie projections <movie_id> [<date>]
show movies''', COMMAND_COLOR))

    def validation_input(self, validator, message, secret=False):
        while True:
            try:
                result = system_input(message, secret)
                validator(result)
            except ValueError as err:
                self.error_view(err)
            else:
                return result

    def login(self):
        print('----- LOG IN -----')
        username = system_input('Username')
        password = system_input('Password', secret=True)
        return username, password

    def signup(self):
        print('----- SIGN UP -----')
        username = system_input('Username')
        email = self.validation_input(validate_email, 'Email')
        password = self.validation_input(validate_password,
                                         'Password', secret=True)

        def validate_equal(confirm):
            if confirm != password:
                raise ValueError('password is not the same')

        self.validation_input(validate_equal, 'Confirm password', secret=True)

        return username, email, password

    def exit(self, username='guest'):
        print(colored(f'Goodbye, {username}!', COLOR_IN_EXIT, attrs=['bold']))


class TutorialViews:
    def process_tutorial(self, tutorial_text):
        start = time.time()
        print_screen(tutorial_text, title=TUTORIAL_WELCOME_TEXT)
        current_position = 0
        is_tutorial_finished = False
        all_pressed = []
        text_for_print = tutorial_text
        while not is_tutorial_finished:
            pressed = str(get_character())[2]
            pressed = pressed.lower()
            if pressed == tutorial_text[current_position]:
                current_position += 1

                if pressed == ' ':
                    tutorial_text = tutorial_text[:current_position - 1] + '_' + tutorial_text[current_position:]
                text_for_print = colored(tutorial_text[:current_position], 'green') + tutorial_text[current_position:]

                if current_position == len(tutorial_text):
                    is_tutorial_finished = True
            print_screen(text_for_print)
            all_pressed.append(pressed)
        end = time.time()
        return end - start

    def result_from_tutorial(self, time_for_completion, words_per_minute):
        clear_screen()
        print(colored('Tutorial completed in ' + "%.2f" % time_for_completion +'s', 'blue').center(os.get_terminal_size().columns))
        print(colored(f'{words_per_minute}wpm', 'blue').center(os.get_terminal_size().columns))
        time.sleep(2)

    def finished_all_tutorials(self):
        print_screen(ALL_TUTORIALS_FINISHED_TEXT)


class SpeedTestViews:
    def process_speedtest(self, speedtest_text):
        start = time.time()
        print_screen(speedtest_text, SPEEDTEST_WELCOME_TEXT)
        current_position = 0
        is_speed_test_finished = False
        all_pressed = []
        text_for_print = speedtest_text
        while not is_speed_test_finished:
            pressed = str(get_character())[2]
            if pressed == speedtest_text[current_position]:
                current_position += 1

                if pressed == ' ':
                    speedtest_text = speedtest_text[:current_position - 1] + '_' + speedtest_text[current_position:]
                text_for_print = colored(speedtest_text[:current_position], 'green') + speedtest_text[current_position:]

                if current_position == len(speedtest_text):
                    is_speed_test_finished = True
            print_screen(text_for_print, SPEEDTEST_WELCOME_TEXT)
            all_pressed.append(pressed)
        end = time.time()
        return end - start

    def result_from_speedtest(self, time_for_completion, words_per_minute):
        clear_screen()
        print(colored('Speed Test completed in ' + "%.2f" % time_for_completion +'s', 'blue').center(os.get_terminal_size().columns))
        print(colored(f'{words_per_minute}wpm', 'blue').center(os.get_terminal_size().columns))
        time.sleep(2)
        # words_in_text = len(speed_test_text.split('_'))

        # words_per_minute = int(round(words_in_text / (end - start) * 60))
        # clear_screen()
        # print(colored('Speed Test completed in ' + "%.2f" % (end - start) +'s', 'blue').center(os.get_terminal_size().columns))
        # print(colored(f'{words_per_minute}wpm', 'blue').center(os.get_terminal_size().columns))
        # print(words_in_text)