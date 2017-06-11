# Winston Zhou
# Carnegie Mellon University

#template from 15-112 course website for delta graphics
#https://www.cs.cmu.edu/~112/notes/deltaGraphicsDemo2.py

from tkinter import *
from time import clock
from math import floor, ceil, pi
from pygame import mixer
from random import randrange
import os
import csv

def init(data):
    data.inMenu = True
    data.inInstruction = False
    data.drawInstructionsNow = False
    data.transitionToGame = False
    data.drawTransitionGameNow = False
    data.waitingOnReturnToMenu = False
    data.returningToMenuNow = False
    data.inGame = False
   
    data.waitingOnClock = False #set to TRUE once game begins #stage where clock has not been revealed
    data.waitingOnReveal = False #waiting for question to be revealed
    data.waitingOnUserAnswerChoice = False #waiting for user to select answer
    data.waitingOnVerify = False #waiting to verify selected answer
    data.clockRunning = False #True when clock starts counting
    data.waitingOnShortReveal = False #True to reveal next question without introducing time
    data.waitingOSwitchQuestion = False #for switch the question lifeline
    data.ranOutOfTime = False #True if user runs out of time
    data.gameOver = False 
    data.waitingOnDisplayWinnings = False #True if about to display winnings (game over)
    data.displayTotalWinningsNow = False

    data.readyForDeltaDraw = False
    data.currentQuestion = 0
    data.clockAmounts = [15, 15, 15, 15, 15,
                         30, 30, 30, 30, 30,
                         45, 45, 45, 45, 45]
    data.timeLeft = data.clockAmounts[data.currentQuestion] #timeLeft serve as countdown time
    data.timerSeconds = data.clockAmounts[data.currentQuestion] 
    data.resumeTime = None #used when resuming a clock
    data.bankedTime = 0 #seconds
    data.revealAnswerDelay = 8 #seconds delay before answers are revealed
    #whereas timerSeconds serves as a way to know total time for question
    data.drawArc = True
    data.startClock = False
    data.activateCircle = False
    data.activateCircleIterations = 150 #frames total
    data.shiftUpHeight = 150
    data.questionBarSwitch = True #switch turns False once startTime decided
    data.semicircularizeSwitch = True
    data.popoutDuration = 0.5
    data.revealQuestion = False #Set to True to reveal question once
    data.selectD = False
    data.selectC = False
    data.selectB = False
    data.selectA = False
    data.selectedAnswer = None #becomes the answer user selects {A,B,C,D}
    data.incorrectSelected = None #for use when user selects incorrect answer
    data.verifyNow = False #True when ready to Verify selection
    data.shortRevealNow = False
    data.longRevealNow = False
    data.winAmounts = ["$100", "$200", "$300", "$500", "$1,000",
                       "$2,000", "$4,000", "$8,000", "$16,000", "$32,000",
                       "$64,000", "$125,000", "$250,000", "$500,000",
                       "MILLIONAIRE"]
    data.winAmountsLabel = ["$100", "$200", "$300", "$500", "$1,000",
                       "$2,000", "$4,000", "$8,000", "$16,000", "$32,000",
                       "$64,000", "$125,000", "$250,000", "$500,000",
                       "$1 MILLION", "$0"]
    data.guaranteedAmounts = ["$0", "$0", "$0", "$0", "$0",
                              "$1,000", "$1,000", "$1,000", "$1,000", "$1,000",
                              "$32,000", "$32,000", "$32,000", "$32,000", "$32,000"]

    #CSV_FILENAME is the path to the csv file which contains the questions and answers
    data.CSV_FILENAME = os.path.dirname(os.path.realpath(__file__)) + os.sep + "game_data.csv"
    data.currentQuestionAttributes = None
    data.q0 = []
    data.q1 = []
    data.q2 = []
    data.q3 = []
    data.q4 = []
    data.q5 = []
    data.q6 = []
    data.q7 = []
    data.q8 = []
    data.q9 = []
    data.q10 = []
    data.q11 = []
    data.q12 = []
    data.q13 = []
    data.questionsContainer = [data.q0, data.q1, data.q2, data.q3, data.q4, 
                               data.q5, data.q6, data.q7, data.q8, data.q9,
                               data.q10, data.q11, data.q12, data.q13]
    data.questionLine1or2 = False
    data.cylinderGiven = False #True once a cylinder question has been generated
    data.dynamicGeneration = True #False when given within 5 questions

    #Lifelines
    data.usedFiftyFifty = False
    data.tempPreventFifty = False
    data.fiftyFiftyActivate = False
    data.removedA = False #in the event an answer choice was removed by a lifeline
    data.removedB = False
    data.removedC = False
    data.removedD = False
    data.usedDoubleDip = False
    data.tempPreventDip = False
    data.doubleDipActivate = False
    data.doubleDipActivate2 = False #special if infinite time was used
    data.usedSwitchQuestion = False
    data.tempPreventSwitch = False
    data.switchQuestionActivate = False
    data.justUsedSwitch = False
    data.switchQuestionNow = False
    data.usedInfiniteTime = False
    data.tempPreventInfiniteTime = False
    data.infiniteTimeActivate = False
    data.resume100Bed = False
    data.clockAlreadyFaded = False
    data.lifelinesRemaining = 4 #deletes "Key:" label once this is 0
    data.lifelinesMillionRemoveSwitch = False

    # https://www.pygame.org/docs/ref/mixer.html
    #adapted from http://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
    data.iconPath = os.path.dirname(os.path.realpath(__file__)) + os.sep + "music" + os.sep + "wwtbam.ico"
    data.path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "music" + os.sep
    mixer.init() #pygame music playing
    data.channel0 = mixer.Channel(0)
    data.channel1 = mixer.Channel(1)
    data.channel2 = mixer.Channel(2)
    data.channel3 = mixer.Channel(3)
    data.letsPlaySounds = ["100-1000lp.wav", "100-1000lp.wav", "100-1000lp.wav", "100-1000lp.wav", "100-1000lp.wav",
                            "2000lp.wav", "4000lp.wav", "8000lp.wav", "16000lp.wav", "32000lp.wav",
                            "64000lp.wav", "125000lp.wav", "250000lp.wav", "500000lp.wav", "1000000lp.wav"]
    data.questionLetsPlay = mixer.Sound(data.path + data.letsPlaySounds[data.currentQuestion])
    data.revealClockSound = mixer.Sound(data.path + "revealclock.wav")
    data.revealQuestionSound = mixer.Sound(data.path + "revealquestion.wav")
    data.tickingSounds = ["100-1000tick.wav", "100-1000tick.wav", "100-1000tick.wav", "100-1000tick.wav", "100-1000tick.wav",
                          "2000tick.wav", "4000tick.wav", "8000tick.wav", "16000tick.wav", "32000tick.wav",
                          "64000tick.wav", "125000tick.wav", "250000tick.wav", "500000tick.wav", "millStart.ogg"]
    data.questionTicking = mixer.Sound(data.path + data.tickingSounds[data.currentQuestion])
    data.questions100to1000Bed = mixer.Sound(data.path + "100-1000bed.ogg")
    data.finalAnswerSounds = ["100final.wav", "200final.wav", "300final.wav", "500final.wav", "1000final.wav",
                              "2000final.wav", "4000final.wav", "8000final.wav", "16000final.wav", "32000final.wav",
                              "2000final.wav", "4000final.wav", "8000final.wav", "16000final.wav", "32000final.wav"]
    data.questionFinalAnswer = mixer.Sound(data.path + data.finalAnswerSounds[data.currentQuestion])
    data.wrongSounds = ["100-1000lose.wav", "100-1000lose.wav", "100-1000lose.wav", "100-1000lose.wav", "100-1000lose.wav",
                        "2000lose.wav", "4000lose.wav", "8000lose.wav", "16000lose.wav", "32000lose.wav",
                        "2000lose.wav", "4000lose.wav", "8000lose.wav", "16000lose.wav", "1000000lose.wav"]
    data.questionWrong = mixer.Sound(data.path + data.wrongSounds[data.currentQuestion])
    data.correctSounds = ["100-1000win.wav", "100-1000win.wav", "100-1000win.wav", "100-1000win.wav", "1000win.wav",
                          "2000win.wav", "4000win.wav", "8000win.wav", "16000win.wav", "1000win.wav",
                          "64000win.wav", "125000win.wav", "250000win.wav", "500000win.wav", "millwin.wav"]
    data.questionCorrect = mixer.Sound(data.path + data.correctSounds[data.currentQuestion])
    data.oldBeds = ["2000old.ogg", "2000old.ogg", "2000old.ogg", "2000old.ogg", "2000old.ogg",
                    "2000old.ogg", "4000old.ogg", "8000old.ogg", "16000old.ogg", "32000old.ogg",
                    "64000old.ogg", "125000old.ogg", "250000old.ogg", "500000old.ogg", "1000000old.ogg"]
    data.oldBed = mixer.Sound(data.path + data.oldBeds[data.currentQuestion])
    data.winningsSizzle = mixer.Sound(data.path + "winsizzle.wav")
    data.fiftyFiftySound = mixer.Sound(data.path + "5050.wav")
    data.switchBed = mixer.Sound(data.path + "switchBed.ogg")
    data.switchAnswer = mixer.Sound(data.path + "switchAnswer.wav")
    data.switchSpecialCue = mixer.Sound(data.path + "switchSpecialCue.wav")
    data.doubleDipBed = mixer.Sound(data.path + "ddbed.wav")
    data.doubleDipAnswer1 = mixer.Sound(data.path + "ddanswer1.wav")
    data.doubleDipAnswer2 = mixer.Sound(data.path + "ddanswer2.wav")
    data.doubleDipWrong = mixer.Sound(data.path + "ddwrong.wav")
    data.stopClock = mixer.Sound(data.path + "stopclock.wav")
    data.resumeClock = mixer.Sound(data.path + "resumeclock.wav")
    data.outOfTimeSound = mixer.Sound(data.path + 'outoftime.wav')
    data.totalWinningsSound = mixer.Sound(data.path + 'totalWinnings.wav')
    data.titlePageIntro = mixer.Sound(data.path + 'titlemusic.wav')
    data.instructionsMusic = mixer.Sound(data.path + 'rulesMusic.wav')
    data.bankedTimeMusic = mixer.Sound(data.path + "bankedTime.wav")
    data.millLast = mixer.Sound(data.path + "mill21left.wav")
    data.finalQuestionReveal = mixer.Sound(data.path + "finalRevealSound.wav")
    data.glintSound = mixer.Sound(data.path + "glint.wav")
    data.glintSwitch = False
    data.millLastSwitch = False #True once millLast starts playing
    data.channel0.play(data.titlePageIntro)

    data.instructionsBottom = "Press [Spacebar] to start game"
    data.instructionsTop = ""
    
########Question Bar###################################### 
    data.questionWidth = 490
    #left side
    data.topleftx = 170
    data.toplefty = 600 #how far down the question bar is
    data.toprightx = 1230 # how wide is the bar
    data.toprighty = data.toplefty

    data.bottomleftx = data.topleftx
    data.bottomlefty = data.toplefty + 115 #115 is gap between top and bottom
    data.bottomrightx = data.toprightx
    data.bottomrighty = data.toprighty + 115 #115 is gap between top and bottom

#######Answer Choice top left 
    #left side
    data.topleftx1 = 140
    data.toplefty1 = data.bottomlefty + 15
    data.toprightx1 = 630 # how wide is the bar
    data.toprighty1 = data.toplefty1

    data.bottomleftx1 = data.topleftx1
    data.bottomlefty1 = data.toplefty1 + 72 #72 is gap between top and bottom
    data.bottomrightx1 = data.toprightx1
    data.bottomrighty1 = data.toprighty1 + 72 #72 is gap between top and bottom

#######Answer Choice top right
    #left side
    data.topleftx2 = 770
    data.toplefty2 = data.bottomlefty + 15
    data.toprightx2 = 1260 # how wide is the bar
    data.toprighty2 = data.toplefty2

    data.bottomleftx2 = data.topleftx2
    data.bottomlefty2 = data.toplefty2 + 72 #72 is gap between top and bottom
    data.bottomrightx2 = data.toprightx2
    data.bottomrighty2 = data.toprighty2 + 72 #72 is gap between top and bottom

#######Answer Choices bottom left
    #left side
    data.topleftx3 = 140
    data.toplefty3 = data.bottomlefty2 + 15
    data.toprightx3 = 630 # how wide is the bar
    data.toprighty3 = data.toplefty3

    data.bottomleftx3 = data.topleftx3
    data.bottomlefty3 = data.toplefty3 + 72 #72 is gap between top and bottom
    data.bottomrightx3 = data.toprightx3
    data.bottomrighty3 = data.toprighty3 + 72 #72 is gap between top and bottom

#######Answer Choice bottom right
    #left side
    data.topleftx4 = 770
    data.toplefty4 = data.bottomlefty2 + 15
    data.toprightx4 = 1260 # how wide is the bar
    data.toprighty4 = data.toplefty4

    data.bottomleftx4 = data.topleftx4
    data.bottomlefty4 = data.toplefty4 + 72 #72 is gap between top and bottom
    data.bottomrightx4 = data.toprightx4
    data.bottomrighty4 = data.toprighty4 + 72 #72 is gap between top and bottom

#######Clock Animations 
    data.colors=[] #nested list for each circle's color
    data.circlesLeft=[]
    data.circlesRight=[]
    for j in range(15):
        data.colors.append([0-j*16,0-j*15,0-j*15,0]) #[R,G,B,switch]
        #switch: 0 for black to active; 1 for active to inert algorithm
        #the list artifically delays the animation for outer circles
        #by giving those circles negative RGB amounts for the delay period
    data.currentcir = 14 #selects which circles to be activated
    data.inerttoactiveswitch = 0

#create clock circle variables 
    data.xtop1 = 700
    data.ytop1 = 600
    data.xbottom1 = data.xtop1
    data.ybottom1 = data.ytop1
    data.xtop2 = data.xtop1
    data.ytop2 = data.ytop1
    data.xbottom2 = data.xtop1
    data.ybottom2 = data.ytop1
    data.xtop3 = data.xtop1
    data.ytop3 = data.ytop1
    data.xbottom3 = data.xtop1
    data.ybottom3 = data.ytop1
    data.timeTextX = data.xtop1
    data.timeTextY = data.ytop1
    data.startvalue=269 #initial start value for pieslice
    data.extentvalue=359 #intial extent value for pieslice
    data.resumeExtent = None #used if resuming clock
    data.currentSecond = 0 #used to determine whether inerttoactive circle should be activated
    data.clockFontSize = 48
    data.diametershrinktime = 0.5
    data.semicircularizeTime = 0.5
    data.startTimeDotSwitch = False
    
def mousePressed(event, data):
    if data.inMenu:
        if event.x > 735 and event.x < 1304 and event.y > 578 and event.y < 647:
            data.readyForDeltaDraw = True
            data.inMenu = False
            data.drawInstructionsNow = True
            data.inInstruction = True
        elif event.x > 101 and event.x < 664 and event.y > 578 and event.y < 647:
            data.readyForDeltaDraw = True
            data.inMenu = False
            data.transitionToGame = True
    if data.waitingOnUserAnswerChoice == True:
        if event.x > 101 and event.x < 664 and event.y > 578 and event.y < 647:
            if data.removedA == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectA = True
        elif event.x > 735 and event.x < 1304 and event.y > 578 and event.y < 647:
            if data.removedB == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectB = True
        elif event.x > 101 and event.x < 664 and event.y > 666 and event.y < 742:
            if data.removedC == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectC = True
        elif event.x > 735 and event.x < 1304 and event.y > 666 and event.y < 742:
            if data.removedD == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                    data.lifelinesRemaining -= 1
                else: data.verifyNow = True
                data.selectD = True
        elif event.x > 100 and event.x < 170 and event.y > 100 and event.y < 155:
            if data.usedFiftyFifty == False: #lifeline not used yet
                if data.tempPreventFifty == False: #not using double dip
                    data.channel2.play(data.fiftyFiftySound)
                    data.fiftyFiftyActivate = True
                    data.usedFiftyFifty = True
                    data.lifelinesRemaining -= 1
        elif event.x > 200 and event.x < 270 and event.y > 100 and event.y < 155:
            if data.usedDoubleDip == False:
                if data.tempPreventDip == False:
                    data.tempPreventFifty = True
                    data.tempPreventSwitch = True
                    data.tempPreventInfiniteTime = True
                    if data.currentQuestion < 5:
                        data.channel0.pause()
                        data.channel3.set_volume(0)
                    else:
                        data.channel0.set_volume(0)
                    data.channel1.play(data.doubleDipBed)
                    data.doubleDipActivate = True
                    data.usedDoubleDip = True
                    data.lifelinesRemaining -= 1
        elif event.x > 300 and event.x < 370 and event.y > 100 and event.y < 155:
            if data.usedSwitchQuestion == False:
                if data.tempPreventSwitch == False:
                    data.justUsedSwitch = True
                    data.instructionsTop = "Activated Switch the Question"
                    data.instructionsBottom = "Press [Spacebar] to reveal the answer"
                    mixer.stop()
                    data.channel0.play(data.switchBed)
                    data.switchQuestionActivate = True
                    data.usedSwitchQuestion = True
                    data.lifelinesRemaining -= 1
        elif event.x > 400 and event.x < 470 and event.y > 100 and event.y < 155:
            if data.usedInfiniteTime == False:
                if data.tempPreventInfiniteTime == False:
                    data.tempPreventSwitch = True
                    data.tempPreventFifty = True
                    if data.currentQuestion > 4:
                        mixer.stop()
                    else:
                        data.channel3.stop()
                    data.channel1.play(data.stopClock)
                    if data.currentQuestion > 4:
                        data.oldBed = mixer.Sound(data.path + data.oldBeds[data.currentQuestion])
                        data.channel0.play(data.oldBed)
                    data.infiniteTimeActivate = True
                    data.usedInfiniteTime = True
                    data.lifelinesRemaining -= 1

def keyPressed(event, data):
    if data.inMenu:
        if event.keysym == "i" or event.keysym == "I":
            data.readyForDeltaDraw = True
            data.inMenu = False
            data.drawInstructionsNow = True
            data.inInstruction = True
        elif event.keysym == "p" or event.keysym == "P":
            data.readyForDeltaDraw = True
            data.inMenu = False
            data.transitionToGame = True
    elif data.inInstruction:
        if event.keysym == "p" or event.keysym == "P":
            data.readyForDeltaDraw = True
            data.transitionToGame = True
    if data.waitingOnClock == True:
        if event.keysym == "space":
            data.instructionsBottom = "For the first 5 questions, you have 15 seconds on the clock"
            data.readyForDeltaDraw = True
            data.activateCircle = True
            data.waitingOnClock = False
            data.waitingOnReveal = True
    elif data.waitingOnReveal == True:
        if event.keysym == "space":
            data.instructionsTop = ""
            data.instructionsBottom = "Answers will appear when clock starts..."
            data.readyForDeltaDraw = True
            data.revealQuestion = True
            data.waitingOnReveal = False
    elif data.waitingOnUserAnswerChoice == True:
        if event.keysym == "d" or event.keysym == "D":
            if data.removedD == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectD = True
        elif event.keysym == "c" or event.keysym == "C":
            if data.removedC == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectC = True
        elif event.keysym == "b" or event.keysym == "B":
            if data.removedB == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectB = True
        elif event.keysym == "a" or event.keysym == "A":
            if data.removedA == False:
                data.clockRunning = False
                data.waitingOnUserAnswerChoice = False
                if data.doubleDipActivate == False: 
                    data.instructionsTop = ""
                    data.instructionsBottom = "Press [Spacebar] to reveal answer"
                    data.waitingOnVerify = True
                else: data.verifyNow = True
                data.selectA = True
        elif event.keysym == "5":
            if data.usedFiftyFifty == False: #lifeline not used yet
                if data.tempPreventFifty == False: #not using double dip
                    data.channel2.play(data.fiftyFiftySound)
                    data.fiftyFiftyActivate = True
                    data.usedFiftyFifty = True
                    data.lifelinesRemaining -= 1
        elif event.keysym == "2":
            if data.usedDoubleDip == False:
                if data.tempPreventDip == False:
                    data.tempPreventFifty = True
                    data.tempPreventSwitch = True
                    data.tempPreventInfiniteTime = True
                    if data.currentQuestion < 5:
                        data.channel0.pause()
                        data.channel3.set_volume(0)
                    else:
                        data.channel0.set_volume(0)
                    data.channel1.play(data.doubleDipBed)
                    data.doubleDipActivate = True
                    data.usedDoubleDip = True
                    data.lifelinesRemaining -= 1
        elif event.keysym == "s" or event.keysym == "S":
            if data.usedSwitchQuestion == False:
                if data.tempPreventSwitch == False:
                    data.justUsedSwitch = True
                    data.instructionsTop = "Activated Switch the Question"
                    data.instructionsBottom = "Press [Spacebar] to reveal the answer"
                    mixer.stop()
                    data.channel0.play(data.switchBed)
                    data.switchQuestionActivate = True
                    data.usedSwitchQuestion = True
                    data.lifelinesRemaining -= 1
        elif event.keysym == "i" or event.keysym == "I":
            if data.usedInfiniteTime == False:
                if data.tempPreventInfiniteTime == False:
                    data.tempPreventSwitch = True
                    data.tempPreventFifty = True
                    if data.currentQuestion > 4:
                        mixer.stop()
                    else:
                        data.channel3.stop()
                    data.channel1.play(data.stopClock)
                    if data.currentQuestion > 4:
                        data.oldBed = mixer.Sound(data.path + data.oldBeds[data.currentQuestion])
                        data.channel0.play(data.oldBed)
                    data.infiniteTimeActivate = True
                    data.usedInfiniteTime = True
                    data.lifelinesRemaining -= 1
    elif data.waitingOnVerify == True:
        if event.keysym == "space":
            data.waitingOnVerify = False
            data.verifyNow = True
    elif data.waitingOSwitchQuestion == True:
        if event.keysym == "space":
            data.waitingOSwitchQuestion = False
            data.switchQuestionNow = True
    elif data.waitingOnShortReveal == True:
        if event.keysym == "space":
            if data.switchQuestionActivate == False:
                data.currentQuestion += 1
                data.bankedTime += data.timeLeft #stores remaining time
                data.timeLeft = data.clockAmounts[data.currentQuestion]
                data.timerSeconds = data.clockAmounts[data.currentQuestion]
                if data.currentQuestion == 14:
                    data.tempPreventSwitch = True
                data.waitingOnShortReveal = False
                if data.currentQuestion in [5, 10, 14]:
                    data.dynamicGeneration = True
                    data.shortRevealNow = False #do a long reveal instead
                    data.longRevealNow = True
                else:
                    data.instructionsTop = ""
                    data.instructionsBottom = "Answers will appear when clock starts..."
                    data.shortRevealNow = True
    elif data.waitingOnDisplayWinnings == True:
        if event.keysym == "space":
            data.waitingOnDisplayWinnings = False
            data.displayTotalWinningsNow = True
    elif data.waitingOnReturnToMenu:
        if event.keysym == "space":
            data.returningToMenuNow = True

def timerFired(data): pass

def redrawAll(canvas, data): pass
        
def deltaDraw(canvas, data):
    if data.inGame: instructions(canvas, data, False, 0) 
    if data.transitionToGame:
        if data.inInstruction:
            data.inInstruction = False
            instructionPlay(canvas, data)
        else: #in menu
            drawInstructionsPage(canvas, data, False)
        data.transitionToGame = False
        canvas.delete("all")
        data.channel0.play(data.questionLetsPlay)
        data.inGame = True
        drawLifelines(canvas, data)
        instructions(canvas, data, True, 0)        
        data.waitingOnClock = True
    if data.drawInstructionsNow:
        data.channel0.play(data.instructionsMusic)
        drawInstructionsPage(canvas, data, True)
        data.drawInstructionsNow = False
    if data.waitingOnClock:
        instructions(canvas, data, False, 0) 
    if data.activateCircle == True:
        clockappear(canvas, data)
        data.activateCircle = False
    elif data.revealQuestion == True:
        shiftUp(canvas, data)
        data.revealQuestion = False
    elif data.selectD == True: 
        selectD(canvas, data, False)
        data.selectD = False
    elif data.selectC == True:
        selectC(canvas, data, False)
        data.selectC = False
    elif data.selectB == True:
        selectB(canvas, data, False)
        data.selectB = False
    elif data.selectA == True:
        selectA(canvas, data, False)
        data.selectA = False
    elif data.verifyNow == True:
        if data.selectedAnswer == None: #out of time
            verifySelection(canvas, data, 5) #5 guarantees wrong answer
        else: verifySelection(canvas, data, data.selectedAnswer)
        if data.gameOver == True:
                data.waitingOnDisplayWinnings = True
        data.selectedAnswer = None #reset 
        data.verifyNow = False
    elif data.doubleDipActivate == True: #only True is infinite time first used
        instructions(canvas, data, False, "dd")
        canvas.delete(data.doubleDipOval)
        canvas.delete(data.doubleDipTop)
        canvas.delete(data.doubleDipBottom)
        canvas.delete(data.doubleDipLabel)
        if data.lifelinesRemaining == 0:
            canvas.delete(data.lifelineBottom)
    elif data.switchQuestionNow == True:
        switchTheQuestion(canvas, data)
        data.switchQuestionNow = False
    elif data.shortRevealNow == True:
        shortRevealAll(canvas, data, False)
    elif data.longRevealNow == True:
        removeQuestionBar(canvas, data)
    elif data.displayTotalWinningsNow:
        correctAnswer = int(data.currentQuestionAttributes[6])
        correctResponse(canvas, data, correctAnswer, False)
        instructions(canvas, data, False, "Final winnings")
        data.displayTotalWinningsNow = False
        data.waitingOnReturnToMenu = True
    elif data.returningToMenuNow:
        removeQuestionBarForTheLastTime(canvas, data)
        canvas.delete("all")
        init(data)
        loadQuestion(data)
        drawMenu(canvas, data)

#RGB to hex
def hexcolor(red,green,blue):
    return '#%02x%02x%02x' % (red, green, blue)

def loadQuestion(data):
    with open(data.CSV_FILENAME, newline='') as csvfile:
        pa9reader = csv.reader(csvfile)
        for row in pa9reader:
            data.questionsContainer[int(row[7])].append(row)

def selectQuestion(data, difficulty):
    data.currentQuestionAttributes = data.questionsContainer[difficulty].pop(randrange(len(data.questionsContainer[difficulty])))
    if data.currentQuestionAttributes[1] == "EMPTY":
        data.questionLine1or2 = 1
    else:
        data.questionLine1or2 = 2
    
def dynamicArithmetic(operand1, operand2, operation):
    if operation == "+":
        correctAnswer = operand1 + operand2
    elif operation == "-":
        correctAnswer = operand1 - operand2
    elif operation == "*":
        correctAnswer = operand1 * operand2
    elif operation == "/":
        correctAnswer = operand1 // operand2
    modulations = [[-9, -8, -7, -6, -5, -4, -3, -2, -1],
                   [+1, +2, +3, +4, +5, +6, +7, +8, +9]] 
    # sublists represent possible incorrect answers modulations
    # 0 means it picks an answer from the negative modulations
    # 1 means it picks an answer from the posible modulations
    possibles = [[0, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1]]
    orderList = [correctAnswer]

    modulation = possibles[randrange(len(possibles[0]))] #randomly selects a possible modulation
    for modIndex in modulation:
        modNumber = modulations[modIndex].pop(randrange(len(modulations[modIndex])))
        if digitcount(correctAnswer) > 5:
            # if answers are greater than 100000, then modulate the third digit from the left
            orderList.append(correctAnswer + modNumber * 10 ** (digitcount(correctAnswer) - 3))
        elif digitcount(correctAnswer) > 4:
            # if answers are between 10000 and 99999, the modulate the hundreds place
            orderList.append(correctAnswer + modNumber * 100)
        else:
            #if answers are less than or equal to 9999, the modulate the tens place
            orderList.append(correctAnswer + modNumber * 10)
    answerOrder = []
    for i in range(4):
        pick = randrange(len(orderList))
        pickedNumber = orderList[pick]
        orderList.remove(pickedNumber)
        answerOrder.append(pickedNumber)
    if correctAnswer in answerOrder:
        answerOrder.append(answerOrder.index(correctAnswer)+1)  
    else:
        answerOrder[randrange(len(answerOrder))] = correctAnswer
        answerOrder.append(answerOrder.index(correctAnswer)+1)  
    for i in range(4):
        answerOrder[i] = insertComma(answerOrder[i])
    return answerOrder

def dynamicArithmeticQuestion(data, difficulty):
    data.questionLine1or2 = 1
    attributes = []
    if difficulty == 3: operations = ["+", "-", "*" , "/"]    
    else: operations = ["+", "-", "*"] #no division in difficulties 1 and 2
    selectedOperation = operations[randrange(len(operations))]
    if selectedOperation == "+" or selectedOperation == "-":
        if difficulty == 1:
            operand1 = randrange(100, 1000)
            operand2 = randrange(100, 1000)
        elif difficulty == 2:
            operand1 = randrange(1000, 10000)
            operand2 = randrange(1000, 10000)
        elif difficulty == 3:
            operand1 = randrange(1000, 100000)
            operand2 = randrange(1000, 100000)
        if selectedOperation == "+":
            questionLabel = "What is the sum of %s and %s?" % (insertComma(operand1), insertComma(operand2))
        else: questionLabel = "What is %s subtracted by %s?" % (insertComma(operand1), insertComma(operand2))
    elif selectedOperation == "*":
        if difficulty == 1:
            operand1 = randrange(30, 100)
            operand2 = randrange(30, 100)
        elif difficulty == 2:
            operand1 = randrange(100, 1000)
            operand2 = randrange(100, 1000)
        elif difficulty == 3:
            operand1 = randrange(1000, 10000)
            operand2 = randrange(1000, 10000)
        questionLabel = "What is the product of %s and %s?" % (insertComma(operand1), insertComma(operand2))
    elif selectedOperation == "/":
        operations = [randrange(100, 1000), randrange(100, 1000)]
        productAnswer = operations[0] * operations[1]
        operand1 = productAnswer
        operand2 = operations[randrange(len(operations))]
        questionLabel = "What is %s divided by %s?" % (insertComma(operand1), insertComma(operand2))
    answersSegment = dynamicArithmetic(operand1, operand2, selectedOperation)
    attributes.append(questionLabel)
    attributes.append("EMPTY")
    attributes = attributes + answersSegment
    return attributes

