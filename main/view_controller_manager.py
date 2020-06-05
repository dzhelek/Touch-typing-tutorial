from .controllers import UserController, TextController, TutorialController, SpeedTestController
from .models import User
from .views import (UserViews, TutorialViews, SpeedTestViews, system_input)
from .urwid_views import Menu
from sqlalchemy.exc import IntegrityError
import re
from datetime import datetime
from .utils import calculate_words_per_minute, clear_screen
import time


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
        while True:
            login_data = self.user_views.login()
            username_entered = login_data[0]
            password_entered = login_data[1]
            try:
                return self.user_controllers.log_user(username_entered,
                                                      password_entered)
            except ValueError as err:
                self.user_views.error_view(str(err))

    def start_tutorial(self, user):
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
        previous_text_id = None
        while True:
            text = self.text_controllers.get_random_text(previous_text_id)
            time_for_completion = self.speedtest_views.process_speedtest(text.content)
            words_per_minute = calculate_words_per_minute(text.words, time_for_completion)
            self.speedtest_views.result_from_speedtest(time_for_completion, words_per_minute)
            previous_text_id = text.id
            self.speedtest_controllers.add_speedtest(user.id, text.id, words_per_minute, datetime.now())

    def get_speedtests_with_best_score(self, user_id, count):
        return self.speedtest_controllers.get_speedtests_with_best_score_for_user(user_id, count)

    def generate_user_statistics(self, user):
        best_speedtests = self.get_speedtests_with_best_score(user.id, 10)
        self.user_views.show_best_ten_speedtests(best_speedtests)
        time.sleep(2)

    def manage_user_commands_views_and_controllers(self, user):
        menu = Menu(f'welcome, {user.username}', ['tutorial', 'speedtest', 'statistics', 'exit'])
        command = menu.command
        if command == 'exit':
            clear_screen()
            raise SystemExit
        try:
            if command == 'tutorial':
                self.start_tutorial(user)
                raise SystemExit
            elif command == 'speedtest':
                self.start_speedtest(user)
            elif command == 'statistics':
                self.generate_user_statistics(user)
                raise SystemExit
            else:
                raise ValueError
        except SystemExit:
            self.manage_user_commands_views_and_controllers(user)

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
