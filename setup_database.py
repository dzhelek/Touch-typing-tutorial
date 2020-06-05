from main.database import Database
from main.controllers import (UserController, TextController, TutorialController)
from settings import SU_NAME, SU_PASS


def setup_database():
    db = Database()
    db.create()

    user_controller = UserController()
    user_controller.sign_user(username=SU_NAME, email=None, password=SU_PASS, superuser=True)
    text_controller = TextController()
    text_controller.add_text('First text added')
    text_controller.add_text('Second text added')
    text_controller.add_text('Third text added')
    text_controller.add_text('Fourth text added')
    text_controller.add_text('Fifth text added')
    text_controller.add_text('a')
    tutorial_controller = TutorialController()
    tutorial_controller.add_tutorial('jj jj')
    tutorial_controller.add_tutorial('aa')
    tutorial_controller.add_tutorial('aw aa')
    tutorial_controller.add_tutorial('aa aa aa')


if __name__ == '__main__':
    setup_database()
