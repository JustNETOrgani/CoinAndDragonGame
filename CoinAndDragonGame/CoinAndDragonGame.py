#   Pygame imports begins.

import pygame
from pygame.locals import *
from sys import exit
import time
import random
import os

#   All imports end here.

# Pygame initialization
pygame.init()

#   Main Pygame configurations begin here. 

# Set the height and width of the screen
display_width   = 756
display_height  = 590

# The Game's window.
gameDisplay = pygame.display.set_mode((display_width,display_height + 40),0,32)

#   Changing the icon for the game.
#   Loading the game's new icon image. 

myGameIcon = pygame.image.load('gIcon.jpg')

#   Setting the game's icon image on the Display Window. 
pygame.display.set_icon(myGameIcon)

# Title for the game.
pygame.display.set_caption("Mine gold or Go Home Game")

# The game's Clock speed and Time settings. 
clock = pygame.time.Clock()

actualSec = clock.tick(60) / 6000

#   Main Pygame configurations begin here. 


# Colours and Detectors to be used begin.

black               = (0,0,0)
white               = (255,255,255)
red                 = (140,0,0)
green               = (0,140,0)
blue                = (0,0,140)
othercol_1          = (140,120,25)
homeColor           = (50,148,164)
yellow              = (120,120,0)
increased_red       = (255,0,0)
increased_green     = (0,255,0)
increased_blue      = (0,0,255)
increased_yellow    = (220,220,0)


# Detection issues
MapCoin     =   False
coinCounter =   0
coinCounterChange = 0
home        =   False
gameExit    =   False
pause      =    False

# Colours and detectors used end. 

#   Special Player Sprite begin.

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        #self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('player.jpg').convert_alpha()
        #self.image.set_colorkey(white)
        self.rect = self.image.get_rect()

#   Special Player Sprite ends here.


# Tilemap to be used in the game begins here.

# Use list comprehension technique.
DRAGON  =   0
WATER   =   1
COIN    =   2
GRASS   =   3
HOME    =   4

resources = [ DRAGON, COIN, WATER, GRASS, HOME ]  

#   If idea of probability in distributing the tiles is not Ok, this can be used -- Which does not change.
#   Makes the game too predictable.    

#tilemap = [
#            [GRASS, WATER, COIN, DRAGON, WATER, GRASS, DRAGON, COIN, HOME],
#            [DRAGON, COIN, GRASS, DRAGON, GRASS, COIN, DRAGON, COIN, DRAGON],
#            [GRASS, GRASS, COIN, DRAGON, WATER, GRASS, WATER, WATER, GRASS],
#            [GRASS, WATER, COIN, GRASS, COIN, GRASS, DRAGON, COIN, WATER],
#            [DRAGON, COIN, WATER, DRAGON, GRASS, COIN, WATER, GRASS, DRAGON],
#            [GRASS, WATER, COIN, GRASS, WATER, GRASS, WATER, GRASS, COIN],
#    ]

# Dimensions of the tile and subsequently the tilemap.

TILESIZE    =   84
MAPWIDTH    =   9
MAPHEIGHT   =   6


tilemap = [[GRASS for w in range (MAPWIDTH)] for h in range(MAPHEIGHT)]


# Dictionary to link tiles to colours begin. Colours are preferred? 
colours = {
            #GRASS  :   green,
            #COIN    :   othercol_1,
            #WATER   :   blue,
            #DRAGON  :   red,
            #HOME    :   homeColor
            }

# Dictionary of tile images to be implemented begins.
textures = {
            GRASS  :   pygame.image.load('grass.jpg'),
            COIN    :   pygame.image.load('coin.jpg'),
            WATER   :   pygame.image.load('water.jpg'),
            DRAGON  :   pygame.image.load('dragon.jpg'),
            HOME    :   pygame.image.load('home.jpg')
            }

# Dictionary of pictures to be used ends.

