# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from scipy import stats



class ElementaryHomogenousCA:
	"""ElementaryHomogenousCA Class
		Complies with Python 3 Generator Pattern
		Initialize with rule, state tuple, and optional iteration max
		Generates each new state (including initial state)"""
	def __init__(self, rule, state, iters=None):
		# State
		self.rule = rule
		self.state = state
		self.iters = iters
		# Convenience parameters
		self.width = len(state)
		# Settings
		self.SHOW_IV = True
		
	
	def __iter__(self):
		return self
	
	
	def neighbors(self, index):
		"""ElementaryHomogenousCA.neighbors(index)
			index = index of cell (1-D) for which you'd like the neighbors
			returns 3-tuple of neighbor indices (including index)."""
		
		n = self.width
		i = index
		if index==0:
			return (n-1, 0, 1)
		if index==n-1:
			return (n-2, n-1, 0)
		else:
			return (i-1, i, i+1)
	
	
	def transition(self, state):
		"""ElementaryHomogenousCA.transition(state)
			index = index of cell (1-D) for which you'd like the neighbors
			returns 3-tuple of neighbor indices (including index)."""
		
		nextState = []
		for i in range(self.width):
			neighbors = [state[j] for j in self.neighbors(i)]
			num = neighbors[2]*2**0 + neighbors[1]*2**1 + neighbors[0]*2**2
			# Identify bit in RULE that corresponds to neighbor vector
			thisBit = (self.rule >> num) % 2
			# Append that bit to nextState
			nextState.append(thisBit)
		return tuple(nextState)
	
	
	def __next__(self):
		if self.SHOW_IV:
			self.SHOW_IV = False
			return self.state
		self.iters -= 1
		if self.iters >= 0:
			self.state = self.transition(self.state)
			return self.state
		else:
			raise StopIteration()



class TransitionGraph:
	"""TransitionGraph Class
		A bundle of algorithms to work with transition graphs of elementary
		cellular automata"""
	def __init__(self, rule, width):
		# Parameters for Transition Graph
		self.rule = rule
		self.width = width
		
		# State Variables for Calculation
		self.clearInternalState()
		
	def clearInternalState(self):
		self.ca = ElementaryHomogenousCA(rule, None)
		self.distances = {}
		self.cycles = []
		
		
	def traverse(self):
		self.clearInternalState()
		for i in range(2**self.width):
			state = tuple([(i>>j)%2 for j in range(self.width)])
			self.steps_until_repeat(state)


	def steps_until_repeat(self, state, cycle_edges=None, tail_edges=None):
		"""
		steps_until_repeat   O(2^N)

		 Calculates the number of steps ca with rule and initial state must run to repeat.

		 input:  tuple, integer
		 output: integer
		"""
		step = 0
		blue = {}
	
		# Step 1, Traverse until repeat
		initial_state = state
		while True:
	
			if state in blue:
				# We've encountered a new cycle. Finish cycle.
				C = step - blue[state] #step+1?
				cycleState = state
				for i in range(C):
					self.distances[cycleState] = C
					next_cycleState = self.elem_step(cycleState)
					# Handle for external functions
					if cycle_edges:
						cycle_edges(cycleState, next_cycleState)
					cycleState = next_cycleState
				self.cycles.append(C)
				break
			
			if state in self.distances:
				blue[state] = step
				C = self.distances[state]
				break
		
			# We've encountered an unvisited vertex. Keep going.
			blue[state] = step
			state = self.elem_step(state)
			step += 1
		
		# We've encountered a finished tail or cycle, or just finished a cycle.
		# If there is a tail, we have to finish it.
		# At this point, state = a finished state, but its blue number is distance from IV
		if (blue[state] > 0):
			tailState = initial_state
			for n in range(blue[state])[::-1]:
				self.distances[tailState] = C + n + 1
				next_tailState = self.elem_step(tailState)
				if tail_edges:
					tail_edges(tailState, next_tailState)
				tailState = next_tailState
	
		return self.distances[initial_state]-1

	
	def for_each_edge(self, cycle_edge, tail_edge):
		WIDTH = self.width
		for i in range(2**WIDTH):
			state = tuple([(i>>j)%2 for j in range(WIDTH)])
			self.steps_until_repeat(state, cycle_edge, tail_edge)

	
	
