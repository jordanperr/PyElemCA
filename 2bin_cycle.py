# Jordan Perr-Sauer
# For Independent Study, 4/26/2017

import numpy as np
from time import perf_counter as clk
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.cluster import KMeans
from pickle import dump
from random import random
from elem_algos import *





rules = range(256)

WIDTH = 7

# Compute max cycle lengths for all rules of certain width
mcl = []
for RULE in rules:
	CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
	CA.traverse()
	mcl.append(max(CA.cycles))
	#cyclefreq = stats.itemfreq(CA.cycles)
	#print(cyclefreq[:,1])
	#mcl.append([max(CA.cycles), max(cyclefreq[:,1])])


# Load classes into memory
# from wolframalpha.com
classes = {
	1: [0,8,32,40,64,96,128,136,160,168,192,224,234,235,238,239,248,249,250,251,252,253,
		254,255],
	2: [1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,19,20,21,23,24,25,26,27,28,29,31,33,34,35,
		36,37,38,39,41,42,43,44,46,47,48,49,50,51,52,53,55,56,57,58,59,61,62,63,65,66,67,
		68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,87,88,91,92,93,94,95,97,98,99,
		100,103,104,107,108,109,111,112,113,114,115,116,117,118,119,121,123,125,127,130,
		131,132,133,134,138,139,140,141,142,143,144,145,148,152,154,155,156,157,158,159,
		162,163,164,166,167,170,171,172,173,174,175,176,177,178,179,180,181,184,185,186,187,
		188,189,190,191,194,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,
		211,212,213,214,215,216,217,218,219,220,221,222,223,226,227,228,229,230,231,232,233,
		236,237,240,241,242,243,243,244,245,246,247],
	3: [18,22,30,45,60,75,86,89,90,101,102,105,122,126,129,135,146,149,150,151,153,161,
		165,182,183,195],
	4: [54,106,110,120,124,137,147,169,193,225]
}

# We need a way to "reverse lookup" class number for a rule
def class_of_rule(rule):
	for cl in classes.keys():
		if rule in classes[cl]:
			return cl
	
# We need a way to measure the fitness of a split value
def fitness(split):
	scores = []
	for cl in classes.keys():
		for rule in classes[cl]:
			predicted_class = mcl[rule] >= split
			actual_class = cl > 2
			scores.append(1 if predicted_class == actual_class else 0)
	#print (scores)
	return sum(scores) / (len(scores)+0.0)
	#predictors = [1 if i > split else 0 for i in mcl]
	#fitness = [predictors[i] == ((i in classes[3]) or (i in classes[4])) for i in range(256)]
	#return (sum(fitness) / (len(fitness)+0.0))

# Graph the fitness
X = np.linspace(min(mcl), max(mcl), 200)
Y = [fitness(x) for x in X]

baseline = (len(classes[1]) + len(classes[2])) / 256.0
plt.plot(X,Y,'b')
plt.plot(X,[baseline for x in X],'g')

print("Maximum fitness: {0}".format(max(Y)))
print("Baseline fitness: {0}".format(baseline))
print("Improvement: {0}".format((max(Y)-baseline)/(1-baseline)))
	
plt.axis([min(X), max(X), 0, 1])
plt.ylabel('Accuracy in 2-Bin Classification')
plt.xlabel('Critical Cycle Length')
plt.title('Cycle Pivot, 2-Bin Classification, Width {0}'.format(WIDTH))
plt.savefig('outputs/2bin_cycle_{0}.png'.format(WIDTH))


#X = [mcl[i][0] for i in range(256)]
#Y = [mcl[i][1] for i in range(256)]

#for i in classes[2]:
#	plt.scatter(X[i],Y[i], marker = '+')
#for i in classes[3]:
#	plt.scatter(X[i],Y[i], marker = '*')

#plt.show()

#reshaped = np.array(mcl).reshape(-1, 1)

#kmeans = KMeans(n_clusters=2, random_state=0).fit(reshaped)
#kmeans.predict(reshaped)


