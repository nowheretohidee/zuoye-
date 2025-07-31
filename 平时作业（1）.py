import pygame
import sys
import numpy as np
import os
from pygame.locals import *
pygame.init()
BOARD_SIZE = 15  # 15x15的棋盘
GRID_SIZE = 40  # 每个格子的像素大小
MARGIN = 50  # 边距
PIECE_RADIUS = 18  # 棋子半径
WINDOW_SIZE = BOARD_SIZE * GRID_SIZE + 2 * MARGIN
FPS = 66
BACKGROUND = (220, 179, 92)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LINE_COLOR = (0, 0, 0)
HIGHLIGHT = (255, 215, 0)
DIALOG_BG = (240, 240, 240)
DIALOG_BORDER = (50, 50, 50)
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("五子棋")
# 加载中文字体
try:
    font_paths = [
        'C:/Windows/Fonts/simhei.ttf',  # Windows 黑体
        'C:/Windows/Fonts/simsun.ttc',  # Windows 宋体
        '/System/Library/Fonts/PingFang.ttc',  # macOS 苹方
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'  # Linux
    ]
    title_font = None
    status_font = None
    dialog_font = None
    for path in font_paths:
        if os.path.exists(path):
            title_font = pygame.font.Font(path, 36)
            status_font = pygame.font.Font(path, 24)
            dialog_font = pygame.font.Font(path, 28)
            break
except Exception as e:
    print(f"字体加载错误: {e}")
    title_font = pygame.font.SysFont(None, 36)
    status_font = pygame.font.SysFont(None, 24)
    dialog_font = pygame.font.SysFont(None, 28)
# 游戏状态
class GameState:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)  # 0: 空, 1: 黑, 2: 白
        self.current_player = 1  # 1: 黑棋, 2: 白棋
        self.game_over = False
        self.winner = 0
        self.last_move = None
    def place_piece(self, row, col):
        # 如果位置有效且为空
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            self.last_move = (row, col)
            # 检查是否获胜
            if self.check_win(row, col):
                self.game_over = True
                self.winner = self.current_player
            else:
                # 切换玩家
                self.current_player = 3 - self.current_player  # 1->2, 2->1
            return True
        return False
    def check_win(self, row, col):
        player = self.board[row][col]
        # 检查方向: 水平, 垂直, 对角线, 反对角线
        directions = [
            [(0, 1), (0, -1)],  #
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]
        for direction_pair in directions:
            count = 1  # 当前位置的棋子
            # 检查两个相反方向
            for dx, dy in direction_pair:
                temp_row, temp_col = row, col
                # 沿着一个方向计数
                for _ in range(4):  # 最多检查4个位置
                    temp_row += dx
                    temp_col += dy
                    if (0 <= temp_row < BOARD_SIZE and
                            0 <= temp_col < BOARD_SIZE and
                            self.board[temp_row][temp_col] == player):
                        count += 1
                    else:
                        break
            # 如果有5个连续的棋子
            if count >= 5:
                return True
        return False
    def reset(self):
        self.__init__()
# 创建游戏状态
game = GameState()
# 绘制棋盘
def draw_board():
    screen.fill(BACKGROUND)
    # 绘制网格线
    for i in range(BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (MARGIN, MARGIN + i * GRID_SIZE),
            (WINDOW_SIZE - MARGIN, MARGIN + i * GRID_SIZE),
            2
        )
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (MARGIN + i * GRID_SIZE, MARGIN),
            (MARGIN + i * GRID_SIZE, WINDOW_SIZE - MARGIN),
            2
        )

    # 绘制天元和星位
    star_points = [3, 7, 11]
    for i in star_points:
        for j in star_points:
            pygame.draw.circle(
                screen,
                BLACK,
                (MARGIN + i * GRID_SIZE, MARGIN + j * GRID_SIZE),
                5
            )
    # 绘制最后落子位置的标记
    if game.last_move:
        row, col = game.last_move
        pygame.draw.circle(
            screen,
            HIGHLIGHT,
            (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
            5
        )
# 绘制棋子
def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game.board[row][col] == 1:  # 黑棋
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                    PIECE_RADIUS
                )
            elif game.board[row][col] == 2:  # 白棋
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                    PIECE_RADIUS
                )
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE),
                    PIECE_RADIUS,
                    1
                )
# 显示游戏状态
def show_game_status():
    if game.game_over:
        winner = "黑方" if game.winner == 1 else "白方"
        text = title_font.render(f"{winner}获胜!", True, RED)
    else:
        player = "黑方" if game.current_player == 1 else "白方"
        text = status_font.render(f"当前回合: {player}", True, BLACK)

    screen.blit(text, (20, 20))
# 显示操作提示
def show_instructions():
    instructions = [
        "操作说明:",
        "左键: 黑方落子",
        "右键: 白方落子",
        "ESC键: 退出游戏"
    ]
    # 计算提示框大小
    max_width = 0
    for line in instructions:
        text = status_font.render(line, True, BLACK)
        if text.get_width() > max_width:
            max_width = text.get_width()
    # 绘制文本
    for i, line in enumerate(instructions):
        text = status_font.render(line, True, BLACK)
        screen.blit(text, (WINDOW_SIZE - max_width - 30, 25 + i * 30))
# 显示胜利对话框
def show_win_dialog():
    winner = "黑方" if game.winner == 1 else "白方"
    # 绘制对话框
    dialog_rect = pygame.Rect(WINDOW_SIZE // 2 - 150, WINDOW_SIZE // 2 - 75, 300, 150)
    pygame.draw.rect(screen, DIALOG_BG, dialog_rect)
    pygame.draw.rect(screen, DIALOG_BORDER, dialog_rect, 3)
    # 显示文本
    title_text = title_font.render("游戏结束", True, RED)
    winner_text = dialog_font.render(f"{winner}获胜!", True, BLACK)

    screen.blit(title_text, (dialog_rect.centerx - title_text.get_width() // 2, dialog_rect.top + 20))
    screen.blit(winner_text, (dialog_rect.centerx - winner_text.get_width() // 2, dialog_rect.top + 60))
    screen.blit(restart_text, (dialog_rect.centerx - restart_text.get_width() // 2, dialog_rect.top + 100))
# 主游戏循环
def main():
    clock = pygame.time.Clock()
    # 绘制初始界面
    draw_board()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r:
                    game.reset()

            if not game.game_over:
                if event.type == MOUSEBUTTONDOWN:
                    # 获取鼠标位置并转换为棋盘坐标
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = round((mouse_x - MARGIN) / GRID_SIZE)
                    row = round((mouse_y - MARGIN) / GRID_SIZE)
                    # 左键: 黑棋
                    if event.button == 1 and game.current_player == 1:
                        game.place_piece(row, col)
                    # 右键: 白棋
                    elif event.button == 3 and game.current_player == 2:
                        game.place_piece(row, col)
        # 绘制游戏
        draw_board()
        draw_pieces()
        show_game_status()
        show_instructions()

        if game.game_over:
            show_win_dialog()

        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    main()