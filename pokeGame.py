import pygame, sys, random, openpyxl, os
from pygame.locals import *
import pokeBallAssets as assets
import pytweening as tween


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Setting windowwidth and windowheight variables as global.
#The risk is that I won't be able to tell where they are being changed.
#The benefit is not needing to pass in and return these variables.
global WINDOWWIDTH, WINDOWHEIGHT

FPS = 30
# To change 
WINDOWWIDTH = assets.WINDOWWIDTH
WINDOWHEIGHT = assets.WINDOWHEIGHT

gridHeight = 192
gridWidth =  170

BLACK           =(  0,   0, 0)
WHITE           =(255, 255, 255)

BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK

throwTween = tween.easeInSine
dropTween = tween.easeInSine
wobbleTween = tween.easeInCirc
bounceTween = tween.easeOutBounce
pokeBallTween = tween.easeInOutSine
throwAnimationSpeed = 7
animationSpeed = 10
ballOffset = 160
flashOffset = 280

locationAngles = [0, 60, 120, 180, 240, 300]

quizPath = r'.\quiz'
possibleUnits = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6']
subSets = ['1', '2']
# tracks = ['johtoTrainerBattle', 'gymBattle', 'darkCave']
# track = random.choice(tracks)
menuTrack = 'menu'
teamTurn = 0

# bkgImg = assets.backgrounds['grass']

