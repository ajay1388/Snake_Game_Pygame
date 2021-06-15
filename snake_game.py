import sys
import pygame
import os
import random

start_width = 500
start_height = 200
window_width = 1200
window_height = 800
score = 0
h_score = 0

count_obstacle = 0
x_obstacle = 0
y_obstacle = 0
snake_length = 20
snake_x = 200
snake_y = 100
direction = "right"
change_to = direction
snake_speed = 10
game_over = 0
x_snake = []
y_snake = []

sand = (160, 128, 96)
snake_colour = (0, 51, 0)
green = (0, 255, 0)
grey = (128, 128, 128)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)


def main():
    global screen, clock, keys, change_to, direction, count_obstacle
    global snake_speed, snake_x, snake_y, score, game_over, x_snake, y_snake
    global start_game
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake Game")
    # keys = pygame.key.get_pressed()
    screen.fill(sand)
    last = pygame.time.get_ticks()

    drawgrid()
    x_snake.append(snake_x)
    y_snake.append(snake_y)
    drawsnake()
    while True:
        for event in pygame.event.get():
            now = pygame.time.get_ticks()
            if (now - last) >= 5000:
                snake_speed = min(15, snake_speed + 1)
                last = now
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_over == 1:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE and game_over == 1:
                    snake_x = 200
                    snake_y = 100
                    count_obstacle = 0
                    x_snake = []
                    y_snake = []
                    direction = "right"
                    change_to = direction
                    score = 0
                    game_over = 0
                    main()
                elif game_over == 1:
                    continue
                elif event.key == pygame.K_LEFT:
                    change_to = "left"
                elif event.key == pygame.K_RIGHT:
                    change_to = "right"
                elif event.key == pygame.K_UP:
                    change_to = "up"
                elif event.key == pygame.K_DOWN:
                    change_to = "down"
        if change_to == "right" and direction != "left":
            direction = "right"
        if change_to == "left" and direction != "right":
            direction = "left"
        if change_to == "up" and direction != "down":
            direction = "up"
        if change_to == "down" and direction != "up":
            direction = "down"
        move(direction)
        pygame.display.update()
        clock.tick(snake_speed)


def move(s):
    global score, x_snake, y_snake
    global count_obstacle, x_obstacle, y_obstacle, snake_x, snake_y, snake_length
    x = snake_x
    y = snake_y
    tx = snake_x
    ty = snake_y
    if count_obstacle == 0:
        x_obstacle = random.randrange(0, window_width - 20, 20)
        y_obstacle = random.randrange(0, window_height - 20, 20)
        while x == x_obstacle and y == y_obstacle:
            x_obstacle = random.randrange(0, window_width - 20, 20)
            y_obstacle = random.randrange(0, window_height - 20, 20)
        pygame.draw.rect(screen, red, (x_obstacle, y_obstacle, 20, 20))
        count_obstacle = 1
    if check(x, y, s):
        gameover()
        return
    elif check_over(x, y, s):
        gameover()
        return
    if s == "left":
        x -= 20
    elif s == "right":
        x += 20
    elif s == "up":
        y -= 20
    else:
        y += 20
    drawgrid()
    x_snake.append(x)
    y_snake.append(y)
    if x != x_obstacle or y != y_obstacle:
        x_snake = x_snake[1:]
        y_snake = y_snake[1:]
        if x_snake[0] - 20 != x_obstacle or y_snake[0] != y_obstacle:
            draw_block(x_snake[0] - 20, y_snake[0], sand)
        elif x_snake[0] - 20 == x_obstacle and y_snake[0] == y_obstacle:
            draw_block(x_snake[0] - 20, y_snake[0], red)
        if x_snake[0] + 20 != x_obstacle or y_snake[0] != y_obstacle:
            draw_block(x_snake[0] + 20, y_snake[0], sand)
        elif x_snake[0] + 20 == x_obstacle and y_snake[0] == y_obstacle:
            draw_block(x_snake[0] + 20, y_snake[0], red)
        if x_snake[0] != x_obstacle or y_snake[0] - 20 != y_obstacle:
            draw_block(x_snake[0], y_snake[0] - 20, sand)
        elif x_snake[0] - 20 == x_obstacle and y_snake[0] == y_obstacle:
            draw_block(x_snake[0], y_snake[0] - 20, red)
        if x_snake[0] != x_obstacle or y_snake[0] + 20 != y_obstacle:
            draw_block(x_snake[0], y_snake[0] + 20, sand)
        elif x_snake[0] - 20 == x_obstacle and y_snake[0] == y_obstacle:
            draw_block(x_snake[0], y_snake[0] + 20, red)
    else:
        draw_block(tx, ty, sand)
    drawsnake()
    if x == x_obstacle and y == y_obstacle:
        draw_block(x, y, sand)
        score += 10
        # snake_length+=20
        x_obstacle = random.randrange(0, window_width - 20, 20)
        y_obstacle = random.randrange(0, window_height - 20, 20)
        while check_val(x_obstacle, y_obstacle):
            x_obstacle = random.randrange(0, window_width - 20, 20)
            y_obstacle = random.randrange(0, window_height - 20, 20)
        pygame.draw.rect(screen, red, (x_obstacle, y_obstacle, 20, 20))
        count_obstacle = 1
    snake_x = x
    snake_y = y


