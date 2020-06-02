import urwid
import subprocess
from getpass import getpass
from termcolor import colored
from help_library import get_character

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


if __name__ == '__main__':
    palette = [
    ('banner', '', '', '', '#ffa', '#60d'),
    ('streak', '', '', '', 'g50', '#60a'),
    ('inside', '', '', '', 'g38', '#808'),
    ('outside', '', '', '', 'g27', '#a06'),
    ('bg', '', '', '', 'g7', '#d06'),]

    clear_screen()
    print(text)
    current_position = 0
    is_tutorial_finished = False
    all_pressed = []
    while not is_tutorial_finished:
        pressed = str(get_character())[2]
        pressed = pressed.lower()
        if pressed == text[current_position]:
            current_position += 1
            clear_screen()
            if pressed == ' ':
                text = text[:current_position - 1] + '_' + text[current_position:]
            print(colored(text[0:current_position], 'green') + text[current_position:])

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