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
        best_score, best_move = self.abnegamax(state, player, 0, 0, 6, -infinity, infinity)
        return best_move

    #performs negamax search for move that scores the highest result for the starting player with Alpha-Beta Pruning
    def abnegamax(self, board, player_symbol, score, current_depth, max_depth, alpha, beta):
        #calculate possible moves
        games = self.get_valid_moves(self.available_cells(board, player_symbol), player_symbol)
        #check if game is over (no moves left) or max depth is reached. if so, bubble up.
        if ((current_depth == max_depth) or (len(games) == 0)):
            return score, None
        #set up best score and placeholder for best move
        best_score = -infinity
        best_move = None
        #flip player for the next move
        if player_symbol == "X":
            player_symbol_next = "O"
        else:
            player_symbol_next = "X"
        #Iterate through each possible move
        for move in games:
            #simulate this move, calculate its score and effect on the board state
            new_score = score + self.calc_change(board, move)
            new_board = board
            new_board[move[0], move[1]] = player_symbol
            #start recursion after this move
            recursed_score, recursed_move = self.abnegamax(new_board, player_symbol_next, -new_score, (current_depth + 1),
                                                           max_depth, -beta, -max(alpha, best_score))
            #reset board (had a weird bug)
            new_board[move[0], move[1]] = None

            #inverse score to account for alternating
            current_score = -recursed_score

            #record best score if found
            if current_score > best_score:
                best_score = current_score
                best_move = move
                #prune unfavourable branch
                if best_score >= beta:
                    return best_score, best_move

        return best_score, best_move

    #Returns best possible move given board and the player moving next.
    #Assumes there is at least 1 possible move
    #If all moves are equally good, returns a random move among the possible options
    #Hand made for testing purposes
    #                    NOT USED IN FINAL (abnegamax) IMPLEMENTATION
    def get_best_move(self, player, state):
        games = self.get_valid_moves(self.available_cells(state, player), player)
        best_result = 0
        best_move = [0, 0]
        for i in range(len(games)):
            this_move_result = self.calc_change(state, games[i])

            if this_move_result > best_result:
                best_result = this_move_result
                best_move = games[i]
        if best_result == 0:
            best_move = random.choice(games)
        return best_move

    #Calculates change this move has on score, assumes player making this move is allowed to do so
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
        if hor_streak == 5:
            score += 6
        elif hor_streak > 1:
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