def tmap():
    for row in range (MAPHEIGHT):
        for column in range (MAPWIDTH):
            # Random number selection
            randomNumber = random.randint(0, 100)
            # If zero then the tile is HOME
            if randomNumber ==1 or randomNumber ==2 or randomNumber ==10:
                tile = HOME
            # Coin if 1 or 2
            elif randomNumber == 2 or randomNumber == 3:
                tile = COIN
            # Water if greater/equal to 3 but less/equal to 6
            elif randomNumber ==4 or randomNumber ==6:
                tile = WATER
            # Dragon if greater/equal to 7 but less/equal to 9.
            elif randomNumber >=7 and randomNumber ==11:
                tile = DRAGON
            else:
                tile = GRASS
            # Position setting in the tilemap accordingly. 
            tilemap[row][column] = tile


# Inventory of items on the tilemap
inventory = {
            GRASS   :   0,
            COIN    :   0,
            WATER   :   0,
            DRAGON  :   0,
            HOME    :   0
             }
INVENTORYFONT = pygame.font.Font('freesansbold.ttf', 35)

#   Tilemap ends. 


#   Player attributes begin.

# Size of the player. 
player_width = 50
player_height =78

# Image for the player
playerImg = pygame.image.load('player.png').convert_alpha()
rectPlayer = playerImg.get_rect()

# Initial position of the player and position tracker.
dx = 0
dy = 0
rectPlayer.x = 690
rectPlayer.y = 504

#   Player attributes end.

#   Declaration of various methods for the game begins. 

def showPlayer():
    gameDisplay.blit(playerImg, (rectPlayer.x, rectPlayer.y))

#   For all text objects in the game to handle kind of text and font styles. 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#   To be used to pass crash events based on position at which the player crashed. 
def msgDisplay(text):
    largeText = pygame.font.Font('freesansbold.ttf',35)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(0.2)
    theGameLoop.gameloop()

#   To be called when the player attempts to pick coin/gold from grass to educate users about illigal mining.
def illegalMining(text):
    largeText = pygame.font.Font('freesansbold.ttf',42)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1.2)
    theGameLoop.gameloop()

#   To be called when the player steps in water. 
def waterTile(text):
    largeText = pygame.font.Font('freesansbold.ttf',43)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1.3)
    theGameLoop.gameloop()

#      To be called when the player is caught by a dragon.
def dragonTile(text):
    largeText = pygame.font.Font('freesansbold.ttf',41)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1.3)
    theGameLoop.gameloop()

#   To be called when the player gets home. 
def unlockHome(text):
    largeText = pygame.font.Font('freesansbold.ttf',45)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2.5)
    #pygame.quit()
    theGameLoop.gameloop()

def gameOverDisplay(text):
    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width*0.5),(display_height*0.5))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2.5)

