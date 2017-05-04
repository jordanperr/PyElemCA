# Jordan Perr-Sauer
# For Independent Study, 4/4/2017

from elem_algos import *
import numpy as np
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import pickle

# For a given rule and given width, generate average bits for all IVs.



def endless(l, i):
	n = len(l)
	if i >= n:
		return l[n-1]
	else:
		return l[i]


print("Rule | Width   |  % Of IVs Leading To Rule Identification")

x_global = []
y_global = []

for RULE in range(256):
	print(RULE)
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
		
		x_global.append(range(1,max_time+1))
		
		y_global.append(y)
		
		#print(y)
		#plt.cla()
		#plt.plot(x, y, 'o')
		#plt.title("Average Number of Bits Known Rule {0} Width {1}".format(RULE, WIDTH))
		#plt.xlabel("Timestep")
		#plt.ylabel("Bits Known")
		#plt.axis([1, 12, 5.5, 8])
		#plt.savefig("./outputs/ruleid/avgRun/IVAvg_r{0}w{1}.png".format(RULE, WIDTH))
		
		
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
	4: [54,106,110,120,124,137,147,169,193,225]
}


for classno in classes:
	y = []
	y_error = []
	y_max = []
	y_min = []
	trendlines = [y_global[i] for i in classes[classno]]
	for i in range(len(trendlines[0])):
		values = [j[i] for j in trendlines]
		y.append(np.array(values).mean())
		y_min.append(min(values))
		y_max.append(max(values))
		y_error.append(np.std(values))
		
	plt.cla()

	plt.errorbar(x_global[0], y, y_error, linestyle='None', marker='^')
	plt.plot(x_global[0], y, '-o', label="Average")
	plt.plot(x_global[0], y_max, '-+', label="Maximum")
	plt.plot(x_global[0], y_min, '-+', label="Minimum")
	plt.legend()
	plt.ylim(ymin=0)
	plt.axis([1, 12, 5.5, 8])
	plt.title("Average Number of Bits Known Per Iteration Class {0} Width {1}".format(classno, 8))
	plt.xlabel("Timestep")
	plt.ylabel("Bits Known")
	plt.savefig("./outputs/ruleid/avg_width8_class{0}.png".format(classno))
	
	#plt.cla()
	#plt.plot(x_global[0], y_max, '+', label="Maximum")
	#plt.plot(x_global[0], y, '-o', label="Average")
	#plt.plot(x_global[0], y_min, '+', label="Minimum")
	#plt.legend()
	#plt.axis([1, 12, 5.5, 8])
	#plt.title("Average Number of Bits Known Per Iteration Class {0} Width {1}".format(classno, 8))
	#plt.xlabel("Timestep")
	#plt.ylabel("Bits Known")
	#plt.savefig("./outputs/ruleid/avg_width8_class{0}.png".format(classno))
	
	

