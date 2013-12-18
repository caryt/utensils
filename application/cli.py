"""Command Line Application
===========================

.. inheritance-diagram:: CommandLineApp

"""
from __future__ import print_function
from classproperty import classproperty
from unittest import TestLoader, TextTestRunner
from sys import argv
from string import digits
from subprocess import call
from webbrowser import open
from os.path import abspath

def doc(obj):
    return obj.__doc__

def autodoc(obj):
    return obj.__autodoc__

def lines(*args):
    return "\n".join(args)

class CLI(object):
    """Helper class to implement a Command Line Interface."""
    _cmds = {}

    def __new__(cls, *args, **kwargs):
        cls.add(cls._cmds)
        return object.__new__(cls, *args, **kwargs)

    @classproperty
    @classmethod
    def commands(cls):
        return cls._cmds.items()

    def __str__(self):
        """Return help / usage message."""
        return lines(
            self.desc,
            ''
            'Usage: run <command> [options]',
            '',
            'Commands:',
            '',
            autodoc(self),
            ''
            )

    @classproperty
    @classmethod
    def desc(cls):
        return doc(cls).split('\n')[0]

    @classproperty
    @classmethod
    def options(self):
        return ["{}\t{}".format(" ".join(i for i in c), doc(func))
            for c, func in sorted(self.commands)]

    def execute(self, cmd, arg):
        """Call `cmd` passing `arg`."""
        for c, func in self.commands:
            if cmd in c:
                return func(self, arg) or ''
        return self.unknown_option(cmd)

    def unknown_option(self, cmd):
        return lines(
            'Unknown option: %s' % cmd,
            'Try --help for more information.',
            )

    @classproperty
    @classmethod
    def __autodoc__(cls):
        """Return additional documentation to insert into Sphinx autodoc."""
        return "\n".join(cls.options)

    @classproperty
    @classmethod
    def cmd(cls):
        """Return the command (the first argument)."""
        return argv[1] if len(argv) > 1 else None

    @classproperty
    @classmethod
    def arg(cls):
        """Return the argument (that follows the cmd)."""
        return argv[2] if len(argv) > 2 else None

    @classmethod
    def add(cls, cmds):
        """Add to the list of commands."""
        cls._cmds.update(cmds)


class CLIApplication(CLI):
    """An object that runs commands passed from an external invocation of the program.

    .. inheritance-diagram:: CommandLineApp

    Command Line Options::

            {autodoc}
    """

    def print_help(self, arg):
        """Print help / usage message."""
        return str(self)

    def build_docs(self, format):
        """Build the Sphinx Help Documentation (html or pdf)."""
        self.shell('cd %s; make %s' % (abspath('.') , format or 'html'))

    def run_tests(self, arg):
        """Run the Test Suite (-t 2 for verbose, --quick to skip slow tests).
        """
        verbosity = int(arg) if arg and arg[0] in digits else 1
        testsuite = TestLoader().discover('.', 'test*.py', '.')
        return TextTestRunner(verbosity=verbosity).run(testsuite)

    _cmds = {
        ('-h', '--help'):  print_help,
        ('-b', '--build'): build_docs,
        ('-t', '--test'):  run_tests,
    }

    @classmethod
    def new_application(cls):
        """This method can be subclassed to return a alternative application
        object when testing. (Useful for mocking).
        """
        return cls()

    @classmethod
    def isTesting(cls):
        return cls.cmd in ['-t', '--test']

    @classmethod
    def run_application(cls, default="--help"):
        """Run the application using the args passed from the command line.
        This is the main entry point to the application."""
        app = cls.new_application()
        return app.execute(cls.cmd or default, cls.arg)

    def shell(self, args, stdin=None, stdout=None, stderr=None, shell=True):
        """Call a shell command."""
        print(args)
        call(args, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)

    def open_file(self, fname):
        """Open local file `fname` in a web browser."""
        open('file://{}'.format(fname))
