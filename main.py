'''
image sources:
-clouds.png from https://gifer.com/en/WMV
-crowL.png + crownR.png: crow design from Monument Valley (https://monumentvalley.fandom.com/wiki/Crows), 
    -redrawn by me
-citybg.png: from https://wallpaperaccess.com/pixel-aesthetic
-ocean1.png-ocean15.png: gif from https://weheartit.com/entry/22698728
-titlebg.png from https://www.rawpixel.com/image/541554/premium-illustration-vector-background-gradient-holographic

code sources:
-modified_cmu_112_graphics file from “cmu_112_graphics.py” from 15112 course
    -modified to include my own right clicking bind
-make3dlist function modified from make2dlist from 15112 course notes
-AI inspired by backtracking done in class 15112
-rbg to hex conversion from https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python

'''

from modified_cmu_112_graphics import * #from class 
import tkinter as tk
import random
import math

import level1
import level2
import level3
import levelbuilder

class TitleScreenMode(Mode):
    def appStarted(mode):
        mode.bg = mode.scaleImage(mode.loadImage("citybg.png"), 0.6)
        mode.margin = 100
        mode.yupbound = 480
        mode.ydownbound = 420

    def keyPressed(mode, event):
        if event.key == "1":
            mode.app.setActiveMode(mode.app.levelOne)
        elif event.key == "2":
            mode.app.setActiveMode(mode.app.levelTwo)
        elif event.key == "3":
            mode.app.setActiveMode(mode.app.levelThree)
        elif event.key == "4":
            mode.app.setActiveMode(mode.app.levelBuilder)

    def mousePressed(mode, event):
        #"begin"
        if (event.x >= mode.margin and event.x <= (mode.width - mode.margin) and
            event.y <= mode.yupbound and event.y >= mode.ydownbound):
            mode.app.setActiveMode(mode.app.levelOne)
        #"instructions"
        elif (event.x >= mode.margin and event.x <= (mode.width - mode.margin) and
            event.y <= mode.yupbound - 100 and event.y >= mode.ydownbound - 100):
            mode.app.setActiveMode(mode.app.levelBuilder)
        elif (event.x >= mode.margin and event.x <= (mode.width - mode.margin) and
            event.y <= mode.yupbound - 200 and event.y >= mode.ydownbound - 200):
            mode.app.setActiveMode(mode.app.instructionMode)
        
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, 
            image = ImageTk.PhotoImage(mode.bg))
        mode.drawButtons(canvas)
    
    #normal mode
    def drawButtons(mode, canvas):
        #game title
        canvas.create_text(mode.width/2 + 3, 123,
            fill = 'thistle', text = "D E L I R I U M",
            font = "Arial 50 bold italic")
        canvas.create_text(mode.width/2, 120,
            fill = 'white', text = "D E L I R I U M",
            font = "Arial 50 bold italic")
        #level builder
        canvas.create_rectangle(mode.margin, mode.yupbound -200,
            mode.width - mode.margin, mode.ydownbound - 200,
            outline = 'white', width = 2)
        canvas.create_text(mode.width/2, (mode.yupbound+mode.ydownbound)/2 - 200,
            fill = 'white', text = "I N S T R U C T I O N S",
            font = "Arial 14 italic")
        #instruction
        canvas.create_rectangle(mode.margin, mode.yupbound -100,
            mode.width - mode.margin, mode.ydownbound - 100,
            outline = 'white', width = 2)
        canvas.create_text(mode.width/2, (mode.yupbound+mode.ydownbound)/2 - 100,
            fill = 'white', text = "L E V E L  B U I L D E R",
            font = "Arial 14 italic")
        #begin
        canvas.create_rectangle(mode.margin, mode.yupbound,
            mode.width - mode.margin, mode.ydownbound,
            outline = 'white', width = 2)
        canvas.create_text(mode.width/2, (mode.yupbound+mode.ydownbound)/2,
            fill = 'white', text = "B E G I N",
            font = "Arial 14 italic")

