import random
import sys
import time
from tkinter import *
from tkinter import messagebox

import pygame

Tk().wm_withdraw()
# цвета
RED = pygame.Color('red')
GREY = pygame.Color('grey')
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')


def load_image(filename):
    return pygame.image.load(filename)


class Game:  # Центральный класс, в котором будут
    # происходить основные действия игры
    def __init__(self):
        self.status = 'start'
        self.key = None
        self.count_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        self.count_ships_enemy = {1: 0, 2: 0, 3: 0, 4: 0}
        self.dif = 'легко'
        self.list_dif = ['легко', "средне", "сложно"]


game = Game()


class Ships(pygame.sprite.Sprite):
    def __init__(self, ships, ship, x, y, size):
        super().__init__(ships)
        im = load_image(ship)
        self.image = im
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, dx, dy, all_sprite):
        self.fire = [load_image('images\star.jpg')]
        for scale in (5, 10, 20):
            self.fire.append(
                pygame.transform.scale(self.fire[0], (scale, scale)))
        super().__init__(all_sprite)

        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        GRAVITY = 1
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0] * 3
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, 300, 300)):
            self.kill()


def create_particles(position, all_sprite):
    particle_count = 5
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers),
                 all_sprite)


class Board:
    def __init__(self, width, height, x, y, type, ship):
        self.width = width
        self.height = height

        self.board = [[0] * width for _ in range(height)]

        self.type = type

        self.left = x
        self.top = y
        self.cell_size = 30
        self.kills = 0
        self.ship = ship
        self.ships = []
        self.kill = False
        self.c = []
        self.x, self.y = random.randrange(0, 10), random.randrange(0, 10)
        self.view = False
        self.combo = 0

    def render(self, screen):
        for index_i, i in enumerate(self.board):
            for index_j, j in enumerate(i):
                if j == 0:
                    pygame.draw.rect(screen, BLACK, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size), 1)
                if j == 1 and self.view is True:
                    pygame.draw.rect(screen, BLACK, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size))

                if j == 2:
                    pygame.draw.rect(screen, BLACK, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size), 1)
                    pygame.draw.rect(screen, GREY, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size))

                if j == 3:
                    pygame.draw.rect(screen, BLACK, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size), 1)
                    pygame.draw.rect(screen, RED, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size))
                if j == 1 and self.view is False:
                    pygame.draw.rect(screen, BLACK, (
                        self.left + self.cell_size * index_i,
                        self.top + self.cell_size * index_j,
                        self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        width = self.width * self.cell_size
        height = self.height * self.cell_size
        if self.left < mouse_pos[0] < self.left + width:
            if self.top < mouse_pos[1] < self.top + height:
                coords = [(mouse_pos[0] - self.top) // self.cell_size, (
                        mouse_pos[1] - self.left) // self.cell_size]
                if self.type == 'Enemy':
                    coords[0] -= 12
                    coords[1] += 12
                return coords
        return None

    def on_click(self, cell_coords, position, text_1):
        if game.status == 'placement':
            if self.type == 'Sea':
                if text_1 == '1' and game.count_ships[1] < 4:
                    if position == 'vertik':
                        if self.check_ship_fits(1, 'gorizont',
                                                cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            game.count_ships[1] += 1
                            Ships(self.ship, 'images\ship_1.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                    else:
                        if self.check_ship_fits(1, 'vertik', cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            game.count_ships[1] += 1
                            Ships(self.ship, 'images\ship_1_1.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                if text_1 == '2' and game.count_ships[2] < 3:
                    if position == 'vertik':
                        if self.check_ship_fits(2, 'gorizont',
                                                cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            self.board[cell_coords[0] + 1][
                                cell_coords[1]] = 1
                            game.count_ships[2] += 1
                            Ships(self.ship, 'images\ship_2_0.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                    else:
                        if self.check_ship_fits(2, 'vertik', cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            self.board[cell_coords[0]][
                                cell_coords[1] + 1] = 1
                            game.count_ships[2] += 1
                            Ships(self.ship, 'images\ship_2_1.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                if text_1 == '3' and game.count_ships[3] < 2:
                    if position == 'vertik':
                        if self.check_ship_fits(3, 'gorizont',
                                                cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            self.board[cell_coords[0] + 1][
                                cell_coords[1]] = 1
                            self.board[cell_coords[0] + 2][
                                cell_coords[1]] = 1
                            game.count_ships[3] += 1
                            Ships(self.ship, 'images\ship_3_0.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                    else:
                        if self.check_ship_fits(3, 'vertik', cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            self.board[cell_coords[0]][
                                cell_coords[1] + 1] = 1
                            self.board[cell_coords[0]][
                                cell_coords[1] + 2] = 1
                            game.count_ships[3] += 1
                            Ships(self.ship, 'images\ship_3_1.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                if text_1 == '4' and game.count_ships[4] < 1:
                    if position == 'vertik':
                        if self.check_ship_fits(4, 'gorizont',
                                                cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            self.board[cell_coords[0] + 1][
                                cell_coords[1]] = 1
                            self.board[cell_coords[0] + 2][
                                cell_coords[1]] = 1
                            self.board[cell_coords[0] + 3][
                                cell_coords[1]] = 1
                            game.count_ships[4] += 1
                            Ships(self.ship, 'images\ship_4_0.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                    else:
                        if self.check_ship_fits(4, 'vertik', cell_coords):
                            self.board[cell_coords[0]][cell_coords[1]] = 1
                            self.board[cell_coords[0]][
                                cell_coords[1] + 1] = 1
                            self.board[cell_coords[0]][
                                cell_coords[1] + 2] = 1
                            self.board[cell_coords[0]][
                                cell_coords[1] + 3] = 1
                            game.count_ships[4] += 1
                            Ships(self.ship, 'images\ship_4_1.jpg',
                                  self.left + self.cell_size *
                                  cell_coords[0],
                                  self.top + self.cell_size * cell_coords[
                                      1],
                                  self.cell_size)
                        else:
                            messagebox.showinfo('Ошибка',
                                                'Невозможно '
                                                'выставить корабль')
                if game.count_ships[1] == 4 and game.count_ships[
                    2] == 3 and game.count_ships[3] == 2 and \
                        game.count_ships[4] == 1:
                    game.status = 'player_attack'
            else:
                messagebox.showinfo('Предупреждение',
                                    'Игра ещё не началась. '
                                    'Раставьте корабли')
        elif game.status == 'player_attack':
            if self.type == 'Enemy':
                try:
                    if self.board[cell_coords[0]][cell_coords[1]] == 0 \
                            or self.board[cell_coords[0]][
                        cell_coords[1]] == 1:
                        if self.board[cell_coords[0]][
                            cell_coords[1]] == 1:
                            count = 0
                            self.kills += 1
                            self.board[cell_coords[0]][cell_coords[1]] = 3
                            if self.board[cell_coords[0] + 1][
                                cell_coords[1]] == 1:
                                count += 1
                            elif self.board[cell_coords[0] - 1][
                                cell_coords[1]] == 1:
                                count += 1
                            elif self.board[cell_coords[0]][
                                cell_coords[1] + 1] == 1:
                                count += 1
                            elif self.board[cell_coords[0]][
                                cell_coords[1] - 1] == 1:
                                count += 1

                            if count == 0:
                                self.combo += 1
                                game.status = 'kill_player'
                                if game.dif == 'средне' \
                                        and self.combo == 3:
                                    game.status = 'enemy_attack'
                                elif game.dif == 'сложно' \
                                        and self.combo == 2:
                                    game.status = 'enemy_attack'

                            else:
                                self.combo += 1
                                print(self.combo)
                                game.status = 'knock_player'
                                if game.dif == 'средне' \
                                        and self.combo == 3:
                                    game.status = 'enemy_attack'
                                elif game.dif == 'сложно' \
                                        and self.combo == 2:
                                    game.status = 'enemy_attack'
                        else:
                            self.board[cell_coords[0]][cell_coords[1]] = 2
                            game.status = 'enemy_attack'
                except IndexError:
                    pass

    def get_click(self, mouse_pos, position, text_1):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords is None:
            return
        self.on_click(cell_coords, position, text_1)

    def random_coord(self):
        x, y = random.randrange(0, 10), random.randrange(0, 10)
        if self.board[x][y] == 3 or self.board[x][y] == 2:
            self.random_coord()
        return x, y

    def enemy_attack(self):
        if self.board[self.x][self.y] == 3 or self.kill:
            self.c.append((self.x, self.y))
            if self.x + 1 < 10 and self.board[self.x + 1][self.y] == 1:
                self.board[self.x + 1][self.y] = 3
                self.enemy_attack()
                self.kills += 1
                if self.x - 1 > - 1 and self.board[self.x - 1][
                    self.y] != 1:
                    self.x = self.x + 1
            elif self.y + 1 < 10 and self.board[self.x][self.y + 1] == 1:
                self.board[self.x][self.y + 1] = 3
                self.enemy_attack()
                self.kills += 1
                if self.y - 1 < -1 and self.board[self.x][
                    self.y - 1] != 1:
                    self.y = self.y + 1
            elif self.x - 1 > -1 and self.board[self.x - 1][self.y] == 1:
                self.board[self.x - 1][self.y] = 3
                self.enemy_attack()
                self.kills += 1
                if self.y + 1 < 10 and self.board[self.x + 1][
                    self.y] != 1:
                    self.x = self.x - 1
            elif self.y - 1 > -1 and self.board[self.x][self.y - 1] == 1:
                self.board[self.x][self.y - 1] = 3
                self.enemy_attack()
                self.kills += 1
                if self.y + 1 < 10 and self.board[self.x][
                    self.y + 1] != 1:
                    self.y = self.y - 1

            else:
                self.kill = False
                x, y = random.randrange(0, 10), random.randrange(0, 10)
                while (x, y) in self.c:
                    x, y = random.randrange(0, 10), random.randrange(0,
                                                                     10)
                self.c.append((x, y))

                if self.board[x][y] == 1:
                    self.board[x][y] = 3
                    self.kill = True

                    self.enemy_attack()
                    self.kills += 1
                elif self.board[x][y] == 2:
                    self.enemy_attack()
                elif self.board[x][y] == 3:
                    self.enemy_attack()

                else:
                    self.board[x][y] = 2
                self.x, self.y = x, y

        else:
            x, y = random.randrange(0, 10), random.randrange(0, 10)
            while (x, y) in self.c:
                x, y = random.randrange(0, 10), random.randrange(0, 10)
            self.c.append((x, y))

            if self.board[x][y] == 1:
                self.board[x][y] = 3
                self.kill = True
                self.enemy_attack()
                self.kills += 1
            elif self.board[x][y] == 2:
                self.enemy_attack()
            elif self.board[x][y] == 3:
                self.enemy_attack()
            else:
                self.board[x][y] = 2
            self.x, self.y = x, y

    def placement_enemy(self):
        count = 0
        k = True
        while True:
            i = random.randrange(1, 10)
            j = random.randrange(1, 10)
            test_list = ['vertik', 'gorizont']
            random_index = random.randint(0, len(test_list) - 1)
            position = test_list[random_index]
            if game.count_ships_enemy[1] < 4:
                if position == 'vertik':
                    if self.check_ship_fits(1, 'gorizont', [i, j]):
                        self.board[i][j] = 1
                        game.count_ships_enemy[1] += 1
                else:
                    if self.check_ship_fits(1, 'vertik', [i, j]):
                        self.board[i][j] = 1
                        game.count_ships_enemy[1] += 1
            if game.count_ships_enemy[2] < 3:
                if position == 'vertik':
                    if self.check_ship_fits(2, 'gorizont', [i, j]):
                        self.board[i][j] = 1
                        self.board[i + 1][j] = 1
                        game.count_ships_enemy[2] += 1
                else:
                    if self.check_ship_fits(2, 'vertik', [i, j]):
                        self.board[i][j] = 1
                        self.board[i][j + 1] = 1
                        game.count_ships_enemy[2] += 1
            if game.count_ships_enemy[3] < 2:
                if position == 'vertik':
                    if self.check_ship_fits(3, 'gorizont', [i, j]):
                        self.board[i][j] = 1
                        self.board[i + 1][j] = 1
                        self.board[i + 2][j] = 1
                        game.count_ships_enemy[3] += 1
                else:
                    if self.check_ship_fits(3, 'vertik', [i, j]):
                        self.board[i][j] = 1
                        self.board[i][j + 1] = 1
                        self.board[i][j + 2] = 1
                        game.count_ships_enemy[3] += 1
            if game.count_ships_enemy[4] == 0:
                if position == 'vertik':
                    if self.check_ship_fits(4, 'gorizont', [i, j]):
                        self.board[i][j] = 1
                        self.board[i + 1][j] = 1
                        self.board[i + 2][j] = 1
                        self.board[i + 3][j] = 1
                        game.count_ships_enemy[4] += 1
                    else:
                        count += 1
                else:
                    if self.check_ship_fits(4, 'vertik', [i, j]):
                        self.board[i][j] = 1
                        self.board[i][j + 1] = 1
                        self.board[i][j + 2] = 1
                        self.board[i][j + 3] = 1
                        game.count_ships_enemy[4] += 1
                    else:
                        count += 1

                if count > 50:
                    self.board = [[0] * self.width for _ in
                                  range(self.height)]
                    for i in range(1, 5):
                        game.count_ships_enemy[i] = 0
                    self.placement_enemy()
            else:
                k = False
            if not k:
                break

    def check_ship_fits(self, ship, element, cell_coords):
        if element == 'gorizont':
            if ship + cell_coords[0] - 1 > 9:
                return False
            for i in range(ship):
                if 10 > cell_coords[0] + i - 1 >= 0 and 10 > cell_coords[
                    1] - 1 >= 0 and self.board[cell_coords[0] + i - 1][
                    cell_coords[1] - 1] == 1:
                    return False

                if 10 > cell_coords[0] + i - 1 >= 0 and 10 > cell_coords[
                    1] >= 0 and self.board[cell_coords[0] + i - 1][
                    cell_coords[1]] == 1:
                    return False

                if 10 > cell_coords[0] + i - 1 >= 0 and 10 > cell_coords[
                    1] + 1 >= 0 and self.board[cell_coords[0] + i - 1][
                    cell_coords[1] + 1] == 1:
                    return False

                if 10 > cell_coords[0] + i >= 0 and 10 > cell_coords[
                    1] - 1 >= 0 and self.board[cell_coords[0] + i][
                    cell_coords[1] - 1] == 1:
                    return False

                if 10 > cell_coords[0] + i >= 0 and 10 > cell_coords[
                    1] >= 0 and self.board[cell_coords[0] + i][
                    cell_coords[1]] == 1:
                    return False

                if 10 > cell_coords[0] + i >= 0 and 10 > cell_coords[
                    1] + 1 >= 0 and self.board[cell_coords[0] + i][
                    cell_coords[1] + 1] == 1:
                    return False

                if 10 > cell_coords[0] + i + 1 >= 0 and 10 > cell_coords[
                    1] - 1 >= 0 and self.board[cell_coords[0] + i + 1][
                    cell_coords[1] - 1] == 1:
                    return False

                if 10 > cell_coords[0] + i + 1 >= 0 and 10 > cell_coords[
                    1] >= 0 and self.board[cell_coords[0] + i + 1][
                    cell_coords[1]] == 1:
                    return False

                if 10 > cell_coords[0] + i + 1 >= 0 and 10 > cell_coords[
                    1] + 1 >= 0 and self.board[cell_coords[0] + i + 1][
                    cell_coords[1] + 1] == 1:
                    return False

        elif element == 'vertik':
            if ship + cell_coords[1] - 1 > 9:
                return False
            for i in range(ship):
                if 10 > cell_coords[0] - 1 >= 0 and 10 > cell_coords[
                    1] + i - 1 >= 0 and self.board[cell_coords[0] - 1][
                    cell_coords[1] + i - 1] == 1:
                    return False

                if 10 > cell_coords[0] - 1 >= 0 and 10 > cell_coords[
                    1] + i >= 0 and self.board[cell_coords[0] - 1][
                    cell_coords[1] + i] == 1:
                    return False

                if 10 > cell_coords[0] - 1 >= 0 and 10 > cell_coords[
                    1] + i + 1 >= 0 and self.board[cell_coords[0] - 1][
                    cell_coords[1] + i + 1] == 1:
                    return False

                if 10 > cell_coords[0] >= 0 and 10 > cell_coords[
                    1] + i - 1 >= 0 and self.board[cell_coords[0]][
                    cell_coords[1] + i - 1] == 1:
                    return False

                if 10 > cell_coords[0] >= 0 and 10 > cell_coords[
                    1] + i >= 0 and self.board[cell_coords[0]][
                    cell_coords[1] + i] == 1:
                    return False

                if 10 > cell_coords[0] >= 0 and 10 > cell_coords[
                    1] + i + 1 >= 0 and self.board[cell_coords[0]][
                    cell_coords[1] + i + 1] == 1:
                    return False

                if 10 > cell_coords[0] + 1 >= 0 and 10 > cell_coords[
                    1] + i - 1 >= 0 and self.board[cell_coords[0] + 1][
                    cell_coords[1] + i - 1] == 1:
                    return False

                if 10 > cell_coords[0] + 1 >= 0 and 10 > cell_coords[
                    1] + i >= 0 and self.board[cell_coords[0] + 1][
                    cell_coords[1] + i] == 1:
                    return False

                if 10 > cell_coords[0] + 1 >= 0 and 10 > cell_coords[
                    1] + i + 1 >= 0 and self.board[cell_coords[0] + 1][
                    cell_coords[1] + i + 1] == 1:
                    return False
        return True


def start():
    pygame.init()
    size = 300, 300
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Морской бой")
    screen.fill(BLACK)
    with open('score.txt', 'r') as t:
        score = t.read()
    render_s = pygame.font.Font(None, 30).render('Ваш счёт в игре: '
                                                 + score, True,
                                                 WHITE)
    rect_s = render_s.get_rect()
    rect_s = (10, 10)
    font = pygame.font.Font(None, 50)
    render = font.render('Морской бой', True, WHITE, (30, 45, 160))
    rect = render.get_rect()
    rect.center = size[0] / 2, size[1] / 2
    screen.blit(render, rect)
    screen.blit(render_s, rect_s)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def loss():
    pygame.init()
    size = 300, 300
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game over')
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    render = font.render('Вы проиграли!', True, WHITE)
    rect = render.get_rect()
    rect.center = size[0] / 2, size[1] / 2
    screen.blit(render, rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def win(p, a):
    pygame.init()
    size = 300, 300
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Game over')
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    render = font.render('Вы победили!', True, WHITE)
    all_sprite = pygame.sprite.Group()
    clock = pygame.time.Clock()
    rect = render.get_rect()
    rect.center = size[0] / 2, size[1] / 2
    screen.blit(render, rect)
    score = (a.kills - p.kills) * (game.list_dif.index(game.dif) + 1)
    with open('score.txt', 'r') as f:
        s = f.read()
    with open('score.txt', 'w') as f:
        f.write(str(score + int(s)))
    render_s = pygame.font.Font(None, 30).render('Ваш счёт: '
                                                 + str(score), True,
                                                 WHITE)
    rect_s = render_s.get_rect()
    rect_s = (10, 10)
    screen.blit(render_s, rect_s)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        create_particles((150, 20), all_sprite)

        all_sprite.update()
        all_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(25)
        screen.fill(BLACK)
        font = pygame.font.Font(None, 50)
        render = font.render('Вы победили!', True, WHITE)
        rect = render.get_rect()
        rect.center = size[0] / 2, size[1] / 2
        screen.blit(render, rect)
        screen.blit(render_s, rect_s)


def main():
    pygame.init()
    size = 750, 450
    ship = pygame.sprite.Group()
    attack = Board(10, 10, 410, 50, 'Enemy', ship)
    player = Board(10, 10, 50, 50, 'Sea', ship)
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Морской бой")
    text_1 = ''
    text = 'Расстановка кораблей'
    font = pygame.font.Font(None, 50)
    render = font.render(text, True, BLACK)
    rect = render.get_rect()
    rect.center = (size[0] / 2, 20)
    sea = pygame.sprite.Group()
    text_f = 'Поле игрока'
    field_name = pygame.font.Font(None, 40).render(text_f, True, BLACK)
    rect_f = field_name.get_rect()
    rect_f = (110, 360)
    text_ef = 'Поле противника'
    efield_name = pygame.font.Font(None, 40). \
        render(text_ef, True, BLACK)
    rect_ef = field_name.get_rect()
    rect_ef = (445, 360)
    position = 'gorizont'
    running = True
    messagebox.showinfo('Предупреждение', 'Для изменения уровня '
                                          'сложности'
                                          ' используйте колесо мыши')
    while running:
        attack.placement_enemy()
        if attack.kills == 20:
            win(player, attack)
            running = False
        elif player.kills == 20:
            loss()
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.left < event.pos[0] < \
                        player.left + player.width * player.cell_size:
                    if player.top < event.pos[
                        1] < player.top + \
                            player.height * player.cell_size:
                        player.get_click(event.pos, position, text_1)
                else:
                    attack.get_click(event.pos, position, text_1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                if game.list_dif.index(game.dif) == 2:
                    game.dif = game.list_dif[0]
                else:
                    game.dif = game.list_dif[
                        game.list_dif.index(game.dif) + 1]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                if game.list_dif.index(game.dif) == 0:
                    game.dif = game.list_dif[2]
                else:
                    game.dif = game.list_dif[
                        game.list_dif.index(game.dif) - 1]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    if attack.view:
                        attack.view = False
                    else:
                        attack.view = True
                if game.status == 'placement':
                    game.key = event.key
                    if game.key == pygame.K_1:
                        text = 'Выбран одноклеточный корабль'
                        text_1 = '1'
                    elif game.key == pygame.K_2:
                        text = 'Выбран двухклеточный корабль'
                        text_1 = '2'
                    elif game.key == pygame.K_3:
                        text = 'Выбран трёхклеточный корабль'
                        text_1 = '3'
                    elif game.key == pygame.K_4:
                        text = 'Выбран четырёхклеточный корабль'
                        text_1 = '4'
                    elif game.key == pygame.K_g:
                        position = 'vertik'
                    elif game.key == pygame.K_v:
                        position = 'gorizont'

        if game.status == 'placement' \
                and game.key is None:
            font = pygame.font.Font(None, 50)
            text = 'Для выбора нажмите 1, 2, 3 или 4'
            render = font.render(text, True, BLACK)
            rect = render.get_rect()
            rect.center = (size[0] / 2, 20)
        elif game.status == 'player_attack':
            text_f = 'Поле игрока'
            text_ef = 'Поле противника'
            efield_name = pygame.font.Font(None, 40). \
                render(text_ef, True, BLACK)
            rect_ef = field_name.get_rect()
            rect_ef = (445, 360)
            field_name = pygame.font.Font(None, 40).render(text_f, True,
                                                           BLACK)
            rect_f = field_name.get_rect()
            rect_f = (105, 360)

            font = pygame.font.Font(None, 50)
            text = 'Ход игрока'
            render = font.render(text, True, BLACK)
            rect = render.get_rect()
            rect.center = (size[0] / 2, 20)
        elif game.status == 'placement':
            text_f = 'Нажмите V - для вертикали, G - для горизонтали'
            field_name = pygame.font.Font(None, 25).render(text_f, True,
                                                           BLACK)
            text_ef = ''
            efield_name = pygame.font.Font(None, 40). \
                render(text_ef, True, BLACK)
            rect_ef = field_name.get_rect()
            rect_ef = (445, 360)
            rect_f = field_name.get_rect()
            rect_f = (50, 360)
            font = pygame.font.Font(None, 25)
            render = font.render(text, True, BLACK)
            rect = render.get_rect()
            rect = (50, 33)

        elif game.status == 'kill_player':
            font = pygame.font.Font(None, 50)
            text = 'Вы уничтожили вражеский корабль'
            render = font.render(text, True, BLACK)
            rect = render.get_rect()
            rect.center = (size[0] / 2, 20)
        elif game.status == 'knock_player':
            font = pygame.font.Font(None, 50)
            text = 'Вы подбили вражеский корабль'
            render = font.render(text, True, BLACK)
            rect = render.get_rect()
            rect.center = (size[0] / 2, 20)
        elif game.status == 'enemy_attack':
            attack.combo = 0
            font = pygame.font.Font(None, 50)
            text = 'Противник атакует'
            render = font.render(text, True, BLACK)
            rect = render.get_rect()
            rect.center = (size[0] / 2, 20)

        dif_text = pygame.font.Font(None, 25). \
            render('Уровень сложности: ' + game.dif, True, BLACK)
        rect_d = dif_text.get_rect()
        rect_d = (10, 425)

        screen.fill(WHITE)
        sea.draw(screen)
        ship.draw(screen)
        player.render(screen)
        attack.render(screen)
        screen.blit(efield_name, rect_ef)
        screen.blit(field_name, rect_f)
        screen.blit(dif_text, rect_d)
        screen.blit(render, rect)
        pygame.display.flip()

        if game.status == 'enemy_attack':
            time.sleep(2)
            player.enemy_attack()
            game.status = 'player_attack'
        elif game.status == 'kill_player' \
                or game.status == 'knock_player':
            time.sleep(2)
            game.status = 'player_attack'
        elif game.status == 'start':
            time.sleep(1)
            game.status = 'placement'


if __name__ == '__main__':
    start()
    main()
