import pygame, sys
import random
import math
from pygame import mixer
from pygame.math import Vector2

# Initialize game
pygame.init()

#  Create font
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

# Define game grid
cell_size = 30
number_of_cells = 25

# Create offset value for game border
OFFSET = 75

# Create screen with coordinates (x, y)
screen = pygame.display.set_mode((2*OFFSET + cell_size * number_of_cells, 2*OFFSET + cell_size * number_of_cells))

# Set title
pygame.display.set_caption("Venomous Villain")

# Create clock to allow us set frame rate of the game
clock = pygame.time.Clock()

# Define colors
background_color = (139, 172, 15)
foreground_color = (34, 34, 34)

# Add background sound
mixer.music.load("bg_sound.wav")
mixer.music.play(-1)

# Create the food for snake
class SnakeFood:
    # Define position of food using Vector2 class that allows row and column positioning 
    def __init__(self, snake_body):
        self.position = self.generate_random_position(snake_body)

    #  Draw food object using Rect
    def draw(self):
        # Define food rect
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET +  self.position.y * cell_size, cell_size, cell_size)
        # Draw food rect on screen using blit
        screen.blit(food_surface, food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)

    # Randomize spawn location for food that isn't in the same location as food
    def generate_random_position(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

# Create snake 
class Snake:
    # The snake is a list of coordinates defined with the Vector2 object
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        #  Define attribute of snake's movement direction
        self.direction = Vector2(1, 0)
        # Boolean to check if current action is adding segment
        self.add_segment = False
        # Load sounds
        self.eat_sound = pygame.mixer.Sound("eat.wav")
        self.game_over_sound = pygame.mixer.Sound("fail.wav")
    
    # Define method to draw snake segments onto the screen
    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, foreground_color, segment_rect, 0, 7)
    
    # Define method to update snake position
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        # Add segment at the head
        if self.add_segment == True:
            self.add_segment = False
        else: 
            # Remove the last element from the snake segment list
            self.body = self.body[:-1]
            
    # Bring snake to starting position
    def restart(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)

# Game class to improve organization
class Game:
    def __init__(self):
        self.snake = Snake()
        self.snake_food = SnakeFood(self.snake.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self):
        self.snake_food.draw()
        self.snake.draw()
    
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.snake_eats_food()
            self.check_collision_with_edge()
            self.check_position_with_body()

    # Check for snake collision with food. 
    def snake_eats_food(self):
        if self.snake.body[0] == self.snake_food.position:
            self.snake_food.position = self.snake_food.generate_random_position(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()
    
    # Check for collision with edge of game
    def check_collision_with_edge(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()
    
    # Check for collision with body
    def check_position_with_body(self):
        body_without_head = self.snake.body[1:]
        if self.snake.body[0] in body_without_head:
            self.game_over()
    
    # Create game over functionality i.e. reset snake body to initial position, generate new food at random position, and pause game until player presses another key
    def game_over(self):
        self.snake.restart()
        self.snake_food.position = self.snake_food.generate_random_position(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        self.snake.game_over_sound.play()


# Create game
game = Game()

# Create food object
food_surface = pygame.image.load("vv_food.png")

# Create custom event that is triggered when I need to update snake's position
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

# Start game loop
running = True
while running:
     # Check for quit event
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE: 
            game.update()
        if event.type == pygame.QUIT:
            running = False

        # Check for key controls and prevent moving in opposite direction
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # Set background color
    screen.fill(background_color)

    
    # Draw food and snake
    game.draw()

    # Add border
    pygame.draw.rect(screen, foreground_color, (OFFSET-5, OFFSET-5, cell_size*number_of_cells + 10, cell_size*number_of_cells + 10), 5)

    # Create surface for fonts and draw them with .blit()
    title_surface = title_font.render("Venomous Villain", True, foreground_color )
    screen.blit(title_surface, (OFFSET-5, 20))

    score_surface = score_font.render(f'Score: {game.score}', True, foreground_color)
    screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells + 10))

    # Update display and set frame rate
    pygame.display.update()
    clock.tick(60)