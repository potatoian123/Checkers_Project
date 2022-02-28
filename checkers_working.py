import tkinter as tk
import math as m

"""
===============================================================================
ENGR 13300 Fall 2021

Program Description
    Code for checkers game

Assignment Information
    Assignment:     Individual Project
    Author:         Ian Quan, iquan@purdue.edu
    Team ID:        LC5 - 03 (e.g. LC1 - 01; for section LC1, team 01)

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

class Cons():
    """
    Class holding constants that are used to create the game

    Args:
        None

    Returns:
        None

    Raises:
        None

    """

    BOARD_SIZE = 400
    ROWS_FILLED = 3
    NUM_SQUARES = 8
    SQUARE_SIZE = BOARD_SIZE/NUM_SQUARES
    PIECE_SIZE = int(0.8 * SQUARE_SIZE)
    PIECE_BORDER = 5
    DARK_SQUARE_COLOR = 'black'
    LIGHT_SQUARE_COLOR = 'white'
    DARK_PIECE_COLOR = 'black'
    LIGHT_PIECE_COLOR = 'red'

class Game:
    """
    Class that stores one instance of the game.

    Creates all game objects and provides code to run the game to completion.

    Args:
        None

    Returns:
        None

    Raises:
        None

    """

    def __init__(self):
        """
        Initilizes one instance of game

        Args:
            self

        Returns:
            None

        Raises:
            None

        """

        self.gamePieceLocation = [[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,2,0,2,0,2,0,2],[2,0,2,0,2,0,2,0],[0,2,0,2,0,2,0,2]] #pre initilization of gameboard
        self.game = tk.Tk() #makes tkinter object
        self.game.attributes('-topmost',True)
        self.game.title('Checkers') #titles window
        self.game.geometry(f'{Cons.BOARD_SIZE}x{Cons.BOARD_SIZE}+100+100') #sets size
        self.game.resizable(0,0) #makes game not resizable, as I don't know how to have dynamic piece adjustment
        self.gameframe = tk.Frame(self.game)
        self.gameframe.pack()
        self.gameCanvas = tk.Canvas(self.gameframe,width = Cons.BOARD_SIZE,height = Cons.BOARD_SIZE)
        board = Board(self.gameCanvas)
        board.initBoard()
        self.drawPieces()
        self.playerTurn = 2 #red goes first
        self.checkerSelected = False
        self.gameCanvas.bind('<Button-1>', self.mouseClicked) #attatches mouseclick to canvas object

    def drawPieces(self):
        """
        Draws pieces as they exist in the game array

        Args:
            self

        Returns:
            None

        Raises:
            None

        """

        self.initPieces()
        for row in self.gamePieceLocation:
            for col in row:
                if(col != 0):
                    col.initPiece()

    def initPieces(self):
        """
        Creates piece objects and places their coordinates in the correct starting position using a formula to calcualulate in which location of the board should a piece go. It also updates the game array to have pieces in the correct row and column.

        Args:
            self

        Returns:
            None

        Raises:
            None

        """
        pieceCanvas = self.gameCanvas
        #The lambda functions below defines a way for the correct location of dark piece and light pieces to be placed at theb eginning of the game.
        darkCoord = lambda row,index,border: ((2*index + row % 2)*Cons.SQUARE_SIZE + Cons.PIECE_SIZE - border * Cons.PIECE_BORDER, row * Cons.SQUARE_SIZE + Cons.PIECE_SIZE - border * Cons.PIECE_BORDER,(2*index + 1 + row % 2)*Cons.SQUARE_SIZE - Cons.PIECE_SIZE + border * Cons.PIECE_BORDER, (row + 1) * Cons.SQUARE_SIZE - Cons.PIECE_SIZE + Cons.PIECE_BORDER * border)
        lightCoord = lambda row,index,border: ((2 * index + 1 - row % 2) * Cons.SQUARE_SIZE + Cons.PIECE_SIZE - border * Cons.PIECE_BORDER, Cons.BOARD_SIZE - (row + 1) * Cons.SQUARE_SIZE + Cons.PIECE_SIZE - border * Cons.PIECE_BORDER, (2 * index + 2 - row % 2) * Cons.SQUARE_SIZE - Cons.PIECE_SIZE + border * Cons.PIECE_BORDER, Cons.BOARD_SIZE - row * Cons.SQUARE_SIZE - Cons.PIECE_SIZE + border * Cons.PIECE_BORDER)
        for i in range(int(Cons.NUM_SQUARES / 2)):
            for row in range(Cons.ROWS_FILLED):
                #an instance of DarkPiece adn LightPiece are created using the values generated by the for loops
                darkpiece = DarkPiece(*darkCoord(row,i,0),pieceCanvas,self.gamePieceLocation)
                lightpiece = LightPiece(*lightCoord(row,i,0),pieceCanvas,self.gamePieceLocation)
                #These update the game array with the correct piece in the correct location
                self.gamePieceLocation[darkpiece.rowLoc][darkpiece.colLoc] = darkpiece
                self.gamePieceLocation[lightpiece.rowLoc][lightpiece.colLoc] = lightpiece

    def delPiece(self,row,col):
        """
        deletes piece at given row and column from game array

        Args:
            int row: given row at which to delete
            int col: given column at which to delete

        Returns:
            None

        Raises:
            None

        """
        piece = self.gamePieceLocation[row][col] #pulls piece from array to reference
        piece.deleteFromArr() #removes piece address from array
        piece.undraw() #removes canvas object tied to piece from the GUI canvas

    def getLocation(self,x0,y0):
        """
        returns location in row and column terms from x and y coord of window location

        Args:
            int x0: x coordinate to find location of
            int y0: y coordinate to find location of

        Returns:
            tuple: row,col

        Raises:
            None

        """
        #chekcs x and y coordinate of piece and sees which coorspoiding row and column the piece is in using very simple logic comparison
        if(y0 <= 50):
            row = 0
        elif(y0 <= 100):
            row = 1
        elif(y0 <= 150):
            row = 2
        elif(y0 <= 200):
            row = 3
        elif(y0 <= 250):
            row = 4
        elif(y0 <= 300):
            row = 5
        elif(y0 <= 350):
            row = 6
        else:
            row = 7
        if(x0 <= 50):
            col = 0
        elif(x0 <= 100):
            col = 1
        elif(x0 <= 150):
            col = 2
        elif(x0 <= 200):
            col = 3
        elif(x0 <= 250):
            col = 4
        elif(x0 <= 300):
            col = 5
        elif(x0 <= 350):
            col = 6
        else:
            col = 7
        return row,col

    def mouseClicked(self,event):
        """
        callback function that executes when mouse is clicked

        Args:
            event: event when mouse is clicked on canvas

        Returns:
            None

        Raises:
            None

        """
        mouseRow,mouseCol = self.getLocation(event.x,event.y) #gets location of where mouse was clicked and determines which row and column it coorsponds to in the game array
        if self.checkerSelected == False: #if no checker selected, selects a checker and draws possible moves
            if self.gamePieceLocation[mouseRow][mouseCol].__class__.__name__ == 'DarkPiece' and self.playerTurn == 1: #if is black players turn and a valid checker is selected
                piece = self.gamePieceLocation[mouseRow][mouseCol] #gtets clicked piece from array
                #changes piece and draws possible moves
                piece.checkerSelected()
                piece.drawMoves()
                self.checkerSelected = piece
            elif self.gamePieceLocation[mouseRow][mouseCol].__class__.__name__ == 'LightPiece' and self.playerTurn == 2: #similar to above, except for red player's turn
                piece = self.gamePieceLocation[mouseRow][mouseCol]
                piece.checkerSelected()
                piece.drawMoves()
                self.checkerSelected = piece
        else: #if there is a checker selected
            leftRow,leftCol,rightRow,rightCol = None,None,None,None
            #makes sure that only valid moves can be clicked, and error not thrown if one move is not drawn
            if(self.checkerSelected.leftMove):
                leftRow = self.checkerSelected.leftMove.rowLoc
                leftCol = self.checkerSelected.leftMove.colLoc
            if(self.checkerSelected.rightMove):
                rightRow = self.checkerSelected.rightMove.rowLoc
                rightCol = self.checkerSelected.rightMove.colLoc
            if ((self.checkerSelected.leftMove) and (mouseRow == leftRow and mouseCol == leftCol)) or ((self.checkerSelected.rightMove) and (mouseRow == rightRow and mouseCol == rightCol)): #if a possible move is selected, moves piece
                if leftRow != None and leftCol != None and mouseRow == leftRow and mouseCol == leftCol: #if the left move is selected
                    #gets coordinates of new position to move
                    placetomove = self.checkerSelected.leftMove.getCoords()
                    placemove = self.checkerSelected.leftMove
                elif rightRow != None and rightCol != None and mouseRow == rightRow and mouseCol == rightCol: #same thing but for the right move
                    placetomove = self.checkerSelected.rightMove.getCoords()
                    placemove = self.checkerSelected.rightMove
                self.checkerSelected.moveChecker(*placetomove) #moves checker and code below updates game array
                self.gamePieceLocation[mouseRow][mouseCol] = self.checkerSelected
                self.checkerSelected.deleteFromArr()
                self.checkerSelected.updateCoords(mouseRow,mouseCol,*placetomove)
                self.gameCanvas.delete('Take') #deletes possible move items from the canvas
                if(placemove.takePiece == 1): #if a piece was taken during the move
                    self.delPiece(placemove.coordskippedR,placemove.coordSkippedC) #updates game array and deletes taken checker from GUI
                self.checkerSelected.leftMove = None #resets checker moves back to None
                self.checkerSelected.rightMove = None
                self.checkerSelected.checkerDeselected() #deselects checker after move is completed
                self.continueGame() #continues game by changing turns
            else: #deselects checker, allows new checker to be selected
                self.checkerSelected.checkerDeselected()
                if self.checkerSelected.leftMove != None: #removes left move if a left move was generated
                    self.checkerSelected.leftMove.deleteFromArr()
                    self.gameCanvas.delete(self.checkerSelected.leftMove)
                    self.checkerSelected.leftMove = None
                if self.checkerSelected.rightMove != None: #same for right move
                    self.checkerSelected.rightMove.deleteFromArr()
                    self.gameCanvas.delete(self.checkerSelected.rightMove)
                    self.checkerSelected.rightMove = None
                self.gameCanvas.delete('Take') #delets generated potential moves from the GUI
                self.checkerSelected = False

    def continueGame(self):
        """
        Continues game

        Resets all variables to be empty, changes player turn

        Args:
            None

        Returns:
            None

        Raises:
            None

        """
        self.checkerSelected = False
        if self.playerTurn == 1:
            self.playerTurn = 2
        else:
            self.playerTurn = 1


class Board: #class that stores drawn gameboard
    """
    Class that creates and stores board object on canvas

    Allows board to be drawn on canvas below everything

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    def __init__(self,canvas): #only needs canvas to draw on
        """
        Initilizes board object by passing needed variables from game, which is the game canvas

        Args:
            Tkinter canvas object

        Returns:
            None

        Raises:
            None

        """

        self.gameCanvas = canvas

    def initBoard(self):
        """
        draws light and dark squares in alternating pattern, like chessboard

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        color = Cons.DARK_SQUARE_COLOR
        for row in range(Cons.NUM_SQUARES + 1):
            for col in range(Cons.NUM_SQUARES + 1):
                color = Cons.LIGHT_SQUARE_COLOR if color == Cons.DARK_SQUARE_COLOR else Cons.DARK_SQUARE_COLOR #updates the color by changing after each draw
                self.gameCanvas.create_rectangle(row*Cons.SQUARE_SIZE,col*Cons.SQUARE_SIZE,row*Cons.SQUARE_SIZE + Cons.SQUARE_SIZE,col*Cons.SQUARE_SIZE + Cons.SQUARE_SIZE,fill = color,outline = color) #draws the actual board squares
        self.gameCanvas.pack()

class Piece:
    """
    general class that is used for all kinds of pieces

    Args:
        None

    Returns:
        None

    Raises:
        None

    """

    def __init__(self,x0,y0,x1,y1,color,canvas,gameArr):
        """
        Constructor for piece class

        Args:
            int x0 : x0 location of circle
            int y0 : y0 location of circle
            int x1 : x1 location of circle
            int y1 : y1 location of circle
            (those coordinates creates bounding box for piece)
            string color : color of piece
            Canvas canvas : game canvas
            list gameArr : array that stores game state

        Returns:
            None

        Raises:
            None

        """

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1 #these are coordinates
        self.color = color #color of given piece
        self.canvas = canvas #game canvas
        self.id = None #will store id of canvas object once it is created
        self.rowLoc,self.colLoc = self.getLocation(x0,y0) #coordinates of piece in game array based off of coordinates
        self.leftMove = None #stores left move when it is drawn and if it exists
        self.rightMove = None #stores right move when it is drawn and if it exists
        self.gameArr = gameArr #stores game state array

    def updateCoords(self,row,col,x0,y0,x1,y1):
        """
        Updates coordinates to inputted coords, and updates list position as well to inputted position

        Args:
            int row : new row
            int col : new col
            int x0 : new x0
            int y0 : new y0
            int x1 : new x1
            int y1 : new y1

        Returns:
            None

        Raises:
            None

        """

        self.rowLoc = row
        self.colLoc = col
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def getCoords(self):
        """
        returns coords of piece

        Args:
            None

        Returns:
            x0,y0,x1,y1 of given piece

        Raises:
            None

        """

        return self.x0,self.y0,self.x1,self.y1

    def getLocation(self,x0,y0):
        """
        returns location in row and column terms from x and y coord of window location

        Args:
            int x0: x coordinate to find location of
            int y0: y coordinate to find location of

        Returns:
            tuple: row,col

        Raises:
            None

        """
        if(y0 < 0 or y0 > Cons.BOARD_SIZE):
            row = -1
        elif(y0 <= 50):
            row = 0
        elif(y0 <= 100):
            row = 1
        elif(y0 <= 150):
            row = 2
        elif(y0 <= 200):
            row = 3
        elif(y0 <= 250):
            row = 4
        elif(y0 <= 300):
            row = 5
        elif(y0 <= 350):
            row = 6
        else:
            row = 7
        if(x0 < 0 or x0 > Cons.BOARD_SIZE):
            col = -1
        elif(x0 <= 50):
            col = 0
        elif(x0 <= 100):
            col = 1
        elif(x0 <= 150):
            col = 2
        elif(x0 <= 200):
            col = 3
        elif(x0 <= 250):
            col = 4
        elif(x0 <= 300):
            col = 5
        elif(x0 <= 350):
            col = 6
        else:
            col = 7
        return row,col


    def checkerSelected(self):
        """
        updates color of checker if selected from color to green

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        self.canvas.itemconfig(self.id, fill='green') #updates piece canvas object to be green

    def checkerDeselected(self):
        """
        deselects checker and removes color, and the move objects from class

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        self.canvas.itemconfig(self.id, fill=self.color) #updates piece canvas object to be original color
        self.leftMove = None #removes generated moves
        self.rightMove = None

    def moveChecker(self,x0,y0,x1,y1):
        """
        moves canvas drawn object and updates coords

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        self.canvas.coords(self.id,x0,y0,x1,y1) #updates coordinates of canvas object relating to piece
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def drawLeft(self,x0,y0,x1,y1,take = 0):
        """
        draws possible left move

        Args:
            x0,y0,x1,y1 : coordinates of piece
            bool take : 0 if not jumping over a piece, 1 if jumping over a piece

        Returns:
            None

        Raises:
            None

        """

        self.leftMove = PossibleMove(x0,y0,x1,y1,self.canvas,self.gameArr,self,take) #assigns to leftmove variable
        self.leftMove.drawCircle()

    def drawRight(self,x0,y0,x1,y1,take = 0):
        """
        draws possible right move

        Args:
            x0,y0,x1,y1 : coordinates of piece
            bool take : 0 if not jumping over a piece, 1 if jumping over a piece

        Returns:
            None

        Raises:
            None

        """

        self.rightMove = PossibleMove(x0,y0,x1,y1,self.canvas,self.gameArr,self,take) #asigns to rightmove variable
        self.rightMove.drawCircle()


    def deleteFromArr(self):
        """
        deletes piece from game array

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        self.gameArr[self.rowLoc][self.colLoc] = 0

    def undraw(self):
        """
        removes drawn canvvas object from canvas

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        self.canvas.delete(self.id) #deletes piece canvas object from canvas

