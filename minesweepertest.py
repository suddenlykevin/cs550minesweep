import random
import sys

guess = ""
firstguess = True

try:
	w,h,b = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
except:
	print("Please enter integers for your parameters")
	sys.exit()
if b>=w*h:
	print("Please enter a valid bomb count.")
	sys.exit()

blindfield = [["■"]*w for x in range(h)] # fills grid with ■s and assigns coordinate axes
field = [[0]*w for x in range(h)]

def start():
	global blindfield
	for x in range(2):
		blindfield.insert(0,list(range(1,w+1)))
	blindfield[1]=[x%10 for x in blindfield[1]]
	blindfield[0]=[x//10 for x in blindfield[0]]
	blindfield[0].insert(0,"  ")
	for y in range(h+1):
		if y<10:
			blindfield[y+1].insert(0,"0"+str(y))
		else:
			blindfield[y+1].insert(0,y)
	printField()

def printField():
	global guess
	for x in range(len(blindfield)): # prints in rows and columns rather than just a long list
		print(*blindfield[x]) # unpacks the list and makes it look grid-like
	print("") # proper spacing
	guessCheck()

def revealField():
	for x in range(len(field)): # prints in rows and columns rather than just a long list
		print(*field[x]) # unpacks the list and makes it look grid-like	

def fieldGenerate(initx,inity):
	global w, h, b
	spaces = w*h
	for t in range(b): #assigning bombs
		x,y = random.randrange(w),random.randrange(h)
		if spaces<=9:
			while field[y][x]=="*" or (y==inity-1 and x==initx-1):
				x,y = random.randrange(w),random.randrange(h)
		else:
			while field[y][x]=="*" or ((y==inity-1 or y==inity or y==inity-2) and (x==initx-1 or x==initx or x==initx-2)): # loop used to avoid redundant placement of bombs over bombs (reducing bomb count)
				x,y = random.randrange(w),random.randrange(h)
		field[y][x]="*"
		spaces -= 1
		z,r = -1,-1
		if x==0: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
			z=0
		if y==0: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
			r=0
		for u in range(z,2,1):
			for v in range(r,2,1): 
				try: # since anything larger than the parameters results in an IndexError
					field[y+v][x+u]+=1
				except: # exceptions for if (x+a,y+b) is out of range or is a bomb.
					pass

def choiceOpen(x,y):
	if field[y-1][x-1]==0:
		blindfield[y+1][x]=field[y-1][x-1]
		reveal0(x,y)
	elif field[y-1][x-1]=="*":
		blindfield[y+1][x]="X"
	else:
		blindfield[y+1][x]=field[y-1][x-1]

def reveal0(x,y):
	z,r = -1,-1
	intx,inty=x,y
	# for t in range(100):
	# 	if x==1: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
	# 		z=0
	# 	if y==1: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
	# 		r=0
	# 	for u in range(z,2,1):
	# 		for v in range(r,2,1): 
	# 			try: # since anything larger than the parameters results in an IndexError
	# 				if field[y-1+v][x-1+u]==0:
	# 					blindfield[y+1+v][x+u] = field[y-1+v][x-1+u]
	# 					if x!=1 and y!=1:
	# 						blindfield[y+1+2*v][x+2*u] = field[y-1+2*v][x-1+2*u]
	# 					x,y=x+u,y+v
	# 				else:
	# 					blindfield[y+1+v][x+u] = field[y-1+v][x-1+u]
	# 					x,y=intx,inty
	# 					break
	# 				if x==1: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
	# 					z=0
	# 				if y==1: # so that the "minesweeper number" does not wrap around the grid to -1 -- abs() cannot solve this problem :(
	# 					r=0
	# 			except: # exceptions for if (x+a,y+b) is out of range or is a bomb.
	# 				pass
	for v in range(h-y+1):
		if field[y-1+v][x-1]=="*":
			break
		elif field[y-1+v][x-1]!=0:
			blindfield[y+1+v][x]=field[y-1+v][x-1]
			break	
		for u in range(w-x+1):
			try:
				if field[y-1+v][x-1+u]==0:
					blindfield[y+1+v][x+u]=field[y-1+v][x-1+u]
					blindfield[y+1+v][x+1+u] = field[y-1+v][x+u]
				else:
					break
			except IndexError:
				pass
		for u in range(x-1):
			try:
				if field[y-1+v][x-1-u]==0:
					blindfield[y+1+v][x-u]=field[y-1+v][x-1-u]
					blindfield[y+1+v][x-1-u] = field[y-1+v][x-2-u]
				else:
					break
			except IndexError:
				pass
	for v in range(y-1):
		if field[y-1-v][x-1]=="*":
			break
		elif field[y-1-v][x-1]!=0:
			blindfield[y+1-v][x]=field[y-1-v][x-1]
			break	
		for u in range(w-x+1):
			try:
				if field[y-1-v][x-1+u]==0:
					blindfield[y+1-v][x+u]=field[y-1-v][x-1+u]	
					blindfield[y+1-v][x+1+u] = field[y-1-v][x+u]
				else:
					break
			except IndexError:
				pass
		for u in range(x-1):
			try:
				if field[y-1-v][x-1-u]==0:
					blindfield[y+1-v][x-u]=field[y-1-v][x-1-u]
					blindfield[y+1-v][x-1-u] = field[y-1-v][x-2-u]
				else:
					break
			except IndexError:
				pass


def guessCheck():
	global firstguess
	guess = list(input("Enter coordinates followed by an \"f\" if you would like to flag/unflag it. \nEG: \"2 5 f\"\n>>> ").split()) # splitting a string https://stackoverflow.com/questions/961263/two-values-from-one-input-in-python
	try:
		x,y=int(guess[0]),int(guess[1])
	except ValueError:
		print("Please use integers for x and y in the form \"x y\" separated by a space.")
		guessCheck()
	if (0>=x or x>w) or (0>=y or y>h):
		print("Please enter valid coordinates in the form \"x y\".")
		guessCheck()
	try: # checking if guess[2] exists: https://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists
		guess[2]
		if guess[2] == "f":
			f = True
		else:
			print("Please enter an \"f\" or leave the final argument blank.")
			guessCheck()
	except IndexError:
		f = False
	if f==True:
		if blindfield[y+1][x]==("►"):
			blindfield[y+1][x]=("■")
		elif blindfield[y+1][x]==("■"):
			blindfield[y+1][x]=("►")
		else:
			print("You cannot flag a revealed space. Try somewhere else.")
			guessCheck()
	elif firstguess == True:
		fieldGenerate(x,y)
		firstguess = False
		revealField()
		choiceOpen(x, y)
	else:
		choiceOpen(x,y)
	printField()


start()