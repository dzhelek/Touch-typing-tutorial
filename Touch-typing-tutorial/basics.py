import urwid
import subprocess
from getpass import getpass
from termcolor import colored
from help_library import get_character
import os
import time

RIGHT_HAND = '''

   _.-._
  | | | |_
  | | | | |
  | | | | |
_ |  '-._ |
\`\`-.'-._;
 \    '   |
  \  .`  /
   |    |
   |    |
'''

LEFT_HAND = '''

    _.-._
  _| | | |
 | | | | |
 | | | | |
 | _.-'  | _
 ;_.-'.-`/`/
 |   '    /
 \  `.  /
  |    |
  |    |
'''

KEYBOARD = '''
,---,---,---,---,---,---,---,---,---,---,---,---,---,-------,
|1/2| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | + | ' | <-    |
|---'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-----|
| ->| | Q | W | E | R | T | Y | U | I | O | P | ] | ^ |     |
|-----',--',--',--',--',--',--',--',--',--',--',--',--'|    |
| Caps | A | S | D | F | G | H | J | K | L | \ | [ | * |    |
|----,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'-,-'---'----|
|    | < | Z | X | C | V | B | N | M | , | . | - |          |
|----'-,-',--'--,'---'---'---'---'---'---'-,-'---',--,------|
| ctrl |  | alt |                          |altgr |  | ctrl |
'------'  '-----'--------------------------'------'  '------'
'''

mapper = {'a': ((1, 1), 0)}

text = 'aaaa'


def clear_screen():
    subprocess.call('clear')


def system_input(text, secret=False):
    if secret:
        inputing = getpass
    else:
        inputing = input
    return inputing(colored('', 'green'))


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def welcome():
    clear_screen()
    print(colored('----- Tutorial -----'.center(os.get_terminal_size().columns), 'blue'))
    print('\n\n')


def print_hands_with_console(left_hand=LEFT_HAND, keyboard=KEYBOARD, right_hand=RIGHT_HAND):
    strings=[left_hand, keyboard, right_hand]
    print(*['    '.join(x).center(os.get_terminal_size().columns) for x in zip(*[[x.ljust(len(max(s.split('\n'), key=len))) for x in s.split('\n')] for s in strings])], sep='\n')


def print_screen(text):
    welcome()
    print(text.center(os.get_terminal_size().columns))
    print('\n\n')
    print_hands_with_console()


def process_tutorial(tutorial_text):
    start = time.time()
    print_screen(tutorial_text)
    current_position = 0
    is_tutorial_finished = False
    all_pressed = []
    text_for_print = tutorial_text
    while not is_tutorial_finished:
        pressed = str(get_character())[2]
        pressed = pressed.lower()
        if pressed == tutorial_text[current_position]:
            current_position += 1

            if pressed == ' ':
                tutorial_text = tutorial_text[:current_position - 1] + '_' + tutorial_text[current_position:]
            text_for_print = colored(tutorial_text[:current_position], 'green') + tutorial_text[current_position:]

            if current_position == len(tutorial_text):
                is_tutorial_finished = True
        print_screen(text_for_print)
        all_pressed.append(pressed)
    end = time.time()
    clear_screen()
    print(colored('Tutorial completed in ' + "%.2f" % (end - start) +'s', 'blue').center(os.get_terminal_size().columns))


if __name__ == '__main__':
    process_tutorial('aa aa')
    time.sleep(2)
    process_tutorial('bb bb')
    time.sleep(2)


# palette = [
#     ('banner', '', '', '', '#ffa', '#184'),
#     ('streak', '', '', '', 'g50', '#000'),
#     ('inside', '', '', '', 'g38', '#000'),
#     ('outside', '', '', '', 'g27', '#000'),
#     ('bg', '', '', '', 'g7', '#000'),]

# placeholder = urwid.SolidFill()
# loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
# loop.screen.set_terminal_properties(colors=256)
# loop.widget = urwid.AttrMap(placeholder, 'bg')
# loop.widget.original_widget = urwid.Filler(urwid.Pile([]))

# div = urwid.Divider()
# outside = urwid.AttrMap(div, 'outside')
# inside = urwid.AttrMap(div, 'inside')
# txt = urwid.Text(('banner', u" aa aa aa aa "), align='center')
# streak = urwid.AttrMap(txt, 'streak')
# pile = loop.widget.base_widget
# for item in [outside, inside, streak, inside, outside]:
#     pile.contents.append((item, pile.options()))

# loop.run()