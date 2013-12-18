"""StateMachine tests.

"""
from unittest import TestCase
from statemachine import State, StateMachine, StateError
from null import Null


#Define a couple of simple States
class State1(State):
    def advance(self, machine):                     machine.message = 'Entered State 2'
    def movesTo(self, new):                         return True if new == State2 else State.movesTo(self, new)
class State2(State):
    def movesTo(self, new):                         State.movesTo(self, new)

State1.movesTo = {State2: State1.advance}
State2.movesTo = {}

class Test_State(TestCase):
    """Test a State."""

    def test_State(self):
        """Test State"""
        self.assertEqual(str(State1),               'State1')
        self.assertEqual(str(State2),               'State2')


class Test_StateMachine(TestCase):
    """Test a State Machine."""

    def test_stateMachine_initialState(self):
        """Test State Machine Initial set up."""
        machine                                     = StateMachine(State1)

        self.assertTrue(machine.inState(State1))
        self.assertFalse(State1 in machine.state.movesTo)
        self.assertTrue(State2 in machine.state.movesTo)

    def test_stateMachine_transitions_byGoto(self):
        """Test State Transations from State 1 to State2."""
        machine                                     = StateMachine(State1)
        self.assertRaises(StateError,               machine.goto, State1)
        self.assertTrue(machine.inState(State1))
        machine.goto(State2)
        self.assertEqual(machine.message,           'Entered State 2')
        self.assertTrue(machine.inState(State2))

    def test_stateMachine_transitions_byCall(self):
        """Test State Transations from State 1 to State2."""
        machine                                     = StateMachine(State1)
        self.assertRaises(StateError,               machine.goto, State1)
        self.assertTrue(machine.inState(State1))
        machine.advance()
        self.assertEqual(machine.message,           'Entered State 2')
        self.assertTrue(machine.inState(State2))

    def test_stateMachine_transitions_byAssignment(self):
        """Test State Transations from State 1 to State2."""
        machine                                     = StateMachine(State1)
        self.assertRaises(StateError,               machine.goto, State1)
        self.assertTrue(machine.inState(State1))
        machine.state = State2
        self.assertEqual(machine.message,           'Entered State 2')
        self.assertTrue(machine.inState(State2))

    def test_stateMachine_finalState(self):
        """Test Final State."""
        machine                                     = StateMachine(State1)
        self.assertTrue(machine.inState(State1))
        machine.goto(State2)
        self.assertTrue(machine.inState(State2))
        self.assertFalse(State1 in machine.state.movesTo)
        self.assertFalse(State2 in machine.state.movesTo)
        self.assertRaises(StateError,               machine.goto, State1)
        self.assertRaises(StateError,               machine.goto, State2)
        self.assertTrue(machine.inState(State2))
