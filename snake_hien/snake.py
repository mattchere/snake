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
def message_display(size, msg, colour, centerX, centerY):
    if size == "large":
        textSurf = fontLarge.render(msg, True, colour)
        textRect = textSurf.get_rect()
    elif size == "small":
        textSurf = fontSmall.render(msg, True, colour)
        textRect = textSurf.get_rect()
    textRect.center = centerX, centerY
    gameDisplay.blit(textSurf,textRect)


def generateFood():
    foodX = random.randrange(0,displayWidth-blockSize, blockSize)
    foodY = random.randrange(0,displayHeight-blockSize, blockSize)
    size = 1
    if random.randrange(0,9) == 0:
        size = 3
        if foodX > displayWidth-blockSize*3:
            foodX = displayWidth-blockSize*3
        if foodY > displayHeight-blockSize*3:
            foodY = displayHeight-blockSize*3
    foodRect = Rect(foodX, foodY, blockSize*size, blockSize*size)
    return foodRect


def snake(snakeList,blockSize):
    for position in snakeList:
        pygame.draw.rect(gameDisplay, white, [position[0],position[1],blockSize,blockSize])

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
        gameDisplay.fill(black)

        # MAKE FOOD
        if eaten:
            foodRect = generateFood()
            eaten = False

        # GAME OVER LOOP
        while gameOver:
            
            # GAME OVER MESSAGE
            gameDisplay.fill(black)
            message_display("large", "GAME OVER", white, displayWidth/2, displayHeight/2)
            message_display("small", "Q: Quit    C: Play Again", white, displayWidth/2, displayHeight*4/7)
            pygame.display.update()

            # QUIT / PLAY AGAIN
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == K_c:
                        gameLoop()
                if event.type == QUIT:
                    gameExit = True
                    gameOver = False
            
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

        headX += headX_change
        headY += headY_change

        # GAME OVER
        if headX >= displayWidth or headX < 0 or headY >= displayHeight or headY < 0:
            gameOver = True

        snakeHead = [headX,headY]
        if snakeHead in snakeList:
            gameOver = True

        # SNAKE MOVEMENT    
        snakeList.append(snakeHead)
        snake(snakeList,blockSize)
        del snakeList[0]

        snakeHeadRect = pygame.Rect(headX, headY, blockSize, blockSize)
        pygame.draw.rect(gameDisplay, red, foodRect)
        
        # EAT FOOD
        if snakeHeadRect.colliderect(foodRect):
            eaten = True
            snakeList.append(snakeHead)

        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    quit()

gameLoop()