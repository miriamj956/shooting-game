import pygame
import os

pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
                    #border placement in center -5 to make it stay aligned and also enlargend, 0= y 10=w
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SHOOTER_WIDTH, SHOOTER_HEIGHT = 55, 40

#To customize the event
GREEN_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

GREEN_SHOOTER_IMAGE = pygame.image.load(os.path.join('Assets', 'girl.png'))
GREEN_SHOOTER = pygame.transform.rotate(pygame.transform.scale(GREEN_SHOOTER_IMAGE,(SHOOTER_WIDTH, SHOOTER_HEIGHT)), 90)

RED_SHOOTER_IMAGE = pygame.image.load(os.path.join('Assets', 'guy.png'))
RED_SHOOTER = pygame.transform.rotate(pygame.transform.scale(RED_SHOOTER_IMAGE,(SHOOTER_WIDTH, SHOOTER_HEIGHT)), 270)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bkg.png')), (WIDTH, HEIGHT))

def draw_window(red, green, red_bullets, green_bullets, red_health, green_health):
    WIN.blit(BACKGROUND,(0,0)) #WIN refers to the screen
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " +str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (700, 10))
    WIN.blit(RED_SHOOTER, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    green_health_text = HEALTH_FONT.render("Health: " +str(green_health), 1, WHITE)
    WIN.blit(green_health_text, (10, 10))
    WIN.blit(GREEN_SHOOTER, (green.x, green.y))

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

#moves w wasd
def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VEL > 0: #LEFT
        green.x -=VEL
    if keys_pressed[pygame.K_d] and green.x + VEL + green.width < BORDER.x: #RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_w] and green.y - VEL > 0: #UP
        green.y -= VEL
    if keys_pressed[pygame.K_s] and green.y + VEL + green.height < HEIGHT - 15: #DOWN
        green.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: 
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL

def handle_bullets(green_bullets, red_bullets, green, red):
  for bullet in green_bullets:
    #move right
    bullet.x += BULLET_VEL
    if red.colliderect(bullet):
      pygame.event.post(pygame.event.Event(RED_HIT))
      green_bullets.remove(bullet)
    elif bullet.x > WIDTH:
      green_bullets.remove(bullet)

  for bullet in red_bullets:
    #move left
    bullet.x -= BULLET_VEL
    if green.colliderect(bullet):
      pygame.event.post(pygame.event.Event(GREEN_HIT))
      red_bullets.remove(bullet)
    elif bullet.x < 0:
      red_bullets.remove(bullet)


def draw_winner(text):
  draw_text = WINNER_FONT.render(text, 1, WHITE)
  WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
  pygame.display.update()
  pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SHOOTER_WIDTH, SHOOTER_HEIGHT)
    green = pygame.Rect(100, 300, SHOOTER_WIDTH, SHOOTER_HEIGHT)
    red_bullets = []
    red_health = 10
    green_bullets = []
    green_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
      
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y, 10, 5)
                    green_bullets.append(bullet)

                if event.key == pygame.K_m and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == GREEN_HIT:
                green_health -= 1

        winner_text = ""
        if red_health < 0:
            winner_text = "Yellow Wins ! "
        if green_health < 0:
            winner_text = "Red Wins !"

        if winner_text != "":
            draw_winner(winner_text)
            break

    keys_pressed = pygame.key.get_pressed()
    green_handle_movement(keys_pressed, green)
    red_handle_movement(keys_pressed, red)
    handle_bullets(green_bullets, red_bullets, green, red)
    draw_window(red, green, red_bullets, green_bullets, red_health, green_health)

    main()



if __name__ == "__main__":
    main()



