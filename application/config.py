"""Configuration Options
========================
"""
import defaults
from os import environ
from shlex import split


class Config(object):
    """Config objects store configuration options.
    Default values for each option are loaded from `defaults.py`,
    and can be overridden by setting a corresponding environment variable.
    """
    def __init__(self):
        self.defaults()
        self.overrides()

    def defaults(self):
        """Read the default configuration options from `defaults.py`."""
        [setattr(self, k, v) for k, v in defaults.__dict__.items()]


    def overrides(self):
        """Override each config from a matching environment variable,
        if it exists.
        """
        [setattr(self, k, int(environ[k]) if isinstance(v, int) else environ[k])
            for k, v in self
                if environ.has_key(k)
        ]

    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items() if not k.startswith('_'))

    def load_script(self, script):
        """Load environment variables from a bash shell script."""
        processed = script.replace('export ', '')
        for line in split(processed):
            key, eq, value = line.partition('=')
            if eq == '=':
                environ[key] = value
                setattr(self, key, value)

    def json(self):
        """Return a list representation of the conf,
        suitable for JSON encoding.
        """
        return ['%s = %s' % (k, v) for k, v in sorted(self)]

    def html(self):
        """Return an HTML representation of this configuration."""
        return "<ul><li>%s</ul>" % "<li>".join(self.json())
