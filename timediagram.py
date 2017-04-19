# Jordan Perr-Sauer
# For Independent Study, 4/16/2017

from PIL import Image, ImageDraw
from random import random
from elem_algos import ElementaryHomogenousCA


# Saves image of a random time diagram to file path output.
# Format is inferred from string in Python Imaging Library

def saveRandomTimeDiagram(rule, steps, width, output, boxwidth=2):
	iv = tuple([1 if random() > 0.5 else 0 for j in range(width)])
	saveTimeDiagram(rule, steps, iv, output, boxwidth)


def saveTimeDiagram(rule, steps, iv, output, boxwidth=2):

	width = len(iv)
	CA = ElementaryHomogenousCA(rule, iv, steps)
	
	im = Image.new("RGB", (width*boxwidth, steps*boxwidth), "white")
	draw = ImageDraw.Draw(im)

	t = 0
	for State in CA:
		xoffset = 0
		for bit in State:
			color = "#000" if bit else "#FFF"
			draw.rectangle([xoffset*boxwidth, t*boxwidth, (xoffset+1)*boxwidth+1, (t+1)*boxwidth+1], color)
			xoffset = xoffset + 1
		t = t+1
	
	im.save(output)


# Command line usage

if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser(description='Generate cellular automata images.')
	parser.add_argument('rule', type=int, help='Wolfram-coded rule for elementary cellular automaton')
	parser.add_argument('width', type=int, help='Width of image in cells')
	parser.add_argument('steps', type=int, help='Height of image in cells')
	parser.add_argument('outfile', help='Output file. Format inferred from extension.')
	args = parser.parse_args()
	
	saveRandomTimeDiagram(args.rule, args.steps, args.width, args.outfile)


