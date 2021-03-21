import pygame, os, math, random, openpyxl

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


WINDOWWIDTH = 1024
WINDOWHEIGHT = 786


# Colours
WHITE           =(255, 255, 255)
BLACK           =(  0,   0,   0)
GREEN           =(  0, 200,   0)
RED             =(255,   0,   0)
YELLOW          =(230, 240,  20)
CLEAR           =(  0,   0,   0,  0)


BKGCOLOR = WHITE
MAINTEXTCOLOR = BLACK

POINTBALLPOSX = 36
POINTBALLPOSY = 0


pygame.init()

def pokeFont(size=20):
    return pygame.font.SysFont('Minecraft', size)

pokeBallFont = pokeFont(20)


pokeBallPath = '.\\common\\assets\\pokeball'
print(os.getcwd())
print(pokeBallPath)

pokeballImgs = {
    'open' : pygame.image.load(os.path.join(pokeBallPath, 'pokeballOpen.png')),
    'closed' : pygame.image.load(os.path.join(pokeBallPath, 'pokeballClosed.png')),
}

bkgPath = r'.\common\assets\backgrounds'

backgrounds = {
    'grass' : pygame.image.load(os.path.join(bkgPath, 'grass.png')),
    'cave' : pygame.image.load(os.path.join(bkgPath, 'cave.png')),
    'dead' : pygame.image.load(os.path.join(bkgPath, 'dead.png')),
    'ice' : pygame.image.load(os.path.join(bkgPath, 'ice.png')),
    'legend' : pygame.image.load(os.path.join(bkgPath, 'legend.png')),
    'sand' : pygame.image.load(os.path.join(bkgPath, 'sand.png')),
    'water' : pygame.image.load(os.path.join(bkgPath, 'water.png')),
}



teamImagesPath = r'.\common\assets\team'
teamImgs = {
    'bar': {
        'A': pygame.image.load(os.path.join(teamImagesPath, 'teamBarA.png')),
        'B': pygame.image.load(os.path.join(teamImagesPath, 'teamBarB.png')),
    },
    'turnIndicator':
    {
        'A': pygame.image.load(os.path.join(teamImagesPath, 'turnIndicatorA.png')),
        'B': pygame.image.load(os.path.join(teamImagesPath, 'turnIndicatorB.png')),
    },
    'pokeScore': pygame.image.load(os.path.join(teamImagesPath, 'scorePokeBall.png')),
    'greatScore': pygame.image.load(os.path.join(teamImagesPath, 'scoreGreatBall.png')),
    'ultraScore': pygame.image.load(os.path.join(teamImagesPath, 'scoreUltraBall.png')),
}


menuPath = r'.\common\assets\menu'
menuBKG = pygame.image.load(os.path.join(menuPath, 'menuTable.png'))

soundPath = r'.\common\assets\sounds'

ballSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballSwirl.ogg'))
ballOpenSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballOpen.ogg'))
selectSound = pygame.mixer.Sound(os.path.join(soundPath, 'wink.ogg'))
ballBounceSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballBounceSound.ogg'))
ballShakeSound = pygame.mixer.Sound(os.path.join(soundPath, 'ballShakeSound.ogg'))
catchFailSound = pygame.mixer.Sound(os.path.join(soundPath, 'catchFailSound.ogg'))
throwSound = pygame.mixer.Sound(os.path.join(soundPath, 'throwSound.ogg'))
critHitSound = pygame.mixer.Sound(os.path.join(soundPath, 'critHit.ogg'))
runAwaySound = pygame.mixer.Sound(os.path.join(soundPath, 'runAway.ogg'))
nopeSound = pygame.mixer.Sound(os.path.join(soundPath, 'nope.ogg'))
hitSound = pygame.mixer.Sound(os.path.join(soundPath, 'hit.ogg'))



musicPath = r'.\common\assets\music'

