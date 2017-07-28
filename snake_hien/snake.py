import pygame
from pygame.locals import *
import random

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
displayWidth = 800
displayHeight = 600
blockSize = 10

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

# DISPLAY TEXT
fontLarge = pygame.font.SysFont(None, 60)
fontSmall = pygame.font.SysFont(None, 25)
def message_display(size, msg, colour, x, y):
    if size == "large":
        text = fontLarge.render(msg, True, colour)
    elif size == "small":
        text = fontSmall.render(msg, True, colour)
    gameDisplay.blit(text, [x, y])

def generateFood():
    foodX = random.randrange(0,displayWidth-blockSize, blockSize)
    foodY = random.randrange(0,displayHeight-blockSize, blockSize)
    large = 0
    if random.randrange(0,9) == 0:
        large = 1
        if foodX > displayWidth-blockSize*3:
            foodX = displayWidth-blockSize*3
        if foodY > displayHeight-blockSize*3:
            foodY = displayHeight-blockSize*3
    return foodX, foodY, large

def snake(snakeList,blockSize):
    for position in snakeList:
        pygame.draw.rect(gameDisplay, black, [position[0],position[1],blockSize,blockSize])

# GAME LOOP
def gameLoop():
    gameExit = False
    gameOver = False
    eaten = True
    snakeList = []

    headX = displayWidth/2
    headY = displayHeight/2
    headX_change = 0
    headY_change = 0

    while not gameExit:
        gameDisplay.fill(white)

        # MAKE FOOD
        if eaten:
            foodX, foodY, largeFood = generateFood()
            eaten = False

        # GAME OVER LOOP
        while gameOver:
            
            # GAME OVER MESSAGE
            gameDisplay.fill(black)
            message_display("large", "GAME OVER", white, displayWidth/2, displayHeight/2)
            message_display("small", "Q: Quit    C: Play Again", white, displayWidth/2, displayHeight*2/3)
            pygame.display.update()

            # QUIT / PLAY AGAIN
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == K_c:
                        gameLoop()
            
        # PLAYER MOVEMENT
        for event in pygame.event.get():
            if event.type == QUIT:
                gameExit = True
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if headX_change >= 0:
                        headX_change = blockSize
                        headY_change = 0
                elif event.key == K_LEFT:
                    if headX_change <= 0:
                        headX_change = -blockSize
                        headY_change = 0
                elif event.key == K_UP:
                    if headY_change <= 0:
                        headX_change = 0
                        headY_change = -blockSize
                elif event.key == K_DOWN:
                    if headY_change >= 0:
                        headX_change = 0
                        headY_change = blockSize
                        
            """
            # Stop when key is lifted
            direction = [K_RIGHT, K_LEFT, K_UP, K_DOWN]
            if event.type == KEYUP:
                if event.key in direction:
                    headY_change = 0
                    headX_change = 0
            """

        headX += headX_change
        headY += headY_change

        # GAME OVER
        if headX >= displayWidth or headX < 0 or headY >= displayHeight or headY < 0:
            gameOver = True

        snakeHead = [headX,headY]
        if snakeHead in snakeList:
            gameOver = True
        snakeList.append(snakeHead)

        snake(snakeList,blockSize)
        del snakeList[0]

        foodSize = blockSize
        if largeFood:
            foodSize = blockSize*3

        pygame.draw.rect(gameDisplay, red, [foodX,foodY,foodSize,foodSize]) # draw apple
        pygame.display.update()
    
        # EAT FOOD
        if headX == foodX and headY == foodY:
            eaten = True
            snakeList.append(snakeHead)

        clock.tick(10)

    pygame.quit()
    quit()

gameLoop()