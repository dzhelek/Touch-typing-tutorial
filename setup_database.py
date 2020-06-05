from main.database import Database
from main.controllers import (UserController, TextController,
                              TutorialController)
from settings import SU_NAME, SU_PASS


def setup_database():
    db = Database()
    db.create()

    user_controller = UserController()
    user_controller.sign_user(username=SU_NAME, email=None,
                              password=SU_PASS, superuser=True)
    text_controller = TextController()

    text_controller.add_text('So I\'m two inches away from her. \
Her luscious lips part. \
Just as I\'m about to kiss her, she looks at me and she says, \
"What\'s your name?" Gogol Ganguli. End of seduction 101.')

    text_controller.add_text('Speed test text to complete')
    text_controller.add_text('Another speed test for you!')

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