class InstructionMode(Mode):
    def appStarted(mode):
        mode.bg = mode.loadImage("titlebg.png")

    def mousePressed(mode, event):
        #go back to normal mode
        if (event.x >=10 and event.x <= 40 and event.y >= 10 and event.y <= 40):
            mode.app.setActiveMode(mode.app.titleScreenMode)
        
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, 
            image = ImageTk.PhotoImage(mode.bg))
        mode.drawInstructions(canvas)
    
    #instruction mode
    def drawInstructions(mode, canvas):
        #title
        canvas.create_text(mode.width/2 + 3, 123,
            fill = 'thistle', text = "I N S T R U C T I O N S",
            font = "Arial 35 bold italic")
        canvas.create_text(mode.width/2, 120,
            fill = 'white', text = "I N S T R U C T I O N S",
            font = "Arial 35 bold italic")
        #instructions
        canvas.create_text(mode.width/2, mode.height/2,
            fill = 'maroon', font = "Arial 12 italic",
            text = "\n\n\n\n      M O V E M E N T :\n\nLEFT CLICK ON CENTER OF TILE TO MOVE\n\nRIGHT CLICK TO ROTATE RED TILES\n\nPRESS RIGHT/LEFT TO ROTATE STRUCTURE\n\nPRESS UP/DOWN TO CLIMB STAIRS\n\n\n      F E A T U R E S :\n\nBUTTONS CHANGE STRUCTURE\n\nA SOLVES PUZZLE WITH AI\n\nR RESTARTS LEVEL\n\n? BRINGS UP INSTRUCTION PAGE\n\nREACH THE BLUE PODIUM TO ADVANCE")
        #backwards arrow
        canvas.create_rectangle(10, 10, 40, 40, outline = 'white', width = 4)
        canvas.create_line(15, 25, 25, 15, fill = 'white', width = 4)
        canvas.create_line(15, 25, 35, 25, fill = 'white', width = 4)
        canvas.create_line(15, 25, 25, 35, fill = 'white', width = 4)

class GameOver(Mode):
    def appStarted(mode):
        mode.image = "ocean1.png"
        mode.bg = mode.scaleImage(mode.loadImage(mode.image), 1.6)
        mode.clouds = mode.scaleImage(mode.loadImage("clouds.png"), 1)
        mode.margin = 100
        mode.yupbound = 480
        mode.ydownbound = 420
        mode.counter = 1
        mode.counter2 = 0
        mode.up = True

    def mousePressed(mode, event):
        #"try again"
        if (event.x >= mode.margin and event.x <= (mode.width - mode.margin) and
            event.y <= mode.yupbound and event.y >= mode.ydownbound):
            mode.app.appStarted()
            mode.app.setActiveMode(mode.app.titleScreenMode)
        
    def timerFired(mode):
        if mode.up == True:
            mode.counter += 1
            if mode.counter == 15:
                mode.up = False
        elif mode.up == False:
            mode.counter -= 1
            if mode.counter == 1:
                mode.up = True
                
        mode.image = "ocean" + str(mode.counter) + ".png"
        mode.bg = mode.scaleImage(mode.loadImage(mode.image), 1.6)
        mode.counter2 += 5
        
        
    def redrawAll(mode, canvas):
        #bg
        canvas.create_image(mode.width/2, mode.height/2, 
            image = ImageTk.PhotoImage(mode.bg))
        mode.gradient(canvas)
        #title
        canvas.create_text(mode.width/2 + 3, 123,
            fill = 'pale violet red', text = "G A M E  O V E R",
            font = "Arial 40 bold italic")
        canvas.create_text(mode.width/2, 120,
            fill = 'royalblue4', text = "G A M E  O V E R",
            font = "Arial 40 bold italic")
        #clouds
        canvas.create_image(mode.counter2%1200 - 200, mode.height/4, 
            image = ImageTk.PhotoImage(mode.clouds))
        canvas.create_image(mode.counter2%1800 - 800, mode.height/4, 
                image = ImageTk.PhotoImage(mode.clouds))
        #try again
        canvas.create_rectangle(mode.margin, mode.yupbound,
            mode.width - mode.margin, mode.ydownbound,
            outline = 'white', width = 2)
        canvas.create_text(mode.width/2, (mode.yupbound+mode.ydownbound)/2,
            fill = 'white', text = "P L A Y  A G A I N",
            font = "Arial 14 italic")

    def gradient(mode, canvas):
        #desired rgb values
        startr, startg, startb = 49, 60, 80
        endr, endg, endb = 80, 190, 140
        #create lines to display solid gradient
        for i in range(255//5):
            newr = startr + (endr - startr) * i * 5 // 250
            newg = startg + (endg - startg) * i * 5 // 250
            newb = startb + (endb - startb) * i * 5 // 250
            #rbg to hex conversion from https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python
            newhex = '#%02x%02x%02x' % (newr, newg, newb)
            canvas.create_line(0, i*5, mode.width, i*5, fill = newhex, width = 5)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.instructionMode = InstructionMode()
        app.gameOver = GameOver()
        app.levelOne = level1.LevelOne()
        app.levelTwo = level2.LevelTwo()
        app.levelThree = level3.LevelThree()
        app.levelBuilder = levelbuilder.LevelBuilder()
        app.playThrough = levelbuilder.PlayThrough()

        app.setActiveMode(app.titleScreenMode)
        # app.setActiveMode(app.levelTwo)
        # app.setActiveMode(app.levelOne)
        # app.setActiveMode(app.gameOver)

app = MyModalApp(width=400, height=600)

