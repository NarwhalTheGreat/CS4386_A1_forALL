##################################
## CS4386 Semester B, 2022-2023
## Assignment 1
## Name: Maksim Samokhvalov
## Student ID: 40144120
##################################
import copy
from math import inf as infinity
import random
import numpy as np


# Importing function from game to check score changes


class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score = 0

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name

    def get_isAI(self):
        return self.isAI

    def get_symbole(self):
        return self.symbole

    def get_score(self):
        return self.score

    def add_score(self, score):
        self.score += score

    def available_cells(self, state, player):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if (cell is None):
                    cells.append([x, y])
        return cells

    def get_move(self, state, player):
        print(player)
        games = self.get_valid_moves(self.available_cells(state, player), player)
        top_result = 0
        top_move = [0, 0]
        for i in range(len(games)):
            this_move_result = self.calc_change(state, games[i][0], games[i][1])
            print(games[i][0], games[i][1])
            print(this_move_result)

            if this_move_result > top_result:
                top_result = this_move_result
                top_move = games[i]
        if top_result == 0:
            top_move = random.choice(games)

        return top_move

    def calc_change(self, state, x, y):
        score = 0
        #Check horizontal
        right_count = x
        left_count = x
        while right_count < 5:
            if (state[right_count + 1][y] != None):
                right_count += 1
            else:
                break
        while left_count >= 0:
            if (state[left_count - 1][y] != None):
                left_count -= 1
            else:
                break
        if (right_count - left_count) == 6:
            score += 6
        elif (right_count - left_count) > 2:
            score += 3

        # Check vertical
        bottom_count = y
        top_count = y
        while bottom_count < 5:
            if (state[x][bottom_count + 1] != None):
                bottom_count += 1
            else:
                break
        while top_count >= 0:
            if (state[x][top_count - 1] != None):
                top_count -= 1
            else:
                break
        if (bottom_count - top_count) == 6:
            score += 6
        elif (bottom_count - top_count) > 2:
            score += 3

        return score

    # This method ensures AI never takes the invalid move
    def get_valid_moves(self, games, player):
        player_val = 1
        if player == "X":
            player_val = 0
        valid_moves = []
        for x in range(len(games)):
            if (games[x][0] + games[x][1]) % 2 == player_val:
                valid_moves.append(games[x])
        return valid_moves
