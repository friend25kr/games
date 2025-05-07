import pygame
import random

# --- 기본 설정 ---
pygame.font.init()

# 화면 크기
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 게임 보드 너비 (10 블록 * 30)
PLAY_HEIGHT = 600 # 게임 보드 높이 (20 블록 * 30)
BLOCK_SIZE = 30

# 게임 보드 위치 계산
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50 # 상단 여백

# --- 테트로미노 모양 정의 ---
# 각 모양은 2D 리스트로 표현되며, 각 리스트는 회전 상태를 나타냅니다.
# '.'은 빈 공간, '0'은 블록을 의미합니다.
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# C = [['..0..',
#       '00000',
#       '..0..',
#       '.0.0.',
#       '0...0'],
#      ['0..0.',
#       '.0.0.',
#       '..000',
#       '.0.0.',
#       '0..0.'],
#      ['0...0',
#       '.0.0.',
#       '..0..',
#       '00000',
#       '..0..'],
#      ['.0..0',
#       '.0.0.',
#       '000..',
#       '.0.0.',
#       '.0..0']]

# 모양 리스트와 색상 정의
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# 인덱스 0 - 7은 shapes 리스트의 모양에 해당

# --- Piece 클래스 ---
class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # 현재 회전 상태

# --- 게임 함수 ---
def create_grid(locked_positions={}):
    """
    게임 보드 그리드를 생성합니다.
    locked_positions: 이미 블록이 고정된 위치 딕셔너리 {(x, y): (r, g, b)}
    """
    # 10x20 크기의 검은색 그리드 생성
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    # 고정된 블록 위치에 색상 적용
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

def convert_shape_format(piece):
    """
    Piece 객체의 모양 정보를 실제 그리드 좌표 리스트로 변환합니다.
    """
    positions = []
    # 현재 회전 상태에 맞는 모양 가져오기
    format = piece.shape[piece.rotation % len(piece.shape)]

    # 모양 문자열을 순회하며 '0'인 위치의 좌표 계산
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    # 좌표 보정 (모양 데이터의 좌상단 기준 -> 실제 그리드 기준)
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # 모양 정의 시 사용한 오프셋 제거

    return positions

def valid_space(piece, grid):
    """
    현재 Piece의 위치가 유효한지 (경계 내, 다른 블록과 겹치지 않는지) 확인합니다.
    """
    # 모든 빈 그리드 셀 좌표 생성 (0~9, 0~19)
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # 1차원 리스트로 변환
    accepted_positions = [j for sub in accepted_positions for j in sub]

    # 현재 Piece의 블록 좌표 가져오기
    formatted = convert_shape_format(piece)

    for pos in formatted:
        # 그리드 범위를 벗어나거나, 해당 위치가 비어있지 않으면 False
        if pos not in accepted_positions:
            if pos[1] > -1: # 화면 상단 위는 허용 (시작 위치)
                return False
    return True

def check_lost(positions):
    """
    게임 오버 상태인지 확인합니다 (블록이 맨 위 경계를 넘었는지).
    """
    for pos in positions:
        x, y = pos
        if y < 1: # y 좌표가 1보다 작으면 (맨 윗줄보다 위)
            return True
    return False

def get_shape():
    """
    새로운 Piece 객체를 랜덤하게 생성하여 반환합니다.
    """
    return Piece(5, 0, random.choice(shapes)) # 중앙 상단(x=5, y=0)에서 시작

