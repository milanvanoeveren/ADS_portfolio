import numpy as np
import random


class TerminalEnv:

    def __init__(self, width, height, max_containers, given_set=None):
        self.width = width
        self.height = height
        self.max_containers = max_containers

        self.score = 0

        self.fields = None
        self.fields_z = None
        self.actions = None

        self.containers_to_place = None

        self.set = given_set

        self.reset(0)

    def reset(self, loop_nr):
        self.score = 0

        self.fields = np.zeros((self.width, self.height, self.max_containers), dtype=int)
        self.fields_z = np.zeros((self.width, self.height), dtype=int)
        self.actions = np.ones((self.width, self.height), dtype=int)

        self.containers_to_place = []
        self.set_containers()

        self.containers_to_place = []
        if self.set is not None:
            self.containers_to_place = self.set.iloc[loop_nr].tolist()
        else:
            self.set_containers()

    def set_containers(self):
        self.containers_to_place += [1] * 8
        self.containers_to_place += [2] * 8
        self.containers_to_place += [3] * 8
        self.containers_to_place += [4] * 8

        random.shuffle(self.containers_to_place)

    def get_state(self):
        amount_of_fields = self.width * self.height

        actions = list(np.reshape(self.actions, amount_of_fields))
        container_list = []
        same_container = []

        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.max_containers):
                    field = self.fields[x][y][z]

                    if field != 0:
                        container_list.append(1)
                    else:
                        container_list.append(0)

                    if len(self.containers_to_place) == 0 or field != self.containers_to_place[0]:
                        same_container.append(0)
                    else:
                        same_container.append(1)

        state = actions + container_list + same_container

        return state

    def place_container(self, container, x, y):
        z = self.fields_z[x][y]

        if z >= self.max_containers:
            print(f"Invalid move - Height {x} {y}")
            return False, False

        self.fields[x][y][z] = container
        self.fields_z[x][y] += 1

        if self.actions[x][y] == 0:
            print("Invalid move - Action")
            return False, True

        return True, True

    def x_y_to_index(self, x, y):
        index = x * self.height + y

        return index

    def index_to_x_y(self, index):
        x = index // self.height
        start_index_x = x * self.height
        y = index - start_index_x

        return x, y

    def update_action(self, x, y, z_top_container):
        blocked_fields = 0

        if z_top_container + 1 >= self.max_containers:
            self.actions[x][y] = 0

        if z_top_container == 0:
            row = self.fields[x][:][z_top_container]
            before_row, after_row = row[:y], row[y + 1:]

            # Before
            last_index_match = None
            for i, value in enumerate(reversed(before_row)):
                if value != 0:
                    last_index_match = len(before_row) - i - 1
                    break

            if last_index_match is not None:
                amount = len(before_row) - last_index_match
                for i in range(1, amount):
                    blocked_fields += 1
                    self.actions[x][y - i] = 0

            # After
            index_first_match = next((index for index, item in enumerate(after_row) if item != 0), None)
            if index_first_match:
                for i in range(1, index_first_match + 1):
                    blocked_fields += 1
                    self.actions[x][y + i] = 0

        return blocked_fields

    def get_reward(self, container_id, x, y):
        reward = 10

        z_top_container = self.fields_z[x][y] - 1

        # score for same ids under
        for i in reversed(range(z_top_container + 1)):
            if self.fields[x][y][i] == container_id and z_top_container != i:
                reward += 4
            else:
                reward -= 6

        before_row, after_row = [], []
        for i in range(self.height):
            if i < y:
                before_row.append(self.fields[x][i][z_top_container])
            if i > y:
                after_row.append(self.fields[x][i][z_top_container])

        for j in reversed(before_row):
            if j == container_id:
                reward += 5
            else:
                break

        for k in after_row:
            if k == container_id:
                reward += 5
            else:
                break

        return reward

    def play_step(self, action):
        done = False
        reward = 0

        action_index = action.index(1)
        x, y = self.index_to_x_y(action_index)

        next_container = self.containers_to_place.pop(0)
        valid, placed = self.place_container(next_container, x, y)

        if placed:
            z_top_container = self.fields_z[x][y] - 1
            blocked_fields = self.update_action(x, y, z_top_container)
            reward -= blocked_fields * 5
        if valid:
            reward += self.get_reward(next_container, x, y)
        else:
            reward = -10

        self.score += reward

        if len(self.containers_to_place) == 0:
            done = True

        return reward, done, self.score