def dynamicCylinderVolume(data, difficulty):
    data.questionLine1or2 = 2
    if difficulty == 1:
        diameter = randrange(4, 10)
        height = randrange(10, 20)
    elif difficulty == 2:
        diameter = randrange(10, 100)
        height = randrange(20, 100)    
    elif difficulty == 3:
        diameterYard = randrange(10, 26)
        heightYard = randrange(10, 26)
        diameterFeet = diameterYard * 3
        heightFeet = heightYard * 3
        diameter = diameterFeet * 12
        height = heightFeet * 12
    if diameter % 2 == 1: diameter += 1
    radius = diameter // 2
    if height == radius:
        height += 1
    if height == diameter:
        height += 1
    if diameter == (height // 2): #do not forget this case!
        height += 1
    if diameter in [8, 11, 18, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
        questionLabel1 = "What is the volume of a right cylinder whose height is %s inches" % insertComma(height)
        questionLabel2 = "and whose circular base has an %s-inch diameter?" % insertComma(diameter)
    else:
        questionLabel1 = "What is the volume of a right cylinder whose height is %s inches" % insertComma(height)
        questionLabel2 = "and whose circular base has a %s-inch diameter?" % insertComma(diameter)
    if difficulty < 3:
        correctAnswer = insertComma(round(radius ** 2 * height * pi))
        incorrect1 = insertComma(round(radius ** 2 * height ** 2 * pi))
        incorrect2 = insertComma(round(diameter ** 2 * height * pi))
        incorrect3 = insertComma(round(radius * height ** 2 * pi))
    else: #difficulty is 3 
        units = ["ft", "yd"]
        unitOrder = [units[randrange(2)], units[randrange(2)], units[randrange(2)], units[randrange(2)]]
        if unitOrder[0] == "ft":
            correctAnswer = insertComma((radius ** 2 * height) // (12 ** 3)) + "π ft³"
        elif unitOrder[0] == "yd":
            correctAnswer = insertComma((radius ** 2 * height) // (36 ** 3)) + "π yd³"
        if unitOrder[1] == "ft": #incorrect1 is not squaring the divisor
            incorrect1 = insertComma((radius ** 2 * height) // (12)) + "π ft³"
        elif unitOrder[1] == "yd":
            incorrect1  = insertComma((radius ** 2 * height) // (36)) + "π yd³"
        if unitOrder[2] == "ft": #incorrect2 is not using radius
            incorrect2 = insertComma((diameter ** 2 * height) // (12 ** 3)) + "π ft³"
        elif unitOrder[2] == "yd":
            incorrect2 = insertComma((diameter ** 2 * height) // (36 ** 3)) + "π yd³"
        if unitOrder[2] == "ft": #incorrect3 is not using radius and not squaring divisor
            incorrect3 = insertComma((diameter ** 2 * height) // (12)) + "π ft³"
        elif unitOrder[2] == "yd":
            incorrect3 = insertComma((diameter ** 2 * height) // (36)) + "π yd³"
    orderList = [correctAnswer, incorrect1, incorrect2, incorrect3]
    answerOrder = []
    for i in range(4):
        pick = randrange(len(orderList))
        pickedNumber = orderList[pick]
        orderList.remove(pickedNumber)
        answerOrder.append(pickedNumber)
    if correctAnswer in answerOrder:
        answerOrder.append(answerOrder.index(correctAnswer)+1)  
    else:
        answerOrder[randrange(len(answerOrder))] = correctAnswer
        answerOrder.append(answerOrder.index(correctAnswer)+1) 
    if difficulty < 3:
        for i in range(4):
            answerOrder[i] = str(answerOrder[i]) + " in³" 
    return [questionLabel1, questionLabel2] + answerOrder 

def difficultySelector(currentQuestion):
    if currentQuestion in [0,1,2,3,4]:
        return 1
    elif currentQuestion in [5,6,7,8,9]:
        return 2
    else:
        return 3

def insertComma(number):
    #takes as input an integer, and returns the string of
    #that integer with commas used to delineate
    #each hundredths mark
    stringNum = str(abs(number))
    commaNum = ""
    charactersRemaining = len(stringNum)
    if charactersRemaining <= 3:
        return str(number)
    else:
        if number < 0: negativeSwitch = True
        else: negativeSwitch = False 
    currentDigit = 0
    firstComma = len(stringNum) % 3
    firstCommaSwitch = False
    secondComma = 1
    for digit in range(len(stringNum)):
        if firstCommaSwitch == False:
            if firstComma == 0:
                if currentDigit == 3:
                    commaNum += ","
                    firstCommaSwitch = True
            elif firstComma == 1:
                if currentDigit == 1:
                    commaNum += ","
                    firstCommaSwitch = True
            elif firstComma == 2:
                if currentDigit == 2:
                    commaNum += ","
                    firstCommaSwitch = True
        else:
            if secondComma % 3 == 0:
                commaNum += ","
            secondComma += 1
        commaNum += str(stringNum[digit])
        currentDigit += 1
    if negativeSwitch == False: return commaNum
    else: return "-" + commaNum

def dynamicSequence():
    coefficients = [randrange(10), randrange(10), randrange(10)]
    exponents = [randrange(5), randrange(5), randrange(5)]
    #print(str(coefficients[0])+"x^"+str(exponents[0])+"+"+str(coefficients[1])+"x^"+str(exponents[1])+"+"+str(coefficients[2])+"x^"+str(exponents[2]))
    sequenceList = []
    for i in range(8):
        sequenceList.append(coefficients[0]*i**exponents[0] + coefficients[1]*i**exponents[1] + coefficients[2]*i**exponents[2])
    if sequenceList[4] < 100: #omg, I'm actually using recursion!
        return dynamicSequence()
    correctAnswer = coefficients[0]*8**exponents[0] + coefficients[1]*8**exponents[1] + coefficients[2]*8**exponents[2]
    return sequenceList, correctAnswer

def dynamicSequenceQuestion():
    sequence, correctAnswer = dynamicSequence()
    questionLabel1 = "%s, %s, %s, %s, %s, %s, %s, %s..." % (sequence[0],
                                                            sequence[1],
                                                            sequence[2],
                                                            sequence[3],
                                                            sequence[4],
                                                            sequence[5],
                                                            sequence[6],
                                                            sequence[7])
    questionLabel2 = "What is the next number in this holonomic sequence?"
    possibles = [[correctAnswer, correctAnswer - 6, correctAnswer - 4, correctAnswer - 2],
                 [correctAnswer, correctAnswer - 4, correctAnswer - 2, correctAnswer + 2],
                 [correctAnswer, correctAnswer - 2, correctAnswer + 2, correctAnswer + 4],
                 [correctAnswer, correctAnswer + 2, correctAnswer + 4, correctAnswer + 6]]
    possibleSelected = possibles[randrange(4)]
    answerOrder = []
    for i in range(4):
        pick = randrange(len(possibleSelected))
        pickedNumber = possibleSelected[pick]
        possibleSelected.remove(pickedNumber)
        answerOrder.append(pickedNumber)
    if correctAnswer in answerOrder:
        answerOrder.append(answerOrder.index(correctAnswer)+1) 
    else:
        answerOrder[randrange(len(answerOrder))] = correctAnswer
        answerOrder.append(answerOrder.index(correctAnswer)+1)
    for i in range(4):
        answerOrder[i] = insertComma(answerOrder[i])
    return [questionLabel1, questionLabel2] + answerOrder

def instructions(canvas, data, original, code):
    if original == True:
        offset = 20
        data.instructBottom = canvas.create_text(data.width // 2,
                              data.height - 0.8 * offset, 
                              text = data.instructionsBottom,
                              font = ("Conduit ITC Medium", 20),
                              fill = "black")
        data.instructTop = canvas.create_text(data.width // 2,
                           data.height - 2 * offset, 
                           text = data.instructionsTop,
                           font = ("Conduit ITC Medium", 20),
                           fill = "black")
        #fade in the instructions
        startTime = clock()
        animationDurationTotal = 1.25
        while (clock() - startTime) < 1.25:
            proportion = (clock() - startTime) / animationDurationTotal
            targetRGBWhite = floor(255 * proportion)
            currentWhiteFill = hexcolor(targetRGBWhite,
                                        targetRGBWhite,
                                        targetRGBWhite)
            canvas.itemconfig(data.instructBottom, fill = currentWhiteFill)
            canvas.itemconfig(data.instructTop, fill = currentWhiteFill)
            canvas.update()
        canvas.itemconfig(data.instructBottom, fill = "white")
        canvas.itemconfig(data.instructTop, fill = "white")
        canvas.update()
    else:
        if code == "delay": #delay hitting spacebar for clock reveal
            data.instructionsTop = data.instructionsBottom
            data.instructionsBottom = "Press [Spacebar] to start game"
        elif code == "startClock":
            data.instructionsTop = "Press [A], [B], [C], or [D] to answer"
            data.instructionsBottom = "or click on the answer with your mouse"
        elif code == "correct":
            if data.gameOver == False:
                if data.currentQuestion < 14:
                    data.instructionsTop = ""
                    data.instructionsBottom = "Correct! Press [Spacebar] to see next question"
                elif data.currentQuestion == 14:
                    data.instructionsTop = "You have won the game!"
                    data.instructionsBottom = "Press [Spacebar] to return to main menu"
                    data.waitingOnReturnToMenu = True
            else: #game over remove all elements
                if data.usedSwitchQuestion == False:
                    canvas.delete(data.switchOval)
                    canvas.delete(data.switchTop1)
                    canvas.delete(data.switchTop2)
                    canvas.delete(data.switchTop3)
                    canvas.delete(data.switchBottom)
                    canvas.delete(data.switchLabel)
                if data.usedInfiniteTime == False:
                    canvas.delete(data.infiniteOval)
                    canvas.delete(data.infiniteTop1)
                    canvas.delete(data.infiniteTop2)
                    canvas.delete(data.infiniteBottom)
                    canvas.delete(data.infiniteLabel)
                if data.usedDoubleDip == False:
                    canvas.delete(data.doubleDipOval)
                    canvas.delete(data.doubleDipTop)
                    canvas.delete(data.doubleDipBottom)
                    canvas.delete(data.doubleDipLabel)
                if data.usedFiftyFifty == False:
                    canvas.delete(data.fiftyFiftyOval)
                    canvas.delete(data.fiftyFiftyLabel)
                    canvas.delete(data.fiftyFiftyTop)
                    canvas.delete(data.fiftyFiftyBottom)
                canvas.delete(data.guaranteedAmount)
                canvas.delete(data.questionValueLabel)
                canvas.delete(data.wonAmount)
                canvas.delete(data.lifelineBottom)
                data.instructionsTop = ""
                data.instructionsBottom = ""
                data.channel0.play(data.totalWinningsSound)
        elif code == "incorrect":
            data.instructionsTop = ""
            if data.switchQuestionActivate == True: 
                data.instructionsBottom = "Press [Spacebar] to see switched question"
            else:
                data.instructionsBottom = "Sorry, game over! Press [Spacebar] to see your winnings"
        elif code == "50:50":
            data.instructionsTop = ""
            data.instructionsBottom = "Activated 50:50"
        elif code == "dd":
            if data.lifelinesRemaining == 0:
                data.instructionsTop = "Activated Double Dip"
            if data.infiniteTimeActivate:
                data.instructionsBottom = "Select your first answer"
            else:
                data.instructionsBottom = "Select your first answer before time runs out"
        elif code == "ddSelect1":
            data.instructionsTop = ""
            data.instructionsBottom = "Please wait as answer is verified by the computer..."
        elif code == "ddWrong":
            data.instructionsTop = "Incorrect"
            if data.clockRunning == False:
                data.instructionsBottom = "Select your second answer"
            else:    
                data.instructionsBottom = "Select your second answer before time runs out"
        elif code == "infinite":
            data.instructionsTop = ""
            data.instructionsBottom = "Activated Infinite Time"
        elif code == "waitForAnswer":
            data.instructionsTop = ""
            data.instructionsBottom = "Answers will appear when clock starts..."
        elif code == "Out of Time":
            data.instructionsTop = "You ran out of time!"
            data.instructionsBottom = "Press [Spacebar] to reveal the answer"
        elif code == "Final winnings":
            data.instructionsTop = "Your total winnings"
            data.instructionsBottom = "Press [Spacebar] to return to main menu"
        elif code == "Mill Clock Appear":
            data.instructionsTop = "For the million dollar question, you will have"
            data.instructionsBottom = "45 seconds plus your banked time..." 
        elif code == "Mill flash":
            data.instructionsTop = "You have " + prettytime(normaltime(data.bankedTime)) + " of banked time,"
            data.instructionsBottom = "Press [Spacebar] to see the million dollar question" 
        canvas.itemconfig(data.instructBottom, text = data.instructionsBottom)
        canvas.itemconfig(data.instructTop, text = data.instructionsTop)
        canvas.update()
        
def selectD(canvas, data, incorrectSwitch):
    if incorrectSwitch == False: #normal (yellow) answer selection
        if data.doubleDipActivate == False:
            if data.doubleDipActivate2 == False:
                if data.currentQuestion > 4:
                    data.channel0.stop()
                data.questionFinalAnswer = mixer.Sound(data.path + data.finalAnswerSounds[data.currentQuestion])
                if data.currentQuestion < 5:
                    data.channel3.stop()
                data.channel1.play(data.questionFinalAnswer)
            else:
                data.channel1.play(data.doubleDipAnswer2)
                data.doubleDipActivate2 = False
                if data.currentQuestion < 5: data.resume100Bed = True
        else:
            instructions(canvas, data, False, "ddSelect1")
            if data.currentQuestion > 4:
                data.channel0.pause()
            else:
                data.channel3.pause()
            data.channel1.play(data.doubleDipAnswer1)
        bgTargetRed = 207
        bgTargetGreen = 122
        bgTargetBlue = 12
        labelTargetRed = 32
        labelTargetGreen = 109
        labelTargetBlue = 223
        answerTargetRGB = 255
    else: #incorrect answer selected; animation for correct answer
        if data.switchQuestionActivate == True:
            data.channel1.play(data.switchAnswer)
        else:
            data.channel0.stop()
            if data.ranOutOfTime == False:
                data.questionWrong = mixer.Sound(data.path + data.wrongSounds[data.currentQuestion])
                data.channel1.play(data.questionWrong)
        bgTargetRed = 16
        bgTargetGreen = 217
        bgTargetBlue = 8
        labelTargetRed = -223
        labelTargetGreen = -146
        labelTargetBlue = -32
        answerTargetRGB = 0
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        canvas.itemconfig(data.q4background, 
                          fill = hexcolor(floor(bgTargetRed * proportion),
                                          floor(bgTargetGreen * proportion),
                                          floor(bgTargetBlue * proportion)))
        canvas.coords(data.q4background,data.topleftx4 - 40,
                  data.toplefty4 - data.shiftUpHeight,
                  data.topleftx4 + (data.questionWidth + 42) * proportion,
                  data.bottomrighty4 - data.shiftUpHeight)
        canvas.itemconfig(data.labelD, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed * proportion),
                                          floor(146 + labelTargetGreen * proportion),
                                          floor(32 + labelTargetBlue * proportion)))
        canvas.itemconfig(data.answerD, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion)))
        canvas.update()
    #fix the final values
    canvas.itemconfig(data.q4background, 
                          fill = hexcolor(floor(bgTargetRed),
                                          floor(bgTargetGreen),
                                          floor(bgTargetBlue)))
    canvas.coords(data.q4background,data.topleftx4 - 40,
                  data.toplefty4 - data.shiftUpHeight,
                  data.topleftx4 + (data.questionWidth + 42),
                  data.bottomrighty4 - data.shiftUpHeight)
    canvas.itemconfig(data.labelD, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed),
                                          floor(146 + labelTargetGreen),
                                          floor(32 + labelTargetBlue)))
    canvas.itemconfig(data.answerD, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB)))
    canvas.update()
    if incorrectSwitch == False: #correct response
        data.selectedAnswer = 4
    else: 
        incorrectResponse(canvas, data, 4)

def doubleDipIncorrectD(canvas, data):
    instructions(canvas, data, False, "ddWrong")
    data.channel1.play(data.doubleDipWrong)
    startTime = clock() 
    animationDuration = 1 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        bgTargetRed = floor(207 - 195 * proportion)
        bgTargetGreen = floor(122 - 12 * proportion)
        bgTargetBlue = floor(12 + 34 * proportion)
        currentFill = hexcolor(bgTargetRed, bgTargetGreen, bgTargetBlue)
        canvas.itemconfig(data.q4background, fill = currentFill)
        canvas.coords(data.q4background,data.topleftx4 - 40,
                  data.toplefty4 - data.shiftUpHeight,
                  data.topleftx4 + (data.questionWidth + 42) - (data.questionWidth + 42) * proportion,
                  data.bottomrighty4 - data.shiftUpHeight)
        canvas.itemconfig(data.labelD, #changes label color
                          fill = hexcolor(floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion)))
        canvas.update()
    canvas.coords(data.q4background,data.topleftx4 - 40, #removes anything left over
                  data.toplefty4 - data.shiftUpHeight,
                  data.topleftx4 - 40,
                  data.bottomrighty4 - data.shiftUpHeight)
    data.removedD = False
    removeAnswer(canvas, data, 4)
    canvas.update()
    if data.infiniteTimeActivate == True:
        instructions(canvas, data, False, "ddWrong")
        data.clockRunning = False
        data.infiniteTimeActivate = False
        data.waitingOnUserAnswerChoice = True
        data.doubleDipActivate2 = True
    else:
        canvas.after(2000)
        beginCountdown(canvas, data, True)

def selectC(canvas, data, incorrectSwitch):
    if incorrectSwitch == False: #normal (yellow) answer selection
        if data.doubleDipActivate == False:
            if data.doubleDipActivate2 == False:
                if data.currentQuestion > 4:
                    data.channel0.stop()
                data.questionFinalAnswer = mixer.Sound(data.path + data.finalAnswerSounds[data.currentQuestion])
                if data.currentQuestion < 5:
                    data.channel3.stop()
                data.channel1.play(data.questionFinalAnswer)
            else:
                data.channel1.play(data.doubleDipAnswer2)
                data.doubleDipActivate2 = False
                if data.currentQuestion < 5: data.resume100Bed = True
        else:
            instructions(canvas, data, False, "ddSelect1")
            if data.currentQuestion > 4:
                data.channel0.pause()
            else:
                data.channel3.pause()
            data.channel1.play(data.doubleDipAnswer1)
        bgTargetRed = 207
        bgTargetGreen = 122
        bgTargetBlue = 12
        labelTargetRed = 32
        labelTargetGreen = 109
        labelTargetBlue = 223
        answerTargetRGB = 255
    else: #incorrect answer selected; animation for correct answer
        if data.switchQuestionActivate == True:
            data.channel1.play(data.switchAnswer)
        else:
            data.channel0.stop()
            if data.ranOutOfTime == False:
                data.questionWrong = mixer.Sound(data.path + data.wrongSounds[data.currentQuestion])
                data.channel1.play(data.questionWrong)
        bgTargetRed = 16
        bgTargetGreen = 217
        bgTargetBlue = 8
        labelTargetRed = -223
        labelTargetGreen = -146
        labelTargetBlue = -32
        answerTargetRGB = 0
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        canvas.itemconfig(data.q3background, 
                          fill = hexcolor(floor(bgTargetRed * proportion),
                                          floor(bgTargetGreen * proportion),
                                          floor(bgTargetBlue * proportion)))
        canvas.coords(data.q3background,data.topleftx3 - 40,
                  data.toplefty3 - data.shiftUpHeight,
                  data.topleftx3 + (data.questionWidth + 42) * proportion,
                  data.bottomrighty3 - data.shiftUpHeight)
        canvas.itemconfig(data.labelC, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed * proportion),
                                          floor(146 + labelTargetGreen * proportion),
                                          floor(32 + labelTargetBlue * proportion)))
        canvas.itemconfig(data.answerC, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion)))
        canvas.update()
    #fix the final values
    canvas.itemconfig(data.q3background, 
                          fill = hexcolor(floor(bgTargetRed),
                                          floor(bgTargetGreen),
                                          floor(bgTargetBlue)))
    canvas.coords(data.q3background,data.topleftx3 - 40,
                  data.toplefty3 - data.shiftUpHeight,
                  data.topleftx3 + (data.questionWidth + 42),
                  data.bottomrighty3 - data.shiftUpHeight)
    canvas.itemconfig(data.labelC, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed),
                                          floor(146 + labelTargetGreen),
                                          floor(32 + labelTargetBlue)))
    canvas.itemconfig(data.answerC, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB)))
    canvas.update()
    if incorrectSwitch == False:
        data.selectedAnswer = 3
    else:
        incorrectResponse(canvas, data, 3)

def doubleDipIncorrectC(canvas, data):
    instructions(canvas, data, False, "ddWrong")
    data.channel1.play(data.doubleDipWrong)
    startTime = clock() #start ticking cue
    animationDuration = 1 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        bgTargetRed = floor(207 - 195 * proportion)
        bgTargetGreen = floor(122 - 12 * proportion)
        bgTargetBlue = floor(12 + 34 * proportion)
        currentFill = hexcolor(bgTargetRed, bgTargetGreen, bgTargetBlue)
        canvas.itemconfig(data.q3background, fill = currentFill)
        canvas.coords(data.q3background,data.topleftx3 - 40,
                  data.toplefty3 - data.shiftUpHeight,
                  data.topleftx3 + (data.questionWidth + 42) - (data.questionWidth + 42) * proportion,
                  data.bottomrighty3 - data.shiftUpHeight)
        canvas.itemconfig(data.labelC, #changes label color
                          fill = hexcolor(floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion)))
        canvas.update()
    canvas.coords(data.q3background,data.topleftx3 - 40, #removes anything left over
                  data.toplefty3 - data.shiftUpHeight,
                  data.topleftx3 - 40,
                  data.bottomrighty3 - data.shiftUpHeight)
    data.removedC = False
    removeAnswer(canvas, data, 3)
    canvas.update()
    if data.infiniteTimeActivate == True:
        instructions(canvas, data, False, "ddWrong")
        data.clockRunning = False
        data.infiniteTimeActivate = False
        data.waitingOnUserAnswerChoice = True
        data.doubleDipActivate2 = True
    else:
        canvas.after(2000)
        beginCountdown(canvas, data, True)

def selectB(canvas, data, incorrectSwitch):
    if incorrectSwitch == False: #normal (yellow) answer selection
        if data.doubleDipActivate == False:
            if data.doubleDipActivate2 == False:
                if data.currentQuestion > 4:
                    data.channel0.stop()
                data.questionFinalAnswer = mixer.Sound(data.path + data.finalAnswerSounds[data.currentQuestion])
                if data.currentQuestion < 5:
                    data.channel3.stop()
                data.channel1.play(data.questionFinalAnswer)
            else:
                data.channel1.play(data.doubleDipAnswer2)
                data.doubleDipActivate2 = False
                if data.currentQuestion < 5: data.resume100Bed = True
        else:
            instructions(canvas, data, False, "ddSelect1")
            if data.currentQuestion > 4:
                data.channel0.pause()
            else:
                data.channel3.pause()
            data.channel1.play(data.doubleDipAnswer1)
        bgTargetRed = 207
        bgTargetGreen = 122
        bgTargetBlue = 12
        labelTargetRed = 32
        labelTargetGreen = 109
        labelTargetBlue = 223
        answerTargetRGB = 255
    else: #incorrect answer selected; animation for correct answer
        if data.switchQuestionActivate == True:
            data.channel1.play(data.switchAnswer)
        else:
            if data.inInstruction == False:
                data.channel0.stop()
                if data.ranOutOfTime == False:
                    data.questionWrong = mixer.Sound(data.path + data.wrongSounds[data.currentQuestion])
                    data.channel1.play(data.questionWrong)
        bgTargetRed = 16
        bgTargetGreen = 217
        bgTargetBlue = 8
        labelTargetRed = -223
        labelTargetGreen = -146
        labelTargetBlue = -32
        answerTargetRGB = 0
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        canvas.itemconfig(data.q2background, 
                          fill = hexcolor(floor(bgTargetRed * proportion),
                                          floor(bgTargetGreen * proportion),
                                          floor(bgTargetBlue * proportion)))
        canvas.coords(data.q2background,data.topleftx2 - 40,
                  data.toplefty2 - data.shiftUpHeight,
                  data.topleftx2 + (data.questionWidth + 42) * proportion,
                  data.bottomrighty2 - data.shiftUpHeight)
        canvas.itemconfig(data.labelB, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed * proportion),
                                          floor(146 + labelTargetGreen * proportion),
                                          floor(32 + labelTargetBlue * proportion)))
        canvas.itemconfig(data.answerB, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion)))
        canvas.update()
    #fix the final values
    canvas.itemconfig(data.q2background, 
                          fill = hexcolor(floor(bgTargetRed),
                                          floor(bgTargetGreen),
                                          floor(bgTargetBlue)))
    canvas.coords(data.q2background,data.topleftx2 - 40,
                  data.toplefty2 - data.shiftUpHeight,
                  data.topleftx2 + (data.questionWidth + 42),
                  data.bottomrighty2 - data.shiftUpHeight)
    canvas.itemconfig(data.labelB, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed),
                                          floor(146 + labelTargetGreen),
                                          floor(32 + labelTargetBlue)))
    canvas.itemconfig(data.answerB, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB)))
    canvas.update()
    if incorrectSwitch == False:
        data.selectedAnswer = 2
    else:
        incorrectResponse(canvas, data, 2)

def doubleDipIncorrectB(canvas, data):
    instructions(canvas, data, False, "ddWrong")
    data.channel1.play(data.doubleDipWrong)
    startTime = clock() #start ticking cue
    animationDuration = 1 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        bgTargetRed = floor(207 - 195 * proportion)
        bgTargetGreen = floor(122 - 12 * proportion)
        bgTargetBlue = floor(12 + 34 * proportion)
        currentFill = hexcolor(bgTargetRed, bgTargetGreen, bgTargetBlue)
        canvas.itemconfig(data.q2background, fill = currentFill)
        canvas.coords(data.q2background,data.topleftx2 - 40,
                  data.toplefty2 - data.shiftUpHeight,
                  data.topleftx2 + (data.questionWidth + 42) - (data.questionWidth + 42) * proportion,
                  data.bottomrighty2 - data.shiftUpHeight)
        canvas.itemconfig(data.labelB, #changes label color
                          fill = hexcolor(floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion)))
        canvas.update()
    canvas.coords(data.q2background,data.topleftx2 - 40, #removes anything left over
                  data.toplefty2 - data.shiftUpHeight,
                  data.topleftx2 - 40,
                  data.bottomrighty2 - data.shiftUpHeight)
    data.removedB = False
    removeAnswer(canvas, data, 2)
    canvas.update()
    if data.infiniteTimeActivate == True:
        instructions(canvas, data, False, "ddWrong")
        data.clockRunning = False
        data.infiniteTimeActivate = False
        data.waitingOnUserAnswerChoice = True
        data.doubleDipActivate2 = True
    else:
        canvas.after(2000)
        beginCountdown(canvas, data, True)

def selectA(canvas, data, incorrectSwitch):
    if incorrectSwitch == False: #normal (yellow) answer selection
        if data.doubleDipActivate == False:
            if data.doubleDipActivate2 == False:
                if data.currentQuestion > 4:
                    data.channel0.stop()
                data.questionFinalAnswer = mixer.Sound(data.path + data.finalAnswerSounds[data.currentQuestion])
                if data.currentQuestion < 5:
                    data.channel3.stop()
                data.channel1.play(data.questionFinalAnswer)
            else:
                data.channel1.play(data.doubleDipAnswer2)
                data.doubleDipActivate2 = False
                if data.currentQuestion < 5: data.resume100Bed = True
        else:
            instructions(canvas, data, False, "ddSelect1")
            if data.currentQuestion > 4:
                data.channel0.pause()
            else:
                data.channel3.pause()
            data.channel1.play(data.doubleDipAnswer1)
        bgTargetRed = 207
        bgTargetGreen = 122
        bgTargetBlue = 12
        labelTargetRed = 32
        labelTargetGreen = 109
        labelTargetBlue = 223
        answerTargetRGB = 255
    else: #incorrect answer selected; animation for correct answer
        if data.switchQuestionActivate == True:
            data.channel1.play(data.switchAnswer)
        else:
            if data.inInstruction == False:
                if data.transitionToGame == False:
                    data.channel0.stop()
                    if data.ranOutOfTime == False:
                        data.questionWrong = mixer.Sound(data.path + data.wrongSounds[data.currentQuestion])
                        data.channel1.play(data.questionWrong)
        bgTargetRed = 16
        bgTargetGreen = 217
        bgTargetBlue = 8
        labelTargetRed = -223
        labelTargetGreen = -146
        labelTargetBlue = -32
        answerTargetRGB = 0
    startTime = clock()
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        canvas.itemconfig(data.q1background, 
                          fill = hexcolor(floor(bgTargetRed * proportion),
                                          floor(bgTargetGreen * proportion),
                                          floor(bgTargetBlue * proportion)))
        canvas.coords(data.q1background,data.topleftx1 - 40,
                  data.toplefty1 - data.shiftUpHeight,
                  data.topleftx1 + (data.questionWidth + 42) * proportion,
                  data.bottomrighty1 - data.shiftUpHeight)
        canvas.itemconfig(data.labelA, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed * proportion),
                                          floor(146 + labelTargetGreen * proportion),
                                          floor(32 + labelTargetBlue * proportion)))
        canvas.itemconfig(data.answerA, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion),
                                          floor(255 - answerTargetRGB * proportion)))
        canvas.update()
    #fix the final values
    canvas.itemconfig(data.q1background, 
                          fill = hexcolor(floor(bgTargetRed),
                                          floor(bgTargetGreen),
                                          floor(bgTargetBlue)))
    canvas.coords(data.q1background,data.topleftx1 - 40,
                  data.toplefty1 - data.shiftUpHeight,
                  data.topleftx1 + (data.questionWidth + 42),
                  data.bottomrighty1 - data.shiftUpHeight)
    canvas.itemconfig(data.labelA, #changes label color
                          fill = hexcolor(floor(223 + labelTargetRed),
                                          floor(146 + labelTargetGreen),
                                          floor(32 + labelTargetBlue)))
    canvas.itemconfig(data.answerA, #changes answer text color
                          fill = hexcolor(floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB),
                                          floor(255 - answerTargetRGB)))
    canvas.update()
    if incorrectSwitch == False:
        data.selectedAnswer = 1
    else:
        incorrectResponse(canvas, data, 1)

def doubleDipIncorrectA(canvas, data):
    instructions(canvas, data, False, "ddWrong")
    data.channel1.play(data.doubleDipWrong)
    startTime = clock() #start ticking cue
    animationDuration = 1 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        bgTargetRed = floor(207 - 195 * proportion)
        bgTargetGreen = floor(122 - 12 * proportion)
        bgTargetBlue = floor(12 + 34 * proportion)
        currentFill = hexcolor(bgTargetRed, bgTargetGreen, bgTargetBlue)
        canvas.itemconfig(data.q1background, fill = currentFill)
        canvas.coords(data.q1background,data.topleftx1 - 40,
                  data.toplefty1 - data.shiftUpHeight,
                  data.topleftx1 + (data.questionWidth + 42) - (data.questionWidth + 42) * proportion,
                  data.bottomrighty1 - data.shiftUpHeight)
        canvas.itemconfig(data.labelA, #changes label color
                          fill = hexcolor(floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion)))
        canvas.update()
    canvas.coords(data.q1background,data.topleftx1 - 40, #removes anything left over
                  data.toplefty1 - data.shiftUpHeight,
                  data.topleftx1 - 40,
                  data.bottomrighty1 - data.shiftUpHeight)
    data.removedA = False
    removeAnswer(canvas, data, 1)
    canvas.update()
    if data.infiniteTimeActivate == True:
        instructions(canvas, data, False, "ddWrong")
        data.clockRunning = False
        data.infiniteTimeActivate = False
        data.waitingOnUserAnswerChoice = True
        data.doubleDipActivate2 = True
    else:
        canvas.after(2000)
        beginCountdown(canvas, data, True)

