from modified_cmu_112_graphics import * #from class 
import tkinter as tk
import random
import math

class LevelBuilder(Mode):
    def appStarted(mode):
        mode.bg = mode.scaleImage(mode.loadImage("citybg.png"), 0.6)
        mode.margin = 100
        mode.yupbound = 480
        mode.ydownbound = 420
        mode.userInput()
    
    def userInput(mode):
        mode.rows = 6
        mode.cols = 6
        mode.layers = 6
        mode.destr = mode.rows
        mode.destc = mode.cols
        mode.destl = 1
        mode.randomize = False
        mode.chaos = 1
        mode.params = [mode.rows, mode.cols, mode.layers, mode.destr, mode.destc, mode.destl, mode.chaos]
        mode.names = ["R O W S", "C O L S", "L A Y E R S", "D E S T R", "D E S T C", "D E S T L", "C H A O S"]

    def checkBounds(mode, param):
        if mode.params[3] > mode.params[0] or mode.params[4] > mode.params[1] or mode.params[5] != 1:
            return False
        if param < 4:
            return False
        elif param > 8:
            return False
        return True
        

    def mousePressed(mode, event):
        #"begin"
        if (event.x >=10 and event.x <= 40 and event.y >= 10 and event.y <= 40):
            mode.app.setActiveMode(mode.app.titleScreenMode)
        if (event.x >= mode.margin and event.x <= (mode.width - mode.margin) and
            event.y <= mode.yupbound and event.y >= mode.ydownbound):
            mode.app.setActiveMode(mode.app.playThrough)

        for param in range(len(mode.params)):
            if (event.x > mode.width//2 - 55 and event.x < mode.width//2 - 45
                and event.y > 200 + param*30 - 10 and event.y < 200 + param*30 + 10):
                if (param == 0 or param == 1 or param == 2) and mode.params[param] == mode.params[param+3]:
                    mode.params[param+3] -= 1
                mode.params[param] -= 1
                if mode.checkBounds(mode.params[param]) == False:
                    if (param == 0 or param == 1 or param == 2) and mode.params[param] == mode.params[param+3]:
                        mode.params[param+3] += 1
                    mode.params[param] += 1
            if (event.x > mode.width//2 + 45 and event.x < mode.width//2 + 55
                and event.y > 200 + param*30 - 10 and event.y < 200 + param*30 + 10):
                mode.params[param] += 1
                if mode.checkBounds(mode.params[param]) == False:
                    mode.params[param] -= 1
                

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, 
            image = ImageTk.PhotoImage(mode.bg))
        mode.drawText(canvas)
        mode.drawControls(canvas)
        canvas.create_rectangle(10, 10, 40, 40, outline = 'white')
        canvas.create_line(15, 25, 25, 15, fill = 'white')
        canvas.create_line(15, 25, 35, 25, fill = 'white')
        canvas.create_line(15, 25, 25, 35, fill = 'white')
    
    #normal mode
    def drawText(mode, canvas):
        #game title
        canvas.create_text(mode.width/2 + 4, 84,
            fill = 'violetred4', text = "L E V E L  B U I L D E R",
            font = "Arial 30 bold italic")
        canvas.create_text(mode.width/2, 80,
            fill = 'white', text = "L E V E L  B U I L D E R",
            font = "Arial 30 bold italic")
        #INSTRUCTIONS
        canvas.create_text(mode.width/2, 115,
            fill = 'white', text = 'destr, destc, destl = destination',
            font = "Arial 12 italic")
        canvas.create_text(mode.width/2, 130,
            fill = 'white', text = '4 < rows, cols, layers < 8',
            font = "Arial 12 italic")
        canvas.create_text(mode.width/2, 145,
            fill = 'white', text = '4 < dest_x < x',
            font = "Arial 12 italic")
        canvas.create_text(mode.width/2, 160,
            fill = 'white', text = 'try higher chaos!',
            font = "Arial 12 italic")
        #GENERATE
        canvas.create_rectangle(mode.margin, mode.yupbound,
            mode.width - mode.margin, mode.ydownbound,
            outline = 'white', width = 2)
        canvas.create_text(mode.width/2, (mode.yupbound+mode.ydownbound)/2,
            fill = 'white', text = "G E N E R A T E",
            font = "Arial 14 italic")
    
    def drawControls(mode, canvas):

        for i in range(len(mode.params)):
            mode.drawBox(canvas, 200 + i*30, mode.params[i], mode.names[i])
    
    def drawBox(mode, canvas, y, param, name):
        hor = 40
        vert = 10
        margin = 5
        x = mode.width//2
        canvas.create_rectangle(x-hor, y-vert, x+hor, y+vert, outline = 'white')
        canvas.create_text(x,y, text = f"{name}: {param}", font = "Arial 10", 
                            fill = 'white')
        canvas.create_polygon(x-hor-margin,y-vert, x-hor-margin, y+vert,
                            x-hor-margin*3, y, outline = 'white', fill = 'white')
        canvas.create_polygon(x+hor+margin,y-vert, x+hor+margin, y+vert,
                            x+hor+margin*3, y, outline = 'white', fill = 'white')
        

