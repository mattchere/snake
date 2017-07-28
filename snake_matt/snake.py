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
        self.speed = 5
        self.rect = Rect((self.posx, self.posy, 5, 5))

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

        self.rect = Rect((self.posx, self.posy, 5, 5))

        if self.next is not None:
            self.next.move_body()

    def collide(self, size):
        # loop to the last node
        node = self
        for i in range(size-1):
            node = node.next
        if node.next is None:
            if node.curr == "LEFT":
                node.next = Node(node.posx+5, node.posy, node)
            elif node.curr == "RIGHT":
                node.next = Node(node.posx-5, node.posy, node)
            elif node.curr == "UP":
                node.next = Node(node.posx, node.posy+5, node)
            elif node.curr == "DOWN":
                node.next = Node(node.posx, node.posy-5, node)
        else:
            print("Error")


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
    node = head.next
    while node.next is not None:
        if head.rect.colliderect(node):
            print("Hit")
        node = node.next
    return False


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Initialise the snake and food
    snake = Node(20, 20, None)
    node = snake
    length = 30
    for i in range(length):
        node.next = Node(20, 20, node)
        node = node.next
    food = Food()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.update()
    direction = "RIGHT"
    end = False
    length += 1
    time = 0

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction = "LEFT"
                if event.key == K_RIGHT:
                    direction = "RIGHT"
                if event.key == K_UP:
                    direction = "UP"
                if event.key == K_DOWN:
                    direction = "DOWN"

        end = snake.move(direction)
        screen.blit(background, (0, 0))
        draw_snake(snake, screen)
        pygame.draw.rect(screen, (0, 0, 0), food.rect)
        pygame.display.update()
        if end:
            return
        if snake.rect.colliderect(food):
            food = Food()
            snake.collide(length)
            length += 1
        if tail_collide(snake) and time > length:
            return
        time += 1

if __name__ == '__main__':
    main()
