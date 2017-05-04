# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

from elem_algos import *



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


w_max = 10
w_min = 3

rules = [0,5]

for CLASS in [1,2,3,4]:
	
	y = []
	y_error = []
	y_min = []
	y_max = []
	x = range(w_min,w_max+1)
	
	for WIDTH in x:
	
		cycles = []
		
		for RULE in classes[CLASS]:
		
			CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
			CA.traverse()

			cycles.append( max(CA.cycles) )
			#print(CA.cycles)
			#print(vars)
			print("Class {0} Rule {1} Width {2}".format(CLASS, RULE, WIDTH))

		y.append(np.average(cycles))
		y_error.append(np.std(cycles))
		y_min.append(min(cycles))
		y_max.append(max(cycles))
		
	plt.clf()
	plt.errorbar(x, y, y_error, linestyle='None', marker='^')
	plt.plot(x, y, '-o', label="Average")
	plt.plot(x, y_max, '-+', label="Maximum")
	plt.plot(x, y_min, '-+', label="Minimum")
	plt.legend()
	plt.ylim(ymin=0)
	plt.title("Maximum Cycle Lengths for all Rules in Class {0}".format(CLASS))
	plt.xlabel("Width")
	plt.ylabel("Maximum Cycle Length")
	plt.savefig("./outputs/cycle/W3-10_class{0}.png".format(CLASS))
