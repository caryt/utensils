"""Test
=======
"""
from unittest import TestCase
from cli import CLI


class MyCLI(CLI):
    """Test CLI."""
    def foo(self, args):
        "Foo."
        return 'Executed Foo'

    _cmds = {('-f', '--foo'): foo}


class TestCLI(TestCase):
    """Test a :class:`.CLI`.
    """

    def setUp(self):
        self.cli = MyCLI()

    def test_commands(self):
        """Test CLI commands."""
        (short, long), func = self.cli.commands[0]
        self.assertEqual(short, '-f')
        self.assertEqual(long, '--foo')
        self.assertEqual(func.__doc__, 'Foo.')

    def test_str(self):
        """Test str(CLI)."""
        self.assertEqual(str(self.cli),
"""Test CLI.
Usage: run <command> [options]

Commands:

-f --foo\tFoo.
"""
        )

    def test_desc(self):
        """Test CLI description."""
        self.assertEqual(self.cli.desc, "Test CLI.")

    def test_options(self):
        """Test CLI options."""
        self.assertEqual(self.cli.options, ["-f --foo\tFoo."])

    def test_execute(self):
        """Test CLI execute."""
        self.assertEqual(self.cli.execute(self.cli, '--foo', None), 'Executed Foo')

    def test_autodoc(self):
        """Test CLI autodoc."""
        self.assertEqual(self.cli.__autodoc__, "-f --foo\tFoo.")