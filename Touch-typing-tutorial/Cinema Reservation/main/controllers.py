from .utils import get_hash, get_hashed_pass_and_salt
from .gateway import UserGateway, MovieGateway, ProjectionGateway, ReservationGateway


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


class MovieController:
    def __init__(self):
        self.gateway = MovieGateway()

    def show_movies(self):
        return self.gateway.select_all_movies()

    def add_movie(self, name, rating):
        self.gateway.update_table_with_movie_data(name, rating)


class ProjectionController:
    def __init__(self):
        self.gateway = ProjectionGateway()

    def show_projection(self, movie, date):
        return self.gateway.select_projections_for_given_movie_and_date(movie, date)

    def add_projection(self, movie, p_type, date, time):
        self.gateway.update_table_with_projection_data(movie, p_type,
                                                       date, time)


class ReservationController:
    def __init__(self):
        self.gateway = ReservationGateway()

    def count_used_seats(self, projection_id):
        return self.gateway.count_reservations_with_projection_id(projection_id)