def draw_text_middle(surface, text, size, color):
    """
    화면 중앙에 텍스트를 그립니다.
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2),
                         TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface, grid):
    """
    게임 보드의 그리드 선을 그립니다.
    """
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    # 가로선
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*BLOCK_SIZE), (sx+PLAY_WIDTH, sy+ i*BLOCK_SIZE))
    # 세로선
    for j in range(len(grid[0])):
         pygame.draw.line(surface, (128, 128, 128), (sx + j*BLOCK_SIZE, sy), (sx + j*BLOCK_SIZE, sy + PLAY_HEIGHT))

def clear_rows(grid, locked):
    """
    꽉 찬 가로줄을 찾아 제거하고, 위의 블록들을 아래로 내립니다. 점수를 반환합니다.
    """
    inc = 0 # 제거된 줄 수
    # 아래에서부터 위로 순회
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        # 현재 줄이 꽉 찼는지 확인 (검은색 블록이 없는지)
        if (0, 0, 0) not in row:
            inc += 1
            # 해당 줄의 locked_positions 제거
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # 제거된 줄이 있다면 위의 줄들을 아래로 이동
    if inc > 0:
        # locked_positions 딕셔너리를 y좌표 기준으로 정렬 (아래쪽 블록부터 처리)
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            # 제거된 줄(ind)보다 위에 있는 블록들만 이동
            if y < ind:
                newKey = (x, y + inc) # 제거된 줄 수만큼 아래로 이동
                locked[newKey] = locked.pop(key)
    return inc # 제거된 줄 수 반환 (점수 계산용)

def draw_next_shape(piece, surface):
    """
    '다음 블록'을 화면 오른쪽에 표시합니다.
    """
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    format = piece.shape[piece.rotation % len(piece.shape)]

    # 다음 블록 미리보기 그리기
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0, last_score=0):
    """
    게임 화면 전체를 그립니다 (배경, 보드, 블록, 텍스트 등).
    """
    surface.fill((0, 0, 0)) # 검은색 배경

    # 게임 제목
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    # 현재 점수
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # 최고 점수 (구현하려면 파일 저장/로드 필요)
    # label = font.render('High Score: ' + str(last_score), 1, (255,255,255))
    # sx = TOP_LEFT_X - 200
    # sy = TOP_LEFT_Y + 200
    # surface.blit(label, (sx + 20, sy + 160))


    # 게임 보드 그리기
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # 보드 테두리 그리기
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    # 그리드 선 그리기
    draw_grid(surface, grid)
    # pygame.display.update() # 여기서 업데이트하면 깜빡임 발생 가능

# --- 메인 게임 루프 ---
def main(win):
    last_score = 0 # 최고 점수 (여기서는 간단히 0으로 시작)
    locked_positions = {}  # 고정된 블록 위치
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27 # 블록 떨어지는 속도 (작을수록 빠름)
    level_time = 0
    score = 0

    while run:
        # 그리드 업데이트 (고정된 블록 반영)
        grid = create_grid(locked_positions)
        # 타이머 업데이트
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick() # FPS 제한

        # 레벨 (속도 증가)
        if level_time/1000 > 5: # 예: 5초마다 속도 증가
            level_time = 0
            if fall_speed > 0.12:
                 fall_speed -= 0.005

        # 블록 자동 하강
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            # 땅에 닿거나 다른 블록 위에 도달했는데 유효하지 않은 공간이면
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1 # 한 칸 위로 복구
                change_piece = True # 블록 고정 및 다음 블록으로 변경

        # 이벤트 처리 (키 입력 등)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    # 아래 방향키: 한 칸 아래로 이동
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP: # 회전
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        # 회전이 유효하지 않으면 원래대로 복구
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                # --- 스페이스바 하드 드롭 기능 추가 ---
                elif event.key == pygame.K_SPACE:
                    # 현재 위치에서 계속 아래로 이동 가능한지 확인하며 y 좌표 증가
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    # 더 이상 내려갈 수 없으면 한 칸 위로 복구 (마지막 유효 위치)
                    current_piece.y -= 1
                    # 블록을 즉시 고정하고 다음 블록 준비
                    change_piece = True
                # --- 기능 추가 끝 ---


        # 현재 블록의 그리드 상 위치 계산
        shape_pos = convert_shape_format(current_piece)

        # 현재 블록을 그리드에 임시로 그리기 (색상 적용)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: # 그리드 범위 내에 있을 때만
                 grid[y][x] = current_piece.color

        # 블록이 바닥에 닿으면 (change_piece == True)
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color # 블록 위치 고정
            current_piece = next_piece # 다음 블록을 현재 블록으로
            next_piece = get_shape() # 새로운 다음 블록 생성
            change_piece = False
            # 줄 제거 처리 및 점수 추가
            # clear_rows 함수는 grid와 locked_positions를 모두 업데이트해야 함
            cleared_rows_count = clear_rows(grid, locked_positions) # grid 업데이트 반영 위해 수정
            score += cleared_rows_count * 10 # 줄당 10점
            # grid = create_grid(locked_positions) # clear_rows 후 grid 다시 생성 (선택적)


        # 화면 그리기
        draw_window(win, grid, score, last_score)
        # 다음 블록 표시
        draw_next_shape(next_piece, win)
        # 화면 업데이트
        pygame.display.update()

        # 게임 오버 확인
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500) # 잠시 대기
            run = False
            # update_score(score) # 최고 점수 업데이트 (필요시 구현)

# --- 메인 메뉴 ---
def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win) # 게임 시작
    pygame.quit()

# --- 게임 실행 ---
if __name__ == '__main__':
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_menu(win)  # 메인 메뉴 시작
