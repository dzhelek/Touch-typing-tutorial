import urwid
import subprocess
from getpass import getpass
from termcolor import colored
from help_library import get_character
import os


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
'''


mapper = {'a': ((1, 1), 0)}

text = 'aa aa aa'


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
    print('\n\n\n')


def print_hands(left_hand=LEFT_HAND, right_hand=RIGHT_HAND):
    strings=[left_hand, right_hand]
    print(*['                                        '.join(x).center(os.get_terminal_size().columns) for x in zip(*[[x.ljust(len(max(s.split('\n'), key=len))) for x in s.split('\n')] for s in strings])], sep='\n')


def print_screen(text):
    welcome()
    print(text.center(os.get_terminal_size().columns))
    print('\n\n\n')
    print_hands()

if __name__ == '__main__':
    print_screen(text)
    cols = os.get_terminal_size().columns
    current_position = 0
    is_tutorial_finished = False
    all_pressed = []
    while not is_tutorial_finished:
        pressed = str(get_character())[2]
        pressed = pressed.lower()
        if pressed == text[current_position]:
            current_position += 1
            
            if pressed == ' ':
                text = text[:current_position - 1] + '_' + text[current_position:]
            text_for_print = ((colored(text[0:current_position], 'green') + text[current_position:]).center(os.get_terminal_size().columns))
            print_screen(text_for_print)
            if current_position == len(text):
                is_tutorial_finished = True
        all_pressed.append(pressed)
    print(all_pressed)

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