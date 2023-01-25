import time
from operator import itemgetter

import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

from Field import Field

pygame.init()
font = pygame.font.SysFont('', 25)

# rgb colors
WHITE = (255, 255, 255)
GREY = (105, 105, 105)
RED = (200, 0, 0)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)

BLOCK_WIDTH = 100
BLOCK_HEIGHT = 50
SPEED = 1000


class ContainerGameAI:

    def __init__(self, width=4, height=5, max_containers=1):
        self.width = width
        self.height = height
        self.w = width * BLOCK_WIDTH
        self.h = height * BLOCK_HEIGHT
        self.max_containers = max_containers

        self.score = 0
        self.steps = 0
        self.frame_iteration = 0
        self.fields = [[Field("container_field", max_containers) for j in range(height)] for i in range(width)]

        self.containers_to_place = []
        for i in range(6):
            self.containers_to_place.append(i)

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('ADS - Containers')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.score = 0
        self.frame_iteration = 0
        self.fields = [[Field("container_field", self.max_containers) for j in range(self.height)] for i in range(self.width)]

        for x in range(self.width):
            self.fields[x][0].type = "road_field"
            self.fields[x][self.height - 1].type = "road_field"

        for y in range(self.height):
            self.fields[0][y].type = "road_field"
            self.fields[self.width - 1][y].type = "road_field"

        self.containers_to_place = []
        for i in range(6):
            self.containers_to_place.append(i)

    def _draw_field(self, x, y, color):
        pygame.draw.rect(self.display, color, pygame.Rect(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT))

    def _draw_borders(self):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(self.display, BLACK,
                                 pygame.Rect(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT), 1)

    def update_ui(self):
        self.display.fill(WHITE)

        for x in range(self.width):
            self._draw_field(x, 0, GREY)
            self._draw_field(x, self.height - 1, GREY)
            for y in range(self.height):
                self._draw_field(0, y, GREY)
                self._draw_field(self.width - 1, y, GREY)

                if len(self.fields[x][y].containers) > 0:
                    self._draw_field(x, y, GREEN)

        self._draw_borders()

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def get_all_available_fields(self):
        available_fields = []

        width = len(self.fields)
        height = len(self.fields[0])

        for x in range(1, width - 1):
            for y in range(1, height - 1):
                if self.is_field_available_to_place_container(x, y):
                    self.fields[x][y].containers.append(0)
                    field = [f"X{x}Y{y}", self.get_field_score(x, y)]
                    available_fields.append(field)
                    self.fields[x][y].containers.pop()

        return available_fields

    def get_all_fields(self):
        all_fields = []

        width = len(self.fields)
        height = len(self.fields[0])

        for x in range(width):
            for y in range(height):
                self.fields[x][y].containers.append(0)
                field = [f"X{x}Y{y}", self.get_field_score(x, y)]
                all_fields.append(field)
                self.fields[x][y].containers.pop()

        return all_fields

    def get_blocked_empty_fields_top(self, x, y):
        empty_fields = 0

        if len(self.fields[x][y].containers) > 0:
            distance_to_top = y
            if distance_to_top != 0:
                for i in range(1, distance_to_top + 1):
                    if len(self.fields[x][y - i].containers) > 0:
                        # print(f"Field [{x},{y}] blocks {empty_fields} empty fields above")
                        return empty_fields
                    empty_fields += 1

        return 0

    def get_blocked_empty_fields_bottom(self, x, y):
        empty_fields = 0

        if len(self.fields[x][y].containers) > 0:
            distance_to_bottom = len(self.fields[x]) - 1 - y
            if distance_to_bottom != 0:
                for i in range(1, distance_to_bottom + 1):
                    if len(self.fields[x][y + i].containers) > 0:
                        # print(f"Field [{x},{y}] blocks {empty_fields} empty fields under")
                        return empty_fields
                    empty_fields += 1

        return 0

    def get_field_score(self, x, y):
        score = 0

        amount_of_containers = len(self.fields[x][y].containers)
        blocked_top = self.get_blocked_empty_fields_top(x, y)
        blocked_bottom = self.get_blocked_empty_fields_bottom(x, y)

        if self.fields[x][y].type == "road_field" and amount_of_containers > 0:
            score -= 60 * amount_of_containers
        elif amount_of_containers > self.fields[x][y].max_height:
            amount_above = amount_of_containers - self.fields[x][y].max_height
            score -= 30 * amount_above
        elif amount_of_containers > 0:
            score += 20

        score -= blocked_top * 15
        score -= blocked_bottom * 15

        return score

    def calculate_score(self):
        score = 0

        width = len(self.fields)
        height = len(self.fields[0])

        for x in range(width):
            for y in range(height):
                field_score = self.get_field_score(x, y)
                score += field_score

        self.score = score
        return score

    def is_field_available_to_place_container(self, x, y):
        if (self.is_top_way_free(x, y) or self.is_bottom_way_free(x, y)) \
                and self.is_under_max_height(x, y) and self.fields[x][y].type == "container_field":
            return True
        return False

    def is_top_way_free(self, x, y):
        distance_to_top = y
        if distance_to_top != 0:
            for i in range(1, distance_to_top + 1):
                if len(self.fields[x][y - i].containers) > 0:
                    return False
        return True

    def is_bottom_way_free(self, x, y):
        distance_to_bottom = len(self.fields[x]) - 1 - y
        for i in range(1, distance_to_bottom + 1):
            if len(self.fields[x][y + i].containers) > 0:
                return False
        return True

    def is_under_max_height(self, x, y):
        if len(self.fields[x][y].containers) >= self.fields[x][y].max_height:
            return False
        return True

    def place_container(self, container, x, y):
        # print(f"Placing container {container} on X{x}-Y{y}..")
        self.fields[x][y].containers.append(container)

    def get_random_move(self):
        move = [0] * (self.width * self.height)

        all_fields = self.get_all_fields()
        random.shuffle(all_fields)
        random_move = all_fields.pop()

        random_move = str(random_move[0])
        x, y = int(random_move[1]), int(random_move[3])

        move_index = x * self.height + y
        move[move_index] = 1

        return move

    def show(self):
        width = len(self.fields)
        height = len(self.fields[0])

        CBLACKBG = '\33[100m'
        CWHITEBG = '\33[107m'
        CGREENBG = '\33[102m'
        CYELLOWBG = '\33[103m'
        CREDBG = '\33[101m'
        CEND = '\033[0m'

        score_row = f"      ============================= Terminal - Score: {self.calculate_score()} ============================= "
        header_row = "      "
        for x in range(width):
            header_row += f"    {x}     "

        border_row = "     +"
        for x in range(width):
            border_row += "---------+"

        print(f"\n{score_row}")
        print(header_row)
        print(border_row)

        for y in range(height):
            value_row = f"  {y}  |"
            for x in range(width):
                amount_of_containers = len(self.fields[x][y].containers)
                background_color = CWHITEBG
                if self.fields[x][y].type == "road_field":
                    background_color = CBLACKBG
                elif amount_of_containers == 1:
                    background_color = CGREENBG
                elif amount_of_containers == 2:
                    background_color = CYELLOWBG
                elif amount_of_containers >= 3:
                    background_color = CREDBG

                value_row += f"{background_color}         {CEND}|"
            print(value_row)
            print(border_row)
        print("\n")

    def play_step(self, final_move):
        old_score = self.calculate_score()

        final_move_index = final_move.index(1)
        final_x = final_move_index // self.height
        final_y = final_move_index - final_x * self.height

        self.place_container(self.containers_to_place.pop(0), final_x, final_y)

        self.steps += 1

        self.frame_iteration += 1
        self.update_ui()

        new_score = self.calculate_score()

        reward = new_score-old_score,

        done = len(self.containers_to_place) == 0

        # if done:
        #     self.show()

        return reward, done, new_score
