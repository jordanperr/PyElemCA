# Jordan Perr-Sauer
# For Independent Study, 4/16/2017

from PIL import Image, ImageDraw
from random import random, seed
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
			draw.rectangle(
				[xoffset*boxwidth, t*boxwidth, (xoffset+1)*boxwidth+1, (t+1)*boxwidth+1],
				color)
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
	parser.add_argument('--initial', help='Initial state of cellular automata ex. 1100110')
	parser.add_argument('--outfile', help='Output file. Format inferred from extension.')
	parser.add_argument('--cellw', type=int, help='Width of each cell in pixels.')
	parser.add_argument('--seed', type=int, help='Set the seed of PRNG.')
	args = parser.parse_args()
	
	if args.seed:
		seed(args.seed)
	
	
	if args.initial:
		iv = tuple([ int(i) for i in args.initial])
		if args.cellw:
			saveTimeDiagram(args.rule, args.steps, iv, args.outfile, args.cellw)
		else:
			saveTimeDiagram(args.rule, args.steps, iv, args.outfile)
	else:
		print(args.width)
		if args.cellw:
			saveRandomTimeDiagram(args.rule, args.steps, args.width, args.outfile, args.cellw)
		else:
			saveRandomTimeDiagram(args.rule, args.steps, args.width, args.outfile)
	


