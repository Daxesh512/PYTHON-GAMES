import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player_img = pygame.image.load('tank.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 40))

bullet_img = pygame.Surface((7, 18), pygame.SRCALPHA)
pygame.draw.rect(bullet_img, (255, 255, 0), [0, 0, 7, 18])
bullet_speed = 9

enemy_imgs = [
    pygame.transform.scale(pygame.image.load('alien1.png').convert_alpha(), (48, 36)),
    pygame.transform.scale(pygame.image.load('alien2.png').convert_alpha(), (48, 36)),
    pygame.transform.scale(pygame.image.load('alien3.png').convert_alpha(), (48, 36))
]

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (70, 130, 180)  
        self.highlight_color = (100, 149, 237) 

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.highlight_color, self.rect)
            if click[0] == 1:  
                return True  
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        return False

def create_enemies():
    enemies = []
    for _ in range(8):
        image = random.choice(enemy_imgs)
        x = random.randint(0, SCREEN_WIDTH - 48)
        y = random.randint(60, 160)
        speed = random.choice([2, 3, 4])
        enemies.append({'img': image, 'x': x, 'y': y, 'speed': speed})
    return enemies

def reset_game():
    global player_x, player_y, bullets, enemies, score, lives, game_over
    player_x = (SCREEN_WIDTH - 60) // 2
    player_y = SCREEN_HEIGHT - 70
    bullets = []
    enemies = create_enemies()
    score = 0
    lives = 3
    game_over = False

def is_collision(x1, y1, x2, y2, threshold=32):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance < threshold

reset_game()

clock = pygame.time.Clock()
running = True

button_width, button_height = 200, 50
restart_button = Button((SCREEN_WIDTH - button_width)//2, SCREEN_HEIGHT//2 + 50, button_width, button_height, "Restart")

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 6
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 60:
            player_x += 6

        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullets.append([player_x + 28, player_y])

        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            screen.blit(bullet_img, (bullet[0], bullet[1]))
            if bullet[1] < 0:
                bullets.remove(bullet)

        for enemy in enemies:
            enemy['x'] += enemy['speed']
            if enemy['x'] <= 0 or enemy['x'] >= SCREEN_WIDTH - 48:
                enemy['speed'] = -enemy['speed']
                enemy['y'] += 40
            screen.blit(enemy['img'], (enemy['x'], enemy['y']))

            for bullet in bullets[:]:
                if is_collision(enemy['x'], enemy['y'], bullet[0], bullet[1]):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    enemy['x'] = random.randint(0, SCREEN_WIDTH - 48)
                    enemy['y'] = random.randint(60, 160)
                    enemy['speed'] = random.choice([2, 3, 4])
                    enemy['img'] = random.choice(enemy_imgs)
                    score += 1

            if is_collision(enemy['x'] + 24, enemy['y'] + 18, player_x + 30, player_y + 20, threshold=40):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    player_x = (SCREEN_WIDTH - 60) // 2
                    bullets.clear()
                    enemies = create_enemies()
                    pygame.display.update()
                    time.sleep(1)
                    break

        screen.blit(player_img, (player_x, player_y))

        score_lives = font.render(f"Score: {score}   Lives: {lives}", True, WHITE)
        screen.blit(score_lives, (10, 10))

    else:
        game_over_text = big_font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, SCREEN_HEIGHT // 2))

        if restart_button.draw(screen):
            reset_game()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
