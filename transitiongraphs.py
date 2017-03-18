# Jordan Perr-Sauer
# For Independent Study, 3/1/2017

import numpy as np
from time import perf_counter as clk
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import pygraphviz as pgv

from elem_algos import *


for RULE in [54, 110]:
	for WIDTH in [14, 15, 16]:
		
		CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
		
		G=pgv.AGraph(directed=True)
		
		cycle = lambda a,b: G.add_edge(str(a), str(b), penwidth = 2, color = "blue")
		tail = lambda a,b: G.add_edge(str(a), str(b), penwidth = 2, color = "red")
		CA.for_each_edge(cycle_edge=cycle, tail_edge=tail)
		
		G.graph_attr['label']='Rule={0} With={1}'.format(RULE, WIDTH)
		G.node_attr['shape']='point'
		G.edge_attr['color']='red'
		G.layout(prog="sfdp")
		G.draw('./t_graphs/bigrun_sfdp_r{0}w{1:02d}.png'.format(RULE, WIDTH))
		print('./t_graphs/bigrun_sfdp_r{0}w{1:02d}.png'.format(RULE, WIDTH))
