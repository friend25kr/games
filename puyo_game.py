# /home/friend25kr/myDev/myProjects/puyo_puyo_game.py
import pygame
import random
import sys

# --- 기본 설정 ---
pygame.init()
pygame.font.init()

# 화면 크기
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
GRID_WIDTH = 6   # 게임 보드 가로 칸 수
GRID_HEIGHT = 12 # 게임 보드 세로 칸 수 (실제로는 13줄, 맨 윗줄은 게임 오버 판정용)
BLOCK_SIZE = 50  # 뿌요 블록 크기

# 게임 보드 크기 계산
PLAY_WIDTH = GRID_WIDTH * BLOCK_SIZE
PLAY_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# 게임 보드 위치 계산 (화면 중앙 정렬)
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 20 # 하단 여백

# 색상 정의 (뿌요 색상 + 배경 등)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

PUYO_COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE]

# --- 게임 요소 ---
# 폰트 설정
score_font = pygame.font.SysFont('comicsans', 30)
game_over_font = pygame.font.SysFont('comicsans', 60)
small_font = pygame.font.SysFont('comicsans', 20)

# --- 게임 상태 변수 ---
score = 0
fall_speed = 0.5 # 초당 떨어지는 속도 (작을수록 빠름)
fall_time = 0
level_time = 0
game_over = False
paused = False

# --- 게임 함수 ---

def create_grid(locked_positions={}):
    """
    게임 보드 그리드를 생성합니다. 비어있는 칸은 0, 뿌요가 있는 칸은 색상 인덱스.
    locked_positions: 이미 뿌요가 고정된 위치 딕셔너리 {(x, y): color_index}
    """
    # GRID_HEIGHT + 1 줄 생성 (맨 윗 줄은 보이지 않지만 게임 오버 판정에 사용)
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT + 1)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color_index = locked_positions[(x, y)]
                grid[y][x] = color_index
    return grid

def get_random_puyo_color_index():
    """랜덤 뿌요 색상 인덱스 (1부터 시작) 를 반환합니다."""
    return random.randint(1, len(PUYO_COLORS))

class PuyoPair:
    """떨어지는 뿌요 쌍 클래스"""
    def __init__(self, x, y):
        self.center_x = x # 중심 뿌요의 그리드 x 좌표
        self.center_y = y # 중심 뿌요의 그리드 y 좌표
        self.other_x_offset = 0  # 다른 뿌요의 x 오프셋 (-1, 0, 1)
        self.other_y_offset = -1 # 다른 뿌요의 y 오프셋 (-1, 0, 1), 초기값은 위에 위치
        self.center_color_index = get_random_puyo_color_index()
        self.other_color_index = get_random_puyo_color_index()

    def get_positions(self):
        """현재 뿌요 쌍의 두 뿌요의 그리드 좌표 (x, y) 튜플 리스트를 반환"""
        center_pos = (self.center_x, self.center_y)
        other_pos = (self.center_x + self.other_x_offset, self.center_y + self.other_y_offset)
        return [center_pos, other_pos]

    def get_colors(self):
        """현재 뿌요 쌍의 두 뿌요의 색상 인덱스 리스트를 반환"""
        return [self.center_color_index, self.other_color_index]

    def move(self, dx, dy):
        """뿌요 쌍을 이동"""
        self.center_x += dx
        self.center_y += dy

    def rotate(self, grid):
        """뿌요 쌍을 시계 방향으로 회전"""
        # 현재 오프셋 저장
        old_other_x_offset = self.other_x_offset
        old_other_y_offset = self.other_y_offset

        # 회전 로직 (시계 방향)
        if old_other_x_offset == 0 and old_other_y_offset == -1: # 위 -> 오른쪽
            self.other_x_offset = 1
            self.other_y_offset = 0
        elif old_other_x_offset == 1 and old_other_y_offset == 0: # 오른쪽 -> 아래
            self.other_x_offset = 0
            self.other_y_offset = 1
        elif old_other_x_offset == 0 and old_other_y_offset == 1: # 아래 -> 왼쪽
            self.other_x_offset = -1
            self.other_y_offset = 0
        elif old_other_x_offset == -1 and old_other_y_offset == 0: # 왼쪽 -> 위
            self.other_x_offset = 0
            self.other_y_offset = -1

        # 회전 후 유효성 검사
        if not self.is_valid_position(grid):
            # 벽이나 다른 뿌요에 막혀 회전 불가 시, 벽 옆에서 회전 시도 (Wall Kick)
            # 1. 오른쪽으로 한 칸 이동 후 회전 시도
            self.center_x += 1
            if self.is_valid_position(grid):
                return # 성공
            self.center_x -= 1 # 원위치

            # 2. 왼쪽으로 한 칸 이동 후 회전 시도
            self.center_x -= 1
            if self.is_valid_position(grid):
                return # 성공
            self.center_x += 1 # 원위치

            # Wall Kick도 실패하면 회전 취소
            self.other_x_offset = old_other_x_offset
            self.other_y_offset = old_other_y_offset


    def is_valid_position(self, grid):
        """현재 뿌요 쌍의 위치가 유효한지 검사"""
        positions = self.get_positions()
        for x, y in positions:
            # 그리드 경계 체크
            if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT + 1):
                return False
            # 다른 뿌요와 충돌 체크 (y < GRID_HEIGHT+1 조건으로 맨 윗줄 위는 허용)
            if y < GRID_HEIGHT + 1 and grid[y][x] != 0:
                return False
        return True

