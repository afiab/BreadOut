import pygame
import random

# initialize Pygame
pygame.init()

# window settings
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('BreadOut')

# colors 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (153, 222, 247)
GREEN = (0, 255,0)

# pics for the ball and bricks
ball_img = pygame.image.load("ball.png")
brick_img = pygame.image.load("brick.png")

# scale the images 
brick_width, brick_height = 25, 25 # brick size
ball_radius = 15  # ball size for scaling
brick_img = pygame.transform.scale(brick_img, (brick_width, brick_height))
ball_img = pygame.transform.scale(ball_img, (ball_radius * 2, ball_radius * 2))

# paddle
paddle_width, paddle_height = 100, 10
paddle_x = (width - paddle_width) // 2
paddle_y = height - 20
paddle_speed = 7

# ball
ball_x = width // 2
ball_y = height // 2
ball_dx = 3 * random.choice((1, -1))
ball_dy = 3 * random.choice((1, -1))

# bricks (positions, not rectangles anymore)
brick_rows = 5
brick_cols = 24
bricks = []

for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        brick_x = col * brick_width
        brick_y = row * brick_height
        brick_row.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))  # rects for collision
    bricks.append(brick_row)

# state variables
running = True
game_over = False
clock = pygame.time.Clock()

# reset game state
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, bricks, game_over
    ball_x = width // 2
    ball_y = height // 2
    ball_dx = 3 * random.choice((1, -1))
    ball_dy = 3 * random.choice((1, -1))
    paddle_x = (width - paddle_width) // 2
    game_over = False
    bricks.clear()
    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick_x = col * brick_width
            brick_y = row * brick_height
            brick_row.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
        bricks.append(brick_row)

# game loop
while running:
    clock.tick(60)
    screen.fill(LIGHTBLUE)
    
    # events handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()  # Reset game if space is pressed

    # paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
        paddle_x += paddle_speed
    
    # only move ball and check collisions if game is not over
    if not game_over:
        # ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # ball collision with walls
        if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
            ball_dx *= -1
        if ball_y - ball_radius < 0:
            ball_dy *= -1

        # ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if paddle_rect.collidepoint(ball_x, ball_y + ball_radius):
            ball_dy *= -1

        # ball collision with bricks
        for row in bricks:
            for brick in row:
                if brick.collidepoint(ball_x, ball_y):
                    ball_dy *= -1
                    row.remove(brick)
                    break

        # game over (ball hits bottom)
        if ball_y + ball_radius > height:
            game_over = True  # Set game over to true

    # draw paddle
    pygame.draw.rect(screen, GREEN, paddle_rect)

    # draw ball with PNG
    screen.blit(ball_img, (ball_x - ball_radius, ball_y - ball_radius))

    # draw bricks with PNG
    for row in bricks:
        for brick in row:
            screen.blit(brick_img, (brick.x, brick.y))

    # game over msg
    if game_over:
        font = pygame.font.SysFont(None, 36)
        text = font.render("Game Over! Press SPACE to Restart", True, RED)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))

    # Update the display
    pygame.display.flip()

pygame.quit()
