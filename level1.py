from modified_cmu_112_graphics import * #from class 
import tkinter as tk
import random
import math

class LevelOne(Mode):
    #initialize variables
    def appStarted(mode):
        mode.rows = 9
        mode.cols = 9
        mode.layers = 9
        mode.cubesize = 30
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
        mode.destination = (0,0,4)
        (mode.destr, mode.destc, mode.destl) = mode.destination
        mode.destblockx = 0
        mode.destblocky = 0
        mode.visited = []
        mode.checked = []
        mode.animate = False
        mode.reached = False
        mode.aistart = False
        mode.done = False
        mode.counter = 0
        mode.rotated = 0


    #helper function, modified from class notes
    def make3dlist(mode, x, y, z): 
        return [[ [None for col in range(x)] for col in range(y)] for row in range(z)] 

    #creates building structure
    def structure(mode):
        mode.board[4][1][0] = True
        mode.board[4][0][0] = True
        for elem in range(5):
            mode.board[4][0][elem] = True
        #top
        mode.board[4][1][4] = True
        for elem in range(5):
            mode.board[elem][0][4] = True
        for elem in range(5):
            mode.board[0][elem][4] = True
        mode.board[1][4][4] = True

        #right L
        mode.board[0][3][0] = True
        mode.board[0][4][0] = True
        mode.board[1][4][0] = True

        #button island
        mode.board[6][2][0] = True
        mode.board[6][3][0] = True

    #creates button, alters structure if hit
    def button(mode):
        mode.buttonrow = 0
        mode.buttoncol = 3
        mode.buttonlayer = 0
        mode.buttonrow2,mode.buttoncol2,mode.buttonlayer2 = (4,7,4)
        if mode.buttonhit == False:
            mode.piece[4][2][0] = True
            mode.piece[4][3][0] = True
            mode.piece[4][4][0] = True
            mode.piece[3][4][0] = True
            mode.piece[2][4][0] = True
        elif mode.buttonhit == True:
            for row in range(mode.rows):
                for col in range(mode.cols):
                    for layer in range(mode.layers):
                        if mode.piece[row][col][0] == True:
                            mode.piece[row][col][4] = True
                            mode.piece[row][col][0] = False

    def resetpiece(mode):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    mode.piece[row][col][layer] = False
        mode.piece[4][2][0] = True
        mode.piece[4][3][0] = True
        mode.piece[4][4][0] = True
        mode.piece[3][4][0] = True
        mode.piece[2][4][0] = True



    #initializes character
    def lildude(mode):
        #import crow image
        mode.crow = mode.scaleImage(mode.loadImage("crowL.png"), 0.5 * mode.cubesize/40)
        #start location for crow
        mode.startrow = 4
        mode.startcol = 1
        mode.startlayer = 0
        mode.startx, mode.starty = mode.getcoor(mode.startrow, mode.startcol, mode.startlayer)
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
        if mode.animate == True:
            mode.counter += 1
            if mode.counter == 1:
                mode.resetpiece()
            elif mode.counter == 20:
                mode.rotateright()
            if mode.counter <= (len(mode.visited)-1)*2:
                (mode.crowrow, mode.crowcol, mode.crowlayer) = mode.visited[mode.counter//2]
                pathx, pathy = mode.getcoor(mode.crowrow-1, mode.crowcol-1, mode.crowlayer)
                mode.crowx, mode.crowy = pathx, pathy
            else:
                mode.animate = False

        if (mode.crowrow, mode.crowcol, mode.crowlayer) == (4, 6, 0):
            (mode.crowrow, mode.crowcol, mode.crowlayer) = (4,6,4)
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
            mode.app.setActiveMode(mode.app.levelTwo)

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
        if (row,col,layer) == (0,3,0):
            (row,col,layer) = (4,7,4)
        if (row, col, layer) in mode.checked:
            return False
        mode.checked.append((row, col, layer))
        for drow, dcol in [(-1,0),(1,0),(0,1),(0,-1)]:
            if mode.valid2(row, col, layer, (drow, dcol)):
                if mode.gettoclick(row+drow, col + dcol, layer, clickrow, clickcol, clicklayer):
                    mode.checked = []
                    return True
        mode.checked.pop()
        return False

    def valid2(mode, row, col, layer, direction):
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
        i, j = 0, 0
        while i < 4:
            if mode.gettobutton(mode.startrow, mode.startcol, mode.startlayer) == True:
                break
            else:
                mode.rotated += 1
                mode.rotateright()
                i += 1

        while j < 4:
            if mode.gettodest(mode.crowrow, mode.crowcol, mode.crowlayer) == True:
                break
            else:
                mode.rotated += 1
                mode.rotateright()
                j += 1
        mode.animate = True

    #inspired by 15112 backtracking examples
    def gettobutton(mode, row, col, layer):
        if (row, col, layer) in mode.visited:
            return False
        mode.visited.append((row, col, layer))
        if (row, col, layer) == (mode.buttonrow, mode.buttoncol, mode.buttonlayer):
            #update values
            mode.crowrow, mode.crowcol, mode.crowlayer = mode.buttonrow2, mode.buttoncol2, mode.buttonlayer2
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

    #inspired by 15112 backtracking examples
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
                # print('valid', row+drow, col+dcol)
                if mode.gettodest(row+drow, col + dcol, layer):
                    return True
        mode.visited.pop()
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

    def rotateright(mode):
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        #rotate piece
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[col][8-row][layer] = mode.piece[row][col][layer]
        mode.piece = temp
       # move layers if button hit
        if mode.buttonhit == True:
            for row in range(mode.rows):
                for col in range(mode.cols):
                    for layer in range(mode.layers):
                        if mode.piece[row][col][0] == True:
                            mode.piece[row][col][4] = True
                            mode.piece[row][col][0] = False
    

    def rotateallright(mode):
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        temp2 = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[4-col][row][layer] = mode.board[row][col][layer]
                    temp2[4-col][row][layer] = mode.piece[row][col][layer]
        mode.board = temp
        mode.piece = temp2
        mode.buttonrow, mode.buttoncol = 4 - mode.buttoncol, mode.buttonrow
        mode.startrow, mode.startcol = 4 - mode.startcol, mode.startrow
        

        (destr, destc, destl) = mode.destination
        tempr, tempc = destr, destc
        mode.destination = (4-tempc, tempr, destl)
        mode.destr, mode.destc, mode.destl = mode.destination

        temprow, tempcol = mode.crowrow, mode.crowcol
        mode.crowrow, mode.crowcol = 4 - tempcol, temprow 
        mode.crowx, mode.crowy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
        mode.crowy = mode.crowy - mode.cubesize



    def rotateallleft(mode):
        temp = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        temp2 = mode.make3dlist(mode.rows, mode.cols, mode.layers)
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    temp[col][4-row][layer] = mode.board[row][col][layer]
                    temp2[col][4-row][layer] = mode.piece[row][col][layer]
        mode.board = temp
        mode.piece = temp2
        mode.buttonrow, mode.buttoncol = mode.buttoncol, 4 - mode.buttonrow
        mode.startrow, mode.startcol = 4 - mode.startcol, mode.startrow

        (destr, destc, destl) = mode.destination
        tempr, tempc = destr, destc
        mode.destination = (tempc, 4 - tempr, destl)

        temprow, tempcol = mode.crowrow, mode.crowcol
        mode.crowrow, mode.crowcol = tempcol, 4 - temprow 
        mode.crowx, mode.crowy = mode.getcoor(mode.crowrow, mode.crowcol, mode.crowlayer)
        mode.crowy = mode.crowy - mode.cubesize



    def clickPiece(mode, event):
        for row in range(mode.rows):
            for col in range(mode.cols):
                for layer in range(mode.layers):
                    if mode.piece[row][col][layer] == True:
                        blockx, blocky = mode.getcoor(row, col, layer)
                        if abs(event.x - blockx) < mode.cubesize*3/2 and abs(event.y - blocky) < mode.cubesize*3/2:
                            return True
        return False
    
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
        if event.x >= 360 and event.y >= 560 and event.x <= 380 and event.y <= 580:
            mode.app.setActiveMode(mode.app.instructionMode)
        if event.x >= 330 and event.y >= 560 and event.x <= 350 and event.y <= 580:
            mode.appStarted()
        if event.x >= 300 and event.y >= 560 and event.x <= 320 and event.y <= 580:
            mode.ai()
        if event.x >= 300 and event.y >= 480 and event.x <= 380 and event.y <= 550:
            if mode.aistart == True:
                mode.app.setActiveMode(mode.app.levelTwo)
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
            fill = 'thistle4', text = "L E V E L  1",
            font = "Arial 20 bold italic")
        canvas.create_text(mode.width/2, 50,
            fill = 'white', text = "L E V E L  1",
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
                    
        #fix overlapping problems
        if mode.piece[4][6][4] == True:
            x, y = mode.getcoor(4,7,4)
            mode.drawCube(canvas, x,y,"normal")
            x, y = mode.getcoor(4,8,4)
            mode.drawCube(canvas, x,y,"normal")
            x, y = mode.getcoor(5,8,4)
            mode.drawCube(canvas, x,y,"normal")
        
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
                text = f'{i+1}. {mode.visited[i+1]}', font = 'Arial 10', fill = 'white')
        
        canvas.create_rectangle(300,480,380,550, outline = 'white')
        canvas.create_text(340,515, text = ' N E X T\nL E V E L', fill = 'white', font = 'Arial 14 bold')
    

# class MyModalApp(ModalApp):
#     def appStarted(app):
#         app.levelOne = LevelOne()
#         app.setActiveMode(app.levelOne)

# app = MyModalApp(width=400, height=600)