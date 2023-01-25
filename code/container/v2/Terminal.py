import random
import time

from Field import Field
from Truck import Truck
import keyboard


class Terminal:

    def __init__(self, width, height, max_containers):
        self.fields = [[Field("container_field", max_containers) for j in range(height)] for i in range(width)]
        self.steps = 0

        width = len(self.fields)
        height = len(self.fields[0])

        for x in range(width):
            self.fields[x][0].type = "road_field"
            self.fields[x][height - 1].type = "road_field"

        for y in range(height):
            self.fields[0][y].type = "road_field"
            self.fields[width - 1][y].type = "road_field"

        self.containers_to_place = []
        for i in range(1, 24):
            self.containers_to_place.append(i)

        self.truck = Truck(0, 0)

    def show(self):
        width = len(self.fields)
        height = len(self.fields[0])

        CBLACKBG = '\33[100m'
        CWHITEBG = '\33[107m'
        CGREENBG = '\33[102m'
        CYELLOWBG = '\33[103m'
        CREDBG = '\33[101m'
        CEND = '\033[0m'

        header_row = "      "
        for x in range(width):
            header_row += f"    {x}     "

        border_row = "     +"
        for x in range(width):
            border_row += "---------+"

        print(f"\n{header_row}")
        print(border_row)

        for y in range(height):
            value_row = f"  {y}  |"
            for x in range(width):
                if self.truck.x == x and self.truck.y == y:
                    if self.truck.container:
                        value_row += f" {CYELLOWBG}  {CEND}{CWHITEBG} {self.truck.container} {CEND}{CYELLOWBG}  {CEND} |"
                    else:
                        value_row += f" {CYELLOWBG}  {CEND}{CWHITEBG}   {CEND}{CYELLOWBG}  {CEND} |"
                else:
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

    def get_valid_moves(self, truck):
        valid_moves = []
        if self.valid_up(truck):
            valid_moves.append(0)
        if self.valid_down(truck):
            valid_moves.append(1)
        if self.valid_left(truck):
            valid_moves.append(2)
        if self.valid_right(truck):
            valid_moves.append(3)
        return valid_moves

    def valid_up(self, truck):
        if truck.y != 0 and len(self.fields[truck.x][truck.y - 1].containers) < self.fields[truck.x][truck.y - 1].max_height:
            return True
        return False

    def valid_down(self, truck):
        height = len(self.fields[0])
        if truck.y != height - 1 and len(self.fields[truck.x][truck.y + 1].containers) < self.fields[truck.x][truck.y + 1].max_height:
            return True
        return False

    def valid_left(self, truck):
        if truck.x != 0 and self.fields[truck.x - 1][truck.y].type == "road_field" and \
                len(self.fields[truck.x - 1][truck.y].containers) < self.fields[truck.x - 1][truck.y].max_height:
            return True
        return False

    def valid_right(self, truck):
        width = len(self.fields)
        if truck.x != width - 1 and self.fields[truck.x + 1][truck.y].type == "road_field" and \
                len(self.fields[truck.x + 1][truck.y].containers) < self.fields[truck.x + 1][truck.y].max_height:
            return True
        return False

    def move_up(self, truck):
        if self.valid_up(truck):
            truck.move_up()
            terminal.steps += 1
            self.show()

    def move_down(self, truck):
        if self.valid_down(truck):
            truck.move_down()
            terminal.steps += 1
            self.show()

    def move_left(self, truck):
        if self.valid_left(truck):
            truck.move_left()
            terminal.steps += 1
            self.show()

    def move_right(self, truck):
        if self.valid_right(truck):
            truck.move_right()
            terminal.steps += 1
            self.show()

    def pickup_new_container(self, truck):
        truck.container = self.containers_to_place.pop()
        terminal.steps += 1
        self.show()

    def place_container(self, x, y, truck):
        if truck.container is not None and self.fields[x][y].type == "container_field":
            print(f"Placing container {truck.container} on X{x}-Y{y}..")
            self.fields[x][y].containers.append(truck.container)
            self.truck.container = None
            terminal.steps += 1
            self.show()

    def move_towards_container_spawn(self, truck):
        if truck.container is None and truck.x == 0 and truck.y == 0:
            print("Picking up new container..")
            self.pickup_new_container(truck)
            return

        distance_to_top = truck.y
        distance_to_bottom = len(self.fields[truck.x]) - 1 - truck.y

        if truck.x == 0:
            print("Moving up towards container spawn..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y - 1))
            self.move_up(truck)

        elif distance_to_top == 0 or distance_to_bottom == 0:
            print("Moving left towards container spawn..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x - 1) + "Y" + str(truck.y))
            self.move_left(truck)

        elif (distance_to_top <= distance_to_bottom and self.is_top_way_free(truck.x, truck.y)) or \
                (not self.is_bottom_way_free(truck.x, truck.y) and self.is_top_way_free(truck.x, truck.y)):
            print("Moving up towards container spawn..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y - 1))
            self.move_up(truck)

        elif self.is_bottom_way_free(truck.x, truck.y):
            print("Moving down towards container spawn..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y + 1))
            self.move_down(truck)

        else:
            print("Can't find a way to go")

    def do_random_move(self, truck):
        if truck.container is None and truck.x == 0 and truck.y == 0:
            print("Picking up new container..")
            self.pickup_new_container(truck)

        if self.is_field_available_to_place_container(truck.x, truck.y):
            if bool(random.getrandbits(1)):
                self.place_container(truck.x, truck.y, truck)
                return

        valid_moves = self.get_valid_moves(truck)
        valid_moves_str = str(valid_moves).replace("0", "up").replace("1", "down").replace("2", "left").replace("3", "right")
        print("Valid moves:", valid_moves_str)
        random.shuffle(valid_moves)

        move = valid_moves.pop()
        if move == 0:
            print("Moving up..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y - 1))
            self.move_up(truck)
        if move == 1:
            print("Moving down..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x) + "Y" + str(truck.y + 1))
            self.move_down(truck)
        if move == 2:
            print("Moving left..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x - 1) + "Y" + str(truck.y))
            self.move_left(truck)
        if move == 3:
            print("Moving right..", "X" + str(truck.x) + "Y" + str(truck.y), "to",
                  "X" + str(truck.x + 1) + "Y" + str(truck.y))
            self.move_right(truck)


terminal = Terminal(8, 6, 1)
terminal.show()

keyboard.on_press_key("q", lambda _: terminal.pickup_new_container(terminal.truck))
keyboard.on_press_key("e", lambda _: terminal.place_container(terminal.truck.x, terminal.truck.y, terminal.truck))
keyboard.on_press_key("w", lambda _: terminal.move_up(terminal.truck))
keyboard.on_press_key("a", lambda _: terminal.move_left(terminal.truck))
keyboard.on_press_key("s", lambda _: terminal.move_down(terminal.truck))
keyboard.on_press_key("d", lambda _: terminal.move_right(terminal.truck))

while len(terminal.containers_to_place) > 0 or terminal.truck.container is not None:
    if terminal.truck.container is not None:
        terminal.do_random_move(terminal.truck)
        time.sleep(0.2)
    else:
        terminal.move_towards_container_spawn(terminal.truck)
        time.sleep(0.2)


print("\n=========================================================================")
print(f"        DONE PLACING ALL CONTAINERS IN {terminal.steps} STEPS")
print("=========================================================================")
