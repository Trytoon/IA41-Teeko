import Game as game
import Board as bd
import AI as ai
import time
import random as rd

"""
@desc Fonction principale pour dérouler la partie
@param int mode - Mode de jeu (JvJ ou JvE)
"""


def play(mode):
    miniMaxdepth = 0
    withIA = False
    difficulty = 0
    maxi = 0

    # initialisation des parametres de la partie en fonction du mode
    # IA contre joueur
    if mode == 1:
        difficulty = game.chooseDifficulty()
        withIA = True
        maxi = 2

        if difficulty == 2:
            miniMaxdepth = 1

        if difficulty == 3:
            miniMaxdepth = 4

    # ======================= Placement des jetons =================================

    print("\n\n======================= Placement des jetons =================================\n\n")
    i = 0
    while i < 8:

        if i % 2 == 0:
            jeton = 1
        else:
            jeton = 2
        bd.printBoard(bd.board)
        print("\n ===== Joueur ", jeton, " =====")
        coordinate = game.ask_coordinate()

        while not (game.is_empty(bd.board, coordinate)):
            print("\n===== Veuillez entrer une coordonnee valide ! ======")
            bd.printBoard(bd.board)
            print("\n ===== Joueur ", jeton, " =====")
            coordinate = game.ask_coordinate()

        bd.board[coordinate[0]][coordinate[1]] = jeton

        if mode == 1:
            coordinate = ai.getTokenPlacementCoordinate(bd.board, 2)
            bd.board[coordinate[0]][coordinate[1]] = 2
            i += 1

        i += 1

    # ======================= Deroulement de la partie =================================

    winnerPlayer = ai.isTerminal(bd.board)

    if winnerPlayer > 0:
        bd.printBoard(bd.board)
        print("Le joueur ", winnerPlayer, " a gagne!")
        winner = True
    else:
        winner = False

    print("\n\n======================= Deroulement de la partie =================================\n\n")
    nbTours = 0
    while winner == False:

        valid = False
        while valid == False:
            if nbTours % 2 == 0:
                player = 1
            else:
                player = 2
            bd.printBoard(bd.board)
            print("\n\n\n ===== Joueur ", player, " =====")
            print("\nVous allez entrer les coordonnes du jeton à déplacer\n")
            start = game.ask_coordinate()
            print("\nVous allez entrer les nouvelles coordonnes du jeton\n")
            end = game.ask_coordinate()

            if game.isMovementValid(bd.board, start, end):
                if bd.board[start[0]][start[1]] == player and bd.board[end[0]][end[1]] == 0:
                    game.moveToken(bd.board, start, end)
                    valid = True

        nbTours += 1
        if withIA == True and difficulty > 1:
            print("\n\n\n ===== Joueur IA  =====")
            bd.board = ai.minimax(bd.board, miniMaxdepth, -999999999999, +999999999999, True, maxi)[1]
            nbTours += 1
        elif withIA == True and difficulty == 1:
            bd.board = ai.playRandom(bd.board, maxi)
            nbTours += 1

        winnerPlayer = ai.isTerminal(bd.board)

        if winnerPlayer > 0:
            bd.printBoard(bd.board)
            print("Le joueur ", winnerPlayer, " a gagne!")
            winner = True


"""
@desc Laisse s'affronter deux IA
"""


def spectate():
    # Premier coup aléatoire du joueur 1
    ligne = rd.randint(0, 4)
    col = rd.randint(0, 4)
    bd.board[ligne][col] = 1
    bd.printBoard(bd.board)

    nbtours = 0

    for i in range(1, 8, 1):
        if i % 2 == 0:
            jeton = 1
        else:
            jeton = 2
        print("===== Joueur ", jeton, " =====")
        coordinate = ai.getTokenPlacementCoordinate(bd.board, 2)
        bd.board[coordinate[0]][coordinate[1]] = jeton
        time.sleep(2)  # Faut bien y voir quelque chose non ?
        bd.printBoard(bd.board)

    print("\n\n======================= Deroulement de la partie =================================\n\n")
    while ai.isTerminal(bd.board) == 0:
        if nbtours % 2 == 0:
            maxi = 1
        else:
            maxi = 2

        print("===== Joueur ", maxi, " =====")
        prob = rd.randint(0, 5)
        if prob == 0:
            # Sans cette petite probabilité d'erreur, la partie peut ne jamais s'arreter
            bd.board = ai.playRandom(bd.board, maxi)
        else:
            bd.board = ai.minimax(bd.board, 4, -999999999999, +999999999999, True, maxi)[1]
        bd.printBoard(bd.board)
        nbtours += 1

    print("Le joueur ", ai.isTerminal(bd.board), "a gagné !")


mode = int(game.chooseMode())

if mode != 3:
    play(mode)
else:
    spectate()
