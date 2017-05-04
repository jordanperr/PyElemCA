# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib.pyplot as plt


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
	
	
#from wolframalpha.com
classes = {
	1: [0,8,32,40,64,96,128,136,160,168,192,224,234,235,238,239,248,249,250,251,252,253,
		254,255],
	2: [1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,19,20,21,23,24,25,26,27,28,29,31,33,34,35,
		36,37,38,39,41,42,43,44,46,47,48,49,50,51,52,53,55,56,57,58,59,61,62,63,65,66,67,
		68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,87,88,91,92,93,94,95,97,98,99,
		100,103,104,107,108,109,111,112,113,114,115,116,117,118,119,121,123,125,127,130,
		131,132,133,134,138,139,140,141,142,143,144,145,148,152,154,155,156,157,158,159,
		162,163,164,167,170,171,172,173,174,175,176,177,178,179,180,181,184,185,186,187,
		188,189,190,191,194,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,
		211,212,213,214,215,216,217,218,219,220,221,222,223,226,227,228,229,230,231,233,
		236,237,240,241,242,243,243,244,245,246,247],
	3: [18,22,30,45,60,75,86,89,90,101,102,105,122,126,129,135,146,149,150,151,153,161,
		165,182,183,195],
	4: [54,106,110,120,124,137,147,169,193,225],
	5: range(256)
}


for classno in classes:
	
	maxwidth = 10

	diameters = {}
	for n in range(3,maxwidth+1):
		diameters[n] = []

	for RULE in classes[classno]:
	
		for WIDTH in range(3,maxwidth+1):
			red = {}
			cycles = []
			for i in range(2**WIDTH):
				# calculate the number of steps until this state repeats
				state = tuple([(i>>j)%2 for j in range(WIDTH)])
				steps = steps_until_repeat(state, RULE, red, cycles)
				diameters[WIDTH].append(steps+1)
		
		print("Class {0} Rule {1}".format(classno, RULE))
		
	plt.cla()
	x_global = range(3,maxwidth+1)
	avg = [np.average(diameters[n]) for n in x_global]
	error = [np.std(diameters[n]) for n in x_global]
	plt.errorbar(x_global, avg, error, linestyle='None', marker='^')
	plt.plot(x_global, avg, '-o', label="Average")
	plt.plot(x_global, [max(diameters[n]) for n in x_global], '-+', label="Maximum")
	plt.plot(x_global, [min(diameters[n]) for n in x_global], '-+', label="Minimum")
	plt.legend()
	plt.ylim(ymin=0)
	plt.title("Diameter vs Width for Class {0}".format(classno))
	plt.xlabel("Width")
	plt.ylabel("Diameter")
	plt.savefig("./outputs/diam/diamVsWidth_class{0}.png".format(classno))

