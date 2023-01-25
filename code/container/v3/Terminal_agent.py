import random
import time
from operator import itemgetter
import pygame
from Terminal_game import ContainerGameAI

import torch
import random
import numpy as np
from collections import deque
from Terminal_model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(20, 256, 20)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = []
        for x in range(game.width):
            for y in range(game.height):
                if len(game.fields[x][y].containers) > 0:
                    state.append(1)
                else:
                    state.append(0)

        return np.array(state, dtype=int)

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

    def get_action(self, game, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 200 - self.n_games
        final_move = [0] * (game.width * game.height)
        if random.randint(0, 200) < self.epsilon and len(game.get_all_available_fields()) > 0:
            final_move = game.get_random_move()
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        # print("Final move:", final_move)
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = -1000
    agent = Agent()
    agent.model.load()
    game = ContainerGameAI()
    while True:
        # time.sleep(0.1)
        # get old state
        state_old = agent.get_state(game)
        # print("Old state:", state_old)

        # get move
        final_move = agent.get_action(game, state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train the long memory (experience replay memory), plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

game = ContainerGameAI()

train()

# while len(game.containers_to_place) > 0 and len(game.get_all_available_fields()) > 0:
#     pygame.event.get()
#
#     available_fields = game.get_all_available_fields()
#     random.shuffle(available_fields)
#     # available_fields.sort(reverse=True, key=itemgetter(1))
#
#     print("Available fields:", available_fields)
#
#     next_move = available_fields.pop(0)[0]
#     x = int(next_move[1])
#     y = int(next_move[3])
#
#     container_id = game.containers_to_place.pop(0)
#     game.place_container(container_id, x, y)
#
#     time.sleep(0.2)
