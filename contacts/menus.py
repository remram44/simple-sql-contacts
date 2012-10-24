import math
from sys import stderr, stdin, stdout


class Option(object):
    def __init__(self, caption, callback=None, value=None):
        self.caption = caption
        if callback and value:
            raise ValueError("Menu#__init__() expects callback or value "
                             "parameters, not both")
        elif callback:
            self._callback = callback
        elif value:
            self._callback = lambda: value

    def __call__(self):
        return self._callback()

    def __str__(self):
        return self.caption


class Menu(object):
    def __init__(self, options, title=None):
        self.title = title
        self._options = options

    def select(self):
        while True:
            stdout.write("\n")
            if self.title:
                stdout.write(self.title)
                stdout.write("\n\n")
            width = int(math.log10(len(self._options)))
            for n, opt in enumerate(self._options, 1):
                stdout.write("%*d) %s\n" % (width, n, opt))
            stdout.write("\nYour choice: ")
            stdout.flush()
            rep = stdin.readline()
            try:
                rep = int(rep)
            except ValueError:
                stderr.write("\nInvalid answer (not a number)\n")
                continue
            if rep <= 0 or rep > len(self._options):
                stderr.write("\nInvalid answer (out of bounds)\n")
                continue
            return self._options[rep-1]()
