#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Rappelez votre nom ici au cas où :

from graphique_jeu import *
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT, QUIT

from random import randint
from math import *


### Vos fonctions ci-dessous

def cree_listes(x, y, taillex, tailley, nbre):
    """
    x, y : coordonnées du joueur
    taillex, tailley : dimensions de l'écran de jeu
    nbre : nombre de carrés voulus
    crée deux listes lx et ly de carrés mobiles en début de jeu,
    et les renvoie"""
    # votre code ici
    lx = {}
    ly = {}

    for i in range(nbre):

        randx = randint(0, taillex - 1)
        randy = randint(0, tailley - 1)

        while randx == x and randy == y:
            randx = randint(0, taillex - 1)
            randy = randint(0, tailley - 1)

        ly[i] = randy
        lx[i] = randx

    return (lx, ly)


def bouge(taillex, tailley, lx, ly, bonus):
    for i in range(len(lx)):

        lx[i] = lx[i] + randint(-1, 1)
        ly[i] = ly[i] + randint(-1, 1)

        if bonus is not None :
            while lx[i] == bonus[0] and ly[i] == bonus[1]:
                lx[i] = lx[i] + randint(-1, 1)
                ly[i] = ly[i] + randint(-1, 1)

        if lx[i] < 0: lx[i] = taillex - 1
        if lx[i] > taillex - 1: lx[i] = 0
        if ly[i] < 0: ly[i] = tailley - 1
        if ly[i] > tailley - 1: ly[i] = 0


############ Fonction du jeu

delai = 1  # délai en secondes entre deux mouvements des objets mobiles
tour = 0  # nombre de tours effectués
vie = 3  # nombre de vies de départ
invincible = 0  # nombre de tours d'invincibilité
ennemies = 0  # nombre d'ennemis
score = 0  # score du joueur
bonus = None  # bonus en cours


def collision(lx, ly, x, y, bonus):
    final = [False, False]
    for i in range(len(lx)):
        if lx[i] == x and ly[i] == y: final[0] = True
        if bonus is not None and bonus[0] == x and bonus[1] == y: final[1] = True
    return final


def jeu(taillex, tailley):
    """ taillex et tailley sont les dimensions du jeu souhaitées
    Règles du jeu : """

    ###### Initialisation du jeu #######
    global delai, tour, vie, invincible, ennemies, score, bonus

    # Initialisation de x et y les coordonnées du carré perso
    x = ceil(taillex / 2)
    y = ceil(tailley / 2)

    # création des objets mobiles en début de jeu (combien ?)
    ennemies = 3 / 100 * (taillex * tailley)

    lx, ly = cree_listes(x, y, taillex, tailley, ceil(ennemies))

    # Autres initialisation (score, points de vie, ... ?)

    # Cette variable pourra passer à False quand on aura perdu (ou qu'on voudra
    # arrêter le jeu)
    continuer = True
    t = 0  # temps écoulé depuis le délai, ne pas modifier

    ###### Boucle principale du jeu #######
    while continuer:
        # Gestion des évènements
        for event in pygame.event.get():  # Si on quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Si touche appuyée
            if event.type == pygame.KEYDOWN:

                if event.key == K_LEFT:
                    # appui sur la touche "gauche"
                    # le carré perso se déplace à gauche
                    if x != 0: x = x - 1
                    pass

                elif event.key == K_RIGHT:
                    # appui sur la touche "droite"
                    if x != taillex - 1: x = x + 1
                    pass

                elif event.key == K_UP:
                    # appui sur la touche "haut"
                    if y != 0: y = y - 1
                    pass

                elif event.key == K_DOWN:
                    # appui sur la touche "bas"
                    if y != tailley - 1: y = y + 1
                    pass

        # Gestion des collisions
        # On récupère l'indice de collision dans i_coll
        col = collision(lx, ly, x, y, bonus)
        if col[0] and invincible == 0:
            vie = vie - 1
            x = ceil(taillex / 2)
            y = ceil(tailley / 2)
            invincible = 3
            if score >= 3: score -= 3
            if vie == 0:
                continuer = False

        if col[1]:
            bonus = None
            vie += 1

        # À vous de jouer, que se passe-t-il s'il y a collision

        t = t + 1 / fps  # temps passé
        if t > delai:  # si on a passé le délai, on fait bouger les objets
            # et il peut se passer autre chose (au choix)
            t = 0

            if tour % 10 == 0 and tour != 0:
                ennemies = ennemies + (1 / 100 * (taillex * tailley))
                lx, ly = cree_listes(x, y, taillex, tailley, ceil(ennemies))
            if tour % 20 == 0 and tour != 0 and bonus is None: bonus = [randint(0, taillex - 1), randint(0, tailley - 1)]

            bouge(taillex, tailley, lx, ly, bonus)

            tour += 1
            score += 1

            if invincible != 0: invincible = invincible - 1

        # Autres événements qui peuvent se passer à chaque nouvelle frame

        texte = {
            'values': [f"Score : {score}", f"Round : {tour}", f"Ennemies : {len(lx)}", f"Life : {vie}",
                       "Tips : Use arrow keys to move"],
            'colors': [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [5, 181, 58]],
            'bg_colors': [[181, 146, 5], [0, 0, 0], [0, 0, 0], [156, 6, 6], [255, 255, 255]],
        }

        vt = False
        if invincible != 0: vt = True

        affiche_jeu(taillex, tailley, lx, ly, x, y, texte, vt, bonus)

        # permet de ne pas aller plus vite que fps frames par seconde
        clock.tick(fps)

        # Si on sort de la boucle, c'est qu'on a perdu (ou autre). Afficher alors
    # quelque chose ?


# Lancement du jeu
jeu(15, 15)
