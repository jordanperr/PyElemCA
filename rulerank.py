# Jordan Perr-Sauer
# For Independent Study, 4/3/2017

from elem_algos import *
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# Let's calculate how many iterations it takes to determine the rule number.

bitsKnown = {}
pathLength = {}

print("Rule | Width   |  % Of IVs Leading To Rule Identification")

for RULE in [0, 19, 20, 30, 54, 78, 105, 110]:
	
	# Plotting Code
	x = []
	y = []
	
	for WIDTH in [3,4,5,6,7,8,9,10,11,12,13,14,15]:
		bitsKnown = []
		pathLength = []
		ca = ElementaryCA_TransitionGraph(RULE, WIDTH)
		for i in range(2**WIDTH):
			state = tuple([(i>>j)%2 for j in range(WIDTH)])
			IV = state
			# How many iterations does it take for this IV to produce a rule?
			# If it does not produce a rule, how many bits were determined?
			states = set()
			states.add(state)
			steps = 0
			rule = [None, None, None, None, None, None, None, None]
			while True:
				# Check if rule is completely determined
				if not (None in rule):
					break
				
				# Calculate next state
				next_state = ca.elem_step(state)
				
				steps += 1
				
				# Compute rule index position from neighborhood
				n = len(next_state)
				# neighborhood is in state, new val is in next_state
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
					
					rule[num] = next_state[i]
				
				#print(rule)
				
				# Check if this state has been visited already
				if next_state in states:
					break
				
				states.add(next_state)
				
				state = next_state
			
			
			# Analyse results
			bitsKnown.append( sum([1 if i != None else 0 for i in rule]) )
			pathLength.append( steps )
		
		# percentage of IVs able to identify rule
		#ruleIdentifiers = sum([1 if bitsKnown[i]==8 else 0 for i in range(len(bitsKnown))])
		#y.append(ruleIdentifiers/len(bitsKnown))
		#x.append(WIDTH)
		#print("{0:3}    {1:2}         {2:<10}".format(RULE, WIDTH, ruleIdentifiers/len(bitsKnown)))
		
		# for IVs with full rule identification, average path length
		ruleIdentifiers = [pathLength[i] for i in range(len(bitsKnown)) if bitsKnown[i] == 8]
		y.append(np.array(ruleIdentifiers).mean())
		x.append(WIDTH)
		#print("{0} {1} {2}".format(RULE, WIDTH, np.array(ruleIdentifiers).mean()))
		
		# for each step in path, how many bits were learned?
		#averageBitsPerPathLength = [bitsKnown[i] / pathLength[i] for i in range(len(bitsKnown))]
		#print("{0} {1} {2}".format(RULE, WIDTH, np.array(averageBitsPerPathLength).mean()))

		#how many bits after n steps?
	
	
	plt.cla()
	plt.plot(x, y, 'o')
	#plt.title("Percentage Of IVs Identifying Rule {0}".format(RULE))
	#plt.xlabel("Width of IVs")
	#plt.ylabel("Percentage of Rule Identifications")
	plt.title("Average Path Length For IVs that Identify Rule {0}".format(RULE))
	plt.xlabel("Width of IVs")
	plt.ylabel("Average Path Length for Rule Identifiers")
	plt.axis([3, 16, 0, 5])
	plt.savefig("./outputs/ruleid/ruleidPathLength_rule{0}.png".format(RULE))

	

