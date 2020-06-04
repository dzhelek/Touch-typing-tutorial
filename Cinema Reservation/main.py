import os
from setup_database import setup_database
from main.views import clear_screen
from main.view_controller_manager import ViewControllerManager


def welcome():
    print('----- WELCOME to our cinema reservation system! -----'.center(os.get_terminal_size().columns))


def start():
    clear_screen()
    welcome()
    manager = ViewControllerManager()
    try:
        user = manager.user_controllers.select_user_by_username('admin', 'fe77a201d3092f0c54c4ce60762957401358a4027b32365b0479dd591dcef9f3c87762977df1eb8d23074c9509c9e5a19bb2bf218819b73be9d0352a55560068')
        manager.start_speedtest(user)
        # manager.start_tutorial(user)
        # user = manager.manage_entering_system_views_and_controllers()
        # manager.manage_user_commands_views_and_controllers(user)
    except SystemExit:
        manager.release_resources()


if __name__ == '__main__':
    try:
        setup_database()
    except Exception:
        pass
    start()
