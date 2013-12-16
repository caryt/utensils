"""Flask Utilities
==================

.. inheritance-diagram:: Utilities.Flask

"""
from __future__ 						import print_function
from Utilities.Validators 				import Validators
from flask 								import Flask, Blueprint, render_template, url_for, redirect, flash, abort, request, session
from copy 								import copy
from logging 							import Formatter
from logging.handlers					import SMTPHandler, SysLogHandler
from operator 							import mul, div

POST 									= ["POST"]
"""HTTP POST method definition."""

DELETE 									= ["DELETE"]
"""HTTP DELETE method definition."""


class FlaskApp(Flask):
	"""A Flask Application, extended with some useful methods, and a factory function `App`."""

	@classmethod
	def App(cls, config):
		"""Create an application object.
		Load the default configuration from `config`, then load configuration overrides from `envvar`."""
		app								= cls(config.APP_NAME, template_folder=config.TEMPLATE_FOLDER)
		app.config.from_object(config.CONFIG_FILE)
		app.config.from_envvar(config.ENVVAR)
		app.configure_email_logging(config)
		app.configure_sys_logging(config)
		return app

	def configure_email_logging(self, config):
		"""Configure a Logger for sending eMails."""
		if config.SMTP_SERVER:
			mail_handler 				= SMTPHandler(	config.SMTP_SERVER,
														config.APP_EMAIL,
														config.WEBMASTER,
														config.EMAIL_SUBJECT)
			mail_handler.setLevel(config.LOG_LEVEL_EMAIL)
			mail_handler.setFormatter(Formatter(config.EMAIL_FORMAT))
			self.logger.addHandler(mail_handler)

	def configure_sys_logging(self, config):
		"""Configure a Logger for logging to syslog."""
		if config.SYSLOG:
			syslog_handler				= SysLogHandler(config.SYSLOG)
			syslog_handler.setFormatter(Formatter(config.SYSLOG_FORMAT))
			syslog_handler.setLevel(config.LOG_LEVEL_SYSLOG)
			self.logger.addHandler(syslog_handler)

	def label(self, rule, n):				return '/'.join(str(rule).split('/')[:-2])+'/'
	def ruleLabel(self, rule):
		"""Return a description for a Rule."""
		return '\t\t"{}" -> "{}" [label="{}"]'.format(rule, rule.endpoint, '\n'.join(m for m in rule.methods if m not in ['OPTIONS', 'HEAD']))

	def shapes(self, rule):
		return '\t\t"{}" [shape=box]'.format(rule.endpoint)

	def ranks(self):
		return ['"{}"'.format(rule.endpoint) for rule in self.url_map.iter_rules()]

	def ranks1(self):
		return ['"{}"'.format(self.label(rule, -1)) for rule in self.url_map.iter_rules()]
	def ranks2(self):
		return ['"{}"'.format(self.label(rule, -2)) for rule in self.url_map.iter_rules()]

	def ruleLabel2(self, rule):
		"""Return a description for a Rule."""
		return '\t\t"{}" -> "{}"'.format(self.label(rule, -2), self.label(rule, -1))

	def ruleLabel3(self, rule):
		"""Return a description for a Rule."""
		return '\t\t"{}" -> "{}"'.format(self.label(rule, -1), rule)

	def routesGraph(self):
		"""Return graph edges (graphviz format) documenting all Routing Rules.
		Sutiable for autodocing a class with a doctring containing

		.. code-block:: rest

			.. graphviz::

				digraph {{graph [rankdir=LR] node [fontsize=12] edge [fontsize=10]
				{autodoc}
				}}
		"""
		return ('\n'.join(self.ruleLabel( rule) for rule in self.url_map.iter_rules()) +
				'\n'.join(self.shapes(rule) for rule in self.url_map.iter_rules()) +
				'\n\t\t{rank=same;' + ';'.join(self.ranks()) + '}' +
				'\n\t\t{rank=same;' + ';'.join(self.ranks1()) + '}' +
				'\n\t\t{rank=same;' + ';'.join(self.ranks2()) + '}' +
				'\n'.join(self.ruleLabel2(rule) for rule in self.url_map.iter_rules()) +
				'\n'.join(self.ruleLabel3(rule) for rule in self.url_map.iter_rules()))

	def abort(self, error):
		"""Raise HTTP Error code `error`."""
		abort(error)

	@property
	def form(self):
		"""Return the `form from the Request object."""
		return request.form

	@property
	def session(self):
		"""Return the session object for the user's curren session."""
		return session

	def set_session(self, session):
		"""Set default values stored in the user's session."""
		pass


