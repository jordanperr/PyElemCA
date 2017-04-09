# Jordan Perr-Sauer
# For Independent Study, 4/4/2017

from elem_algos import *
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

# For a given rule and given width, generate average bits for all IVs.



def endless(l, i):
	n = len(l)
	if i >= n:
		return l[n-1]
	else:
		return l[i]


print("Rule | Width   |  % Of IVs Leading To Rule Identification")

for RULE in range(256):
	for WIDTH in [8]:
		ca = ElementaryCA_TransitionGraph(RULE, WIDTH)
		results = []
		for i in range(2**WIDTH):
			iv_result = []
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
				
				bitsKnown = sum([1 if i != None else 0 for i in rule])
				iv_result.append(bitsKnown)
				
				# Check if this state has been visited already
				if next_state in states:
					break
				
				states.add(next_state)
				
				state = next_state
			
			results.append(iv_result)
			
		# now we must average results array
		max_time = 0
		
		for result in results:
			max_time = max(max_time, len(result))
			
		max_time=10
		
		y = []
		for i in range(max_time):
			bits = [endless(r, i) for r in results]
			y.append(np.array(bits).mean())
		
		x = range(1,max_time+1)
		
		print(y)
		plt.cla()
		plt.plot(x, y, 'o')
		plt.title("Average Number of Bits Known Rule {0} Width {1}".format(RULE, WIDTH))
		plt.xlabel("Timestep")
		plt.ylabel("Bits Known")
		plt.axis([1, 12, 5.5, 8])
		plt.savefig("./outputs/ruleid/avgRun/IVAvg_r{0}w{1}.png".format(RULE, WIDTH))
		
		
		# percentage of IVs able to identify rule
		#ruleIdentifiers = sum([1 if bitsKnown[i]==8 else 0 for i in range(len(bitsKnown))])
		#y.append(ruleIdentifiers/len(bitsKnown))
		#x.append(WIDTH)
		#print("{0:3}    {1:2}         {2:<10}".format(RULE, WIDTH, ruleIdentifiers/len(bitsKnown)))
		
		# for IVs with full rule identification, average path length
		#print("{0} {1} {2}".format(RULE, WIDTH, np.array(ruleIdentifiers).mean()))
		
		# for each step in path, how many bits were learned?
		#averageBitsPerPathLength = [bitsKnown[i] / pathLength[i] for i in range(len(bitsKnown))]
		#print("{0} {1} {2}".format(RULE, WIDTH, np.array(averageBitsPerPathLength).mean()))

		#how many bits after n steps?
		

	

