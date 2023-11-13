import random
import pygame
from sys import exit

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_values(self, node1, node2):
        x_total = node1.x + node2.x
        y_total = node1.y + node2.y
        return Node(x_total, y_total)
    
    def compare_values(self, node1, node2):
        if node1.x == node2.x and node1.y == node2.y:
            return True
        
        return False
    
    def insert_nodes(self, new_data): #for the base of the snake
        new_node = new_data

        if self.head is None:
            self.head = new_node
            return

        last = self.head
        while (last.next):
            last = last.next

        last.next = new_node
    
    def insert_at_beginning(self, new_data): #for moving snake method
        new_node = new_data

        new_node.next = self.head
        self.head = new_node

    def delete_end(self): #for moving snake method
        temp = self.head
        while(temp.next is not None):
            prev = temp
            temp = temp.next
        prev.next = None

    def delete_all_nodes(self): #For reset method
        while self.head:
            self.head = self.head.next

class MAIN:
    def __init__(self):
        self.linkedlist = LinkedList() #For compare functions
        self.snake = snake() 
        self.fruit = fruit()

    def update(self):
        self.snake.move_snake()
        self.eat()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def eat(self):
        if self.linkedlist.compare_values(self.fruit.pos, self.snake.linkedlist.head):
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.linkedlist.head.x < cell_number or not 0 <= self.snake.linkedlist.head.y < cell_number: #If head collides with wall, game resets
            self.snake.reset()

        snake_body = self.snake.linkedlist.head.next
        while snake_body:
            if self.linkedlist.compare_values(snake_body, self.fruit.pos): #Prevents the fruit from spawning in the snake
                self.fruit.randomize()
            if self.linkedlist.compare_values(snake_body, self.snake.linkedlist.head): #If head collides with body, game resets
                self.snake.reset()
            snake_body = snake_body.next

class snake:
    def __init__(self):
        self.linkedlist = LinkedList()
        self.linkedlist.head = Node(5,10)
        self.linkedlist.insert_nodes(Node(4,10))
        self.linkedlist.insert_nodes(Node(3,10))

        self.direction = Node(0,0) #Changes value depending on the key press
        self.new_block = False

    def draw_snake(self):
        #Draws each block of the snake
        node = self.linkedlist.head
        while node:
            x_pos = node.x * cell_size
            y_pos = node.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 132), block_rect)
            node = node.next

    def move_snake(self):
        #Makes the snake grow by 1 block
        if self.new_block == True:
            body_copy = self.linkedlist
            body_copy.insert_at_beginning(self.linkedlist.add_values(body_copy.head, self.direction))
            self.linkedlist = body_copy
            self.new_block = False
        else:
            body_copy = self.linkedlist
            body_copy.delete_end()
            body_copy.insert_at_beginning(self.linkedlist.add_values(body_copy.head, self.direction))
            self.linkedlist = body_copy
        
    def add_block(self):
        self.new_block = True

    def reset(self):
        self.linkedlist.delete_all_nodes()
        self.linkedlist.head = Node(5,10)
        self.linkedlist.insert_nodes(Node(4,10))
        self.linkedlist.insert_nodes(Node(3,10))
        self.direction = Node(0,0)

class fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        #Draws the fruit
        x_pos = self.pos.x * cell_size
        y_pos = self.pos.y * cell_size
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, (235, 134, 52), fruit_rect)

    def randomize(self):
        #Randomize the fruit's x and y positions
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Node(self.x, self.y)

pygame.init()

cell_size = 40 #Measured in pixels
cell_number = 15 
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number)) #600 x 600 screen
pygame.display.set_caption("Snakes")
clock = pygame.time.Clock()

BG_SURFACE = pygame.transform.scale(pygame.image.load("grass_bg.jpg").convert(), (cell_size * cell_number, cell_size * cell_number))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150) #Speed of the snake measured in milliseconds

main_game = MAIN()

#Display the screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #stops displaying
            exit() #stops code
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            #WASD Movement keys
            if event.key == pygame.K_w and main_game.snake.direction.y != 1:
                main_game.snake.direction = Node(0, -1)
            elif event.key == pygame.K_s and main_game.snake.direction.y != -1:
                main_game.snake.direction = Node(0, 1)
            elif event.key == pygame.K_a and main_game.snake.direction.x != 1:
                main_game.snake.direction = Node(-1, 0)
            elif event.key == pygame.K_d and main_game.snake.direction.x != -1:
                main_game.snake.direction = Node(1, 0)

    screen.blit(BG_SURFACE, (0, 0)) #shows background
    main_game.draw_elements() #draws the fruit and snake
    pygame.display.update()
    clock.tick(60) #controls fps