class Blueprint(Blueprint):
	"""A Flask Blueprint with some additional methods."""

	def add_rules(self, fldr, cls, create=None, read=None, update=None, delete=None, add=None, index=None):
		"""Add a set of URL routing rules to this blueprint and its parent folder `fldr`.
		These rules perform CRUD operations for a blueprint at these URL's:

			`POST /cls/`
				Create a new object.
			`GET /cls/<id>`
				Display the object.
			`POST /cls/<id>`
				Update the object.
			`DELETE /cls/<id>`
				Delete the object.
			`GET /cls/`
				Display a list all all objects.
			`GET /add_cls`
				Display a new, empty, object.
		"""

		def fmt(str, cls):
			return str.format(cls.__name__.lower())

		def add_rule(blue, rule, endpoint, view_func, methods=None):
			if rule is not None:
				blue.add_url_rule(rule, endpoint, view_func=view_func, methods=methods)

		add_rule(fldr, fmt('/{}/', cls), 	fmt('create_{}', cls), 	create,	POST)
		add_rule(self, '', 					fmt('{}', cls), 		read)
		add_rule(self, '', 					fmt('update_{}', cls), 	update, POST)
		add_rule(self, '', 					fmt('delete_{}', cls), 	delete, DELETE)
		add_rule(fldr, fmt('/{}/', cls), 	fmt('list_{}', cls), 	index)
		add_rule(fldr, fmt('/add_{}', cls), fmt('add_{}', cls), 	add)


class Template(object):
	"""A wrapper for a Flask (Jinja2) Template.
	Initialise with the name of a template file, then call to render it.
	"""

	def __init__(self, name, template):
		self.name 						= name
		"""The name of the route for this Template (as used by url_for()).
		If the route is defined in a Blueprint use dot syntax i.e. *blueprintName.templateName*."""

		self.template 					= template
		"""The name of the Jinja2 Template document used to render this Template."""

	def __call__(self, o, error=None): return render_template(self.template, obj=o, error=error)
	def __repr__(self):					return "{}({}, {})".format(self.__class__.__name__, self.name, self.template)
	def url(self, **kwargs):
		tab 	 						= kwargs.pop('tab', None)
		return url_for(self.name, **kwargs) + ("#tab_{}".format(tab) if tab else '')


