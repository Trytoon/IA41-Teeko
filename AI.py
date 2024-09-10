"""
@desc Ce fichier contient toutes les fonctions utiles à l'IA du jeu (generation du coup à jouer)
"""

import Game as game
import Board as bd
import random as rd
import copy

"""
@desc Genère tous les coups possibles d'un joueur
@param int[] board - Grille actuelle
@param int player - Joueur qui joue
@return states - Liste qui contient tous les coups du joueur
"""


def nextState(board, player):
    states = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                start_coordinate = (i, j)
                i2 = i - 1
                j2 = j - 1
                for i2 in range(i2 + 3):
                    for j2 in range(j2 + 3):
                        if game.check_coordinates((i2, j2)):
                            if game.isMovementValid(board, start_coordinate, (i2, j2)):
                                temp = copy.deepcopy(board)
                                game.moveToken(temp, start_coordinate, (i2, j2))
                                states.append(temp)
    return states


"""
@desc Verifie si la partie est finie
@param int[] board - Grille actuelle
@return victoire - Retourne le numéro du joueur victorieux
"""


def isTerminal(board):
    for i in range(5):
        for j in range(5):
            if board[i][j] != 0:
                if game.is_victorious(board, (i, j)) > 0:
                    return game.is_victorious(board, (i, j))
    return 0


"""
@desc Calcule l'écratement maximal des jetons d'un joueur, c'est à dire la surface couverte par un joueur.
@param int[] board - Grille actuelle
@param int player - Joueur qui joue
@return surf - La surface calculée
"""


def surface(board, player):
    coos = bd.searchTokens(board, player)
    surf = 1
    for i in range(len(coos)):
        x1, y1 = coos[i]
        for j in range(i + 1, len(coos), 1):
            x2, y2 = coos[j]
            if x1 > x2:
                xf = x1 - x2 + 1
            else:
                xf = x2 - x1 + 1

            if (y1 > y2):
                yf = y1 - y2 + 1
            else:
                yf = y2 - y1 + 1

            temp = xf * yf
            surf = max(surf, temp)

    return surf


"""
@desc Associe une case à un poids, plus il est grand, plus les pions poudu joueur pourront se déplacer sur la grille
@param int[]  board - Grille actuelle
@param int player - Joueur qui joue
@return int v - Le poids des pions d'un joueur
"""


def pawn_weight(board, player):
    ppp = [[0, 1, 1, 1, 0],
           [1, 2, 2, 2, 1],
           [1, 2, 3, 2, 1],
           [1, 2, 2, 2, 1],
           [0, 1, 1, 1, 0]]

    coos = bd.searchTokens(board, player)

    v = 0

    for coordinate in coos:
        v += ppp[coordinate[0]][coordinate[1]]

    return v


"""
@desc Fonction heuristique utilisée dans le minimax
@param int board - Grille actuelle
@param int player - Joueur qui joue
@return int v2-v1 - La valeur de la grille pour un joueur donné
"""


def eval3(state, player):
    opponent = 1 if player == 2 else 2

    v1 = 1 / surface(state, opponent) + pawn_weight(state, opponent) * max(bd.countMaxAligned(state, opponent),
                                                                           bd.countMaxInSquare(state, opponent))
    v2 = 1 / surface(state, player) + pawn_weight(state, player) * max(bd.countMaxAligned(state, player),
                                                                       bd.countMaxInSquare(state, player))

    return v2 - v1


"""
@desc Algorithme Minimax (avec elagage alpha beta): Choisi le meilleur coup de l'IA
@param int[] board - Grille actuelle
@param int depth - Profondeur de recherche
@param int alpha - Valeur alpha
@param int beta - Valeur beta
@param boolean maxiMizingPlayer - Est-ce que c'est au tour du joueur min ou max ?
@return int max - La valeur max
@return int[] bestMove  - La grille associée à la valeur max
"""


def minimax(state, depth, alpha, beta, maxiMizingPlayer, maxi):
    mini = 1 if maxi == 2 else 2

    if isTerminal(state) == maxi:
        return 99 + depth, state

    if isTerminal(state) == mini:
        return -99 - depth, state

    if maxiMizingPlayer:
        if depth == 0 or isTerminal(state) != 0:
            return eval3(state, maxi), state
        maxEva = -9999
        ns = nextState(state, maxi)
        bestMove = None

        for child in ns:
            eva = minimax(child, depth - 1, alpha, beta, False, maxi)[0]

            maxEva = max(maxEva, eva)
            alpha = max(alpha, maxEva)

            if (eva == maxEva):
                bestMove = child
            if beta <= alpha:
                bestMove = child
                break
        return maxEva, bestMove

    else:
        if depth == 0 or isTerminal(state) != 0:
            return eval3(state, mini), state

        minEva = +9999
        ns = nextState(state, mini)
        bestMove = None

        for child in ns:
            eva = minimax(child, depth - 1, alpha, beta, True, maxi)[0]
            minEva = min(minEva, eva)
            beta = min(beta, eva)

            if (eva == minEva):
                bestMove = child

            if beta <= alpha:
                break
        return minEva, bestMove


"""
@desc Calcule la meilleure case pour poser un jeton lorsque l'ordinateur joue.
@param int[] board - Grille actuelle
@param int player - Joueur qui joue
@return temp - Un tuple contenant les coordonnées d'une case
"""


def getTokenPlacementCoordinate(board, joueur):
    ppp = [[0, 1, 0, 1, 0],
           [1, 2, 1, 2, 1],
           [1, 1, 3, 1, 0],
           [1, 2, 1, 2, 1],
           [0, 1, 0, 1, 0]]
    tuples = []
    if joueur == 1:
        opponent = 2
    else:
        opponent = 1
    for i in range(5):
        for j in range(5):
            if board[i][j] != 0:

                tuples.extend([(i, j), 0])
            else:
                board[i][j] = joueur
                if bd.countAlignedFrom(board, [i, j]) == 4 or bd.countSquare(board, [i, j]) == 4:
                    temp = 99
                else:
                    temp = bd.countAlignedFrom(board, [i, j]) + bd.countSquare(board, [i, j])

                board[i][j] = opponent
                if bd.countAlignedFrom(board, [i, j]) == 4 or bd.countSquare(board, [i, j]) == 4:
                    temp2 = 99
                else:
                    temp2 = bd.countAlignedFrom(board, [i, j]) + bd.countSquare(board, [i, j])
                board[i][j] = 0
                if abs(temp) < abs(temp2):
                    temp2 = temp2 * 2 - ppp[i][j]
                    tuples.extend([(i, j), temp2])
                else:
                    temp = temp * 2 + ppp[i][j]
                    tuples.extend([(i, j), temp])
    max = 0
    tokencoord = (0, 0)

    for i in range(25):
        if max < (abs(tuples[i * 2 + 1])):
            max = (abs(tuples[i * 2 + 1]))
            tokencoord = tuples[i * 2]

    return tokencoord


"""
@desc Genere tous les coups d'un joueur et en choisi un aléatoirement
@param int[] board - Grille actuelle
@param int player - Joueur qui joue
@return int[] ns[coup] - Le coup choisi
"""


def playRandom(board, player):
    ns = nextState(board, player)
    coup = rd.randint(0, len(ns) - 1)
    return ns[coup]