def check_lost(locked_positions):
    """게임 오버 상태인지 확인 (맨 윗줄의 특정 칸에 뿌요가 있는지)"""
    # 일반적으로 뿌요뿌요는 왼쪽에서 3번째 칸(인덱스 2)이 막히면 게임 오버
    game_over_col = 2
    for x, y in locked_positions:
        if y == 0 and x == game_over_col: # 맨 윗줄(보이지 않는 줄)의 게임오버 칸
             return True
    return False

def find_connections(grid, x, y, visited):
    """
    주어진 좌표 (x, y)에서 시작하여 같은 색의 연결된 뿌요 그룹을 찾습니다.
    DFS (Depth-First Search) 사용.
    """
    if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT + 1) or \
       grid[y][x] == 0 or (x, y) in visited:
        return set()

    color_index = grid[y][x]
    connections = set([(x, y)])
    visited.add((x, y))

    # 상하좌우 인접 칸 탐색
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT + 1 and \
           grid[ny][nx] == color_index and (nx, ny) not in visited:
            connections.update(find_connections(grid, nx, ny, visited))

    return connections

def pop_puyos(grid, locked_positions):
    """
    연결된 뿌요 그룹(4개 이상)을 찾아 제거하고, 터진 뿌요 개수와 연쇄 수를 반환합니다.
    """
    popped_count = 0
    chain = 0
    popped_this_turn = set() # 이번 턴에 터진 뿌요 좌표 저장

    visited_total = set() # 전체 탐색 중 방문한 좌표

    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0 and (x, y) not in visited_total:
                visited_group = set() # 현재 그룹 탐색 중 방문한 좌표
                connections = find_connections(grid, x, y, visited_group)
                visited_total.update(visited_group) # 전체 방문 기록에 추가

                if len(connections) >= 4:
                    popped_this_turn.update(connections)

    if popped_this_turn:
        chain = 1 # 일단 터졌으면 1연쇄
        popped_count = len(popped_this_turn)
        for x, y in popped_this_turn:
            grid[y][x] = 0 # 그리드에서 제거
            if (x, y) in locked_positions:
                del locked_positions[(x, y)] # 고정된 뿌요 목록에서도 제거

    return popped_count, chain, popped_this_turn # 터진 뿌요 좌표 반환

def apply_gravity(grid, locked_positions):
    """
    뿌요를 아래로 떨어뜨립니다. 이동이 있었는지 여부를 반환합니다.
    """
    moved = False
    new_locked = {}
    # 아래 줄부터 위로 스캔
    for x in range(GRID_WIDTH):
        empty_space = GRID_HEIGHT # 현재 열에서 가장 낮은 빈 공간의 y 좌표
        for y in range(GRID_HEIGHT, -1, -1): # 맨 아래부터 위로
            if grid[y][x] == 0:
                # 빈 공간이면 empty_space 업데이트 (더 낮은 빈 공간 기록)
                empty_space = min(empty_space, y)
            elif empty_space > y: # 뿌요가 있고, 아래에 빈 공간이 있다면
                # 뿌요를 가장 낮은 빈 공간으로 이동
                color_index = grid[y][x]
                grid[empty_space][x] = color_index
                grid[y][x] = 0 # 원래 위치는 비움
                # locked_positions 업데이트 준비
                if (x, y) in locked_positions:
                    del locked_positions[(x, y)] # 기존 위치 제거
                new_locked[(x, empty_space)] = color_index # 새 위치 추가
                empty_space -= 1 # 다음 뿌요가 떨어질 위치 업데이트
                moved = True
            else: # 뿌요가 있고 아래 빈 공간이 없으면, 그 자리에 그대로 둠
                 if (x, y) in locked_positions:
                     new_locked[(x, y)] = locked_positions[(x, y)]
                 empty_space = y - 1 # 이 뿌요 바로 위가 다음 빈 공간 후보

    locked_positions.clear()
    locked_positions.update(new_locked)
    return moved

