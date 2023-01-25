import time

import numpy as np
import pandas as pd
import matplotlib
from matplotlib import colors

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random

HEIGHT = 5
MAX_CONTAINERS = 3

data = {
    0: [[], [], [], [], []],
    1: [[], [], [], [], []],
    2: [[], [], [], [], []],
    3: [[], [], [], [], []],
    4: [[], [], [], [], []],
}

board = pd.DataFrame(data)

grid_vis = pd.DataFrame({0: [0, 0, 0, 0, 0],
                         1: [0, 0, 0, 0, 0],
                         2: [0, 0, 0, 0, 0],
                         3: [0, 0, 0, 0, 0],
                         4: [0, 0, 0, 0, 0]})

# visualisatie dingen initialiseren
plt.ion()
fix, ax = plt.subplots()
color_list = ['white', 'green', 'orange', 'red']
levels = range(MAX_CONTAINERS + 2)
color_map, norm = colors.from_levels_and_colors(levels, color_list)


def visualize():
    # lengte rows en cols verzamelen
    rows, cols = grid_vis.shape

    # containers verschuiven op assen + ticks goed schuiven
    ax.set_xticklabels('')
    ax.set_yticklabels('')
    ax.set_xticks(np.arange(-.5, rows, 1))
    ax.set_yticks(np.arange(-.5, cols, 1))
    cols_strings = [str(i + 1) for i in list(range(cols))]
    rows_strings = [str(i + 1) for i in list(range(rows))]
    ax.xaxis.set_minor_locator(ticker.FixedLocator([0, 1, 2, 3, 4]))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter(cols_strings))
    ax.yaxis.set_minor_locator(ticker.FixedLocator([0, 1, 2, 3, 4]))
    ax.yaxis.set_minor_formatter(ticker.FixedFormatter(rows_strings))

    # labels
    plt.xlabel(xlabel='x-coordinaten', fontsize=14)
    plt.ylabel(ylabel='y-coordinaten', fontsize=14)
    ax.xaxis.set_label_position('top')

    # ticks op x-as boven zetten
    ax.tick_params(axis="x", which="minor", direction="out", top=True, labeltop=True, bottom=False, labelbottom=False)

    # grid aanmaken en image tekenen op basis van color map
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.imshow(grid_vis, cmap=color_map, norm=norm)
    # hoogte op container annoteren
    for i in range(cols):
        for j in range(rows):
            ax.annotate('{}'.format(grid_vis.iloc[i, j]), xy=(j, i))
    # pauzeren en canvas weer leeghalen voor volgende loop
    plt.pause(.25)
    plt.draw()
    plt.cla()


visualize()
time.sleep(1)

def is_move_valid(x, y):
    distance_to_top = y
    distance_to_bottom = HEIGHT - 1 - y

    current_height = len(board[x][y])

    ride_from_top_bool = True
    ride_from_bottom_bool = True

    if distance_to_top != 0:
        # Check if top way is free
        for i in range(1, distance_to_top + 1):
            if len(board[x][y - i]) != 0:
                ride_from_top_bool = False
                break

    if distance_to_bottom != 0:
        # Check if bottom way is free
        for i in range(1, distance_to_bottom + 1):
            if len(board[x][y + i]) != 0:
                ride_from_bottom_bool = False

    errors = []
    if not ride_from_top_bool and not ride_from_bottom_bool:
        if not ride_from_top_bool:
            errors.append("De weg van boven is niet vrij")
        if not ride_from_bottom_bool:
            errors.append("De weg van onder is niet vrij")
    if current_height >= MAX_CONTAINERS:
        errors.append("Er staan al " + str(MAX_CONTAINERS) + " containers op deze plek")

    if len(errors) == 0:
        return [True, errors]

    print(x, y, errors)
    return [False, errors]


def get_possible_places():
    possible_places = []

    for x in range(5):
        for y in range(5):
            if is_move_valid(x, y)[0]:
                possible_places.append("x" + str(x) + "y" + str(y))

    return possible_places


def place_container(container_id, x, y):
    valid = is_move_valid(x, y)

    if valid[0]:
        board[x][y].append(container_id)
        grid_vis[x][y] += 1
        print("Succesvol geplaatst")
    else:
        print("Errors", valid[1])


container_id = 1
while len(get_possible_places()):
    possible_places = get_possible_places()
    print(possible_places)
    random.shuffle(possible_places)
    print(possible_places)

    coordinates = possible_places.pop()

    x = coordinates[1]
    y = coordinates[3]
    print(container_id, x, y)

    place_container(container_id, int(x), int(y))
    container_id += 1

    visualize()

    print(board)
