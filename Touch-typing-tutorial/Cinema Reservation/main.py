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
        user = manager.manage_entering_system_views_and_controllers()
        manager.manage_user_commands_views_and_controllers(user)
    except SystemExit:
        manager.release_resources()


if __name__ == '__main__':
    try:
        setup_database()
    except Exception:
        pass
    start()
