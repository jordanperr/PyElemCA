# Jordan Perr-Sauer
# For Independent Study, 4/16/2017

from PIL import Image, ImageDraw
from random import random
from elem_algos import *

IV = (1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0)

IV = tuple([1 if random() > 0.5 else 0 for j in range(1000)])

IV = tuple([1 if j==499 else 0 for j in range(500)])

RULE = 110
STEPS = 500

BOXWIDTH = 2 #pixels




width = len(IV)

CA = ElementaryCA_TransitionGraph(RULE, width)

im = Image.new("RGB", (width*BOXWIDTH, STEPS*BOXWIDTH), "white")
draw = ImageDraw.Draw(im)

State = IV
for t in range(STEPS):
	xoffset = 0
	for bit in State:
		color = "#000" if bit else "#FFF"
		draw.rectangle([xoffset*BOXWIDTH, t*BOXWIDTH, (xoffset+1)*BOXWIDTH+1, (t+1)*BOXWIDTH+1], color)
		xoffset = xoffset + 1
	State = CA.elem_step(State)

im.save("./outputs/ca-img.png")