def removeAnswer(canvas, data, number):
    if number == 1:
        data.removedA = True
        canvas.itemconfig(data.answerA, text = "")
        canvas.itemconfig(data.labelA, text = "")
    elif number == 2:
        data.removedB = True
        canvas.itemconfig(data.answerB, text = "")
        canvas.itemconfig(data.labelB, text = "")        
    elif number == 3:
        data.removedC = True
        canvas.itemconfig(data.answerC, text = "")
        canvas.itemconfig(data.labelC, text = "") 
    elif number == 4:
        data.removedD = True
        canvas.itemconfig(data.answerD, text = "")
        canvas.itemconfig(data.labelD, text = "")

def verifySelection(canvas, data, selected): #checks if selection is correct or not
    correctAnswer = int(data.currentQuestionAttributes[6]) #1 for A, 2 for B, 3 for C, 4 for D
    labelAnimations = [None, data.labelA,data.labelB,data.labelC,data.labelD]
    answerAnimations = [None, data.answerA, data.answerB, data.answerC, data.answerD]
    bgAnimations = [None, data.q1background, data.q2background,
                            data.q3background, data.q4background]
    correctLabelAnimation = labelAnimations[correctAnswer]
    correctAnswerAnimation = answerAnimations[correctAnswer]
    correctBgAnimation = bgAnimations[correctAnswer]
    data.incorrectSelected = selected
    if data.waitingOnUserAnswerChoice == False:
        if selected == correctAnswer: #user selected correct answer
            data.incorrectSelected = None
            if data.doubleDipActivate == True:
                data.doubleDipActivate = False
                canvas.after(5000) #delays revealing answer if double dip used
                if data.currentQuestion < 4:
                    data.channel0.unpause()
            data.questionCorrect = mixer.Sound(data.path + data.correctSounds[data.currentQuestion])
            data.channel1.play(data.questionCorrect)
            #4-stage animation: Stage 1: yellow to bright green
            startTime = clock() #start ticking cue
            animationDuration = 0.25 #seconds
            while (clock() - startTime) < animationDuration:
                proportion = (clock() - startTime) / animationDuration
                targetRed = 207 - floor(191 * proportion)
                targetGreen = 122 + floor(95 * proportion)
                targetBlue = 12 - floor(4 * proportion)
                currentFill= hexcolor(targetRed,
                                                     targetGreen, 
                                                     targetBlue)
                canvas.itemconfig(correctBgAnimation, 
                                  fill = currentFill)
                canvas.itemconfig(correctLabelAnimation, #changes label to black
                          fill = hexcolor(floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion),
                                          floor(255 - 255 * proportion)))
                canvas.itemconfig(correctAnswerAnimation, #changes answer text to white
                          fill = hexcolor(floor(255 * proportion),
                                          floor(255 * proportion),
                                          floor(255 * proportion)))
                canvas.update()
            #Stage 2: bright green to dark green
            startTime = clock() #start ticking cue
            animationDuration = 0.25 #seconds
            while (clock() - startTime) < animationDuration:
                proportion = (clock() - startTime) / animationDuration
                targetRed = 16 - floor(4 * proportion)
                targetGreen = 217 - floor(107 * proportion)
                targetBlue = 8 + floor(38 * proportion)
                currentFill= hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(correctBgAnimation, 
                                  fill = currentFill)
                canvas.update()
            #Stage 3: dark green to bright green
            startTime = clock() #start ticking cue
            animationDuration = 0.25 #seconds
            while (clock() - startTime) < animationDuration:
                proportion = (clock() - startTime) / animationDuration
                targetRed = 12 + floor(4 * proportion)
                targetGreen = 110 + floor(107 * proportion)
                targetBlue = 46 - floor(38 * proportion)
                currentFill= hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(correctBgAnimation, 
                                  fill = currentFill)
                canvas.update()
            #Stage 4: bright green to dark green again
            startTime = clock() #start ticking cue
            animationDuration = 0.25 #seconds
            while (clock() - startTime) < animationDuration:
                proportion = (clock() - startTime) / animationDuration
                targetRed = 16 - floor(4 * proportion)
                targetGreen = 217 - floor(107 * proportion)
                targetBlue = 8 + floor(38 * proportion)
                currentFill= hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(correctBgAnimation, 
                                  fill = currentFill)
                canvas.update()
            correctResponse(canvas, data, correctAnswer, False)
        else: #user selected incorrect answer
            if data.doubleDipActivate == True:
                data.resumeTime = data.timeLeft #loads resume variables
                data.resumeExtent = data.extentvalue 
                data.doubleDipActivate = False
                canvas.after(5000)
                if selected == 1:
                    doubleDipIncorrectA(canvas, data)
                elif selected == 2:
                    doubleDipIncorrectB(canvas, data)
                elif selected == 3:
                    doubleDipIncorrectC(canvas, data)
                elif selected == 4:
                    doubleDipIncorrectD(canvas, data)
            else: #double dip lifeline not being used
                if correctAnswer == 1: selectA(canvas, data, True)
                elif correctAnswer == 2: selectB(canvas, data, True)
                elif correctAnswer == 3: selectC(canvas, data, True)
                else: selectD(canvas, data, True)

