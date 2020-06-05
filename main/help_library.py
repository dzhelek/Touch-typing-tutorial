import contextlib
import os
import sys
import termios
import tty


_MAX_CHARACTER_BYTE_LENGTH = 4


@contextlib.contextmanager
def _tty_reset(file_descriptor):
    """
    A context manager that saves the tty flags of a file descriptor upon
    entering and restores them upon exiting.
    """
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        yield
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)


def get_character(file=sys.stdin):
    """
    Read a single character from the given input stream (defaults to sys.stdin).
    """
    file_descriptor = file.fileno()
    with _tty_reset(file_descriptor):
        tty.setcbreak(file_descriptor)
        return os.read(file_descriptor, _MAX_CHARACTER_BYTE_LENGTH)
