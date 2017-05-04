# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

from elem_algos import *




rules = [0,5,30,54,32,142,45,110]
w_max = 14
w_min = 7

rules = [0,5]

for RULE in rules:
	
	plt.clf()
	handles = []
	
	for WIDTH in range(w_min,w_max+1):
		
		CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
		CA.traverse()

		vars = stats.itemfreq(CA.cycles)
		#print(CA.cycles)
		#print(vars)

		plot, = plt.plot(vars[:,0], vars[:,1], 'o', label="Width={0}".format(WIDTH))
		handles.append(plot)

	plt.title("Histograms of Cycle Lengths for Rule {0} and Various Widths".format(RULE))
	plt.xlabel("Length of cycle")
	plt.ylabel("Number of cycles")
	plt.legend(handles=handles)
	plt.xlim(xmin=0)
	plt.ylim(ymin=0)
	if RULE in [5, 0]:
		plt.xlim(xmax = 5)
		plt.ylim(ymax = 1000)
	plt.savefig("./outputs/cycleplots/R{0}_w{1}-{2}.png".format(RULE, w_min, w_max))
