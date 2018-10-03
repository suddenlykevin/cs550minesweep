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
	for t in range(b): #assigning bombs
		x,y = random.randrange(w),random.randrange(h)
		if ((inity-1==0 or inity-1==h) and (initx-1==0 or initx-1==w) and w*h-b<4) or ((inity-1==0 or initx-1==0 or inity-1==h or initx-1==w) and w*h-b<6) or (inity-1!=0 and inity-1!=h and initx-1!=0 and initx-1!=w and w*h-b<9):
			while field[y][x]=="*" or (y==inity-1 and x==initx-1):
				x,y = random.randrange(w),random.randrange(h)
		else:
			while field[y][x]=="*" or ((y==inity-1 or y==inity or y==inity-2) and (x==initx-1 or x==initx or x==initx-2)): # loop used to avoid redundant placement of bombs over bombs (reducing bomb count)
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

def guessCheck():
	global firstguess
	guess = list(input("Enter coordinates followed by an \"f\" if you would like to flag/unflag it. \nEG: \"2 5 f\"\n>>> ").split())
	try:
		x,y=int(guess[0]),int(guess[1])
	except ValueError:
		print("Please use integers for x and y in the form \"x y\" separated by a space.")
		guessCheck()
	if (0>x or x>w) or (0>y or y>h):
		print("Please enter valid coordinates in the form \"x y\".")
		guessCheck()
	try:
		guess[2]
		if guess[2] == "f":
			f = True
		else:
			print("Please enter an \"f\" or leave the final argument blank.")
			guessCheck()
	except IndexError:
		f = False
	if firstguess == True:
		if f == True:
			print("You cannot flag your first coordinate. Generating field...")
		fieldGenerate(x,y)
		firstguess = False
		revealField()

start()