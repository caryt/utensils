"""Test
=======
"""
from unittest import TestCase
from cli import CLI
from config import Config
from os import environ


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
        self.assertEqual(self.cli.execute('--foo', None), 'Executed Foo')

    def test_autodoc(self):
        """Test CLI autodoc."""
        self.assertEqual(self.cli.__autodoc__, "-f --foo\tFoo.")


class TestConfig(TestCase):
    """Test :class:`.Config`."""

    def setUp(self):
        environ["CONFIG_OPTION"] = "override"
        self.config = Config()

    def test_defaults(self):
        """Test default configuration loaded from defaults.py."""
        self.assertEqual(self.config.CONFIG_NAME, 'value')

    def test_overrides(self):
        """Test configuration loaded from environment variables."""
        self.assertEqual(self.config.CONFIG_OPTION, 'override')

    def test_iter(self):
        """Test iterating over configuration."""
        self.assertEqual([config for config in self.config],
            [('CONFIG_NAME', 'value'), ('CONFIG_OPTION', 'override')]
        )

    def test_json(self):
        """Test JSON configuration."""
        self.assertEqual(self.config.json(),
            ['CONFIG_NAME = value', 'CONFIG_OPTION = override']
        )

    def test_html(self):
        """Test HTML configuration."""
        self.assertEqual(self.config.html(),
            '<ul><li>CONFIG_NAME = value<li>CONFIG_OPTION = override</ul>'
        )

