import urwid


class Menu:
    def __init__(self, title, choices):
        self.choices = choices
        self.title = title
        self.main = urwid.Padding(self.menu(), left=2, right=2)
        top = urwid.Overlay(self.main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                            align='center', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)
        urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

    def menu(self):
        body = [urwid.Text(self.title), urwid.Divider()]
        for c in self.choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def item_chosen(self, button, choice):
        self.command = choice

        raise urwid.ExitMainLoop()


class Confirm:
    def __init__(self, title):
        self.title = title
        self.main = urwid.Padding(self.confirm(), left=2, right=2)
        top = urwid.Overlay(self.main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                            align='center', width=('relative', 60),
                            valign='middle', height=('relative', 60),
                            min_width=20, min_height=9)
        urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

    def confirm(self):
        response = urwid.Text(self.title)
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        return urwid.Filler(
            urwid.Pile(
                [response, urwid.AttrMap(done, None, focus_map='reversed')]
            )
        )

    def exit_program(self, button):
        raise urwid.ExitMainLoop()