def calculate_score(popped_count, chain):
    """점수 계산 (단순화된 버전)"""
    base_score = popped_count * 10
    chain_bonus = (chain ** 2) * 50 # 연쇄 보너스
    return base_score + chain_bonus

def draw_grid_lines(surface):
    """게임 보드의 그리드 선을 그립니다."""
    for y in range(GRID_HEIGHT + 1): # +1 해서 맨 윗줄 경계도 그림
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + y * BLOCK_SIZE),
                         (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + y * BLOCK_SIZE))
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y),
                         (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

    # 게임 오버 라인 표시 (예: 1번째 줄 위)
    pygame.draw.line(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y + BLOCK_SIZE),
                     (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + BLOCK_SIZE), 2)
    # 게임 오버 트리거 칸 표시 (X 표시)
    game_over_col = 2
    pygame.draw.line(surface, RED, (TOP_LEFT_X + game_over_col * BLOCK_SIZE + 5, TOP_LEFT_Y + 5),
                        (TOP_LEFT_X + (game_over_col + 1) * BLOCK_SIZE - 5, TOP_LEFT_Y + BLOCK_SIZE - 5), 3)
    pygame.draw.line(surface, RED, (TOP_LEFT_X + game_over_col * BLOCK_SIZE + 5, TOP_LEFT_Y + BLOCK_SIZE - 5),
                        (TOP_LEFT_X + (game_over_col + 1) * BLOCK_SIZE - 5, TOP_LEFT_Y + 5), 3)


def draw_puyos(surface, grid):
    """그리드에 있는 뿌요들을 그립니다."""
    for y in range(GRID_HEIGHT + 1):
        for x in range(GRID_WIDTH):
            color_index = grid[y][x]
            if color_index > 0: # 색 인덱스가 0보다 크면 (뿌요가 있으면)
                color = PUYO_COLORS[color_index - 1] # 인덱스는 1부터 시작했으므로 -1
                # y 좌표는 1줄 위부터 그리므로 TOP_LEFT_Y에서 BLOCK_SIZE를 더함
                # 맨 윗줄(y=0)은 그리지 않음
                if y > 0:
                    pygame.draw.rect(surface, color,
                                     (TOP_LEFT_X + x * BLOCK_SIZE + 1,
                                      TOP_LEFT_Y + y * BLOCK_SIZE + 1,
                                      BLOCK_SIZE - 2, BLOCK_SIZE - 2), border_radius=5) # 약간 둥글게

def draw_current_puyo(surface, puyo_pair):
    """현재 조작 중인 뿌요 쌍을 그립니다."""
    positions = puyo_pair.get_positions()
    colors = puyo_pair.get_colors()
    for i, (x, y) in enumerate(positions):
        color_index = colors[i]
        color = PUYO_COLORS[color_index - 1]
        # 맨 윗줄(y=0)은 그리지 않음
        if y > 0:
            pygame.draw.rect(surface, color,
                             (TOP_LEFT_X + x * BLOCK_SIZE + 1,
                              TOP_LEFT_Y + y * BLOCK_SIZE + 1,
                              BLOCK_SIZE - 2, BLOCK_SIZE - 2), border_radius=5)

def draw_next_puyo(surface, puyo_pair):
    """'다음 뿌요'를 화면 오른쪽에 표시합니다."""
    label = small_font.render('Next', 1, WHITE)
    sx = TOP_LEFT_X + PLAY_WIDTH + 30
    sy = TOP_LEFT_Y + 50
    surface.blit(label, (sx, sy - 25))

    positions = puyo_pair.get_positions() # 상대 좌표 얻기 위함
    colors = puyo_pair.get_colors()

    # 다음 뿌요 표시 위치 조정 (상대 좌표 기준)
    base_x = sx + BLOCK_SIZE // 2
    base_y = sy + BLOCK_SIZE

    # 중심 뿌요 그리기
    center_color = PUYO_COLORS[puyo_pair.center_color_index - 1]
    pygame.draw.rect(surface, center_color,
                     (base_x, base_y, BLOCK_SIZE - 2, BLOCK_SIZE - 2), border_radius=5)

    # 다른 뿌요 그리기 (중심 기준 오프셋 적용)
    other_color = PUYO_COLORS[puyo_pair.other_color_index - 1]
    other_draw_x = base_x + puyo_pair.other_x_offset * BLOCK_SIZE
    other_draw_y = base_y + puyo_pair.other_y_offset * BLOCK_SIZE
    pygame.draw.rect(surface, other_color,
                     (other_draw_x, other_draw_y, BLOCK_SIZE - 2, BLOCK_SIZE - 2), border_radius=5)


