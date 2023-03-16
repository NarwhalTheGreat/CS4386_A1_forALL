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
        random_choice = random.choice(games)

        best_score, best_move = self.negamax(state, 1, 0, player, None)

        #if all else fails, just give us a random one

        print(best_score)
        print(best_move)
        return best_move

    #Algorithm to perform negamax search to determine best move. Assumes player never makes the wrong move
    def negamax(self, state, max_depth, current_depth, player, current_move):
        #Get list of possible moves from the state we are working with
        games = self.get_valid_moves(self.available_cells(state, player), player)

        #If game is over (no more moves left) or max depth is reached, bubble up
        if ((len(games) == 0) or (max_depth == current_depth)):
            return self.calc_change(state, current_move), None


        best_move = None
        best_score = -infinity

        if player == "X":
            player = "O"
        else:
            player = "X"

        for move in games:
            new_state = self.simulate_move(state, move, player)
            print(new_state)
            recursed_score, current_move = self.negamax(new_state, max_depth, current_depth + 1, player, move)
            current_score = -recursed_score
            if current_score > best_score:
                best_score = current_score
                best_move = move

        return best_score, best_move


    #Simulates a move on a state, chaning the board
    def simulate_move(self, state, move, player):
        if (player == "X"):
            state[move[0]][move[1]] = "X"
        else:
            state[move[0]][move[1]] = "O"
        return state

    #finds best move out of set of moves and with a state of board as context
    def best_move(self, games, state):
        best_score = 0
        best_move = [0, 0]
        for i in range(len(games)):
            this_move_result = self.calc_change(state, games[i])

            if this_move_result > best_score:
                best_score = this_move_result
                best_move = games[i]
        return best_score, best_move


    #This function scans the change a move makes to the player's score (the one making said move)
    #Taking some inspiration from alignment function in game.py
    def calc_change(self, state, move):
        x = move[0]
        y = move[1]
        score = 0
        #Check horizontal
        right_count = x + 1
        left_count = x - 1
        hor_streak = 0
        while right_count < 5:
            if (state[right_count][y] != None):
                hor_streak += 1
                right_count += 1
            else:
                break
        while left_count >= 0:
            if (state[left_count][y] != None):
                left_count -= 1
                hor_streak += 1
            else:
                break
        if hor_streak == 6:
            score += 6
        elif hor_streak > 2:
            score += 3

        # Check vertical
        bottom_count = y + 1
        top_count = y - 1
        ver_streak = 0
        while bottom_count < 5:
            if (state[x][bottom_count] != None):
                bottom_count += 1
                ver_streak += 1
            else:
                break
        while top_count >= 0:
            if (state[x][top_count] != None):
                top_count -= 1
                ver_streak += 1

            else:
                break
        if ver_streak == 5:
            score += 6
        elif ver_streak > 1:
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
