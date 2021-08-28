import pygame
import os
from pygame import transform
from pygame import image

from pygame.draw import rect
pygame.font.init()
pygame.mixer.init()
pygame.init()

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Space Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
TRANSPARENT = (0, 0, 0, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 50)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 10
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 110, 80

global start
start = False

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BUTTON_PRESSED = pygame.USEREVENT + 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

START_IMAGE = pygame.image.load(os.path.join('assets', 'Start_Button.png'))

class Button():
    def __init__ (self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.event.post(pygame.event.Event(BUTTON_PRESSED))
        WIN.blit(self.image, (self.rect.x, self.rect.y))

start_button = Button(WIDTH // 2 - 300 // 2, HEIGHT // 2 - START_IMAGE.get_height() // 2, START_IMAGE, 10)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    start_button.draw()

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
        
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:
        yellow.y += VELOCITY

    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:
        yellow.x -= VELOCITY

    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x + BORDER.width:
        yellow.x += VELOCITY

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
        
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15:
        red.y += VELOCITY

    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY

    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:
        red.x += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    global start

    red = pygame.Rect(WIDTH - 100, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(15, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    #start_button.image.fill(BLACK)

    red_bullets = []
    yellow_bullets = []

    red_health = 3
    yellow_health = 3

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    exit()
                if(start == True):
                    if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 20, 10)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 20, 10)
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BUTTON_PRESSED:
                start_button.image.fill(TRANSPARENT)
                start = True

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
            
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        if start == True:
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_movement(keys_pressed, red)
            handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow , red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()