# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

from elem_algos import *



####
#
# O(256*width_max-width_min*steps_until_repeat)
#
#
####
RULE = 56

handles = []

for WIDTH in range(7,15):
	
	CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
	CA.traverse()

	vars = stats.itemfreq(CA.cycles)
	print(CA.cycles)
	print(vars)

	plot, = plt.plot(vars[:,0], vars[:,1], 'o', label="Width={0}".format(WIDTH))
	handles.append(plot)

plt.title("Histograms of Cycle Lengths for Rule {0} and Various Widths".format(RULE))
plt.xlabel("Length of cycle")
plt.ylabel("Number of cycles")
plt.legend(handles=handles)
plt.savefig("./outputs/cycleplots/fig.png")
