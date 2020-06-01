from main.database import Database
from main.controllers import (UserController, MovieController,
                              ProjectionController)
from settings import SU_NAME, SU_PASS


def setup_database():
    db = Database()
    db.create()
    # db.insert()
    controller = UserController()
    controller.sign_user(username=SU_NAME, email=None,
                         password=SU_PASS, superuser=True)
    controller = MovieController()
    controller.add_movie('The Hunger Games: Catching Fire', 7.9)
    controller.add_movie('Wreck-It Ralph', 7.8)
    controller.add_movie('Her', 8.3)
    controller = ProjectionController()
    controller.add_projection(1, '3D', '2020-04-01', '19:10')
    controller.add_projection(1, '2D', '2020-04-01', '19:00')
    controller.add_projection(1, '4DX', '2020-04-02', '21:00')
    controller.add_projection(3, '2D', '2020-04-05', '20:20')
    controller.add_projection(2, '3D', '2020-04-02', '22:00')
    controller.add_projection(2, '2D', '2020-04-02', '19:30')


if __name__ == '__main__':
    setup_database()