class Views(object):
	"""Mix-in class for objects that have supporting Jinga2 Templates."""
	SUCCESS 							= 'success'
	ERROR 								= 'error'

	template 							= Template(None, 'error/501.html')

	def _notImpl(self, **kwargs):
		"""Return a URL that resolves to a 501 (Not Implemented) error page.
		This is handy during development to produce nice error messages when objects aren't fully implemented.
		"""
		return '/501/{}'.format('&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))

	def url(self, **kwargs):
		"""Return the URL for this object. (Links to 501 error if not implemented yet)."""
		return self.template.url(**kwargs) if self.template.name is not None else self._notImpl(**kwargs)

	def validate(self, error):
		"""Override this method to update `error` by validating form data for this object."""
		pass

	def flash_message(self, message, category=None):
		"""Create a Jinja2 *flash* message."""
		flash(message.format(obj=self), category or self.SUCCESS)

	def redirect(self, parent=False, subpath=None):
		"""Redirect to the URL for this object (or its parent index page)."""
		url 							= self.url()
		if parent:						url = '/'.join(url.rstrip('/').split('/')[:-1])
		if subpath:						url = url + subpath
		return redirect(url)

	def actioned(self, message, category=None, parent=False):
		"""Flash a message and redirect back to object."""
		if message: 					self.flash_message(message, category=category)
		return self.redirect(parent)

	def set_session(self, session):
		"""Set default values stored in the user's session."""
		pass


class Record(object):
	"""A dictionary-like object that can be accessed via dict.field or dict['field']."""
	def __getitem__(self, item):		return getattr(self, item)


class Validate(Validators):
	"""Error Handling. Implements methods for validating an object and reporting any resulting errors."""

	CREATE 								= "create"
	"""The Create action for forms."""

	UPDATE 								= "update"
	"""The default action for forms."""

	DELETE 								= "delete"
	"""The Delete action for forms."""

	UPDATE_ITEM 						= "update."
	"""The prefix used in `<button type="submit" name="action" value="update.{index}"...>` form buttons.
	These buttons will update {index} for the object."""

	DELETE_ITEM 						= "delete."
	"""The prefix used in `<button type="submit" name="action" value="delete.{index}"...>` form buttons.
	These buttons will delete {index} from the object."""

	ADD_ITEM 							= "add"
	"""The action for `<button type="submit" name="action" value="add"...>` form buttons.
	These buttons will add an item into the object."""


	def __init__(self, obj, form=None):
		"""Validate the object, create error messages (and web page *flash* messages)."""
		Validators.__init__(self)
		self.obj 						= obj
		self.form 						= form
		self._error 					= None
		self.index 						= None
		self.validate_action()

	def message(self, msg, field):
		"""Create and format an error message with {field} and {value} interpolation."""
		self.error[field] 				= msg.format(	field 	= field,
														value 	= '"{}"'.format(self.form.get(field, '')),
														units 	= '"{}"'.format(self.form.get('dropdown_'+str(field), '')))
		return False

	def __call__(self, validate, *fields, **kwargs):
		"""Validate multiple fields against a validator."""
		[validate(field, **kwargs) for field in fields]

	def _try(self, func, field, msg):
		try:
			self[field] 				= func(self.form[field])
			return True
		except:
			return self.message(msg, field)

	def _dropdown(self, dict, field, func):
		try:
			dropdown 					= self.form['dropdown_{}'.format(field)]
			unit 						= dict[dropdown]
			self[field] 				= func(self[field], unit)
		except KeyError:
			if dropdown == '':
				return self.message('Select a {field} from the drop-down list.', field)
			return self.message('{field} had unexpected Unit ({units})', field)

	def _units(self, dict, field):
		"""Check that the `field` has a dropdown field with units as stored in `dict`."""
		return self._dropdown(dict, field, mul)

	def _rate(self, dict, field):
		"""Check that the `field` has a dropdown field with rate as stored in `dict`."""
		return self._dropdown(dict, field, div)

	@property
	def error(self):
		"""Perform the validations and return any errors.
		If there are no errors, the action (usually update) is performed.
		This has the side-effect of modifying the object.
		"""
		if self._error is None:
			self._error 				= {}
			self.obj.validate(self)
			self.perform_action()
		return self._error

	def actioned_message(self, app):
		"""Return the message to be displayed after perofmrig the action."""
		action 							= self.action
		if action == self.CREATE: 		return app.config['CREATED'].format(obj=self.obj)
		if action == self.UPDATE: 		return app.config['UPDATED'].format(obj=self.obj)
		if action == self.DELETE: 		return app.config['DELETED'].format(obj=self.obj)
		if action == self.UPDATE_ITEM: 	return None #app.config['UPDATED_ITEM'].format(item='entry')
		if action == self.DELETE_ITEM: 	return None #app.config['DELETED_ITEM'].format(item='entry')
		if action == self.ADD_ITEM: 	return None #app.config['ADDED_ITEM'].format(item='entry')
		return app.config['PERFORMED'].format(action=action)

	def perform_action(self):
		"""Perform the `action`."""
		action 							= self.action
		if self.error: 					return self._error
		if action == self.CREATE: 		return self.perform_update()
		if action == self.UPDATE: 		return self.perform_update()
		if action == self.DELETE: 		return self.perform_update()
		if action == self.UPDATE_ITEM: 	return self.perform_update_item(self.index)
		if action == self.DELETE_ITEM: 	return self.perform_delete_item(self.index)
		if action == self.ADD_ITEM: 	return self.perform_add()

	def perform_update(self):
		"""Copy all field values from `value` back into the object."""
		[setattr(self.obj, field, value) for field, value in self.items() if field is not None]

	def perform_update_item(self, index):
		"""Copy all field values from `value` back into the object[index]."""
		[setattr(self.obj[index], field, value) for field, value in self.items() if field is not None]

	def perform_add(self):
		"""Add an item into the object."""
		item = Record()
		[setattr(item, field, value) for field, value in self.items() if field is not None]
		self.obj.addItem(item)
		return self.obj

	def perform_delete_item(self, index):
		"""Delete the `index` item from the object."""
		del self.obj[index]
		return self.obj

	def copy(self):
		"""Return a copy of the object, to render in the template, when errors are present.
		This means that the form, including erroneous input, is redisplayed to the user when errorsa
		are present - without updating the underlying object.
		"""
		result 							= copy(self.obj)
		[setattr(result, field, self.form[field]) for field in self.error.keys() if field is not None]
		return result

	def render_error(self):
		"""Display the objects template, with error messages, and rendered with the users input
		(including any erroneous entries).
		"""
		flash('\n'.join(self.error.values()), self.obj.ERROR)
		return self.obj.template(self.copy(), self.error)

	def validate_action(self, field=None):
		"""Validate the submit button's action.
		Sets the action property, and the index property if the action is on a sub-item.
		"""
		field 							= 'action' if field is None else field
		self.action 					= self.form.get(field, self.UPDATE)
		self.validate_action_item(self.form[field])

	def set_action_index(self, action):
		"""Return None or the index of the form's action to be perfomed."""
		try:
			self.index					= int(action.split('.')[1])
			return self.index
		except (ValueError, KeyError):
			return self.message('Unexpected value:{}'.format(action), None)
		return None

	def validate_action_item(self, action):
		"""Check **if** the field is an action on an individual item.
		Returns None, or the index of the item to be actioned.
		Used when the form has `<button type="submit" name="action" value="{action}.{index}"...`.
		This also sets the `action` and `index` properties.
		"""
		if action.startswith(self.UPDATE_ITEM):
			self.action 				= self.UPDATE_ITEM
			return self.set_action_index(action)
		elif action.startswith(self.DELETE_ITEM):
			self.action 				= self.DELETE_ITEM
			return self.set_action_index(action)
		return None

