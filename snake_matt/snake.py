from collections import deque
import random
import pygame
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

class Node:

    def __init__(self, posx, posy, prevnode):
        self.posx = posx
        self.posy = posy
        self.prev = prevnode
        self.next = None
        self.last = None
        self.curr = None
        self.speed = 12
        self.rect = Rect((self.posx, self.posy, 12, 12))

    def move(self, direction):
        self.last = self.curr
        self.curr = direction
        self._move()
        if self.posx < 0 or self.posy < 0 \
           or self.posx > WINDOWWIDTH or self.posy > WINDOWHEIGHT:
            return True
        return False

    def move_body(self):
        self.last = self.curr
        self.curr = self.prev.last
        self._move()

    def _move(self):
        if self.curr == "LEFT":
            self.posx -= self.speed
        elif self.curr == "RIGHT":
            self.posx += self.speed
        elif self.curr == "UP":
            self.posy -= self.speed
        elif self.curr == "DOWN":
            self.posy += self.speed

        self.rect = Rect((self.posx, self.posy, 12, 12))

        if self.next is not None:
            self.next.move_body()

    def collide(self, size):
        # loop to the last node
        node = self
        for i in range(size-1):
            node = node.next

        if node.curr == "LEFT":
            node.next = Node(node.posx+12, node.posy, node)
        elif node.curr == "RIGHT":
            node.next = Node(node.posx-12, node.posy, node)
        elif node.curr == "UP":
            node.next = Node(node.posx, node.posy+12, node)
        elif node.curr == "DOWN":
            node.next = Node(node.posx, node.posy-12, node)


class Food:

    def __init__(self):
        random.seed()
        self.posx = random.randint(25, WINDOWWIDTH-25)
        self.posy = random.randint(25, WINDOWHEIGHT-25)
        self.rect = Rect((self.posx, self.posy, 25, 25))


def draw_snake(node, display):
    if node is not None:
        pygame.draw.rect(display, (0, 0, 0), node.rect)
        draw_snake(node.next, display)

def tail_collide(head):
    node = head
    while node.next is not None:
        node = node.next
        if head.rect.colliderect(node.rect):
            return True
    return False

def show_quit(screen):
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Display some text
    font = pygame.font.Font(None, 60)
    text = font.render("Game Over", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)

    font = pygame.font.Font(None, 35)
    text = font.render("Press q to quit, or c to continue", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery + 80
    background.blit(text, textpos)

    screen.blit(background, (0,0))


def main():
    # Initialise screen
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Initialise the snake and food
    snake = Node(background.get_rect().centerx, background.get_rect().centery, None)
    length = 1
    food = Food()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    draw_snake(snake, screen)
    pygame.draw.rect(screen, (0, 0, 0), food.rect)
    pygame.display.update()

    # Set up local variables
    start = False
    end = False
    direction = None

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                start = True
                if event.key == K_LEFT:
                    if direction != "RIGHT":
                        direction = "LEFT"
                if event.key == K_RIGHT:
                    if direction != "LEFT":
                        direction = "RIGHT"
                if event.key == K_UP:
                    if direction != "DOWN":
                        direction = "UP"
                if event.key == K_DOWN:
                    if direction != "UP":
                        direction = "DOWN"
                if end:
                    if event.key == K_q:
                        return
                    if event.key == K_c:
                        snake = Node(background.get_rect().centerx, background.get_rect().centery, None)
                        length = 1
                        food = Food()
                        direction = None
                        end = False
        if not end and start:
            end = snake.move(direction)
            if snake.rect.colliderect(food):
                food = Food()
                snake.collide(length)
                length += 1
            if tail_collide(snake):
                end = True
                print("hit")
            screen.blit(background, (0, 0))
            draw_snake(snake, screen)
            pygame.draw.rect(screen, (0, 0, 0), food.rect)
        elif end:
            start = False
            show_quit(screen)
        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