def check_val(x, y):
    global x_snake, y_snake
    for i in range(0, len(x_snake)):
        if x == x_snake[i] and y == y_snake[i]:
            return True
    return False


def check(x, y, s):
    global x_snake, y_snake
    global window_height, window_width
    if s == "left" and x == 0:
        return True
    if s == "right" and x == (window_width - 20):
        return True
    if s == "up" and y == 0:
        return True
    if s == "down" and y == (window_height - 20):
        return True
    return False


def check_over(x, y, s):
    global x_snake, y_snake
    if s == "left":
        x -= 20
    elif s == "right":
        x += 20
    elif s == "up":
        y -= 20
    elif s == "down":
        y += 20
    for i in range(0, len(x_snake)):
        if x == x_snake[i] and y == y_snake[i]:
            return True
    return False


def gameover():
    filepath = os.path.realpath("image.jpg")
    global score, h_score, game_over
    screen = pygame.display.set_mode((window_width, window_height))
    screen.fill(black)
    font = pygame.font.SysFont('century', 54, bold=True)
    h_score = max(h_score, score)
    s = 'Your Score ' + str(score) + "    " + 'High Score ' + str(h_score)
    text = font.render(s, True, green)
    image = pygame.image.load(filepath)
    image_rect = image.get_rect()
    image_rect.center = (window_width // 2, window_height // 2)
    screen.blit(image, image_rect)
    text_rect = text.get_rect()
    text_rect.center = (window_width // 2, window_height - 200)
    screen.blit(text, text_rect)

    pygame.display.update()
    font = pygame.font.SysFont('centaur', 30, bold=True)
    text = font.render("Press ENTER to exit and SPACE to restart", True, black)
    text_rect = text.get_rect()
    text_rect.center = (window_width // 2, window_height - 100)
    screen.blit(text, text_rect)
    game_over = 1
    '''
    now = pygame.time.get_ticks()
    while (now - last) <= 1500:
        now = pygame.time.get_ticks()
    sys.exit()
    '''


def drawgrid():
    block_size = 20
    for x in range(0, window_width, block_size):
        for y in range(0, window_height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, black, rect, 1)


def drawsnake():
    if (len(x_snake) == 0):
        return
    # rect = pygame.Rect(x_snake[-1], y_snake[-1], 20, 20)
    # pygame.draw.rect(screen, snake_colour, rect)
    pygame.draw.circle(screen, black, (x_snake[-1] + 10, y_snake[-1] + 10), 10, 3)
    for i in range(0, len(x_snake) - 1):
        # rect = pygame.Rect(x_snake[i], y_snake[i], 20, 20)
        # pygame.draw.rect(screen, green, rect)
        pygame.draw.circle(screen, white, (x_snake[i] + 10, y_snake[i] + 10), 10, 3)


def draw_block(x, y, color):
    rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, black, rect, 1)


def start_game_space():
    done = True
    pygame.init()
    screen = pygame.display.set_mode((start_width, start_height))
    pygame.display.set_caption("Snake Game")
    filepath = os.path.realpath("space_start.jpg")
    image = pygame.image.load(filepath)
    image_rect = image.get_rect()
    image_rect.center = (start_width // 2, start_height // 2)
    screen.blit(image, image_rect)
    font = pygame.font.SysFont('century', 70, bold=True)
    text = font.render("Snake Game", True, green)
    text_rect = text.get_rect()
    text_rect.center = (start_width // 2, 40)
    screen.blit(text, text_rect)
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    return
        pygame.display.update()


if __name__ == "__main__":
    start_game_space()
    main()
