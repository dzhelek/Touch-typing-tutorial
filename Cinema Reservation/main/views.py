from getpass import getpass
import subprocess

from .models import User
from views_constants import *
from .utils import validate_email, validate_password

from tabulate import tabulate
from termcolor import colored


def clear_screen():
    subprocess.call('clear')


def system_input(text, secret=False):
    if secret:
        inputing = getpass
    else:
        inputing = input
    return inputing(colored(f'{text}: ', INPUT_COLOR))


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


class MovieViews:
    def show_all_view(self, movies):
        table = []
        print()
        for movie in movies:
            table.append([colored(movie.id, ID_COLOR),
                          movie.name, movie.rating])
        print(tabulate(table,
                       headers=[colored('id', ID_COLOR), 'name', 'rating']))


class ProjectionViews:
    def show_all_projections(self, projections):
        print()
        if projections == []:
            print('No projections available')
        else:
            table = []
            for projection in projections:
                table.append([colored(projection.id, ID_COLOR),
                              projection.type, projection.date,
                              projection.time])
            print(tabulate(table, headers=[colored('id', ID_COLOR),
                                           'type', 'date', 'time']))


class ReservationViews:
    def index(self):
        print('\nStart creating reservation.')
        print('On each step if you would like to quit just type cancel!')
