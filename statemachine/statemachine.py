"""State Machine
================

.. inheritance-diagram:: StateMachine
"""
from null 								import Null
from functools 							import partial


class StateError(TypeError):
	"""A StateException is raised when an operation is attempted on a StateMachine when it is in an inappropriate State."""
	pass


class MetaState(type):
	"""The meta-class for State. Since State **classes** as used, some operations on those classes are defined here."""
	def __repr__(cls):					return cls.__name__
	__str__ = __repr__
	def __len__(cls):					return len(str(cls))


class State(object):
	"""A State class represents the current state of a :class:`.StateMachine`.

	States have:-

	* a `moveTo` set which contains the States we can transitionto.
	* or `moveTo` can be a dictionary of states with a transition method that is called when moving to the new state.
	* an `__init__` method which performs the processing required when moving to this new state.

	"""
	__metaclass__						= MetaState
	"""The metaclass defines some methods on State **Class**."""

	def __init__(self, machine):
		"""Processing to be performed when transitioning to this state."""
		pass

	def __repr__(self):					return repr(self.__class__)
	def __str__(self):					return str(self.__class__)
	def __eq__(self, other):			return isinstance(self, other)

	@property
	def an(self):
		"""Format a/an depending on the state."""
		return _.Plural.indefinite(self)

	def transition(self, machine, newState):
		"""Move `machine` to `newState`:

			1. Check that the new state is a valid transition from this state.
			2. Set the new state.
			3. Call the transition method (if present).
		"""
		if newState in self.movesTo:
			machine._state 				= newState(self)
			if hasattr(self.movesTo, 'get'):
				self.movesTo[newState](self, machine)
			machine.transitioned(self, newState)
		else:
			raise StateError("A{n} {state} {machine} can't be {new}.".format(n=self.an, state=self, machine=self.__class__.__name__, new=newState))

	movesTo 							= {}
	"""A dictionary of State Transitions {NewState: transition_method}."""


class StateMachine(object):
	"""A StateMachine is an object that can be in one of a number of different :class:`.State`'s'.

	Setting the `state` checks whether the transition is allowed and moves the StateMachine into the new state -
	performing any required processing on the transition.
	A `StateError` is raised if the transition is not allowed.
	"""
	def __init__(self, InitialState):
		"""Set the initial State to `InitialState` (a Class)."""
		self._state = InitialState(self)

	def goto(self, newState):
		"""Transition to the `newState` state (a class)."""
		self.state = newState

	def inState(self,  State):
		"""Return True is machine is in `State` (a class, or a list of State classes)."""
		if isinstance(State, list):
			return any(isinstance(self.state, state) for state in State)
		return isinstance(self.state, State)

	def assertInState(self, State, message=None):
		"""Raise a StateError if StateMachine is not in `State` (a class, or a list of State classes).

		message is passed with the exception. It can contain "a{n} {state}"" which will be replaced by the current state."""
		if not self.inState(State): raise StateError(message.format(state=self.state, n=self.state.an))

	def __getattr__(self, attr):
		"""Find and return a function to execute a state transition. Allows State Transitions to be written as ``machine.transition()``.

		This is a convenient alternative to ``machine.state=NewState``, when newState in state.movesTo.
		"""
		if not attr.startswith('_') and hasattr(self.movesTo, 'get'):
			for newState, transition_method in self.movesTo.items():
				if attr == transition_method.__func__.__name__:
					return partial(self.state.transition, self, newState)
		raise AttributeError('{} object has no attribute "{}"'.format(self.__class__.__name__, attr))

	@property
	def state(self):					return self._state
	@state.setter
	def state(self, newState):			self._state.transition(self, newState)

	@property
	def movesTo(self):					return self._state.movesTo

	def can(self, stateName):
		"""Return True if machine can moveTo `stateName`."""
		return stateName in map(str, self.movesTo.keys())

	def transitioned(self, oldState, newState):
		"""Called after machine moves from `oldSate` to `newState`."""
		pass

	# @classmethod
	# def transitions(cls):
	# 	"""Return a dictionary documenting all state transitions."""
	# 	def can(From, To): 				return To in From.movesTo
	# 	def row(From):					return [can(From, To) for To in cls.allStates]
	# 	transitions 					= []
	# 	[transitions.append(row(From)) for From in cls.allStates]
	# 	return transitions

	# @classmethod
	# def transitionsTable(cls):
	# 	"""Return a table (in Restructured Text format) documenting all State Transitions."""
	# 	def Max(allStates):		return 'x' * max(len(s) for s in allStates)
	# 	cols 					= [Max(cls.allStates)] + cls.allStates
	# 	separater 				= '\n{}\n'.format(' '.join('=' * len(s) for s in cols))
	# 	header					= ' '.join(str(s) for s in cols)
	# 	def entry(s, x):		return (('Y' if x else '-') + ' ' * len(s))
	# 	def line(row):			return [entry(s, x) for (s, x) in zip(cls.allStates, row)]
	# 	def labelled(s, row):	return format(str(s), str(len(Max(cls.allStates))+1)) + ''.join(line(row))
	# 	return separater + header + separater + '\n'.join(labelled(state, row) for (state, row) in zip(cls.allStates, cls.transitions())) + separater

	@classmethod
	def edgeLabel(cls, From, To):
		"""Return a named label for a state transition. (Only applicable if the transition has an associated method)."""
		return '[label="{}()"]'.format(From.movesTo[To].__func__.__name__) if hasattr(From.movesTo, 'get') else ''

	@classmethod
	def transitionLabel(cls, From, To):
		"""Return a description for a State Transition."""
		return '\t\t\t{} -> {} {}'.format(From, To, cls.edgeLabel(From, To))

	@classmethod
	def transitionsGraph(cls, states):
		"""Return the edges for a graph (graphviz format) documenting all State Transitions.
		"""
		return '\n'.join(cls.transitionLabel(From, To) for From in states for To in From.movesTo)
