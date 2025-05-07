import pygame
import random
import math

# --- 기본 설정 ---
pygame.init()
pygame.font.init() # 폰트 초기화 추가

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("갤러그 스타일 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 배경 이미지 (선택 사항)
# background = pygame.image.load('background.png') # 배경 이미지 파일 경로

# 플레이어
# player_img = pygame.image.load('player.png') # 플레이어 이미지 파일 경로
player_size = 50
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - player_size - 10
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, player_size, player_size) # 이미지 대신 사각형 사용

# 총알
bullet_size = 5
bullet_speed = 7
bullets = [] # 플레이어 총알 리스트

# 적
enemy_size = 40
enemy_speed = 2
enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = 60 # 프레임 단위 (낮을수록 빨리 생성)

# 점수
score = 0
font = pygame.font.SysFont('comicsans', 30)

# 게임 루프 제어
running = True
game_over = False
clock = pygame.time.Clock()

# --- 게임 함수 ---
def spawn_enemy():
    """새로운 적을 생성합니다."""
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)
    enemy_y = random.randint(-100, -enemy_size) # 화면 위에서 시작
    # enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size) # 이미지 대신 사각형 사용
    enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))

def draw_elements():
    """화면에 게임 요소들을 그립니다."""
    # 배경 그리기 (이미지 또는 단색)
    screen.fill(BLACK)
    # screen.blit(background, (0, 0)) # 배경 이미지 사용 시

    # 플레이어 그리기 (이미지 또는 사각형)
    pygame.draw.rect(screen, GREEN, player_rect)
    # screen.blit(player_img, (player_rect.x, player_rect.y)) # 플레이어 이미지 사용 시

    # 총알 그리기
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    # 적 그리기 (이미지 또는 사각형)
    for enemy in enemies:
        pygame.draw.rect(screen, BLUE, enemy)
        # screen.blit(enemy_img, (enemy.x, enemy.y)) # 적 이미지 사용 시

    # 점수 표시
    score_label = font.render(f"Score: {score}", 1, WHITE)
    screen.blit(score_label, (10, 10))

    # 게임 오버 메시지
    if game_over:
        game_over_font = pygame.font.SysFont('comicsans', 60)
        game_over_label = game_over_font.render("GAME OVER", 1, RED)
        screen.blit(game_over_label, (SCREEN_WIDTH // 2 - game_over_label.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - game_over_label.get_height() // 2))
        restart_label = font.render("Press R to Restart", 1, WHITE)
        screen.blit(restart_label, (SCREEN_WIDTH // 2 - restart_label.get_width() // 2,
                                     SCREEN_HEIGHT // 2 + game_over_label.get_height()))


    pygame.display.flip() # 화면 업데이트 (pygame.display.update() 와 유사)

def reset_game():
    """게임을 초기 상태로 리셋합니다."""
    global player_x, player_y, player_rect, bullets, enemies, score, game_over, enemy_spawn_timer
    player_x = SCREEN_WIDTH // 2 - player_size // 2
    player_y = SCREEN_HEIGHT - player_size - 10
    player_rect.topleft = (player_x, player_y)
    bullets = []
    enemies = []
    score = 0
    game_over = False
    enemy_spawn_timer = 0


# --- 메인 게임 루프 ---
while running:
    clock.tick(60) # FPS 설정 (초당 60 프레임)

    # --- 이벤트 처리 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                # 스페이스바로 총알 발사
                if event.key == pygame.K_SPACE:
                    bullet_x = player_rect.centerx - bullet_size // 2
                    bullet_y = player_rect.top
                    bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_size, bullet_size * 3)) # 길쭉한 총알 모양
            else:
                # 게임 오버 상태에서 R키로 재시작
                if event.key == pygame.K_r:
                    reset_game()


    if not game_over:
        # --- 키 입력 처리 (지속적인 입력) ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed

        # --- 게임 로직 업데이트 ---
        # 총알 이동 및 화면 밖 총알 제거
        bullets_to_remove = []
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets_to_remove.append(bullet)
        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        # 적 생성 타이머
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_delay:
            spawn_enemy()
            enemy_spawn_timer = 0 # 타이머 리셋

        # 적 이동 및 화면 밖 적 제거
        enemies_to_remove = []
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.top > SCREEN_HEIGHT:
                enemies_to_remove.append(enemy)
        for enemy in enemies_to_remove:
            enemies.remove(enemy)

        # 충돌 감지
        bullets_hit = []
        enemies_hit = []
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy): # 총알과 적 충돌
                    if bullet not in bullets_hit:
                        bullets_hit.append(bullet)
                    if enemy not in enemies_hit:
                        enemies_hit.append(enemy)
                    score += 10 # 점수 증가

        # 충돌한 총알과 적 제거
        for bullet in bullets_hit:
            if bullet in bullets: # 이미 제거되지 않았는지 확인
                 bullets.remove(bullet)
        for enemy in enemies_hit:
             if enemy in enemies: # 이미 제거되지 않았는지 확인
                 enemies.remove(enemy)

        # 플레이어와 적 충돌 감지
        for enemy in enemies:
            if player_rect.colliderect(enemy):
                game_over = True
                break # 충돌 즉시 루프 종료

    # --- 화면 그리기 ---
    draw_elements()


pygame.quit()
