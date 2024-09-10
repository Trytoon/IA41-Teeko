"""
@desc Ce fichier contient toutes les fonctions utiles au bon déroulement du jeu : vérification des mouvements selon les
@desc règles du jeu, bouger les jetons sur la grille, demander les paramètres de la partie (difficulté et mode de jeu).
"""

import Board as bd

"""
@desc Verifie si une case est vide
@param int[] board - Grille actuelle
@param coordinate - Coordonnée d'origine
@return boolean  - Vrai si la case est vide, faux sinon
"""


def is_empty(board, coordinate):
    if coordinate[0] < 0 or coordinate[0] > 4 or coordinate[1] < 0 or coordinate[1] > 4:
        return False
    if board[coordinate[0]][coordinate[1]] > 0:
        return False
    return True


"""
@desc Verifie si la coordonnée renvoie à une case dans la grille
@param int[] board - Grille actuelle
@param coordinate - Coordonnée d'origine
@return boolean  - Vrai si la coodonnées est valide, faux sinon
"""


def check_coordinates(coordinate):
    return coordinate[0] >= 0 and coordinate[0] <= 4 and coordinate[1] >= 0 and coordinate[1] <= 4


"""
@desc Demande et verifie une coordonnée au joueur
@return coordinate  - La coordonée entrée au clavier
"""


def ask_coordinate():
    valid = False
    coordinate = (-1, -1)
    while (valid == False):
        try:
            tempX = int(input("Entre la valeur de la ligne (1 - 5):"))
            tempY = int(input("Entre la valeur de la colonne (1 - 5):"))
            coordinate = (tempX - 1, tempY - 1)
            valid = check_coordinates(coordinate)
        except Exception:
            print("Coordonnée invalide !")
            valid = False

    return coordinate


"""
@desc Verifie si une piece peut se déplacer de la coordonnée de départ à celle d'arrivée
@param int[] board - Grille actuelle
@param startCoordinate - Coordonnée de départ
@param endCoordinate - Coordonnée d'arrivée
@return boolean  - Vrai si une piece peut se déplacer de la coordonnée de départ à celle d'arrivée
"""


def isMovementValid(board, startCoordinate, endCoordinate):
    if abs(endCoordinate[0] - startCoordinate[0]) > 1 or abs(endCoordinate[1] - startCoordinate[1]) > 1:
        return False

    if bd.getColor(board, endCoordinate) != 0:
        return False

    return True


"""
@desc Verifie si un joueur gagne à une coordonée particulière
@param int[] board - Grille actuelle
@param coordinate - Coordonnée d'origine
@return int  - Renvoie le numéro du joueur qui gagne
"""


def is_victorious(board, coordinate):
    if bd.countAlignedFrom(board, coordinate) >= 4:
        return board[coordinate[0]][coordinate[1]]

    return bd.checkSquare(board, coordinate)


"""
@desc Verifie si le déplacement peut petre effectué selon les règles du jeu
@param int[] board - Grille actuelle
@param startCoordinate - Coordonnée de départ
@param endCoordinate - Coordonnée d'arrivée
@return boolean  - Vrai si le déplacement a été effectué selon les règles du jeu
"""


def moveToken(board, startCoordinate, endCoordinate):
    if isMovementValid(board, startCoordinate, endCoordinate) == False:
        print("You cannot move like this !")
        return False

    color = bd.getColor(board, startCoordinate)
    board[startCoordinate[0]][startCoordinate[1]], board[endCoordinate[0]][endCoordinate[1]] = 0, color
    return True


"""
@desc Demande à l'utilisateur d'entrer la difficulté souhaité pour le jeu
@return int dif  - La difficulté choisie
"""


def chooseDifficulty():
    print("================================================")
    print("Quelle difficulté souhaitez vous ?")
    print("Entrer 1 pour jouer contre une IA qui ne connais rien au jeu")
    print("Entrer 2 pour la difficulté facile")
    print("Entrer 3 pour la difficulté normale")

    dif = input()
    while dif != "1" and dif != "2" and dif != "3":
        print("\nVeuillez entrer une difficulté valide !\n")
        print("Quelle difficulté souhaitez vous ?")
        print("Entrer 1 pour jouer contre une IA qui ne connais rien au jeu")
        print("Entrer 2 pour la difficulté facile")
        print("Entrer 3 pour la difficulté normale")
        dif = input()

    return int(dif)


"""
@desc Demande à l'utilisateur d'entrer le mode de jeu souhaité
@return int mode  - Le mode de jeu choisi
"""


def chooseMode():
    print("\n========================= Quel mode de jeu souhaitez vous ? =========================")
    print("Entrer 1 pour jouer contre une IA")
    print("Entrer 2 pour contre un autre joueur")
    print("Entrer 3 pour voir un combat d'IA\n")

    mode = input()

    while mode != "1" and mode != "2" and mode != "3":
        print("\nVeuillez entrer un mode de jeu valide !\n")
        print("Entrer 1 pour jouer contre une IA")
        print("Entrer 2 pour contre un autre joueur")
        print("Entrer 3 pour voir un combat d'IA\n")
        mode = input()

    return mode
