"""Command Line Interface
=========================
"""
from classproperty import classproperty
from sys import argv

def doc(obj):
    return obj.__doc__

def autodoc(obj):
    return obj.__autodoc__

def lines(*args):
    return "\n".join(args)


class CLI(object):
    """Helper class to implement a Command Line Interface."""
    _cmds = {}

    def __init__(self, cmds=None):
        self.add(cmds or {})

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

    def execute(self, app, cmd, arg):
        """Call `cmd` passing `arg`."""
        for c, func in self.commands:
            if cmd in c:
                return func(app or self, arg) or ''
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

    def __call__(self, app=None, default="--help"):
        """Run the application using the args passed from the command line.
        This is the main entry point to the application."""
        return self.execute(app, self.cmd or default, self.arg)
