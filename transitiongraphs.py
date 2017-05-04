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

labels = True

for RULE in range(168,169):
	for WIDTH in range(5,6):
		
		CA = ElementaryCA_TransitionGraph(RULE, WIDTH)
		
		G=pgv.AGraph(directed=True)
		
		cycle = lambda a,b: G.add_edge(str(a), str(b), penwidth = 1, color = "blue")
		tail = lambda a,b: G.add_edge(str(a), str(b), penwidth = 1, color = "red")
		CA.for_each_edge(cycle_edge=cycle, tail_edge=tail)
		
		G.graph_attr['label']='Rule={0} With={1}'.format(RULE, WIDTH)
		G.node_attr['shape']='point'
		G.edge_attr['color']='red'
		
		if labels:
			G.node_attr['labelloc']='t'
			G.edge_attr['dir']='back'
			G.edge_attr['arrowtail']='invempty'
			
			for node in G.nodes():
				#print(str(node))
				G.get_node(node).attr['xlabel'] = str(node)
				G.get_node(node).attr['fontsize'] = 10
		
		G.layout()
		G.draw('./outputs/t_graphs/labeled_tgraphs_sfdp_r{0}w{1:02d}.png'.format(RULE, WIDTH))
		print('./outputs/t_graphs/labeled_tgraphs_sfdp_r{0}w{1:02d}.png'.format(RULE, WIDTH))
