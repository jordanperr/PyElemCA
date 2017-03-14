# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib.pyplot as plt
from scipy import stats
import pygraphviz as pgv

from elem_algos import *


for RULE in [110, 19, 0, 78, 20, 30, 105, 54]:
	for WIDTH in [3,4,5,6,7,8,9,10,11]:
		
		CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
		
		G=pgv.AGraph(directed=True)
		
		cycle = lambda a,b: G.add_edge(str(a), str(b), penwidth = 5, color = "blue")
		tail = lambda a,b: G.add_edge(str(a), str(b), penwidth = 5, color = "red")
		CA.for_each_edge(cycle_edge=cycle, tail_edge=tail)
		
		G.graph_attr['label']='Rule={0} With={1}'.format(RULE, WIDTH)
		G.node_attr['shape']='point'
		G.edge_attr['color']='red'
		G.layout()
		G.draw('./t_graphs/bigrun_r{0}w{1:02d}.png'.format(RULE, WIDTH))
		print('./t_graphs/bigrun_r{0}w{1:02d}.png'.format(RULE, WIDTH))
