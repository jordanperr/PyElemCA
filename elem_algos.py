import numpy as np
from time import perf_counter as clk
import matplotlib.pyplot as plt
from scipy import stats

class ElementaryCA_TransitionGraph:
	
	def __init__(self, rule, width):
		self.rule = rule
		self.width = width
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