music = {
    'grass' :
    {
        'intro' : os.path.join(musicPath, 'grassIntro.ogg'),
        'main' : os.path.join(musicPath, 'grassMain.ogg'),
    },
    'legend' :
    {
        'intro' : os.path.join(musicPath, 'ultimateIntro.ogg'),
        'main' : os.path.join(musicPath, 'ultimateMain.ogg'),
    },
    'cave' :
    {
        'intro' : os.path.join(musicPath, 'caveIntro.ogg'),
        'main' : os.path.join(musicPath, 'caveMain.ogg'),
    },
    'ice' :
    {
        'intro' : os.path.join(musicPath, 'caveIntro.ogg'),
        'main' : os.path.join(musicPath, 'caveMain.ogg'),
    },
    'dead' :
    {
        'intro' : os.path.join(musicPath, 'ghostIntro.ogg'),
        'main' : os.path.join(musicPath, 'ghostMain.ogg'),
    },
    'sand' :
    {
        'intro' : os.path.join(musicPath, 'gymIntro.ogg'),
        'main' : os.path.join(musicPath, 'gymMain.ogg'),
    },
    'water' :
    {
        'intro' : os.path.join(musicPath, 'waterIntro.ogg'),
        'main' : os.path.join(musicPath, 'waterMain.ogg'),
    },
    'menu' : {
        'intro' : os.path.join(musicPath, 'menuIntro.ogg'),
        'main' : os.path.join(musicPath, 'menuMain.ogg'),
    },
    'victory' : {
        'intro' : os.path.join(musicPath, 'mainVictoryIntro.ogg'),
        'main' : os.path.join(musicPath, 'mainVictoryMain.ogg'),
    },
    'game' : {
        'intro' : os.path.join(musicPath, 'gameCornerIntro.ogg'),
        'main' : os.path.join(musicPath, 'gameCornerMain.ogg'),
    },
    'bonus' : {
        'intro' : os.path.join(musicPath, 'bonusVictoryIntro.ogg'),
        'main' : os.path.join(musicPath, 'bonusVictoryMain.ogg'),
    }
}
# bonusPath = r'C:\Come On Python Games\resources\pokeBallGame\common\assets\bonus\pokes'
bonusPath = r'.\common\assets\bonus\allPokes'
pokemonDataSheet = r'.\common\assets\bonus\pokemonDataSheet.xlsx'
hpBarImg = pygame.image.load(r'.\common\assets\bonus\hpBar.png')



bonusPokemonImages = [os.path.join(bonusPath, pokeImageFile) for pokeImageFile in os.listdir(bonusPath) if os.path.splitext(pokeImageFile)[1] in ('.png', '.PNG')]


bonusBallPath = r'.\common\assets\bonus\ball'
bonusBallImages = {
    'P': {
        'closed': pygame.image.load(os.path.join(bonusBallPath, 'bonusPokeClosed.png')),
        'open': pygame.image.load(os.path.join(bonusBallPath, 'bonusPokeOpen.png')),
    },
    'G': {
        'closed': pygame.image.load(os.path.join(bonusBallPath, 'bonusGreatClosed.png')),
        'open': pygame.image.load(os.path.join(bonusBallPath, 'bonusGreatOpen.png')),
    },
    'U': {
        'closed': pygame.image.load(os.path.join(bonusBallPath, 'bonusUltraClosed.png')),
        'open': pygame.image.load(os.path.join(bonusBallPath, 'bonusUltraOpen.png')),
    },
}
bonusCatchPath = r'.\common\assets\bonus\catchAnim'
bonusBallCatch = [pygame.image.load(os.path.join(bonusCatchPath, imageFile)) for imageFile in os.listdir(bonusCatchPath) if os.path.splitext(imageFile)[1] in ('.png', '.PNG')]

class bonusBall():
    def __init__(self):
        self.__Type = None
        self.dict = bonusBallImages
        self.__state = 'closed'
    
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, setState):
        self.__state = setState

    @property
    def ballType(self):
        return self.__type

    @ballType.setter
    def ballType(self, setType):
        self.__type = setType
    
    @property
    def surface(self):
        image = self.dict[self.ballType][self.state]
        newSurf = pygame.Surface((40, 60), pygame.SRCALPHA)
        newSurf.blit(image, (0, 0))
        return newSurf


    @property
    def rect(self):
        return self.surface.get_rect()        

