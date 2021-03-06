from modified_cmu_112_graphics import * #from class 
import tkinter as tk
import random
import math

class LevelThree(Mode):

    #############################################
    ############## INITIALIZATION ###############
    #############################################

    #initialize variables
    def appStarted(mode):
        mode.rows = 10
        mode.cols = 10
        mode.layers = 10
        mode.cubesize = 24
        mode.cubewidth = mode.cubesize/2*math.sqrt(3)
        mode.margin = 0
        mode.board = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        mode.piece = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        mode.speed = 5
        mode.yeet = False
        mode.targetx = None
        mode.targety = None
        mode.buttonhit = False
        mode.structure()
        mode.button()
        mode.lildude()
        mode.destination = (5,0,4)
        mode.destr, mode.destc, mode.destl = mode.destination
        mode.destblockx = 0
        mode.destblocky = 0
        mode.visited = []
        mode.visited1 = []
        mode.visited2 = []
        mode.checked = []
        mode.aistart = False
        mode.rotated = 0
        mode.animate = False
        mode.counter = 0


    #helper function, modified from class notes
    def make3dlist(mode, x, y, z): 
        return [[ [None for col in range(x)] for col in range(y)] for row in range(z)] 

    #creates building structure
    def structure(mode):
        #LEFT SIDE
        for row in range(6):
            mode.board[row][0][0] = True
        for layer in range(5):
            mode.board[5][0][layer] = True
            #top part
        mode.board[4][0][4] = True
        mode.board[4][1][4] = True
        mode.board[4][2][4] = True

        #RIGHT SIDE
        for col in range(5):
            mode.board[0][1+col][0] = True
            #pillar
        mode.board[0][5][1] = True
        mode.board[0][5][2] = True
            #protrusion
        for row in range(4):
            mode.board[row][5][3] = True
        mode.board[3][4][3] = True
        
        #BACK SIDE
        for layer in range(4):
            for col in range(5):
                mode.board[0][col][layer] = True
        mode.board[0][0][4] = True
        mode.board[0][1][4] = True

        mode.ladder = [(0,3,3),(0,1,4)]
        (startr, startc, startl),(finr, finc, finl) = mode.ladder
        mode.ladx0, mode.lady0 = mode.getcoor(startr, startc, startl)
        mode.ladx1, mode.lady1 = mode.getcoor(finr, finc, finl)

    def resetstructure(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    mode.board[row][col][layer] = False
        mode.structure()
        mode.buttonrow = 0
        mode.buttoncol = 0
        mode.buttonlayer = 4
        mode.destination = (5,0,4)
        mode.destr, mode.destc, mode.destl = mode.destination


    #creates button, alters structure if hit
    def button(mode):
        mode.buttonrow = 0
        mode.buttoncol = 0
        mode.buttonlayer = 4
        if mode.buttonhit == False:
            pass
        elif mode.buttonhit == True:
            for row in range(4):
                for col in range(4):
                    mode.board[1+row][1+col][0] = True


    #initializes character
    def lildude(mode):
        #import crow image
        mode.crow = mode.scaleImage(mode.loadImage("crowL.png"), 0.5 * mode.cubesize/40)
        #start location for crow
        mode.startrow = 0
        mode.startcol = 5
        mode.startlayer = 3
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

    #############################################
    ################## TIMER ####################
    #############################################

    #move character when desired
    def timerFired(mode):
        if mode.animate == True:
            mode.counter += 1
            print(mode.counter)
            if mode.counter <15:
                mode.resetstructure()
            if mode.counter == 15:
                mode.rotateallright()
                mode.crowrow, mode.crowcol, mode.crowlayer = 1,0,3
                x,y = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
                mode.crowx, mode.crowy = x,y
            if mode.counter <= (len(mode.visited)-1)*2:
                if mode.visited[mode.counter//2] == 'rotate right':
                    pass
                else:
                    (mode.crowrow, mode.crowcol, mode.crowlayer) = mode.visited[mode.counter//2]
                    pathx, pathy = mode.getcoor(mode.crowrow-1, mode.crowcol-1, mode.crowlayer)
                    mode.crowx, mode.crowy = pathx, pathy
            else:
                mode.animate = False
        if mode.yeet == True:
            dx = mode.targetx - mode.crowx
            dy = mode.targety - mode.crowy
            dy = dy - mode.cubesize/2
            #check stop
            if (dx)**2 + (dy)**2 < 20:
                mode.crowx = mode.destblockx
                mode.crowy = mode.destblocky - mode.cubesize
                mode.yeet = False
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
            
        #see if button is hit
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
        x, y = mode.getcoor(mode.destr, mode.destc, mode.destl)
        y = y - mode.cubesize*2.5/2
        if abs(mode.crowx - x) < 10 and abs(mode.crowy - y) < 10 and mode.aistart == False:
            mode.app.setActiveMode(mode.app.gameOver)

    
    #############################################
    ############### CHECK BOUNDS ################
    #############################################
    
    def checkValid(mode, x, y):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    if mode.board[row][col][layer] == True or mode.piece[row][col][layer] == True:
                        blockx, blocky = mode.getcoor(row, col, layer)
                        if mode.pointOnSurface(x, y, blockx, blocky) and mode.checkLine(blockx, blocky) == True:
                            print('crow', mode.crowrow, mode.crowcol, mode.crowlayer)
                            if mode.gettoclick(mode.crowrow, mode.crowcol, mode.crowlayer, row, col, layer):
                                mode.destblockx = blockx
                                mode.destblocky = blocky
                                mode.crowrow = row
                                mode.crowcol = col
                                return True
        return False

    #inspired by 15112 backtracking examples
    def gettoclick(mode, row, col, layer, clickrow, clickcol, clicklayer):
        if (row, col, layer) == (clickrow, clickcol, clicklayer):
            return True
        if mode.rotated%4 == 1 and (row,col,layer) == (2,3,3):
            (mode.crowrow,mode.crowcol,mode.crowlayer) = (3,4,4)
        if (row, col, layer) in mode.checked:
            return False
        mode.checked.append((row, col, layer))
        for drow, dcol in [(-1,0),(1,0),(0,1),(0,-1)]:
            if mode.validpath(row, col, layer, (drow, dcol)):
                if mode.gettoclick(row+drow, col + dcol, layer, clickrow, clickcol, clicklayer):
                    mode.checked = []
                    return True
        mode.checked.pop()
        return False

    def validpath(mode, row, col, layer, direction):
        (drow, dcol) = direction
        if mode.board[row+drow][col+dcol][layer+1] == True:
            return False
        if (mode.board[row+drow][col+dcol][layer] == True \
            or mode.piece[row+drow][col+dcol][layer] == True):
            return True
        for i in range(mode.rows):
            if row+drow+i < mode.rows and col+dcol+i<mode.cols and layer+i<mode.layers:
                if mode.board[row+drow+i][col+dcol+i][layer+i] == True:
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

    #############################################
    ################ AI SOLUTION ################
    #############################################

    def ai(mode):
        mode.appStarted()
        mode.aistart = True
        mode.gettobutton(mode.startrow, mode.startcol, mode.startlayer)
        mode.returntostart()
        mode.visited.extend(mode.visited1)
        mode.visited.extend(['rotate right'])
        mode.rotateallright()
        mode.gettodest(mode.crowrow, mode.crowcol, mode.crowlayer)
        mode.visited.extend(mode.visited2)
        mode.animate = True

    #inspired by 15112 backtracking examples
    def gettobutton(mode, row, col, layer):
        if (row,col,layer) == mode.ladder[0]:
            (row,col,layer) = mode.ladder[1]
        if (row, col, layer) in mode.visited:
            return False
        mode.visited.append((row, col, layer))
        if (row, col, layer) == (mode.buttonrow, mode.buttoncol, mode.buttonlayer):
            mode.crowrow, mode.crowcol, mode.crowlayer = mode.buttonrow, mode.buttoncol, mode.buttonlayer
            x, y = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
            mode.crowx, mode.crowy = x, y - mode.cubesize
            mode.buttonhit = True
            return True
        for drow, dcol in [(-1,0),(1,0),(0,1),(0,-1)]:
            if mode.isValid(row, col, layer, (drow, dcol)):
                if mode.gettobutton(row+drow, col + dcol, layer):
                    return True
        mode.visited.pop()
        return False

    def returntostart(mode):
        length = len(mode.visited)
        for i in range(length):
            (mode.crowrow, mode.crowcol, mode.crowlayer) = mode.visited[length - i - 1]
            x, y = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
            mode.crowx, mode.crowy = x, y - mode.cubesize
            mode.visited1.append(mode.visited[length - i - 1])
    
    #inspired by 15112 backtracking examples
    def gettodest(mode, row, col, layer):
        #illusion
        if (row, col, layer) == (3,3,3):
            return mode.gettodest(4,4,4)
        if (row, col, layer) in mode.visited2:
            return False
        mode.visited2.append((row, col, layer))
        if (row, col, layer) == (mode.destr, mode.destc, mode.destl):
            mode.crowrow, mode.crowcol, mode.crowlayer = mode.destr, mode.destc, mode.destl
            x, y = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
            mode.crowx, mode.crowy = x, y - mode.cubesize
            return True
        for drow, dcol in [(-1,0),(1,0),(0,1),(0,-1)]:
            if mode.isValid(row, col, layer, (drow, dcol)):
                if mode.gettodest(row+drow, col + dcol, layer):
                    return True
        mode.visited2.pop()
        return False


    def isValid(mode, row, col, layer, direction):
        (drow, dcol) = direction
        if (mode.board[row+drow][col+dcol][layer] == True \
            and mode.board[row+drow][col+dcol][layer+1] == False\
            or mode.piece[row+drow][col+dcol][layer] == True):
            return True
        for i in range(mode.rows):
            if row+drow+i < mode.rows and col+dcol+i<mode.cols and layer+i<mode.layers:
                if mode.board[row+drow+i][col+dcol+i][layer+i] == True:
                    return True
        return False


    #############################################
    ########### ROTATION + LADDER ###############
    #############################################

    def rotateallright(mode):
        mode.rotated += 1
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[6-col][row][layer] = mode.board[row][col][layer]
        mode.board = temp
        mode.buttonrow, mode.buttoncol = 6 - mode.buttoncol, mode.buttonrow
        mode.startrow, mode.startcol = 6 - mode.startcol, mode.startrow
        

        (destr, destc, destl) = mode.destination
        tempr, tempc = destr, destc
        mode.destination = (6-tempc, tempr, destl)
        mode.destr, mode.destc, mode.destl = mode.destination

        if mode.animate == False:
            temprow, tempcol = mode.crowrow, mode.crowcol
            mode.crowrow, mode.crowcol = 6 - tempcol, temprow 
            mode.crowx, mode.crowy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
            mode.crowy = mode.crowy - mode.cubesize

        mode.ladder = [(0,0,0),(0,0,0)]


    def rotateallleft(mode):
        mode.rotated -= 1
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[col][6-row][layer] = mode.board[row][col][layer]
        mode.board = temp
        mode.buttonrow, mode.buttoncol = mode.buttoncol, 6 - mode.buttonrow
        mode.startrow, mode.startcol = 6 - mode.startcol, mode.startrow

        (destr, destc, destl) = mode.destination
        tempr, tempc = destr, destc
        mode.destination = (tempc, 6 - tempr, destl)

        temprow, tempcol = mode.crowrow, mode.crowcol
        mode.crowrow, mode.crowcol = tempcol, 6- temprow 
        mode.crowx, mode.crowy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
        mode.crowy = mode.crowy - mode.cubesize

        mode.ladder = [(0,0,0),(0,0,0)]


    def rotateright(mode):
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        onblock = False
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    if mode.piece[row][col][layer] == True:
                        blockx, blocky = mode.getcoor(row, col, layer)
                        if blockx == mode.crowx and blocky == mode.crowy + mode.cubesize:
                            onblock = True
                    temp[col][4-row][layer] = mode.piece[row][col][layer]
        mode.piece = temp
        if onblock == True:
            temprow = mode.crowrow
            tempcol = mode.crowcol
            mode.destblockx = mode.crowrow = tempcol
            mode.destblocky = mode.crowcol = 4 - temprow
            mode.destblockx
            
            tempx, tempy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
            mode.crowx = tempx
            mode.crowy = tempy - mode.cubesize

    def clickPiece(mode, event):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    if mode.piece[row][col][layer] == True:
                        blockx, blocky = mode.getcoor(row, col, layer)
                        if abs(event.x - blockx) < mode.cubesize*3/2 and abs(event.y - blocky) < mode.cubesize*3/2:
                            return True
        return False
                        
    def nearLadder(mode, location):
        if location == "Bottom":
            if abs(mode.crowx - mode.ladx0) < mode.cubesize:
                if abs(mode.crowy - mode.lady0 + mode.cubesize)<mode.cubesize:
                    return True
        elif location == "Top":
            if abs(mode.crowx - mode.ladx1) < mode.cubesize:
                if abs(mode.crowy - mode.lady1 + mode.cubesize)<mode.cubesize:
                    return True
        return False
    
    #############################################
    ################## EVENTS ###################
    #############################################

    def keyPressed(mode, event):
        if event.key == "Right":
            mode.rotateallright()
        elif event.key == "Left":
            mode.rotateallleft()
        elif event.key == "Up":
            if mode.nearLadder("Bottom"):
                mode.crowx -= mode.cubewidth*2
                mode.crowy -= mode.cubesize*2
                mode.crowcol -= 2
                mode.crowlayer += 1
                mode.destblockx -= mode.cubewidth*2
                mode.destblocky -= mode.cubesize*2
        elif event.key == "Down":
            if mode.nearLadder("Top"):
                mode.crowx += mode.cubewidth*2
                mode.crowy += mode.cubesize*2
                mode.destblockx += mode.cubewidth*2
                mode.destblocky += mode.cubesize*2
                mode.crowcol += 2
                mode.crowlayer -= 1
        if event.key == "r":
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
        if event.x >= 360 and event.y >= 560 and event.x <= 380 and event.y <= 580:
            mode.app.setActiveMode(mode.app.instructionMode)
        if event.x >= 330 and event.y >= 560 and event.x <= 350 and event.y <= 580:
            mode.appStarted()
        if event.x >= 300 and event.y >= 560 and event.x <= 320 and event.y <= 580:
            mode.ai()
        if event.x >= 300 and event.y >= 480 and event.x <= 380 and event.y <= 550:
            if mode.aistart == True:
                mode.app.setActiveMode(mode.app.gameOver)
        else:
            mode.targetx = event.x
            mode.targety = event.y
            if mode.checkValid(event.x, event.y) == True:
                mode.yeet = True

    
    def rightMousePressed(mode, event):
        if mode.clickPiece(event):
            mode.rotateright()

    #############################################
    ################### VIEW ####################
    #############################################

    #draw all
    def redrawAll(mode, canvas):
        mode.drawGradient(canvas)
        mode.drawGrid(canvas)
        mode.drawLadder(canvas)
        mode.drawButton(canvas)
        mode.drawDude(canvas)
        mode.drawHelper(canvas)
        if mode.aistart == True:
            mode.drawAI(canvas)

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
            fill = 'thistle4', text = "L E V E L  3",
            font = "Arial 20 bold italic")
        canvas.create_text(mode.width/2, 50,
            fill = 'white', text = "L E V E L  3",
            font = "Arial 20 bold italic")
 
    def drawGrid(mode, canvas):
        destr, destc, destl = mode.destination
        for row in range(len(mode.board)):
            for col in range(len(mode.board[0])):
                for layer in range(len(mode.board[0][0])):
                    if mode.board[row][col][layer] == True:
                        x, y = mode.getcoor(row, col, layer)
                        if (row, col, layer) == (4,6,6) and mode.piece[1][2][2] == True:
                            mode.illusion(canvas)
                        elif row == destr and col == destc and layer == destl:
                            
                            mode.drawCube(canvas, x, y, "destination")
                            canvas.create_oval(x - 10, y - 16,
                            x + 10, y - 8, 
                            outline = 'lightskyblue1', width = 3)
                        else:
                            mode.drawCube(canvas, x, y, "normal")
                    if mode.piece[row][col][layer] == True:
                        x, y = mode.getcoor(row, col, layer)
                        mode.drawCube(canvas, x, y, "moving")

    def drawLadder(mode, canvas):
        (startr, startc, startl),(finr, finc, finl) = mode.ladder
        
        startx, starty = mode.getcoor(startr, startc, startl)
        finx, finy = mode.getcoor(finr, finc, finl)
        canvas.create_polygon(startx,starty,
                        finx,finy,
                        finx, starty- mode.cubesize,
                        startx,starty,
                        outline = 'white', fill = 'thistle')
        canvas.create_polygon(startx, starty,
                        startx + mode.cubewidth, starty - mode.cubesize/2-1,
                        finx + mode.cubewidth -2, finy - mode.cubesize/2 - 1,
                        finx, finy, outline = 'white', fill = 'plum4')


    def illusion(mode, canvas):               
        #fix overlapping problems
        x, y = mode.getcoor(0,2,2)
        cubew = mode.cubesize * math.sqrt(3)
        halfsize = mode.cubesize // 2
        canvas.create_polygon(  x, y - mode.cubesize,
                            x - cubew//2, y + halfsize - mode.cubesize,
                            x, y,
                            x + cubew//2, y + halfsize - mode.cubesize,
                            width =0,
                            outline = 'white', fill ='lavender blush')
        canvas.create_polygon(  x, y,
                            x + cubew//2, y - halfsize,
                            x + cubew//2, y + halfsize,
                            x, y + mode.cubesize,
                            width =0,
                            outline = 'plum3', fill = 'plum4')  
            
        
    #draw individual cubes
    def drawCube(mode, canvas, x, y, piecetype):
        if piecetype == "normal":
            color = ['lavender blush', 'thistle', 'plum4']
        elif piecetype == "moving":
            color = ['pink', 'pale violet red', 'maroon']
        elif piecetype == "destination":
            color = ['skyblue1', 'royal blue', 'midnight blue']
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
        canvas.create_oval(mode.destblockx - 5, mode.destblocky - 3 - mode.cubesize/2,
            mode.destblockx + 5, mode.destblocky+3 - mode.cubesize/2, outline = "red")
        canvas.create_image(mode.crowx, mode.crowy, image = ImageTk.PhotoImage(mode.crow))



    #draw instruction box
    def drawHelper(mode, canvas):
        canvas.create_rectangle(360, 560, 380, 580, outline = 'white')
        canvas.create_text(370, 569, fill = 'white', text = "?",
            font = 'Arial 16')
        canvas.create_rectangle(330, 560, 350, 580, outline = 'white')
        canvas.create_text(340, 569, fill = 'white', text = "R",
            font = 'Arial 16')
        canvas.create_rectangle(300, 560, 320, 580, outline = 'white')
        canvas.create_text(310, 569, fill = 'white', text = "AI",
            font = 'Arial 16')

    def drawAI(mode, canvas):
        canvas.create_rectangle(10, 480, 290, 580, outline = 'white')
        canvas.create_text(150,492,text='P A T H  S O L U T I O N',
            font = 'Arial 14 bold', fill = 'white')
        canvas.create_line(70,500,230,500,fill = 'white')
        canvas.create_text(150, 507,
            text = 'start from (row, col, layer) = (4,1,0)', font = 'Arial 10',
            fill = 'white')
        for i in range(len(mode.visited)-1):
            canvas.create_text(40 + i//5 * 70, 520 + i % 5 * 13,
                text = f'{i+1}. {mode.visited[i+1]}', font = 'Arial 9', fill = 'white')
        
        canvas.create_rectangle(300,480,380,550, outline = 'white')
        canvas.create_text(340,515, text = ' N E X T\nL E V E L', fill = 'white', font = 'Arial 14 bold')


# class MyModalApp(ModalApp):
#     def appStarted(app):
#         app.levelThree = LevelThree()
#         app.setActiveMode(app.levelThree)

# app = MyModalApp(width=400, height=600)