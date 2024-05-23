import os
import pickle
import platform
import random
import shutil
import string
from sys import exit

import numpy as np
from colorama import init, Back, Fore, Style

bateau = {'porte-avions': [1] * 5, 'croiseur': [2] * 4,
          'contre-torpilleurs': [3] * 3, 'sous-marin': [4] * 3, 'torpilleur': [5] * 2}
num = {1: 'porte-avions', 2: 'croiseur',
       3: 'contre-torpilleurs', 4: 'sous-marin', 5: 'torpilleur'}


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def title(text):
    terminal_width = shutil.get_terminal_size().columns
    text_width = len(text)
    spaces = " " * ((terminal_width - text_width) // 2)
    centered_text = spaces + text
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + centered_text + Style.RESET_ALL)


def print_centered(text):
    terminal_width = shutil.get_terminal_size().columns
    text_width = len(text)
    spaces = " " * ((terminal_width - text_width) // 2)
    print(Fore.LIGHTWHITE_EX + spaces + text)


def top10():
    if os.path.isfile('scores.txt'):
        with open('scores.txt', 'rb') as f:
            scores = pickle.load(f)
    else:
        scores = {}
    top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    print("")
    title("====  TOP 10  ====")
    print_centered("-" * 30)
    print("{:<27}{:<0}".format(" " * 8 + Style.BRIGHT + "Joueur", "Score" + Style.RESET_ALL).center(
        shutil.get_terminal_size().columns))
    print_centered("-" * 30)
    for joueur, score in top_scores:
        print("{:<20}{:<-6}".format(joueur, score).center(shutil.get_terminal_size().columns))
    print_centered("-" * 30)


def stats(gagnant, point):
    scores = {}
    if os.path.exists("scores.txt"):
        with open('scores.txt', 'rb') as f:
            scores = pickle.load(f)
    if gagnant in scores:
        scores[gagnant] += point
    else:
        scores[gagnant] = point
    with open('scores.txt', 'wb') as f:
        pickle.dump(scores, f)
    return scores


def sauvegarder_partie(grid1, grid2, view1, view2, coups, nom_fichier, j1=None, j2=None, niveau=None, proba=None):
    with open(nom_fichier, 'wb') as fichier:
        data = {'grid1': grid1, 'grid2': grid2, 'view1': view1, 'view2': view2, 'coups': coups}
        if j1 is not None:
            data['j1'] = j1
        if j2 is not None:
            data['j2'] = j2
        if niveau is not None:
            data['niveau'] = niveau
        if proba is not None:
            data['proba'] = proba
        pickle.dump(data, fichier)


def reprendre_partie(nom_fichier):
    with open(nom_fichier, 'rb') as fichier:
        data = pickle.load(fichier)
        if nom_fichier == "SavePlay2.txt":
            grid1, grid2, view1, view2, coups, j1, niveau, proba = data.values()
            return grid1, grid2, view1, view2, coups, j1, niveau, proba
        elif nom_fichier == "SavePlay1.txt":
            grid1, grid2, view1, view2, coups, j1, j2 = data.values()
            return grid1, grid2, view1, view2, coups, j1, j2
        else:
            raise ValueError("Le fichier de sauvegarde est corrompu.")


def printGrid(grille):
    print_centered("    " + " ".join(" " + chr(i + 65) for i in range(len(grille))))
    for i, row in enumerate(grille):
        cells = []
        for cell in row:
            if cell == 9:
                cells.append(Fore.BLUE + str(cell) + Style.RESET_ALL)
            elif cell == 6:
                cells.append(Fore.RED + str(cell) + Style.RESET_ALL)
            elif cell == 0:
                cells.append(Fore.WHITE + str(cell) + Style.RESET_ALL)
            else:
                cells.append(str(cell))
        row_index = str(i + 1).rjust(2)
        terminal_width = shutil.get_terminal_size().columns
        text_width = len(str(row_index))
        spaces = " " * (((terminal_width - text_width) // 3) - len(str(10)))
        print_centered(spaces + row_index + "  " + '  '.join(cells).center(len(grille) * 3 - 1))
    print("")


def calculateProbabilities():
    grid = [[0] * 10 for i in range(10)]
    ships = [5, 4, 3, 3, 2]
    proba = [[0] * 5 for i in range(5)]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if col + row < len(grid[0]) and row < 5 and col < 5:
                for ship in ships:
                    if validPosition(grid, ship, row, col, 1):
                        for i in range(ship):
                            if col + i < 5:
                                proba[row][col + i] += 1
                    if validPosition(grid, ship, row, col, 2):
                        for i in range(ship):
                            if row + i < 5:
                                proba[row + i][col] += 1
    proba = proba + proba[::-1]
    proba = [row + row[::-1] for row in proba]
    return proba


def fill(grille, l, c, d, t, key):
    if d == 1:
        for i in bateau[key]:
            for j in range(c, (c + t)):
                grille[l][j] = i
    else:
        for i in bateau[key]:
            for j in range(l, (l + t)):
                grille[j][c] = i
    return grille


def validPosition(grille, l, c, d, t):
    if grille[l][c] != 0:
        return False
    if d == 1:
        if c + t > 10:
            return False
        for i in range(t):
            if grille[l][c + i] != 0:
                return False
    else:
        if l + t > 10:
            return False
        for i in range(t):
            if grille[l + i][c] != 0:
                return False
    return True


def initGridComp():
    grille = [[0] * 10 for i in range(10)]
    for b in bateau:
        v = False
        while v is False:
            l = random.randint(0, 9)
            c = random.randint(0, 9)
            d = random.randint(1, 2)
            t = len(bateau[b])
            v = validPosition(grille, l, c, d, t)
        grille = fill(grille, l, c, d, t, b)
    return grille


def initGridPlay():
    grille = [[0] * 10 for i in range(10)]
    for i in bateau:
        v = False
        while v is False:
            c = ""
            l = 0
            d = 0
            printGrid(grille)
            while c not in (list(string.ascii_uppercase)[:10]):
                c = input(f"Donnez la lettre pour le {i} :\n")
            while l not in range(1, 11):
                l = int(input(f"Donnez le nombre pour le {i} :\n"))
            while d not in [1, 2]:
                d = int(
                    input("Horizontal (1) ou vertical (2)? \n"))
            v = validPosition(grille, l - 1, ord(c) - 65, d, len(bateau[i]))
            if v is not True:
                print_centered(
                    f"Erreur : Le {i} ne rentre pas dans la grille.")
            else:
                grille = fill(grille, l - 1, ord(c) - 65, d, len(bateau[i]), i)
    printGrid(grille)
    return grille


def hasDrowned(grid, boat):
    for row in grid:
        for cell in row:
            if cell == boat:
                return False
    return True


def oneMove(grid, GridView, l, c):
    a = grid[l][c]
    if grid[l][c] not in (0, 6, 9):
        print_centered("Touché")
        grid[l][c] = 6
        GridView[l][c] = 6
        if hasDrowned(grid, a) is True:
            print_centered(f"{num[a]} coulé")
    else:
        print_centered("A l'eau")
        grid[l][c] = 9
        GridView[l][c] = 9
    return grid, GridView


def isOver(grid):
    for n in range(1, 6):
        for row in grid:
            if n in row:
                return False
    return True


def playComp(view):
    i, j = random.randint(0, 9), random.randint(0, 9)
    while view[i][j] != 0:
        i, j = random.randint(0, 9), random.randint(0, 9)
    return [i, j]


def playComp2(view, proba):
    for i in range(len(view)):
        for j in range(len(view[i])):
            if view[i][j] == 6:
                for k in range(j + 1, len(view[i])):
                    if view[i][k] == 0:
                        return [i, k]
                    elif view[i][k] != 6:
                        break
                for k in range(j - 1, -1, -1):
                    if view[i][k] == 0:
                        return [i, k]
                    elif view[i][k] != 6:
                        break
                for k in range(i + 1, len(view)):
                    if view[k][j] == 0:
                        return [k, j]
                    elif view[k][j] != 6:
                        break
                for k in range(i - 1, -1, -1):
                    if view[k][j] == 0:
                        return [k, j]
                    elif view[k][j] != 6:
                        break

    i, j = np.unravel_index(np.argmax(proba), proba.shape)
    while view[i][j] != 0:
        proba[i][j] = 0
        i, j = np.unravel_index(np.argmax(proba), proba.shape)
    return [i, j]


def playComp3(view):
    for i in range(len(view)):
        for j in range(i % 2, len(view[i]), 2):
            if view[i][j] == 6:
                for k in range(j + 1, len(view[i])):
                    if view[i][k] == 0:
                        return [i, k]
                    elif view[i][k] != 6:
                        break
                for k in range(j - 1, -1, -1):
                    if view[i][k] == 0:
                        return [i, k]
                    elif view[i][k] != 6:
                        break
                for k in range(i + 1, len(view)):
                    if view[k][j] == 0:
                        return [k, j]
                    elif view[k][j] != 6:
                        break
                for k in range(i - 1, -1, -1):
                    if view[k][j] == 0:
                        return [k, j]
                    elif view[k][j] != 6:
                        break

    for i in range(0, len(view), 2):
        for j in range(i % 2, len(view[i]), 2):
            if view[i][j] == 0:
                return [i, j]

    for i in range(1, len(view), 2):
        for j in range(i % 2, len(view[i]), 2):
            if view[i][j] == 0:
                return [i, j]

    i, j = random.randint(0, 9), random.randint(0, 9)
    while view[i][j] != 0:
        i, j = random.randint(0, 9), random.randint(0, 9)
    return [i, j]


def playPlayer(GridPlay, GridComp, GridView):
    position = input("Entrez une position à jouer (ex=E3): ")
    while len(position) <= 1:
        position = input("Entrez une position à jouer (ex=E3): ")
    row, col = int(position[1:]) - 1, ord(position[0]) - 65
    if row < 0 or row > 9 or col < 0 or col > 9:
        print_centered("Position invalide. Rejouez")
        playPlayer(GridPlay, GridComp, GridView)
    elif GridView[row][col] == 9 or GridView[row][col] == 6:
        print_centered("Déjà joué")
        playPlayer(GridPlay, GridComp, GridView)
    return [row, col]


def play1():
    global save
    if os.path.exists("SavePlay1.txt"):
        save = input(
            "Une partie est deja en cours. La reprendre ? (Oui ou Non) ")
        if save == "Oui":
            GridPlay1, GridPlay2, GridViewPlay1, GridViewPlay2, coups1, j1, j2 = reprendre_partie("SavePlay1.txt")
            coups2 = coups1
    if not os.path.exists("SavePlay1.txt") or save == "Non":
        pseudo1 = input("Donnez moi le pseudo d'un joueur: ")
        pseudo2 = input("Donnez moi le pseudo du deuxième joueur: ")
        joueur_debut = random.choice([pseudo1, pseudo2])
        if joueur_debut == pseudo1:
            j1 = pseudo1
            j2 = pseudo2
        else:
            j1 = pseudo2
            j2 = pseudo1
        print_centered(f"Bien, {j1} tu commences")
        print_centered(f"Initialisation de la grille pour {j1}...")
        GridPlay1 = initGridPlay()
        clear()
        print_centered(f"Initialisation de la grille pour {j2}...")
        GridPlay2 = initGridPlay()
        clear()

        GridViewPlay1 = [[0] * 10 for i in range(10)]
        GridViewPlay2 = [[0] * 10 for i in range(10)]

        coups1, coups2 = 0, 0
    while not isOver(GridPlay1) and not isOver(GridPlay2):
        sauvegarder_partie(GridPlay1, GridPlay2, GridViewPlay1,
                           GridViewPlay2, coups1, "SavePlay1.txt", j1, j2)
        print("")
        print_centered(f"{j1}, à toi")
        print_centered(f"Coups de {j1}: ")
        printGrid(GridViewPlay1)
        [l, c] = playPlayer(GridPlay1, GridPlay2, GridViewPlay1)
        print_centered(f"{j1} joue en {chr(c + 65)}{l + 1}")
        GridPlay2, GridViewPlay1 = oneMove(GridPlay2, GridViewPlay1, l, c)
        coups1 += 1
        clear()
        if isOver(GridPlay2):
            print_centered(f"{j1} a gagné en {coups1} coups!")
            os.remove("SavePlay1.txt")
            stats(j1, 1)
            break

        print("")
        print_centered(f"{j2}, c'est ton tour")
        print_centered(f"Coups du {j2}: ")
        printGrid(GridViewPlay2)
        [l, c] = playPlayer(GridPlay2, GridPlay1, GridViewPlay2)
        print_centered(f"{j2} joue en {chr(c + 65)}{l + 1}")
        GridPlay1, GridViewPlay2 = oneMove(GridPlay1, GridViewPlay2, l, c)
        coups2 += 1
        clear()
        if isOver(GridPlay1):
            print_centered(f"{j2} a gagné en {coups2} coups!")
            os.remove("SavePlay1.txt")
            stats(j2, 1)
            break


def play2():
    if os.path.exists("SavePlay2.txt"):
        save = input(
            "Une partie est deja en cours. La reprendre ? (Oui ou Non) ")
        if save == "Oui":
            GridPlay, GridComp, GridViewPlay, GridViewComp, coups1, joueur, niveau, proba = reprendre_partie(
                "SavePlay2.txt")
            coups2 = coups1
    if not os.path.exists("SavePlay2.txt") or save == "Non":
        joueur = input("Quel est ton pseudo ? ")
        niveau = int(
            input("Quel niveau veux-tu ? Facile (1), Moyen (2) ou Difficile (3) ?  "))

        print_centered("Initialisation de la grille pour l'ordinateur...")
        GridComp = initGridComp()
        print_centered(f"Initialisation de la grille pour {joueur}...")
        GridPlay = initGridPlay()

        GridViewPlay = [[0] * 10 for i in range(10)]
        GridViewComp = [[0] * 10 for i in range(10)]
        coups1, coups2 = 0, 0

    proba = np.array(calculateProbabilities())

    while not isOver(GridComp) and not isOver(GridPlay):
        sauvegarder_partie(GridPlay, GridComp, GridViewPlay, GridViewComp,
                           coups1, "SavePlay2.txt", joueur, None, niveau, proba)
        print("")
        print_centered(f"{joueur}, à toi")
        print_centered("Grille de l'ordinateur : ")
        printGrid(GridViewPlay)
        [l, c] = playPlayer(GridPlay, GridComp, GridViewPlay)
        print_centered(f"{joueur} joue en {chr(c + 65)}{l + 1}")
        GridComp, GridViewPlay = oneMove(GridComp, GridViewPlay, l, c)
        coups1 += 1
        if isOver(GridComp):
            print_centered(f"Tu as gagné en {coups1} coups!")
            os.remove("SavePlay2.txt")
            stats(joueur, niveau)
            break
        print("")
        print_centered("Tour de l'ordinateur")

        if niveau == 1:
            [l, c] = playComp(GridViewComp)
        elif niveau == 2:
            [l, c] = playComp2(GridViewComp, proba)
            proba[l, c] = 0
        elif niveau == 3:
            [l, c] = playComp3(GridViewComp)

        print_centered(f"L'ordinateur joue en {chr(c + 65)}{l + 1}")
        GridPlay, GridViewComp = oneMove(GridPlay, GridViewComp, l, c)
        print_centered("Ta grille : ")
        printGrid(GridPlay)
        coups2 += 1
        if isOver(GridPlay):
            print_centered(f"L'ordinateur a gagné en {coups2} coups!")
            os.remove("SavePlay2.txt")
            stats("Ordinateur", niveau)
            break


def play3():
    niveau1 = int(
        input("Quel niveau veux-tu pour l'ordinateur 1? Facile (1), Moyen (2) ou Difficile (3) ? "))
    niveau2 = int(
        input("Quel niveau veux-tu pour l'ordinateur 2? Facile (1), Moyen (2) ou Difficile (3) ? "))
    print_centered("Initialisation de la grille pour l'ordinateur 1...")
    GridComp1 = initGridComp()
    print_centered("Initialisation de la grille pour l'ordinateur 2...")
    GridComp2 = initGridComp()

    GridViewComp1 = [[0] * 10 for i in range(10)]
    GridViewComp2 = [[0] * 10 for i in range(10)]
    coups1, coups2 = 0, 0
    proba1 = np.array(calculateProbabilities())
    proba2 = np.array(calculateProbabilities())

    while not isOver(GridComp1) and not isOver(GridComp2):
        print("")
        print_centered("Tour de l'ordinateur 1")
        if niveau1 == 1:
            [l, c] = playComp(GridViewComp1)
        elif niveau1 == 2:
            [l, c] = playComp2(GridViewComp1, proba1)
            proba1[l, c] = 0
        elif niveau1 == 3:
            [l, c] = playComp3(GridViewComp1)

        print_centered(f"L'ordinateur 1 joue en {chr(c + 65)}{l + 1}")
        GridComp2, GridViewComp1 = oneMove(GridComp2, GridViewComp1, l, c)
        coups1 += 1
        if isOver(GridComp2):
            print_centered("Grille de l'ordinateur 1")
            printGrid(GridComp1)
            print_centered("Grille de l'ordinateur 2")
            printGrid(GridComp2)
            print_centered(f"L'ordinateur 1 a gagné en {coups1} coups!")
            stats("Ordinateur 1", niveau1)
            break
        print("")
        print_centered("Tour de l'ordinateur 2")
        if niveau2 == 1:
            [l, c] = playComp(GridViewComp2)
        elif niveau2 == 2:
            [l, c] = playComp2(GridViewComp2, proba2)
            proba2[l, c] = 0
        elif niveau2 == 3:
            [l, c] = playComp3(GridViewComp2)
        print_centered(f"L'ordinateur joue en {chr(c + 65)}{l + 1}")
        GridComp1, GridViewComp2 = oneMove(GridComp1, GridViewComp2, l, c)
        coups2 += 1
        if isOver(GridComp1):
            print_centered("Grille de l'ordinateur 1")
            printGrid(GridComp1)
            print_centered("Grille de l'ordinateur 2")
            printGrid(GridComp2)
            print_centered(f"L'ordinateur 2 a gagné en {coups2} coups!")
            stats("Ordinateur 2", niveau2)
            break


def menu():
    print_centered("")
    title("=== MENU PRINCIPAL ===")
    print_centered("1. Jouer à 2 joueurs")
    print_centered("2. Jouer contre l'IA")
    print_centered("3. Deux IA l'une face à l'autre")
    print_centered("4. Voir les règles du jeu")
    print_centered("5. Voir les statistiques")
    print_centered("6. Quitter le jeu")
    choix = input("? ")
    return int(choix)


def rules():
    print("")
    title("=== REGLES DU JEU ===")
    print_centered("Ce jeu se joue à deux joueurs, chacun dispose d’une grille de 10 cases")
    print_centered(" sur 10 cases, les colonnes de cette grille sont indiquées par une lettre")
    print_centered(" de A à J et les lignes sont numérotées de 1 à 10.")
    print_centered("Sur cette grille sont placés 5 bateaux en horizontal ou en vertical :")
    print_centered("1. Un porte-avions (5 cases)")
    print_centered("2. Un croiseur (4 cases)")
    print_centered("3. Un contre-torpilleurs (3 cases)")
    print_centered("4. Un sous-marin (3 cases)")
    print_centered("5. Un torpilleur (2 cases)")
    print_centered("Le but de chaque joueur est de couler tous les bateaux de l’autre joueur.")
    print_centered("Chaque joueur joue tour à tour en proposant une position où lancer une ")
    print_centered("torpille pour toucher un bateau adverse en indiquant une position sur la")
    print_centered(" grille (par exemple B3) et l’adversaire répond :")
    print_centered("- Touché (6) si la torpille touche un bateau,")
    print_centered("- Coulé si l’adversaire touche un bateau et le coule,")
    print_centered("- ou À l’eau (9) si rien ou un bateau déjà coulé a été touché.")


def game():
    choix = menu()
    while choix not in (1, 2, 3, 4, 5, 6):
        choix = menu()
    if choix == 1:
        play1()
        game()
    elif choix == 2:
        play2()
        game()
    elif choix == 3:
        play3()
        game()
    elif choix == 4:
        rules()
        game()
    elif choix == 5:
        top10()
        game()
    elif choix == 6:
        print_centered("Merci d'avoir joué!")
        exit()


if __name__ == '__main__':
    print(Fore.CYAN + Style.BRIGHT)
    print("              |    |    |                 ")
    print("             )_)  )_)  )_) ")
    print("            )___))___))___)\\\\        Bienvenue         ")
    print("           )____)____)_____)\\\\\\\\            dans le jeu                             ")
    print("         _____|____|____|____\\\\\\\\\\\\__           de la Bataille Navale!")
    print("---------\\                   /---------")
    print("      ^^^^^ ^^^^^^^^^^^^^^^^^^^^^")
    print("     ^^^^      ^^^^     ^^^    ^^")
    print("            ^^^^      ^^^")
    game()