bonusPokeBall = bonusBall()



def getRandomPoke(pokemonList=pokemonDataSheet):
    wb = openpyxl.load_workbook(pokemonDataSheet)

    sheet = wb.active


    randomPokeRow = random.randint(1, 384)

    pokemonName = sheet.cell(column=1, row=randomPokeRow).value
    print(f'You will battle {pokemonName}!')
    pokemonThemeScheme = sheet.cell(column=2, row=randomPokeRow).value

    pokemonImagePath = os.path.join(bonusPath, f'{pokemonName}_sprite.png')

    return pokemonImagePath, pokemonThemeScheme




    return random.choice(imageList)


class bonusPokemon():
    def __init__(self, pokeImagePath, HPStat=7):
        self.path = pokeImagePath
        self.rect = self.makeRect()
        self.__HPValue = HPStat
        self.maxHP = HPStat

    @property
    def surface(self):
        image = pygame.image.load(self.path)
        return image

    @property
    def HPValue(self):
        return self.__HPValue

    @HPValue.setter
    def HPValue(self, setValue):
        if setValue >= 0:
            self.__HPValue = setValue
        else:
            self.__HPValue = 0

    def makeRect(self):
        return self.surface.get_rect()

    

    def drawHP(self, targetSurf, xPos, yPos):
        HPBarX = xPos/2
        HPBarY = yPos/2 +80
        HPSurf = pygame.Surface((159, 15), pygame.SRCALPHA)
        HPRect = HPSurf.get_rect()
        HPRect.center = (HPBarX, HPBarY)
        HPBarBkg = pygame.Surface((117, 5))
        HPBarBkg.fill(WHITE)
        HPSurf.blit(HPBarBkg, (39, 5))

        if self.HPValue > 0:
            HPBarFill = pygame.Surface((((120 / self.maxHP) * self.HPValue) , 9))
            color = BLACK
            if self.HPValue >= (self.maxHP//2):
                color = GREEN
            elif self.HPValue >=(self.maxHP//3):
                color = YELLOW
            elif self.HPValue < 3:
                color = RED
            HPBarFill.fill(color)
            HPSurf.blit(HPBarFill, (38, 5))

        HPSurf.blit(hpBarImg, (0, 0))
        
        targetSurf.blit(HPSurf, HPRect)
        



class pokeball():
    def __init__(self, pathDict, message=None, state=None):
        self.path = pathDict
        self.__state = state
        
        self.surfaceWidth = 180
        self.surfaceHeight = 90
        self.__surface = pygame.Surface((self.surfaceWidth, self.surfaceHeight), pygame.SRCALPHA)

        self.__message = message

        self.closedBall = self.drawClosedBall()
        self.openBall = self.drawOpenBall()
        self.rect = self.makeRect()

        


    # State Setter/Getter
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, setState):
        self.__state = setState

    # Message Setter/Getter
    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, setMessage):
        self.__message = setMessage
        self.openBall = self.drawOpenBall()
        self.closedBall = self.drawClosedBall()
        


    def drawClosedBall(self):
        # print("DEBUG: Pokeball: draw closed image")

        closedBallSurf = pygame.Surface((self.surfaceWidth, self.surfaceHeight), pygame.SRCALPHA)
        closedBallSurf.fill(CLEAR)

        closedBall = self.path['closed'].copy()

        closedBallRect = closedBall.get_rect()
        closedBallRect.center = (self.surfaceWidth/2, self.surfaceHeight/2)
        closedBallSurf.blit(closedBall, closedBallRect)

        return closedBallSurf

    def drawOpenBall(self):
        # print("DEBUG: Pokeball: draw open image")

        openBallSurf = pygame.Surface((self.surfaceWidth, self.surfaceHeight), pygame.SRCALPHA)
        openBallSurf.fill(CLEAR)

        text = pokeBallFont.render(self.message, 1, MAINTEXTCOLOR)
        messageRect = text.get_rect()
        messageRect.center = (self.surfaceWidth/2, 50)

        openBall = self.path['open'].copy()
        openBallRect = openBall.get_rect()
        openBallRect.center = (self.surfaceWidth/2, self.surfaceHeight/2)

        openBallSurf.blit(openBall, openBallRect)
        openBallSurf.blit(text, messageRect)

        return openBallSurf


    @property
    def surface(self):

        if self.state == 'closed':
            # Set result to be closed surface
            self.__surface = self.closedBall
            return self.__surface

        else:
            self.__surface = self.openBall
            return self.__surface


    def makeRect(self):
        return self.surface.get_rect()

