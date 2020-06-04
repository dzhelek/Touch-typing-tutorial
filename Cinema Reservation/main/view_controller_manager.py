from .controllers import UserController, TextController, TutorialController, SpeedTestController
from .models import User
from .views import (UserViews, TutorialViews, SpeedTestViews, system_input)
from .urwid_views import Menu
from views_constants import PROJECTION_SEATS
from sqlalchemy.exc import IntegrityError
import re
from datetime import datetime
from .utils import calculate_words_per_minute


class ViewControllerManager:
    def __init__(self):
        self.user_views = UserViews()
        self.user_controllers = UserController()
        self.text_controllers = TextController()
        self.tutorial_views = TutorialViews()
        self.tutorial_controllers = TutorialController()
        self.speedtest_views = SpeedTestViews()
        self.speedtest_controllers = SpeedTestController()

    def manage_entering_system_views_and_controllers(self):
        user_entered_system = None
        menu = Menu('welcome', ['login', 'signup', 'exit'])
        command = menu.command
        if command == 'login':
            user_entered_system = self.manage_login_view_and_controller()
        elif command == 'signup':
            user_entered_system = self.manage_signup_view_and_controller()
        elif command == 'exit':
            raise SystemExit
        else:
            raise ValueError

        return user_entered_system

    def manage_login_view_and_controller(self):
        login_data = self.user_views.login()
        username_entered = login_data[0]
        password_entered = login_data[1]
        try:
            return self.user_controllers.log_user(username_entered, password_entered)
        except ValueError as err:
            self.user_views.error_view(str(err))

    def start_tutorial(self, user):
        # while not is_correct_data_entered:
        #     data_entered = system_input(input_message)
        #     if data_entered == 'cancel':
        #         raise SystemExit
        #     try:
        #         data_for_reservation += int(data_entered)
        #         is_correct_data_entered = True
        #     except Exception as e:
        #         print(error_message)
        # return data_for_reservation
        tutorials_count = self.tutorial_controllers.get_tutorials_count()
        is_playing_finished = False
        while not is_playing_finished:
            tutorial = self.tutorial_controllers.get_tutorial_for_user(user.next_tutorial_order_id)
            time_for_completion = self.tutorial_views.process_tutorial(tutorial.content)
            words_per_minute = calculate_words_per_minute(tutorial.words, time_for_completion)

            self.tutorial_views.result_from_tutorial(time_for_completion, words_per_minute)
            if tutorial.order_id < tutorials_count:
                self.user_controllers.increment_user_next_tutorial_order_id(user)
            else:
                self.user_controllers.set_one_as_user_next_tutorial_order_id(user)
                is_playing_finished = True
        self.tutorial_views.finished_all_tutorials()

    def start_speedtest(self, user):
        is_playing_finished = False
        count = 0 #TODO remove this count
        previous_text_id = None
        while not is_playing_finished:
            text = self.text_controllers.get_random_text(previous_text_id)
            # TODO:
            # call start_speedtest view instead of print()
            time_for_completion = self.speedtest_views.process_speedtest(text.content)
            words_per_minute = calculate_words_per_minute(text.words, time_for_completion)
            self.speedtest_views.result_from_speedtest(time_for_completion, words_per_minute)

            if count > 4: #TODO check if process is canceled by user
                is_playing_finished = True
            else:
                previous_text_id = text.id
                count += 1
            self.speedtest_controllers.add_speedtest(user.id, text.id, text.words / 10 * 60, datetime.now())

    def get_speedtests_with_best_score(self, user_id, count):
        return self.speedtest_controllers.get_speedtests_with_best_score_for_user(user_id, count)

    def read_input_for_reservation(self, input_message, error_message):
        is_correct_data_entered = False
        data_for_reservation = 0
        while not is_correct_data_entered:
            data_entered = system_input(input_message)
            if data_entered == 'cancel':
                raise SystemExit
            try:
                data_for_reservation += int(data_entered)
                is_correct_data_entered = True
            except Exception as e:
                print(error_message)
        return data_for_reservation

    def manage_user_commands_views_and_controllers(self, user):
        self.user_views.welcome_user(user)
        while True:
            command = self.user_views.console_read_command_view()
            if command == 'help':
                self.user_views.logged_user_help_view()
            elif command == 'show movies':
                self.show_movies()
            elif command.startswith('show movie projections'):
                entered_data =\
                    command.replace('show movie projections', '').split()
                if len(entered_data) == 2:
                    date = entered_data[1]
                else:
                    date = ''
                if len(entered_data) == 0:
                    print('please specifie movie_id (and date)')
                else:
                    movie = entered_data[0]
                    try:
                        self.show_movie_projections(movie, date)
                    except Exception as e:
                        print(str(e))
                        raise
            elif command == 'make reservation':
                try:
                    self.reservation_views.index()
                    seats = self.read_input_for_reservation('number of seats', 'Seats need to be number in range 1-10')
                    # print(f'Seats: {seats}')
                    self.show_movies()
                    movie_id = self.read_input_for_reservation('movie id', 'Movie id needs to be a number')
                    # print(f'Movie id: {movie}')
                    self.show_movie_projections(movie_id)
                    projection_id = self.read_input_for_reservation('projection id', 'Projection id needs to be a number')
                    projection_used_seats = self.reservation_controllers.count_used_seats(projection_id)
                    if PROJECTION_SEATS - projection_used_seats[0] >= seats:
                        print(f'You can reserve {seats} seats')
                    else:
                        print(f'There aren`t {seats} available seats')
                except SystemExit:
                    print('\nProcess canceled!')

            elif command == 'exit':
                raise SystemExit
            else:
                print(f'\'{command}\' command not found')

    def manage_signup_view_and_controller(self):
        signup_data = self.user_views.signup()
        if isinstance(signup_data, ValueError):
            self.user_views.error_view(signup_data)
        else:
            username_entered = signup_data[0]
            email_entered = signup_data[1]
            password_entered = signup_data[2]
            try:
                self.user_controllers.sign_user(username_entered, email_entered, password_entered)
                user = self.user_controllers.select_user_by_username(username_entered, password_entered)
                return user
            except ValueError as err:
                self.user_views.error_view(err)
            except IntegrityError as e:
                not_unique_constaint = re.search(': [a-z]+.[a-z]+', str(e)).group(0)
                error_message_fields = not_unique_constaint.split('.')
                message_to_print = f'User with this {error_message_fields[1]} already exists!'
                self.user_views.error_view(message_to_print)
                self.user_controllers.gateway.db.session.rollback()

    def release_resources(self):
        self.user_controllers.gateway.db.close()
        self.text_controllers.gateway.db.close()
        self.tutorial_controllers.gateway.db.close()
        self.speedtest_controllers.gateway.db.close()
