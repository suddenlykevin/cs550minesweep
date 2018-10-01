# Minesweeper Phase I
# Kevin Xie CS550
# On My Honor, I have neither given nor received unauthorized help.

import random # to generate random coordinates with
import sys # to retrieve parameters and to exit if parameters are invalid

try: # to catch invalid inputs (non-integers)
	w,h,b = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
except ValueError:
	print("Please only enter integers for your parameters.")
	sys.exit()

if b>w*h: # to catch if there are more bombs than available coordinates
	print("Please enter a valid number of bombs.")
	sys.exit()

field = [[0]*w for x in range(h)] # fills grid with 0s

for t in range(b): #assigning bombs
	x,y = random.randrange(w),random.randrange(h)
	while field[y][x]=="*": # loop used to avoid redundant placement of bombs over bombs (reducing bomb count)
		x,y = random.randrange(w),random.randrange(h)
	field[y][x]="*"
	z,r = -1,-1
	if x==0: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
		z=0
	if y==0: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
		r=0
	for a in range(z,2,1):
		for b in range(r,2,1): 
			try: # since anything larger than the parameters results in an IndexError
				field[y+b][x+a]+=1
			except: # exceptions for if (x+a,y+b) is out of range or is a bomb.
				pass

for x in range(len(field)): # prints in rows and columns rather than just a long list
	print(*field[x]) # unpacks the list and makes it look grid-like