class question():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer




class Menubutton():
    def __init__(self, path, series, gameType, state='up', surface=None):
        self.path = path
        self.__state = state
        self.series = series
        self.gameType = gameType
        self.__surface = surface
        self.rect = self.makeRect()
        
        # self.surface = self.path[self.state]
        # self.rect = self.surface.get_rect()




    @property
    def state(self):
        return self.__state


    @state.setter
    def state(self, setState):
        self.__state = setState

    @property
    def surface(self):
        return self.path[self.state]

    def makeRect(self):
        return self.surface.get_rect()




class Team():
    def __init__(self, name):
        self.name = name
        self.scoreList = [] # Contains a letter for each type of point
        
        self.images = teamImgs
        self.isTurn = False

        self.barImg = self.images['bar'][self.name]

        self.turnIndicator = self.images['turnIndicator'][self.name]
        self.turnIndicatorX = 20 + 100
        self.turnIndicatorY = WINDOWHEIGHT - 80

        self.teamSurf = pygame.Surface((154, 70), pygame.SRCALPHA)
        self.teamRect = self.teamSurf.get_rect()
        self.teamRectY = WINDOWHEIGHT - 120
        self.teamRectX = 20
        

        self.pointSurf = pygame.Surface((108,18), pygame.SRCALPHA)
        self.pointRect = self.pointSurf.get_rect()
        self.pointSpacing = 0

        self.labelText = f'Team {self.name}'



    # State Setter/Getter
    @property
    def score(self):
        scoreVal = 0
        for ball in self.scoreList:
            if ball == 'U':
                scoreVal += 3
            elif ball == 'G':
                scoreVal += 2
            elif ball == 'P':
                scoreVal += 1
        return scoreVal
    
        
    @property
    def hasWon(self):
        if self.score >= 4:
            return True
        else:
            return False

    def addPoint(self):
        self.scoreList.append('P')

    def addGreatPoint(self):
        self.scoreList.append('G')
    
    def addUltraPoint(self):
        self.scoreList.append('U')

    @property
    def popPoint(self):
        scoreList = self.scoreList
        lastPoint = scoreList.pop()
        self.scoreList = scoreList
        # print(self.scoreList)
        return lastPoint

    

    def drawTeamLabel(self, targetSurf, xPos):

        ballX = 0
        ballY = 0
        self.teamSurf = pygame.Surface((154, 70), pygame.SRCALPHA)
        self.teamSurf.blit(self.barImg, (0, 0))
        self.pointSurf = pygame.Surface((108,18), pygame.SRCALPHA)
        self.pointSurf.fill(WHITE)
        self.pointSurf.fill((0,0,0,0))
        for ball in self.scoreList:
            if ball == "P":
                ballImage = self.images['pokeScore']
            elif ball == "G":
                ballImage = self.images['greatScore']
            elif ball == "U":
                ballImage = self.images['ultraScore']
                 # Calculate how many balls to show
            self.pointSurf.blit(ballImage, (ballX, ballY))
            ballX += 18

        self.pointRect.topleft = (self.pointSpacing, 0)
        self.teamSurf.blit(self.pointSurf, self.pointRect) # Add balls to main surface

        teamLabel = pokeFont().render(self.labelText, 1, MAINTEXTCOLOR)
        teamLabelRect = teamLabel.get_rect()
        teamLabelRect.topleft = ((20, 40))
        self.teamSurf.blit(teamLabel, teamLabelRect)

        self.teamRect.topleft = ((xPos-1024)/2 + self.teamRectX, self.teamRectY)
        targetSurf.blit(self.teamSurf, self.teamRect)

    def drawTurnIndicator(self, targetSurf, xPos):
        turnIndicatorRect = self.turnIndicator.get_rect()
        turnIndicatorRect.topleft = ((xPos-1024)/2 + self.turnIndicatorX, self.turnIndicatorY)
        targetSurf.blit(self.turnIndicator, turnIndicatorRect)         
    

    
