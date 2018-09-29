# Minesweeper Phase I
# Kevin Xie CS550
# On My Honor, I have neither given nor received unauthorized help.

import random # to generate random coordinates with
import sys # to retrieve parameters and to exit if parameters are invalid

try: # to catch invalid inputs (non-integers)
	w=int(sys.argv[1])
	h=int(sys.argv[2])
	b=int(sys.argv[3])
except ValueError:
	print("Please only enter integers for your parameters.")
	sys.exit()

if b>w*h: # to catch if there are more bombs than available coordinates
	print("Please enter a valid number of bombs.")
	sys.exit()

field = [[0]*w for x in range(h)] # fills grid with 0s

for t in range(b): #assigning bombs
	x = random.randrange(w)
	y = random.randrange(h)
	while field[y][x]=="*": # loop used to avoid redundant placement of bombs over bombs (reducing bomb count)
		x = random.randrange(w)
		y = random.randrange(h)
	field[y][x]="*"

for y in range(h): # assigning numbers
	for x in range(w): # goes across all columns in each row
		if field[y][x]=="*":
			if x==0: # so that the "minesweeper number" does not wrap around the grid to -1
				z=0
			else:
				z=-1
			for a in range(z,2,1):
				if y==0: # so that the "minesweeper number" does not wrap around the grid to -1
					r=0
				else:
					r=-1
				for b in range(r,2,1): 
					try: # since anything larger than the parameters results in an IndexError
						if field[y+b][x+a]!="*": # adds 1 everytime a bomb is nearby this non-bomb coordinate
							field[y+b][x+a]+=1
					except IndexError:
						pass

for x in range(len(field)): # prints in rows and columns rather than just a long list
	print(*field[x]) # unpacks the list and makes it look grid-like
