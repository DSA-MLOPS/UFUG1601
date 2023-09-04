import pygame
import random

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width = 500
screen_height = 500

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set the colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)

# Set the font
font = pygame.font.SysFont(None, 25)

# Set the clock
clock = pygame.time.Clock()

# Set the block size and speed
block_size = 10
speed = 15

# Define the snake function
def snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], block_size, block_size])

# Define the message function
def message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [screen_width/6, screen_height/3])

# Define the game loop function
def gameLoop():
    gameExit = False
    gameOver = False

    # Set the starting position of the snake
    lead_x = screen_width/2
    lead_y = screen_height/2

    # Set the change in position
    lead_x_change = 0
    lead_y_change = 0

    # Set the starting length of the snake
    snake_list = []
    snake_length = 1

    # Set the starting position of the food
    food_x = round(random.randrange(0, screen_width-block_size)/10.0)*10.0
    food_y = round(random.randrange(0, screen_height-block_size)/10.0)*10.0

    while not gameExit:

        while gameOver == True:
            screen.fill(black)
            message("Game over! Press C to play again or Q to quit.", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        # Check if the snake hits the edge of the screen
        if lead_x >= screen_width or lead_x < 0 or lead_y >= screen_height or lead_y < 0:
            gameOver = True

        # Update the position of the snake
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Fill the screen with white
        screen.fill(black)

        # Draw the food
        pygame.draw.rect(screen, yellow, [food_x, food_y, block_size, block_size])

        # Draw the snake
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                gameOver = True

        snake(block_size, snake_list)

        # Update the score
        score = snake_length - 1
        score_text = font.render("Score: "+str(score), True, white)
        screen.blit(score_text, [0, 0])

        # Update the display
        pygame.display.update()

        # Check if the snake hits the food
        if lead_x == food_x and lead_y == food_y:
            food_x = round(random.randrange(0, screen_width-block_size)/10.0)*10.0
            food_y = round(random.randrange(0, screen_height-block_size)/10.0)*10.0
            snake_length += 1

        # Set the speed of the game
        clock.tick(speed)

    # Quit pygame
    pygame.quit()

# Call the game loop function
gameLoop()

