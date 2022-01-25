import sys
import sqlite3

import pygame
import copy

# списки координат снарядов в 1 и в 2 уровнях
CIRCLES = []
CIRCLES_level_2 = []

CIRCLES_LEVEL_1_TANK_ANGRY_1 = []
CIRCLES_LEVEL_1_TANK_ANGRY_2 = []
CIRCLES_LEVEL_1_TANK_ANGRY_3 = []

CIRCLES_LEVEL_2_TANK_ANGRY_1 = []
CIRCLES_LEVEL_2_TANK_ANGRY_2 = []
CIRCLES_LEVEL_2_TANK_ANGRY_3 = []
CIRCLES_LEVEL_2_TANK_ANGRY_4 = []
CIRCLES_LEVEL_2_TANK_ANGRY_5 = []

con = sqlite3.connect("result_player.db")  # Открываю базу данных
cur = con.cursor()


class Main:
    def __init__(self):
        self.board = [[0] * width for _ in range(height)]
        # открываю изображения
        image = pygame.image.load("f5fef-tank-143400_1920.jpg")
        self.global_image_tank = pygame.transform.scale(image, (1920, 1080))
        self.global_image_level_1 = pygame.image.load('снимок экрана 2022-01-06 162258.png')
        self.global_image_level_2 = pygame.image.load('снимок экрана 2022-01-06 164142.png')
        self.count = 0
        # Флаги для того чтобы узнать какая сечас открыта страница
        self.flag_main = True
        self.flag_info = False
        self.flag_level_1 = False
        self.flag_level_2 = False
        self.con = sqlite3.connect("result_player.db")  # Открываю базу данных
        self.cur = self.con.cursor()

    def djl(self, screen):
        # Добавляю изаображения и тест для главного экрана
        screen.blit(self.global_image_tank, (0, 0))
        screen.blit(self.global_image_level_1, (1000, 600))
        screen.blit(self.global_image_level_2, (1000, 725))
        pygame.draw.circle(screen, pygame.Color('blue'), (230, 150), 15)
        font = pygame.font.Font(None, 40)
        text_question = font.render("?", True, pygame.Color('white'))
        screen.blit(text_question, (221, 138))
        font = pygame.font.Font(None, 80)
        text_question = font.render("Выберите уровень", True, pygame.Color('red'))
        screen.blit(text_question, (1000, 535))

        # Осуществляю показ и поиск бышвих результатов игроков
        pygame.draw.rect(screen, pygame.Color('black'), (250, 750, 300, 200))
        pygame.draw.rect(screen, pygame.Color('black'), (600, 750, 300, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (250, 750, 300, 200), 3)
        pygame.draw.rect(screen, pygame.Color('green'), (600, 750, 300, 200), 3)
        font = pygame.font.Font(None, 40)
        text_level_1 = font.render("level_1:", True, pygame.Color('white'))
        text_level_2 = font.render("level_2:", True, pygame.Color('white'))
        screen.blit(text_level_1, (255, 755))
        screen.blit(text_level_2, (601, 755))
        minutes_level_1 = self.cur.execute(f"""SELECT l.minutes FROM level_1 AS l""").fetchall()
        seconds_level_1 = self.cur.execute(f"""SELECT l.minutes FROM level_1 AS l""").fetchall()
        minutes_level_2 = self.cur.execute(f"""SELECT l.minutes FROM level_2 AS l""").fetchall()
        seconds_level_2 = self.cur.execute(f"""SELECT l.minutes FROM level_2 AS l""").fetchall()
        m_s_level_1 = [(minutes_level_1[i][0], seconds_level_1[i][0]) for i in range(len(minutes_level_1))]
        m_s_level_2 = [(minutes_level_2[i][0], seconds_level_2[i][0]) for i in range(len(minutes_level_2))]
        font = pygame.font.Font(None, 30)
        m_s_level_1.sort()
        m_s_level_2.sort()
        count = 0
        for i in range(len(m_s_level_1)):
            if i > 5:
                break
            text = font.render(f'{m_s_level_1[i][0]}.{m_s_level_1[i][1]}', True, pygame.Color('white'))
            screen.blit(text, (255, 800 + count))
            count += 20
        count = 0
        for i in range(len(m_s_level_2)):
            if i > 5:
                break
            text = font.render(f'{m_s_level_2[i][0]}.{m_s_level_2[i][1]}', True, pygame.Color('white'))
            screen.blit(text, (605, 800 + count))
            count += 20

    def get_click(self, pos):
        # Функция для того чтобы узнать на какую кнопку нажал пользователь
        x = pos[0]
        y = pos[1]
        if self.count == 0 or self.count == 1:
            if 218 <= x <= 241 and 138 <= y <= 161:
                self.count = 1
                if self.flag_info:
                    self.flag_info = False
                else:
                    self.flag_info = True
            elif 1100 <= x <= 1600 and 620 <= y <= 700:
                self.count = 2
                self.flag_level_1 = True
            elif 1100 <= x <= 1600 and 745 <= y <= 825:
                self.count = 3
                self.flag_level_2 = True
        elif self.count == 2:
            if (1665 <= x <= 1695 and 140 <= y <= 185) or (1100 <= x <= 1210 and 490 <= y <= 550):
                self.count = 0
                self.flag_level_1 = False
            if 700 <= x <= 790 and 490 <= y <= 550:
                level_1.restart()
        elif self.count == 3:
            if (1665 <= x <= 1695 and 140 <= y <= 185) or (1100 <= x <= 1210 and 490 <= y <= 550):
                self.count = 0
                self.flag_level_2 = False
            if 700 <= x <= 790 and 490 <= y <= 550:
                level_2.restart()

    def search_click(self):
        return self.count

    def flag(self, name):
        # Функция для того чтобы узнать какое окно открыто
        if name == 'main':
            return self.flag_main
        elif name == 'info':
            return self.flag_info
        elif name == 'level_1':
            return self.flag_level_1
        elif name == 'level_2':
            return self.flag_level_2

    def flag_change(self, name):
        # Измена статуса окон
        if name == 'main':
            self.flag_main = False
        elif name == 'info':
            self.flag_info = False
        elif name == 'level_1':
            self.flag_level_1 = False
        elif name == 'level_2':
            self.flag_level_2 = False


class Info(Main):
    def __init__(self):
        super().__init__()
        # Класс с окном для изображения информауии о игре

    def render(self, screen):
        # Созда. дизайн и текст окна
        pygame.draw.rect(screen, (0, 0, 0), (250, 150, 500, 300))
        pygame.draw.rect(screen, (0, 255, 0), (249, 149, 502, 302), 3)
        font = pygame.font.Font(None, 25)
        text_1 = font.render("Эта игра создана для развлечений, чтобы ", True, pygame.Color('green'))
        text_2 = font.render("проводить своё свободное время с весельем.", True, pygame.Color('green'))
        text_3 = font.render("В этой игре нужно выбрать уровень, пока их два,", True, pygame.Color('green'))
        text_4 = font.render("а затем начать играть, что не составит труда,", True, pygame.Color('green'))
        text_5 = font.render("передвижение и стрельба осуществляется с помощью", True, pygame.Color('green'))
        text_6 = font.render("клавиатуры.", True, pygame.Color('green'))
        text_7 = font.render("Чтобы закрыть это окно ещё раз нажмите на кнопку ", True, pygame.Color('green'))
        text_8 = font.render("об информации.", True, pygame.Color('green'))
        screen.blit(text_1, (255, 155))
        screen.blit(text_2, (255, 185))
        screen.blit(text_3, (255, 215))
        screen.blit(text_4, (255, 245))
        screen.blit(text_5, (255, 275))
        screen.blit(text_6, (255, 305))
        screen.blit(text_7, (255, 370))
        screen.blit(text_8, (255, 400))


class Level_1(Main):
    def __init__(self):
        super().__init__()
        # Класс первого уровня
        # ДОбавляю изображения всех сотрон таноков и обозночаю координаты препятсвий
        self.botton_exit = pygame.image.load('Снимок экрана 2022-01-08 112056.png')
        self.tank_forward = pygame.image.load('танк forward.png')
        self.tank_bottom = pygame.image.load('танк bottom.png')
        self.tank_right = pygame.image.load('танк right.png')
        self.tank_left = pygame.image.load('танк left.png')
        self.coordinates_tank = (220, 135)
        self.image_common = pygame.image.load('танк bottom.png')
        self.x = [(320, 328), (1610, 1618), (1610, 1618), (1450, 1705), (425, 545), (665, 785), (370, 620), (800, 1030),
                  (1300, 1530), (605, 705), (810, 940), (1105, 1315), (1055, 1175), (1400, 1500)]
        self.y = [(135, 230), (135, 230), (855, 945), (500, 508), (135, 325), (135, 280), (665, 945), (795, 945),
                  (745, 945), (470, 550), (385, 585), (320, 440), (550, 675), (520, 570)]
        self.flag_side_tank = 'bottom'
        self.tank_angry_1_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_1_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_1_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_1_left = pygame.image.load('вражеский танк left.png')
        self.tank_angry_2_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_2_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_2_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_2_left = pygame.image.load('вражеский танк left.png')
        self.tank_angry_3_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_3_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_3_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_3_left = pygame.image.load('вражеский танк left.png')
        self.coordinates_tank_angry_1 = (1618, 135)
        self.coordinates_tank_angry_2 = (1618, 135)
        self.coordinates_tank_angry_3 = (1618, 135)
        self.image_common_angry_1 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_2 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_3 = pygame.image.load('вражеский танк bottom.png')
        self.f = True
        # Жизнь таннков
        self.xp_tank = 1000
        self.xp_tank_angry_1 = 500
        self.xp_tank_angry_2 = 500
        self.xp_tank_angry_3 = 500
        self.flag_live_tank = True
        self.flag_live_tank_angry_1 = True
        self.flag_live_tank_angry_2 = True
        self.flag_live_tank_angry_3 = True

    def render(self, screen):
        # Функция для дизайна главного экрана
        for x in range(215, 1706, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (x, 135), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (x, 945), 5)

        for y in range(135, 946, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (215, y), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (1705, y), 5)

        screen.blit(self.botton_exit, (1665, 140))
        pygame.draw.rect(screen, (0, 255, 0), (1665, 140, 30, 45), 2)
        pygame.draw.line(screen, pygame.Color('green'), (320, 135), (320, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 135), (1610, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 855), (1610, 945), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1450, 500), (1705, 500), 8)
        pygame.draw.rect(screen, pygame.Color('green'), (425, 135, 120, 190))
        pygame.draw.rect(screen, pygame.Color('green'), (665, 135, 120, 145))
        pygame.draw.rect(screen, pygame.Color('green'), (370, 665, 250, 280))
        pygame.draw.rect(screen, pygame.Color('green'), (800, 795, 230, 150))
        pygame.draw.rect(screen, pygame.Color('green'), (1300, 745, 230, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (605, 470, 100, 80))
        pygame.draw.rect(screen, pygame.Color('green'), (810, 385, 130, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (1105, 320, 210, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1055, 550, 120, 125))
        pygame.draw.rect(screen, pygame.Color('green'), (1400, 520, 100, 50))

        if self.flag_live_tank:
            screen.blit(self.image_common, self.coordinates_tank)
        if self.flag_live_tank_angry_1:
            screen.blit(self.image_common_angry_1, self.coordinates_tank_angry_1)
        if self.flag_live_tank_angry_2:
            screen.blit(self.image_common_angry_2, self.coordinates_tank_angry_2)
        if self.flag_live_tank_angry_3:
            screen.blit(self.image_common_angry_3, self.coordinates_tank_angry_3)

    def defeat(self, screen):
        # Функция для дизайна окна после смерти
        for x in range(215, 1706, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (x, 135), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (x, 945), 5)

        for y in range(135, 946, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (215, y), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (1705, y), 5)

        screen.blit(self.botton_exit, (1665, 140))
        pygame.draw.rect(screen, (0, 255, 0), (1665, 140, 30, 45), 2)
        pygame.draw.line(screen, pygame.Color('green'), (320, 135), (320, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 135), (1610, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 855), (1610, 945), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1450, 500), (1705, 500), 8)
        pygame.draw.rect(screen, pygame.Color('green'), (425, 135, 120, 190))
        pygame.draw.rect(screen, pygame.Color('green'), (665, 135, 120, 145))
        pygame.draw.rect(screen, pygame.Color('green'), (370, 665, 250, 280))
        pygame.draw.rect(screen, pygame.Color('green'), (800, 795, 230, 150))
        pygame.draw.rect(screen, pygame.Color('green'), (1300, 745, 230, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (605, 470, 100, 80))
        pygame.draw.rect(screen, pygame.Color('green'), (810, 385, 130, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (1105, 320, 210, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1055, 550, 120, 125))
        pygame.draw.rect(screen, pygame.Color('green'), (1400, 520, 100, 50))

        pygame.draw.rect(screen, pygame.Color('red'), (660, 255, 600, 300))
        font = pygame.font.Font(None, 80)
        text_1 = font.render("Вы хотите начать", True, pygame.Color('black'))
        text_2 = font.render('сначала?', True, pygame.Color('black'))
        text_3 = font.render("ДА", True, pygame.Color('blue'))
        text_4 = font.render("НЕТ", True, pygame.Color('blue'))
        screen.blit(text_1, (720, 255))
        screen.blit(text_2, (820, 340))
        screen.blit(text_3, (700, 490))
        screen.blit(text_4, (1100, 490))
        pygame.draw.rect(screen, pygame.Color('green'), (700, 490, 90, 60), 2)
        pygame.draw.rect(screen, pygame.Color('green'), (1100, 490, 110, 60), 2)

    def win(self, screen):
        # Функция для отображения окна после победы
        for x in range(215, 1706, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (x, 135), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (x, 945), 5)

        for y in range(135, 946, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (215, y), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (1705, y), 5)

        screen.blit(self.botton_exit, (1665, 140))
        pygame.draw.rect(screen, (0, 255, 0), (1665, 140, 30, 45), 2)
        pygame.draw.line(screen, pygame.Color('green'), (320, 135), (320, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 135), (1610, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 855), (1610, 945), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1450, 500), (1705, 500), 8)
        pygame.draw.rect(screen, pygame.Color('green'), (425, 135, 120, 190))
        pygame.draw.rect(screen, pygame.Color('green'), (665, 135, 120, 145))
        pygame.draw.rect(screen, pygame.Color('green'), (370, 665, 250, 280))
        pygame.draw.rect(screen, pygame.Color('green'), (800, 795, 230, 150))
        pygame.draw.rect(screen, pygame.Color('green'), (1300, 745, 230, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (605, 470, 100, 80))
        pygame.draw.rect(screen, pygame.Color('green'), (810, 385, 130, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (1105, 320, 210, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1055, 550, 120, 125))
        pygame.draw.rect(screen, pygame.Color('green'), (1400, 520, 100, 50))

        pygame.draw.rect(screen, pygame.Color('red'), (660, 255, 600, 300))
        font = pygame.font.Font(None, 80)
        text_1 = font.render("Вы одержали", True, pygame.Color('black'))
        text_2 = font.render("победу!", True, pygame.Color('black'))
        text_3 = font.render('хотите начать', True, pygame.Color('black'))
        text_4 = font.render('сначала?', True, pygame.Color('black'))
        text_5 = font.render("ДА", True, pygame.Color('blue'))
        text_6 = font.render("НЕТ", True, pygame.Color('blue'))
        screen.blit(text_1, (770, 255))
        screen.blit(text_2, (835, 315))
        screen.blit(text_3, (770, 375))
        screen.blit(text_4, (835, 435))
        screen.blit(text_5, (700, 490))
        screen.blit(text_6, (1100, 490))
        pygame.draw.rect(screen, pygame.Color('green'), (700, 490, 90, 60), 2)
        pygame.draw.rect(screen, pygame.Color('green'), (1100, 490, 110, 60), 2)

    def forward(self, screen):
        # Фуекция передвижения игрока на вверх
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if y - 1 > 135:
            for i in range(len(self.x)):
                if self.x[i][0] <= x + 73 and x <= self.x[i][1] and self.y[i][0] <= y - 1 <= self.y[i][1]:
                    f = False
            if f:
                y -= 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_forward, self.coordinates_tank)
                self.image_common = self.tank_forward
                self.flag_side_tank = 'forward'

    def bottom(self, screen):
        # Функция передвиженрия игрока вниз
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if y + 1 < 848:
            for i in range(len(self.x)):
                if self.x[i][0] <= x + 72 and x <= self.x[i][1] and self.y[i][0] <= y + 1 + 97 <= self.y[i][1]:
                    f = False
            if f:
                y += 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_bottom, self.coordinates_tank)
                self.image_common = self.tank_bottom
                self.flag_side_tank = 'bottom'

    def left(self, screen):
        # Функция передвижения игрока в лево
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if x - 1 > 220:
            for i in range(len(self.x)):
                if self.x[i][0] <= x - 1 <= self.x[i][1] and self.y[i][0] <= y + 72 and y <= self.y[i][1]:
                    f = False
            if f:
                x -= 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_left, self.coordinates_tank)
                self.image_common = self.tank_left
                self.flag_side_tank = 'left'

    def right(self, screen):
        # Функция для передвижения игрока в право
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if x + 1 < 1620:
            for i in range(len(self.x)):
                if self.x[i][0] <= x + 1 + 92 <= self.x[i][1] and self.y[i][0] <= y + 71 and y <= self.y[i][1]:
                    f = False
            if f:
                x += 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_right, self.coordinates_tank)
                self.image_common = self.tank_right
                self.flag_side_tank = 'right'

    def shooting_click(self, screen):
        # Добавляем снаряд в спиоск
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        if self.flag_side_tank == 'forward':
            CIRCLES.append((x, y, 'forward'))
        elif self.flag_side_tank == 'bottom':
            CIRCLES.append((x, y, 'bottom'))
        elif self.flag_side_tank == 'left':
            CIRCLES.append((x, y, 'left'))
        elif self.flag_side_tank == 'right':
            CIRCLES.append((x, y, 'right'))

    def shooting(self, screen):
        # Функция для осущетвления стрельбы
        deleted = []
        x_angry_tank_1 = self.coordinates_tank_angry_1[0]
        y_angry_tank_1 = self.coordinates_tank_angry_1[1]
        x_angry_tank_2 = self.coordinates_tank_angry_2[0]
        y_angry_tank_2 = self.coordinates_tank_angry_2[1]
        x_angry_tank_3 = self.coordinates_tank_angry_3[0]
        y_angry_tank_3 = self.coordinates_tank_angry_3[1]
        for i in range(len(CIRCLES)):
            if CIRCLES[i][2] == 'forward':
                x = CIRCLES[i][0]
                y = CIRCLES[i][1]
                f = True
                if y - 1 > 135:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x + 39 <= self.x[j][1] and self.y[j][0] <= y - 1 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x + 39 <= x_angry_tank_1 + 98 and \
                            y_angry_tank_1 + 72 == y - 1:
                        self.xp_tank_angry_1 -= 100
                        f = False
                    if x_angry_tank_2 <= x + 39 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y - 1 <= y_angry_tank_2 + 97:
                        self.xp_tank_angry_2 -= 100
                        f = False
                    if x_angry_tank_3 <= x + 39 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y - 1 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if f:
                        y -= 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x + 39, y), 5)
                        CIRCLES[i] = (x, y, 'forward')
                    else:
                        deleted.append(CIRCLES[i])
            elif CIRCLES[i][2] == 'right':
                x = CIRCLES[i][0]
                y = CIRCLES[i][1]
                f = True
                if x + 1 < 1620:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x + 1 + 97 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x + 1 <= x_angry_tank_1 + 98 and \
                            y_angry_tank_1 <= y + 35 <= y_angry_tank_1 + 72:
                        self.xp_tank_angry_1 -= 100
                        f = False
                    if x_angry_tank_2 <= x + 1 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y + 35 <= y_angry_tank_2 + 97:
                        self.xp_tank_angry_2 -= 100
                        f = False
                    if x_angry_tank_3 <= x + 1 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y + 35 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if f:
                        x += 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x + 97, y + 35), 5)
                        CIRCLES[i] = (x, y, 'right')
                    else:
                        deleted.append(CIRCLES[i])
            elif CIRCLES[i][2] == 'bottom':
                x = CIRCLES[i][0]
                y = CIRCLES[i][1]
                f = True
                if y + 1 < 848:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 1 + 96 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x + 39 <= x_angry_tank_1 + 98 and \
                            y_angry_tank_1 <= y + 1 <= y_angry_tank_1 + 72:
                        f = False
                        self.xp_tank_angry_1 -= 100
                    if x_angry_tank_2 <= x + 39 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y + 1 <= y_angry_tank_2 + 97:
                        f = False
                        self.xp_tank_angry_2 -= 100
                    if x_angry_tank_3 <= x + 39 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y + 1 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if f:
                        y += 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x + 36, y + 96), 5)
                        CIRCLES[i] = (x, y, 'bottom')
                    else:
                        deleted.append(CIRCLES[i])
            elif CIRCLES[i][2] == 'left':
                x = CIRCLES[i][0]
                y = CIRCLES[i][1]
                f = True
                if x - 1 > 220:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x - 1 <= x_angry_tank_1 + 98 and \
                            y_angry_tank_1 <= y + 36 <= y_angry_tank_1 + 72:
                        f = False
                        self.xp_tank_angry_1 -= 100
                    if x_angry_tank_2 <= x - 1 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y + 36 <= y_angry_tank_2 + 97:
                        f = False
                        self.xp_tank_angry_2 -= 100
                    if x_angry_tank_3 <= x - 1 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y + 36 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if f:
                        x -= 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x, y + 36), 5)
                        CIRCLES[i] = (x, y, 'left')
                    else:
                        deleted.append(CIRCLES[i])
        for i in deleted:
            index = CIRCLES.index(i)
            CIRCLES.pop(index)

    def common_angry_tank_1(self, screen):
        # Функция для передвижения вражеского танка
        x = self.coordinates_tank_angry_1[0]
        y = self.coordinates_tank_angry_1[1]
        f = True
        if y + 1 + 97 < 500:
            y += 1
            self.coordinates_tank_angry_1 = (x, y)
        else:
            if x - 1 > 1315 and self.f:
                x -= 1
                self.coordinates_tank_angry_1 = (x, y)
                self.image_common_angry_1 = self.tank_angry_1_left
            else:
                if y + 1 + 97 < 745:
                    y += 1
                    self.coordinates_tank_angry_1 = (x, y)
                    self.image_common_angry_1 = self.tank_angry_1_bottom
                    self.f = False
                else:
                    if x + 1 + 92 < 1705:
                        x += 1
                        self.coordinates_tank_angry_1 = (x, y)
                        self.image_common_angry_1 = self.tank_angry_1_right
                    else:
                        self.image_common_angry_1 = self.tank_angry_1_left

    def common_angry_tank_2(self, screen):
        # Функция для передвижения вражеского танка
        x = self.coordinates_tank_angry_2[0]
        y = self.coordinates_tank_angry_2[1]
        if y + 1 < 230:
            y += 1
            self.coordinates_tank_angry_2 = (x, y)
            self.image_common_angry_2 = self.tank_angry_2_bottom
        else:
            if x - 1 > 940:
                x -= 1
                self.coordinates_tank_angry_2 = (x, y)
                self.image_common_angry_2 = self.tank_angry_2_left
            else:
                self.image_common_angry_2 = self.tank_angry_2_bottom

    def common_angry_tank_3(self, screen):
        # Функция для передвижения вражеского танка
        x = self.coordinates_tank_angry_3[0]
        y = self.coordinates_tank_angry_3[1]
        if y + 1 + 97 < 500:
            y += 1
            self.coordinates_tank_angry_3 = (x, y)
        else:
            if x - 1 > 1315:
                x -= 1
                self.coordinates_tank_angry_3 = (x, y)
                self.image_common_angry_3 = self.tank_angry_3_left
            else:
                if y + 1 + 97 < 675:
                    y += 1
                    self.coordinates_tank_angry_3 = (x, y)
                    self.image_common_angry_3 = self.tank_angry_3_bottom
                else:
                    if x - 1 > 1175:
                        x -= 1
                        self.coordinates_tank_angry_3 = (x, y)
                        self.image_common_angry_3 = self.tank_angry_3_left
                    else:
                        self.image_common_angry_3 = self.tank_angry_3_bottom

    def shooting_tank_angry_1_click(self, screen):
        # Функция нахождения игрока в зоне стрельбы
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_1[0]
        y_tank_angry = self.coordinates_tank_angry_1[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_1_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_1 = self.tank_angry_1_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_1_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_1 = self.tank_angry_1_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_1_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_1 = self.tank_angry_1_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_1_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_1 = self.tank_angry_1_right

    def shooting_tank_angry_2_click(self, screen):
        # Функция нахождения игрока в зоне стрельбы
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_2[0]
        y_tank_angry = self.coordinates_tank_angry_2[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_1_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_2 = self.tank_angry_2_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_1_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_2 = self.tank_angry_2_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_1_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_2 = self.tank_angry_2_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_1_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_2 = self.tank_angry_2_right

    def shooting_tank_angry_3_click(self, screen):
        # Функция нахождения игрока в зоне стрельбы
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_3[0]
        y_tank_angry = self.coordinates_tank_angry_3[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_1_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_3 = self.tank_angry_3_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_1_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_3 = self.tank_angry_3_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_1_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_3 = self.tank_angry_3_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_1_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_3 = self.tank_angry_3_right

    def shooting_tank_angry_1(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_1_TANK_ANGRY_1)):
            if CIRCLES_LEVEL_1_TANK_ANGRY_1[i][2] == 'bottom':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_1[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_1[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_1[i][2] == 'forward':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_1[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_1[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_1[i][2] == 'right':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_1[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_1[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_1[i][2] == 'left':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_1[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_1[i])
        for i in deleted:
            index = CIRCLES_LEVEL_1_TANK_ANGRY_1.index(i)
            CIRCLES_LEVEL_1_TANK_ANGRY_1.pop(index)

    def shooting_tank_angry_2(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_1_TANK_ANGRY_2)):
            if CIRCLES_LEVEL_1_TANK_ANGRY_2[i][2] == 'bottom':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_2[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_2[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_2[i][2] == 'forward':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_2[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_2[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_2[i][2] == 'right':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_2[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_2[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_2[i][2] == 'left':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_2[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_2[i])
        for i in deleted:
            index = CIRCLES_LEVEL_1_TANK_ANGRY_2.index(i)
            CIRCLES_LEVEL_1_TANK_ANGRY_2.pop(index)

    def shooting_tank_angry_3(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_1_TANK_ANGRY_3)):
            if CIRCLES_LEVEL_1_TANK_ANGRY_3[i][2] == 'bottom':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_3[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_3[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_3[i][2] == 'forward':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_3[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_3[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_3[i][2] == 'right':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_3[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_3[i])
            elif CIRCLES_LEVEL_1_TANK_ANGRY_3[i][2] == 'left':
                x = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_1_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_1_TANK_ANGRY_3[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_1_TANK_ANGRY_3[i])
        for i in deleted:
            index = CIRCLES_LEVEL_1_TANK_ANGRY_3.index(i)
            CIRCLES_LEVEL_1_TANK_ANGRY_3.pop(index)

    def search_xp_healthy(self):
        # Функция для проверки жизни танков
        if self.xp_tank <= 0:
            self.flag_live_tank = False
        if self.xp_tank_angry_1 <= 0:
            self.flag_live_tank_angry_1 = False
        if self.xp_tank_angry_2 <= 0:
            self.flag_live_tank_angry_2 = False
        if self.xp_tank_angry_3 <= 0:
            self.flag_live_tank_angry_3 = False

    def restart(self):
        # Функция перезапуска
        self.coordinates_tank = (220, 135)
        self.image_common = pygame.image.load('танк bottom.png')
        self.flag_side_tank = 'bottom'
        self.coordinates_tank_angry_1 = (1618, 135)
        self.coordinates_tank_angry_2 = (1618, 135)
        self.coordinates_tank_angry_3 = (1618, 135)
        self.image_common_angry_1 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_2 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_3 = pygame.image.load('вражеский танк bottom.png')
        self.f = True
        self.xp_tank = 1000
        self.xp_tank_angry_1 = 500
        self.xp_tank_angry_2 = 500
        self.xp_tank_angry_3 = 500
        self.flag_live_tank = True
        self.flag_live_tank_angry_1 = True
        self.flag_live_tank_angry_2 = True
        self.flag_live_tank_angry_3 = True

    def research_win(self):
        # Функция проверки жизни вражеских танков
        if not (self.flag_live_tank_angry_1) and not (self.flag_live_tank_angry_2) and not (
        self.flag_live_tank_angry_3):
            return False
        else:
            return True

    def display_time(self, time_s, screen):
        # Функция таймера
        # time string with tents of seconds
        time_str = str(int(time_s * 10) / 10)
        font = pygame.font.Font(None, 30)
        label = font.render(f"Time : {time_str}", 1, pygame.Color('red'))
        screen.blit(label, (230, 900))


class Level_2(Main):
    def __init__(self):
        super().__init__()
        # Класс второго уровня
        # ДОбавляю изображения всех сотрон таноков и обозночаю координаты препятсвий
        self.botton_exit = pygame.image.load('Снимок экрана 2022-01-08 112056.png')
        self.tank_forward = pygame.image.load('танк forward.png')
        self.tank_bottom = pygame.image.load('танк bottom.png')
        self.tank_right = pygame.image.load('танк right.png')
        self.tank_left = pygame.image.load('танк left.png')
        self.coordinates_tank = (220, 135)
        self.image_common = pygame.image.load('танк bottom.png')
        self.x = [(320, 328), (1610, 1618), (1610, 1618), (960, 974), (960, 974), (215, 515), (625, 775), (215, 565),
                  (1065, 1185), (1290, 1495), (645, 775), (1079, 1229), (1205, 1485), (1365, 1565)]
        self.y = [(135, 230), (135, 230), (855, 945), (135, 335), (745, 945), (485, 494), (135, 305), (745, 825),
                  (825, 945), (815, 845), (485, 660), (240, 360), (465, 625), (135, 305)]
        self.flag_side_tank = 'bottom'
        self.tank_angry_1_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_1_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_1_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_1_left = pygame.image.load('вражеский танк left.png')
        self.tank_angry_2_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_2_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_2_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_2_left = pygame.image.load('вражеский танк left.png')
        self.tank_angry_3_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_3_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_3_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_3_left = pygame.image.load('вражеский танк left.png')
        self.tank_angry_4_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_4_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_4_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_4_left = pygame.image.load('вражеский танк left.png')
        self.tank_angry_5_forward = pygame.image.load('вражеский танк forward.png')
        self.tank_angry_5_bottom = pygame.image.load('вражеский танк bottom.png')
        self.tank_angry_5_right = pygame.image.load('вражеский танк right.png')
        self.tank_angry_5_left = pygame.image.load('вражеский танк left.png')
        self.coordinates_tank_angry_1 = (1618, 135)
        self.coordinates_tank_angry_2 = (1618, 135)
        self.coordinates_tank_angry_3 = (1618, 135)
        self.coordinates_tank_angry_4 = (1618, 135)
        self.coordinates_tank_angry_5 = (1618, 135)
        self.image_common_angry_1 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_2 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_3 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_4 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_5 = pygame.image.load('вражеский танк bottom.png')
        self.f = True
        # Жизнь танков
        self.xp_tank = 1000
        self.xp_tank_angry_1 = 500
        self.xp_tank_angry_2 = 500
        self.xp_tank_angry_3 = 500
        self.xp_tank_angry_4 = 500
        self.xp_tank_angry_5 = 500
        self.flag_live_tank = True
        self.flag_live_tank_angry_1 = True
        self.flag_live_tank_angry_2 = True
        self.flag_live_tank_angry_3 = True
        self.flag_live_tank_angry_4 = True
        self.flag_live_tank_angry_5 = True

    def render(self, screen):
        # Функция для дизайна главного экрана
        for x in range(215, 1706, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (x, 135), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (x, 945), 5)

        for y in range(135, 946, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (215, y), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (1705, y), 5)

        screen.blit(self.botton_exit, (1665, 140))
        pygame.draw.rect(screen, (0, 255, 0), (1665, 140, 30, 45), 2)
        pygame.draw.line(screen, pygame.Color('green'), (320, 135), (320, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 135), (1610, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 855), (1610, 945), 8)

        pygame.draw.line(screen, pygame.Color('green'), (960, 135), (960, 335), 14)
        pygame.draw.line(screen, pygame.Color('green'), (960, 745), (960, 945), 14)

        pygame.draw.line(screen, pygame.Color('green'), (215, 485), (515, 485), 8)

        pygame.draw.circle(screen, pygame.Color('green'), (960, 535), 70)

        pygame.draw.rect(screen, pygame.Color('green'), (625, 135, 150, 170))
        pygame.draw.rect(screen, pygame.Color('green'), (215, 745, 350, 80))
        pygame.draw.rect(screen, pygame.Color('green'), (1065, 825, 120, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1290, 815, 205, 130))
        pygame.draw.rect(screen, pygame.Color('green'), (645, 485, 130, 175))
        pygame.draw.rect(screen, pygame.Color('green'), (1079, 240, 150, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1205, 465, 280, 160))
        pygame.draw.rect(screen, pygame.Color('green'), (1365, 135, 200, 170))

        if self.flag_live_tank:
            screen.blit(self.image_common, self.coordinates_tank)
        if self.flag_live_tank_angry_1:
            screen.blit(self.image_common_angry_1, self.coordinates_tank_angry_1)
        if self.flag_live_tank_angry_2:
            screen.blit(self.image_common_angry_2, self.coordinates_tank_angry_2)
        if self.flag_live_tank_angry_3:
            screen.blit(self.image_common_angry_3, self.coordinates_tank_angry_3)
        if self.flag_live_tank_angry_4:
            screen.blit(self.image_common_angry_4, self.coordinates_tank_angry_4)
        if self.flag_live_tank_angry_5:
            screen.blit(self.image_common_angry_5, self.coordinates_tank_angry_5)

    def defeat(self, screen):
        # Функция для дизайна экрана после смерти
        for x in range(215, 1706, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (x, 135), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (x, 945), 5)

        for y in range(135, 946, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (215, y), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (1705, y), 5)

        screen.blit(self.botton_exit, (1665, 140))
        pygame.draw.rect(screen, (0, 255, 0), (1665, 140, 30, 45), 2)
        pygame.draw.line(screen, pygame.Color('green'), (320, 135), (320, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 135), (1610, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 855), (1610, 945), 8)

        pygame.draw.line(screen, pygame.Color('green'), (960, 135), (960, 335), 14)
        pygame.draw.line(screen, pygame.Color('green'), (960, 745), (960, 945), 14)

        pygame.draw.line(screen, pygame.Color('green'), (215, 485), (515, 485), 8)

        pygame.draw.circle(screen, pygame.Color('green'), (960, 535), 70)

        pygame.draw.rect(screen, pygame.Color('green'), (625, 135, 150, 170))
        pygame.draw.rect(screen, pygame.Color('green'), (215, 745, 350, 80))
        pygame.draw.rect(screen, pygame.Color('green'), (1065, 825, 120, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1290, 815, 205, 130))
        pygame.draw.rect(screen, pygame.Color('green'), (645, 485, 130, 175))
        pygame.draw.rect(screen, pygame.Color('green'), (1079, 240, 150, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1205, 465, 280, 160))
        pygame.draw.rect(screen, pygame.Color('green'), (1365, 135, 200, 170))

        pygame.draw.rect(screen, pygame.Color('red'), (660, 255, 600, 300))
        font = pygame.font.Font(None, 80)
        text_1 = font.render("Вы хотите начать", True, pygame.Color('black'))
        text_2 = font.render('сначала?', True, pygame.Color('black'))
        text_3 = font.render("ДА", True, pygame.Color('blue'))
        text_4 = font.render("НЕТ", True, pygame.Color('blue'))
        screen.blit(text_1, (720, 255))
        screen.blit(text_2, (820, 340))
        screen.blit(text_3, (700, 490))
        screen.blit(text_4, (1100, 490))
        pygame.draw.rect(screen, pygame.Color('green'), (700, 490, 90, 60), 2)
        pygame.draw.rect(screen, pygame.Color('green'), (1100, 490, 110, 60), 2)

    def win(self, screen):
        # Функция дизайна после победы
        for x in range(215, 1706, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (x, 135), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (x, 945), 5)

        for y in range(135, 946, 10):
            pygame.draw.circle(screen, pygame.Color('green'), (215, y), 5)
            pygame.draw.circle(screen, pygame.Color('green'), (1705, y), 5)

        screen.blit(self.botton_exit, (1665, 140))
        pygame.draw.rect(screen, (0, 255, 0), (1665, 140, 30, 45), 2)
        pygame.draw.line(screen, pygame.Color('green'), (320, 135), (320, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 135), (1610, 230), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1610, 855), (1610, 945), 8)
        pygame.draw.line(screen, pygame.Color('green'), (1450, 500), (1705, 500), 8)
        pygame.draw.rect(screen, pygame.Color('green'), (425, 135, 120, 190))
        pygame.draw.rect(screen, pygame.Color('green'), (665, 135, 120, 145))
        pygame.draw.rect(screen, pygame.Color('green'), (370, 665, 250, 280))
        pygame.draw.rect(screen, pygame.Color('green'), (800, 795, 230, 150))
        pygame.draw.rect(screen, pygame.Color('green'), (1300, 745, 230, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (605, 470, 100, 80))
        pygame.draw.rect(screen, pygame.Color('green'), (810, 385, 130, 200))
        pygame.draw.rect(screen, pygame.Color('green'), (1105, 320, 210, 120))
        pygame.draw.rect(screen, pygame.Color('green'), (1055, 550, 120, 125))
        pygame.draw.rect(screen, pygame.Color('green'), (1400, 520, 100, 50))

        pygame.draw.rect(screen, pygame.Color('red'), (660, 255, 600, 300))
        font = pygame.font.Font(None, 80)
        text_1 = font.render("Вы одержали", True, pygame.Color('black'))
        text_2 = font.render("победу!", True, pygame.Color('black'))
        text_3 = font.render('хотите начать', True, pygame.Color('black'))
        text_4 = font.render('сначала?', True, pygame.Color('black'))
        text_5 = font.render("ДА", True, pygame.Color('blue'))
        text_6 = font.render("НЕТ", True, pygame.Color('blue'))
        screen.blit(text_1, (770, 255))
        screen.blit(text_2, (835, 315))
        screen.blit(text_3, (770, 375))
        screen.blit(text_4, (835, 435))
        screen.blit(text_5, (700, 490))
        screen.blit(text_6, (1100, 490))
        pygame.draw.rect(screen, pygame.Color('green'), (700, 490, 90, 60), 2)
        pygame.draw.rect(screen, pygame.Color('green'), (1100, 490, 110, 60), 2)

    def forward(self, screen):
        # Функция для передвижения игрока вверх
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if y - 1 > 135:
            for i in range(len(self.x)):
                if self.x[i][0] <= x + 73 and x <= self.x[i][1] and self.y[i][0] <= y - 1 <= self.y[i][1]:
                    f = False
            if f:
                y -= 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_forward, self.coordinates_tank)
                self.image_common = self.tank_forward
                self.flag_side_tank = 'forward'

    def bottom(self, screen):
        # Функция для передвижения игрока вниз
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if y + 1 < 848:
            for i in range(len(self.x)):
                if self.x[i][0] <= x + 72 and x <= self.x[i][1] and self.y[i][0] <= y + 1 + 97 <= self.y[i][1]:
                    f = False
            if f:
                y += 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_bottom, self.coordinates_tank)
                self.image_common = self.tank_bottom
                self.flag_side_tank = 'bottom'

    def left(self, screen):
        # Функция для передвижения игрока в лево
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if x - 1 > 220:
            for i in range(len(self.x)):
                if self.x[i][0] <= x - 1 <= self.x[i][1] and self.y[i][0] <= y + 72 and y <= self.y[i][1]:
                    f = False
            if f:
                x -= 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_left, self.coordinates_tank)
                self.image_common = self.tank_left
                self.flag_side_tank = 'left'

    def right(self, screen):
        # Функция предвижения игрока в лево
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        f = True
        if x + 1 < 1620:
            for i in range(len(self.x)):
                if self.x[i][0] <= x + 1 + 92 <= self.x[i][1] and self.y[i][0] <= y + 71 and y <= self.y[i][1]:
                    f = False
            if f:
                x += 1
                self.coordinates_tank = (x, y)
                screen.blit(self.tank_right, self.coordinates_tank)
                self.image_common = self.tank_right
                self.flag_side_tank = 'right'

    def shooting_click(self, screen):
        # Функция для добавления снаряда в список
        x = self.coordinates_tank[0]
        y = self.coordinates_tank[1]
        if self.flag_side_tank == 'forward':
            CIRCLES_level_2.append((x, y, 'forward'))
        elif self.flag_side_tank == 'bottom':
            CIRCLES_level_2.append((x, y, 'bottom'))
        elif self.flag_side_tank == 'left':
            CIRCLES_level_2.append((x, y, 'left'))
        elif self.flag_side_tank == 'right':
            CIRCLES_level_2.append((x, y, 'right'))

    def shooting(self, screen):
        # Функция для стрельбы игрока
        deleted = []
        x_angry_tank_1 = self.coordinates_tank_angry_1[0]
        y_angry_tank_1 = self.coordinates_tank_angry_1[1]
        x_angry_tank_2 = self.coordinates_tank_angry_2[0]
        y_angry_tank_2 = self.coordinates_tank_angry_2[1]
        x_angry_tank_3 = self.coordinates_tank_angry_3[0]
        y_angry_tank_3 = self.coordinates_tank_angry_3[1]
        x_angry_tank_4 = self.coordinates_tank_angry_4[0]
        y_angry_tank_4 = self.coordinates_tank_angry_4[1]
        x_angry_tank_5 = self.coordinates_tank_angry_5[0]
        y_angry_tank_5 = self.coordinates_tank_angry_5[1]
        for i in range(len(CIRCLES_level_2)):
            if CIRCLES_level_2[i][2] == 'forward':
                x = CIRCLES_level_2[i][0]
                y = CIRCLES_level_2[i][1]
                f = True
                if y - 1 > 135:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x + 39 <= self.x[j][1] and self.y[j][0] <= y - 1 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x + 39 <= x_angry_tank_1 + 72 and \
                            y_angry_tank_1 <= y - 1 <= y_angry_tank_1 + 97:
                        self.xp_tank_angry_1 -= 100
                        f = False
                    if x_angry_tank_2 <= x + 39 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y - 1 <= y_angry_tank_2 + 97:
                        self.xp_tank_angry_2 -= 100
                        f = False
                    if x_angry_tank_3 <= x + 39 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y - 1 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if x_angry_tank_4 <= x + 39 <= x_angry_tank_4 + 72 and \
                            y_angry_tank_4 <= y - 1 <= y_angry_tank_4 + 97:
                        self.xp_tank_angry_4 -= 100
                        f = False
                    if x_angry_tank_5 <= x + 39 <= x_angry_tank_5 + 72 and \
                            y_angry_tank_5 <= y - 1 <= y_angry_tank_5 + 97:
                        f = False
                        self.xp_tank_angry_5 -= 100
                    if f:
                        y -= 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x + 39, y), 5)
                        CIRCLES_level_2[i] = (x, y, 'forward')
                    else:
                        deleted.append(CIRCLES_level_2[i])
            elif CIRCLES_level_2[i][2] == 'right':
                x = CIRCLES_level_2[i][0]
                y = CIRCLES_level_2[i][1]
                f = True
                if x + 1 < 1620:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x + 1 + 97 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x + 1 <= x_angry_tank_1 + 72 and \
                            y_angry_tank_1 <= y + 35 <= y_angry_tank_1 + 97:
                        self.xp_tank_angry_1 -= 100
                        f = False
                    if x_angry_tank_2 <= x + 1 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y + 35 <= y_angry_tank_2 + 97:
                        self.xp_tank_angry_2 -= 100
                        f = False
                    if x_angry_tank_3 <= x + 1 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y + 35 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if x_angry_tank_4 <= x + 1 + 97 \
                            <= x_angry_tank_4 + 72 and \
                            y_angry_tank_4 <= y + 35 <= y_angry_tank_4 + 97:
                        self.xp_tank_angry_4 -= 100
                        f = False
                    if x_angry_tank_5 <= x + 1 <= x_angry_tank_5 + 72 and \
                            y_angry_tank_5 <= y + 35 <= y_angry_tank_5 + 97:
                        f = False
                        self.xp_tank_angry_5 -= 100
                    if f:
                        x += 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x + 97, y + 35), 5)
                        CIRCLES_level_2[i] = (x, y, 'right')
                    else:
                        deleted.append(CIRCLES_level_2[i])
            elif CIRCLES_level_2[i][2] == 'bottom':
                x = CIRCLES_level_2[i][0]
                y = CIRCLES_level_2[i][1]
                f = True
                if y + 1 < 848:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 1 + 96 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x + 36 <= x_angry_tank_1 + 72 and \
                            y_angry_tank_1 <= y + 1 <= y_angry_tank_1 + 97:
                        self.xp_tank_angry_1 -= 100
                        f = False
                    if x_angry_tank_2 <= x + 36 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y + 1 <= y_angry_tank_2 + 97:
                        self.xp_tank_angry_2 -= 100
                        f = False
                    if x_angry_tank_3 <= x + 36 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y + 1 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if x_angry_tank_4 <= x + 36 <= x_angry_tank_4 + 72 and \
                            y_angry_tank_4 <= y + 1 <= y_angry_tank_4 + 97:
                        self.xp_tank_angry_4 -= 100
                        f = False
                    if x_angry_tank_5 <= x + 36 <= x_angry_tank_5 + 72 and \
                            y_angry_tank_5 <= y + 1 <= y_angry_tank_5 + 97:
                        f = False
                        self.xp_tank_angry_5 -= 100
                    if f:
                        y += 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x + 36, y + 96), 5)
                        CIRCLES_level_2[i] = (x, y, 'bottom')
                    else:
                        deleted.append(CIRCLES_level_2[i])
            elif CIRCLES_level_2[i][2] == 'left':
                x = CIRCLES_level_2[i][0]
                y = CIRCLES_level_2[i][1]
                f = True
                if x - 1 > 220:
                    for j in range(len(self.x)):
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    if x_angry_tank_1 <= x - 1 <= x_angry_tank_1 + 72 and \
                            y_angry_tank_1 <= y + 36 <= y_angry_tank_1 + 97:
                        self.xp_tank_angry_1 -= 100
                        f = False
                    if x_angry_tank_2 <= x - 1 <= x_angry_tank_2 + 72 and \
                            y_angry_tank_2 <= y + 36 <= y_angry_tank_2 + 97:
                        self.xp_tank_angry_2 -= 100
                        f = False
                    if x_angry_tank_3 <= x - 1 <= x_angry_tank_3 + 72 and \
                            y_angry_tank_3 <= y + 36 <= y_angry_tank_3 + 97:
                        f = False
                        self.xp_tank_angry_3 -= 100
                    if x_angry_tank_4 <= x - 1 <= x_angry_tank_4 + 72 and \
                            y_angry_tank_4 <= y + 36 <= y_angry_tank_4 + 97:
                        self.xp_tank_angry_4 -= 100
                        f = False
                    if x_angry_tank_5 <= x - 1 <= x_angry_tank_5 + 72 and \
                            y_angry_tank_5 <= y + 36 <= y_angry_tank_5 + 97:
                        f = False
                        self.xp_tank_angry_5 -= 100
                    if f:
                        x -= 1
                        pygame.draw.circle(screen, pygame.Color('white'), (x, y + 36), 5)
                        CIRCLES_level_2[i] = (x, y, 'left')
                    else:
                        deleted.append(CIRCLES_level_2[i])
        for i in deleted:
            index = CIRCLES_level_2.index(i)
            CIRCLES_level_2.pop(index)

    def common_angry_tank_1(self, scrren):
        # Функция передвижения вражеского танка
        x = self.coordinates_tank_angry_1[0]
        y = self.coordinates_tank_angry_1[1]
        if y + 1 + 95 < 550:
            y += 1
            self.coordinates_tank_angry_1 = (x, y)
            self.image_common_angry_1 = self.tank_angry_1_bottom

    def common_angry_tank_2(self, screen):
        # Функция передвижения вражеского танка
        x = self.coordinates_tank_angry_2[0]
        y = self.coordinates_tank_angry_2[1]
        if y + 1 < 306:
            y += 1
            self.coordinates_tank_angry_2 = (x, y)
            self.image_common_angry_2 = self.tank_angry_2_bottom
        else:
            if x - 1 > 1485:
                x -= 1
                self.coordinates_tank_angry_2 = (x, y)
                self.image_common_angry_2 = self.tank_angry_2_left
            else:
                if y + 1 + 95 < 625:
                    y += 1
                    self.coordinates_tank_angry_2 = (x, y)
                    self.image_common_angry_2 = self.tank_angry_2_bottom

    def common_angry_tank_3(self, screen):
        # Функция передвижения вражеского танка
        x = self.coordinates_tank_angry_3[0]
        y = self.coordinates_tank_angry_3[1]
        if y + 1 < 360 and self.f:
            y += 1
            self.coordinates_tank_angry_3 = (x, y)
            self.image_common_angry_3 = self.tank_angry_3_bottom
        else:
            if x - 1 > 966:
                x -= 1
                self.coordinates_tank_angry_3 = (x, y)
                self.image_common_angry_3 = self.tank_angry_3_left
                self.f = False
            else:
                if y - 1 > 135:
                    y -= 1
                    self.coordinates_tank_angry_3 = (x, y)
                    self.image_common_angry_3 = self.tank_angry_3_forward
                else:
                    self.image_common_angry_3 = self.tank_angry_3_bottom

    def common_angry_tank_4(self, screen):
        # Функция передвижения вражеского танка
        x = self.coordinates_tank_angry_4[0]
        y = self.coordinates_tank_angry_4[1]
        if y + 1 + 95 < 465:
            y += 1
            self.coordinates_tank_angry_4 = (x, y)
            self.image_common_angry_4 = self.tank_angry_4_bottom
        else:
            if x - 1 + 92 > 1205:
                x -= 1
                self.coordinates_tank_angry_4 = (x, y)
                self.image_common_angry_4 = self.tank_angry_4_left
            else:
                if y + 1 + 95 < 745:
                    y += 1
                    self.coordinates_tank_angry_4 = (x, y)
                    self.image_common_angry_4 = self.tank_angry_4_bottom
                else:
                    if x - 1 + 92 > 959:
                        x -= 1
                        self.coordinates_tank_angry_4 = (x, y)
                        self.image_common_angry_4 = self.tank_angry_4_left
                    else:
                        if y + 1 + 95 < 945:
                            y += 1
                            self.coordinates_tank_angry_4 = (x, y)
                            self.image_common_angry_4 = self.tank_angry_4_bottom
                        else:
                            self.image_common_angry_4 = self.tank_angry_4_forward

    def common_angry_tank_5(self, screen):
        # Функция передвижения вражеского танка
        x = self.coordinates_tank_angry_5[0]
        y = self.coordinates_tank_angry_5[1]
        if y + 1 + 95 < 465:
            y += 1
            self.coordinates_tank_angry_5 = (x, y)
            self.image_common_angry_5 = self.tank_angry_5_bottom
        else:
            if x - 1 + 92 > 1205:
                x -= 1
                self.coordinates_tank_angry_5 = (x, y)
                self.image_common_angry_5 = self.tank_angry_5_left
            else:
                if y + 1 + 95 < 615:
                    y += 1
                    self.coordinates_tank_angry_5 = (x, y)
                    self.image_common_angry_5 = self.tank_angry_5_bottom

    def shooting_tank_angry_1_click(self, screen):
        # Функция для пойка игрока в зоне атаки противноником
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_1[0]
        y_tank_angry = self.coordinates_tank_angry_1[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_2_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_1 = self.tank_angry_1_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_2_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_1 = self.tank_angry_1_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_1 = self.tank_angry_1_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_1.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_1 = self.tank_angry_1_right

    def shooting_tank_angry_2_click(self, screen):
        # Функция для пойка игрока в зоне атаки противноником
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_2[0]
        y_tank_angry = self.coordinates_tank_angry_2[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_2_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_2 = self.tank_angry_2_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_2_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_2 = self.tank_angry_2_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_2 = self.tank_angry_2_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_2.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_2 = self.tank_angry_2_right

    def shooting_tank_angry_3_click(self, screen):
        # Функция для пойка игрока в зоне атаки противноником
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_3[0]
        y_tank_angry = self.coordinates_tank_angry_3[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_2_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_3 = self.tank_angry_3_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_2_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_3 = self.tank_angry_3_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_3 = self.tank_angry_3_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_3.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_3 = self.tank_angry_3_right

    def shooting_tank_angry_4_click(self, screen):
        # Функция для пойка игрока в зоне атаки противноником
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_4[0]
        y_tank_angry = self.coordinates_tank_angry_4[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_2_TANK_ANGRY_4.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_4 = self.tank_angry_4_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_2_TANK_ANGRY_4.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_4 = self.tank_angry_4_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_4.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_4 = self.tank_angry_4_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_4.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_4 = self.tank_angry_4_right

    def shooting_tank_angry_5_click(self, screen):
        # Функция для пойка игрока в зоне атаки противноником
        x_tank = self.coordinates_tank[0]
        y_tank = self.coordinates_tank[1]
        x_tank_angry = self.coordinates_tank_angry_5[0]
        y_tank_angry = self.coordinates_tank_angry_5[1]
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and y_tank_angry <= y_tank <= 945:
            CIRCLES_LEVEL_2_TANK_ANGRY_5.append((x_tank_angry, y_tank_angry, 'bottom'))
            self.image_common_angry_5 = self.tank_angry_5_bottom
        if x_tank_angry <= x_tank <= x_tank_angry + 72 and 135 <= y_tank <= y_tank_angry:
            CIRCLES_LEVEL_2_TANK_ANGRY_5.append((x_tank_angry, y_tank_angry, 'forward'))
            self.image_common_angry_5 = self.tank_angry_5_forward
        if 215 <= x_tank <= x_tank_angry and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_5.append((x_tank_angry, y_tank_angry, 'left'))
            self.image_common_angry_5 = self.tank_angry_5_left
        if x_tank_angry + 92 <= x_tank <= 1705 and y_tank_angry <= y_tank <= y_tank_angry + 73:
            CIRCLES_LEVEL_2_TANK_ANGRY_5.append((x_tank_angry, y_tank_angry, 'right'))
            self.image_common_angry_5 = self.tank_angry_5_right

    def shooting_tank_angry_1(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_2_TANK_ANGRY_1)):
            if CIRCLES_LEVEL_2_TANK_ANGRY_1[i][2] == 'bottom':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_1[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_1[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_1[i][2] == 'forward':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_1[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_1[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_1[i][2] == 'right':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_1[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_1[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_1[i][2] == 'left':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_1[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_1[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_1[i])
        for i in deleted:
            index = CIRCLES_LEVEL_2_TANK_ANGRY_1.index(i)
            CIRCLES_LEVEL_2_TANK_ANGRY_1.pop(index)

    def shooting_tank_angry_2(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_2_TANK_ANGRY_2)):
            if CIRCLES_LEVEL_2_TANK_ANGRY_2[i][2] == 'bottom':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_2[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_2[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_2[i][2] == 'forward':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_2[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_2[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_2[i][2] == 'right':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_2[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_2[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_2[i][2] == 'left':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_2[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_2[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_2[i])
        for i in deleted:
            index = CIRCLES_LEVEL_2_TANK_ANGRY_2.index(i)
            CIRCLES_LEVEL_2_TANK_ANGRY_2.pop(index)

    def shooting_tank_angry_3(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_2_TANK_ANGRY_3)):
            if CIRCLES_LEVEL_2_TANK_ANGRY_3[i][2] == 'bottom':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_3[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_3[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_3[i][2] == 'forward':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_3[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_3[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_3[i][2] == 'right':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_3[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_3[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_3[i][2] == 'left':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_3[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_3[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_3[i])
        for i in deleted:
            index = CIRCLES_LEVEL_2_TANK_ANGRY_3.index(i)
            CIRCLES_LEVEL_2_TANK_ANGRY_3.pop(index)

    def shooting_tank_angry_4(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_2_TANK_ANGRY_4)):
            if CIRCLES_LEVEL_2_TANK_ANGRY_4[i][2] == 'bottom':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_4[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_4[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_4[i][2] == 'forward':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_4[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_4[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_4[i][2] == 'right':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_4[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_4[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_4[i][2] == 'left':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_4[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_4[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_4[i])
        for i in deleted:
            index = CIRCLES_LEVEL_2_TANK_ANGRY_4.index(i)
            CIRCLES_LEVEL_2_TANK_ANGRY_4.pop(index)

    def shooting_tank_angry_5(self, screen):
        # Функция стрельбы вражеского танка
        deleted = []
        for i in range(len(CIRCLES_LEVEL_2_TANK_ANGRY_5)):
            if CIRCLES_LEVEL_2_TANK_ANGRY_5[i][2] == 'bottom':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y + 3 + 95 < 945:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y + 3 + 95 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y + 95), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_5[i] = (x, y, 'bottom')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_5[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_5[i][2] == 'forward':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if y - 3 > 135:
                        if self.x[j][0] <= x + 36 <= self.x[j][1] and self.y[j][0] <= y - 3 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    y -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 36, y), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_5[i] = (x, y, 'forward')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_5[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_5[i][2] == 'right':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x + 3 < 1705:
                        if self.x[j][0] <= x + 3 + 98 <= self.x[j][1] and self.y[j][0] <= y + 35 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x += 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x + 98, y + 35), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_5[i] = (x, y, 'right')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_5[i])
            elif CIRCLES_LEVEL_2_TANK_ANGRY_5[i][2] == 'left':
                x = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][0]
                y = CIRCLES_LEVEL_2_TANK_ANGRY_5[i][1]
                x_tank = self.coordinates_tank[0]
                y_tank = self.coordinates_tank[1]
                f = True
                for j in range(len(self.x)):
                    if x - 3 > 220:
                        if self.x[j][0] <= x - 1 <= self.x[j][1] and self.y[j][0] <= y + 36 <= self.y[j][1]:
                            f = False
                    else:
                        f = False
                if x_tank <= x <= x_tank + 93 and y_tank <= y <= y_tank + 72:
                    self.xp_tank -= 50
                    f = False
                if f:
                    x -= 3
                    pygame.draw.circle(screen, pygame.Color('yellow'), (x, y + 36), 5)
                    CIRCLES_LEVEL_2_TANK_ANGRY_5[i] = (x, y, 'left')
                else:
                    deleted.append(CIRCLES_LEVEL_2_TANK_ANGRY_5[i])
        for i in deleted:
            index = CIRCLES_LEVEL_2_TANK_ANGRY_5.index(i)
            CIRCLES_LEVEL_2_TANK_ANGRY_5.pop(index)

    def search_xp_healthy(self):
        # Функция для проверки жизни танков
        if self.xp_tank <= 0:
            self.flag_live_tank = False
        if self.xp_tank_angry_1 <= 0:
            self.flag_live_tank_angry_1 = False
        if self.xp_tank_angry_2 <= 0:
            self.flag_live_tank_angry_2 = False
        if self.xp_tank_angry_3 <= 0:
            self.flag_live_tank_angry_3 = False
        if self.xp_tank_angry_4 <= 0:
            self.flag_live_tank_angry_4 = False
        if self.xp_tank_angry_5 <= 0:
            self.flag_live_tank_angry_5 = False

    def restart(self):
        # Функция перезапуска
        self.coordinates_tank = (220, 135)
        self.image_common = pygame.image.load('танк bottom.png')
        self.flag_side_tank = 'bottom'
        self.coordinates_tank_angry_1 = (1618, 135)
        self.coordinates_tank_angry_2 = (1618, 135)
        self.coordinates_tank_angry_3 = (1618, 135)
        self.image_common_angry_1 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_2 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_3 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_4 = pygame.image.load('вражеский танк bottom.png')
        self.image_common_angry_5 = pygame.image.load('вражеский танк bottom.png')
        self.f = True
        self.xp_tank = 1000
        self.xp_tank_angry_1 = 500
        self.xp_tank_angry_2 = 500
        self.xp_tank_angry_3 = 500
        self.xp_tank_angry_4 = 500
        self.xp_tank_angry_5 = 500
        self.flag_live_tank = True
        self.flag_live_tank_angry_1 = True
        self.flag_live_tank_angry_2 = True
        self.flag_live_tank_angry_3 = True
        self.flag_live_tank_angry_4 = True
        self.flag_live_tank_angry_5 = True

    def research_win(self):
        # Функция проверки жизни всех вражеских танков
        if not (self.flag_live_tank_angry_1) and not (self.flag_live_tank_angry_2) \
                and not (self.flag_live_tank_angry_3) and not (self.flag_live_tank_angry_4) \
                and not (self.flag_live_tank_angry_5):
            return False
        else:
            return True

    def display_time(self, time_s, screen):
        # Функция таймера
        # time string with tents of seconds
        time_str = str(int(time_s * 10) / 10)
        font = pygame.font.Font(None, 30)
        label = font.render(f"Time : {time_str}", 1, pygame.Color('red'))
        screen.blit(label, (230, 900))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    running = True
    # открытие окон
    main = Main()
    info = Info()
    level_1 = Level_1()
    level_2 = Level_2()
    time_seconds = 0
    flag_f = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                count = main.search_click()
                main.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    count = main.search_click()
                    if count == 2:
                        level_1.shooting_click(screen)
                    elif count == 3:
                        level_2.shooting_click(screen)
        screen.fill(pygame.Color('black'))
        count = main.search_click()
        if count == 0 and main.flag_main:
            main.djl(screen)
        elif count == 1 and main.flag_info:
            screen.fill(pygame.Color('black'))
            main.djl(screen)
            info.render(screen)
        elif count == 2 and main.flag_level_1:
            screen.fill(pygame.Color('black'))
            time_millis = clock.tick(500)
            f = level_1.research_win()
            level_1.search_xp_healthy()
            if level_1.flag_live_tank and f:
                level_1.render(screen)
                level_1.display_time(time_seconds, screen)
                time_seconds += time_millis / 1000
                flag_f = True
            elif not (level_1.flag_live_tank) and f:
                level_1.defeat(screen)
                time_seconds = 0
            else:
                level_1.win(screen)
                if flag_f:
                    time_str = str(int(time_seconds * 10) / 10)
                    time_base = time_str.split('.')
                    cur.execute("""INSERT INTO level_1(minutes, secunds)
                                        VALUES(?, ?);""", (time_base[0], time_base[1]))  # Добавляю результат
                    # базу данных
                    con.commit()
                    flag_f = False
                time_seconds = 0
            if level_1.flag_live_tank_angry_1:
                level_1.common_angry_tank_1(screen)
                level_1.shooting_tank_angry_1_click(screen)
                level_1.shooting_tank_angry_1(screen)
            if level_1.flag_live_tank_angry_2:
                level_1.common_angry_tank_2(screen)
                level_1.shooting_tank_angry_2_click(screen)
                level_1.shooting_tank_angry_2(screen)
            if level_1.flag_live_tank_angry_3:
                level_1.common_angry_tank_3(screen)
                level_1.shooting_tank_angry_3_click(screen)
                level_1.shooting_tank_angry_3(screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                level_1.forward(screen)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                level_1.bottom(screen)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                level_1.left(screen)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                level_1.right(screen)
            level_1.shooting(screen)
        elif count == 3 and main.flag_level_2:
            screen.fill(pygame.Color('black'))
            time_millis = clock.tick(500)
            level_2.search_xp_healthy()
            f = level_2.research_win()
            if level_2.flag_live_tank and f:
                level_2.render(screen)
                level_1.display_time(time_seconds, screen)
                time_seconds += time_millis / 1000
                flag_f = True
            elif not (level_2.flag_live_tank) and f:
                level_2.defeat(screen)
                time_seconds = 0
            else:
                level_2.win(screen)
                if flag_f:
                    time_str = str(int(time_seconds * 10) / 10)
                    time_base = time_str.split('.')
                    cur.execute("""INSERT INTO level_2(minutes, seconds)
                                        VALUES(?, ?);""", (time_base[0], time_base[1]))  # Добавляю результат
                    # базу данных
                    con.commit()
                    flag_f = False
                time_seconds = 0
            if level_2.flag_live_tank_angry_1:
                level_2.common_angry_tank_1(screen)
                level_2.shooting_tank_angry_1_click(screen)
                level_2.shooting_tank_angry_1(screen)
            if level_2.flag_live_tank_angry_2:
                level_2.common_angry_tank_2(screen)
                level_2.shooting_tank_angry_2_click(screen)
                level_2.shooting_tank_angry_2(screen)
            if level_2.flag_live_tank_angry_3:
                level_2.common_angry_tank_3(screen)
                level_2.shooting_tank_angry_3_click(screen)
                level_2.shooting_tank_angry_3(screen)
            if level_2.flag_live_tank_angry_4:
                level_2.common_angry_tank_4(screen)
                level_2.shooting_tank_angry_4_click(screen)
                level_2.shooting_tank_angry_4(screen)
            if level_2.flag_live_tank_angry_5:
                level_2.common_angry_tank_5(screen)
                level_2.shooting_tank_angry_5_click(screen)
                level_2.shooting_tank_angry_5(screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                level_2.forward(screen)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                level_2.bottom(screen)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                level_2.left(screen)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                level_2.right(screen)
            level_2.shooting(screen)
        else:
            screen.fill(pygame.Color('black'))
            main.djl(screen)
        pygame.display.flip()
    pygame.quit()
