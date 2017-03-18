# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib.pyplot as plt
from scipy import stats

#####
# elem_step
#
# Calculates one step of elem automata using rule on state.
#
# input:  tuple, integer
# output: tuple
#
#####

def elem_step(state, rule):
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
		thisBit = (rule >> num) % 2
		# Append that bit to nextState
		nextState.append(thisBit)
	return tuple(nextState)

#####
# steps_until_repeat   O(2^N)
# Calculates the number of steps ca with rule and initial state must run to repeat.
#
# input:  tuple, integer
# output: integer
#
#####

def steps_until_repeat(state, rule, red, cycles):
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
				red[cycleState] = C
				cycleState = elem_step(cycleState,rule)
			cycles.append(C)
			break
			
		if state in red:
			blue[state] = step
			C = red[state]
			break
		
		# We've encountered an unvisited vertex. Keep going.
		blue[state] = step
		state = elem_step(state, rule)
		step += 1
		
	# We've encountered a finished tail or cycle, or just finished a cycle.
	# If there is a tail, we have to finish it.
	# At this point, state = a finished state, but its blue number is distance from IV
	if (blue[state] > 0):
		tailState = initial_state
		for n in range(blue[state])[::-1]:
			red[tailState] = C + n + 1
			tailState = elem_step(tailState,rule)
	
	return red[initial_state]-1
	
	

####
#
# O(256*width_max-width_min*steps_until_repeat)
#
#
####
RULE = 56
handles = []
for WIDTH in range(7,15):
	diameters = []
	red = {}
	cycles = []
	for i in range(2**WIDTH):
		# calculate the number of steps until this state repeats
		state = tuple([(i>>j)%2 for j in range(WIDTH)])
		steps = steps_until_repeat(state, RULE, red, cycles)
		diameters.append(steps)

	vars = stats.itemfreq(cycles)
	print(cycles)
	print(vars)

	plot, = plt.plot(vars[:,0], vars[:,1], 'o', label="Width={0}".format(WIDTH))
	handles.append(plot)

plt.title("Histograms of Cycle Lengths for Rule {0} and Various Widths".format(RULE))
plt.xlabel("Length of cycle")
plt.ylabel("Number of cycles")
plt.legend(handles=handles)
plt.savefig("cycleplots/fig.png")
