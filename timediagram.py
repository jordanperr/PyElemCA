# Jordan Perr-Sauer
# For Independent Study, 4/16/2017

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from elem_algos import *

RULE = 110
WIDTH = 8
TMAX = 8

CA = ElementaryCA_TransitionGraph(RULE, WIDTH)

fig = plt.figure()
ax = fig.add_subplot(111)
for t in range(TMAX):
	if t == 0:
		State = (1, 0, 0, 1, 1, 0, 1, 0)
	xoffset = 0
	for bit in State:
		ax.add_patch(
    	patches.Rectangle(
        	(xoffset, t),   # (x,y)
        	1,          # width
        	1,          # height
        	edgecolor="none",
        	facecolor="black" if bit==1 else "white"
    		)
		)
		xoffset = xoffset + 1
	State = CA.elem_step(State)
ax.set_ylim([0,8])
ax.set_xlim([0,8])
fig.savefig('./outputs/ca.png')
