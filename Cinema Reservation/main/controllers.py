from .utils import get_hash, get_hashed_pass_and_salt
from .gateway import UserGateway, TextGateway, SpeedTestGateway, TutorialGateway
from .models import User
import random


class UserController:
    def __init__(self):
        self.gateway = UserGateway()

    def log_user(self, username, entered_password):
        user = self.gateway.search_user_by_name(username)
        if user is not None:
            if user.password == get_hash(entered_password, user.salt):
                return user
        raise ValueError('Invalid username or password')

    def sign_user(self, username, email, password, superuser=False):
        password, salt = get_hashed_pass_and_salt(password)
        self.gateway.update_table_with_user_data(username, email,
                                                 password, salt, superuser)

    def select_user_by_username(self, username, password):
        return self.gateway.search_user_by_name(username)

    def increment_user_next_tutorial_order_id(self, user):
        # self.gateway.update_user_next_tutorial_id(user_id)
        user.next_tutorial_order_id = User.next_tutorial_order_id + 1
        self.gateway.db.commit()

    def set_one_as_user_next_tutorial_order_id(self, user):
        user.next_tutorial_order_id = 1
        self.gateway.db.commit()


class TextController:
    def __init__(self):
        self.gateway = TextGateway()

    def search_text_by_id(self, id):
        return self.gateway.select_text_by_id(id)

    def get_all_texts(self):
        return self.gateway.select_all_texts()

    def add_text(self, text_content):
        self.gateway.update_table_with_text_data(text_content)

    def get_random_text(self, previous_text_id=None):
        all_texts = self.get_all_texts()
        if previous_text_id:
            previous_text = self.search_text_by_id(previous_text_id)
            all_texts.remove(previous_text)
        return random.choice(all_texts)


class SpeedTestController:
    def __init__(self):
        self.gateway = SpeedTestGateway()

    def add_speedtest(self, user_id, text_id, words_per_minute, when):
        self.gateway.update_table_with_speedtest_data(user_id, text_id, words_per_minute, when)

    def get_speedtests_with_best_score_for_user(self, user_id, count=1):
        return self.gateway.select_speedtests_for_user_ordered_by_words_per_minute(user_id, count)


class TutorialController:
    def __init__(self):
        self.gateway = TutorialGateway()

    def get_tutorials_count(self):
        return self.gateway.select_tutorials_count()

    def get_tutorial_for_user(self, tutorial_order_id):
        return self.gateway.select_tutorial_by_order_id(tutorial_order_id)

    def add_tutorial(self, tutorial_content):
        tutorials_count = self.get_tutorials_count()
        self.gateway.update_table_with_tutorial_data(tutorials_count + 1, tutorial_content)


# class MovieController:
#     def __init__(self):
#         self.gateway = MovieGateway()

#     def show_movies(self):
#         return self.gateway.select_all_movies()

#     def add_movie(self, name, rating):
#         self.gateway.update_table_with_movie_data(name, rating)


# class ProjectionController:
#     def __init__(self):
#         self.gateway = ProjectionGateway()

#     def show_projection(self, movie, date):
#         return self.gateway.select_projections_for_given_movie_and_date(movie, date)

#     def add_projection(self, movie, p_type, date, time):
#         self.gateway.update_table_with_projection_data(movie, p_type,
#                                                        date, time)


# class ReservationController:
#     def __init__(self):
#         self.gateway = ReservationGateway()

#     def count_used_seats(self, projection_id):
#         return self.gateway.count_reservations_with_projection_id(projection_id)
