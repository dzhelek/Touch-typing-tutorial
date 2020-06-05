from getpass import getpass
import subprocess

from .models import User
from views_constants import *
from .utils import validate_email, validate_password, clear_screen, system_input

from tabulate import tabulate
from termcolor import colored

from .constants import (LEFT_HAND, KEYBOARD, RIGHT_HAND, ALL_TUTORIALS_FINISHED_TEXT,
                        TUTORIAL_WELCOME_TEXT, SPEEDTEST_WELCOME_TEXT, ESCAPE_KEY_CODE)
import os
import time
from .help_library import get_character
from pynput import keyboard


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

    def show_best_ten_speedtests(self, speedtests):
        clear_screen()
        print(colored('BEST SCORES\n', 'blue').center(os.get_terminal_size().columns))
        print('wps ----- completed on               '.center(os.get_terminal_size().columns))
        speedtests_count = 0
        for speedtest in speedtests:
            print(colored((str(speedtest.words_per_minute) + ' ----- ' + str(speedtest.when)[:19]), 'green').\
                                            center(os.get_terminal_size().columns))
            speedtests_count += 1

        if speedtests_count == 0:
            print(colored('You have not completed any speed tests', 'green').center(os.get_terminal_size().columns))
        pressed = str(get_character())[2]
        if pressed:
            raise SystemExit


class TutorialViews:
    # def on_press(key):
    #     print('{0} pressed'.format(
    #         key))

    # def on_release(key):
    #     print('{0} release'.format(
    #         key))
    #     if key == Key.esc:
    #         # Stop listener
    #         return False

    # # Collect events until released
    # with keyboard.Listener(
    #         on_press=on_press,
    #         on_release=on_release) as listener:

    def process_tutorial(self, tutorial_text):
        start = time.time()
        print_screen(tutorial_text, title=TUTORIAL_WELCOME_TEXT)
        current_position = 0
        is_tutorial_finished = False
        all_pressed = []
        text_for_print = tutorial_text
        while not is_tutorial_finished:
            pressed = get_character()
            # if pressed == b'x\\1b':
            #     print(pressed)
            #     time.sleep(2)
            pressed = str(pressed)[2]

            
            if pressed == '\\':
                raise SystemExit
            if pressed == tutorial_text[current_position]:
                current_position += 1

                if pressed == ' ':
                    tutorial_text = tutorial_text[:current_position - 1] + '_' + tutorial_text[current_position:]
                text_for_print = colored(tutorial_text[:current_position], 'green') + tutorial_text[current_position:]

                if current_position == len(tutorial_text):
                    is_tutorial_finished = True
            print_screen(text_for_print, title=TUTORIAL_WELCOME_TEXT)
            all_pressed.append(pressed)
        end = time.time()
        return end - start

    def result_from_tutorial(self, time_for_completion, words_per_minute):
        clear_screen()
        print(colored('Tutorial completed in ' + "%.2f" % time_for_completion +'s', 'blue').center(os.get_terminal_size().columns))
        print(colored(f'{words_per_minute}wpm', 'blue').center(os.get_terminal_size().columns))
        time.sleep(2)

    def finished_all_tutorials(self):
        print_screen(ALL_TUTORIALS_FINISHED_TEXT, title=TUTORIAL_WELCOME_TEXT)
        time.sleep(2)


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
            if pressed == '\\':
                raise SystemExit
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