def draw_window(surface, grid, current_puyo, next_puyo, current_score, paused_state, game_over_state):
    """게임 화면 전체를 그립니다."""
    surface.fill(BLACK) # 배경 채우기

    # 게임 제목
    title_label = game_over_font.render('PUYO PUYO', 1, WHITE)
    surface.blit(title_label, (SCREEN_WIDTH // 2 - title_label.get_width() // 2, 20))

    # 점수 표시
    score_label = score_font.render(f'Score: {current_score}', 1, WHITE)
    sx = TOP_LEFT_X + PLAY_WIDTH + 30
    sy = TOP_LEFT_Y + 150
    surface.blit(score_label, (sx, sy))

    # 게임 보드 테두리
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 2)

    # 그리드 선 그리기
    draw_grid_lines(surface)

    # 고정된 뿌요 그리기
    draw_puyos(surface, grid)

    # 현재 움직이는 뿌요 그리기 (게임오버 아닐 때)
    if not game_over_state and current_puyo:
        draw_current_puyo(surface, current_puyo)

    # 다음 뿌요 표시 (게임오버 아닐 때)
    if not game_over_state and next_puyo:
        draw_next_puyo(surface, next_puyo)

    # 게임 오버 메시지
    if game_over_state:
        game_over_label = game_over_font.render("GAME OVER", 1, RED)
        surface.blit(game_over_label, (SCREEN_WIDTH // 2 - game_over_label.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - game_over_label.get_height() // 2))
        restart_label = score_font.render("Press R to Restart", 1, WHITE)
        surface.blit(restart_label, (SCREEN_WIDTH // 2 - restart_label.get_width() // 2,
                                     SCREEN_HEIGHT // 2 + game_over_label.get_height()))

    # 일시정지 메시지
    if paused_state and not game_over_state:
        pause_label = game_over_font.render("PAUSED", 1, YELLOW)
        surface.blit(pause_label, (SCREEN_WIDTH // 2 - pause_label.get_width() // 2,
                                   SCREEN_HEIGHT // 2 - pause_label.get_height() // 2))

    pygame.display.update()

# --- 메인 게임 루프 ---
def main():
    global score, fall_speed, fall_time, level_time, game_over, paused

    locked_positions = {} # (x, y): color_index
    grid = create_grid(locked_positions)

    current_puyo = PuyoPair(GRID_WIDTH // 2 -1, 0) # 초기 위치 (중앙 상단)
    next_puyo = PuyoPair(GRID_WIDTH // 2 -1, 0)
    clock = pygame.time.Clock()

    change_puyo = False # 현재 뿌요를 고정하고 다음 뿌요로 바꿀지 여부
    is_chaining = False # 연쇄 반응 중인지 여부
    chain_count = 0 # 현재 연쇄 수

    run = True
    while run:
        grid = create_grid(locked_positions) # 매 프레임 그리드 업데이트
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick() # FPS 제한

        # --- 레벨 (속도 증가) ---
        # 예: 15초마다 속도 증가 (최소 속도 제한)
        if not game_over and not paused and level_time / 1000 > 15:
            level_time = 0
            fall_speed = max(0.1, fall_speed * 0.9) # 점점 빠르게, 최소 0.1초

        # --- 이벤트 처리 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r: # 재시작
                        # 게임 상태 초기화
                        locked_positions = {}
                        grid = create_grid(locked_positions)
                        current_puyo = PuyoPair(GRID_WIDTH // 2 -1, 0)
                        next_puyo = PuyoPair(GRID_WIDTH // 2 -1, 0)
                        score = 0
                        fall_speed = 0.5
                        fall_time = 0
                        level_time = 0
                        game_over = False
                        paused = False
                        is_chaining = False
                        chain_count = 0
                        continue # 다음 루프 반복으로

                elif event.key == pygame.K_p: # 일시정지 토글
                    paused = not paused

                if not paused and not game_over and not is_chaining: # 게임 진행 중에만 조작 가능
                    if event.key == pygame.K_LEFT:
                        current_puyo.move(-1, 0)
                        if not current_puyo.is_valid_position(grid):
                            current_puyo.move(1, 0) # 원위치
                    elif event.key == pygame.K_RIGHT:
                        current_puyo.move(1, 0)
                        if not current_puyo.is_valid_position(grid):
                            current_puyo.move(-1, 0) # 원위치
                    elif event.key == pygame.K_DOWN: # 아래로 빠르게 내리기
                        current_puyo.move(0, 1)
                        if not current_puyo.is_valid_position(grid):
                            current_puyo.move(0, -1) # 원위치
                            change_puyo = True # 바닥이나 다른 뿌요에 닿으면 고정
                        else:
                             fall_time = 0 # 수동으로 내리면 자동 하강 타이머 초기화
                    elif event.key == pygame.K_UP or event.key == pygame.K_x: # 회전 (위 또는 X키)
                        current_puyo.rotate(grid)
                    elif event.key == pygame.K_SPACE: # 하드 드롭
                        while current_puyo.is_valid_position(grid):
                            current_puyo.move(0, 1)
                        current_puyo.move(0, -1) # 마지막 유효 위치로 복구
                        change_puyo = True # 즉시 고정

        # --- 게임 로직 ---
        if not paused and not game_over:
            # 연쇄 반응 중이 아닐 때만 뿌요 자동 하강
            if not is_chaining:
                if fall_time / 1000 >= fall_speed:
                    fall_time = 0
                    current_puyo.move(0, 1)
                    if not current_puyo.is_valid_position(grid):
                        current_puyo.move(0, -1)
                        change_puyo = True # 바닥 또는 다른 뿌요 도달

            # 뿌요 고정 처리
            if change_puyo and not is_chaining:
                positions = current_puyo.get_positions()
                colors = current_puyo.get_colors()
                valid_landing = True
                for i, (x, y) in enumerate(positions):
                    # 뿌요가 그리드 밖(특히 위쪽)으로 나가면 고정 불가 (게임 오버 조건으로 이어질 수 있음)
                    if y < 0:
                         valid_landing = False
                         game_over = True # 맨 위에 닿으면 게임 오버
                         break
                    if y < GRID_HEIGHT + 1: # 그리드 내부에만 고정
                        locked_positions[(x, y)] = colors[i]
                    else: # 그리드 높이 초과 (이론상 발생하기 어려움)
                        valid_landing = False
                        game_over = True
                        break

                if valid_landing:
                    # 다음 뿌요 준비
                    current_puyo = next_puyo
                    next_puyo = PuyoPair(GRID_WIDTH // 2 -1, 0)
                    change_puyo = False
                    is_chaining = True # 뿌요가 놓였으므로 연쇄 확인 시작
                    chain_count = 0 # 연쇄 카운트 초기화
                else:
                    # 게임 오버 처리 (예: 잘못된 위치에 착지)
                    print("Game Over - Invalid Landing")
                    game_over = True


            # 연쇄 반응 처리
            if is_chaining:
                # 1. 중력 적용
                moved = apply_gravity(grid, locked_positions)

                # 2. 중력으로 움직임이 멈춘 후 연결 확인 및 터뜨리기
                if not moved:
                    popped_count, chain_increment, popped_coords = pop_puyos(grid, locked_positions)
                    if popped_count > 0:
                        chain_count += chain_increment # 연쇄 수 증가
                        score += calculate_score(popped_count, chain_count)
                        # 터진 후에는 다시 중력 적용부터 시작해야 하므로 moved=True 처리 효과
                        # (다음 루프에서 apply_gravity 다시 실행)
                        # 여기서 특별한 처리는 필요 없음. 다음 루프에서 apply_gravity가 호출됨.
                        # 효과음 재생 등 가능
                        # print(f"{chain_count} Chain! Popped: {popped_count}")
                    else:
                        # 더 이상 터질 뿌요가 없으면 연쇄 종료
                        is_chaining = False
                        chain_count = 0
                        # 게임 오버 체크 (뿌요가 놓인 직후 + 연쇄 종료 후)
                        if check_lost(locked_positions):
                             print("Game Over - Blocked Top")
                             game_over = True


        # --- 화면 그리기 ---
        draw_window(win, grid, current_puyo, next_puyo, score, paused, game_over)

    pygame.quit()
    sys.exit()

# --- 메인 메뉴 (선택 사항) ---
def main_menu():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Puyo Puyo Clone')
    run = True
    while run:
        win.fill(BLACK)
        title_font = pygame.font.SysFont('comicsans', 70)
        label_font = pygame.font.SysFont('comicsans', 40)

        title = title_font.render('PUYO PUYO', 1, WHITE)
        label = label_font.render('Press Any Key To Play', 1, WHITE)

        win.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()))
        win.blit(label, (SCREEN_WIDTH/2 - label.get_width()/2, SCREEN_HEIGHT/2 + 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main() # 게임 시작
            if event.type == pygame.MOUSEBUTTONDOWN:
                 main() # 게임 시작

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main_menu() # 메인 메뉴 시작