class TeamA(Team):
    def __init__(self):
        super().__init__(name='A')

        self.barImg = self.images['bar']['A']
        self.teamRectX = 20
        self.pointSpacing = 20
        


class TeamB(Team):
    def __init__(self):
        super().__init__(name='B')

        self.barImg = self.images['bar']['B']
        self.teamRectX = 1024-174
        self.turnIndicatorX = 1024-174
        self.pointSpacing = 8


        def drawTeamLabel(self, targetSurf, xPos):

            ballX = 0
            ballY = 0
            self.teamSurf = pygame.Surface((154, 70), pygame.SRCALPHA)
            self.teamSurf.blit(self.barImg, (0, 0))
            self.pointSurf = pygame.Surface((108,18), pygame.SRCALPHA)
            self.pointSurf.fill(WHITE)
            self.pointSurf.fill((0,0,0,0))
            for ball in self.scoreList:
                if ball == "P":
                    ballImage = self.images['pokeScore']
                elif ball == "G":
                    ballImage = self.images['greatScore']
                elif ball == "U":
                    ballImage = self.images['ultraScore']
                    # Calculate how many balls to show
                self.pointSurf.blit(ballImage, (ballX, ballY))
                ballX += 18

            self.pointRect.topleft = (self.pointSpacing, 0)
            self.teamSurf.blit(self.pointSurf, self.pointRect) # Add balls to main surface

            teamLabel = pokeFont().render(self.labelText, 1, MAINTEXTCOLOR)
            teamLabelRect = teamLabel.get_rect()
            teamLabelRect.topleft = ((20, 40))
            self.teamSurf.blit(teamLabel, teamLabelRect)

            self.teamRect.topleft = ((xPos-1024)/2 + self.teamRectX , self.teamRectY)
            targetSurf.blit(self.teamSurf, self.teamRect)
        