class PlayThrough(Mode):
    #initialize variables
    def appStarted(mode):
        mode.rows = mode.app.levelBuilder.params[0] + 1
        mode.cols = mode.app.levelBuilder.params[1] + 1
        mode.layers = mode.app.levelBuilder.params[2] + 1
        mode.cubesize = 30
        mode.cubewidth = mode.cubesize/2*math.sqrt(3)
        mode.chaos = mode.app.levelBuilder.params[6]
        mode.margin = 0
        mode.board = mode.make3dlist(mode.rows+1, mode.cols+1, mode.layers+1)
        mode.piece = mode.make3dlist(mode.rows+1, mode.cols+1, mode.layers+1)
        mode.speed = 5
        mode.yeet = False
        mode.targetx = None
        mode.targety = None
        mode.buttonhit = False
        mode.destr = mode.app.levelBuilder.params[3]-1
        mode.destc = mode.app.levelBuilder.params[4]-1
        mode.destl = 0
        mode.lildude()
        mode.structure()
        mode.button()
        mode.destination = (mode.destr, mode.destc, mode.destl) 
        mode.destblockx = 0
        mode.destblocky = 0
        mode.visited = []
        mode.animate = False
        mode.reached = False
        mode.aistart = False
        mode.solved = False

    #helper function, modified from class notes
    def make3dlist(mode, x, y, z): 
        return [[ [None for col in range(x)] for col in range(y)] for row in range(z)] 

    #creates building structure
    def structure(mode):
        for row in range(len(mode.board[0][0])-2):
            for col in range(len(mode.board[0])-2):
                num = random.randint(0,10)
                if (num <= mode.chaos and (row, col) != (mode.crowrow, mode.crowcol)
                    and (row, col) != (mode.destr, mode.destc)
                    and (row, col) != (0,0)):
                    mode.board[row][col][0] = False
                else:
                    mode.board[row][col][0] = True
                if (mode.board[row][col][0] == True
                    and (row, col) != (mode.crowrow, mode.crowcol)
                    and (row, col) != (mode.destr, mode.destc)
                    and (row, col) != (0,0)):
                    num2 = random.randint(7,10)
                    if num2 < mode.chaos:
                        mode.board[row][col][(num2-5)//2] = True
                if ((row == 0 or col == 0) and mode.board[row][col][0] == True
                    and (row,col) != (0,0) and (row,col) != (1,0) and (row,col) != (0,1)):
                    num3 = random.randint(0,3)
                    if num3 == 1:
                        mode.board[row][col][1] = True
                    elif num3 == 2:
                        mode.board[row][col][1] = True
                        mode.board[row][col][2] = True
                    elif num3 == 3:
                        for layer in range(mode.layers+2):
                            mode.board[row][col][layer//2] = True
                    

    #creates button, alters structure if hit
    def button(mode):
        chosen = False
        while chosen == False:
            num1, num2 = random.randint(0,mode.rows-3), random.randint(0,mode.rows-3)
            if ((num1, num2) != (mode.destr, mode.destc)
                and (num1, num2) != (0,0)
                and mode.board[num1][num2][0] == True
                and mode.board[num1][num2][1] == None):
                chosen = True
        mode.buttonrow = num1
        mode.buttoncol = num2
        mode.buttonlayer = 0
        mode.buttonrow2,mode.buttoncol2,mode.buttonlayer2 = (4,7,4)
        if mode.buttonhit == True:
            for row in range(mode.rows):
                for col in range(mode.cols):
                    if mode.board[row][col][0] == True:
                        num = random.randint(0,10)
                        if (num <= mode.chaos and (row, col) != (mode.crowrow, mode.crowcol)
                            and (row, col) != (mode.destr, mode.destc)
                            and (row, col) != (mode.buttonrow, mode.buttoncol)):
                            mode.board[row][col][0] = False
                        else:
                            mode.board[row][col][0] = True


    #initializes character
    def lildude(mode):
        #import crow image
        mode.crow = mode.scaleImage(mode.loadImage("crowL.png"), 0.5 * mode.cubesize/40)
        #start location for crow
        mode.startrow = 0
        mode.startcol = 0
        mode.startlayer = 0
        mode.crowrow = mode.startrow
        mode.crowcol = mode.startcol
        mode.crowlayer = mode.startlayer
        mode.crowx, mode.crowy = mode.getcoor(mode.startrow, mode.startcol, mode.startlayer)
        mode.crowy = mode.crowy - mode.cubesize


    #converts row/col/layer to x/y coordinates
    def getcoor(mode, row, col, layer):
        midw = mode.width //2 
        midh = mode.height //2
        sqr = mode.cubesize // 2 * math.sqrt(3)
        half = mode.cubesize//2
        x = midw - sqr * row + sqr * col
        y = midh + half * row + half * col - mode.cubesize * layer
        return x, y

    #move character when desired
    def timerFired(mode):
        if mode.yeet == True:
            mode.reached = False
            dx = mode.targetx - mode.crowx
            dy = mode.targety - mode.crowy
            dy = dy - mode.cubesize/2
            #check stop
            if (dx)**2 + (dy)**2 < 20:
                mode.crowx = mode.destblockx
                mode.crowy = mode.destblocky - mode.cubesize
                mode.yeet = False
                mode.reached = True
            #slope of isometric cube is 1/sqrt(3) -> best approximation is 4/7
            #each four directions
            elif dx > 0 and dy > 0:
                mode.crow = mode.scaleImage(mode.loadImage("crowR.png"), 0.5 * mode.cubesize/40)
                mode.crowx += 7
                mode.crowy += 4
            elif dx > 0 and dy < 0:
                mode.crow = mode.scaleImage(mode.loadImage("crowR.png"), 0.5 * mode.cubesize/40)
                mode.crowx += 7
                mode.crowy -= 4
            elif dx < 0 and dy > 0:
                mode.crow = mode.scaleImage(mode.loadImage("crowL.png"), 0.5 * mode.cubesize/40)
                mode.crowx -= 7
                mode.crowy += 4
            elif dx < 0 and dy < 0:
                mode.crow = mode.scaleImage(mode.loadImage("crowL.png"), 0.5 * mode.cubesize/40)
                mode.crowx -= 7
                mode.crowy -= 4
            
        mode.buttonHit()
        mode.destReached()


    def buttonHit(mode):
        #see if button is hit
        x, y = mode.getcoor(mode.buttonrow, mode.buttoncol, mode.buttonlayer)
        y = y - mode.cubesize*2.5/2
        if abs(mode.crowx - x) < 20 and abs(mode.crowy - y) < 20:
            mode.buttonhit = True
            mode.button()

    def destReached(mode):
        #see if destination reached
        destr, destc, destl = mode.destination
        x, y = mode.getcoor(destr, destc, destl)
        y = y - mode.cubesize*2.5/2
        if abs(mode.crowx - x) < 20 and abs(mode.crowy - y) < 20 and mode.aistart == False:
            mode.solved = True
            mode.ai()

        
    def checkValid(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    if mode.board[row][col][layer] == True or mode.piece[row][col][layer] == True:
                        blockx, blocky = mode.getcoor(row, col, layer)
                        if mode.pointOnSurface(x, y, blockx, blocky):
                            if mode.checkLine(blockx, blocky) == True:
                                if mode.checkMissing(row, col, blockx, blocky) == True:
                                    mode.destblockx = blockx
                                    mode.destblocky = blocky
                                    mode.crowrow = row
                                    mode.crowcol = col
                                    return True
        return False

    def pointOnSurface(mode, x, y, blockx, blocky):
        if (x - blockx)**2 + (y - blocky + mode.cubesize/2)**2 < 100:
            return True
        return False
        
    def checkLine(mode, blockx, blocky):
        run = abs(blockx - mode.crowx)
        rise = abs(blocky - (mode.crowy + mode.cubesize))
        if abs(rise*math.sqrt(3) - run) < 10:
            return True
        return False

    def checkMissing(mode, row, col, blockx, blocky):
        dx = mode.targetx - mode.crowx
        dy = mode.targety - mode.crowy
        direc = 0,0
        if dx > 0 and dy > 0:
            direc = 1,1
        elif dx > 0 and dy < 0:
            direc = 1, -1
        elif dx < 0 and dy > 0:
            direc = -1, 1
        elif dx < 0 and dy < 0:
            direc = -1, -1
        direcx, direcy = direc
        rowdiff = abs(mode.crowrow - row)
        coldiff = abs(mode.crowcol - col)
        tempcrowrow = mode.crowrow
        tempcrowcol = mode.crowcol
        
        while coldiff != 0:
            found = False
            wantedx, wantedy = mode.getcoor(tempcrowrow, tempcrowcol + direcy, mode.crowlayer)
            for row in range(mode.rows):
                for col in range(mode.cols):
                    for layer in range(mode.layers):
                        if mode.board[row][col][layer] == True or mode.piece[row][col][layer] == True:
                            otherx, othery = mode.getcoor(row, col, layer)
                            if otherx == wantedx and othery == wantedy:
                                found = True
            if found == True:
                tempcrowcol += direcy
                coldiff -= 1
            else:
                return False
        return True

    def ai(mode):
        mode.aistart = True
        mode.gettodest(mode.crowrow, mode.crowcol, mode.crowlayer)

    def gettodest(mode, row, col, layer):
        if (row, col, layer) in mode.visited:
            return False
        mode.visited.append((row, col, layer))
        if (row, col, layer) == (mode.destr, mode.destc, mode.destl):
            mode.crowrow, mode.crowcol, mode.crowlayer = mode.destr, mode.destc, mode.destl
            x, y = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
            mode.crowx, mode.crowy = x, y - mode.cubesize
            return True
        for drow, dcol in [(-1,0),(1,0),(0,1),(0,-1)]:
            if mode.isValid(row, col, layer, (drow, dcol)):
                if mode.gettodest(row+drow, col + dcol, layer):
                    return True
        mode.visited.pop()
        return False

    def isValid(mode, row, col, layer, direction):
        (drow, dcol) = direction
        if row + drow >= mode.rows or row + drow < 0 or col + dcol >= mode.cols or col + dcol < 0 :
            return False
        if mode.board[row + drow][col + dcol][1] == True:
            return False
        if (mode.board[row+drow][col+dcol][layer] == True \
            and mode.board[row+drow][col+dcol][layer+1] == False\
            or mode.piece[row+drow][col+dcol][layer] == True):
            return True
        for i in range(mode.rows):
            if row+drow+i < mode.rows and col+dcol+i<mode.cols and layer+i<mode.layers:
                if mode.board[row+drow+i][col+dcol+i][layer+i] == True:
                    return True
        return False


    def clickPiece(mode, event):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    if mode.piece[row][col][layer] == True:
                        blockx, blocky = mode.getcoor(row, col, layer)
                        if abs(event.x - blockx) < mode.cubesize*3/2 and abs(event.y - blocky) < mode.cubesize*3/2:
                            return True
        return False
    

    def rotateallright(mode):
        shift = mode.cols-2
        temp = mode.make3dlist(mode.cols, mode.rows, mode.layers)
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[shift-col][row][layer] = mode.board[row][col][layer]
        mode.board = temp
        mode.buttonrow, mode.buttoncol = shift - mode.buttoncol, mode.buttonrow
        mode.startrow, mode.startcol = shift - mode.startcol, mode.startrow
        

        (destr, destc, destl) = mode.destination
        tempr, tempc = destr, destc
        mode.destination = (shift-tempc, tempr, destl)
        mode.destr, mode.destc, mode.destl = mode.destination

        temprow, tempcol = mode.crowrow, mode.crowcol
        mode.crowrow, mode.crowcol = shift - tempcol, temprow 
        mode.crowx, mode.crowy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
        mode.crowy = mode.crowy - mode.cubesize

        mode.ladder = [(0,0,0),(0,0,0)]


    def rotateallleft(mode):
        shift = mode.rows - 1
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[col][shift-row][layer] = mode.board[row][col][layer]
        mode.board = temp
        mode.buttonrow, mode.buttoncol = mode.buttoncol, shift - mode.buttonrow
        mode.startrow, mode.startcol = shift - mode.startcol, mode.startrow

        (destr, destc, destl) = mode.destination
        tempr, tempc = destr, destc
        mode.destination = (tempc, shift - tempr, destl)

        temprow, tempcol = mode.crowrow, mode.crowcol
        mode.crowrow, mode.crowcol = tempcol, shift - temprow 
        mode.crowx, mode.crowy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
        mode.crowy = mode.crowy - mode.cubesize

        mode.ladder = [(0,0,0),(0,0,0)]


    def keyPressed(mode, event):
        if event.key == "Right":
            mode.rotateallright()
        elif event.key == "Left":
            mode.rotateallleft()
        elif event.key == "r":
            mode.appStarted()
        elif event.key == "1":
            mode.app.setActiveMode(mode.app.levelOne)
        elif event.key == "2":
            mode.app.setActiveMode(mode.app.levelTwo)
        elif event.key == "3":
            mode.app.setActiveMode(mode.app.levelThree)
        elif event.key == "4":
            mode.app.setActiveMode(mode.app.levelBuilder)


    #move to mouse direction
    def mousePressed(mode,event):
        if (event.x >=10 and event.x <= 40 and event.y >= 10 and event.y <= 40):
            mode.appStarted()
            mode.app.appStarted()
            mode.app.setActiveMode(mode.app.levelBuilder)
        elif event.x >= 360 and event.y >= 560 and event.x <= 380 and event.y <= 580:
            mode.app.setActiveMode(mode.app.instructionMode)
        elif event.x >= 330 and event.y >= 560 and event.x <= 350 and event.y <= 580:
            mode.app.appStarted()
        elif event.x >= 300 and event.y >= 560 and event.x <= 320 and event.y <= 580:
            mode.ai()
        elif event.x >= 300 and event.y >= 480 and event.x <= 380 and event.y <= 550:
            mode.appStarted()
        else:
            mode.targetx = event.x
            mode.targety = event.y
            if mode.checkValid(event.x, event.y) == True:
                mode.yeet = True

    
    def rightMousePressed(mode, event):
        if mode.clickPiece(event):
            mode.rotateright()

    #draw all
    def redrawAll(mode, canvas):
        mode.drawGradient(canvas)
        mode.drawGrid(canvas)
        mode.drawButton(canvas)
        mode.drawDude(canvas)
        mode.drawHelper(canvas)
        if mode.aistart == True:
            mode.drawAI(canvas)
        canvas.create_rectangle(10, 10, 40, 40, outline = 'white', width = 4)
        canvas.create_line(15, 25, 25, 15, fill = 'white', width = 4)
        canvas.create_line(15, 25, 35, 25, fill = 'white', width = 4)
        canvas.create_line(15, 25, 25, 35, fill = 'white', width = 4)

    #gradient background
    def drawGradient(mode, canvas):
        #desired rgb values
        startr, startg, startb = 240, 175, 200
        endr, endg, endb = 150, 190, 235
        #create lines to display solid gradient
        for i in range(mode.height//5):
            newr = startr + (endr - startr) * i * 5 // mode.height
            newg = startg + (endg - startg) * i * 5 // mode.height
            newb = startb + (endb - startb) * i * 5 // mode.height
            #rbg to hex
            newhex = '#%02x%02x%02x' % (newr, newg, newb)
            canvas.create_line(0, i*5, mode.width, i*5, fill = newhex, width = 5)
        #level title

        canvas.create_text(mode.width/2 + 3, 53,
            fill = 'thistle4', text = "C U S T O M  L E V E L",
            font = "Arial 20 bold italic")
        canvas.create_text(mode.width/2, 50,
            fill = 'white', text = "C U S T O M  L E V E L",
            font = "Arial 20 bold italic")

        if mode.solved == True and mode.aistart == False:
            canvas.create_text(mode.width/2, 200,
                fill = 'white', text = "Y O U  S O L V E D  I T ! \n\t   G O O D  J O B!!",
                font = "Arial 20 bold italic")
        
 
    def drawGrid(mode, canvas):
        destr, destc, destl = mode.destination
        for row in range(len(mode.board)):
            for col in range(len(mode.board[0])):
                for layer in range(len(mode.board[0][0])):
                    if mode.board[row][col][layer] == True:
                        x, y = mode.getcoor(row, col, layer)
                        if row == destr and col == destc and layer == destl:
                            mode.drawCube(canvas, x, y, "destination")
                            canvas.create_oval(x - 10, y - 20,
                            x + 10, y - 10, 
                            outline = 'steelblue3', width = 3)
                        else:
                            mode.drawCube(canvas, x, y, "normal")
                    if mode.piece[row][col][layer] == True:
                        x, y = mode.getcoor(row, col, layer)
                        mode.drawCube(canvas, x, y, "moving")
                 
    #draw individual cubes
    def drawCube(mode, canvas, x, y, piecetype):
        if piecetype == "normal":
            color = ['lavender blush', 'thistle', 'plum4']
        elif piecetype == "moving":
            color = ['pink', 'pale violet red', 'maroon']
        elif piecetype == "destination":
            color = ['blue', 'navy', 'black']
        cubew = mode.cubesize * math.sqrt(3)
        halfsize = mode.cubesize // 2
        #top plane
        canvas.create_polygon(  x, y - mode.cubesize,
                                x - cubew//2, y + halfsize - mode.cubesize,
                                x, y,
                                x + cubew//2, y + halfsize - mode.cubesize,
                                width =0,
                                outline = 'white', fill = color[0])
        #left plane
        canvas.create_polygon(  x, y,
                                x - cubew//2, y - halfsize,
                                x - cubew//2, y + halfsize,
                                x, y + mode.cubesize,
                                width =0,
                                outline = 'white', fill = color[1])                        
        #right plane
        canvas.create_polygon(  x, y,
                                x + cubew//2, y - halfsize,
                                x + cubew//2, y + halfsize,
                                x, y + mode.cubesize,
                                width =0,
                                outline = 'plum3', fill = color[2])  

    #draw button with shadow
    def drawButton(mode, canvas):
        x, y = mode.getcoor(mode.buttonrow, mode.buttoncol, mode.buttonlayer)
        cubew = mode.cubesize * math.sqrt(3) / 2
        #shadow
        canvas.create_oval( x - cubew/2, y - mode.cubesize*2/3,
                            x + cubew/2, y - mode.cubesize/3, 
                            outline = 'white', fill = 'maroon')
        #top
        canvas.create_oval( x - cubew/2, y - mode.cubesize*2/3 - 3,
                            x + cubew/2, y-mode.cubesize/3 - 3, 
                            width = 0, fill = 'pale violet red')

    #draw character
    def drawDude(mode, canvas):
        canvas.create_image(mode.crowx, mode.crowy, image = ImageTk.PhotoImage(mode.crow))
        canvas.create_oval(mode.destblockx - 3, mode.destblocky - 3, mode.destblockx + 3, mode.destblocky+3, outline = "red")
        canvas.create_oval(mode.crowx - 3, mode.crowy - 3, mode.crowx + 3, mode.crowy+3, outline = "white")

    #draw instruction box
    def drawHelper(mode, canvas):
        canvas.create_rectangle(360, 560, 380, 580, outline = 'white', width = 1)
        canvas.create_text(370, 569, fill = 'white', text = "?",
            font = 'Arial 14')
        canvas.create_rectangle(330, 560, 350, 580, outline = 'white', width = 1)
        canvas.create_text(340, 569, fill = 'white', text = "R",
            font = 'Arial 14')
        canvas.create_rectangle(300, 560, 320, 580, outline = 'white', width = 1)
        canvas.create_text(310, 569, fill = 'white', text = "AI",
            font = 'Arial 14')
        canvas.create_rectangle(300,500,380,550, outline = 'white')
        canvas.create_text(340,525, text = 'R E G E N -\n E R A T E', fill = 'white', font = 'Arial 12')
        

    def drawAI(mode, canvas):
        canvas.create_rectangle(10, 500, 290, 580, outline = 'white')
        if len(mode.visited) != 0:
            canvas.create_text(150,512,text='P A T H  S O L U T I O N',
                font = 'Arial 14 bold', fill = 'white')
            canvas.create_line(70,520,230,520,fill = 'white')
            for i in range(len(mode.visited)-1):
                canvas.create_text(40 + i//5 * 70, 530 + i % 5 * 10,
                    text = f'{i+1}. ({str(mode.visited[i+1])[1:5]})', font = 'Arial 9', fill = 'white')
        elif len(mode.visited) == 0:
            canvas.create_text(150,550,text='N O  S O L U T I O N',
            font = 'Arial 14 bold', fill = 'white')
            canvas.create_line(80,560,220,560,fill = 'white')

# class MyModalApp(ModalApp):
#     def appStarted(app):
#         app.levelBuilder = LevelBuilder()
#         app.playThrough = PlayThrough()
#         app.setActiveMode(app.levelBuilder)

# app = MyModalApp(width=400, height=600)