def correctResponse(canvas, data, correctAnswer, switchQuestion):
    if switchQuestion == False:
        if data.currentQuestion < 4:
            if data.resume100Bed == True:
                data.resume100Bed = False
                data.channel0.play(data.questions100to1000Bed)
            data.channel2.play(data.winningsSizzle)
        elif data.currentQuestion == 4:
            data.channel0.stop()
    bgAnimations = [None, data.q1background, data.q2background,
                            data.q3background, data.q4background]
    correctBgAnimation = bgAnimations[correctAnswer]
    if data.gameOver == True: #selects correct yellow strip to fade out 
        if data.ranOutOfTime == False:
            correctBgYellow = bgAnimations[data.incorrectSelected] 
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        # fade out green background on correct answer
        targetRed = floor(6 - 6 * proportion)
        targetGreen = floor(169 - 169 * proportion)
        targetBlue = 0
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(correctBgAnimation, 
                                  fill = currentFill)
        if data.gameOver == True: #fades out yellow strip in event of game over
            if data.ranOutOfTime == False:
                targetRed = floor(207 - 207 * proportion)
                targetGreen = floor(122 - 122 * proportion)
                targetBlue = floor(12 - 12 * proportion)

                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(correctBgYellow, 
                                      fill = currentFill)
                #fade out answer labels
                targetRedOrange = floor(223 - 223 * proportion)
                targetGreenOrange = floor(146 - 146 * proportion)
                targetBlueOrange = floor(32 - 32 * proportion)
                fillOrange = hexcolor(targetRedOrange, targetGreenOrange, targetBlueOrange)
                if data.incorrectSelected != 1:
                    if correctAnswer != 1:
                        canvas.itemconfig(data.labelA, fill = fillOrange)
                if data.incorrectSelected != 2:
                    if correctAnswer != 2:
                        canvas.itemconfig(data.labelB, fill = fillOrange)
                if data.incorrectSelected != 3:
                    if correctAnswer != 3:
                        canvas.itemconfig(data.labelC, fill = fillOrange)
                if data.incorrectSelected != 4:
                    if correctAnswer != 4:
                        canvas.itemconfig(data.labelD, fill = fillOrange)
                targetRed = floor(255 - 255 * proportion)
                targetGreen = floor(255 - 255 * proportion)
                targetBlue = floor(255 - 255 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                if data.incorrectSelected == 1:
                    canvas.itemconfig(data.labelA, fill = currentFill)
                if data.incorrectSelected == 2:
                    canvas.itemconfig(data.labelB, fill = currentFill)
                if data.incorrectSelected == 3:
                    canvas.itemconfig(data.labelC, fill = currentFill)
                if data.incorrectSelected == 4:
                    canvas.itemconfig(data.labelD, fill = currentFill)
            else: #ran out of time case
                targetRedOrange = floor(223 - 223 * proportion)
                targetGreenOrange = floor(146 - 146 * proportion)
                targetBlueOrange = floor(32 - 32 * proportion)
                fillOrange = hexcolor(targetRedOrange, targetGreenOrange, targetBlueOrange)
                if correctAnswer != 1:
                    canvas.itemconfig(data.labelA, fill = fillOrange)
                if correctAnswer != 2:
                    canvas.itemconfig(data.labelB, fill = fillOrange)
                if correctAnswer != 3:
                    canvas.itemconfig(data.labelC, fill = fillOrange)
                if correctAnswer != 4:
                    canvas.itemconfig(data.labelD, fill = fillOrange)
        else: #not game over case
            targetRedOrange = floor(223 - 223 * proportion)
            targetGreenOrange = floor(146 - 146 * proportion)
            targetBlueOrange = floor(32 - 32 * proportion)
            fillOrange = hexcolor(targetRedOrange, targetGreenOrange, targetBlueOrange)
            if correctAnswer != 1:
                canvas.itemconfig(data.labelA, fill = fillOrange)
            if correctAnswer != 2:
                canvas.itemconfig(data.labelB, fill = fillOrange)
            if correctAnswer != 3:
                canvas.itemconfig(data.labelC, fill = fillOrange)
            if correctAnswer != 4:
                canvas.itemconfig(data.labelD, fill = fillOrange)
        #fade out question and answer texts; as well as question value label
        targetRed = floor(255 - 255 * proportion)
        targetGreen = floor(255 - 255 * proportion)
        targetBlue = floor(255 - 255 * proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        if data.incorrectSelected != 1:
            canvas.itemconfig(data.answerA, fill = currentFill)
        if data.incorrectSelected != 2:
            canvas.itemconfig(data.answerB, fill = currentFill)
        if data.incorrectSelected != 3:
            canvas.itemconfig(data.answerC, fill = currentFill)
        if data.incorrectSelected != 4:
            canvas.itemconfig(data.answerD, fill = currentFill)
        canvas.itemconfig(data.questionlabel1, fill = currentFill)
        canvas.itemconfig(data.questionlabel2b, fill = currentFill)
        canvas.itemconfig(data.questionlabel2a, fill = currentFill)
        canvas.itemconfig(data.questionValueLabel, fill = currentFill)
        
        # data.oval1 (55, 95, 134)
        # data.oval2red (195, 85, 117)
        # data.oval2 (240, 240, 249)
        # data.oval3 (18, 44, 138)
        #fading out semicircular clock
        if data.clockAlreadyFaded == False: #infinite time not used
            if data.currentQuestion < 14:
                targetRed = floor(55 - 55 * proportion)
                targetGreen = floor(95 - 95 * proportion)
                targetBlue = floor(134 - 134 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval1, fill = currentFill)
                canvas.itemconfig(data.oval1, outline = currentFill)
                targetRed = floor(195 - 195 * proportion)
                targetGreen = floor(85 - 85 * proportion)
                targetBlue = floor(117 - 117 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval2red, fill = currentFill)
                targetRed = floor(240 - 240 * proportion)
                targetGreen = floor(240 - 240 * proportion)
                targetBlue = floor(249 - 249 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval2, fill = currentFill)
                targetRed = floor(17 - 17 * proportion)
                targetGreen = floor(48 - 48 * proportion)
                targetBlue = floor(79 - 79 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval2red, outline = currentFill)
                canvas.itemconfig(data.oval2, outline = currentFill)
                if data.ranOutOfTime == True: #ran out of time 
                    targetRedOval3 = 0
                    targetGreenOval3 = floor(15 - 15 * proportion)
                    targetBlueOval3 = floor(73 - 73 * proportion)
                    targetRedText = floor(155 - 155 * proportion)
                    targetGreenText = floor(158 - 158 * proportion)
                    targetBlueText = floor(191 - 191 * proportion)
                else: #wrong answer
                    targetRedOval3 = floor(18 - 18 * proportion)
                    targetGreenOval3 = floor(44 - 44 * proportion)
                    targetBlueOval3 = floor(138 - 138 * proportion)
                    targetRedText = floor(236 - 236 * proportion)
                    targetGreenText = floor(222 - 222 * proportion)
                    targetBlueText = floor(177 - 177 * proportion)
                fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
                canvas.itemconfig(data.oval3, fill = fillOval3)
                canvas.itemconfig(data.oval3, outline = fillOval3)
                fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
                canvas.itemconfig(data.timelabel, fill = fillText)
            else: #million dollar question golden clock fade out
                targetRed = floor(168 - 168 * proportion)
                targetGreen = floor(149 - 149 * proportion)
                targetBlue = floor(102 - 102 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval1, fill = currentFill)
                canvas.itemconfig(data.oval1, outline = currentFill)
                targetRed = floor(171 - 171 * proportion)
                targetGreen = floor(105 - 105 * proportion)
                targetBlue = floor(75 - 75 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval2red, fill = currentFill)
                targetRed = floor(223 - 223 * proportion)
                targetGreen = floor(206 - 206 * proportion)
                targetBlue = floor(142 - 142 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval2, fill = currentFill)
                targetRed = floor(223 - 223 * proportion)
                targetGreen = floor(206 - 206 * proportion)
                targetBlue = floor(142 - 142 * proportion)
                currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                canvas.itemconfig(data.oval2red, outline = currentFill)
                canvas.itemconfig(data.oval2, outline = currentFill)
                if data.ranOutOfTime == True: #ran out of time on milion
                    targetRedOval3 = floor(99 - 99 * proportion)
                    targetGreenOval3 = floor(74 - 74 * proportion)
                    targetBlueOval3 = floor(45 - 45 * proportion)
                    targetRedText = floor(156 - 156 * proportion)
                    targetGreenText = floor(159 - 159 * proportion)
                    targetBlueText = floor(192 - 192 * proportion)
                else: #wrong answer on million
                    targetRedOval3 = floor(138 - 138 * proportion)
                    targetGreenOval3 = floor(113 - 113 * proportion)
                    targetBlueOval3 = floor(36 - 36 * proportion)
                    targetRedText = floor(235 - 235 * proportion)
                    targetGreenText = floor(232 - 232 * proportion)
                    targetBlueText = floor(177 - 177 * proportion)
                fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
                canvas.itemconfig(data.oval3, fill = fillOval3)
                canvas.itemconfig(data.oval3, outline = fillOval3)
                fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
                canvas.itemconfig(data.timelabel, fill = fillText)
            if data.ranOutOfTime == False: #some circles inert some active
                for indicatorDot in range(15):
                    if indicatorDot > data.currentcir:
                        #active dot fade to black animation
                        if data.currentQuestion < 14: #non-million dollar fade
                            targetRed = floor(175 - 175 * proportion)
                            targetGreen = floor(253 - 253 * proportion)
                            targetBlue = floor(255 - 255 * proportion)
                        else: #million dollar question fade
                            targetRed = floor(255 - 255 * proportion)
                            targetGreen = floor(246 - 246 * proportion)
                            targetBlue = floor(204 - 204 * proportion)
                    else: #inert dot fade to black animation
                        if data.currentQuestion < 14: #non-million dollar fade
                            targetRed = floor(76 - 76 * proportion)
                            targetGreen = floor(91 - 91 * proportion)
                            targetBlue = floor(219 - 219 * proportion)
                        else: #million dollar question fade
                            targetRed = floor(165 - 165 * proportion)
                            targetGreen = floor(149 - 149 * proportion)
                            targetBlue = floor(81 - 81 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.circlesRight[indicatorDot], fill = currentFill)
                    canvas.itemconfig(data.circlesLeft[indicatorDot], fill = currentFill)
            else: #if user ran out of time, then all circles must be active
                for indicatorDot in range(15):
                    if data.currentQuestion < 14: #non-million dollar fade
                        targetRed = floor(175 - 175 * proportion)
                        targetGreen = floor(253 - 253 * proportion)
                        targetBlue = floor(255 - 255 * proportion)
                    else: #million dollar question fade
                        targetRed = floor(165 - 165 * proportion)
                        targetGreen = floor(149 - 149 * proportion)
                        targetBlue = floor(81 - 81 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.circlesRight[indicatorDot], fill = currentFill)
                    canvas.itemconfig(data.circlesLeft[indicatorDot], fill = currentFill)
        canvas.update()
    # remove any residual shades
    blackFill = "#000000"
    canvas.itemconfig(data.answerA, fill = blackFill)
    canvas.itemconfig(data.answerB, fill = blackFill)
    canvas.itemconfig(data.answerC, fill = blackFill)
    canvas.itemconfig(data.answerD, fill = blackFill)
    canvas.itemconfig(data.questionlabel1, fill = blackFill)
    canvas.itemconfig(data.questionlabel2b, fill = blackFill)
    canvas.itemconfig(data.questionlabel2a, fill = blackFill)
    canvas.itemconfig(data.questionValueLabel, fill = blackFill)
    canvas.itemconfig(data.labelA, fill = blackFill)
    canvas.itemconfig(data.labelB, fill = blackFill)
    canvas.itemconfig(data.labelC, fill = blackFill)
    canvas.itemconfig(data.labelD, fill = blackFill)
    canvas.itemconfig(data.oval1, fill = blackFill)
    canvas.itemconfig(data.oval1, outline = blackFill)
    canvas.itemconfig(data.oval2red, fill = blackFill)
    canvas.itemconfig(data.oval2, fill = blackFill)
    canvas.itemconfig(data.oval2red, outline = blackFill)
    canvas.itemconfig(data.oval2, outline = blackFill)
    canvas.itemconfig(data.oval3, fill = blackFill)
    canvas.itemconfig(data.oval3, outline = blackFill)
    canvas.itemconfig(data.timelabel, fill = blackFill)
    canvas.itemconfig(correctBgAnimation, fill = blackFill)
    if data.gameOver == True:
        if data.ranOutOfTime == False:
            canvas.itemconfig(correctBgYellow, 
                                  fill = blackFill)
    for indicatorDot in range(15):
        canvas.itemconfig(data.circlesRight[indicatorDot], fill = blackFill)
        canvas.itemconfig(data.circlesLeft[indicatorDot], fill = blackFill)
    canvas.update()
    if switchQuestion == False:
        instructions(canvas, data, False, "correct")
    else: #using switch the question
        instructions(canvas, data, False, "waitForAnswer")
    #variable resets
    data.questioncontent2b = "" #reset question contents
    data.questioncontent2a = ""
    data.questioncontent1 = ""
    canvas.itemconfig(data.questionlabel1, text = data.questioncontent1)
    canvas.itemconfig(data.questionlabel2b, text = data.questioncontent2b)
    canvas.itemconfig(data.questionlabel2a, text = data.questioncontent2a)
    data.answerTextA = "" #reset answer contents
    data.answerTextB = ""
    data.answerTextC = ""
    data.answerTextD = ""
    canvas.itemconfig(data.answerA, text = data.answerTextA)
    canvas.itemconfig(data.answerB, text = data.answerTextB)
    canvas.itemconfig(data.answerC, text = data.answerTextC)
    canvas.itemconfig(data.answerD, text = data.answerTextD)
    canvas.itemconfig(data.labelA, text = "")
    canvas.itemconfig(data.labelB, text = "")
    canvas.itemconfig(data.labelC, text = "")
    canvas.itemconfig(data.labelD, text = "")
    data.removedA = False #reset any removed answer choices
    data.removedB = False
    data.removedC = False
    data.removedD = False
    data.infiniteTimeActivate = False #stops any infinite time lifeline effects
    data.tempPreventDip = False
    data.tempPreventFifty = False
    data.tempPreventSwitch = False
    data.tempPreventInfiniteTime = False
    data.clockAlreadyFaded = False
    data.startTimeDotSwitch = False #in case a dot was in the middle of animating
    #resets any double dip muted channels
    data.channel0.set_volume(1)
    data.channel3.set_volume(1) # in case double dip was used on first 5 questions
                                # and the first dip was already correct
    #resets any lifelines that were temporarily deactivated 
    if data.usedFiftyFifty == False:
        canvas.itemconfig(data.fiftyFiftyOval, outline = "#456089")
        canvas.itemconfig(data.fiftyFiftyLabel, fill = "white")
        canvas.itemconfig(data.fiftyFiftyTop, fill = "white")
        canvas.itemconfig(data.fiftyFiftyBottom, fill = "white") 
    if data.usedDoubleDip == False:
        canvas.itemconfig(data.doubleDipOval, outline = "#456089")
        canvas.itemconfig(data.doubleDipLabel, fill = "white")
        canvas.itemconfig(data.doubleDipTop, fill = "white")
        canvas.itemconfig(data.doubleDipBottom, fill = "white")
    if data.usedSwitchQuestion == False:
        canvas.itemconfig(data.switchOval, outline = "#456089")
        canvas.itemconfig(data.switchLabel, fill = "white")
        canvas.itemconfig(data.switchTop1, fill = "white")
        canvas.itemconfig(data.switchTop2, fill = "white")
        canvas.itemconfig(data.switchTop3, fill = "white")
        canvas.itemconfig(data.switchBottom, fill = "white")
    if data.usedInfiniteTime == False:
        canvas.itemconfig(data.infiniteOval, outline = "#456089")
        canvas.itemconfig(data.infiniteTop1, fill = "white")
        canvas.itemconfig(data.infiniteTop2, fill = "white")
        canvas.itemconfig(data.infiniteBottom, fill = "white")
        canvas.itemconfig(data.infiniteLabel, fill = "white")
    canvas.itemconfig(data.oval2, extent = 180) #reset to full semicircle
    if switchQuestion == False:
        #updates the game information in the upper-right on winnings:
        if data.currentQuestion < 14:
            canvas.itemconfig(data.questionValueLabel,
                              text = "Question Value: " + data.winAmountsLabel[data.currentQuestion + 1])
            canvas.itemconfig(data.wonAmount,
                          text = "Current amount won: " + data.winAmountsLabel[data.currentQuestion])
            canvas.itemconfig(data.guaranteedAmount,
                          text = "Guaranteed amount won: " + data.guaranteedAmounts[data.currentQuestion])
        else:
            canvas.delete(data.questionValueLabel)
            canvas.delete(data.wonAmount)
            canvas.delete(data.guaranteedAmount)
        
        if data.gameOver == False:
            winFill = data.winAmounts[data.currentQuestion]
            canvas.itemconfig(data.winningsLabel, text = winFill) #assign amount won
            revealAnswerBars(canvas, data, True)
            if data.currentQuestion < 14:
                data.waitingOnShortReveal = True
        else: #game over
            if data.currentQuestion < 5: #lost before hitting $1,000 mark
                winFill = "$0"
            elif data.currentQuestion < 10:
                winFill = "$1,000"
            else:
                winFill = "$32,000"
            canvas.itemconfig(data.winningsLabel, text = winFill) #assign amount won
            revealAnswerBars(canvas, data, True)

def incorrectResponse(canvas, data, selection): #finishes the incorrect animation
    bgAnimations = [None, data.q1background, data.q2background,
                            data.q3background, data.q4background]
    labelAnimations = [None, data.labelA,data.labelB,data.labelC,data.labelD]                            
    correctBgAnimation = bgAnimations[selection]
    correctLabelAnimation = labelAnimations[selection]
    #4-stage animation: Stage 1: bright green to normal
    startTime = clock() 
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRed = 16 - floor(16 * proportion)
        targetGreen = 217 - floor(217 * proportion)
        targetBlue = 8 - floor(8 * proportion)
        currentFill= hexcolor(targetRed,
                              targetGreen, 
                              targetBlue)
        canvas.itemconfig(correctBgAnimation, 
                          fill = currentFill)
        canvas.itemconfig(correctLabelAnimation, #changes label to orange
                  fill = hexcolor(floor(223 * proportion),
                                  floor(146 * proportion),
                                  floor(32 * proportion)))
        canvas.update()
    #Stage 2: normal to median green
    startTime = clock() 
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRed = floor(6 * proportion)
        targetGreen = floor(169 * proportion)
        targetBlue = 0
        currentFill= hexcolor(targetRed,
                              targetGreen, 
                              targetBlue)
        canvas.itemconfig(correctBgAnimation, 
                          fill = currentFill)
        canvas.itemconfig(correctLabelAnimation, #changes label to black
                  fill = hexcolor(223 - floor(223 * proportion),
                                  146 -floor(146 * proportion),
                                  32 - floor(32 * proportion)))
        canvas.update()
    #Stage 3: median green to normal
    startTime = clock() 
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRed = 6 - floor(6 * proportion)
        targetGreen = 169 - floor(169 * proportion)
        targetBlue = 0
        currentFill= hexcolor(targetRed,
                              targetGreen, 
                              targetBlue)
        canvas.itemconfig(correctBgAnimation, 
                          fill = currentFill)
        canvas.itemconfig(correctLabelAnimation, #changes label to orange
                  fill = hexcolor(floor(223 * proportion),
                                  floor(146 * proportion),
                                  floor(32 * proportion)))
        canvas.update()
    #Stage 4: normal to median green for final time
    startTime = clock() 
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRed = floor(6 * proportion)
        targetGreen = floor(169 * proportion)
        targetBlue = 0
        currentFill= hexcolor(targetRed,
                              targetGreen, 
                              targetBlue)
        canvas.itemconfig(correctBgAnimation, 
                          fill = currentFill)
        canvas.itemconfig(correctLabelAnimation, #changes label to black
                  fill = hexcolor(223 - floor(223 * proportion),
                                  146 -floor(146 * proportion),
                                  32 - floor(32 * proportion)))
        canvas.update()
    if data.inInstruction == False:
        if data.transitionToGame == False:
            instructions(canvas, data, False, "incorrect")
            canvas.update()
            if data.switchQuestionActivate == True: #in switch the question phase
                data.waitingOSwitchQuestion = True
            else:
                data.gameOver = True

def switchTheQuestion(canvas, data):
    correctAnswer = int(data.currentQuestionAttributes[6])
    correctResponse(canvas, data, correctAnswer, True)
    shortRevealAll(canvas, data, True)

def seenQuestionBefore(data, questionID): 
    #for use with switch the question lifeline: checks if the
    #new question was seen before.
    if questionID in data.seenQuestions:
        return True
    else: return False

def removeQuestionBarForTheLastTime(canvas, data):
    startTime = clock() 
    animationDuration = 0.25 
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        #fade out winnings label
        if data.currentQuestion < 14: #non million dollar question
            targetRed = floor(199 - 199 * proportion)
            targetGreen = floor(211 - 211 * proportion)
            targetBlue = floor(247 - 247 * proportion)
        else: #million dollar fade out
            if data.gameOver == False: #golden fade out
                targetRed = floor(224 - 224 * proportion)
                targetGreen = floor(221 - 221 * proportion)
                targetBlue = floor(138 - 138 * proportion)   
            else: #regular fade out
                targetRed = floor(199 - 199 * proportion)
                targetGreen = floor(211 - 211 * proportion)
                targetBlue = floor(247 - 247 * proportion)         
        winningFill = hexcolor(targetRed,
                               targetGreen,
                               targetBlue)
        canvas.itemconfig(data.winningsLabel, fill = winningFill)

        #fade out question bar
        if data.currentQuestion < 14: #non million dollar question
            targetRed = floor(105 - 105 * proportion)
            targetGreen = floor(140 - 140 * proportion)
            targetBlue = floor(193 - 193 * proportion)
        else:
            if data.gameOver == False: #golden fade out
                targetRed = floor(222 - 222 * proportion)
                targetGreen = floor(212 - 212 * proportion)
                targetBlue = floor(156 - 156 * proportion)
            else: #regular fade out
                targetRed = floor(105 - 105 * proportion)
                targetGreen = floor(140 - 140 * proportion)
                targetBlue = floor(193 - 193 * proportion)
        currentFill = hexcolor(targetRed,
                               targetGreen,
                               targetBlue)
        canvas.itemconfig(data.questiontop, fill = currentFill)
        canvas.itemconfig(data.questiontopleft, fill = currentFill)
        canvas.itemconfig(data.questionbottomleft, fill = currentFill)
        canvas.itemconfig(data.questionleftdiagonattotop, outline = currentFill)
        canvas.itemconfig(data.questionleftdiagonaltobottom, outline = currentFill)
        canvas.itemconfig(data.questionlefttodiagonaltop, outline = currentFill)
        canvas.itemconfig(data.questionlefttodiagonalbottom, outline = currentFill)
        canvas.itemconfig(data.questionbottom, fill = currentFill)
        canvas.itemconfig(data.questionleft, fill = currentFill)
        canvas.itemconfig(data.questiontopright, fill = currentFill)
        canvas.itemconfig(data.questionbottomright, fill = currentFill)
        canvas.itemconfig(data.questionrightdiaonaltotop, outline = currentFill)
        canvas.itemconfig(data.questionrightdiagonaltobottom, outline = currentFill)
        canvas.itemconfig(data.questionrighttodiagonaltop, outline = currentFill)
        canvas.itemconfig(data.questionrighttodiagonalbottom, outline = currentFill)
        canvas.itemconfig(data.questionright, fill = currentFill)


        #fade out the instructions at the bottom of the window
        targetRGBWhite = floor(255 - 255 * proportion)
        currentWhiteFill = hexcolor(targetRGBWhite,
                                    targetRGBWhite,
                                    targetRGBWhite)
        canvas.itemconfig(data.instructBottom, fill = currentWhiteFill)
        canvas.itemconfig(data.instructTop, fill = currentWhiteFill)
        canvas.update()
    currentFill = hexcolor(0, 0, 0)
    canvas.itemconfig(data.questiontop, fill = currentFill)
    canvas.itemconfig(data.questiontopleft, fill = currentFill)
    canvas.itemconfig(data.questionbottomleft, fill = currentFill)
    canvas.itemconfig(data.questionleftdiagonattotop, outline = currentFill)
    canvas.itemconfig(data.questionleftdiagonaltobottom, outline = currentFill)
    canvas.itemconfig(data.questionlefttodiagonaltop, outline = currentFill)
    canvas.itemconfig(data.questionlefttodiagonalbottom, outline = currentFill)
    canvas.itemconfig(data.questionbottom, fill = currentFill)
    canvas.itemconfig(data.questionleft, fill = currentFill)
    canvas.itemconfig(data.questiontopright, fill = currentFill)
    canvas.itemconfig(data.questionbottomright, fill = currentFill)
    canvas.itemconfig(data.questionrightdiaonaltotop, outline = currentFill)
    canvas.itemconfig(data.questionrightdiagonaltobottom, outline = currentFill)
    canvas.itemconfig(data.questionrighttodiagonaltop, outline = currentFill)
    canvas.itemconfig(data.questionrighttodiagonalbottom, outline = currentFill)
    canvas.itemconfig(data.questionright, fill = currentFill)
    canvas.itemconfig(data.instructBottom, fill = currentFill)
    canvas.itemconfig(data.instructTop, fill = currentFill)
    canvas.itemconfig(data.winningsLabel, fill = currentFill)
    canvas.update()

def removeQuestionBar(canvas, data):
    data.longRevealNow = False
    startTime = clock() 
    animationDuration = 0.25 
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration

        #fade out winnings label
        targetRed = floor(199 - 199 * proportion)
        targetGreen = floor(211 - 211 * proportion)
        targetBlue = floor(247 - 247 * proportion)
        winningFill = hexcolor(targetRed,
                               targetGreen,
                               targetBlue)
        canvas.itemconfig(data.winningsLabel, fill = winningFill)

        #fade out question bar
        targetRed = floor(105 - 105 * proportion)
        targetGreen = floor(140 - 140 * proportion)
        targetBlue = floor(193 - 193 * proportion)
        currentFill = hexcolor(targetRed,
                               targetGreen,
                               targetBlue)
        canvas.itemconfig(data.questiontop, fill = currentFill)
        canvas.itemconfig(data.questiontopleft, fill = currentFill)
        canvas.itemconfig(data.questionbottomleft, fill = currentFill)
        canvas.itemconfig(data.questionleftdiagonattotop, outline = currentFill)
        canvas.itemconfig(data.questionleftdiagonaltobottom, outline = currentFill)
        canvas.itemconfig(data.questionlefttodiagonaltop, outline = currentFill)
        canvas.itemconfig(data.questionlefttodiagonalbottom, outline = currentFill)
        canvas.itemconfig(data.questionbottom, fill = currentFill)
        canvas.itemconfig(data.questionleft, fill = currentFill)
        canvas.itemconfig(data.questiontopright, fill = currentFill)
        canvas.itemconfig(data.questionbottomright, fill = currentFill)
        canvas.itemconfig(data.questionrightdiaonaltotop, outline = currentFill)
        canvas.itemconfig(data.questionrightdiagonaltobottom, outline = currentFill)
        canvas.itemconfig(data.questionrighttodiagonaltop, outline = currentFill)
        canvas.itemconfig(data.questionrighttodiagonalbottom, outline = currentFill)
        canvas.itemconfig(data.questionright, fill = currentFill)

        #fade out instructions temporarily
        targetRGB = floor(255 - 255 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.instructBottom, fill = currentFill)
        canvas.itemconfig(data.instructTop, fill = currentFill)
        canvas.update()
    #reset clock appearance variables
    data.questionBarSwitch = True
    canvas.delete("all")
    drawLifelinesWithoutAnimation(canvas, data)
    canvas.update()
    data.colors = []
    data.circlesLeft=[]
    data.circlesRight=[]
    for j in range(15): #reset dots
        data.colors.append([0-j*16,0-j*15,0-j*15,0])
    data.currentcir = 14
    data.inerttoactiveswitch = 0
    data.startTimeDotSwitch = False #in case a dot was in the middle of animating
    data.currentSecond = 0

    #redraw instructions
    if data.currentQuestion == 5:
        data.instructionsBottom = "For the next 5 questions, you have 30 seconds on the clock"
        data.instructionsTop = ""
    elif data.currentQuestion == 10:
        data.instructionsBottom = "For the next 4 questions, you have 45 seconds on the clock"
        data.instructionsTop = ""
    elif data.currentQuestion == 14:
        data.instructionsTop = "For the million dollar question, you will have"
        data.instructionsBottom = "45 seconds plus your banked time..." 

    # wait to actually draw the instructions to right before the clock appears

    #reset clock and question bar coordinates
    data.xtop1 = 700
    data.ytop1 = 600
    data.xbottom1 = data.xtop1
    data.ybottom1 = data.ytop1
    data.xtop2 = data.xtop1
    data.ytop2 = data.ytop1
    data.xbottom2 = data.xtop1
    data.ybottom2 = data.ytop1
    data.xtop3 = data.xtop1
    data.ytop3 = data.ytop1
    data.xbottom3 = data.xtop1
    data.ybottom3 = data.ytop1
    data.timeTextX = data.xtop1
    data.timeTextY = data.ytop1

    data.topleftx = 170
    data.toplefty = 600 #how far down the question bar is
    data.toprightx = 1230 # how wide is the bar
    data.toprighty = data.toplefty

    data.bottomleftx = data.topleftx
    data.bottomlefty = data.toplefty + 115 #115 is gap between top and bottom
    data.bottomrightx = data.toprightx
    data.bottomrighty = data.toprighty + 115 #115 is gap between top and bottom

    data.topleftx1 = 140
    data.toplefty1 = data.bottomlefty + 15
    data.toprightx1 = 630 # how wide is the bar
    data.toprighty1 = data.toplefty1

    data.bottomleftx1 = data.topleftx1
    data.bottomlefty1 = data.toplefty1 + 72 #72 is gap between top and bottom
    data.bottomrightx1 = data.toprightx1
    data.bottomrighty1 = data.toprighty1 + 72 #72 is gap between top and bottom

    data.topleftx2 = 770
    data.toplefty2 = data.bottomlefty + 15
    data.toprightx2 = 1260 # how wide is the bar
    data.toprighty2 = data.toplefty2

    data.bottomleftx2 = data.topleftx2
    data.bottomlefty2 = data.toplefty2 + 72 #72 is gap between top and bottom
    data.bottomrightx2 = data.toprightx2
    data.bottomrighty2 = data.toprighty2 + 72 #72 is gap between top and bottom

    data.topleftx3 = 140
    data.toplefty3 = data.bottomlefty2 + 15
    data.toprightx3 = 630 # how wide is the bar
    data.toprighty3 = data.toplefty3

    data.bottomleftx3 = data.topleftx3
    data.bottomlefty3 = data.toplefty3 + 72 #72 is gap between top and bottom
    data.bottomrightx3 = data.toprightx3
    data.bottomrighty3 = data.toprighty3 + 72 #72 is gap between top and bottom

    data.topleftx4 = 770
    data.toplefty4 = data.bottomlefty2 + 15
    data.toprightx4 = 1260 # how wide is the bar
    data.toprighty4 = data.toplefty4

    data.bottomleftx4 = data.topleftx4
    data.bottomlefty4 = data.toplefty4 + 72 #72 is gap between top and bottom
    data.bottomrightx4 = data.toprightx4
    data.bottomrighty4 = data.toprighty4 + 72 #72 is gap between top and bottom
    data.clockFontSize = 48
    #start let's play music for next question
    data.questionLetsPlay = mixer.Sound(data.path + data.letsPlaySounds[data.currentQuestion])
    data.channel0.play(data.questionLetsPlay)
    canvas.after(4000)
    data.waitingOnReveal = True
    instructions(canvas, data, True, 0) # now draw the instructions
    clockappear(canvas,data)

def drawQuestions(canvas, data):
    #######Answer Choice top left
    #left side
    data.answerHeight = 565 
    topleftx1 = 140
    toplefty1 = data.answerHeight + 15
    toprightx1 = 630 # how wide is the bar
    toprighty1 = toplefty1

    bottomleftx1 = topleftx1
    bottomlefty1 = toplefty1 + 72 #72 is gap between top and bottom
    bottomrightx1 = toprightx1
    bottomrighty1 = toprighty1 + 72 #72 is gap between top and bottom

    #answer backgrounds
    data.q1background = canvas.create_rectangle(topleftx1 - 40, toplefty1, bottomrightx1 + 42, bottomrighty1, fill = "black")
    data.topleftcover1a = canvas.create_arc(topleftx1 - 58, toplefty1-30, topleftx1 - 20, toplefty1 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.topleftcover1b = canvas.create_arc(topleftx1 - 45, toplefty1-30, topleftx1-4, toplefty1 + 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.bottomleftcover1a = canvas.create_arc(bottomleftx1 - 58, bottomlefty1 + 30, bottomleftx1 - 20, bottomlefty1 - 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.bottomleftcover1b = canvas.create_arc(bottomleftx1 - 45, bottomlefty1 + 30, bottomleftx1-4, bottomlefty1 - 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.toprightcover1a = canvas.create_arc(toprightx1 + 60, toprighty1-30, toprightx1 + 22, toprighty1 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.toprightcover1b = canvas.create_arc(toprightx1 + 56, toprighty1-29, toprightx1 + 7, toprighty1 + 19, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.bottomrightcover1a = canvas.create_arc(bottomrightx1 + 60, bottomrighty1-31, bottomrightx1 + 22, bottomrighty1 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)
    data.bottomrightcover1b = canvas.create_arc(bottomrightx1 + 56, bottomrighty1-20, bottomrightx1 + 8, bottomrighty1 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)

    ###Answer labels
    data.topAnswerABCDOffsetX = 20 #offset for labels A:, B:, C:, D:
    data.labelABCDSpacing = 5 #spaces the actual answers from ABCD labels
    data.topAnswerActualOffsetX = (data.topAnswerABCDOffsetX -
                                            data.labelABCDSpacing)
    data.topAnswerOffsetY = 50 #offsets the Y coordinate of top answers
    data.topAnswerY = data.answerHeight + data.topAnswerOffsetY
    data.leftAnswerABCDX = data.topleftx - data.topAnswerABCDOffsetX
    data.leftAnswerActualX = data.topleftx + data.labelABCDSpacing
    data.answerTextA = ""
    data.labelA = canvas.create_text(data.leftAnswerABCDX,
                                      data.topAnswerY,
                                      text = "",
                                      font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")
    data.answerA = canvas.create_text(data.leftAnswerActualX,
                                      data.topAnswerY,
                                      text = data.answerTextA,
                                      font = ("Conduit ITC Medium", 32),
                                      anchor = "w",
                                      fill = "#000000")

    ###connecting lines
    data.questiontopleft1 = canvas.create_line(topleftx1 - 33, toplefty1 + 30, topleftx1 - 9, toplefty1 + 4, fill = "#000000", width = 4)
    data.questionbottomleft1 = canvas.create_line(topleftx1 - 34, toplefty1 + 43, topleftx1 - 9, toplefty1 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questiontop1 = canvas.create_line(topleftx1, toplefty1, toprightx1, toprighty1, fill = "#000000", width = 4)
    xa = 20 #curvature coefficients
    ya = 80 #curvature coefficients
    data.questionleftdiagonattotop1 = canvas.create_arc(topleftx1 - xa, toplefty1, topleftx1 + xa, toplefty1 + ya, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 30)
    data.questionleftdiagonaltobottom1 = canvas.create_arc(topleftx1 - xa, bottomlefty1 - ya, topleftx1 + xa, bottomlefty1, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 240, extent = 30)
    x1a = 30 #curvature coefficients
    y1a = 50 #curvature coefficients
    data.questionlefttodiagonaltop1 = canvas.create_arc((topleftx1 - 45) - x1a, round((toplefty1 + bottomlefty1)/2) - y1a, (topleftx1 - 55) + x1a, round((toplefty1 + bottomlefty1)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 44)
    data.questionlefttodiagonalbottom1 = canvas.create_arc((topleftx1 - 45) - x1a, round((toplefty1 + bottomlefty1)/2), (topleftx1 - 55) + x1a, round((toplefty1 + bottomlefty1)/2) + y1a, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 46, extent = 44)

    data.questionbottom1 = canvas.create_line(bottomleftx1, bottomlefty1, bottomrightx1, bottomrighty1, fill = "#000000", width = 4)
    data.questionleft1 = canvas.create_line(0, round((toplefty1 + bottomlefty1)/2), topleftx1 - 40, round((toplefty1 + bottomlefty1)/2), fill = "#000000", width = 4)

    #right side

    ###connecting lines
    data.questiontopright1 = canvas.create_line(toprightx1 + 33, toprighty1 + 30, toprightx1 + 9, toprighty1 + 4, fill = "#000000", width = 4)
    data.questionbottomright1 = canvas.create_line(toprightx1 + 34, toprighty1 + 43, toprightx1 + 9, toprighty1 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questionrightdiaonaltotop1 = canvas.create_arc(toprightx1 - xa, toprighty1, toprightx1 + xa, toprighty1 + ya, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 60, extent = 30)
    data.questionrightdiagonaltobottom1 = canvas.create_arc(toprightx1 - xa, bottomrighty1 - ya, toprightx1 + xa, bottomrighty1, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 30)
    data.questionrighttodiagonaltop1 = canvas.create_arc(toprightx1 + 51 - x1a, round((toplefty1 + bottomlefty1)/2) - y1a, toprightx1 + 61 + x1a, round((toplefty1 + bottomlefty1)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 226, extent = 44) #anomalous
    data.questionrighttodiagonalbottom1 = canvas.create_arc(toprightx1 + 52 - x1a, round((toplefty1 + bottomlefty1)/2), toprightx1 + 62 + x1a, round((toplefty1 + bottomlefty1)/2) + y1a, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 44)



    #######Answer Choice top right
    #left side
    topleftx2 = 770
    toplefty2 = data.answerHeight + 15
    toprightx2 = 1260 # how wide is the bar
    toprighty2 = toplefty2

    bottomleftx2 = topleftx2
    bottomlefty2 = toplefty2 + 72 #72 is gap between top and bottom
    bottomrightx2 = toprightx2
    bottomrighty2 = toprighty2 + 72 #72 is gap between top and bottom

    #answer backgrounds
    data.q2background = canvas.create_rectangle(topleftx2 - 40, toplefty2, bottomrightx2 + 42, bottomrighty2, fill = "black")
    data.topleftcover2a = canvas.create_arc(topleftx2 - 58, toplefty2-30, topleftx2 - 20, toplefty2 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.topleftcover2b = canvas.create_arc(topleftx2 - 45, toplefty2-30, topleftx2-4, toplefty2 + 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.bottomleftcover2a = canvas.create_arc(bottomleftx2 - 58, bottomlefty2 + 30, bottomleftx2 - 20, bottomlefty2 - 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.bottomleftcover2b = canvas.create_arc(bottomleftx2 - 45, bottomlefty2 + 30, bottomleftx2-4, bottomlefty2 - 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.toprightcover2a = canvas.create_arc(toprightx2 + 60, toprighty2-30, toprightx2 + 22, toprighty2 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.toprightcover2b = canvas.create_arc(toprightx2 + 56, toprighty2-29, toprightx2 + 7, toprighty2 + 19, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.bottomrightcover2a = canvas.create_arc(bottomrightx2 + 60, bottomrighty2-31, bottomrightx2 + 22, bottomrighty2 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)
    data.bottomrightcover2b = canvas.create_arc(bottomrightx2 + 56, bottomrighty2-20, bottomrightx2 + 8, bottomrighty2 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)

    ###Answer labels
    data.rightAnswerOffsetX = 170 #horizontal offset for rightside answers text
    data.rightAnswerABCDX = (data.toprightx1 - data.topAnswerABCDOffsetX
                                + data.rightAnswerOffsetX)
    data.rightAnswerActualX = (data.toprightx1 + data.labelABCDSpacing
                                  + data.rightAnswerOffsetX)
    data.answerTextB = ""
    data.labelB = canvas.create_text(data.rightAnswerABCDX,
                                      data.topAnswerY,
                                      text = "",
                                      font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")
    data.answerB = canvas.create_text(data.rightAnswerActualX,
                                      data.topAnswerY,
                                      text = data.answerTextB,
                                      font = ("Conduit ITC Medium", 32),
                                      anchor = "w",
                                      fill = "#000000")

    ###connecting lines
    data.questiontopleft2 = canvas.create_line(topleftx2 - 33, toplefty2 + 30, topleftx2 - 9, toplefty2 + 4, fill = "#000000", width = 4)
    data.questionbottomleft2 = canvas.create_line(topleftx2 - 34, toplefty2 + 43, topleftx2 - 9, toplefty2 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questiontop2 = canvas.create_line(topleftx2, toplefty2, toprightx2, toprighty2, fill = "#000000", width = 4)
    xb = 20 #curvature coefficients
    yb = 80 #curvature coefficients
    data.questionleftdiagonattotop2 = canvas.create_arc(topleftx2 - xb, toplefty2, topleftx2 + xb, toplefty2 + yb, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 30)
    data.questionleftdiagonaltobottom2 = canvas.create_arc(topleftx2 - xb, bottomlefty2 - yb, topleftx2 + xb, bottomlefty2, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 240, extent = 30)
    x1b = 30 #curvature coefficients
    y1b = 50 #curvature coefficients
    data.questionlefttodiagonaltop2 = canvas.create_arc((topleftx2 - 45) - x1b, round((toplefty2 + bottomlefty2)/2) - y1b, (topleftx2 - 55) + x1b, round((toplefty2 + bottomlefty2)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 44)
    data.questionlefttodiagonalbottom2 = canvas.create_arc((topleftx2 - 45) - x1b, round((toplefty2 + bottomlefty2)/2), (topleftx2 - 55) + x1b, round((toplefty2 + bottomlefty2)/2) + y1b, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 46, extent = 44)

    data.questionbottom2 = canvas.create_line(bottomleftx2, bottomlefty2, bottomrightx2, bottomrighty2, fill = "#000000", width = 4)


    #right side

    ###connecting lines
    data.questiontopright2 = canvas.create_line(toprightx2 + 33, toprighty2 + 30, toprightx2 + 9, toprighty2 + 4, fill = "#000000", width = 4)
    data.questionbottomright2 = canvas.create_line(toprightx2 + 34, toprighty2 + 43, toprightx2 + 9, toprighty2 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questionrightdiaonaltotop2 = canvas.create_arc(toprightx2 - xb, toprighty2, toprightx2 + xb, toprighty2 + yb, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 60, extent = 30)
    data.questionrightdiagonaltobottom2 = canvas.create_arc(toprightx2 - xb, bottomrighty2 - yb, toprightx2 + xb, bottomrighty2, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 30)
    data.questionrighttodiagonaltop2 = canvas.create_arc(toprightx2 + 51 - x1b, round((toplefty2 + bottomlefty2)/2) - y1b, toprightx2 + 61 + x1b, round((toplefty2 + bottomlefty2)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 226, extent = 44) #anomalous
    data.questionrighttodiagonalbottom2 = canvas.create_arc(toprightx2 + 52 - x1b, round((toplefty2 + bottomlefty2)/2), toprightx2 + 62 + x1b, round((toplefty2 + bottomlefty2)/2) + y1b, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 44)

    data.questionright2 = canvas.create_line(toprightx2 + 50, round((toplefty2 + bottomlefty2)/2), 1500, round((toplefty2 + bottomlefty2)/2), fill = "#000000", width = 4)

    ###top middle line 
    data.middletop = canvas.create_line(680, round((toplefty2 + bottomlefty2)/2), 720, round((toplefty2 + bottomlefty2)/2), fill = "#000000", width = 4)
    ###
    ####################################################################
    #Following is just a copy of the code above with minor modifications

    #######Answer Choices bottom left
    #left side
    topleftx3 = 140
    toplefty3 = bottomlefty2 + 15
    toprightx3 = 630 # how wide is the bar
    toprighty3 = toplefty3

    bottomleftx3 = topleftx3
    bottomlefty3 = toplefty3 + 72 #72 is gap between top and bottom
    bottomrightx3 = toprightx3
    bottomrighty3 = toprighty3 + 72 #72 is gap between top and bottom

    #answer backgrounds
    data.q3background = canvas.create_rectangle(topleftx3 - 40, toplefty3, bottomrightx3 + 42, bottomrighty3, fill = "black")
    data.topleftcover3a = canvas.create_arc(topleftx3 - 58, toplefty3-30, topleftx3 - 20, toplefty3 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.topleftcover3b = canvas.create_arc(topleftx3 - 45, toplefty3-30, topleftx3-4, toplefty3 + 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.bottomleftcover3a = canvas.create_arc(bottomleftx3 - 58, bottomlefty3 + 30, bottomleftx3 - 20, bottomlefty3 - 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.bottomleftcover3b = canvas.create_arc(bottomleftx3 - 45, bottomlefty3 + 30, bottomleftx3-4, bottomlefty3 - 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.toprightcover3a = canvas.create_arc(toprightx3 + 60, toprighty3-30, toprightx3 + 22, toprighty3 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.toprightcover3b = canvas.create_arc(toprightx3 + 56, toprighty3-29, toprightx3 + 7, toprighty3 + 19, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.bottomrightcover3a = canvas.create_arc(bottomrightx3 + 60, bottomrighty3-31, bottomrightx3 + 22, bottomrighty3 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)
    data.bottomrightcover3b = canvas.create_arc(bottomrightx3 + 56, bottomrighty3-20, bottomrightx3 + 8, bottomrighty3 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)
    
    ###Answer labels
    data.bottomTopGap = 87 #gap between bottom answers and top answers
    data.bottomAnswerOffsetY = data.topAnswerOffsetY + data.bottomTopGap
    data.bottomAnswerY = data.answerHeight + data.bottomAnswerOffsetY
    data.answerTextC = ""
    data.labelC = canvas.create_text(data.leftAnswerABCDX,
                                      data.bottomAnswerY,
                                      text = "",
                                      font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")
    data.answerC = canvas.create_text(data.leftAnswerActualX,
                                      data.bottomAnswerY,
                                      text = data.answerTextC,
                                      font = ("Conduit ITC Medium", 32),
                                      anchor = "w",
                                      fill = "#000000")

    ###connecting lines
    data.questiontopleft3 = canvas.create_line(topleftx3 - 33, toplefty3 + 30, topleftx3 - 9, toplefty3 + 4, fill = "#000000", width = 4)
    data.questionbottomleft3 = canvas.create_line(topleftx3 - 34, toplefty3 + 43, topleftx3 - 9, toplefty3 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questiontop3 = canvas.create_line(topleftx3, toplefty3, toprightx3, toprighty3, fill = "#000000", width = 4)

    data.questionleftdiagonattotop3 = canvas.create_arc(topleftx3 - xa, toplefty3, topleftx3 + xa, toplefty3 + ya, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 30)
    data.questionleftdiagonaltobottom3 = canvas.create_arc(topleftx3 - xa, bottomlefty3 - ya, topleftx3 + xa, bottomlefty3, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 240, extent = 30)

    data.questionlefttodiagonaltop3 = canvas.create_arc((topleftx3 - 45) - x1a, round((toplefty3 + bottomlefty3)/2) - y1a, (topleftx3 - 55) + x1a, round((toplefty3 + bottomlefty3)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 44)
    data.questionlefttodiagonalbottom3 = canvas.create_arc((topleftx3 - 45) - x1a, round((toplefty3 + bottomlefty3)/2), (topleftx3 - 55) + x1a, round((toplefty3 + bottomlefty3)/2) + y1a, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 46, extent = 44)

    data.questionbottom3 = canvas.create_line(bottomleftx3, bottomlefty3, bottomrightx3, bottomrighty3, fill = "#000000", width = 4)
    data.questionleft3 = canvas.create_line(0, round((toplefty3 + bottomlefty3)/2), topleftx3 - 40, round((toplefty3 + bottomlefty3)/2), fill = "#000000", width = 4)

    #right side

    ###connecting lines
    data.questiontopright3 = canvas.create_line(toprightx3 + 33, toprighty3 + 30, toprightx3 + 9, toprighty3 + 4, fill = "#000000", width = 4)
    data.questionbottomright3 = canvas.create_line(toprightx3 + 34, toprighty3 + 43, toprightx3 + 9, toprighty3 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questionrightdiaonaltotop3 = canvas.create_arc(toprightx3 - xa, toprighty3, toprightx3 + xa, toprighty3 + ya, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 60, extent = 30)
    data.questionrightdiagonaltobottom3 = canvas.create_arc(toprightx3 - xa, bottomrighty3 - ya, toprightx3 + xa, bottomrighty3, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 30)
    data.questionrighttodiagonaltop3 = canvas.create_arc(toprightx3 + 51 - x1a, round((toplefty3 + bottomlefty3)/2) - y1a, toprightx3 + 61 + x1a, round((toplefty3 + bottomlefty3)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 226, extent = 44) #anomalous
    data.questionrighttodiagonalbottom3 = canvas.create_arc(toprightx3 + 52 - x1a, round((toplefty3 + bottomlefty3)/2), toprightx3 + 62 + x1a, round((toplefty3 + bottomlefty3)/2) + y1a, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 44)

    #######Answer Choice bottom right
    #left side
    topleftx4 = 770
    toplefty4 = bottomlefty2 + 15
    toprightx4 = 1260 # how wide is the bar
    toprighty4 = toplefty4

    bottomleftx4 = topleftx4
    bottomlefty4 = toplefty4 + 72 #72 is gap between top and bottom
    bottomrightx4 = toprightx4
    bottomrighty4 = toprighty4 + 72 #72 is gap between top and bottom


    #answer backgrounds
    data.q4background = canvas.create_rectangle(topleftx4 - 40, toplefty4, bottomrightx4 + 42, bottomrighty4, fill = "black")
    data.topleftcover4a = canvas.create_arc(topleftx4 - 58, toplefty4-30, topleftx4 - 20, toplefty4 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.topleftcover4b = canvas.create_arc(topleftx4 - 45, toplefty4-30, topleftx4-4, toplefty4 + 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 270, extent = 90)
    data.bottomleftcover4a = canvas.create_arc(bottomleftx4 - 58, bottomlefty4 + 30, bottomleftx4 - 20, bottomlefty4 - 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.bottomleftcover4b = canvas.create_arc(bottomleftx4 - 45, bottomlefty4 + 30, bottomleftx4-4, bottomlefty4 - 15, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 0, extent = 90)
    data.toprightcover4a = canvas.create_arc(toprightx4 + 60, toprighty4-30, toprightx4 + 22, toprighty4 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.toprightcover4b = canvas.create_arc(toprightx4 + 56, toprighty4-29, toprightx4 + 7, toprighty4 + 19, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 180, extent = 90)
    data.bottomrightcover4a = canvas.create_arc(bottomrightx4 + 60, bottomrighty4-31, bottomrightx4 + 22, bottomrighty4 + 32, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)
    data.bottomrightcover4b = canvas.create_arc(bottomrightx4 + 56, bottomrighty4-20, bottomrightx4 + 8, bottomrighty4 + 30, style = "pieslice",
     fill = "black", outline = "black", width = 1, start = 90, extent = 90)
    
    ###Answer labels
    data.answerTextD = ""
    data.labelD = canvas.create_text(data.rightAnswerABCDX,
                                      data.bottomAnswerY,
                                      text = "",
                                      font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")
    data.answerD = canvas.create_text(data.rightAnswerActualX,
                                      data.bottomAnswerY,
                                      text = data.answerTextD,
                                      font = ("Conduit ITC Medium", 32),
                                      anchor = "w",
                                      fill = "#000000")

    ###connecting lines
    data.questiontopleft4 = canvas.create_line(topleftx4 - 33, toplefty4 + 30, topleftx4 - 9, toplefty4 + 4, fill = "#000000", width = 4)
    data.questionbottomleft4 = canvas.create_line(topleftx4 - 34, toplefty4 + 43, topleftx4 - 9, toplefty4 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questiontop4 = canvas.create_line(topleftx4, toplefty4, toprightx4, toprighty4, fill = "#000000", width = 4)

    data.questionleftdiagonattotop4 = canvas.create_arc(topleftx4 - xb, toplefty4, topleftx4 + xb, toplefty4 + yb, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 30)
    data.questionleftdiagonaltobottom4 = canvas.create_arc(topleftx4 - xb, bottomlefty4 - yb, topleftx4 + xb, bottomlefty4, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 240, extent = 30)

    data.questionlefttodiagonaltop4 = canvas.create_arc((topleftx4 - 45) - x1b, round((toplefty4 + bottomlefty4)/2) - y1b, (topleftx4 - 55) + x1b, round((toplefty4 + bottomlefty4)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 44)
    data.questionlefttodiagonalbottom4 = canvas.create_arc((topleftx4 - 45) - x1b, round((toplefty4 + bottomlefty4)/2), (topleftx4 - 55) + x1b, round((toplefty4 + bottomlefty4)/2) + y1b, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 46, extent = 44)

    data.questionbottom4 = canvas.create_line(bottomleftx4, bottomlefty4, bottomrightx4, bottomrighty4, fill = "#000000", width = 4)


    #right side

    ###connecitng lines
    data.questiontopright4 = canvas.create_line(toprightx4 + 33, toprighty4 + 30, toprightx4 + 9, toprighty4 + 4, fill = "#000000", width = 4)
    data.questionbottomright4 = canvas.create_line(toprightx4 + 34, toprighty4 + 43, toprightx4 + 9, toprighty4 + 67, fill = "#000000", width = 4) #y=1.16(x-194)-108
    ###

    data.questionrightdiaonaltotop4 = canvas.create_arc(toprightx4 - xb, toprighty4, toprightx4 + xb, toprighty4 + yb, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 60, extent = 30)
    data.questionrightdiagonaltobottom4 = canvas.create_arc(toprightx4 - xb, bottomrighty4 - yb, toprightx4 + xb, bottomrighty4, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 270, extent = 30)
    data.questionrighttodiagonaltop4 = canvas.create_arc(toprightx4 + 51 - x1b, round((toplefty4 + bottomlefty4)/2) - y1b, toprightx4 + 61 + x1b, round((toplefty4 + bottomlefty4)/2), style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 226, extent = 44) #anomalous
    data.questionrighttodiagonalbottom4 = canvas.create_arc(toprightx4 + 52 - x1b, round((toplefty4 + bottomlefty4)/2), toprightx4 + 62 + x1b, round((toplefty4 + bottomlefty4)/2) + y1b, style = "arc",
     fill = "black", outline = "#000000", width = 4, start = 90, extent = 44)

    data.questionright4 = canvas.create_line(toprightx4 + 50, round((toplefty4 + bottomlefty4)/2), 1500, round((toplefty4 + bottomlefty4)/2), fill = "#000000", width = 4)

    ###top middle line 
    data.middlebottom = canvas.create_line(680, round((toplefty4 + bottomlefty4)/2), 720, round((toplefty4 + bottomlefty4)/2), fill = "#000000", width = 4)
    ###

    ###Question Bar########################
    #left side
    topleftx = 170
    toplefty = 600 #how far down the question bar is #450 for normal mode 600 for initial
    toprightx = 1230 # how wide is the bar
    toprighty = toplefty

    bottomleftx = topleftx
    bottomlefty = toplefty + 115 #115 is gap between top and bottom
    bottomrightx = toprightx
    bottomrighty = toprighty + 115 #115 is gap between top and bottom
    data.questionTopCoord = (data.topleftx,
                            data.toplefty,
                            data.toprightx,
                            data.toprighty)
    data.questiontop = canvas.create_line(data.questionTopCoord,
                                          fill = "#000000",
                                          width = 4)
    data.questionTopLeftCoord = (data.topleftx - 50, 
                                 data.toplefty + 51,
                                 data.topleftx - 10,
                                 data.toplefty + 4)
    data.questiontopleft = canvas.create_line(data.questionTopLeftCoord,
                                              fill = "#000000",
                                              width = 4) #y=1.16(x-194)-108
    data.questionBottomLeftCoord = (data.bottomleftx - 50,
                                    data.bottomlefty - 50,
                                    data.bottomleftx - 10,
                                    data.bottomlefty - 4)
    data.questionbottomleft = canvas.create_line(data.questionBottomLeftCoord,
                                                 fill = "#000000",
                                                 width = 4) #y=-1.16(x-194)-108
    data.x = 30 #curvature coefficients
    data.y = 80 #curvature coefficients
    data.qLeftDiagonalToTopCoord = (data.topleftx - data.x,
                                    data.toplefty,
                                    data.topleftx + data.x,
                                    data.toplefty + data.y)
    data.questionleftdiagonattotop = canvas.create_arc(data.qLeftDiagonalToTopCoord,
                                                       style = "arc",
                                                       fill = "black",
                                                       outline = "#000000",
                                                       width = 4,
                                                       start = 90,
                                                       extent = 70)
    data.qLeftDiagonalToBottomCoord = (data.topleftx - data.x,
                                       data.bottomlefty - data.y,
                                       data.topleftx + data.x,
                                       data.bottomlefty)
    data.questionleftdiagonaltobottom = canvas.create_arc(data.qLeftDiagonalToBottomCoord,
                                                          style = "arc",
                                                          fill = "black",
                                                          outline = "#000000",
                                                          width = 4,
                                                          start = 200,
                                                          extent = 70)
    data.x1 = 30 #curvature coefficients
    data.y1 = 50 #curvature coefficients
    data.qLeftToDiagonalTopCoord = ((data.topleftx - 60) - data.x1,
                                    round((data.toplefty + data.bottomlefty)/2) - data.y1,
                                    (data.topleftx - 70) + data.x1,
                                    round((data.toplefty + data.bottomlefty)/2))
    data.questionlefttodiagonaltop = canvas.create_arc(data.qLeftToDiagonalTopCoord,
                                                       style = "arc",
                                                       fill = "black",
                                                       outline = "#000000",
                                                       width = 4,
                                                       start = 270,
                                                       extent = 70)
    data.qLeftToDiagonalBottomCoord = ((data.topleftx - 60) - data.x1,
                                       round((data.toplefty + data.bottomlefty)/2),
                                       (data.topleftx - 70) + data.x1,
                                       round((data.toplefty + data.bottomlefty)/2) + data.y1)
    data.questionlefttodiagonalbottom = canvas.create_arc(data.qLeftToDiagonalBottomCoord,
                                                          style = "arc",
                                                          fill = "black",
                                                          outline = "#000000",
                                                          width = 4,
                                                          start = 20,
                                                          extent = 70)
    data.questionBottomCoord = (data.bottomleftx,
                                data.bottomlefty,
                                data.bottomrightx,
                                data.bottomrighty)
    data.questionbottom = canvas.create_line(data.questionBottomCoord,
                                             fill = "#000000",
                                             width = 4)
    data.questionLeftCoord = (0,
                              round((data.toplefty + data.bottomlefty)/2),
                              data.topleftx - 65,
                              round((data.toplefty + data.bottomlefty)/2))
    data.questionleft = canvas.create_line(data.questionLeftCoord,
                                           fill = "#000000",
                                           width = 4)

    #right side
    data.questionTopRightCoord = (data.toprightx + 50,
                                  data.toprighty + 51,
                                  data.toprightx + 10,
                                  data.toprighty + 4)
    data.questiontopright = canvas.create_line(data.questionTopRightCoord,
                                               fill = "#000000",
                                               width = 4) #y=-1.16(x-194)-108
    data.questionBottomRightCoord = (data.bottomrightx + 50,
                                    data.bottomrighty - 50,
                                    data.bottomrightx + 10,
                                    data.bottomrighty - 4)
    data.questionbottomright = canvas.create_line(data.questionBottomRightCoord,
                                                  fill = "#000000",
                                                  width = 4) #y=1.16(x-194)-108
    data.qRightDiagonalToTopCoord = (data.toprightx - data.x,
                                    data.toprighty,
                                    data.toprightx + data.x,
                                    data.toprighty + data.y,)
    data.questionrightdiaonaltotop = canvas.create_arc(data.qRightDiagonalToTopCoord,
                                                       style = "arc",
                                                       fill = "black",
                                                       outline = "#000000",
                                                       width = 4,
                                                       start = 20,
                                                       extent = 70)
    data.qRightDiagonalToBottomCoord = (data.toprightx - data.x,
                                   data.bottomrighty - data.y,
                                   data.toprightx + data.x,
                                   data.bottomrighty)
    data.questionrightdiagonaltobottom = canvas.create_arc(data.qRightDiagonalToBottomCoord,
                                                           style = "arc",
                                                           fill = "black",
                                                           outline = "#000000",
                                                           width = 4,
                                                           start = 270,
                                                           extent = 70)
    data.qRightToDiagonalTopCoord = (data.toprightx + 72 - data.x1,
                                     round((data.toplefty + data.bottomlefty)/2) - data.y1,
                                     data.toprightx + 72 + data.x1,
                                     round((data.toplefty + data.bottomlefty)/2))
    data.questionrighttodiagonaltop = canvas.create_arc(data.qRightToDiagonalTopCoord,
                                                        style = "arc",
                                                        fill = "black",
                                                        outline = "#000000",
                                                        width = 4,
                                                        start = 200,
                                                        extent = 70) #anomalous
    data.qRightToDiagonalBottomCoord = (data.toprightx + 72 - data.x1,
                                        round((data.toplefty + data.bottomlefty)/2),
                                        data.toprightx + 72 + data.x1,
                                        round((data.toplefty + data.bottomlefty)/2) + data.y1)
    data.questionrighttodiagonalbottom = canvas.create_arc(data.qRightToDiagonalBottomCoord,
                                                           style = "arc",
                                                           fill = "black",
                                                           outline = "#000000",
                                                           width = 4,
                                                           start = 90,
                                                           extent = 70)
    data.questionRightCoord = (data.toprightx + 65,
                              round((data.toplefty + data.bottomlefty)/2),
                              1500,
                              round((data.toplefty + data.bottomlefty)/2))
    data.questionright = canvas.create_line(data.questionRightCoord,
                                            fill = "#000000", width = 4)

    #####Question and Answer Labels 
    data.questioncontent1 = ""
    data.questionlabel1 = canvas.create_text((topleftx + toprightx)/2,
                                              round((toplefty + bottomlefty)/2) - data.shiftUpHeight,
                                              text = data.questioncontent1,
                                              font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")
    data.winningsLabel = canvas.create_text((topleftx + toprightx)/2,
                                              round((toplefty + bottomlefty)/2) - data.shiftUpHeight,
                                              text = "",
                                              font = ("Interstate", 72),
                                              fill = "#000000")


    #reverse the order in which the lines are executed so that
    #the p's, q's, and ,g's of the upper line extend down into
    #the empty space of the bottom line
    data.questioncontent2b = ""
    data.questionlabel2b = canvas.create_text((topleftx + toprightx)/2,
                                              round((toplefty + bottomlefty)/2) + 22,
                                              text = data.questioncontent2b,
                                              font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")
    data.questioncontent2a = ""
    data.questionlabel2a = canvas.create_text((topleftx + toprightx)/2,
                                              round((toplefty + bottomlefty)/2) - 22,
                                              text = data.questioncontent2a,
                                              font = ("Conduit ITC Medium", 32),
                                              fill = "#000000")

def drawLifelines(canvas, data):
    ###lifeline icons
    data.lifelineX1 = 100
    data.lifelineY1 = 100
    data.lifelineX2 = data.lifelineX1 + 70
    data.lifelineY2 = data.lifelineY1 + 54
    data.lifelineXMid = (data.lifelineX1 + data.lifelineX2) / 2
    data.lifelineYMid = (data.lifelineY1 + data.lifelineY2) / 2
    captionOffset = 45
    if data.usedFiftyFifty == False:
        data.fiftyFiftyOvalX = (data.lifelineX1 + data.lifelineX2) / 2
        data.lifelineY = (data.lifelineY1 + data.lifelineY2) / 2
        data.fiftyFiftyOval = canvas.create_oval(data.lifelineX1, data.lifelineY1,
                                                 data.lifelineX2, data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.fiftyFiftyLabel = canvas.create_text(data.lifelineXMid, data.lifelineYMid,
                                                  fill = "black", text = "50:50",
                                                  font = ("Arial", 16))
        data.fiftyFiftyTop = canvas.create_text(data.lifelineXMid,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "black", text = "Fifty-Fifty",
                                                  font = ("Conduit ITC Medium", 14))
        data.fiftyFiftyBottom = canvas.create_text(data.lifelineXMid,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "black", text = "[5]",
                                                  font = ("Conduit ITC Medium", 14))
    lifelineSpace = 100
    if data.usedDoubleDip == False:
        data.doubleDipOval = canvas.create_oval(data.lifelineX1 + lifelineSpace * 1,
                                                 data.lifelineY1,
                                                 data.lifelineX2 + lifelineSpace * 1,
                                                 data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.doubleDipOvalX = data.lifelineXMid + lifelineSpace * 1
        data.doubleDipLabel = canvas.create_text(data.doubleDipOvalX,
                                                  data.lifelineYMid,
                                                  fill = "black", text = "x2",
                                                  font = ("Arial Bold", 20))
        data.doubleDipTop = canvas.create_text(data.lifelineXMid + lifelineSpace * 1,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "black", text = "Double Dip",
                                                  font = ("Conduit ITC Medium", 14))
        data.doubleDipBottom = canvas.create_text(data.lifelineXMid + lifelineSpace * 1,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "black", text = "[2]",
                                                  font = ("Conduit ITC Medium", 14))
    additionalOffset = 20
    if data.usedSwitchQuestion == False:
        data.switchOval = canvas.create_oval(data.lifelineX1 + lifelineSpace * 2,
                                                 data.lifelineY1,
                                                 data.lifelineX2 + lifelineSpace * 2,
                                                 data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.switchOvalX = data.lifelineXMid + lifelineSpace * 2
        data.switchLabel = canvas.create_text(data.switchOvalX,
                                              data.lifelineYMid,
                                              fill = "black", text = "S",
                                              font = ("Arial Bold Italic", 28))
        data.switchTop1 = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "black", text = "Question",
                                                  font = ("Conduit ITC Medium", 14))
        data.switchTop2 = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                             data.lifelineYMid - captionOffset - additionalOffset * 1,
                                             fill = "black", text = "the",
                                             font = ("Conduit ITC Medium", 14))
        data.switchTop3 = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                             data.lifelineYMid - captionOffset - additionalOffset * 2,
                                             fill = "black", text = "Switch",
                                             font = ("Conduit ITC Medium", 14))
        data.switchBottom = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "black", text = "[S]",
                                                  font = ("Conduit ITC Medium", 14))
    if data.usedInfiniteTime == False:
        data.infiniteOval = canvas.create_oval(data.lifelineX1 + lifelineSpace * 3,
                                                 data.lifelineY1,
                                                 data.lifelineX2 + lifelineSpace * 3,
                                                 data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.infiniteOvalX = data.lifelineXMid + lifelineSpace * 3
        data.infiniteLabel = canvas.create_text(data.infiniteOvalX,
                                                data.lifelineYMid - 3,
                                                fill = "black", text = "∞",
                                                font = ("Conduit ITC Medium", 36))
        data.infiniteTop1 = canvas.create_text(data.lifelineXMid + lifelineSpace * 3,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "black", text = "Time",
                                                  font = ("Conduit ITC Medium", 14))
        data.infiniteTop2 = canvas.create_text(data.lifelineXMid + lifelineSpace * 3,
                                              data.lifelineYMid - captionOffset - additionalOffset,
                                              fill = "black", text = "Infinite",
                                              font = ("Conduit ITC Medium", 14))
        data.infiniteBottom = canvas.create_text(data.lifelineXMid + lifelineSpace * 3,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "black", text = "[I]",
                                                  font = ("Conduit ITC Medium", 14))
    if data.lifelinesRemaining > 0:
        data.lifelineBottom = canvas.create_text(data.lifelineXMid - lifelineSpace/2,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "black", text = "Key:",
                                                  font = ("Conduit ITC Medium", 14))
    #Game information about winnings
    winningsVerticalStart = 75
    data.questionValueLabel = canvas.create_text(data.width - 2 * lifelineSpace - 150,
                                              winningsVerticalStart + captionOffset * 0,
                                              fill = "black", anchor = "w",
                                              text = "Question Value: " + data.winAmountsLabel[data.currentQuestion],
                                              font = ("Conduit ITC Medium", 20))
    data.wonAmount = canvas.create_text(data.width - 2 * lifelineSpace - 204,
                                              winningsVerticalStart + captionOffset * 1,
                                              fill = "black", anchor = "w",
                                              text = "Current amount won: " + data.winAmountsLabel [data.currentQuestion - 1],
                                              font = ("Conduit ITC Medium", 20))
    data.guaranteedAmount = canvas.create_text(data.width - 2 * lifelineSpace - 248,
                                              winningsVerticalStart + captionOffset * 2,
                                              fill = "black", anchor = "w",
                                              text = "Guaranteed amount won: " + data.guaranteedAmounts[data.currentQuestion],
                                              font = ("Conduit ITC Medium", 20))
    #fade in lifelines and game winnings statistics
    startTime = clock()
    animationDurationTotal = 0.5
    while (clock() - startTime) < 0.5:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRedOval = floor(69 * proportion)
        targetGreenOval = floor(96 * proportion)
        targetBlueOval = floor(137 * proportion)
        currentFillOval = hexcolor(targetRedOval,
                                   targetGreenOval,
                                   targetBlueOval)
        targetRGBWhite = floor(255 * proportion)
        currentWhiteFill = hexcolor(targetRGBWhite,
                                    targetRGBWhite,
                                    targetRGBWhite)
        canvas.itemconfig(data.fiftyFiftyOval, outline = currentFillOval)
        canvas.itemconfig(data.fiftyFiftyLabel, fill = currentWhiteFill)
        canvas.itemconfig(data.fiftyFiftyTop, fill = currentWhiteFill)
        canvas.itemconfig(data.fiftyFiftyBottom, fill = currentWhiteFill)
        canvas.itemconfig(data.doubleDipOval, outline = currentFillOval)
        canvas.itemconfig(data.doubleDipLabel, fill = currentWhiteFill)
        canvas.itemconfig(data.doubleDipTop, fill = currentWhiteFill)
        canvas.itemconfig(data.doubleDipBottom, fill = currentWhiteFill)
        canvas.itemconfig(data.switchOval, outline = currentFillOval)
        canvas.itemconfig(data.switchLabel, fill = currentWhiteFill)
        canvas.itemconfig(data.switchTop1, fill = currentWhiteFill)
        canvas.itemconfig(data.switchTop2, fill = currentWhiteFill)
        canvas.itemconfig(data.switchTop3, fill = currentWhiteFill)
        canvas.itemconfig(data.switchBottom, fill = currentWhiteFill)
        canvas.itemconfig(data.infiniteOval, outline = currentFillOval)
        canvas.itemconfig(data.infiniteLabel, fill = currentWhiteFill)
        canvas.itemconfig(data.infiniteTop1, fill = currentWhiteFill)
        canvas.itemconfig(data.infiniteTop2, fill = currentWhiteFill)
        canvas.itemconfig(data.infiniteBottom, fill = currentWhiteFill)
        canvas.itemconfig(data.lifelineBottom, fill = currentWhiteFill)
        canvas.itemconfig(data.wonAmount, fill = currentWhiteFill)
        canvas.itemconfig(data.guaranteedAmount, fill = currentWhiteFill)
        canvas.update()
    #fix the final values
    targetRedOval = 69
    targetGreenOval = 96
    targetBlueOval = 137
    currentFillOval = hexcolor(targetRedOval,
                               targetGreenOval,
                               targetBlueOval)
    currentWhiteFill = hexcolor(255, 255, 255)
    canvas.itemconfig(data.fiftyFiftyOval, outline = currentFillOval)
    canvas.itemconfig(data.fiftyFiftyLabel, fill = currentWhiteFill)
    canvas.itemconfig(data.fiftyFiftyTop, fill = currentWhiteFill)
    canvas.itemconfig(data.fiftyFiftyBottom, fill = currentWhiteFill)
    canvas.itemconfig(data.doubleDipOval, outline = currentFillOval)
    canvas.itemconfig(data.doubleDipLabel, fill = currentWhiteFill)
    canvas.itemconfig(data.doubleDipTop, fill = currentWhiteFill)
    canvas.itemconfig(data.doubleDipBottom, fill = currentWhiteFill)
    canvas.itemconfig(data.switchOval, outline = currentFillOval)
    canvas.itemconfig(data.switchLabel, fill = currentWhiteFill)
    canvas.itemconfig(data.switchTop1, fill = currentWhiteFill)
    canvas.itemconfig(data.switchTop2, fill = currentWhiteFill)
    canvas.itemconfig(data.switchTop3, fill = currentWhiteFill)
    canvas.itemconfig(data.switchBottom, fill = currentWhiteFill)
    canvas.itemconfig(data.infiniteOval, outline = currentFillOval)
    canvas.itemconfig(data.infiniteLabel, fill = currentWhiteFill)
    canvas.itemconfig(data.infiniteTop1, fill = currentWhiteFill)
    canvas.itemconfig(data.infiniteTop2, fill = currentWhiteFill)
    canvas.itemconfig(data.infiniteBottom, fill = currentWhiteFill)
    canvas.itemconfig(data.lifelineBottom, fill = currentWhiteFill)
    canvas.itemconfig(data.wonAmount, fill = currentWhiteFill)
    canvas.itemconfig(data.guaranteedAmount, fill = currentWhiteFill)
    canvas.update()

def drawLifelinesWithoutAnimation(canvas, data):
    ###lifeline icons
    data.lifelineX1 = 100
    data.lifelineY1 = 100
    data.lifelineX2 = data.lifelineX1 + 70
    data.lifelineY2 = data.lifelineY1 + 54
    data.lifelineXMid = (data.lifelineX1 + data.lifelineX2) / 2
    data.lifelineYMid = (data.lifelineY1 + data.lifelineY2) / 2
    captionOffset = 45
    if data.usedFiftyFifty == False:
        data.fiftyFiftyOvalX = (data.lifelineX1 + data.lifelineX2) / 2
        data.lifelineY = (data.lifelineY1 + data.lifelineY2) / 2
        data.fiftyFiftyOval = canvas.create_oval(data.lifelineX1, data.lifelineY1,
                                                 data.lifelineX2, data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.fiftyFiftyLabel = canvas.create_text(data.lifelineXMid, data.lifelineYMid,
                                                  fill = "white", text = "50:50",
                                                  font = ("Arial", 16))
        data.fiftyFiftyTop = canvas.create_text(data.lifelineXMid,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "white", text = "Fifty-Fifty",
                                                  font = ("Conduit ITC Medium", 14))
        data.fiftyFiftyBottom = canvas.create_text(data.lifelineXMid,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "white", text = "[5]",
                                                  font = ("Conduit ITC Medium", 14))
    lifelineSpace = 100
    if data.usedDoubleDip == False:
        data.doubleDipOval = canvas.create_oval(data.lifelineX1 + lifelineSpace * 1,
                                                 data.lifelineY1,
                                                 data.lifelineX2 + lifelineSpace * 1,
                                                 data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.doubleDipOvalX = data.lifelineXMid + lifelineSpace * 1
        data.doubleDipLabel = canvas.create_text(data.doubleDipOvalX,
                                                  data.lifelineYMid,
                                                  fill = "white", text = "x2",
                                                  font = ("Arial Bold", 20))
        data.doubleDipTop = canvas.create_text(data.lifelineXMid + lifelineSpace * 1,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "white", text = "Double Dip",
                                                  font = ("Conduit ITC Medium", 14))
        data.doubleDipBottom = canvas.create_text(data.lifelineXMid + lifelineSpace * 1,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "white", text = "[2]",
                                                  font = ("Conduit ITC Medium", 14))
    additionalOffset = 20
    if data.usedSwitchQuestion == False:
        data.switchOval = canvas.create_oval(data.lifelineX1 + lifelineSpace * 2,
                                                 data.lifelineY1,
                                                 data.lifelineX2 + lifelineSpace * 2,
                                                 data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.switchOvalX = data.lifelineXMid + lifelineSpace * 2
        data.switchLabel = canvas.create_text(data.switchOvalX,
                                              data.lifelineYMid,
                                              fill = "white", text = "S",
                                              font = ("Arial Bold Italic", 28))
        data.switchTop1 = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "white", text = "Question",
                                                  font = ("Conduit ITC Medium", 14))
        data.switchTop2 = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                             data.lifelineYMid - captionOffset - additionalOffset * 1,
                                             fill = "white", text = "the",
                                             font = ("Conduit ITC Medium", 14))
        data.switchTop3 = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                             data.lifelineYMid - captionOffset - additionalOffset * 2,
                                             fill = "white", text = "Switch",
                                             font = ("Conduit ITC Medium", 14))
        data.switchBottom = canvas.create_text(data.lifelineXMid + lifelineSpace * 2,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "white", text = "[S]",
                                                  font = ("Conduit ITC Medium", 14))
    if data.usedInfiniteTime == False:
        data.infiniteOval = canvas.create_oval(data.lifelineX1 + lifelineSpace * 3,
                                                 data.lifelineY1,
                                                 data.lifelineX2 + lifelineSpace * 3,
                                                 data.lifelineY2,
                                                 fill = "black",
                                                 outline = "#456089", width = 4)
        data.infiniteOvalX = data.lifelineXMid + lifelineSpace * 3
        data.infiniteLabel = canvas.create_text(data.infiniteOvalX,
                                                data.lifelineYMid - 3,
                                                fill = "white", text = "∞",
                                                font = ("Conduit ITC Medium", 36))
        data.infiniteTop1 = canvas.create_text(data.lifelineXMid + lifelineSpace * 3,
                                                  data.lifelineYMid - captionOffset,
                                                  fill = "white", text = "Time",
                                                  font = ("Conduit ITC Medium", 14))
        data.infiniteTop2 = canvas.create_text(data.lifelineXMid + lifelineSpace * 3,
                                              data.lifelineYMid - captionOffset - additionalOffset,
                                              fill = "white", text = "Infinite",
                                              font = ("Conduit ITC Medium", 14))
        data.infiniteBottom = canvas.create_text(data.lifelineXMid + lifelineSpace * 3,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "white", text = "[I]",
                                                  font = ("Conduit ITC Medium", 14))
    if data.lifelinesRemaining > 0:
        data.lifelineBottom = canvas.create_text(data.lifelineXMid - lifelineSpace/2,
                                                  data.lifelineYMid + captionOffset,
                                                  fill = "white", text = "Key:",
                                                  font = ("Conduit ITC Medium", 14))
    #Game information about winnings
    winningsVerticalStart = 75
    data.questionValueLabel = canvas.create_text(data.width - 2 * lifelineSpace - 150,
                                              winningsVerticalStart + captionOffset * 0,
                                              fill = "white", anchor = "w",
                                              text = "Question Value: " + data.winAmountsLabel[data.currentQuestion],
                                              font = ("Conduit ITC Medium", 20))
    data.wonAmount = canvas.create_text(data.width - 2 * lifelineSpace - 204,
                                              winningsVerticalStart + captionOffset * 1,
                                              fill = "white", anchor = "w",
                                              text = "Current amount won: " + data.winAmountsLabel [data.currentQuestion - 1],
                                              font = ("Conduit ITC Medium", 20))
    data.guaranteedAmount = canvas.create_text(data.width - 2 * lifelineSpace - 248,
                                              winningsVerticalStart + captionOffset * 2,
                                              fill = "white", anchor = "w",
                                              text = "Guaranteed amount won: " + data.guaranteedAmounts[data.currentQuestion],
                                              font = ("Conduit ITC Medium", 20))

def drawMenu(canvas, data):
    drawQuestions(canvas, data)
    startTime = clock() #start ticking cue
    while (clock() - startTime) < 0.5:
        canvas.itemconfig(data.questiontopleft1, fill = "black")
        canvas.update()
    canvas.delete(data.questionleftdiagonattotop)
    canvas.delete(data.questionleftdiagonaltobottom)
    canvas.delete(data.questionlefttodiagonaltop)
    canvas.delete(data.questionlefttodiagonalbottom)
    canvas.delete(data.questionrightdiaonaltotop)
    canvas.delete(data.questionrightdiagonaltobottom)
    canvas.delete(data.questiontopleft)
    canvas.delete(data.questiontopright)
    canvas.delete(data.questiontop)
    canvas.delete(data.questionbottomleft)
    canvas.delete(data.questionbottomright)
    canvas.delete(data.questionrighttodiagonaltop)
    canvas.itemconfig(data.answerA, text = "Play")
    canvas.itemconfig(data.answerB, text = "Instructions")
    canvas.update()
    startTime = clock() #start ticking cue
    animationDurationTotal = 0.75 #seconds
    animationPartialDuration = 0.75 #each bar reveal takes this many seconds
    while (clock() - startTime) < animationDurationTotal:
        if (clock() - startTime) < animationPartialDuration:
            #reveal top answer bars
            proportionTop = (clock() - startTime) / animationPartialDuration
            currentRed, currentGreen, currentBlue = 0, 0, 0
            targetRedTop = 105
            targetGreenTop = 140
            targetBlueTop = 193
            targetRedFirst = currentRed + floor(targetRedTop * proportionTop)
            targetGreenFirst = currentGreen + floor(targetGreenTop * proportionTop)
            targetBlueFirst = currentBlue + floor(targetBlueTop * proportionTop)
            currentFillTop = hexcolor(targetRedFirst,
                                   targetGreenFirst,
                                   targetBlueFirst)
            #top left
            canvas.itemconfig(data.questiontopleft1, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomleft1, fill = currentFillTop)
            canvas.itemconfig(data.questiontop1, fill = currentFillTop)
            canvas.itemconfig(data.questionbottom1, fill = currentFillTop)
            canvas.itemconfig(data.questionleft1, fill = currentFillTop)
            canvas.itemconfig(data.questiontopright1, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomright1, fill = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonattotop1, outline = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonaltobottom1, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonaltop1, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonalbottom1, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiaonaltotop1, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiagonaltobottom1, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonaltop1, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonalbottom1, outline = currentFillTop)
            #top right
            canvas.itemconfig(data.questiontopleft2, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomleft2, fill = currentFillTop)
            canvas.itemconfig(data.questiontop2, fill = currentFillTop)
            canvas.itemconfig(data.questionbottom2, fill = currentFillTop)
            canvas.itemconfig(data.questiontopright2, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomright2, fill = currentFillTop)
            canvas.itemconfig(data.questionright2, fill = currentFillTop)
            canvas.itemconfig(data.middletop, fill = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonattotop2, outline = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonaltobottom2, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonaltop2, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonalbottom2, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiaonaltotop2, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiagonaltobottom2, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonaltop2, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonalbottom2, outline = currentFillTop)
            targetRGB = floor(proportionTop * 255)
            currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
            canvas.itemconfig(data.answerA, fill = currentFill)
            canvas.itemconfig(data.answerB, fill = currentFill)
            canvas.update()
    data.title = canvas.create_text(data.width//2, data.height//4,
                               text = "WHO WANTS TO BE A MILLIONAIRE",
                               font = ("Copperplate Gothic Bold", 32),
                               fill = "black")
    data.byline = canvas.create_text(data.width//2, data.height - 10,
                               text = "Winston Zhou",
                               font = ("Conduit ITC Medium", 16),
                               fill = "black")
    startTime = clock() 
    animationDurationTotal = 1 #seconds
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.title, fill = currentFill)
        canvas.itemconfig(data.byline, fill = currentFill)
        canvas.update()

def drawInstructionsPage(canvas, data, instructions):
    if instructions: #user clicked on Instructions button
        selectB(canvas, data, True)
    else: #user clicked on Play button
        selectA(canvas, data, True)
    startTime = clock() 
    animationDurationTotal = 1 #seconds
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        currentRed, currentGreen, currentBlue = 105, 140, 193
        targetRedFirst = floor(currentRed - currentRed * proportion)
        targetGreenFirst = floor(currentGreen - currentGreen * proportion)
        targetBlueFirst = floor(currentBlue - currentBlue * proportion)
        currentFillTop = hexcolor(targetRedFirst,
                               targetGreenFirst,
                               targetBlueFirst)
        #top left
        canvas.itemconfig(data.questiontopleft1, fill = currentFillTop)
        canvas.itemconfig(data.questionbottomleft1, fill = currentFillTop)
        canvas.itemconfig(data.questiontop1, fill = currentFillTop)
        canvas.itemconfig(data.questionbottom1, fill = currentFillTop)
        canvas.itemconfig(data.questionleft1, fill = currentFillTop)
        canvas.itemconfig(data.questiontopright1, fill = currentFillTop)
        canvas.itemconfig(data.questionbottomright1, fill = currentFillTop)
        canvas.itemconfig(data.questionleftdiagonattotop1, outline = currentFillTop)
        canvas.itemconfig(data.questionleftdiagonaltobottom1, outline = currentFillTop)
        canvas.itemconfig(data.questionlefttodiagonaltop1, outline = currentFillTop)
        canvas.itemconfig(data.questionlefttodiagonalbottom1, outline = currentFillTop)
        canvas.itemconfig(data.questionrightdiaonaltotop1, outline = currentFillTop)
        canvas.itemconfig(data.questionrightdiagonaltobottom1, outline = currentFillTop)
        canvas.itemconfig(data.questionrighttodiagonaltop1, outline = currentFillTop)
        canvas.itemconfig(data.questionrighttodiagonalbottom1, outline = currentFillTop)
        #top right
        canvas.itemconfig(data.questiontopleft2, fill = currentFillTop)
        canvas.itemconfig(data.questionbottomleft2, fill = currentFillTop)
        canvas.itemconfig(data.questiontop2, fill = currentFillTop)
        canvas.itemconfig(data.questionbottom2, fill = currentFillTop)
        canvas.itemconfig(data.questiontopright2, fill = currentFillTop)
        canvas.itemconfig(data.questionbottomright2, fill = currentFillTop)
        canvas.itemconfig(data.questionright2, fill = currentFillTop)
        canvas.itemconfig(data.middletop, fill = currentFillTop)
        canvas.itemconfig(data.questionleftdiagonattotop2, outline = currentFillTop)
        canvas.itemconfig(data.questionleftdiagonaltobottom2, outline = currentFillTop)
        canvas.itemconfig(data.questionlefttodiagonaltop2, outline = currentFillTop)
        canvas.itemconfig(data.questionlefttodiagonalbottom2, outline = currentFillTop)
        canvas.itemconfig(data.questionrightdiaonaltotop2, outline = currentFillTop)
        canvas.itemconfig(data.questionrightdiagonaltobottom2, outline = currentFillTop)
        canvas.itemconfig(data.questionrighttodiagonaltop2, outline = currentFillTop)
        canvas.itemconfig(data.questionrighttodiagonalbottom2, outline = currentFillTop)

        targetRGB = floor(255 - 255 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.byline,
                          fill = currentFill)
        canvas.itemconfig(data.title,
                          fill = currentFill)
        canvas.itemconfig(data.answerB,
                          fill = currentFill)
        canvas.itemconfig(data.answerA,
                          fill = currentFill)
        targetRedGreenDown = floor(6 - 6 * proportion)
        targetGreenGreenDown = floor(169 - 169 * proportion)
        targetBlueGreenDown = 0
        greenDownFill = hexcolor(targetRedGreenDown,
                                 targetGreenGreenDown,
                                 targetBlueGreenDown)
        if instructions:
            canvas.itemconfig(data.q2background, fill = greenDownFill)
        else:
            canvas.itemconfig(data.q1background, fill = greenDownFill)
        canvas.update()
    if instructions == False: return None
    p1 = '''"Who Wants to Be a Millionaire?" is a multiple-choice style trivia game. The game consists of answering questions each of
which has four possible answer choices. Only one answer choice is correct in each problem. There is a time limit for each question.
    '''
    p2 = '''Questions 1-5: 15 seconds;
Questions 6-10: 30 seconds;
Questions 11-14: 45 seconds; Question 15: 45 seconds + banked time (unused time from previous questions)
    '''
    p3 = '''You have four lifelines which you can use throughout the game. Available lifelines will be shown in the upper-left of the window.'''

    p3a = '''    
Computer removes two incorrect answers. May not be used in conjunction with Double Dip.'''
    p3b = '''
Up to two chances to select the correct answer. Once activated, no further lifelines may be
activated on the current question.'''
    p3c = '''
Computer switches the current question out for another one of equal value.
May not be used on Question 15.'''
    p3d = '''
Infinite time to answer the current question. Once activated, Switch the Question and/or
50:50 may not be activated on the  current question.'''


                       

    p4 = '''Once the fifth question is correctly answered, you are guaranteed to walk away with at least $1,000. After the tenth question
is answered, that figure increases to $32,000. Winnings statistics will be on the upper-right of the window.
'''

    p5 = '''Questions get progressively more difficult. Some questions are dynamically generated.
Instructions will be shown at the bottom of each screen in case one gets lost.
    '''

    p6 = "Press [P] to play"

    data.paragraph1 = canvas.create_text(100, 100, text = p1, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")

    data.paragraph2 = canvas.create_text(100, 190, text = p2, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")

    data.paragraph3 = canvas.create_text(100, 250, text = p3, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3a = canvas.create_text(380, 292, text = p3a, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3alabel = canvas.create_text(180, 307, text = "50:50:", fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3blabel = canvas.create_text(180, 368, text = "Double Dip:",
                                    fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3b = canvas.create_text(380, 358, text = p3b, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3c = canvas.create_text(380, 418, text = p3c, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3clabel = canvas.create_text(180, 430, text = "Switch the Question:", fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3d = canvas.create_text(380, 480, text = p3d, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph3dlabel = canvas.create_text(180, 493, text = "Infinite Time:", fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph4 = canvas.create_text(100, 580, text = p4, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")

    data.paragraph5 = canvas.create_text(100, 650, text = p5, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.paragraph6 = canvas.create_text(100, 720, text = p6, fill = "black",
                                    font = ("Conduit ITC Medium", 18),
                                    anchor = "w")
    data.lifelineX1Instr = 100
    data.lifelineY1Instr = 280
    data.lifelineX2Instr = data.lifelineX1Instr + 70
    data.lifelineY2Instr = data.lifelineY1Instr + 54
    data.lifelineXMidInstr = (data.lifelineX1Instr + data.lifelineX2Instr) / 2
    data.lifelineYMidInstr = (data.lifelineY1Instr + data.lifelineY2Instr) / 2
    ovalMul = 62
    data.fiftyFiftyOvalInstr = canvas.create_oval(data.lifelineX1Instr, data.lifelineY1Instr,
                                                 data.lifelineX2Instr, data.lifelineY2Instr,
                                                 fill = "black",
                                                 outline = "black", width = 4)
    data.ddOvalInstr = canvas.create_oval(data.lifelineX1Instr,
                                          data.lifelineY1Instr + ovalMul * 1,
                                          data.lifelineX2Instr,
                                          data.lifelineY2Instr + ovalMul * 1,
                                          fill = "black",
                                          outline = "black",
                                          width = 4)
    data.switchOvalInstr = canvas.create_oval(data.lifelineX1Instr,
                                          data.lifelineY1Instr + ovalMul * 2,
                                          data.lifelineX2Instr,
                                          data.lifelineY2Instr + ovalMul * 2,
                                          fill = "black",
                                          outline = "black",
                                          width = 4)
    data.infiniteOvalInstr = canvas.create_oval(data.lifelineX1Instr,
                                          data.lifelineY1Instr + ovalMul * 3,
                                          data.lifelineX2Instr,
                                          data.lifelineY2Instr + ovalMul * 3,
                                          fill = "black",
                                          outline = "black",
                                          width = 4)
    data.fiftyFiftyLabelInstr = canvas.create_text(data.lifelineXMidInstr, data.lifelineYMidInstr,
                                              fill = "black", text = "50:50",
                                              font = ("Arial", 16))
    data.doubleDipLabelInstr = canvas.create_text(data.lifelineXMidInstr,
                                             data.lifelineYMidInstr + ovalMul * 1,
                                             fill = "black", text = "x2",
                                             font = ("Arial Bold", 20))
    data.switchLabelInstr = canvas.create_text(data.lifelineXMidInstr,
                                               data.lifelineYMidInstr + ovalMul * 2,
                                               fill = "black", text = "S",
                                               font = ("Arial Bold Italic", 28))
    data.infiniteLabel = canvas.create_text(data.lifelineXMidInstr,
                                            data.lifelineYMidInstr + 183,
                                            #hardcoded 180 so that it's centered
                                            fill = "black", text = "∞",
                                            font = ("Conduit ITC Medium", 36))
    startTime = clock() 
    animationDurationTotal = 0.75 #seconds
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph1,
                          fill = currentFill)
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph2,
                          fill = currentFill)
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph3,
                          fill = currentFill)
        canvas.update() 
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        targetRedOval = floor(69 * proportion)
        targetGreenOval = floor(96 * proportion)
        targetBlueOval = floor(137 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph3a,
                          fill = currentFill)
        canvas.itemconfig(data.paragraph3alabel,
                          fill = currentFill)
        canvas.itemconfig(data.fiftyFiftyLabelInstr,
                          fill = currentFill)
        canvas.itemconfig(data.fiftyFiftyOvalInstr,
                          outline = hexcolor(targetRedOval,
                                             targetGreenOval,
                                             targetBlueOval))
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        targetRedOval = floor(69 * proportion)
        targetGreenOval = floor(96 * proportion)
        targetBlueOval = floor(137 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph3b,
                          fill = currentFill)
        canvas.itemconfig(data.paragraph3blabel,
                          fill = currentFill)
        canvas.itemconfig(data.doubleDipLabelInstr,
                          fill = currentFill)
        canvas.itemconfig(data.ddOvalInstr,
                          outline = hexcolor(targetRedOval,
                                             targetGreenOval,
                                             targetBlueOval))
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        targetRedOval = floor(69 * proportion)
        targetGreenOval = floor(96 * proportion)
        targetBlueOval = floor(137 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph3c,
                          fill = currentFill)
        canvas.itemconfig(data.paragraph3clabel,
                          fill = currentFill)
        canvas.itemconfig(data.switchLabelInstr,
                          fill = currentFill)
        canvas.itemconfig(data.switchOvalInstr,
                          outline = hexcolor(targetRedOval,
                                             targetGreenOval,
                                             targetBlueOval))
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        targetRedOval = floor(69 * proportion)
        targetGreenOval = floor(96 * proportion)
        targetBlueOval = floor(137 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph3d,
                          fill = currentFill)
        canvas.itemconfig(data.paragraph3dlabel,
                          fill = currentFill)
        canvas.itemconfig(data.infiniteLabel,
                          fill = currentFill)
        canvas.itemconfig(data.infiniteOvalInstr,
                          outline = hexcolor(targetRedOval,
                                             targetGreenOval,
                                             targetBlueOval))
        canvas.update()   
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph4,
                          fill = currentFill)
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(proportion * 255)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph5,
                          fill = currentFill)
        canvas.update()
    startTime = clock()
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRed = floor(proportion * 207)
        targetGreen = floor(proportion * 122)
        targetBlue = floor(proportion * 12)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.paragraph6,
                          fill = currentFill)
        canvas.update()

def instructionPlay(canvas, data):
    startTime = clock() 
    animationDurationTotal = 0.75 #seconds
    while (clock() - startTime) < animationDurationTotal:
        proportion = (clock() - startTime) / animationDurationTotal
        targetRGB = floor(255 - 255 * proportion)
        targetRedOval = floor(69 - 69 * proportion)
        targetGreenOval = floor(96 - 96 * proportion)
        targetBlueOval = floor(137 - 137 * proportion)
        targetRGBOvals = hexcolor(targetRedOval, targetGreenOval, targetBlueOval)
        currentFillBlack = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.paragraph1, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph2, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph4, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph5, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3a, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3alabel, fill = currentFillBlack)
        canvas.itemconfig(data.fiftyFiftyLabelInstr, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3b, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3blabel, fill = currentFillBlack)
        canvas.itemconfig(data.doubleDipLabelInstr, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3c, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3clabel, fill = currentFillBlack)
        canvas.itemconfig(data.switchLabelInstr, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3d, fill = currentFillBlack)
        canvas.itemconfig(data.paragraph3dlabel, fill = currentFillBlack)
        canvas.itemconfig(data.infiniteLabel, fill = currentFillBlack)
        canvas.itemconfig(data.fiftyFiftyOvalInstr, outline = targetRGBOvals)
        canvas.itemconfig(data.ddOvalInstr, outline = targetRGBOvals)
        canvas.itemconfig(data.switchOvalInstr, outline = targetRGBOvals)
        canvas.itemconfig(data.infiniteOvalInstr, outline = targetRGBOvals)
        targetRed = floor(207 - 207 * proportion)
        targetGreen = floor(122 - 122 * proportion)
        targetBlue = floor(12 - 12 * proportion)
        currentFillOrange = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.paragraph6, fill = currentFillOrange)
        canvas.update()

def createCircleObjects(canvas, data):
    for i in range(15):
        data.rxtop=790+20*i #90 above center/2
        data.ytop = 575 
        data.rxbottom=805+20*i #15 greater than rxtop
        data.ybottom=data.ytop + 15 #15 greater than ytop
        data.circlesRight.append(canvas.create_oval(data.rxtop,data.ytop,data.rxbottom
            ,data.ybottom, outline="black",fill="#000000")) #create right circles
        data.lxtop=595-20*i 
        data.lxbottom=610-20*i #15 greater than lxtop, 90 less than center/2
        data.circlesLeft.append(canvas.create_oval(data.lxtop,data.ytop,data.lxbottom
            ,data.ybottom, outline="black",fill="#000000")) #create left circles
    data.drawArc = False

#entirely my own
def activatecircle(canvas, data): #initial animation of circles upon clock reveal
    for i in range(data.activateCircleIterations):
        for cirnum in range(15):
            if data.colors[cirnum][3] == 0: #black to active
                if ((data.colors[cirnum][0]==208) and (data.colors[cirnum][1]==255) and (data.colors[cirnum][2]==255)):
                    data.colors[cirnum][3] = 1 #switch to active to inert algorithm
                if data.colors[cirnum][0] < 205: #active target red
                    data.colors[cirnum][0] += 16
                if data.colors[cirnum][1] < 251: #active target green
                    data.colors[cirnum][1] += 15
                if data.colors[cirnum][2] < 251: #active target blue
                    data.colors[cirnum][2] += 15
                if ((data.colors[cirnum][0] > 0) and (data.colors[cirnum][1] > 0) and (data.colors[cirnum][2] > 0)):
                    canvas.itemconfig(data.circlesLeft[cirnum],fill = hexcolor(data.colors[cirnum][0],
                        data.colors[cirnum][1],data.colors[cirnum][2]))
                    canvas.itemconfig(data.circlesRight[cirnum],fill = hexcolor(data.colors[cirnum][0],
                        data.colors[cirnum][1],data.colors[cirnum][2]))
            else: #active to inert algorithm 
                if data.currentQuestion < 14: #non-million dollar question inert
                    if data.colors[cirnum][0] > 77: #inert target red
                        data.colors[cirnum][0] -= 2
                    if data.colors[cirnum][1] > 92: #inert target green
                        data.colors[cirnum][1] -= 2
                    if data.colors[cirnum][2] > 219: #inert target blue
                        data.colors[cirnum][2] -= 1
                else: #million dollar question inert golden
                    if data.colors[cirnum][0] > 166: #inert target red
                        data.colors[cirnum][0] -= 2
                    if data.colors[cirnum][1] > 150: #inert target green
                        data.colors[cirnum][1] -= 2
                    if data.colors[cirnum][2] > 82: #inert target blue
                        data.colors[cirnum][2] -= 2

                canvas.itemconfig(data.circlesLeft[cirnum],fill = hexcolor(data.colors[cirnum][0],
                        data.colors[cirnum][1],data.colors[cirnum][2]))
                canvas.itemconfig(data.circlesRight[cirnum],fill = hexcolor(data.colors[cirnum][0],
                        data.colors[cirnum][1],data.colors[cirnum][2]))
        canvas.update()
        canvas.after(25)
    if data.currentQuestion in [0, 5, 10]:
        if data.justUsedSwitch == False:
            instructions(canvas, data, False, "delay")
            canvas.update()
        else: #next time, will display above line
            data.justUsedSwitch = True
    return None

def createclockpieslices(canvas, data): #initializes the shapes for the clock
    data.oval1 = canvas.create_arc(data.xtop1,data.ytop1,data.xbottom1,data.ybottom1, style = "pieslice",fill="#375f86",outline="#375f86",
     width = 1, start = 269, extent = 359) #outermost pieslice
    data.oval2red = canvas.create_arc(data.xtop2,data.ytop2,data.xbottom2,data.ybottom2, style = "pieslice",fill="#c35575",outline="#11304f",
     width = 1, start = 269, extent = 359) #middle pieslice deeper segment
    data.oval2 = canvas.create_arc(data.xtop2,data.ytop2,data.xbottom2,data.ybottom2, style = "pieslice",fill="#f0f0f9",outline="#11304f",
     width = 1, start = 269, extent = 359) #middle pieslice shallower segment
    data.oval2out = canvas.create_arc(data.xtop2,data.ytop2,data.xbottom2,data.ybottom2, style = "pieslice",fill="#f0f0f9",outline="#f0f0f9",
     width = 1, start = 268, extent = 1) #middle pieslice last degree segment (concealer)
    data.oval3 = canvas.create_arc(data.xtop3,data.ytop3,data.xbottom3,data.ybottom3, style = "pieslice",fill="#122c8a",outline="#000945",
     width = 1, start = 269, extent = 359) #innermost pieslice
    data.oval3out = canvas.create_arc(data.xtop3,data.ytop3,data.xbottom3,data.ybottom3, style = "pieslice",fill="#122c8a",outline="#122c8a",
     width = 1, start = 268, extent = 1) #innermost pieslice last degree segment (concealer)


def createGoldenClockSlices(canvas, data):
    data.oval1 = canvas.create_arc(data.xtop1,data.ytop1,data.xbottom1,data.ybottom1, style = "pieslice",fill="#a89566",outline="#a89566",
     width = 1, start = 269, extent = 359) #outermost pieslice
    data.oval2red = canvas.create_arc(data.xtop2,data.ytop2,data.xbottom2,data.ybottom2, style = "pieslice",fill="#ab694b",outline="#dfce8e",
     width = 1, start = 269, extent = 359) #middle pieslice deeper segment
    data.oval2 = canvas.create_arc(data.xtop2,data.ytop2,data.xbottom2,data.ybottom2, style = "pieslice",fill="#dfce8e",outline="#dfce8e",
     width = 1, start = 269, extent = 359) #middle pieslice shallower segment
    data.oval2out = canvas.create_arc(data.xtop2,data.ytop2,data.xbottom2,data.ybottom2, style = "pieslice",fill="#dfce8e",outline="#dfce8e",
     width = 1, start = 268, extent = 1) #middle pieslice last degree segment (concealer)
    data.oval3 = canvas.create_arc(data.xtop3,data.ytop3,data.xbottom3,data.ybottom3, style = "pieslice",fill="#8a7124",outline="#8a7124",
     width = 1, start = 269, extent = 359) #innermost pieslice
    data.oval3out = canvas.create_arc(data.xtop3,data.ytop3,data.xbottom3,data.ybottom3, style = "pieslice",fill="#8a7124",outline="#8a7124",
     width = 1, start = 268, extent = 1) #innermost pieslice last degree segment (concealer)
    if data.usedSwitchQuestion == False:
        canvas.itemconfig(data.switchOval, outline = "#2c2b2b")
        canvas.itemconfig(data.switchLabel, fill = "#2c2b2b")
        canvas.itemconfig(data.switchTop1, fill = "#2c2b2b")
        canvas.itemconfig(data.switchTop2, fill = "#2c2b2b")
        canvas.itemconfig(data.switchTop3, fill = "#2c2b2b")
        canvas.itemconfig(data.switchBottom, fill = "#2c2b2b")
    instructions(canvas, data, False, "Mill Clock Appear")

def clockAppearSigmoid(x):
    return x**(1/3)

def clockappear(canvas, data): #animation of clock popping out and question bar revealing
    data.channel1.play(data.revealClockSound)
    drawQuestions(canvas, data)
    createCircleObjects(canvas, data)
    if data.currentQuestion < 14:
        createclockpieslices(canvas, data)
    else:
        createGoldenClockSlices(canvas, data)
    startTime = clock() #start ticking cue
    animationDuration = data.popoutDuration #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        canvas.coords(data.oval1,data.xtop1 - 99 * clockAppearSigmoid(proportion),
                      data.ytop1 - 99 * clockAppearSigmoid(proportion),
                      data.xbottom1 + 99 * clockAppearSigmoid(proportion),
                      data.ybottom1 + 99 * clockAppearSigmoid(proportion)) #actual changes here
        canvas.coords(data.oval2,data.xtop2 - 82 * clockAppearSigmoid(proportion),
                      data.ytop2 - 82 * clockAppearSigmoid(proportion),
                      data.xbottom2+ 82 * clockAppearSigmoid(proportion),
                      data.ybottom2 + 82 * clockAppearSigmoid(proportion))
        canvas.coords(data.oval2red,data.xtop2 - 82 * clockAppearSigmoid(proportion),
                      data.ytop2 - 82 * clockAppearSigmoid(proportion),
                      data.xbottom2 + 82 * clockAppearSigmoid(proportion),
                      data.ybottom2 + 82 * clockAppearSigmoid(proportion))
        canvas.coords(data.oval2out,data.xtop2 - 82 * clockAppearSigmoid(proportion),
                      data.ytop2 - 82 * clockAppearSigmoid(proportion),
                      data.xbottom2 + 82 * clockAppearSigmoid(proportion),
                      data.ybottom2 + 82 * clockAppearSigmoid(proportion))
        canvas.coords(data.oval3,data.xtop3 - 65 * clockAppearSigmoid(proportion),
                      data.ytop3 - 65 * clockAppearSigmoid(proportion),
                      data.xbottom3 + 65 * clockAppearSigmoid(proportion),
                      data.ybottom3 + 65 * clockAppearSigmoid(proportion))
        canvas.coords(data.oval3out,data.xtop3 - 65 * clockAppearSigmoid(proportion),
                      data.ytop3 - 65 * clockAppearSigmoid(proportion),
                      data.xbottom3 + 65 * clockAppearSigmoid(proportion),
                      data.ybottom3 + 65 * clockAppearSigmoid(proportion))
        if (clock() - startTime) > data.popoutDuration * 0.60:
            if data.questionBarSwitch == True:
                startTime2 = clock() #secondary proportion for nested animation
                data.questionBarSwitch = False
            animationDuration2 = data.popoutDuration * 0.40
            proportion2 = (clock() - startTime2) / animationDuration2
            targetRed = 105
            targetGreen = 140
            targetBlue = 193
            currentFill = hexcolor(floor(targetRed * proportion2),
                                   floor(targetGreen * proportion2),
                                   floor(targetBlue * proportion2))
            canvas.itemconfig(data.questiontop, fill = currentFill)
            canvas.itemconfig(data.questiontopleft, fill = currentFill)
            canvas.itemconfig(data.questionbottomleft, fill = currentFill)
            canvas.itemconfig(data.questionleftdiagonattotop, outline = currentFill)
            canvas.itemconfig(data.questionleftdiagonaltobottom, outline = currentFill)
            canvas.itemconfig(data.questionlefttodiagonaltop, outline = currentFill)
            canvas.itemconfig(data.questionlefttodiagonalbottom, outline = currentFill)
            canvas.itemconfig(data.questionbottom, fill = currentFill)
            canvas.itemconfig(data.questionleft, fill = currentFill)
            canvas.itemconfig(data.questiontopright, fill = currentFill)
            canvas.itemconfig(data.questionbottomright, fill = currentFill)
            canvas.itemconfig(data.questionrightdiaonaltotop, outline = currentFill)
            canvas.itemconfig(data.questionrightdiagonaltobottom, outline = currentFill)
            canvas.itemconfig(data.questionrighttodiagonaltop, outline = currentFill)
            canvas.itemconfig(data.questionrighttodiagonalbottom, outline = currentFill)
            canvas.itemconfig(data.questionright, fill = currentFill)
        canvas.update()
    timeinerttoactive(canvas, data)
    if data.currentQuestion < 14:
        activatecircle(canvas, data)

def createtimelabel(canvas, data):
    if data.currentQuestion < 14:
        data.timelabel = canvas.create_text(700,600, text = data.timerSeconds,
            font = ("DIN-Black", data.clockFontSize), fill = "#122c8a")
        #Current 18  44  138 
        #Target   236 222 177
        data.red1 = 18  #inert
        data.green1 = 44
        data.blue1 = 138
    else: #million dollar question variant
        data.clockFontSize = 36
        data.timelabel = canvas.create_text(700,600, text = "0:45",
            font = ("DIN-Black", data.clockFontSize), fill = "#122c8a")
        #Current 18  44  138 
        #Target   236 222 177
        data.red1 = 18  #inert
        data.green1 = 44
        data.blue1 = 138

def timeinerttoactive(canvas, data): #fade in time
    createtimelabel(canvas, data)
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        if data.currentQuestion < 14:        
            data.red1 = 18 + floor(217 * proportion)
            data.green1 = 44 + floor(188 * proportion)
            data.blue1 = 138 + floor(39 * proportion)
        else:
            data.red1 = 138 + floor(97 * proportion)
            data.green1 = 113 + floor(119 * proportion)
            data.blue1 = 36 + floor(141 * proportion)
        canvas.itemconfig(data.timelabel,
                          fill = hexcolor(data.red1, data.green1, data.blue1))
        canvas.update()
    if data.currentQuestion == 14:
        activatecircle(canvas, data)
        data.channel2.play(data.bankedTimeMusic)
        instructions(canvas, data, False, "Mill flash")
        bankedTime(canvas, data)

def bankedTime(canvas, data):
    data.timeLeft = 45 + data.bankedTime
    data.timerSeconds = 45 + data.bankedTime
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRedOval2 = floor(223 + 32 * proportion)
        targetGreenOval2 = floor(206 + 49 * proportion)
        targetBlueOval2 = floor(142 + 113 * proportion)
        targetRedOval3 = floor(138 + 117 * proportion)
        targetGreenOval3 = floor(113 + 142 * proportion)
        targetBlueOval3 = floor(36 + 219 * proportion)
        targetRedText = floor(235 + 20 * proportion)
        targetGreenText = floor(232 + 23 * proportion)
        targetBlueText = floor(177 + 78 * proportion)
        fillOval2 = hexcolor(targetRedOval2, targetGreenOval2, targetBlueOval2)
        fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
        fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
        canvas.itemconfig(data.oval2, fill = fillOval2)
        canvas.itemconfig(data.oval2, outline = fillOval2)
        canvas.itemconfig(data.oval2out, fill = fillOval2)
        canvas.itemconfig(data.oval2out, outline = fillOval2)
        canvas.itemconfig(data.oval3, fill = fillOval3)
        canvas.itemconfig(data.oval3, outline = fillOval3)
        canvas.itemconfig(data.oval3out, fill = fillOval3)
        canvas.itemconfig(data.oval3out, outline = fillOval3)
        canvas.itemconfig(data.timelabel, fill = fillText)
        canvas.update()
    canvas.itemconfig(data.timelabel, text = prettytime(normaltime(data.bankedTime)))
    canvas.itemconfig(data.timelabel, font = ("DIN-Black", data.clockFontSize))
    data.bankedLabel1 = canvas.create_text(700, 635, text = "BANKED",
                                          font = ("Conduit ITC Medium", 16),
                                          fill = "white")
    data.bankedLabel2 = canvas.create_text(700, 655, text = "TIME",
                                          font = ("Conduit ITC Medium", 16),
                                          fill = "white")    
    startTime = clock() #start ticking cue
    animationDuration = 0.5 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRedOval2 = floor(255 - 32 * proportion)
        targetGreenOval2 = floor(255 - 40 * proportion)
        targetBlueOval2 = floor(255 - 105 * proportion)
        targetRedOval3 = floor(255 - 237 * proportion)
        targetGreenOval3 = floor(255 - 211 * proportion)
        targetBlueOval3 = floor(255 - 117 * proportion)
        targetRedText = floor(255 - 20 * proportion)
        targetGreenText = floor(255 - 23 * proportion)
        targetBlueText = floor(255 - 78 * proportion)
        fillOval2 = hexcolor(targetRedOval2, targetGreenOval2, targetBlueOval2)
        fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
        fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
        canvas.itemconfig(data.oval2, fill = fillOval2)
        canvas.itemconfig(data.oval2, outline = fillOval2)
        canvas.itemconfig(data.oval2out, fill = fillOval2)
        canvas.itemconfig(data.oval2out, outline = fillOval2)
        canvas.itemconfig(data.oval3, fill = fillOval3)
        canvas.itemconfig(data.oval3, outline = fillOval3)
        canvas.itemconfig(data.oval3out, fill = fillOval3)
        canvas.itemconfig(data.oval3out, outline = fillOval3)
        canvas.itemconfig(data.timelabel, fill = fillText)
        canvas.update()

def updateCoord(data):
    #updating dot coordinates
    data.ybottom = data.ytop + 15
    #updating clock coordinates
    data.xbottom1 = data.xtop1
    data.ybottom1 = data.ytop1
    data.xtop2 = data.xtop1
    data.ytop2 = data.ytop1
    data.xbottom2 = data.xtop1
    data.ybottom2 = data.ytop1
    data.xtop3 = data.xtop1
    data.ytop3 = data.ytop1
    data.xbottom3 = data.xtop1
    data.ybottom3 = data.ytop1
    data.timeTextX = data.xtop1
    #updating question coordinates
    data.toprighty = data.toplefty
    data.bottomlefty = data.toplefty + 115
    data.bottomrighty = data.toprighty + 115
    data.questionTopCoord = (data.topleftx,
                            data.toplefty,
                            data.toprightx,
                            data.toprighty)
    data.questionTopLeftCoord = (data.topleftx - 50, 
                                 data.toplefty + 51,
                                 data.topleftx - 10,
                                 data.toplefty + 4)
    data.questionBottomLeftCoord = (data.bottomleftx - 50,
                                    data.bottomlefty - 50,
                                    data.bottomleftx - 10,
                                    data.bottomlefty - 4)
    data.qLeftDiagonalToTopCoord = (data.topleftx - data.x,
                                    data.toplefty,
                                    data.topleftx + data.x,
                                    data.toplefty + data.y)
    data.qLeftDiagonalToBottomCoord = (data.topleftx - data.x,
                                       data.bottomlefty - data.y,
                                       data.topleftx + data.x,
                                       data.bottomlefty)
    data.qLeftToDiagonalTopCoord = ((data.topleftx - 60) - data.x1,
                                    round((data.toplefty + data.bottomlefty)/2) - data.y1,
                                    (data.topleftx - 70) + data.x1,
                                    round((data.toplefty + data.bottomlefty)/2))
    data.qLeftToDiagonalBottomCoord = ((data.topleftx - 60) - data.x1,
                                       round((data.toplefty + data.bottomlefty)/2),
                                       (data.topleftx - 70) + data.x1,
                                       round((data.toplefty + data.bottomlefty)/2) + data.y1)
    data.questionBottomCoord = (data.bottomleftx,
                                data.bottomlefty,
                                data.bottomrightx,
                                data.bottomrighty)
    data.questionLeftCoord = (0,
                              round((data.toplefty + data.bottomlefty)/2),
                              data.topleftx - 65,
                              round((data.toplefty + data.bottomlefty)/2))
    data.questionTopRightCoord = (data.toprightx + 50,
                                  data.toprighty + 51,
                                  data.toprightx + 10,
                                  data.toprighty + 4)
    data.questionBottomRightCoord = (data.bottomrightx + 50,
                                    data.bottomrighty - 50,
                                    data.bottomrightx + 10,
                                    data.bottomrighty - 4)
    data.qRightDiagonalToTopCoord = (data.toprightx - data.x,
                                    data.toprighty,
                                    data.toprightx + data.x,
                                    data.toprighty + data.y,)
    data.qRightDiagonalToBottomCoord = (data.toprightx - data.x,
                                   data.bottomrighty - data.y,
                                   data.toprightx + data.x,
                                   data.bottomrighty)
    data.qRightToDiagonalTopCoord = (data.toprightx + 72 - data.x1,
                                     round((data.toplefty + data.bottomlefty)/2) - data.y1,
                                     data.toprightx + 72 + data.x1,
                                     round((data.toplefty + data.bottomlefty)/2))
    data.qRightToDiagonalBottomCoord = (data.toprightx + 72 - data.x1,
                                        round((data.toplefty + data.bottomlefty)/2),
                                        data.toprightx + 72 + data.x1,
                                        round((data.toplefty + data.bottomlefty)/2) + data.y1)
    data.questionRightCoord = (data.toprightx + 65,
                              round((data.toplefty + data.bottomlefty)/2),
                              1500,
                              round((data.toplefty + data.bottomlefty)/2))

def digitcount(n): #counts number of digits in number n
    if n < 0: n *= -1
    elif n == 0 : return 1
    count = 0
    while n > 0:
        n //= 10
        count += 1
    return count

def secondstime(binarytime): #converts to seconds
    if (digitcount(binarytime) < 3): #under 60 seconds
        return binarytime
    elif (digitcount(binarytime) < 5): #under 60 minutes
        secondsdigits = binarytime % 100 #seconds count
        minutesdigits = binarytime // 100 #minutes count
        return minutesdigits * 60 + secondsdigits
    else: #over 60 minutes
        secondsdigits = binarytime % 100
        hourdigit = binarytime // 10000 #hours count
        minutesdigits = (binarytime - hourdigit * 10000) // 100
        return hourdigit * 3600 + minutesdigits * 60 + secondsdigits

def normaltime(sec): #converts to regular looking time
    hours = sec // 3600
    minutes = sec // 60 - hours * 60
    seconds = sec - hours * 3600 - minutes * 60
    return seconds + minutes * 100 + hours * 10000

def prettytime(uglytime): #puts colons in the time
    if (digitcount(uglytime) < 3): #under 60 seconds
        if uglytime < 10: #case with leading seconds' 0
            return "0:0" + str(uglytime)
        else: #no leading zeros required in seconds place
            return "0:" + str(uglytime)
    elif (digitcount(uglytime) < 5): #under 60 minutes
        if uglytime % 100 < 10: #case with leading seconds' 0
            return str(uglytime // 100)+":0"+str(uglytime % 100)
        else: #no leading zeros required in seconds place
            return str(uglytime // 100)+":"+str(uglytime % 100)
    else: #over an hour
        if (uglytime // 100 - uglytime // 10000 * 100) < 10: #case with leading minutes' 0
            if uglytime % 100 < 10: #case with leading seconds' 0
                return str(uglytime//10000)+":0"+str(uglytime // 100 - uglytime//10000 * 100)+":0"+str(uglytime % 100)
            else: #no leading zeros required in seconds place
                return str(uglytime//10000)+":0"+str(uglytime // 100 - uglytime//10000 * 100)+":"+str(uglytime % 100)
        else: #case without leading minutes' 0
            if uglytime % 100 < 10: #case with leading seconds' 0
                return str(uglytime//10000)+":"+str(uglytime // 100 - uglytime//10000 * 100)+":0"+str(uglytime % 100)
            else: #no leading zeros required in seconds place
                return str(uglytime//10000)+":"+str(uglytime // 100 - uglytime//10000 * 100)+":"+str(uglytime % 100)

def shiftUp(canvas, data):
    if data.currentQuestion == 14: #million dollar question flash from banked time to yellow clock
        startTime = clock() #start ticking cue
        animationDuration = 0.25 #seconds
        while (clock() - startTime) < animationDuration: #banked time to white
            proportion = (clock() - startTime) / animationDuration
            targetRedOval2 = floor(223 + 32 * proportion)
            targetGreenOval2 = floor(215 + 40 * proportion)
            targetBlueOval2 = floor(150 + 105 * proportion)
            targetRedOval3 = floor(18 + 237 * proportion)
            targetGreenOval3 = floor(44 + 211 * proportion)
            targetBlueOval3 = floor(138 + 117 * proportion)
            targetRedText = floor(235 + 20 * proportion)
            targetGreenText = floor(232 + 23 * proportion)
            targetBlueText = floor(177 + 78 * proportion)
            fillOval2 = hexcolor(targetRedOval2, targetGreenOval2, targetBlueOval2)
            fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
            fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
            canvas.itemconfig(data.oval2, fill = fillOval2)
            canvas.itemconfig(data.oval2, outline = fillOval2)
            canvas.itemconfig(data.oval2out, fill = fillOval2)
            canvas.itemconfig(data.oval2out, outline = fillOval2)
            canvas.itemconfig(data.oval3, fill = fillOval3)
            canvas.itemconfig(data.oval3, outline = fillOval3)
            canvas.itemconfig(data.oval3out, fill = fillOval3)
            canvas.itemconfig(data.oval3out, outline = fillOval3)
            canvas.itemconfig(data.timelabel, fill = fillText)
            canvas.update()
        canvas.delete(data.bankedLabel1) #delete banked time labels
        canvas.delete(data.bankedLabel2) 
        canvas.itemconfig(data.timelabel, text = "0:45")
        startTime = clock() #start ticking cue
        animationDuration = 0.25 #seconds
        data.channel1.play(data.finalQuestionReveal)
        while (clock() - startTime) < animationDuration: #white to 0:45 gold clock
            proportion = (clock() - startTime) / animationDuration
            targetRedOval2 = floor(255 - 32 * proportion)
            targetGreenOval2 = floor(255 - 49 * proportion)
            targetBlueOval2 = floor(255 - 113 * proportion)
            targetRedOval3 = floor(255 - 117 * proportion)
            targetGreenOval3 = floor(255 - 142 * proportion)
            targetBlueOval3 = floor(255 - 219 * proportion)
            targetRedText = floor(255 - 20 * proportion)
            targetGreenText = floor(255 - 23 * proportion)
            targetBlueText = floor(255 - 78 * proportion)
            fillOval2 = hexcolor(targetRedOval2, targetGreenOval2, targetBlueOval2)
            fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
            fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
            canvas.itemconfig(data.oval2, fill = fillOval2)
            canvas.itemconfig(data.oval2, outline = fillOval2)
            canvas.itemconfig(data.oval2out, fill = fillOval2)
            canvas.itemconfig(data.oval2out, outline = fillOval2)
            canvas.itemconfig(data.oval3, fill = fillOval3)
            canvas.itemconfig(data.oval3, outline = fillOval3)
            canvas.itemconfig(data.oval3out, fill = fillOval3)
            canvas.itemconfig(data.oval3out, outline = fillOval3)
            canvas.itemconfig(data.timelabel, fill = fillText)
            canvas.update()  
    if data.currentQuestion < 14:
        data.channel1.play(data.revealQuestionSound)
    if data.currentQuestion < 5:
        data.channel0.play(data.questions100to1000Bed)
    canvas.delete(data.oval2out) #no longer need concealers
    canvas.delete(data.oval3out)
    startTime = clock() #start ticking cue
    animationDuration = 1 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        if data.currentQuestion == 14:
            timeSweep = prettytime(normaltime(45 + floor(data.bankedTime * proportion)))
            canvas.itemconfig(data.timelabel, text = timeSweep)
        data.toplefty = 600 - data.shiftUpHeight * proportion
        data.ytop = 575 - data.shiftUpHeight * proportion
        updateCoord(data) #updates all the coordinates for movement
        #moving up question bar
        canvas.coords(data.questiontop, data.questionTopCoord)
        canvas.coords(data.questiontopleft, data.questionTopLeftCoord)
        canvas.coords(data.questionbottomleft, data.questionBottomLeftCoord)
        canvas.coords(data.questionleftdiagonattotop, data.qLeftDiagonalToTopCoord)
        canvas.coords(data.questionleftdiagonaltobottom, data.qLeftDiagonalToBottomCoord)
        canvas.coords(data.questionlefttodiagonaltop, data.qLeftToDiagonalTopCoord)
        canvas.coords(data.questionlefttodiagonalbottom, data.qLeftToDiagonalBottomCoord)
        canvas.coords(data.questionbottom, data.questionBottomCoord)
        canvas.coords(data.questionleft, data.questionLeftCoord)
        canvas.coords(data.questiontopright, data.questionTopRightCoord)
        canvas.coords(data.questionbottomright, data.questionBottomRightCoord)
        canvas.coords(data.questionrightdiaonaltotop, data.qRightDiagonalToTopCoord)
        canvas.coords(data.questionrightdiagonaltobottom, data.qRightDiagonalToBottomCoord)
        canvas.coords(data.questionrighttodiagonaltop, data.qRightToDiagonalTopCoord)
        canvas.coords(data.questionrighttodiagonalbottom, data.qRightToDiagonalBottomCoord)
        canvas.coords(data.questionright, data.questionRightCoord)
            
        #moving up clock while simultaneously decreasing its diameter
        data.ytop1 = 600 - 155 * proportion
        canvas.coords(data.oval1,data.xtop1 - 99 + 15 * proportion,
                      data.ytop1 - 99+ 15 * proportion,
                      data.xbottom1 + 99- 15 * proportion,
                      data.ybottom1 + 99- 15 * proportion) #actual changes here
        canvas.coords(data.oval2,data.xtop2 - 82+ 15 * proportion,
                      data.ytop2 - 82 + 15 * proportion,
                      data.xbottom2+ 82 - 15 * proportion,
                      data.ybottom2 + 82- 15 * proportion)
        canvas.coords(data.oval2red,data.xtop2 - 82 + 15 * proportion,
                      data.ytop2 - 82+ 15 * proportion,
                      data.xbottom2 + 82 - 15 * proportion,
                      data.ybottom2 + 82- 15 * proportion)
        canvas.coords(data.oval2out,data.xtop2 - 82+ 15 * proportion,
                      data.ytop2 - 82+ 15 * proportion,
                      data.xbottom2 + 82- 15 * proportion,
                      data.ybottom2 + 82- 15 * proportion)
        canvas.coords(data.oval3,data.xtop3 - 65+ 15 * proportion,
                      data.ytop3 - 65+ 15 * proportion,
                      data.xbottom3 + 65- 15 * proportion,
                      data.ybottom3 + 65- 15 * proportion)
        canvas.coords(data.oval3out,data.xtop3 - 65+ 15 * proportion,
                      data.ytop3 - 65+ 15 * proportion,
                      data.xbottom3 + 65- 15 * proportion,
                      data.ybottom3 + 65- 15 * proportion)
        data.startvalue = 269 + 91 * proportion
        data.extentvalue = 359 - 179 * proportion
        canvas.itemconfig(data.oval1, start = data.startvalue)
        canvas.itemconfig(data.oval1, extent = data.extentvalue)
        canvas.itemconfig(data.oval2red, start = data.startvalue)
        canvas.itemconfig(data.oval2red, extent = data.extentvalue)
        canvas.itemconfig(data.oval2, start = data.startvalue)
        canvas.itemconfig(data.oval2, extent = data.extentvalue)
        canvas.itemconfig(data.oval3, start = data.startvalue)
        canvas.itemconfig(data.oval3, extent = data.extentvalue) 

        #moving up dots
        for cirnum in range(15):
            data.rxtop=790+20*cirnum 
            data.rxbottom=805+20*cirnum 
            data.ybottom=data.ytop + 15 
            data.lxtop=595-20*cirnum
            data.lxbottom=610-20*cirnum
            canvas.coords(data.circlesRight[cirnum],
                                       data.rxtop, data.ytop,
                                       data.rxbottom, data.ybottom)
            canvas.coords(data.circlesLeft[cirnum],
                                       data.lxtop, data.ytop,
                                       data.lxbottom, data.ybottom)
        #shrinking time label size and shifting it up
        data.timeTextY = 600 - (173 * proportion) #173 because 155 + 18
        #where the extra 18 pixels is so that the time label is not centered in
        #the semicircle; it should be slightly above center
        canvas.itemconfig(data.timelabel,
                                  font=("DIN-Black",data.clockFontSize))
        canvas.coords(data.timelabel,data.timeTextX,data.timeTextY)
        if data.currentQuestion < 14:
            data.clockFontSize = 48 - floor(19 * proportion)
        else: #million dollar question font size different
            data.clockFontSize = 36 - floor(7 * proportion)
        canvas.update()
    #make the circle perfectly semicircular
    data.startvalue = 269 + 91 
    data.extentvalue = 359 - 179 
    canvas.itemconfig(data.oval1, start = data.startvalue)
    canvas.itemconfig(data.oval1, extent = data.extentvalue)
    canvas.itemconfig(data.oval2red, start = data.startvalue)
    canvas.itemconfig(data.oval2red, extent = data.extentvalue)
    canvas.itemconfig(data.oval2, start = data.startvalue)
    canvas.itemconfig(data.oval2, extent = data.extentvalue)
    canvas.itemconfig(data.oval3, start = data.startvalue)
    canvas.itemconfig(data.oval3, extent = data.extentvalue)
    canvas.update()
    if data.currentQuestion == 14:
        timeSweep = prettytime(normaltime(45 + floor(data.bankedTime)))
        canvas.itemconfig(data.timelabel, text = timeSweep)
        canvas.update()
    revealQuestion(canvas, data)

def revealQuestion(canvas, data):
    # assign question
    difficulty = difficultySelector(data.currentQuestion)
    if data.currentQuestion == 14:
        data.questionLine1or2 = 2
        data.currentQuestionAttributes = dynamicSequenceQuestion()
    else:
        if data.dynamicGeneration == True:
            testGenerate = randrange(10) 
            if testGenerate < 3: 
                data.dynamicGeneration = False
                if data.cylinderGiven == False:
                    testGenerate = randrange(10) 
                    if testGenerate < 5: 
                        data.cylinderGiven = True
                        data.currentQuestionAttributes = dynamicCylinderVolume(data, difficulty)
                    else:
                        data.currentQuestionAttributes = dynamicArithmeticQuestion(data, difficulty)
                else:
                    data.currentQuestionAttributes = dynamicArithmeticQuestion(data, difficulty)
            else: selectQuestion(data, data.currentQuestion)
        else:
            selectQuestion(data, data.currentQuestion)
    if data.questionLine1or2 == 1:
        data.questioncontent1 = data.currentQuestionAttributes[0]
        canvas.itemconfig(data.questionlabel1, text = data.questioncontent1)
    elif data.questionLine1or2 == 2:    
        data.questioncontent2b = data.currentQuestionAttributes[1]
        data.questioncontent2a = data.currentQuestionAttributes[0]
        canvas.itemconfig(data.questionlabel2b, text = data.questioncontent2b)
        canvas.itemconfig(data.questionlabel2a, text = data.questioncontent2a)
    # revelation animation
    startTime = clock() #start ticking cue
    animationDuration = 0.5 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        red, green, blue = 255 * proportion, 255 * proportion, 255 * proportion
        currentFill = hexcolor(floor(red), floor(green), floor(blue))
        canvas.itemconfig(data.questionlabel1, fill = currentFill)
        canvas.itemconfig(data.questionlabel2b, fill = currentFill)
        canvas.itemconfig(data.questionlabel2a, fill = currentFill)
        canvas.itemconfig(data.questionValueLabel, fill = currentFill)
        canvas.coords(data.questionlabel2b,(data.topleftx + data.toprightx)/2,
                      round((data.toplefty + data.bottomlefty)/2) + 22)
        canvas.coords(data.questionlabel2a,(data.topleftx + data.toprightx)/2,
                      round((data.toplefty + data.bottomlefty)/2) - 22)
        canvas.update()
    revealAnswerBars(canvas, data, False)

def revealAnswerBars(canvas, data, reverseReveal):
    startTime = clock() #start ticking cue
    animationDurationTotal = 0.75 #seconds
    animationPartialDuration = 0.5 #each bar reveal takes this many seconds
    animationBottomStart = 0.25 #delay to reveal bottom answer bars
    bottomStartTimeSwitch = True #False once bottom animation starts
    while (clock() - startTime) < animationDurationTotal:
        if (clock() - startTime) < animationPartialDuration:
            #reveal top answer bars
            proportionTop = (clock() - startTime) / animationPartialDuration
            if reverseReveal == False: #means to do a reveal animation
                currentRed, currentGreen, currentBlue = 0, 0, 0
                targetRedTop = 105
                targetGreenTop = 140
                targetBlueTop = 193
            else: #means to do a fade out animation
                currentRed, currentGreen, currentBlue = 105, 140, 193
                targetRedTop = -105
                targetGreenTop = -140
                targetBlueTop = -193
                if data.currentQuestion < 14: #regular winnings label
                    targetRedWinings = floor(199 * proportionTop)
                    targetGreenWinings = floor(211 * proportionTop)
                    targetBlueWinings = floor(247 * proportionTop)
                else: #golden millionaire label if correctly answered
                    if data.gameOver == False:
                        if data.lifelinesMillionRemoveSwitch == False:
                            data.lifelinesMillionRemoveSwitch = True
                            if data.lifelinesRemaining > 0:
                                canvas.delete(data.lifelineBottom)
                            if data.usedSwitchQuestion == False:
                                canvas.delete(data.switchOval)
                                canvas.delete(data.switchTop1)
                                canvas.delete(data.switchTop2)
                                canvas.delete(data.switchTop3)
                                canvas.delete(data.switchBottom)
                                canvas.delete(data.switchLabel)
                            if data.usedInfiniteTime == False:
                                canvas.delete(data.infiniteOval)
                                canvas.delete(data.infiniteTop1)
                                canvas.delete(data.infiniteTop2)
                                canvas.delete(data.infiniteBottom)
                                canvas.delete(data.infiniteLabel)
                            if data.usedDoubleDip == False:
                                canvas.delete(data.doubleDipOval)
                                canvas.delete(data.doubleDipTop)
                                canvas.delete(data.doubleDipBottom)
                                canvas.delete(data.doubleDipLabel)
                            if data.usedFiftyFifty == False:
                                canvas.delete(data.fiftyFiftyOval)
                                canvas.delete(data.fiftyFiftyLabel)
                                canvas.delete(data.fiftyFiftyTop)
                                canvas.delete(data.fiftyFiftyBottom)
                        #turn question bar golden
                        targetRedQuestionBar = floor(105 + 117 * proportionTop)
                        targetGreenQuestionBar = floor(140 + 72 * proportionTop)
                        targetBlueQuestionBar = floor(193 - 37 * proportionTop)
                        questionBarFillGolden = hexcolor(targetRedQuestionBar,
                                                         targetGreenQuestionBar,
                                                         targetBlueQuestionBar)
                        canvas.itemconfig(data.questiontop, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questiontopleft, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questionbottomleft, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questionleftdiagonattotop, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionleftdiagonaltobottom, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionlefttodiagonaltop, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionlefttodiagonalbottom, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionbottom, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questionleft, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questiontopright, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questionbottomright, fill = questionBarFillGolden)
                        canvas.itemconfig(data.questionrightdiaonaltotop, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionrightdiagonaltobottom, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionrighttodiagonaltop, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionrighttodiagonalbottom, outline = questionBarFillGolden)
                        canvas.itemconfig(data.questionright, fill = questionBarFillGolden)
                        targetRedWinings = floor(224 * proportionTop)
                        targetGreenWinings = floor(221 * proportionTop)
                        targetBlueWinings = floor(138 * proportionTop)  
                    else: #lost on the million dollar questoin
                        targetRedWinings = floor(199 * proportionTop)
                        targetGreenWinings = floor(211 * proportionTop)
                        targetBlueWinings = floor(247 * proportionTop)             
                winningFill = hexcolor(targetRedWinings,
                                       targetGreenWinings,
                                       targetBlueWinings)
                canvas.itemconfig(data.winningsLabel, fill = winningFill)
            targetRedFirst = currentRed + floor(targetRedTop * proportionTop)
            targetGreenFirst = currentGreen + floor(targetGreenTop * proportionTop)
            targetBlueFirst = currentBlue + floor(targetBlueTop * proportionTop)
            currentFillTop = hexcolor(targetRedFirst,
                                   targetGreenFirst,
                                   targetBlueFirst)
            #top left
            canvas.itemconfig(data.questiontopleft1, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomleft1, fill = currentFillTop)
            canvas.itemconfig(data.questiontop1, fill = currentFillTop)
            canvas.itemconfig(data.questionbottom1, fill = currentFillTop)
            canvas.itemconfig(data.questionleft1, fill = currentFillTop)
            canvas.itemconfig(data.questiontopright1, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomright1, fill = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonattotop1, outline = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonaltobottom1, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonaltop1, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonalbottom1, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiaonaltotop1, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiagonaltobottom1, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonaltop1, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonalbottom1, outline = currentFillTop)
            #top right
            canvas.itemconfig(data.questiontopleft2, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomleft2, fill = currentFillTop)
            canvas.itemconfig(data.questiontop2, fill = currentFillTop)
            canvas.itemconfig(data.questionbottom2, fill = currentFillTop)
            canvas.itemconfig(data.questiontopright2, fill = currentFillTop)
            canvas.itemconfig(data.questionbottomright2, fill = currentFillTop)
            canvas.itemconfig(data.questionright2, fill = currentFillTop)
            canvas.itemconfig(data.middletop, fill = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonattotop2, outline = currentFillTop)
            canvas.itemconfig(data.questionleftdiagonaltobottom2, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonaltop2, outline = currentFillTop)
            canvas.itemconfig(data.questionlefttodiagonalbottom2, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiaonaltotop2, outline = currentFillTop)
            canvas.itemconfig(data.questionrightdiagonaltobottom2, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonaltop2, outline = currentFillTop)
            canvas.itemconfig(data.questionrighttodiagonalbottom2, outline = currentFillTop)

        if ((clock() - startTime) > animationBottomStart and
            (clock() - startTime) < animationDurationTotal):
            # reveal bottom answer slots
            if bottomStartTimeSwitch == True:
                startTimeBottom = clock()
                bottomStartTimeSwitch = False
            proportionBottom = (clock() - startTimeBottom) / animationPartialDuration
            targetRedSecond = currentRed + floor(targetRedTop * proportionBottom)
            targetGreenSecond = currentGreen + floor(targetGreenTop * proportionBottom)
            targetBlueSecond = currentBlue + floor(targetBlueTop * proportionBottom)
            currentFillBottom = hexcolor(targetRedSecond,
                                   targetGreenSecond,
                                   targetBlueSecond)
            #bottom left
            canvas.itemconfig(data.questiontopleft3, fill = currentFillBottom)
            canvas.itemconfig(data.questionbottomleft3, fill = currentFillBottom)
            canvas.itemconfig(data.questiontop3, fill = currentFillBottom)
            canvas.itemconfig(data.questionbottom3, fill = currentFillBottom)
            canvas.itemconfig(data.questionleft3, fill = currentFillBottom)
            canvas.itemconfig(data.questiontopright3, fill = currentFillBottom)
            canvas.itemconfig(data.questionbottomright3, fill = currentFillBottom)
            canvas.itemconfig(data.questionleftdiagonattotop3, outline = currentFillBottom)
            canvas.itemconfig(data.questionleftdiagonaltobottom3, outline = currentFillBottom)
            canvas.itemconfig(data.questionlefttodiagonaltop3, outline = currentFillBottom)
            canvas.itemconfig(data.questionlefttodiagonalbottom3, outline = currentFillBottom)
            canvas.itemconfig(data.questionrightdiaonaltotop3, outline = currentFillBottom)
            canvas.itemconfig(data.questionrightdiagonaltobottom3, outline = currentFillBottom)
            canvas.itemconfig(data.questionrighttodiagonaltop3, outline = currentFillBottom)
            canvas.itemconfig(data.questionrighttodiagonalbottom3, outline = currentFillBottom)
            #bottom right
            canvas.itemconfig(data.questiontopleft4, fill = currentFillBottom)
            canvas.itemconfig(data.questionbottomleft4, fill = currentFillBottom)
            canvas.itemconfig(data.questiontop4, fill = currentFillBottom)
            canvas.itemconfig(data.questionbottom4, fill = currentFillBottom)
            canvas.itemconfig(data.questiontopright4, fill = currentFillBottom)
            canvas.itemconfig(data.questionbottomright4, fill = currentFillBottom)
            canvas.itemconfig(data.questionright4, fill = currentFillBottom)
            canvas.itemconfig(data.middlebottom, fill = currentFillBottom)
            canvas.itemconfig(data.questionleftdiagonattotop4, outline = currentFillBottom)
            canvas.itemconfig(data.questionleftdiagonaltobottom4, outline = currentFillBottom)
            canvas.itemconfig(data.questionlefttodiagonaltop4, outline = currentFillBottom)
            canvas.itemconfig(data.questionlefttodiagonalbottom4, outline = currentFillBottom)
            canvas.itemconfig(data.questionrightdiaonaltotop4, outline = currentFillBottom)
            canvas.itemconfig(data.questionrightdiagonaltobottom4, outline = currentFillBottom)
            canvas.itemconfig(data.questionrighttodiagonaltop4, outline = currentFillBottom)
            canvas.itemconfig(data.questionrighttodiagonalbottom4, outline = currentFillBottom)
        canvas.update()
    if reverseReveal == False: #normal reveal session
        if data.shortRevealNow == False:
            glint(canvas, data)
        else:
            data.shortRevealNow = False
    
def glint(canvas, data):
    #glints each answer slot, first goes up to blue for each, then 
    #goes back down to black with a 0.5 second delay for each answer slot
    startTime = clock()
    switch1Down = True
    switch2Down = True
    switch3Down = True
    switch4Down = True
    switch2 = True
    switch3 = True
    switch4 = True
    animationDurationTotal = 3.5 #seconds
    animationPartialDuration = 1
    animate2start, animate3start, animate4start = 0.5, 1, 1.5
    animate1end, animate2end, animate3end, animate4end = 2, 2.5, 3, 3.5
    animate1downStart, animate2downStart, animate3downStart, animate4downStart = 1, 1.5, 2, 2.5
    while (clock() - startTime) < animationDurationTotal:
        if (clock() - startTime) < animationPartialDuration:
            #top left goes up to blue
            proportionUp1 = (clock() - startTime) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedUp1 = 2 * proportionUp1
                targetGreenUp1 = 0 * proportionUp1
                targetBlueUp1 = 67 * proportionUp1
            else:
                if data.glintSwitch == False:
                    data.channel2.play(data.glintSound)
                    data.glintSwitch = True
                targetRedUp1 = 217 * proportionUp1
                targetGreenUp1 = 184 * proportionUp1
                targetBlueUp1 = 52 * proportionUp1
            FillUp1 = hexcolor(floor(targetRedUp1),
                                   floor(targetGreenUp1),
                                   floor(targetBlueUp1))
            canvas.itemconfig(data.q1background, fill = FillUp1)
        if ((clock() - startTime) > animate1downStart
             and (clock() - startTime) < animate1end):
            #top left goes down to black
            if switch1Down == True:
                startTime1Down = clock()
                switch1Down = False
            proportionDown1 = (clock() - startTime1Down) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedDown1 = 2 - 2 * proportionDown1
                targetGreenDown1 = 0
                targetBlueDown1 = 67 - 67 * proportionDown1
            else:
                targetRedDown1 = 217 - 217 * proportionDown1
                targetGreenDown1 = 184 - 184 * proportionDown1
                targetBlueDown1 = 52 - 52 * proportionDown1
            fillDown1 = hexcolor(floor(targetRedDown1),
                                   floor(targetGreenDown1),
                                   floor(targetBlueDown1))
            canvas.itemconfig(data.q1background, fill = fillDown1)
        if ((clock() - startTime) > animate2start
             and (clock() - startTime) < animate2downStart):
            #top right goes up to blue
            if switch2 == True:
                startTime2 = clock()
                switch2 = False
            proportionUp2 = (clock() - startTime2) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedUp2 = 2 * proportionUp2
                targetGreenUp2 = 0 * proportionUp2
                targetBlueUp2 = 67 * proportionUp2
            else:
                targetRedUp2 = 217 * proportionUp2
                targetGreenUp2 = 184 * proportionUp2
                targetBlueUp2 = 52 * proportionUp2
            fillUp2 = hexcolor(floor(targetRedUp2),
                                   floor(targetGreenUp2),
                                   floor(targetBlueUp2))
            canvas.itemconfig(data.q2background, fill = fillUp2)
        if ((clock() - startTime) > animate2downStart
             and (clock() - startTime) < animate2end):
            #top right goes down to black
            if switch2Down == True:
                startTime2Down = clock()
                switch2Down = False
            proportionDown2 = (clock() - startTime2Down) / animationPartialDuration
            if data.currentQuestion < 14:    
                targetRedDown2 = 2 - 2 * proportionDown2
                targetGreenDown2 = 0
                targetBlueDown2 = 67 - 67 * proportionDown2
            else:
                targetRedDown2 = 217 - 217 * proportionDown2
                targetGreenDown2 = 184 - 184 * proportionDown2
                targetBlueDown2 = 52 - 52 * proportionDown2
            fillDown2 = hexcolor(floor(targetRedDown2),
                                   floor(targetGreenDown2),
                                   floor(targetBlueDown2))
            canvas.itemconfig(data.q2background, fill = fillDown2)
        if ((clock() - startTime) > animate3start
             and (clock() - startTime) < animate3downStart):
            if switch3 == True:
                startTime3 = clock()
                switch3 = False
            proportionUp3 = (clock() - startTime3) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedUp3 = 2 * proportionUp3
                targetGreenUp3 = 0 * proportionUp3
                targetBlueUp3 = 67 * proportionUp3
            else:
                targetRedUp3 = 217 * proportionUp3
                targetGreenUp3 = 184 * proportionUp3
                targetBlueUp3 = 52 * proportionUp3
            fillUp3 = hexcolor(floor(targetRedUp3),
                                   floor(targetGreenUp3),
                                   floor(targetBlueUp3))
            canvas.itemconfig(data.q3background, fill = fillUp3)
        if ((clock() - startTime) > animate3downStart
             and (clock() - startTime) < animate3end):
            if switch3Down == True:
                startTime3Down = clock()
                switch3Down = False
            proportionDown3 = (clock() - startTime3Down) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedDown3 = 2 - 2 * proportionDown3
                targetGreenDown3 = 0
                targetBlueDown3 = 67 - 67 * proportionDown3
            else:
                targetRedDown3 = 217 - 217 * proportionDown3
                targetGreenDown3 = 184 - 184 * proportionDown3
                targetBlueDown3 = 52 - 52 * proportionDown3
            fillDown3 = hexcolor(floor(targetRedDown3),
                                 floor(targetGreenDown3),
                                 floor(targetBlueDown3))
            canvas.itemconfig(data.q3background, fill = fillDown3)
        if ((clock() - startTime) > animate4start
             and (clock() - startTime) < animate4downStart):
            if switch4 == True:
                startTime4 = clock()
                switch4 = False
            proportionUp4 = (clock() - startTime4) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedUp4 = 2 * proportionUp4
                targetGreenUp4 = 0 * proportionUp4
                targetBlueUp4 = 67 * proportionUp4
            else:
                targetRedUp4 = 217 * proportionUp4
                targetGreenUp4 = 184 * proportionUp4
                targetBlueUp4 = 52 * proportionUp4
            fillUp4 = hexcolor(floor(targetRedUp4),
                                   floor(targetGreenUp4),
                                   floor(targetBlueUp4))
            canvas.itemconfig(data.q4background, fill = fillUp4)
        if ((clock() - startTime) > animate4downStart
             and (clock() - startTime) < animate4end):
            if switch4Down == True:
                startTime4Down = clock()
                switch4Down = False
            proportionDown4 = (clock() - startTime4Down) / animationPartialDuration
            if data.currentQuestion < 14:
                targetRedDown4 = 2 - 2 * proportionDown4
                targetGreenDown4 = 0
                targetBlueDown4 = 67 - 67 * proportionDown4
            else:
                targetRedDown4 = 217 - 217 * proportionDown4
                targetGreenDown4 = 184 - 184 * proportionDown4
                targetBlueDown4 = 52 - 52 * proportionDown4
            fillDown4 = hexcolor(floor(targetRedDown4),
                                   floor(targetGreenDown4),
                                   floor(targetBlueDown4))
            canvas.itemconfig(data.q4background, fill = fillDown4)
        canvas.update()
    startTime = clock()
    while ((clock() - startTime) < 
           data.revealAnswerDelay - animationDurationTotal):
        canvas.after(1000) #keep waiting
    beginCountdown(canvas, data, False)

def beginCountdown(canvas, data, resume): #clock starts counting down; answers revealed
    data.waitingOnUserAnswerChoice = True #user can now select answers
    if data.infiniteTimeActivate == True: #in case infinite time was used then double dip
        instructions(canvas, data, False, "dd")
        data.clockRunning = False
        data.infiniteTimeActivate = False
    else: data.clockRunning = True #clock is now running
    if resume == False: #normal
        instructions(canvas, data, False, "startClock")
        data.questionTicking = mixer.Sound(data.path + data.tickingSounds[data.currentQuestion])
        if data.currentQuestion > 4: data.channel0.play(data.questionTicking) #starts ticking sound
        else: data.channel3.play(data.questionTicking) 
    else: #came from double dip wrong answer
        instructions(canvas, data, False, "ddWrong")
        data.channel0.unpause()
        data.channel0.set_volume(1)
        data.channel1.play(data.resumeClock)
        if data.currentQuestion < 5:
            data.channel3.set_volume(1)
            data.channel3.unpause()
        data.startTimeDotSwitch = False #in case double dip wrong answer and
        #the wrong answer was selected while a dot is in the middle of animating
    switchB = True #sets up startTime for each answer revelation
    switchC = True
    switchD = True
    animationPartialDuration = 0.25
    animate2Start, animate3Start, animate4Start = 0.1, 0.2, 0.3
    animate1End,animate2End, animate3End, animate4End = 0.25, 0.35, 0.45, 0.55
    if resume == False:
        ############Answer Options
        data.answerTextA = data.currentQuestionAttributes[2]
        data.answerTextB = data.currentQuestionAttributes[3]
        data.answerTextC = data.currentQuestionAttributes[4]
        data.answerTextD = data.currentQuestionAttributes[5]

        canvas.itemconfig(data.answerA, text = (data.answerTextA))
        canvas.itemconfig(data.answerB, text = (data.answerTextB))
        canvas.itemconfig(data.answerC, text = (data.answerTextC))
        canvas.itemconfig(data.answerD, text = (data.answerTextD))
        canvas.itemconfig(data.labelA, text = "A:")
        canvas.itemconfig(data.labelB, text = "B:")
        canvas.itemconfig(data.labelC, text = "C:")
        canvas.itemconfig(data.labelD, text = "D:")

    startTime = clock() #start ticking cue
    animationDuration = data.timeLeft #seconds
    while (clock() - startTime) < animationDuration - 0.1:
        if data.currentQuestion == 14:
            if data.millLastSwitch == False:
                if data.timeLeft == 20:
                    data.millLastSwitch = True
                    data.channel0.play(data.millLast)
        if data.clockRunning == False: break
        if data.switchQuestionActivate == True: #switch the question lifeline activated
            data.clockRunning = False
            data.waitingOnUserAnswerChoice = False
            data.waitingOnVerify = True
            #remove lifeline icon
            canvas.delete(data.switchOval)
            canvas.delete(data.switchTop1)
            canvas.delete(data.switchTop2)
            canvas.delete(data.switchTop3)
            canvas.delete(data.switchBottom)
            canvas.delete(data.switchLabel)
            if data.lifelinesRemaining == 0:
                canvas.delete(data.lifelineBottom)
            break
        elif data.infiniteTimeActivate == True:
            instructions(canvas, data, False, "infinite")
            data.clockRunning = False
            canvas.delete(data.infiniteOval)
            canvas.delete(data.infiniteTop1)
            canvas.delete(data.infiniteTop2)
            canvas.delete(data.infiniteBottom)
            canvas.delete(data.infiniteLabel)
            data.clockAlreadyFaded = True
            #####fade out clock
            startTimeFadeOutClock = clock() #start ticking cue
            animationDurationFadeOutClock = 0.5
            while (clock() - startTimeFadeOutClock) < animationDurationFadeOutClock:
                proportion = (clock() - startTimeFadeOutClock) / animationDurationFadeOutClock
                #fading out semicircular clock
                if data.currentQuestion < 14:
                    targetRed = floor(55 - 55 * proportion)
                    targetGreen = floor(95 - 95 * proportion)
                    targetBlue = floor(134 - 134 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval1, fill = currentFill)
                    canvas.itemconfig(data.oval1, outline = currentFill)
                    targetRed = floor(195 - 195 * proportion)
                    targetGreen = floor(85 - 85 * proportion)
                    targetBlue = floor(117 - 117 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval2red, fill = currentFill)
                    targetRed = floor(240 - 240 * proportion)
                    targetGreen = floor(240 - 240 * proportion)
                    targetBlue = floor(249 - 249 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval2, fill = currentFill)
                    targetRed = floor(17 - 17 * proportion)
                    targetGreen = floor(48 - 48 * proportion)
                    targetBlue = floor(79 - 79 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval2red, outline = currentFill)
                    canvas.itemconfig(data.oval2, outline = currentFill)
                    if data.ranOutOfTime == True: #ran out of time 
                        targetRedOval3 = 0
                        targetGreenOval3 = floor(15 - 15 * proportion)
                        targetBlueOval3 = floor(73 - 73 * proportion)
                        targetRedText = floor(155 - 155 * proportion)
                        targetGreenText = floor(158 - 158 * proportion)
                        targetBlueText = floor(191 - 191 * proportion)
                    else: #wrong answer
                        targetRedOval3 = floor(18 - 18 * proportion)
                        targetGreenOval3 = floor(44 - 44 * proportion)
                        targetBlueOval3 = floor(138 - 138 * proportion)
                        targetRedText = floor(236 - 236 * proportion)
                        targetGreenText = floor(222 - 222 * proportion)
                        targetBlueText = floor(177 - 177 * proportion)
                    fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
                    canvas.itemconfig(data.oval3, fill = fillOval3)
                    canvas.itemconfig(data.oval3, outline = fillOval3)
                    fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
                    canvas.itemconfig(data.timelabel, fill = fillText)
                else: #million dollar question golden clock fade out
                    targetRed = floor(168 - 168 * proportion)
                    targetGreen = floor(149 - 149 * proportion)
                    targetBlue = floor(102 - 102 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval1, fill = currentFill)
                    canvas.itemconfig(data.oval1, outline = currentFill)
                    targetRed = floor(171 - 171 * proportion)
                    targetGreen = floor(105 - 105 * proportion)
                    targetBlue = floor(75 - 75 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval2red, fill = currentFill)
                    targetRed = floor(223 - 223 * proportion)
                    targetGreen = floor(206 - 206 * proportion)
                    targetBlue = floor(142 - 142 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval2, fill = currentFill)
                    targetRed = floor(223 - 223 * proportion)
                    targetGreen = floor(206 - 206 * proportion)
                    targetBlue = floor(142 - 142 * proportion)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.oval2red, outline = currentFill)
                    canvas.itemconfig(data.oval2, outline = currentFill)
                    if data.ranOutOfTime == True: #ran out of time on milion
                        targetRedOval3 = floor(99 - 99 * proportion)
                        targetGreenOval3 = floor(74 - 74 * proportion)
                        targetBlueOval3 = floor(45 - 45 * proportion)
                        targetRedText = floor(156 - 156 * proportion)
                        targetGreenText = floor(159 - 159 * proportion)
                        targetBlueText = floor(192 - 192 * proportion)
                    else: #wrong answer on million
                        targetRedOval3 = floor(138 - 138 * proportion)
                        targetGreenOval3 = floor(113 - 113 * proportion)
                        targetBlueOval3 = floor(36 - 36 * proportion)
                        targetRedText = floor(235 - 235 * proportion)
                        targetGreenText = floor(232 - 232 * proportion)
                        targetBlueText = floor(177 - 177 * proportion)
                    fillOval3 = hexcolor(targetRedOval3, targetGreenOval3, targetBlueOval3)
                    canvas.itemconfig(data.oval3, fill = fillOval3)
                    canvas.itemconfig(data.oval3, outline = fillOval3)
                    fillText = hexcolor(targetRedText, targetGreenText, targetBlueText)
                    canvas.itemconfig(data.timelabel, fill = fillText)                    
                if data.ranOutOfTime == False: #some circles inert some active
                    for indicatorDot in range(15):
                        if indicatorDot > data.currentcir:
                            #active dot fade to black animation
                            if data.currentQuestion < 14: #non-million dollar fade
                                targetRed = floor(175 - 175 * proportion)
                                targetGreen = floor(253 - 253 * proportion)
                                targetBlue = floor(255 - 255 * proportion)
                            else: #million dollar question fade
                                targetRed = floor(255 - 255 * proportion)
                                targetGreen = floor(246 - 246 * proportion)
                                targetBlue = floor(204 - 204 * proportion)
                        else: #inert dot fade to black animation
                            if data.currentQuestion < 14: #non-million dollar fade
                                targetRed = floor(76 - 76 * proportion)
                                targetGreen = floor(91 - 91 * proportion)
                                targetBlue = floor(219 - 219 * proportion)
                            else: #million dollar question fade
                                targetRed = floor(165 - 165 * proportion)
                                targetGreen = floor(149 - 149 * proportion)
                                targetBlue = floor(81 - 81 * proportion)
                        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                        canvas.itemconfig(data.circlesRight[indicatorDot], fill = currentFill)
                        canvas.itemconfig(data.circlesLeft[indicatorDot], fill = currentFill)
                else: #if user ran out of time, then all circles must be active
                    for indicatorDot in range(15):
                        if data.currentQuestion < 14: #non-million dollar fade
                            targetRed = floor(175 - 175 * proportion)
                            targetGreen = floor(253 - 253 * proportion)
                            targetBlue = floor(255 - 255 * proportion)
                        else: #million dollar question fade
                            targetRed = floor(165 - 165 * proportion)
                            targetGreen = floor(149 - 149 * proportion)
                            targetBlue = floor(81 - 81 * proportion)
                        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                        canvas.itemconfig(data.circlesRight[indicatorDot], fill = currentFill)
                        canvas.itemconfig(data.circlesLeft[indicatorDot], fill = currentFill)
                canvas.update()
            for indicatorDot in range(15): #ensure all circles are faded out
                canvas.itemconfig(data.circlesRight[indicatorDot], fill = "#000000")
                canvas.itemconfig(data.circlesLeft[indicatorDot], fill = "#000000")

            ######end fade out clock code
            #fade out switch the question and 50:50 to indicate they may not be used 
            #once infinite time has been activated
            if data.usedSwitchQuestion == False:
                canvas.itemconfig(data.switchOval, outline = "#2c2b2b")
                canvas.itemconfig(data.switchLabel, fill = "#2c2b2b")
                canvas.itemconfig(data.switchTop1, fill = "#2c2b2b")
                canvas.itemconfig(data.switchTop2, fill = "#2c2b2b")
                canvas.itemconfig(data.switchTop3, fill = "#2c2b2b")
                canvas.itemconfig(data.switchBottom, fill = "#2c2b2b")
            if data.usedFiftyFifty == False:
                canvas.itemconfig(data.fiftyFiftyOval, outline = "#2c2b2b")
                canvas.itemconfig(data.fiftyFiftyLabel, fill = "#2c2b2b")
                canvas.itemconfig(data.fiftyFiftyTop, fill = "#2c2b2b")
                canvas.itemconfig(data.fiftyFiftyBottom, fill = "#2c2b2b")
            if data.lifelinesRemaining == 0:
                canvas.delete(data.lifelineBottom)
        elif data.doubleDipActivate == True:
            instructions(canvas, data, False, "dd")
            canvas.delete(data.doubleDipOval)
            canvas.delete(data.doubleDipTop)
            canvas.delete(data.doubleDipBottom)
            canvas.delete(data.doubleDipLabel)
            if data.usedInfiniteTime == False:
                canvas.itemconfig(data.infiniteOval, outline = "#2c2b2b")
                canvas.itemconfig(data.infiniteTop1, fill = "#2c2b2b")
                canvas.itemconfig(data.infiniteTop2, fill = "#2c2b2b")
                canvas.itemconfig(data.infiniteBottom, fill = "#2c2b2b")
                canvas.itemconfig(data.infiniteLabel, fill = "#2c2b2b")
            if data.usedFiftyFifty == False:
                canvas.itemconfig(data.fiftyFiftyOval, outline = "#2c2b2b")
                canvas.itemconfig(data.fiftyFiftyLabel, fill = "#2c2b2b")
                canvas.itemconfig(data.fiftyFiftyTop, fill = "#2c2b2b")
                canvas.itemconfig(data.fiftyFiftyBottom, fill = "#2c2b2b")
            if data.usedSwitchQuestion == False:
                canvas.itemconfig(data.switchOval, outline = "#2c2b2b")
                canvas.itemconfig(data.switchLabel, fill = "#2c2b2b")
                canvas.itemconfig(data.switchTop1, fill = "#2c2b2b")
                canvas.itemconfig(data.switchTop2, fill = "#2c2b2b")
                canvas.itemconfig(data.switchTop3, fill = "#2c2b2b")
                canvas.itemconfig(data.switchBottom, fill = "#2c2b2b")
            if data.lifelinesRemaining == 0:
                canvas.delete(data.lifelineBottom)
        proportion = (clock() - startTime) / animationDuration

        # reveal answers
        if ((clock() - startTime) < animate1End and
             resume == False): #reveal answer A
            proportionA = (clock() - startTime) / animationPartialDuration
            targetRedActualA = 255 * proportionA
            targetGreenActualA = 255 * proportionA
            targetBlueActualA = 255 * proportionA
            #label target RGB (223, 146, 32)
            targetRedLabelA = 223 * proportionA
            targetGreenLabelA = 146 * proportionA
            targetBlueLabelA = 32 * proportionA
            fillActualA = hexcolor(floor(targetRedActualA),
                                   floor(targetGreenActualA),
                                   floor(targetBlueActualA))
            fillLabelA = hexcolor(floor(targetRedLabelA),
                                   floor(targetGreenLabelA),
                                   floor(targetBlueLabelA))
            canvas.itemconfig(data.answerA, fill = fillActualA)
            canvas.itemconfig(data.labelA, fill = fillLabelA)
        if ((clock() - startTime) > animate2Start 
            and (clock() - startTime) < animate2End 
            and resume == False):
            if switchB == True:
                startTimeB = clock()
                switchB = False
            proportionB = (clock() - startTimeB) / animationPartialDuration
            targetRedActualB = 255 * proportionB
            targetGreenActualB = 255 * proportionB
            targetBlueActualB = 255 * proportionB
            #label target RGB (223, 146, 32)
            targetRedLabelB = 223 * proportionB
            targetGreenLabelB = 146 * proportionB
            targetBlueLabelB = 32 * proportionB
            fillActualB = hexcolor(floor(targetRedActualB),
                                   floor(targetGreenActualB),
                                   floor(targetBlueActualB))
            fillLabelB = hexcolor(floor(targetRedLabelB),
                                   floor(targetGreenLabelB),
                                   floor(targetBlueLabelB))
            canvas.itemconfig(data.answerB, fill = fillActualB)
            canvas.itemconfig(data.labelB, fill = fillLabelB)
        if ((clock() - startTime) > animate3Start 
            and (clock() - startTime) < animate3End 
            and resume == False):
            if switchC == True:
                startTimeC = clock()
                switchC = False
            proportionC = (clock() - startTimeC) / animationPartialDuration
            targetRedActualC = 255 * proportionC
            targetGreenActualC = 255 * proportionC
            targetBlueActualC = 255 * proportionC
            #label target RGB (223, 146, 32)
            targetRedLabelC = 223 * proportionC
            targetGreenLabelC = 146 * proportionC
            targetBlueLabelC = 32 * proportionC
            fillActualC = hexcolor(floor(targetRedActualC),
                                   floor(targetGreenActualC),
                                   floor(targetBlueActualC))
            fillLabelC = hexcolor(floor(targetRedLabelC),
                                   floor(targetGreenLabelC),
                                   floor(targetBlueLabelC))
            canvas.itemconfig(data.answerC, fill = fillActualC)
            canvas.itemconfig(data.labelC, fill = fillLabelC)
        if ((clock() - startTime) > animate4Start 
            and (clock() - startTime) < animate4End 
            and resume == False):
            if switchD == True:
                startTimeD = clock()
                switchD = False
            proportionD = (clock() - startTimeD) / animationPartialDuration
            targetRedActualD = 255 * proportionD
            targetGreenActualD = 255 * proportionD
            targetBlueActualD = 255 * proportionD
            #label target RGB (223, 146, 32)
            targetRedLabelD = 223 * proportionD
            targetGreenLabelD = 146 * proportionD
            targetBlueLabelD = 32 * proportionD
            fillActualD = hexcolor(floor(targetRedActualD),
                                   floor(targetGreenActualD),
                                   floor(targetBlueActualD))
            fillLabelD = hexcolor(floor(targetRedLabelD),
                                   floor(targetGreenLabelD),
                                   floor(targetBlueLabelD))
            canvas.itemconfig(data.answerD, fill = fillActualD)
            canvas.itemconfig(data.labelD, fill = fillLabelD)
        #fifty-fifty lifeline activation
        if data.fiftyFiftyActivate == True:
            instructions(canvas, data, False, "50:50")
            data.fiftyFiftyActivate = False
            data.tempPreventDip = True
            data.correctAnswer = int(data.currentQuestionAttributes[6])
            firstRemove = randrange(1,5)
            while firstRemove == data.correctAnswer: #prevent removing correct answer
                firstRemove = randrange(1,5)
            secondRemove = randrange(1,5)
            while (secondRemove == firstRemove or secondRemove == data.correctAnswer):
                secondRemove = randrange(1,5)
            removeAnswer(canvas, data, firstRemove)
            removeAnswer(canvas, data, secondRemove)
            canvas.delete(data.fiftyFiftyOval)
            canvas.delete(data.fiftyFiftyLabel)
            canvas.delete(data.fiftyFiftyTop)
            canvas.delete(data.fiftyFiftyBottom)
            if data.usedDoubleDip == False:
                canvas.itemconfig(data.doubleDipOval, outline = "#2c2b2b")
                canvas.itemconfig(data.doubleDipLabel, fill = "#2c2b2b")
                canvas.itemconfig(data.doubleDipTop, fill = "#2c2b2b")
                canvas.itemconfig(data.doubleDipBottom, fill = "#2c2b2b")
            if data.lifelinesRemaining == 0:
                canvas.delete(data.lifelineBottom)
        #updating the clock arc    
        if data.timerSeconds - (clock()-startTime) > 0:
            if resume == False:
                data.timeLeft = floor(data.timerSeconds - (clock()-startTime))
                if data.currentQuestion < 14:
                    canvas.itemconfig(data.timelabel, text = data.timeLeft)
                else: #million dollar question
                    canvas.itemconfig(data.timelabel, text = prettytime(normaltime(data.timeLeft)))
                data.extentvalue = floor((180 - 180 * proportion))
                canvas.itemconfig(data.oval2, extent = data.extentvalue)
            else: #resuming timer
                data.timeLeft = floor(data.resumeTime - (clock()-startTime))
                if data.currentQuestion < 14:
                    canvas.itemconfig(data.timelabel, text = data.timeLeft)
                else: #million dollar question resume from double dip incorrect
                    canvas.itemconfig(data.timelabel, text = prettytime(normaltime(data.timeLeft)))
                data.extentvalue = (data.resumeExtent - data.resumeExtent * proportion) 
                canvas.itemconfig(data.oval2, extent = data.extentvalue)
        else:
            data.red2 = 18 #for oval3 in outoftime 
            data.green2 = 44
            data.blue2 = 138
        if data.inerttoactiveswitch == 0: #switch is 0 which means delay
            if ceil((clock()- startTime)) % (data.timerSeconds // 15) == 0 and \
                      ceil((clock()- startTime)) != data.currentSecond:
                      #mod 3 for 45 seconds, mod 2 for 30 seconds, mod 1 for 15 seconds
                data.currentSecond = ceil((clock()- startTime)) 
                data.inerttoactiveswitch = 1 
        if data.inerttoactiveswitch == 1 and data.clockRunning == True: 
            if data.startTimeDotSwitch == False:
                startTimeDot = clock()
                data.startTimeDotSwitch = True
            animationDurationDot = 0.25
            if (clock() - startTimeDot) < animationDurationDot:
                if data.currentcir >= 0:
                    proportionDot = (clock() - startTimeDot) / animationDurationDot
                    if data.currentQuestion < 14: #non-million active blue
                        targetRed = 76 + floor(99 * proportionDot)
                        targetGreen = 91 + floor(162 * proportionDot)
                        targetBlue = 219 + floor(36 * proportionDot)
                    else: #million dollar question active golden
                        targetRed = 165 + floor(90 * proportionDot)
                        targetGreen = 149 + floor(97 * proportionDot)
                        targetBlue = 81 + floor(123 * proportionDot)
                    currentFill = hexcolor(targetRed, targetGreen, targetBlue)
                    canvas.itemconfig(data.circlesLeft[data.currentcir],fill = currentFill) #animates left circles
                    canvas.itemconfig(data.circlesRight[data.currentcir],fill = currentFill) #animates right circles
            else:
                data.inerttoactiveswitch = 0 #delay until next circle is ready to animate
                if data.currentcir >= 0:
                    data.currentcir -= 1 #change the index of the circle to be animated next
                    data.startTimeDotSwitch = False
        canvas.update()
    if data.clockRunning == False: return None
    if data.currentcir >= 0:
        startTimeDot = clock() #animate last dot pair
        while (clock() - startTimeDot) < animationDurationDot: 
            proportionDot = (clock() - startTimeDot) / animationDurationDot
            if data.currentQuestion < 14: #non-million active blue
                targetRed = 76 + floor(99 * proportionDot)
                targetGreen = 91 + floor(162 * proportionDot)
                targetBlue = 219 + floor(36 * proportionDot)
            else:
                targetRed = 165 + floor(90 * proportionDot)
                targetGreen = 149 + floor(97 * proportionDot)
                targetBlue = 81 + floor(123 * proportionDot)
            currentFill = hexcolor(targetRed, targetGreen, targetBlue)
            canvas.itemconfig(data.circlesLeft[data.currentcir],fill = currentFill) #animates left circles
            canvas.itemconfig(data.circlesRight[data.currentcir],fill = currentFill) #animates right circles
            canvas.update()
    data.extentvalue = 0 
    canvas.itemconfig(data.oval2, extent = data.extentvalue)
    if data.currentQuestion < 14:
        canvas.itemconfig(data.timelabel, text = "0")
    else:
        canvas.itemconfig(data.timelabel, text = "0:00")
    canvas.update()

    data.ranOutOfTime = True
    instructions(canvas, data, False, "Out of Time")
    if data.doubleDipActivate == True:
        data.channel1.play(data.outOfTimeSound)
    else: #no double dip used
        if data.currentQuestion < 5:
            data.channel0.play(data.outOfTimeSound)
    startTime = clock() #out of time animation
    animationDurationTotal = 1
    animationDownStart = 0.25
    animationPartialDuration1, animationPartialDuration2 = 0.25, 0.75
    switchDown = True #False once semicircle is bright red
    while (clock() - startTime) < animationDurationTotal: 
        proportion = (clock() - startTime) / animationDurationTotal
        if (clock() - startTime) < animationDownStart:
            proportionUp = (clock() - startTime) / animationPartialDuration1
            if data.currentQuestion < 14:
                targetRedCircle = 18 + floor(192 * proportionUp)
                targetGreenCircle = 44 + floor(98 * proportionUp)
                targetBlueCircle = 138 + floor(60 * proportionUp)
            else: #million dollar question out of time 
                targetRedCircle = 138 + floor(117 * proportionUp)
                targetGreenCircle = 113 + floor(142 * proportionUp)
                targetBlueCircle = 36 + floor(219 * proportionUp)
                targetRedTextUp = 235 + floor(20 * proportionUp)
                targetGreenTextUp = 232 + floor(23 * proportionUp)
                targetBlueTextUp = 177 + floor(78 * proportionUp)
                fillUpText = hexcolor(targetRedTextUp, targetGreenTextUp,
                                      targetBlueTextUp)
                canvas.itemconfig(data.timelabel, fill = fillUpText)
            fillUp = hexcolor(targetRedCircle, 
                              targetGreenCircle,
                              targetBlueCircle)
            canvas.itemconfig(data.oval3, fill = fillUp)
        if ((clock() - startTime) > animationDownStart and 
            (clock() - startTime) < animationDurationTotal):
            if switchDown == True:
                startTimeDown = clock()
                switchDown = False
            proportionDown = (clock() - startTimeDown) / animationPartialDuration2
            if data.currentQuestion < 14:
                targetRedCircleDown = 210 - floor(210 * proportionDown)
                targetGreenCircleDown = 142 - floor(127 * proportionDown)
                targetBlueCircleDown = 198 - floor(125 * proportionDown)
            else: #million dollar question out of time white to dark yellow
                targetRedCircleDown = 255 - floor(157 * proportionDown)
                targetGreenCircleDown = 255 - floor(182 * proportionDown)
                targetBlueCircleDown = 255 - floor(211 * proportionDown)
            fillDown = hexcolor(targetRedCircleDown, 
                              targetGreenCircleDown,
                              targetBlueCircleDown)
            canvas.itemconfig(data.oval3, fill = fillDown)
            if data.currentQuestion < 14:
                targetRedText = 236 - floor(81 * proportionDown)
                targetGreenText = 222 - floor(64 * proportionDown)
                targetBlueText = 177 + floor(14 * proportionDown)
            else:
                targetRedText = 255 - floor(100 * proportionDown)
                targetGreenText = 255 - floor(97 * proportionDown)
                targetBlueText = 255 - floor(64 * proportionDown)
            fillText = hexcolor(targetRedText, 
                                  targetGreenText,
                                  targetBlueText)
            canvas.itemconfig(data.timelabel, fill = fillText)
        canvas.update()
    #remove residual proportions from oval3 and timelabel
    if data.currentQuestion < 14:
        targetRedCircleDown = 210 - floor(210 * 1)
        targetGreenCircleDown = 142 - floor(127 * 1)
        targetBlueCircleDown = 198 - floor(125 * 1)
    else: #million dollar question out of time white to dark yellow
        targetRedCircleDown = 255 - floor(157 * 1)
        targetGreenCircleDown = 255 - floor(182 * 1)
        targetBlueCircleDown = 255 - floor(211 * 1)
    fillDown = hexcolor(targetRedCircleDown, 
                      targetGreenCircleDown,
                      targetBlueCircleDown)
    canvas.itemconfig(data.oval3, fill = fillDown)
    canvas.itemconfig(data.timelabel, fill = fillText)
    canvas.update()
    data.gameOver = True
    data.doubleDipActivate = False
    data.waitingOnReveal = False
    data.waitingOnUserAnswerChoice = False
    data.waitingOnVerify = True

def shortRevealAll(canvas, data, switchQuestion):
    if switchQuestion == False:
        startTime = clock() #start ticking cue
        animationDuration = 0.5 #seconds
        musicSwitch = False
        while (clock() - startTime) < animationDuration: #fade out winnings label
            if musicSwitch == False and data.currentQuestion > 4:
                musicSwitch = True
                data.questionLetsPlay = mixer.Sound(data.path + data.letsPlaySounds[data.currentQuestion])
                data.channel0.play(data.questionLetsPlay)
            proportion = (clock() - startTime) / animationDuration
            targetRed = floor(199 - 199 * proportion)
            targetGreen = floor(211 - 211 * proportion)
            targetBlue = floor(247 - 247 * proportion)
            winningFill = hexcolor(targetRed,
                                   targetGreen,
                                   targetBlue)
            canvas.itemconfig(data.winningsLabel, fill = winningFill)
            canvas.update()    
        if data.currentQuestion > 4: canvas.after(4000) #delay next question's reveal
        data.channel1.play(data.revealQuestionSound)
        revealAnswerBars(canvas, data, False)
    else:
        if data.currentQuestion < 5:
            data.channel0.play(data.questions100to1000Bed) #start replaying music
        else: data.channel0.play(data.switchSpecialCue)
        data.channel1.play(data.revealQuestionSound) 
        data.switchQuestionActivate = False #just switched the question
        data.timeLeft = data.clockAmounts[data.currentQuestion]
        data.timerSeconds = data.clockAmounts[data.currentQuestion]
    canvas.itemconfig(data.timelabel, text = data.timeLeft) #reset time label
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration

        #fade in semicircular clock
        targetRed = floor(55* proportion)
        targetGreen = floor(95* proportion)
        targetBlue = floor(134* proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.oval1, fill = currentFill)
        canvas.itemconfig(data.oval1, outline = currentFill)
        targetRed = floor(195 * proportion)
        targetGreen = floor(85 * proportion)
        targetBlue = floor(117 * proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.oval2red, fill = currentFill)
        targetRed = floor(240* proportion)
        targetGreen = floor(240 * proportion)
        targetBlue = floor(249 * proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.oval2, fill = currentFill)
        targetRed = floor(17 * proportion)
        targetGreen = floor(48* proportion)
        targetBlue = floor(79* proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.oval2red, outline = currentFill)
        canvas.itemconfig(data.oval2, outline = currentFill)
        targetRed = floor(18 * proportion)
        targetGreen = floor(44 * proportion)
        targetBlue = floor(138 * proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.oval3, fill = currentFill)
        targetRed = 0
        targetGreen = floor(9* proportion)
        targetBlue = floor(69 * proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.oval3, outline = currentFill)
        #fade in clock label
        targetRed = floor(236 * proportion)
        targetGreen = floor(222 * proportion)
        targetBlue = floor(177 * proportion)
        currentFill = hexcolor(targetRed, targetGreen, targetBlue)
        canvas.itemconfig(data.timelabel, fill = currentFill)
        canvas.update()
    canvas.itemconfig(data.winningsLabel, text = "") #reset winnings label
    #new question attributes initialized
    # data.currentQuestionAttributes = selectQuestion(data, data.currentQuestion)
    difficulty = difficultySelector(data.currentQuestion)
    if data.dynamicGeneration == True:
        testGenerate = randrange(10) 
        if testGenerate < 3: 
            data.dynamicGeneration = False
            if data.cylinderGiven == False:
                testGenerate = randrange(10) 
                if testGenerate < 5: 
                    data.cylinderGiven = True
                    data.currentQuestionAttributes = dynamicCylinderVolume(data, difficulty)
                else:
                    data.currentQuestionAttributes = dynamicArithmeticQuestion(data, difficulty)
            else:
                data.currentQuestionAttributes = dynamicArithmeticQuestion(data, difficulty)
        else: selectQuestion(data, data.currentQuestion)
    else:
        selectQuestion(data, data.currentQuestion)
    if data.questionLine1or2 == 1:
        data.questioncontent1 = data.currentQuestionAttributes[0]
        canvas.itemconfig(data.questionlabel1, text = data.questioncontent1)
    elif data.questionLine1or2 == 2:    
        data.questioncontent2b = data.currentQuestionAttributes[1]
        data.questioncontent2a = data.currentQuestionAttributes[0]
        canvas.itemconfig(data.questionlabel2b, text = data.questioncontent2b)
        canvas.itemconfig(data.questionlabel2a, text = data.questioncontent2a)
    #after fading out winnings label, then fade in new question text
    startTime = clock() #start ticking cue
    animationDuration = 0.25 #seconds
    while (clock() - startTime) < animationDuration:
        proportion = (clock() - startTime) / animationDuration
        targetRGB = floor(255 * proportion)
        currentFill = hexcolor(targetRGB, targetRGB, targetRGB)
        canvas.itemconfig(data.questionlabel1, fill = currentFill)
        canvas.itemconfig(data.questionlabel2b, fill = currentFill)
        canvas.itemconfig(data.questionlabel2a, fill = currentFill)
        #fade in new question's value label
        canvas.itemconfig(data.questionValueLabel, fill = currentFill)
        canvas.update()   
    data.colors = []
    for j in range(15): #reset dots
        data.colors.append([0-j*16,0-j*15,0-j*15,0])
    data.currentcir = 14
    data.inerttoactiveswitch = 0
    data.currentSecond = 0
    activatecircle(canvas, data)
    glint(canvas, data)

def run(width, height):
    def deltaDrawWrapper(canvas, data):
        if (data.readyForDeltaDraw == True):
            deltaDraw(canvas, data)
            canvas.update()
        else:
            redrawAllWrapper(canvas, data)

    def redrawAllWrapper(canvas, data):
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        deltaDrawWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    loadQuestion(data)
    data.width, data.height = width, height
    # create the root and the canvas
    root = Tk()
    root.title("Who Wants to Be a Millionaire?")
    root.iconbitmap(data.iconPath)
    root.resizable(0,0)
    canvas = Canvas(root, width=data.width, height=data.height,
                    borderwidth=0, highlightthickness=0, bg="black")
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    drawMenu(canvas, data)
    timerFiredWrapper(canvas, data)
    root.mainloop()  # blocks until window is closed

run(1400,800)