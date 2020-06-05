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
    tutorial_controller = TutorialController()
    tutorial_controller.add_tutorial('aa ss dd ff jj kk ll ;;')
    tutorial_controller.add_tutorial('as as df df jk jk l; l;')
    tutorial_controller.add_tutorial('asdf asdf jkl; jkl;')
    tutorial_controller.add_tutorial('fdsa fdsa ;lkj ;lkj')
    tutorial_controller.add_tutorial('jkl; jkl; asdf asdf')
    tutorial_controller.add_tutorial(';lkj ;lkj fdsa fdsa')
    tutorial_controller.add_tutorial('ee ii ee ii')
    tutorial_controller.add_tutorial('ei ei ie ie')
    tutorial_controller.add_tutorial('fefe fefe efef efef')


if __name__ == '__main__':
    setup_database()