class DarkPiece(Piece):
    """
    subclass of piece, only for dark pieces

    Args:
        None

    Returns:
        None

    Raises:
        None

    """

    def __init__(self,x0,y0,x1,y1,canvas,gameArr):
        """
        Constructor for dark piece

        Args:
            x0,y0,x1,y1 : coords for piece
            canvas : game Canvas
            gameArr : array that stores game state

        Returns:
            type: description

        Raises:
            Exception: description

        """

        super().__init__(x0,y0,x1,y1,Cons.DARK_PIECE_COLOR,canvas,gameArr)

    def initPiece(self):
        """
        Draws piece on the canvas as a circle, using coordinates stored from constructor

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        self.id = self.canvas.create_oval(self.x0,self.y0,self.x1,self.y1,fill = self.color, tags=('Checker')) #creates a canvas object using inputted data from constructor



    def drawMoves(self):
        """
        Draws possible moves that the selected piece can make

        Creates instances of possible moves, and stores them in respective variables to be used later with mouse clicks.

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        if(self.y1 + Cons.SQUARE_SIZE < Cons.BOARD_SIZE): #if not at the end of board
            if(self.x0 - Cons.SQUARE_SIZE > 0): #if not at edge of board
                potentialRow,potentialCol = self.getLocation(self.x0 - Cons.SQUARE_SIZE,self.y0 + Cons.SQUARE_SIZE) #get location of left move
                if self.gameArr[potentialRow][potentialCol] == 0: #if space is empty
                    self.drawLeft(self.x0 - Cons.SQUARE_SIZE,self.y0 + Cons.SQUARE_SIZE, self.x1 - Cons.SQUARE_SIZE,self.y1 + Cons.SQUARE_SIZE) #allow piece to move

                elif self.gameArr[potentialRow][potentialCol].__class__.__name__ == 'LightPiece': #if piece is opposite color
                    takeRow,takeCol = self.getLocation(self.x0 - 2 * Cons.SQUARE_SIZE,self.y0 + 2 * Cons.SQUARE_SIZE) #checks to see if opponent piece can be taken
                    if takeRow >= 0 and takeCol >= 0 and self.gameArr[takeRow][takeCol] == 0: #if it can be taken
                        self.drawLeft(self.x0 - Cons.SQUARE_SIZE * 2,self.y0 + Cons.SQUARE_SIZE * 2, self.x1 - Cons.SQUARE_SIZE * 2,self.y1 + Cons.SQUARE_SIZE * 2,1) #draw possible move
                        self.leftMove.setSkip(potentialRow,potentialCol) #remember piece that can be taken

            if(self.x1 + Cons.SQUARE_SIZE < Cons.BOARD_SIZE):
                potentialRow,potentialCol = self.getLocation(self.x0 + Cons.SQUARE_SIZE,self.y0 + Cons.SQUARE_SIZE) #gets location of right move
                if self.gameArr[potentialRow][potentialCol] == 0: #smilar to above, except checking for right side now
                    self.drawRight(self.x0 + Cons.SQUARE_SIZE,self.y0 + Cons.SQUARE_SIZE, self.x1 + Cons.SQUARE_SIZE,self.y1 + Cons.SQUARE_SIZE)

                elif self.gameArr[potentialRow][potentialCol].__class__.__name__ == 'LightPiece':
                    takeRow,takeCol = self.getLocation(self.x0 + 2 * Cons.SQUARE_SIZE,self.y0 + 2 * Cons.SQUARE_SIZE)
                    if takeRow >= 0 and takeCol >= 0 and self.gameArr[takeRow][takeCol] == 0:
                        self.drawRight(self.x0 + Cons.SQUARE_SIZE * 2,self.y0 + Cons.SQUARE_SIZE * 2, self.x1 + Cons.SQUARE_SIZE * 2,self.y1 + Cons.SQUARE_SIZE * 2,1)
                        self.rightMove.setSkip(potentialRow,potentialCol)

