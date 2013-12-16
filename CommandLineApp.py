"""Command Line Application
===========================

.. inheritance-diagram:: Utilities.CommandLineApp

"""
from __future__ 						import print_function
from sys 								import argv
import subprocess
import webbrowser


class CommandLineApp(object):
	"""An object that runs commands passed from an external invocation of the program."""

	def __init__(self, app=None):
		self.app 						= app

	def __call__(self):
		"""Parse the command line arguments passed via `argv`, and run the requested command."""
		cmd 							= argv[1] if len(argv) > 1 else '--help'
		opt 							= argv[2] if len(argv) > 2 else '*'
		[func(self, opt) for c, func in self if cmd in c]

	@property
	def desc(self):						return __doc__.split('\n')[0]

	def __str__(self):
		"""Return help message and usage."""
		help 							= '{}\n\n{}\n\n{}\n'.format(self.desc,
																	'usage: run <command> [options]',
																	'Commands:')
		options 						= []
		[options.append('{}\t{}'.format(' '.join(i for i in c), func.__doc__)) for c, func in sorted(self)]
		return '{}\n{}'.format(help, '\n'.join(options))

	def __getitem__(self, index):		return self._cmds.items()[index]

	def help(self, opt=None):
		"""Display help message and usage."""
		print (self)

	_cmds 								= {('-h', '--help'):			help}

	def shell(self, args, stdin=None, stdout=None, stderr=None, shell=False):
		"""Call a shell command."""
		subprocess.call(args, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)

	def open_file(self, fname):
		"""Open local file `fname` in a web browser."""
		webbrowser.open('file://{}'.format(fname))

	@classmethod
	def __autodoc__(cls):
		"""Return additional documentation to insert into Sphinx autodoc."""
		return str(cls())
