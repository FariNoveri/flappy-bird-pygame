import pygame
import random
import sys

pygame.init()

# Setup game
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
RED = (200, 0, 0)

# Bird
bird = pygame.Rect(100, 300, 30, 30)
gravity = 0.25
bird_movement = 0

# Pipes
pipe_width = 70
pipe_gap = 200
pipe_speed = 3
pipes = []
pipe_info = []  # Untuk menyimpan info pasangan pipa

def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height - pipe_gap // 2)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap // 2, pipe_width, HEIGHT - height)
    pipe_info.append({'x': WIDTH, 'counted': False})  # Simpan posisi x awal dan status
    return top_pipe, bottom_pipe

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Game state
score = 0
highscore = 0
font = pygame.font.SysFont(None, 40)
button_font = pygame.font.SysFont(None, 36)

def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(SCREEN, RED, rect)
    label = button_font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    SCREEN.blit(label, label_rect)
    return rect

clock = pygame.time.Clock()
running = True
game_active = True
game_paused = False

while running:
    clock.tick(60)
    SCREEN.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if game_active and not game_paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = -6
                elif event.key == pygame.K_p:
                    game_paused = True

            if event.type == SPAWNPIPE:
                pipes.extend(create_pipe())

        elif game_paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = False

        else:  # Game over screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    bird.y = 300
                    bird_movement = 0
                    pipes.clear()
                    pipe_info.clear()
                    score = 0
                    game_active = True
                elif exit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    sys.exit()

    if game_paused:
        pause_text = font.render("PAUSED", True, WHITE)
        SCREEN.blit(pause_text, (WIDTH // 2 - 60, HEIGHT // 2 - 30))
        resume_text = font.render("Press P to Resume", True, WHITE)
        SCREEN.blit(resume_text, (WIDTH // 2 - 120, HEIGHT // 2 + 10))
        pygame.display.update()
        continue

    if game_active:
        # Bird physics
        bird_movement += gravity
        bird.y += bird_movement
        pygame.draw.ellipse(SCREEN, WHITE, bird)

        # Process pipes
        new_pipes = []
        new_pipe_info = []
        
        for i in range(0, len(pipes), 2):
            if i+1 < len(pipes):  # Pastikan ada pasangan pipa
                top_pipe = pipes[i]
                bottom_pipe = pipes[i+1]
                info = pipe_info[i//2]
                
                # Gerakkan pipa
                top_pipe.x -= pipe_speed
                bottom_pipe.x -= pipe_speed
                
                # Gambar pipa
                pygame.draw.rect(SCREEN, GREEN, top_pipe)
                pygame.draw.rect(SCREEN, GREEN, bottom_pipe)
                
                # Cek jika pipa masih di layar
                if top_pipe.right > 0:
                    new_pipes.extend([top_pipe, bottom_pipe])
                    new_pipe_info.append(info)
                    
                    # Cek skor (hanya untuk pipa bawah)
                    if bottom_pipe.right < bird.left and not info['counted']:
                        info['counted'] = True
                        score += 1
                
                # Cek tabrakan
                if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
                    game_active = False
        
        pipes = new_pipes
        pipe_info = new_pipe_info

        # Cek burung keluar layar
        if bird.top <= -100 or bird.bottom >= HEIGHT:
            game_active = False

        # Tampilkan skor
        score_text = font.render(f"Score: {int(score)}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

    else:  # Game over screen
        if score > highscore:
            highscore = int(score)

        game_over_text = font.render("GAME OVER", True, WHITE)
        SCREEN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 90))
        final_score = font.render(f"Final Score: {int(score)}", True, WHITE)
        SCREEN.blit(final_score, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        SCREEN.blit(highscore_text, (WIDTH // 2 - 100, HEIGHT // 2 - 10))

        restart_button = draw_button("Restart", WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 40)
        exit_button = draw_button("Exit", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 40)

    pygame.display.update()