"""Command Line Application
===========================

.. inheritance-diagram:: CommandLineApp

"""
from __future__ import print_function
from cli import CLI
from testing import HTMLTestRunner
from unittest import TestLoader, TextTestRunner
from string import digits
from subprocess import call
from webbrowser import open
from os.path import abspath


class CLIApplication(object):
    """An object that runs commands passed from an external invocation of the program.

    .. inheritance-diagram:: CommandLineApp

    Command Line Options::

            {autodoc}
    """
    Runner = HTMLTestRunner or TextTestRunner
    """The TestRunner class."""

    def __init__(self):
        self.cli = CLI()
        self.cli.add(self._cmds)

    def print_help(self, arg):
        """Print help / usage message."""
        return str(self.cli)

    def build_docs(self, format):
        """Build the Sphinx Help Documentation (html or pdf)."""
        self.shell('cd %s; make %s' % (abspath('.') , format or 'html'))

    def run_tests(self, arg):
        """Run the Test Suite (-t 2 for verbose, --quick to skip slow tests).
        """
        verbosity = int(arg) if arg and arg[0] in digits else 1
        testsuite = TestLoader().discover('.', 'test*.py', '.')
        testrunner = self.Runner(verbosity=verbosity)
        result = testrunner.run(testsuite)
        if hasattr(testrunner, 'fname'):
            self.open_file(testrunner.fname)
        return result


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
    def run_application(cls):
        """Run the application using the args passed from the command line.
        This is the main entry point to the application."""
        app = cls.new_application()
        return app.cli(app)

    def shell(self, args, stdin=None, stdout=None, stderr=None, shell=True):
        """Call a shell command."""
        call(args, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)

    def open_file(self, fname):
        """Open local file `fname` in a web browser."""
        open('file://{}'.format(fname))
