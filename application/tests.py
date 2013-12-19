"""Test
=======
"""
from unittest import TestCase
from config import Config
from os import environ


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