class bookScheme():
    def __init__(self, book, path=None):
        self.book = book
        self.__path = path
        self.__unit = None
        self.__subset = None
        self.__possibleSubsets = None
        self.__flashcardRange = None
        self.__questionFormat = None
        self.__questions = None
    
    @property
    def path(self):
        return os.path.join(r'.\quiz', f'{self.book}.xlsx')

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, valueToSetAsUnit):
        self.__unit = valueToSetAsUnit
    
    @property
    def subset(self):
        return self.__subset
    
    @subset.setter
    def subset(self, valueToSetAsSubset):
        self.__subset = valueToSetAsSubset

    @property
    def possibleSubsets(self):
        return self.__possibleSubsets
    
    @possibleSubsets.setter
    def possibleSubsets(self, valueToSetAsPossibleSubsets):
        self.__possibleSubsets = valueToSetAsPossibleSubsets

    @property
    def flashcardRange(self):
        return self.__flashcardRange
    
    @flashcardRange.setter
    def flashcardRange(self, valueToSetAsFlashcardRange):
        self.__flashcardRange = valueToSetAsFlashcardRange

    @property
    def questionFormat(self):
        return self.__questionFormat
    
    @questionFormat.setter
    def questionFormat(self, valueToSetAsQuestionFormat):
        self.__questionFormat = valueToSetAsQuestionFormat

    @property
    def questions(self):
        return self.__questions
    
    @questions.setter
    def questions(self, valueToSetAsQuestions):
        self.__questions = valueToSetAsQuestions
    



    def getPossibleUnits(self):
        wb = openpyxl.load_workbook(self.path)
        unitSheetsInBook = wb.get_sheet_names()
        return unitSheetsInBook

    def getPossibleSubsets(self):
        wb = openpyxl.load_workbook(self.path)
        sheet = wb[self.unit]

        subsetLabelRow = 1
        subsetLabelStartingColumn = 2
        listOfSubsets = []
        while True:
            cellContents = sheet.cell(subsetLabelRow, subsetLabelStartingColumn).value
            if cellContents:
                listOfSubsets.append(str(cellContents))
                subsetLabelStartingColumn += 1
            else:
                break
        self.possibleSubsets = listOfSubsets
        # print(listOfSubsets)
        return listOfSubsets

    def getScheme(self):
        wb = openpyxl.load_workbook(self.path)
        sheet = wb[self.unit]

        subsetColumnLocation = int(self.subset)
        # print(f'Subset location: {subsetColumnLocation}')
        flashcardRangeCell = sheet.cell(2, subsetColumnLocation).value
        questionTypeCell = sheet.cell(3, subsetColumnLocation).value

        if not flashcardRangeCell:
            flashcardRangeCell = 'ALL'

        self.flashcardRange = flashcardRangeCell
        self.questionFormat = questionTypeCell

        print(f"FLASHCARD RANGE IS {self.flashcardRange}")

        return flashcardRangeCell,  questionTypeCell
        
    def getQuestions(self):
        
        self.getScheme()
        # print(self.questionFormat)
        if self.questionFormat == None:
            return None
        elif self.questionFormat in ('be', 'BE', 'Be'):
            self.questions = [
                'Is she...?',
                'Is he...?',
                'Are they...?',
                'Are you...?',
                'Is Tom...?',
                'Is Ellie...?'
            ]
        elif self.questionFormat in ('do', 'DO', 'Do'):
            self.questions = [
                'Does she...?',
                'Does he...?',
                'Do they...?',
                'Do you...?',
                'Does Tom...?',
                'Does Ellie...?'
            ]
        else:
            wb = openpyxl.load_workbook(self.path)
            sheet = wb[self.unit]
            subsetColumnLocation = int(self.subset)
            questionRangeCell = 4

            questionsLoadedFromExcelSheet = []
            while True:
                currentQuestionCellContents = sheet.cell(column=subsetColumnLocation, row=questionRangeCell).value
                if currentQuestionCellContents:
                    questionsLoadedFromExcelSheet.append(currentQuestionCellContents)
                    questionRangeCell += 1
                else:
                    break
            if len(questionsLoadedFromExcelSheet) < 1:
                questionsLoadedFromExcelSheet.append('NO QUESTIONS LOADED')
            
            self.questions = questionsLoadedFromExcelSheet
        # print(self.questions)
        return self.questions
            
        


# Trig Functions
def degToRadian(deg):
    return deg * math.pi / 180

def getXcoord(deg, hypo):
    # The sin of the degree is equal to ANS divided by HYPO
    # Get sin of degree.
    # Multiply this number by the HYPO
    # This will be the length co-ord
    radA = degToRadian(deg)
    sinA = math.sin(radA)
    xLength = sinA * hypo

    return xLength

def getYcoord(deg, hypo):
    # The same but wit COSINE I think.
    radA = degToRadian(deg)
    cosA = math.cos(radA)
    yLength = cosA * hypo
    return yLength

def getTrigoXY(deg, hypo):
    x = getXcoord(deg, hypo)
    y = getYcoord(deg, hypo)
    intx = int(x)
    inty = int(y)
    return (intx, inty)

def getTrigoFromCenter(deg, hypo, width, height):
    trigX, trigY = getTrigoXY(deg, hypo)

    return (trigX + width, trigY + height)

def getTrigoForArc(deg, hypo, centreX, centreY):
    trigX, trigY = getTrigoXY(deg, hypo)

    return (trigX + centreX, trigY+centreY)

