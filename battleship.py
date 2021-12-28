"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["boardsize"]=500
    data["cellsize"]=data["boardsize"]/data["rows"]
    data["userboard"]=emptyGrid(data["rows"],data["cols"])
    data["computerboard"]=emptyGrid(data["rows"],data["cols"])
    data["numberofShips"]=5
    data["computerboard"]=addShips(data["computerboard"],data["numberofShips"])
    data["temporaryShips"]=[]
    data["userships"]=0
    data["winner"]=None
    data["currentturns"]=0
    data["maxturns"]=50
    

    return data


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["userboard"],True)
    drawGrid(data,compCanvas,data["computerboard"],False)
    drawShip(data,userCanvas,data["temporaryShips"])
    
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    return
       


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"]!=None:
        return None
    row,col=getClickedCell(data, event)
    if board=="user":
        clickUserBoard(data, row, col)
    if board=="comp":
        runGameTurn(data, row, col)
  

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    a=[]
    for i in range(rows):
        b=[]
        for j in range(cols):
            b.append(EMPTY_UNCLICKED)
        a.append(b)
    return a


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    r=random.randint(1,8)
    c=random.randint(1,8)
    b=random.randint(0,1)
    if b == 0:
        ship=[[r-1,c],[r,c],[r+1,c]]
    else:
        ship=[[r,c-1],[r,c],[r,c+1]]
    return ship
print(createShip());


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in range(len(ship)):
        if grid[ship[i][0]][ship[i][1]]!=EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    a=0
    while a<numShips*3:
        b=createShip()
        c=checkShip(grid, b)
        if c == True:
            for j in b:
                grid[j[0]][j[1]] = 2
                a=a+1
    return grid;


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["rows"]):
         for cols in range(data["cols"]):
             if grid[row][cols]==SHIP_UNCLICKED:
                 if showShips:
                     canvas.create_rectangle(cols*data["cellsize"],row*data["cellsize"],data["cellsize"]+cols*data["cellsize"], row*data["cellsize"]+data["cellsize"], fill="yellow")
                 else:
                     canvas.create_rectangle(cols*data["cellsize"],row*data["cellsize"],data["cellsize"]+cols*data["cellsize"], row*data["cellsize"]+data["cellsize"], fill="blue")
             elif grid[row][cols]==SHIP_CLICKED:
                 canvas.create_rectangle(cols*data["cellsize"],row*data["cellsize"],data["cellsize"]+cols*data["cellsize"], row*data["cellsize"]+data["cellsize"], fill="red")
             elif grid[row][cols]==EMPTY_CLICKED:
                 canvas.create_rectangle(cols*data["cellsize"],row*data["cellsize"],data["cellsize"]+cols*data["cellsize"], row*data["cellsize"]+data["cellsize"], fill="white")
             else:
                 canvas.create_rectangle(cols*data["cellsize"],row*data["cellsize"],data["cellsize"]+cols*data["cellsize"], row*data["cellsize"]+data["cellsize"], fill="blue")
    return 


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    row=0
    if ship[row][1]==ship[row+1][1]==ship[row+2][1]:
        ship.sort()
        if ship[row+1][0]-ship[row][0]==1 and ship[row+2][0]-ship[row+1][0]==1:
            return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    col=0
    if ship[col][0]==ship[col+1][0]==ship[col+2][0]:
        ship.sort()
        if ship[col+1][1]-ship[col][1]==1 and ship[col+2][1]-ship[col+1][1]==1:
            return True
    return False

'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    a=data["cellsize"]
    return [int(event.y/a),int(event.x/a)]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in ship:
        row=i[0]
        cols=i[1]
        canvas.create_rectangle(cols*data["cellsize"],row*data["cellsize"],data["cellsize"]+cols*data["cellsize"], row*data["cellsize"]+data["cellsize"], fill="white")



'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid, ship):
        if (isVertical(ship)==True or isHorizontal(ship)==True):
            return True
    return False
    


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    a=data["userboard"]
    if shipIsValid(a, data["temporaryShips"]):
        for i in data["temporaryShips"]:
            a[i[0]][i[1]]=SHIP_UNCLICKED
        data["userships"]=data["userships"]+1
    else:
        print("Ship is not Valid")
    data["temporaryships"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    b=data["userboard"]
    if [row,col] in b or data["userships"]==5:
        return
    data["temporaryShips"].append([row,col])
    if len(data["temporaryShips"])==3:
        placeShip(data)
        data["temporaryShips"]=[]
    if data["userships"]==5:
        print("You can start the game")
    return



### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
    else:
        board[row][col]==EMPTY_UNCLICKED
        board[row][col]=EMPTY_CLICKED

    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    z=data["computerboard"]
    if z[row][col]==SHIP_CLICKED or z[row][col]==EMPTY_CLICKED:
        return
    else:
        updateBoard(data, z, row, col, "user")
    [r,c]=getComputerGuess(data["userboard"])
    updateBoard(data,data["userboard"], r, c,"comp")
    data["currentturns"]=data["currentturns"]+1
    if (data["currentturns"]==data["maxturns"]):
        data["winner"]="draw"

        
    


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    randomrowvalue = random.randint(0,9)
    randomcolvalue = random.randint(0,9)
    while (board[randomrowvalue][randomcolvalue]== SHIP_CLICKED) or (board[randomrowvalue][randomcolvalue]== EMPTY_CLICKED):
        randomrowvalue = random.randint(0,9)
        randomcolvalue = random.randint(0,9)
    return [randomrowvalue,randomcolvalue]

  


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if (data["winner"]=="user"):
        canvas.create_text(250,150, text="CONGRACTULATIONS", fill="gold",font=("Arial","24","bold italic"))
        canvas.create_text(250,250, text="PRESS ENTER IF U WANT TO PLAY AGAIN", fill="black",font=("Arial","16","bold italic"))
    if (data["winner"]=="comp"):
        canvas.create_text(250,150, text="YOU LOSE", fill="brown",font=("Arial","24","bold italic"))
        canvas.create_text(250,250, text="PRESS ENTER IF U WANT TO PLAY AGAIN", fill="black",font=("Arial","16","bold italic"))
    if (data["winner"]=="draw"):
        canvas.create_text(250,150, text="OUT OF MOVES", fill="silver",font=("Arial","24","bold italic"))
        canvas.create_text(250,250, text="PRESS ENTER IF U WANT TO PLAY AGAIN", fill="black",font=("Arial","16", "bold italic"))

        canvas.pack()

    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    
    
    
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)