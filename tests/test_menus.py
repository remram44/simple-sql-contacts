from contextlib import contextmanager
import unittest
import sys

from contacts import menus
from contacts.menus import Menu, Option


class StdinOverride(object):
    def __init__(self, f):
        self._f = f

    def readline(self):
        return self._f()


class StdoutOverride(object):
    def write(self, msg):
        pass

    def flush(self):
        pass


@contextmanager
def override_readline(func):
    if isinstance(func, basestring):
        s = func
        func = lambda: s
    elif isinstance(func, tuple):
        it = iter(func)
        def func():
            try:
                return next(it)
            except StopIteration:
                raise ValueError
    menus.stdin = StdinOverride(func)
    menus.stdout = menus.stderr = StdoutOverride()
    yield
    menus.stdin = sys.stdin
    menus.stdout = sys.stdout
    menus.stderr = sys.stderr


class Test_menu(unittest.TestCase):
    def test_option(self):
        self.assertRaises(ValueError,
                          lambda: Option('le caption',
                                         callback=lambda: 42,
                                         value=43))
        self.assertEqual(Option('le caption', callback=lambda: 42)(), 42)
        self.assertEqual(Option('le caption', value=42)(), 42)
        self.assertIsNone(Option('le caption')())

    def test_options(self):
        menu = Menu([
                Option('le first caption', callback=lambda: 7),
                Option('le second caption', value=18),
                Option('le third caption'),
            ])
        with override_readline('1'):
            self.assertEqual(menu.select(), 7)
        with override_readline('2'):
            self.assertEqual(menu.select(), 18)
        with override_readline('3'):
            self.assertIsNone(menu.select())

    def test_invalid(self):
        def callback():
            callback.called = True
        callback.called = False
        menu = Menu([
                Option('le caption', callback=callback),
                Option('le exit', value=42),
                Option('le other caption', callback=callback),
            ])
        with override_readline(('0', '-2', '2')):
            self.assertEqual(menu.select(), 42)
            self.assertFalse(callback.called)
        with override_readline(('6', '4', '2')):
            self.assertEqual(menu.select(), 42)
            self.assertFalse(callback.called)