#   Various button features to be displayed when the game starts or pauses. 
def button(msg,x,y,w,h,ic,ac,action=None):
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)   ----  This is to verify if click event can be tracked. 

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None: 
            if action == 'play':
                mainGame()

            elif action == 'quit':
                 quiteGame()
            elif action == 'restart':
                game_intro()
                

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font('freesansbold.ttf',20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
 

# Quiting the game.
def quiteGame():
    pygame.quit()
    quit()


# Game introduction phase to implement Start, Pause, Replay etc. 
def game_intro():
    SoundCorner.gameSound()
    intro = False

    while not intro:
        for event in pygame.event.get():
            #print(event)    ----  This is to verify if event is being tracked. 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
                
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',45)
        TextSurf, TextRect = text_objects("Mine gold or Go Home Game.", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        
        button("Start",150,450,100,50,green,increased_green,'play')
        button("Quit",550,450,100,50,red,increased_red,'quit')

        tmap()

        rectPlayer.x = 690
        rectPlayer.y = 504
        pygame.display.update()
        clock.tick(15)

#   To keep track of coins or Points.

def countCoinsPicked(coinCounter):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Total Coins Picked: "+ str(coinCounter), True, red)
    gameDisplay.blit(text,(460,589))



# Now creating a pauseGame functionality to the game. 

def paused():    # pauseGame method. 

    #pause      =   True
    pygame.mixer.music.pause()

    largeText = pygame.font.Font('freesansbold.ttf',90)
    TextSurf, TextRect = text_objects("Game Paused.", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while paused:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #   This can be run if screen needs to be made White again hiding the tiles and player.   
              
        #gameDisplay.fill(white)   
        

        #   On pause, more button functionality can be added to this button group. 
        button("Continue",150,450,100,50,green,increased_green,'play')

        button("Restart",350,450,100,50,yellow,increased_yellow,'restart')

        button("Quit",550,450,100,50,red,increased_red,'quit')
        

        pygame.display.update()
        clock.tick(16)  

#   Now creating unpause functionality to the game. 
def unpause():
    global pause

    pygame.mixer.music.play(-1)

    pause = False


#   Declaration of various methods for the game end here. 

#   Class Declarations begin here. 

class gameOverTime:                      # To be referenced when countdown timer is 00:00 
    def gameOver():
        pygame.mixer.music.stop()
        SoundCorner.gameIsOverSound()
        gameOverDisplay('Time up... Game Over.')
        

class homeSweet:                      # To be updated later for replay game functionality. 
    def homeSweetHome():
        unlockHome('Congratulations. You are Home.') 

class coinMining:
    def mineGold():
         illegalMining('Illegal gold mining. Coins deducted.')

  
class waterPassing:
    def steppedInWater():
         waterTile('Stepped in Water. Coins deducted.')

class dragonPassing:
    def insideDragon():
         dragonTile('Caught by Dragon. Coins deducted.')

class SoundCorner:

    def crashSound(self):
        playSoundCrash = pygame.mixer.Sound("chime.wav")
        pygame.mixer.Sound.play(playSoundCrash)
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)

    def gameSound():
        pygame.mixer.music.load('gSound.wav')
        pygame.mixer.music.play(-1) # This will make the game sound play throughout the game. 
    
    def gameIsOverSound():
        pygame.mixer.music.load('gOverSound.wav')
        pygame.mixer.music.play(3) # This will make the game sound play for three seconds.

    
class crashEvents(SoundCorner):
    def crashRight():
        msgDisplay('Crashed at the right. Come back.')
        c = crashEvents()
        c.crashSound()

    def crashLeft():
        msgDisplay('Crashed at the left. Come back.')
        c = crashEvents()
        c.crashSound()

    def crashTop():
        msgDisplay('Crashed at the top. Come down.')
        c = crashEvents()
        c.crashSound()

    def crashDown():
        msgDisplay('Crashed at the bottom. Come up.')
        c = crashEvents()
        c.crashSound()

class theGameLoop:

    def gameloop():

        global pause
        
        #   Calling the game sound to be activated.
        SoundCorner.gameSound() 

        playerposition_x = 690
        playerposition_y = 504

        countCoinsPicked(coinCounter)
       
        gameExit    =   False
    
#   Class Declarations begin end. 

#   The main method to run the game now begins. 
   
def mainGame():
    #   Main game globals begin.

    dx = 0      #   Track change in x-axis Calculus.
    dy = 0      #   Track change in y-axis as used in Calculus.
    TilemapLowestPoint = 420
    TilemapRightmostPoint = 672
    coinCounter =   0
    coinCounterChange = 0  
    gameExit    =   False
    
    frame_count = 0      
    frame_rate = 60
    start_time = 10   # This sets the time the game will last. 
    sumTime = 0       # This would be used to check when count down reaches zero to halt the game. 

    #   Main game globals end here.

    while not gameExit:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dx = 84
                if event.key == pygame.K_LEFT:
                    dx = -84
                if event.key == pygame.K_UP:
                    dy = -84
                if event.key == pygame.K_DOWN:
                    dy = 84
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_SPACE:

                    # Check tile player is standing on.
                    
                    #for row in range (MAPHEIGHT):
                        #for column in range (MAPWIDTH):

                    if tilemap[round(rectPlayer.y/TILESIZE)][round(rectPlayer.x/TILESIZE)]== COIN:
                        # Increase coincounter 
                        coinCounterChange =10
                        coinCounter += coinCounterChange
                        # Change the current coin tile to grass. 
                        tilemap[round(rectPlayer.y/TILESIZE)][round(rectPlayer.x/TILESIZE)] = GRASS
                            
                    elif tilemap[round(rectPlayer.y/TILESIZE)][round(rectPlayer.x/TILESIZE)] == GRASS:
                        coinCounterChange =-10
                        # Display "Illegal gold mining" message.
                        coinMining.mineGold()
                        coinCounter += coinCounterChange

                    elif tilemap[round(rectPlayer.y/TILESIZE)][round(rectPlayer.x/TILESIZE)] == HOME:
                        # Display that player has reached home as well as total coins picked. 
                        homeSweet.homeSweetHome()
                        game_intro()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    dx = 0
                    dy = 0


            #   When player steps into Water and Dragon tiles, points should be deducted.
            #   To be implemented automatically. 
            #   Possibly displaying messages to prompt player of such occurrences. 
            
            #   First checking to be sure player is on the tilemap to start detection processes. 
            if rectPlayer.y <= TilemapLowestPoint and rectPlayer.x <= TilemapRightmostPoint: 
                
                        #   Constantly checking to see if player is on Water Tile. 

                        if tilemap[round(rectPlayer.y/TILESIZE)][round(rectPlayer.x/TILESIZE)]== WATER:
                            coinCounterChange =-10
                            #   Display message.
                            waterPassing.steppedInWater()
                            #   Update coin counter.
                            coinCounter += coinCounterChange
                            inventory[WATER]+=1

                        #   Now checking for Dragon Tile.

                        if  tilemap[round(rectPlayer.y/TILESIZE)][round(rectPlayer.x/TILESIZE)] == DRAGON:
                            coinCounterChange =-10
                            #   Display message.
                            dragonPassing.insideDragon()
                            #   update coin counter.
                            coinCounter += coinCounterChange
                            inventory[DRAGON]+=1

                    # Updating the coin and Inventory counter accordingly to be displayed later. 
            else:   
                coinCounterChange =0
                coinCounter += coinCounterChange


        rectPlayer.x += dx
        rectPlayer.y += dy
        
        gameDisplay.fill(white)
          
        
        if rectPlayer.x > display_width - rectPlayer.width:
            crashEvents.crashRight()    
        if rectPlayer.x < 0:
            crashEvents.crashLeft() 
        if rectPlayer.y < 0:  
            crashEvents.crashTop() 
        if rectPlayer.y > display_height - rectPlayer.height:
            crashEvents.crashDown() 


        for row in range(MAPHEIGHT):        # Looping through the rows.
            for column in range(MAPWIDTH):  # Looping through the columns.

                #pygame.draw.rect(gameDisplay, textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE,TILESIZE,TILESIZE))  # If colours are to be used next time. 
                
                gameDisplay.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE)) # For images to be used for the map or tiles. 
                
                showPlayer()
        
        locationOnScreen = 1
        
        for item in resources:
            # Add corresponding images
            gameDisplay.blit(textures[item], (locationOnScreen, MAPHEIGHT*TILESIZE+20))
            locationOnScreen += 30
            # Add text showing total number in inventory.
            textObj = INVENTORYFONT.render(str(inventory[item]), True, white, black)
            gameDisplay.blit(textObj,(locationOnScreen, MAPHEIGHT*TILESIZE + 20))
            locationOnScreen += 50


        
        total_seconds = start_time - (frame_count // frame_rate)
        if  total_seconds < 0:
            total_seconds = 0
 
        # Dividing by sixty to get time in minutes.
        minutes = total_seconds // 60
 
        # Using modulus to derive time in seconds.
        seconds = total_seconds % 60

        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        font = pygame.font.Font('freesansbold.ttf', 25)
        clockText = font.render(output_string, True, (blue))
        gameDisplay.blit(clockText,(460,550))

        frame_count += 1
        if minutes + seconds == 0:
            #gameExit = True
            gameOverTime.gameOver()
            game_intro()
        
        # Displaying the Coins accumulated. 
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render("Total Coins Picked: "+ str(coinCounter), True, red)
        gameDisplay.blit(text,(460,589))
             
        
        pygame.display.update()
        
        clock.tick(20)

SoundCorner.gameSound() 
game_intro()
theGameLoop.gameloop()
pygame.quit()
quit()

#   The main method to run the game ends here. 