locations = [
    assets.getTrigoFromCenter(0, ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(60, ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(120, ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(180, ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(240, ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(300, ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2)
    ]




def main(teams, initObjects, teamTurn, quizObject):
    global FPSCLOCK, WINDOWWIDTH, WINDOWHEIGHT
    pygame.init()

    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    enemyPoke = initObjects[2]
    roundTheme = initObjects[3]

    firstTeam = teams[0]
    secondTeam = teams[1]

    sessionQuestions = quizObject.questions
    random.shuffle(sessionQuestions)
    sessionFlashcards = getFlashcards(quizObject)
    
    sessionChosenQuestion = random.choice(sessionQuestions)

    # correctQAPair, sessionQAList, sessionFlashcards = excelGetGameScheme(book, unit, section)

    ballMessages = ['X' for _ in range(5)]
    ballMessages.append('O')
    random.shuffle(ballMessages)

    questionSurf, questionRect = makeQuestionPanel(sessionChosenQuestion)
    
    pokeBalls = generatePokeballs(ballMessages)


    bkgImg = assets.backgrounds[roundTheme]
    enemyPoke.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 20)

    rotations = random.randint(3, 5)

    spinAnimation(pokeBalls, locationAngles, animationSpeed, enemyPoke, DISPLAYSURF, teams, roundTheme, bkgImg, rotations)
    questionRect.centerx = WINDOWWIDTH/2
    
    lastGuess = None
    winState = None
    tries = 0
       
    

    while True:

        DISPLAYSURF.fill(BLACK)
        drawBackground(bkgImg, DISPLAYSURF)
        if teamTurn > 1:
            teamTurn = 0

        currentTeam = teams[teamTurn]
        currentTeam.drawTurnIndicator(DISPLAYSURF, WINDOWWIDTH)
        
    
        

        mouseClick = False
        lastGuess = None


        checkForQuit()


        mouseX, mouseY = pygame.mouse.get_pos()

        musicRepeat(roundTheme)

        newDim = None
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouseClick = True
            elif event.type == VIDEORESIZE:
                newDim = event.size
        
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)

            enemyPoke.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2 + 20)
            questionRect.centerx = WINDOWWIDTH/2

            

        for ball in pokeBalls:
            collideRect = ball.rect.copy()
            collideRect.inflate_ip(-120, -30)
            if collideRect.collidepoint(mouseX, mouseY):
                if mouseClick:
                    
                    if ball.state == 'closed':
                        assets.ballOpenSound.play()
                        tries += 1
                        
                        lastGuess = ball.message
                        ball.state = 'open'    

        if lastGuess:
            if lastGuess == 'O':
                winState = 'Win'
                
                
                
                if tries == 1:
                    currentTeam.addUltraPoint()
                    enemyPoke.HPValue -= 2
                    assets.critHitSound.play()

                
                elif tries == 2 :
                    currentTeam.addGreatPoint()
                    enemyPoke.HPValue -= 2
                    assets.critHitSound.play()
                else:
                    currentTeam.addPoint()
                    enemyPoke.HPValue -= 1
                    assets.hitSound.play()

            teamTurn += 1
            

        if tries > 4 and winState != 'Win': # On the 5th try, if no-one won, alakazam laughs.
            winState = 'Fail'
            assets.nopeSound.play()
            

        
        for team in teams:
            team.drawTeamLabel(DISPLAYSURF, WINDOWWIDTH)
        

        DISPLAYSURF.blit(enemyPoke.surface, enemyPoke.rect)
        drawFlashcards(sessionFlashcards, DISPLAYSURF)
        drawPokeBallDefaultLocations(pokeBalls, locationAngles, DISPLAYSURF)
        
        
        DISPLAYSURF.blit(questionSurf, questionRect)

        enemyPoke.drawHP(DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT)

        
   

        pygame.display.update()

        FPSCLOCK.tick(FPS)           

        if winState:
            pygame.time.wait(1000)
            return teams, teamTurn, enemyPoke
        

def terminate():
    print('Terminating game...')
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def generatePokeballs(messages):
    random.shuffle(messages)

    pokeObjs = []
    for n in range(len(messages)):
        current = assets.pokeball(assets.pokeballImgs)
        current.message = messages[n]
        current.state = 'closed'
        pokeObjs.append(current)

    return pokeObjs


def drawPokeBallDefaultLocations(pokeballs, locations, targetSurf):
    for n in range(len(pokeballs)):
        current = pokeballs[n]
        current.rect.center = assets.getTrigoFromCenter(locations[n], ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2)
        targetSurf.blit(current.surface, current.rect)

def spinAnimation(pokeballs, locations, animationSpeed, enemyPokemon, targetSurf, teams, track, bkgImg, rotateTimes=4):
    global WINDOWWIDTH, WINDOWHEIGHT
    assets.ballSound.play()
    totalRotation = 360 * rotateTimes

    enemyPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    
    

    for rotationStep in range(0, totalRotation, animationSpeed):
        checkForQuit()
        musicRepeat(track)    

        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            elif event.type == QUIT:
                terminate()

        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
            enemyPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

        offset = pokeBallTween(rotationStep / totalRotation) * 360
        drawBackground(bkgImg, targetSurf)
        targetSurf.blit(enemyPokemon.surface, enemyPokemon.rect) 
        enemyPokemon.drawHP(targetSurf, WINDOWWIDTH, WINDOWHEIGHT)



        for n in range(len(pokeballs)):
            location = assets.getTrigoFromCenter((locations[n]+offset), ballOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2)
            pokeballs[n].rect.center = location
            targetSurf.blit(pokeballs[n].surface, pokeballs[n].rect)

           
  
        for team in teams:
            team.drawTeamLabel(targetSurf, WINDOWWIDTH)
        
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
           
# Mega meta function to set out the whole game questions and flashcards
def excelGetGameScheme(book, unit, subSet):
    path = r'.\quiz'
    bookPath = f'{book}.xlsx'
    excelPath = os.path.join(path, bookPath)

    

    wb = openpyxl.load_workbook(excelPath)
    sheet = wb[unit]

    sessionQuestions = []

    questionType = None
    flashInstructions = None

    if subSet == '1':
        questionType = sheet['A9'].value
        flashInstructions = sheet['B9'].value

    elif subSet == '2':
        questionType = sheet['A19'].value
        flashInstructions = sheet['B19'].value

    

    if questionType.lower() == 'open':
        if subSet == '1':
            rowRangeStart = 10
            rowRangeStop = 16

        elif subSet == '2':
            rowRangeStart = 20
            rowRangeStop = 26
    
        potentialQuestions = []
        for row in range(rowRangeStart, rowRangeStop):
            questionCell = sheet.cell(row=row, column=1).value
            answerCell = sheet.cell(row=row, column=2).value
            potentialQuestions.append(assets.question(questionCell, answerCell))

        correctQuestionAnswerPair = random.choice(potentialQuestions)
        sessionQuestions = [assets.question('', 'X') for _ in range(5)]
        sessionQuestions.append(correctQuestionAnswerPair)
        random.shuffle(sessionQuestions)

    elif questionType.lower() == 'closed':
        if subSet == '1':
            bedo = sheet.cell(row=10, column=1).value
        elif subSet == '2':
            bedo = sheet.cell(row=20, column=1).value

        correctQuestionAnswerPair, sessionQuestions = closedQuestionType(bedo.lower())

    
    if flashInstructions in ('all', 'All', 'ALL'):
        sessionFlashcards = getFlashcards(book, unit)
    else:
        if subSet == '1':
            setStart = int(sheet['B9'].value)
            setEnd = int(sheet['C9'].value)
        else:
            setStart = int(sheet['B19'].value)
            setEnd = int(sheet['C19'].value)
        
        
        sessionFlashcards = getFlashcards(book, unit, [setStart, setEnd])

    
    return correctQuestionAnswerPair, sessionQuestions, sessionFlashcards 
 

def closedQuestionType(bedo):
    if bedo == 'be':
        questions = [
                ("Is he...?", "Yes, he is",  "No, he isn't"),
                ("Is she...?", "Yes, she is",  "No, she isn't"),
                ("Is Tom...?", "Yes, he is",  "No, he isn't"),
                ("Is Alice...?", "Yes, she is",  "No, she isn't"),
                ("Are they...?", "Yes, they are",  "No, they're not"),
                ("Are you...?", "Yes, I am",  "No, I'm not")
            ]
    else:
        questions = [
                ("Does he...?", "Yes, he does",  "No, he doesn't"),
                ("Does she...?", "Yes, she does",  "No, she doesn't"),
                ("Does Tom...?", "Yes, he does",  "No, he doesn't"),
                ("Does Alice...?", "Yes, she does",  "No, she doesn't"),
                ("Do they...?", "Yes, they do",  "No, they don't"),
                ("Do you...?", "Yes, I do",  "No, I don't")
            ]

    randomlyPickedQuestion = random.choice(questions)
    question = randomlyPickedQuestion[0]
    correctAnswer = randomlyPickedQuestion[1]
    wrongAnswer = randomlyPickedQuestion[2]

    rightQAPair = assets.question(question, correctAnswer)

    AnswerList = [assets.question(None, wrongAnswer) for _ in range(5)]
    AnswerList.append(rightQAPair)
    random.shuffle(AnswerList)

    return rightQAPair, AnswerList


def makeQuestionPanel(question):

    global WINDOWWIDTH

    questionFont = assets.pokeFont(30)
    text = questionFont.render(question, 1, MAINTEXTCOLOR)
    textRect = text.get_rect()
    textRect.center = (WINDOWWIDTH/2, 30)

    return (text, textRect)

def getFlashcards(quizObject):
    basePath = '.\\'

    sessionPath = os.path.join(basePath, quizObject.book, quizObject.unit)

    try:
        imagePaths = [os.path.join(sessionPath, image) for image in os.listdir(sessionPath) if os.path.splitext(image)[1] in ('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG')]
    except:
        print('ERROR: Failed to find the unit folder or flashcard files. Do the units in the excel file have the same name as the flashcard folders?')
    
    sessionFlashcardRange = quizObject.flashcardRange  
    flashcardRangeTriggers = (',', ';', ':')
    needToSplit = False
    triggerUsed = None
    for trigger in flashcardRangeTriggers:
        if trigger in sessionFlashcardRange:
            triggerUsed = trigger
            needToSplit = True
            break
    if needToSplit:
        print('Playing with selection of flashcards')
        splitRangeIntoList = sessionFlashcardRange.split(triggerUsed)
        start = int(splitRangeIntoList[0])-1
        if start > 0:
            start = 0
        stop = int(splitRangeIntoList[1])
        imagePaths = imagePaths[start:stop]

        
    else:
        print(f'Playing with all flashcards')


    
    if len(imagePaths) > 6:
        sessionImgs = random.sample(imagePaths, 6)
    else:
        sessionImgs = imagePaths
        random.shuffle(sessionImgs)

    pyImages = [pygame.image.load(imgFile) for imgFile in sessionImgs]

    #TODO this is where the transform needs to be updated
    return [doImageTransform(image) for image in pyImages]

def doImageTransform(image):
    targetWidth = 250
    targetHeight = 175

    size = image.get_rect().size
    width, height = size

    if width > height:
        dividingRatio = width / targetWidth
        targetHeight = int(height // dividingRatio)
    elif width < height:
        dividingRatio = height / targetHeight
        targetWidth = int(width // dividingRatio)
    
    elif width == height:
        targetWidth == 200
        targetHeight == 200

    return pygame.transform.scale(image, (targetWidth, targetHeight))


def drawFlashcards(flashList, targetSurf):
    global WINDOWWIDTH, WINDOWHEIGHT
    flashLocationList = [
    assets.getTrigoFromCenter(0, flashOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(60, flashOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(120, flashOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(180, flashOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(240, flashOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2),
    assets.getTrigoFromCenter(300, flashOffset, WINDOWWIDTH/2, WINDOWHEIGHT/2)
    ]
    for n in range(len(flashList)):
            
            current = flashList[n]
            
            currentRect = current.get_rect()
            currentRect.center = flashLocationList[n]

            targetSurf.blit(current, currentRect)



def musicRepeat(track):
    for event in pygame.event.get(pygame.USEREVENT):
            pygame.mixer.music.load(assets.music[track]['main'])
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()       
        

def selectionMenu(initObjects, menuList):
    global WINDOWWIDTH, WINDOWHEIGHT

    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]

    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    # This menu function is reusable. Books, units, and subsets can all be passed in as menuList.
       
    menuLabels = [assets.pokeFont(30).render(label, 1, assets.MAINTEXTCOLOR) for label in menuList]
    menuRects = [label.get_rect() for label in menuLabels]

    menuLeftBorder = WINDOWWIDTH/2 - 200
    menuTopBorder = WINDOWHEIGHT/2 - 130
    menuSpacing = 35

    selectionIcon = assets.teamImgs['turnIndicator']['B']
    selectionRect = selectionIcon.get_rect()
    overflowBorder = 170
    selection = 0
    selectionX = menuLeftBorder - 20 + overflowBorder * (selection // 8)
    

    for n in range(len(menuLabels)):
        overflowAmount = n // 8
        menuRects[n].topleft = (menuLeftBorder + (overflowBorder * overflowAmount), (menuTopBorder + menuSpacing * n) - (menuSpacing * 8) * overflowAmount)
        
        


    while True:
        checkForQuit()
        musicRepeat(menuTrack)
        DISPLAYSURF.fill(BKGCOLOR)
        DISPLAYSURF.blit(menuSurf,menuRect)

        
        for n in range(len(menuLabels)):
            DISPLAYSURF.blit(menuLabels[n], menuRects[n])

        newDim = None
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in (K_UP, K_DOWN, K_RETURN, K_KP_ENTER, K_ESCAPE):
                    assets.selectSound.play()

                if event.key == K_UP:
                    selection -= 1
                elif event.key == K_DOWN:
                    selection += 1
                elif event.key in (K_RETURN, K_KP_ENTER):
                    return menuList[selection]
                elif event.key == K_ESCAPE:
                    terminate()
            elif event.type == VIDEORESIZE:
                newDim = event.size
        
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
            menuLeftBorder = WINDOWWIDTH/2 - 200
            menuTopBorder = WINDOWHEIGHT/2 - 130
            menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            selectionX = menuLeftBorder - 20 + overflowBorder * (selection // 8)
            overflowBorder = 170
    

            for n in range(len(menuLabels)):
                overflowAmount = n // 8
                menuRects[n].topleft = (menuLeftBorder + (overflowBorder * overflowAmount), (menuTopBorder + menuSpacing * n) - (menuSpacing * 8) * overflowAmount)
        
       

        if selection < 0:
            selection = len(menuLabels)-1
        elif selection > len(menuLabels)-1:
            selection = 0
        

        selectionX = menuLeftBorder - 20 + overflowBorder * (selection // 8)
        selectionY = (menuTopBorder + menuSpacing * selection + 5) - (menuSpacing * 8) * (selection // 8)
        selectionRect.topleft = (selectionX, selectionY)
        DISPLAYSURF.blit(selectionIcon, selectionRect)

        pygame.display.update()

        FPSCLOCK.tick(FPS)


def catchWildPokemon(animationSpeed, targetSurf, bkgImg, teams, currentTeam, bonusPokemon, lastScoredPoint, shakeHowManyTimes, caught):

    global WINDOWWIDTH, WINDOWHEIGHT    

    musicRepeat('game')

    newDim = None
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            newDim = event.size
    if newDim:
        
        WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
        targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
   
    pokeBall = assets.bonusPokeBall

    pokeBall.ballType = lastScoredPoint
    pokeBall.state = 'closed'

    pokeBallImg = pokeBall.surface
    pokeBallRect = pokeBall.rect

    
    

    totalRotation = 100
    dropDistance = 200
    bounceHeight = 100

    if currentTeam.name == 'A':
        arcCentreX = (WINDOWWIDTH-1024)/2 + 500
        arcCentreY = (WINDOWHEIGHT-786)/2 + 600
        startingLocation = -100
        reverseMode = -1
    else:
        arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
        arcCentreY = (WINDOWHEIGHT-786)/2 + 600
        startingLocation = +100
        reverseMode = 1
    

    # Throw Arc Animation part
    assets.throwSound.play()
    for rotationStep in range(0, totalRotation, animationSpeed):
        musicRepeat('game')
        checkForQuit()
        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
            if currentTeam.name == 'A':
                arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                arcCentreY = (WINDOWHEIGHT-786)/2 + 600
            else:
                arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                arcCentreY = (WINDOWHEIGHT-786)/2 + 600
            bonusPokemon.rect.centerx = (WINDOWWIDTH/2)
            location = assets.getTrigoForArc(startingLocation + offset, distFromRotationalCentre, arcCentreX, arcCentreY)       
        
        offset = (throwTween(rotationStep / totalRotation) * 80)
        offset *= reverseMode
        drawBackground(bkgImg, targetSurf)
        distFromRotationalCentre = 300

        location = assets.getTrigoForArc(startingLocation + offset, distFromRotationalCentre, arcCentreX, arcCentreY)
        pokeBallRect.center = location
        targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)
        targetSurf.blit(pokeBallImg, pokeBallRect)

        currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    
    startingCentery = pokeBallRect.centery

    # Pokemon Goes Into Ball section will go here:

    assets.ballOpenSound.play()

    pokeBall.state = 'open'
    pokeBallImg = pokeBall.surface

    for animFrame in assets.bonusBallCatch:
        for time in range (0, 10):
            checkForQuit()
            newDim = None
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    newDim = event.size
            if newDim:
                WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )    
                if currentTeam.name == 'A':
                    arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                else:
                    arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600   
                bonusPokemon.rect.centerx = (WINDOWWIDTH/2)   
            if time == 1:
                musicRepeat('game')
                animFrameSurf = animFrame
                animFrameRect = animFrame.get_rect()
                animFrameRect.centerx = pokeBallRect.centerx
                animFrameRect.centery = pokeBallRect.centery

                drawBackground(bkgImg, targetSurf)
                
                targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)
                targetSurf.blit(pokeBallImg, pokeBallRect)
                targetSurf.blit(animFrameSurf, animFrameRect)

                currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)

                pygame.display.flip()
                FPSCLOCK.tick(FPS)





    
    
    # Drop and bounce animation
    pokeBall.state = 'closed'
    pokeBallImg = pokeBall.surface

    soundPlayed = False
    for dropStep in range(1, 100, animationSpeed):
        checkForQuit()
        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )    
            if currentTeam.name == 'A':
                arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                arcCentreY = (WINDOWHEIGHT-786)/2 + 600
            else:
                arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                arcCentreY = (WINDOWHEIGHT-786)/2 + 600  
            bonusPokemon.rect.centerx = (WINDOWWIDTH/2)    
        musicRepeat('game')
        offset =  dropDistance * (bounceTween(dropStep/100))

        drawBackground(bkgImg, targetSurf)
        
        pokeBallRect.centery = startingCentery + offset
        # print(pokeBallRect.centerx)
        targetSurf.blit(pokeBallImg, pokeBallRect)

        currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)
        if dropStep > 50 and soundPlayed == False:
            assets.ballBounceSound.play()
            soundPlayed = True
            
        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    
    # Waiting animation
    waitTime = random.randint(20, 30)
    for waitStep in range(1, waitTime):
        checkForQuit()
        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
            if currentTeam.name == 'A':
                arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                arcCentreY = (WINDOWHEIGHT-786)/2 + 600
            else:
                arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                arcCentreY = (WINDOWHEIGHT-786)/2 + 600
            bonusPokemon.rect.centerx = (WINDOWWIDTH/2)          
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

    # Wobble Animation
    jumpStartY = pokeBallRect.centery
    jumpHeight = 40
    
    for _ in range(shakeHowManyTimes):
        assets.ballShakeSound.play()
        musicRepeat('game')
        for jumpStep in range(1, 100, animationSpeed*6):

            checkForQuit()
            newDim = None
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    newDim = event.size
            if newDim:
                WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
                if currentTeam.name == 'A':
                    arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                else:
                    arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600 
                bonusPokemon.rect.centerx = (WINDOWWIDTH/2)         
            
            offset =  (jumpHeight * (wobbleTween(jumpStep/100)))
            drawBackground(bkgImg, targetSurf)
            
            pokeBallRect.centery = jumpStartY - offset
            targetSurf.blit(pokeBallImg, pokeBallRect)
            currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        for fallStep in range(1, 100, animationSpeed):

            checkForQuit()
            newDim = None
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    newDim = event.size
            if newDim:
                WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
                if currentTeam.name == 'A':
                    arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                else:
                    arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                bonusPokemon.rect.centerx = (WINDOWWIDTH/2)          
            musicRepeat('game')

            offset =  (jumpHeight * (bounceTween(fallStep/100))) - jumpHeight
            drawBackground(bkgImg, targetSurf)
            pokeBallRect.centery = jumpStartY + offset
            targetSurf.blit(pokeBallImg, pokeBallRect)

            currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        waitTime = random.randint(6, 20)
        for waitStep in range(1, waitTime):
            checkForQuit()
            newDim = None
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    newDim = event.size
            if newDim:
                WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
                if currentTeam.name == 'A':
                    arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                else:
                    arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                bonusPokemon.rect.centerx = (WINDOWWIDTH/2)          
            musicRepeat('game')
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        

    if not caught:

        assets.catchFailSound.play()

        for animFrame in assets.bonusBallCatch:
            for time in range (0, 10):
                musicRepeat('game')
                checkForQuit()
                newDim = None
                for event in pygame.event.get():
                    if event.type == VIDEORESIZE:
                        newDim = event.size
                if newDim:
                    WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                    targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
                    if currentTeam.name == 'A':
                        arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                        arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                    else:
                        arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                        arcCentreY = (WINDOWHEIGHT-786)/2 + 600  
                    bonusPokemon.rect.centerx = (WINDOWWIDTH/2)        
                if time == 1:
                    animFrameSurf = animFrame
                    animFrameRect = animFrame.get_rect()
                    animFrameRect.centerx = pokeBallRect.centerx
                    animFrameRect.centery = pokeBallRect.centery

                    drawBackground(bkgImg, targetSurf)
                    targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)
                    targetSurf.blit(animFrameSurf, animFrameRect)

                    currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)

                    pygame.display.flip()
                    FPSCLOCK.tick(FPS)

            pygame.display.flip()
            FPSCLOCK.tick(FPS)    


        for waitStep in range(1, 20):
            checkForQuit()
            newDim = None
            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    newDim = event.size
            if newDim:
                WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
                if currentTeam.name == 'A':
                    arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                else:
                    arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                    arcCentreY = (WINDOWHEIGHT-786)/2 + 600  
                bonusPokemon.rect.centerx = (WINDOWWIDTH/2)                    
            musicRepeat('game')
            drawBackground(bkgImg, targetSurf)
            currentTeam.drawTeamLabel(targetSurf, WINDOWWIDTH)
            targetSurf.blit(bonusPokemon.surface, bonusPokemon.rect)    
            pygame.display.flip()
            FPSCLOCK.tick(FPS)
        
        WAITING = True
        while WAITING:
            checkForQuit()

            musicRepeat('game')
            newDim = None
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key in (K_RETURN, K_KP_ENTER):
                        WAITING = False
    
                elif event.type == VIDEORESIZE:
                    newDim = event.size

                if newDim:
                    WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
                    targetSurf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0 )
                    if currentTeam.name == 'A':
                        arcCentreX = (WINDOWWIDTH-1024)/2 + 500
                        arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                    else:
                        arcCentreX = (WINDOWWIDTH-1024)/2 + (1024 - 500)
                        arcCentreY = (WINDOWHEIGHT-786)/2 + 600
                    bonusPokemon.rect.centerx = (WINDOWWIDTH/2)          
                else:
                    continue
                
            pygame.display.flip()
            FPSCLOCK.tick(FPS)


def rollToCatch(ballType):
    if ballType == 'U':
        return random.randint(0, 150)
    elif ballType == 'G':
        return random.randint(0, 120)
    else:
        return random.randint(0, 100)
    




def catchMechanic(ballType):
    catchChance = rollToCatch(ballType)

    # print(f'Ball type {ballType}, catch chance {catchChance}.')
    
    if catchChance > 85:
        return True, 3
    
    return False, random.randint(1, 3)


def bonusGame(teams, playingTeam, initObjects, bonusPokemon, theme):
    global WINDOWWIDTH, WINDOWHEIGHT
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]

    bkgImg = assets.backgrounds[theme]

    
    RUNNING = True
    caught = 'wait'

    while RUNNING:

        DISPLAYSURF.fill(BKGCOLOR)
        musicRepeat('game')

        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)


        
        if playingTeam.score != 0:
            
            lastScoredPoint = playingTeam.popPoint
            caught, shakeTimes = catchMechanic(lastScoredPoint)
            catchWildPokemon(throwAnimationSpeed, DISPLAYSURF, bkgImg, teams, playingTeam, bonusPokemon, lastScoredPoint, shakeTimes, caught)
            if caught:
                caught = 'yes'

        
        if playingTeam.score == 0:
            print('You ran out of pokeballs!')
            caught = 'no'

        return caught, playingTeam

    
