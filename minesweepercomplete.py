# minesweeper
# by Kevin Xie
# CS550 Healey
#
# A game of minesweeper programmed using 2D lists, recursion, and functions.
# Organized with comments (can be condensed further)
#
# Sources:
# splitting a string https://stackoverflow.com/questions/961263/two-values-from-one-input-in-python
# checking if list entry exists: https://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists
# space opening method inspired by Anan Aramthanapon
# 
# On My Honor, I have neither given nor received unauthorized aid.
# Kevin Xie

import random # for placing bombs
import sys # used for initial arguments

try: # authenticate that all entered arguments are valid integers
	w,h,b = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
except:
	print("Please enter integers for your parameters")
	sys.exit()
if b>=w*h: # checks if bombs can be generated within the given parameters
	print("Please enter a valid bomb count.")
	sys.exit()

def start(): # sets up starting variables and axes
	global blindfield, firstguess, field, spacesleft
	# VARIABLE SETUP
	firstguess = True # if firstguess is true, the bombs have not been placed yet
	blindfield = [["■"]*w for x in range(h)] # fills grid with ■s and assigns coordinate axes
	field = [[0]*w for x in range(h)] # fills solution set with 0s
	spacesleft = w*h-b # the number of unrevealed spaces (used to calculate victory)
	# X AXIS
	for x in range(2): # next lines add variable x and y axes to the blind grid for more comfortable UX
		blindfield.insert(0,list(range(1,w+1))) 
	blindfield[0]=[x//10 for x in blindfield[0]] # x axis is vertical to maintain correct monospacing (first digit above second digit)
	blindfield[1]=[x%10 for x in blindfield[1]]
	blindfield[0].insert(0,"  ")
	# Y AXIS
	for y in range(h+1):
		if y<10:
			blindfield[y+1].insert(0,"0"+str(y))
		else:
			blindfield[y+1].insert(0,y)
	printField()

def printField(): # prints the blind grid with revealed spaces
	print("\n")
	for x in range(len(blindfield)): # prints in rows and columns rather than just a long list
		print(*blindfield[x]) # unpacks the list and makes it look grid-like
	print("") # proper spacing
	guessCheck()

def fieldGenerate(initx,inity): # places the bombs once first space is revealed
	spaces = w*h # the number of non-bomb spaces left
	for t in range(b): # assigning the correct # bombs
		x,y = random.randrange(w),random.randrange(h)
		if spaces<=9: # prioritizes the selected space to be 0 unless there are fewer than 9 spaces left, which helps the reveal of more spaces on first step.
			while field[y][x]=="*" or (y==inity-1 and x==initx-1):
				x,y = random.randrange(w),random.randrange(h)
		else:
			while field[y][x]=="*" or ((y==inity-1 or y==inity or y==inity-2) and (x==initx-1 or x==initx or x==initx-2)): # bombs are placed outside a radius of two of the guess
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

def choiceOpen(x,y): # opens the space based on coordinates entered (if zero, then reveal more; if bomb, then lose)
	global spacesleft
	if field[y-1][x-1]==0: # if the corresponding solution set space is a 0, then commence expanding reveal
		blindfield[y+1][x]=field[y-1][x-1]
		spacesleft-=1
		reveal0(x,y)
	elif field[y-1][x-1]=="*": # if the solution coordinate is a bomb, the game ends
		blindfield[y+1][x]="▲"
		loseGame()
	else: # if the corresponding solution set space is a number, then space is revealed
		blindfield[y+1][x]=field[y-1][x-1]
		spacesleft-=1
	winCheck()

def reveal0(x,y): # the "forest fire" effect of revealing touching 0s recursively
	global spacesleft
	for u in range(-1,2,1):
		for v in range(-1,2,1): 
			try: # since anything larger than the parameters results in an IndexError
				if field[y-1+v][x-1+u]==0 and blindfield[y+1+v][x+u]=="■": # opens up all surrounding spaces if selected space ==0
					blindfield[y+1+v][x+u] = field[y-1+v][x-1+u]
					spacesleft-=1 
					reveal0(x+u,y+v) # loops if contiguous space is 0
				else:
					if blindfield[y+1+v][x+u]=="■":
						blindfield[y+1+v][x+u] = field[y-1+v][x-1+u]
						spacesleft-=1
			except: # exceptions for if (x+a,y+b) is out of range or is a bomb.
				pass

def guessCheck(): # asks for user to guess/flag and acts accordingly
	global firstguess
	guess = list(input("Enter coordinates followed by an \"f\" if you would like to flag/unflag it. \nEG: \"2 5 f\"\n>>> ").split()) # splitting a string https://stackoverflow.com/questions/961263/two-values-from-one-input-in-python
	# X AND Y
	try: # authenticates that x and y are integers and do exist. checking if guess[x] exists: https://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists
		x,y=int(guess[0]),int(guess[1])
	except ValueError:
		print("Please use integers for x and y in the form \"x y\" separated by a space.")
		guessCheck()
	except IndexError:
		print("Please enter x and y in the form \"x y\" separated by a space.")
		guessCheck()
	if (0>=x or x>w) or (0>=y or y>h): # checks if coordinates are within height and width
		print("Please enter valid coordinates in the form \"x y\".")
		guessCheck()
	# FLAG TOGGLE
	try: # checks if user wants to flag
		guess[2]
		if guess[2] == "f":
			if blindfield[y+1][x]=="►":
				blindfield[y+1][x]="■"
			elif blindfield[y+1][x]=="■":
				blindfield[y+1][x]="►"
			else:
				print("You cannot flag a revealed space. Try somewhere else.")
				guessCheck()
		else:
			print("Please enter an \"f\" or leave the final argument blank.")
			guessCheck()
	except IndexError: # if flag is null, then don't flag and continue to look for options
	# REVEALS
		if blindfield[y+1][x]=="►":
			print("You cannot reveal a flagged space. Try somewhere else.") 
			guessCheck()
		elif firstguess == True: # drops bombs and reveals space on first guess
			fieldGenerate(x,y)
			firstguess = False
			choiceOpen(x, y)
		else:
			choiceOpen(x,y)
	printField()

def winCheck(): # if the spaces that remain is equal to the number of bombs placed, then player wins
	if spacesleft == 0:
		for y in range(h):
			for x in range(w):
				if blindfield[y+2][x+1]=="■" or blindfield[y+2][x+1]=="►":
					blindfield[y+2][x+1]="☻"
		print("\n")
		for x in range(len(blindfield)): # prints in rows and columns rather than just a long list
			print(*blindfield[x]) # unpacks the list and makes it look grid-like
		print("\nYOU WIN ☺!\n\n") # proper spacing
		restart()

def loseGame(): # loss of game (reveal formatted solution set)
	for y in range(h):
			for x in range(w):
				if blindfield[y+2][x+1]=="■": 
					blindfield[y+2][x+1]=field[y][x]
				elif blindfield[y+2][x+1]=="►" and field[y][x]!="*":
					blindfield[y+2][x+1]="≠"
				elif blindfield[y+2][x+1]=="►":
					blindfield[y+2][x+1]="☻"
	print("\n")
	for x in range(len(blindfield)): # prints in rows and columns rather than just a long list
			print(*blindfield[x]) # unpacks the list and makes it look grid-like
	print("\nYOU LOSE... \n\n") # proper spacing
	restart()

def restart(): # function for restarting or exiting the program
	reYes = input("Would you like to play again? (y/n) \n\n>>> ").lower()
	if reYes == "y": # everything reset
		start()
	elif reYes == "n": # os.exit from program
		sys.exit()
	else:
		print("Please enter either \"y\" or \"n\".")
		restart()

start()