class LightPiece(Piece):
    """
    subclass of piece, only for light pieces

    Args:
        None

    Returns:
        None

    Raises:
        None

    """
    def __init__(self,x0,y0,x1,y1,canvas,gameArr):
        """
        Constructor for light piece

        Args:
            x0,y0,x1,y1 : coords for piece
            canvas : game Canvas
            gameArr : array that stores game state

        Returns:
            type: description

        Raises:
            Exception: description

        """
        super().__init__(x0,y0,x1,y1,Cons.LIGHT_PIECE_COLOR,canvas,gameArr)

    def initPiece(self):
        """
        Draws piece on the canvas as a circle, using coordinates stored from constructor

        Args:
            None

        Returns:
            None

        Raises:
            None

        """
        self.id = self.canvas.create_oval(self.x0,self.y0,self.x1,self.y1,fill = self.color, tags=('Checker'))


    def drawMoves(self):
        """
        Draws possible moves that the selected piece can make

        Creates instances of possible moves, and stores them in respective variables to be used later with mouse clicks.

        This concept is the same as the drawMoves in DarkPiece, just the math is slightly different as light pieces go up the board and dark pieces are going down.
        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        #Logic behind moving is the same as DarkPiece
        if(self.y0 - Cons.SQUARE_SIZE > 0):
            if(self.x0 - Cons.SQUARE_SIZE > 0):
                potentialRow,potentialCol = self.getLocation(self.x0 - Cons.SQUARE_SIZE,self.y0 - Cons.SQUARE_SIZE)
                if self.gameArr[potentialRow][potentialCol] == 0:
                    self.drawLeft(self.x0 - Cons.SQUARE_SIZE,self.y0 - Cons.SQUARE_SIZE, self.x1 - Cons.SQUARE_SIZE,self.y1 - Cons.SQUARE_SIZE)
                elif self.gameArr[potentialRow][potentialCol].__class__.__name__ == 'DarkPiece':
                    takeRow,takeCol = self.getLocation(self.x0 - 2 * Cons.SQUARE_SIZE,self.y0 - 2 * Cons.SQUARE_SIZE)
                    if takeRow >= 0 and takeCol >= 0 and self.gameArr[takeRow][takeCol] == 0:
                        self.drawLeft(self.x0 - Cons.SQUARE_SIZE * 2,self.y0 - Cons.SQUARE_SIZE * 2, self.x1 - Cons.SQUARE_SIZE * 2,self.y1 - Cons.SQUARE_SIZE * 2,1)
                        self.leftMove.setSkip(potentialRow,potentialCol)
            if(self.x1 + Cons.SQUARE_SIZE < Cons.BOARD_SIZE):
                potentialRow,potentialCol = self.getLocation(self.x0 + Cons.SQUARE_SIZE,self.y0 - Cons.SQUARE_SIZE)
                if self.gameArr[potentialRow][potentialCol] == 0:
                    self.drawRight(self.x0 + Cons.SQUARE_SIZE,self.y0 - Cons.SQUARE_SIZE, self.x1 + Cons.SQUARE_SIZE,self.y1 - Cons.SQUARE_SIZE)

                elif self.gameArr[potentialRow][potentialCol].__class__.__name__ == 'DarkPiece':
                    takeRow,takeCol = self.getLocation(self.x0 + 2 * Cons.SQUARE_SIZE,self.y0 - 2 * Cons.SQUARE_SIZE)
                    if takeRow >= 0 and takeCol >= 0 and self.gameArr[takeRow][takeCol] == 0:
                        self.drawRight(self.x0 + Cons.SQUARE_SIZE * 2,self.y0 - Cons.SQUARE_SIZE * 2, self.x1 + Cons.SQUARE_SIZE * 2,self.y1 - Cons.SQUARE_SIZE * 2,1)
                        self.rightMove.setSkip(potentialRow,potentialCol)


class PossibleMove(Piece):
    """
    class for possible moves

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    def __init__(event,x0,y0,x1,y1,canvas,gameArr,piece,take):
        """
        Constructor for possible move

        Main difference is that this uses an event instead of referring to self, as it is only created when there is a mouse click event

        Args:
            accepts the same inputs as the superclass constructor, please refer to that
            also takes piece, which is the piece that the move is created for
            take : if the possible move piece is created with the possibility to take another piece

        Returns:
            None

        Raises:
            Exception: description

        """

        super().__init__(x0,y0,x1,y1,'blue',canvas,gameArr)
        event.takePiece = take #if there is piece to be taken, bool value
        event.parentPiece = piece #parent piece that generated this move
        event.coordskippedR = -1 #stores position in array of piece to be taken if it exists
        event.coordskippedC = -1

    def setSkip(self,row,col):
        """
        Sets coords of piece to remove if a piece can be taken, stores in class variables

        Args:
            row,col : location in the array of piece that can be removed.

        Returns:
            None

        Raises:
            None

        """

        self.coordskippedR = row
        self.coordSkippedC = col

    def drawCircle(self):
        """
        draws on canvas

        draws the circle at the given coords of possible move on the canvas as defined by inital parameters stored in class variables.

        Args:
            opponentCanContinue

        Returns:
            None

        Raises:
            None

        """

        self.id = self.canvas.create_oval(self.x0,self.y0,self.x1,self.y1,fill = self.color,tags=('Take'))
        row,col = self.getLocation(self.x0,self.y0)

def startGame():
    """
    general method to start the game by creating game object and therefore tkinter window

    creates the game object, and shows the tkinter window by calling mainloop on the created tkinter object.

    Args:
        None

    Returns:
        None

    Raises:
        None

    """

    game = Game()
    game.game.mainloop()
