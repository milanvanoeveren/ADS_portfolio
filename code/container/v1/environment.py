import numpy as np
import pandas as pd

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


def get_possible_places():
    possible_places = []

    for x in range(5):
        for y in range(5):
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
                possible_places.append("x" + str(x) + "y" + str(y))

    return possible_places


def place_container(container_id, x, y):
    coordinates = "x" + str(x) + "y" + str(y)

    possible = get_possible_places()
    print(possible)

    if coordinates in possible:
        board[x][y].append(container_id)
        print("Succesvol geplaatst")


print(board)