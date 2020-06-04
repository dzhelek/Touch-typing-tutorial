from .models import User, Text, Tutorial
from .database import Database
from .utils import get_datetime_object, get_time_object
from sqlalchemy import func


class UserGateway:
    def __init__(self):
        self.db = Database()

    def search_user_by_name(self, username):
        user = self.db.session.query(User).\
            filter(User.username == username).first()
        self.db.commit()
        return user

    def update_table_with_user_data(self, username, email,
                                    password, salt, superuser):
        self.db.add(User(username=username, email=email, password=password,
                         salt=salt, superuser=True))


class TextGateway:
    def __init__(self):
        self.db = Database()

    def select_text_by_id(self, id):
        text = self.db.session.query(Text).\
            filter(Text.id == id).first()
        self.db.commit()
        return text

    def select_all_texts(self):
        texts = self.db.session.query(Text).all()
        self.db.commit()
        return texts

    def update_table_with_text_data(self, content):
        self.db.add(Text(content=content))


class SpeedTestGateway:
    def __init__(self):
        self.db = Database()


class TutorialGateway:
    def __init__(self):
        self.db = Database()

    def select_tutorials_count(self):
        return self.db.session.query(Tutorial.order_id).count()

    def update_table_with_tutorial_data(self, order_id, content):
        self.db.add(Tutorial(order_id=order_id, content=content))


# class MovieGateway:
#     def __init__(self):
#         self.db = Database()

#     def select_all_movies(self):
#         movies = self.db.session.query(Movie).\
#             order_by(Movie.rating.desc()).all()
#         self.db.commit()
#         return movies

#     def update_table_with_movie_data(self, name, rating):
#         self.db.add(Movie(name=name, rating=rating))


# class ProjectionGateway:
#     def __init__(self):
#         self.db = Database()

#     def select_projections_for_given_movie_and_date(self, movie, date):
#         projections = []
#         # print(movie)
#         if date == '':
#             projections = self.db.session.query(Projection).\
#                 filter(Projection.movie_id == movie).\
#                 order_by(Projection.date).order_by(Projection.time).all()
#         else:
#             projections = self.db.session.query(Projection).\
#                 filter(Projection.movie_id == movie, Projection.date == date).\
#                 order_by(Projection.time).all()

#         self.db.commit()
#         return projections

#     def update_table_with_projection_data(self, movie, p_type, date, time):
#         date = get_datetime_object(date)
#         time = get_time_object(time)
#         self.db.add(Projection(movie_id=movie, type=p_type,
#                                date=date, time=time))


# class ReservationGateway:
#     def __init__(self):
#         self.db = Database()

#     def count_reservations_with_projection_id(self, projection_id):
#         return self.db.session.query(func.count(Reservation.projection_id)).\
#             filter(Reservation.projection_id == projection_id).first()