def beginMusic(track):
    pygame.mixer.music.load(assets.music[track]['intro'])
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

def gameOver(whoWon, initObjects):
    global WINDOWWIDTH, WINDOWHEIGHT
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    beginMusic('victory')

    victoryMessageA = f'Congratulations, Team {whoWon.name}.'
    victoryMessageB = 'You win!'
    victorySurfA = assets.pokeFont(30).render(victoryMessageA, 1, MAINTEXTCOLOR)
    victoryRectA = victorySurfA.get_rect()
    victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    victorySurfB = assets.pokeFont(50).render(victoryMessageB, 0, MAINTEXTCOLOR)
    victoryRectB = victorySurfB.get_rect()
    victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
    
    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    while True:
        musicRepeat('victory')
        checkForQuit()
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(menuSurf, menuRect)
        DISPLAYSURF.blit(victorySurfA, victoryRectA)
        DISPLAYSURF.blit(victorySurfB, victoryRectB)

        newDim = None
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in (K_RETURN, K_KP_ENTER):
                    return
            elif event.type == VIDEORESIZE:
                newDim = event.size
        
        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)


        

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        



def bonusSuccess(whoWon, initObjects, bonusPokemon):
    global WINDOWWIDTH, WINDOWHEIGHT
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    

    victoryMessageA = f'Congratulations, Team {whoWon.name}.'
    victoryMessageB = 'You caught the pokemon!'
    victorySurfA = assets.pokeFont(30).render(victoryMessageA, 1, MAINTEXTCOLOR)
    victoryRectA = victorySurfA.get_rect()
    victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    victorySurfB = assets.pokeFont(30).render(victoryMessageB, 0, MAINTEXTCOLOR)
    victoryRectB = victorySurfB.get_rect()
    victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
    
    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)


    bonusPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/4)
    beginMusic('bonus')

    while True:
        musicRepeat('bonus')
        checkForQuit()
        
        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RETURN:
                    return
            elif event.type == QUIT:
                terminate()

        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
            victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
            menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            bonusPokemon.rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/4)


        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(menuSurf, menuRect)
        DISPLAYSURF.blit(bonusPokemon.surface, bonusPokemon.rect)
        DISPLAYSURF.blit(victorySurfA, victoryRectA)
        DISPLAYSURF.blit(victorySurfB, victoryRectB)

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

 



