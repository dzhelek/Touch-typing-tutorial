from .models import User, Text, Tutorial, SpeedTest
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

    def update_user_next_tutorial_id(self, user_id):
        self.db.session.query().\
            filter(User.id == user_id).update({"next_tutorial_order_id": (User.next_tutorial_order_id + 1)})
        self.db.commit()

    # def select_next_tutorial_id_by_user_id(user_id):
    #     next_tutorial_id = self.db.session.query(User).filter


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

    def update_table_with_speedtest_data(self, user_id, text_id, words_per_minute, when):
        self.db.add(SpeedTest(user_id=user_id, text_id=text_id, words_per_minute=words_per_minute, when=when))

    def select_speedtests_for_user_ordered_by_words_per_minute(self, user_id, count):
        speedtests = self.db.session.query(SpeedTest).filter(SpeedTest.user_id == user_id).\
            order_by(SpeedTest.words_per_minute.desc()).\
            order_by(SpeedTest.when.desc()).limit(count)
        self.db.commit()
        return speedtests


class TutorialGateway:
    def __init__(self):
        self.db = Database()

    def select_tutorial_by_order_id(self, order_id):
        order_id = self.db.session.query(Tutorial).filter(Tutorial.order_id == order_id).first()
        self.db.commit()
        return order_id

    def select_tutorials_count(self):
        count = self.db.session.query(Tutorial.order_id).count()
        self.db.commit()
        return count

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