class ElementaryCA_TransitionGraph:
	
	def __init__(self, rule, width):
		# Properties of cellular automaton
		self.rule = rule
		self.width = width
		# Helper variables for steps_until_repeat
		# Call traverse() to update these.
		self.distances = {}
		self.cycles = []
	
	def clearInternalState(self):
		self.distances = {}
		self.cycles = []

	def elem_step(self, state):
		"""
		elem_step

		 Calculates one step of elementary automata using self.rule on state.
	
		 input:  tuple (state at t)
		 output: tuple (state at t+1)
	
		"""
		nextState = []
		n = len(state)
		# Built nextState term by term
		for i in range(n):
			# compute neighbors
			if i==0:
				neighbors = [state[n-1], state[0], state[1]]
			if i==n-1:
				neighbors = [state[n-2], state[n-1], state[0]]
			else:
				neighbors = [state[i-1], state[i], state[i+1]]	
			# convert state of neighbors to an integer
			num = neighbors[2]*2**0 + neighbors[1]*2**1 + neighbors[0]*2**2
			# Identify bit in RULE that corresponds to neighbor vector
			thisBit = (self.rule >> num) % 2
			# Append that bit to nextState
			nextState.append(thisBit)
		return tuple(nextState)
		
		
	def traverse(self):
		self.clearInternalState()
		for i in range(2**self.width):
			state = tuple([(i>>j)%2 for j in range(self.width)])
			self.steps_until_repeat(state)
			
	def diameter(self):
		self.clearInternalState()
		diam = -1
		for i in range(2**self.width):
			state = tuple([(i>>j)%2 for j in range(self.width)])
			newDiam = self.steps_until_repeat(state)
			if newDiam > diam:
				diam = newDiam
		return diam
		


	def steps_until_repeat(self, state, cycle_edges=None, tail_edges=None):
		"""
		steps_until_repeat   O(2^N)

		 Calculates the number of steps ca with rule and initial state must run to repeat.

		 input:  tuple, integer
		 output: integer
		"""
		step = 0
		blue = {}
	
		# Step 1, Traverse until repeat
		initial_state = state
		while True:
	
			if state in blue:
				# We've encountered a new cycle. Finish cycle.
				C = step - blue[state] #step+1?
				cycleState = state
				for i in range(C):
					self.distances[cycleState] = C
					next_cycleState = self.elem_step(cycleState)
					# Handle for external functions
					if cycle_edges:
						cycle_edges(cycleState, next_cycleState)
					cycleState = next_cycleState
				self.cycles.append(C)
				break
			
			if state in self.distances:
				blue[state] = step
				C = self.distances[state]
				break
		
			# We've encountered an unvisited vertex. Keep going.
			blue[state] = step
			state = self.elem_step(state)
			step += 1
		
		# We've encountered a finished tail or cycle, or just finished a cycle.
		# If there is a tail, we have to finish it.
		# At this point, state = a finished state, but its blue number is distance from IV
		if (blue[state] > 0):
			tailState = initial_state
			for n in range(blue[state])[::-1]:
				self.distances[tailState] = C + n + 1
				next_tailState = self.elem_step(tailState)
				if tail_edges:
					tail_edges(tailState, next_tailState)
				tailState = next_tailState
	
		return self.distances[initial_state]-1
	
	def for_each_edge(self, cycle_edge, tail_edge):
		WIDTH = self.width
		for i in range(2**WIDTH):
			state = tuple([(i>>j)%2 for j in range(WIDTH)])
			self.steps_until_repeat(state, cycle_edge, tail_edge)
			
		
