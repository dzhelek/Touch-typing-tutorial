import os
from basics import clear_screen
from termcolor import colored
from help_library import get_character
import textwrap
import time


def welcome():
    clear_screen()
    print(colored('----- Speed Test -----'.center(os.get_terminal_size().columns), 'blue'))
    print('\n\n')


def print_screen(text):
    welcome()
    # for line in textwrap.wrap(text):
    #     print(line.center(os.get_terminal_size().columns))
    print(text.center(os.get_terminal_size().columns))
    print('\n\n')


# text = '''Most of what I learnt at Cambridge had to be painfully unlearnt later; on the whole, what I had learnt for myself from being left alone in an old library had proved more solid.'''
text = 'Is your housekeeper acting suspicious? Try asking the girl a few key questions, such as "don\'t you think those Vox Populi folk have a valid complaint against the Prophet?" And "I\'m sure some of your friends have attended meetings... I\'d sure like to see what they\'re all about!" Now, back to the music...'

def process_speed_test(speed_test_text):
    start = time.time()
    print_screen(speed_test_text)
    current_position = 0
    is_speed_test_finished = False
    all_pressed = []
    text_for_print = speed_test_text
    while not is_speed_test_finished:
        pressed = str(get_character())[2]
        if pressed == speed_test_text[current_position]:
            current_position += 1

            if pressed == ' ':
                speed_test_text = speed_test_text[:current_position - 1] + '_' + speed_test_text[current_position:]
            text_for_print = colored(speed_test_text[:current_position], 'green') + speed_test_text[current_position:]

            if current_position == len(speed_test_text):
                is_speed_test_finished = True
        print_screen(text_for_print)
        all_pressed.append(pressed)
    end = time.time()
    words_in_text = len(speed_test_text.split('_'))

    words_per_minute = int(round(words_in_text / (end - start) * 60))
    clear_screen()
    print(colored('Speed Test completed in ' + "%.2f" % (end - start) +'s', 'blue').center(os.get_terminal_size().columns))
    print(colored(f'{words_per_minute}wpm', 'blue').center(os.get_terminal_size().columns))
    print(words_in_text)


if __name__ == '__main__':
    process_speed_test(text)
