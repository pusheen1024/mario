import sys
import os
import pygame

deltas = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
tile_width = tile_height = 50


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя", "Герой двигается", "Карта на месте", "Несколько уровней"]

    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def load_level(filename):
    filename = os.path.join('data', filename)
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(list, map(lambda x: x.ljust(max_width, '.'), level_map)))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(*self.recalc(self.pos_x, self.pos_y))

    def recalc(self, x, y):
        return tile_width * x + 15, tile_height * y + 5

    def move(self, event):
        dx, dy = deltas.get(event.key, (0, 0))
        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x <= level_x and 0 <= new_y <= level_y and level[new_y][new_x] in '.@':
            level[self.pos_y][self.pos_x] = '.'
            level[new_y][new_x] = '@'
            self.pos_x, self.pos_y = new_x, new_y
            self.rect.x, self.rect.y = self.recalc(new_x, new_y)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()

level = load_level(sys.stdin.readline().strip() + '.txt')
player, level_x, level_y = generate_level(level)

pygame.init()
size = WIDTH, HEIGHT = (level_x + 1) * tile_width, (level_y + 1) * tile_height

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя')
clock = pygame.time.Clock()
start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.move(event)
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
pygame.quit()
