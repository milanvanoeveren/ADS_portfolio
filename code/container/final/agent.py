import os
from _csv import writer
from datetime import datetime
import torch
import random
from collections import deque

import pandas as pd
from sklearn.model_selection import train_test_split

from matplotlib import pyplot as plt

from dqn_model import DQN, QTrainer
from terminal_env import TerminalEnv

MAX_MEMORY = 100_000
BATCH_SIZE = 24
LR = 0.001

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Device:", device)

data = pd.read_csv('container_dataset.csv', header=None)
train_set, rem = train_test_split(data, train_size=0.8)
val_set, test_set = train_test_split(rem, train_size=0.5)


class Agent:
    def __init__(self, env):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.env = env

        has_set = env.set is not None

        if has_set:
            self.random_games = 0
        else:
            self.random_games = 400

        input_size = len(env.get_state())
        output_size = env.width * env.height

        self.model = DQN(input_size, 256, output_size, has_set).to(device)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma, requires_grad=False)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #   self. trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, env, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = self.random_games - self.n_games
        final_move = [0] * (env.width * env.height)
        if random.randint(0, self.random_games) < self.epsilon:
            random_index = random.randint(0, env.width * env.height - 1)
            final_move[random_index] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float32, device=device)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def show_fields(env):
    data = env.fields

    # Creating a list of colors
    colors = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Indigo', 'Violet', 'White', 'Gray', 'Black', 'Crimson',
              'Maroon', 'Magenta', 'Aquamarine', 'Beige', 'Turquoise', 'Cyan', 'Olive', 'Navy', 'Lime', 'Lavender',
              'Mint', 'Plum', 'Salmon', 'Fuchsia', 'Teal', 'Sage', 'Ginger', 'Tan', 'Auburn', 'Mauve', 'Peach', 'Ivory',
              'Coral', 'Mustard', 'Cherry', 'Slate', 'Honeydew', 'Azure', 'Scarlet', 'Plaid', 'Rust', 'Gold', 'Cocoa',
              'Cinnamon', 'Cardinal', 'Periwinkle', 'Lilac', 'Moss', 'Wheat', 'Sienna', 'Khaki', 'Orchid']

    # Setting up the plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the array values
    for x in range(len(data)):
        for y in range(len(data[x])):
            for z in range(len(data[x][y])):
                if data[x][y][z] != 0:
                    ax.bar3d(x, y, z, 1, 0.4, 1, color=colors[data[x, y, z] - 1], alpha=1, edgecolor='black')

    plt.title(f"Record: {env.score}")

    # Labeling the axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.view_init(60, -160)

    # Showing the plot
    plt.show()


def train(chosen_set=None):
    record_amount = 0
    start_time = datetime.now()
    record = -1000
    env = TerminalEnv(4, 4, 2, chosen_set)
    agent = Agent(env)
    agent.model.load()

    train_size = 0
    if env.set is not None:
        train_size = env.set.shape[0]

    print(train_size)
    game_start_time = datetime.now()
    while True:
        # get old state
        state_old = env.get_state()

        # get move
        final_move = agent.get_action(env, state_old)

        # perform move and get new state
        reward, done, score = env.play_step(final_move)
        state_new = env.get_state()

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            if score > record:
                record_amount = 0
                record = score
                agent.model.save()
                show_fields(env)
            if score == record:
                record_amount += 1
                agent.model.save()

            env.reset(agent.n_games)
            agent.n_games += 1
            agent.train_long_memory()

            runtime = datetime.now() - start_time

            game_end_time = datetime.now()

            print('Game', agent.n_games, 'Score', score, 'Record:', record, "Record amount:", record_amount,
                  "Game time:",
                  game_end_time - game_start_time, "Total time:", runtime)

            game_start_time = game_end_time

            if chosen_set is not None and agent.n_games >= train_size:
                break


def save_tune(tune_name, game_id, score, run_time, lr, bs):
    row = [tune_name, game_id, score, run_time, lr, bs]

    with open('tune_training.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(row)
        f_object.close()


def train_tune(chosen_set=None, tune_name=""):
    record_amount = 0

    start_time = datetime.now()
    record = -1000
    env = TerminalEnv(4, 4, 2, chosen_set)
    agent = Agent(env)
    agent.model.load()

    train_size = 0
    if env.set is not None:
        train_size = env.set.shape[0]

    game_start_time = datetime.now()
    while True:
        # get old state
        state_old = env.get_state()

        # get move
        final_move = agent.get_action(env, state_old)

        # perform move and get new state
        reward, done, score = env.play_step(final_move)
        state_new = env.get_state()

        # train short memory
        # agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            if score > record:
                record_amount = 0
                record = score
                # agent.model.save()
                show_fields(env)
            if score == record:
                record_amount += 1
                # agent.model.save()

            env.reset(agent.n_games)
            agent.n_games += 1
            # agent.train_long_memory()

            runtime = datetime.now() - start_time

            game_end_time = datetime.now()
            game_time = game_end_time - game_start_time

            print('Game', agent.n_games, 'Score', score, 'Record:', record, "Record amount:", record_amount,
                  "Game time:",
                  game_end_time - game_start_time, "Total time:", runtime)

            save_tune(tune_name, game_id=agent.n_games, score=score, run_time=game_time, lr=LR, bs=BATCH_SIZE)

            if agent.n_games == 1500:
                break

            game_start_time = game_end_time

            # if chosen_set is not None and agent.n_games >= train_size:
            #     break


# with torch.no_grad():
#     tune_name = f'Getraind'
#     train_tune(tune_name=tune_name)
#
# learning_rates = [0.001]
# batch_sizes = [24]
#
# for learning_rate in learning_rates:
#     LR = learning_rate
#     for batch_size in batch_sizes:
#         BATCH_SIZE = batch_size

train()
