import pygame


class Container:
    def __init__(self, id, ship_id):
        self.id = id
        self.ship_id = ship_id


pygame.init()
font = pygame.font.SysFont('', 25)
container_font = pygame.font.SysFont('', 18)

WHITE = (255, 255, 255)
GREY = (105, 105, 105)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)

BLOCK_WIDTH = 100
BLOCK_HEIGHT = 50

display = pygame.display.set_mode((4 * BLOCK_WIDTH, 3 * BLOCK_HEIGHT))
pygame.display.set_caption('ADS - Containers')

container_dict = {1: 1,
                  2: 3,
                  3: 3,
                  4: 2,
                  5: 2,
                  6: 3,
                  7: 3,
                  8: 2,
                  9: 3,
                  10: 1,
                  11: 2,
                  12: 2,
                  13: 1,
                  14: 3,
                  15: 3,
                  16: 2,
                  17: 3,
                  18: 3,
                  19: 1,
                  20: 2}

setup = {(4, 1, 1): 4,
         (4, 1, 2): 5,
         (4, 2, 1): 8,
         (4, 2, 2): 11,
         (4, 3, 1): 12,
         (4, 3, 2): 16,
         (3, 1, 1): 2,
         (3, 1, 2): 3,
         (3, 2, 1): 6,
         (3, 2, 2): 7,
         (3, 3, 1): 9,
         (3, 3, 2): 14,
         (1, 1, 1): 1,
         (1, 1, 2): 10,
         (1, 2, 1): 13,
         (2, 1, 1): 15,
         (2, 1, 2): 17,
         (2, 2, 1): 18,
         (1, 2, 2): 19,
         (2, 2, 2): 20}

containers = []

for key in container_dict.keys():
    container = Container(key, container_dict[key])


def draw_borders():
    for x in range(4):
        for y in range(3):
            pygame.draw.rect(display, BLACK,
                             pygame.Rect(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT), 1)


display.fill(WHITE)

for key in setup.keys():
    x, y, z, container_id = key[0] - 1, key[1] - 1, key[2] - 1, setup[key]
    print(x, y, z, container_id)

    color_id = container_dict[container_id]
    color = GREEN
    if color_id == 2:
        color = ORANGE
    elif color_id == 3:
        color = RED

    container_text = container_font.render(str(container_id), True, color)
    margin = 5 + z * 20
    display.blit(container_text, [x * BLOCK_WIDTH + margin, y * BLOCK_HEIGHT + 5])


draw_borders()
pygame.display.flip()

while True:
    pygame.event.pump()
    pass