def bonusFail(initObjects):
    global WINDOWWIDTH, WINDOWHEIGHT
    FPSCLOCK = initObjects[0]
    DISPLAYSURF = initObjects[1]
    pygame.mixer.music.stop()

    victoryMessageA = f'Oh no!'
    victoryMessageB = 'The pokemon got away!'
    victorySurfA = assets.pokeFont(30).render(victoryMessageA, 1, MAINTEXTCOLOR)
    victoryRectA = victorySurfA.get_rect()
    victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    victorySurfB = assets.pokeFont(30).render(victoryMessageB, 0, MAINTEXTCOLOR)
    victoryRectB = victorySurfB.get_rect()
    victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
    
    menuSurf = assets.menuBKG
    menuRect = menuSurf.get_rect()
    menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    while True:
        
        checkForQuit()

        newDim = None
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                newDim = event.size
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RETURN:
                    return
            elif event.type == QUIT:
                terminate()

        if newDim:
            WINDOWWIDTH, WINDOWHEIGHT = newDim[0], newDim[1]
            DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
            victoryRectA.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            victoryRectB.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2+50)
            menuRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(menuSurf, menuRect)
        DISPLAYSURF.blit(victorySurfA, victoryRectA)
        DISPLAYSURF.blit(victorySurfB, victoryRectB)

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def drawBackground(image, targetSurf):
    global WINDOWWIDTH, WINDOWHEIGHT
    bkgRect = image.get_rect()
    bkgRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    targetSurf.fill(BLACK)
    targetSurf.blit(image, bkgRect)

