#----------------------------
# Gobang-wuziqi
# author: NUAA-XSF
#----------------------------

import pygame
import random
import os
import sys

WIDTH = 800
HEIGHT = 800
FPS = 30

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
INTERSECTION = 19
BLOCK_SIZE = 40

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Gobang-wuziqi')
clock = pygame.time.Clock()

abs_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(abs_dir, 'img')
font_dir = os.path.join(abs_dir, 'font')
snd_dir = os.path.join(abs_dir,'snd')

background = pygame.image.load(os.path.join(img_dir,'starfield.png')).convert()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
background_rect = background.get_rect()
drop_piece_snd = pygame.mixer.Sound(os.path.join(snd_dir, 'Pickup_Coin3.wav'))

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(os.path.join(font_dir, 'SourceHanSansSC-Normal.otf'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_start_screen(surf):
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        draw_text(surf, '五子棋', 40, WIDTH/2, HEIGHT * 1 / 4)
        draw_text(surf, '黑棋先手', 26, WIDTH/2, HEIGHT * 1 / 3)
        draw_text(surf, '按任意键开始游戏', 30 , WIDTH/2, HEIGHT * 1 / 2)
        pygame.display.flip()


def show_end_screen(surf, winner):
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        draw_text(surf, 'game over', 40, WIDTH/2, HEIGHT * 1 / 4)
        draw_text(surf, '黑棋获胜' if winner==1 else '白棋获胜', 26, WIDTH/2, HEIGHT * 1 / 3)
        draw_text(surf, '按任意键开始游戏', 30 , WIDTH/2, HEIGHT * 1 / 2)
        pygame.display.flip()

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((220,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.midtop = (WIDTH / 2, 5)

        self.back_button = pygame.Surface((80,30))
        self.back_button.set_colorkey(BLACK)
        self.back_rect = self.back_button.get_rect()
        draw_text(self.back_button, '悔   棋', 20, self.back_rect.width / 2, 1)
        self.image.blit(self.back_button, self.back_rect)

        self.which_button = pygame.Surface((80,30))
        self.which_button.set_colorkey(BLACK)
        self.which_rect = self.which_button.get_rect()
        self.which_rect.x = 140
        draw_text(self.which_button, '黑棋下', 20, self.back_rect.width / 2, 1)
        self.image.blit(self.which_button, self.which_rect)


    def update(self):

        self.which_button.fill(BLACK)
        # self.which_button.set_colorkey(BLACK)
        self.which_rect = self.which_button.get_rect()
        self.which_rect.x = 140
        draw_text(self.which_button, '黑棋下' if checker_board.turn == 1 else '白棋下', 20, self.back_rect.width / 2, 1)
        self.image.fill(BLACK, rect=self.which_rect)
        self.image.blit(self.which_button, self.which_rect)

    def check_button(self,checker_board, pos):
        track_pos = checker_board.track_pos
        turn = checker_board.turn
        state = checker_board.state
        back_button_rect_abs = pygame.Rect(self.rect.x, self.rect.y, 80, 20)
        if back_button_rect_abs.collidepoint(pos) and track_pos:
            if track_pos[-1][2] == turn:
                x, y = track_pos[-1][0], track_pos[-1][1]
                track_pos.pop()
                state[x][y] = 0

            if track_pos[-1][2] != turn:
                x, y = track_pos[-1][0], track_pos[-1][1]
                track_pos.pop()
                state[x][y] = 0
                if track_pos:
                    x, y = track_pos[-1][0], track_pos[-1][1]
                    track_pos.pop()
                    state[x][y] = 0

class CheckerBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.board_image = pygame.image.load(os.path.join(img_dir,'checkerboard.png')).convert()
        self.image = pygame.Surface((self.board_image.get_width(), self.board_image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.state = [ [0 for y in range(INTERSECTION)]  for x  in range(INTERSECTION)]
        self.turn = 1
        self.piece_radius = 18
        self.game_over = False
        self.last_win = pygame.time.get_ticks()
        self.track_pos = []

    def update(self):
        circle = pygame.draw.circle
        image = self.image
        piece_radius = self.piece_radius
        state = self.state
        self.image.blit(self.board_image, (0, 0))
        for x in range(INTERSECTION):
            for y in range(INTERSECTION):
                if state[x][y] == 1:
                    circle(image, BLACK, (x*40, y*40), piece_radius)
                if state[x][y] == 2:
                    circle(image, WHITE, (x*40, y*40), piece_radius)
        if self.game_over and pygame.time.get_ticks() - self.last_win > 3000:
            self.kill()

    def update_state(self, pos):
        if not self.game_over:
            if self.rect.collidepoint(pos):
                x, y = pos
                x, y = x-self.rect.left, y-self.rect.top
                m, n= x % 40, y % 40
                h, k = x // 40, y // 40
                px = py = -1
                if m < 15:
                    px = h
                if m > 25:
                    px = h + 1
                if n < 15:
                    py = k
                if n > 25:
                    py = k + 1

                if px >= 0 and py >= 0 and self.state[px][py] == 0:
                    self.state[px][py] = self.turn
                    self.track_pos.append([px, py, self.turn])
                    drop_piece_snd.play()

                    if self.check_win(px, py):
                        self.game_over = True
                        self.last_win = pygame.time.get_ticks()

    def check_win(self, x, y):
        state = self.state
        turn = self.turn

        # 左右方向
        length = 0
        for l in range(-1,-5,-1):
            if x+l >= 0:
                if state[x+l][y] != turn:
                    break
                else:
                    length += 1

        for r in range(1,5):
            if x+r <= INTERSECTION-1:
                if state[x+r][y] != turn:
                    break
                else:
                    length += 1
        if length+1 >= 5:
            # print(turn , 'win')
            return True

        # 上下方向
        length = 0
        for t in range(-1,-5,-1):
            if y+t >= 0:
                if state[x][y+t] != turn:
                    break
                else:
                    length += 1

        for b in range(1,5):
            if y+b <= INTERSECTION-1:
                if state[x][y+b] != turn:
                    break
                else:
                    length += 1
        if length+1 >= 5:
            return True

        # 右斜方向
        length = 0
        for rt in range(1,5):
            if y-rt >= 0 and x+rt <= INTERSECTION-1:
                if state[x+rt][y-rt] != turn:
                    break
                else:
                    length += 1

        for lb in range(1,5):
            if x-lb >=0 and y+lb <= INTERSECTION-1:
                if state[x-lb][y+lb] != turn:
                    break
                else:
                    length += 1
        if length+1 >= 5:
            return True

        # 左斜方向
        length = 0
        for lt in range(1,5):
            if y-lt >= 0 and x-lt >=0:
                if state[x-lt][y-lt] != turn:
                    break
                else:
                    length += 1

        for rb in range(1,5):
            if x+rb <=INTERSECTION-1 and y+rb <= INTERSECTION-1:
                if state[x+rb][y+rb] != turn:
                    break
                else:
                    length += 1
        if length+1 >= 5:
            return True

        self.turn = 2 if turn == 1 else 1

        return False

all_sprites = pygame.sprite.Group()
checker_board = CheckerBoard()
menu = Menu()
all_sprites.add(checker_board)
all_sprites.add(menu)
# Game loop
show_start_screen(screen)
running = True
while running:
    # keep loop runing at the ringht speed
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                checker_board.update_state(event.pos)
                menu.check_button(checker_board, event.pos)

    # Updata
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()
    if checker_board.game_over and not checker_board.alive():
        show_end_screen(screen, checker_board.turn)
        checker_board = CheckerBoard()
        all_sprites.add(checker_board)

pygame.quit()