def game():
    global WINDOWWIDTH, WINDOWHEIGHT
    WINDOWWIDTH = assets.WINDOWWIDTH
    WINDOWHEIGHT = assets.WINDOWHEIGHT
    FPSCLOCK = pygame.time.Clock()    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE, display=0)
    DISPLAYSURF.fill(BLACK)
    pygame.display.set_caption('The PokeBall Game')
    while True:
        randomPokemon = assets.getRandomPoke()
        pokemonTheme = randomPokemon[1]
    
        roundPokemon = assets.bonusPokemon(randomPokemon[0])

        initObjects = [FPSCLOCK, DISPLAYSURF, roundPokemon, pokemonTheme] # Makes sending this into main, other screens flippin EASY tho.

        sessionTeams = [assets.TeamB(), assets.TeamA()]
        random.shuffle(sessionTeams)      


        teamTurn = 0

        # Books: It gives a choice of any excel files in the folder, but not the ~$ temp file, and skips 'example' files.

        books = [os.path.splitext(title)[0] for title in os.listdir(quizPath) if os.path.splitext(title)[1] in ('.xlsx', '.XLSX') and '~$' not in os.path.splitext(title)[0] and os.path.splitext(title)[0] not in ('example', 'EXAMPLE')]
        beginMusic(menuTrack)
    
        chosenBook = selectionMenu(initObjects, books)
        sessionQuiz = assets.bookScheme(chosenBook)
    
        possibleUnits = sessionQuiz.getPossibleUnits()
        chosenUnit = selectionMenu(initObjects, possibleUnits)
        sessionQuiz.unit = chosenUnit

        subsets = sessionQuiz.getPossibleSubsets()
        chosenSubset = selectionMenu(initObjects, subsets)
        subsetIndex = sessionQuiz.possibleSubsets.index(chosenSubset) + 2 # Plus 2 because also excel uses indexing starting from 0 :|
        sessionQuiz.subset = subsetIndex

        sessionQuiz.getQuestions()

        # selectionList = [bookSelection, unitSelection, subSetSelection]
        beginMusic(pokemonTheme)

        winner = None

    
        # sessionTeams[0].addGreatPoint()
        # sessionTeams[0].addGreatPoint()  
        # sessionTeams[0].addGreatPoint()  
        # sessionTeams[0].addGreatPoint()  #Shortcut

        while True: # This loop locks the game into repeating rounds
        
            sessionTeams, teamTurn, pokemon = main(sessionTeams, initObjects, teamTurn, sessionQuiz)
            if pokemon.HPValue <= 0:
                if sessionTeams[0].score > sessionTeams[1].score:
                    winner = sessionTeams[0]
                elif sessionTeams[1].score > sessionTeams[0].score:
                    winner = sessionTeams[1]
                else:
                    winner = random.choice(sessionTeams)
            if winner:
                break

    
        gameOver(winner, initObjects) # Show the main Game Over Screen


        bonusPokemon = roundPokemon
        beginMusic('game')
        while True:
            musicRepeat('game')
            caught, bonusPlayer = bonusGame(sessionTeams, winner, initObjects, bonusPokemon, pokemonTheme)
            if caught == 'yes' and bonusPlayer:
                bonusSuccess(bonusPlayer, initObjects, bonusPokemon)
                break
            elif caught == 'no':
                assets.runAwaySound.play()
                bonusFail(initObjects)
                break
            winner = bonusPlayer
            

       


if __name__ == "__main__":
    game()