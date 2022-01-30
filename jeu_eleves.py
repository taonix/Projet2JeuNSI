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

        if bonus is not None:
            while lx[i] == bonus[0] and ly[i] == bonus[1]:
                lx[i] = lx[i] + randint(-1, 1)
                ly[i] = ly[i] + randint(-1, 1)

        if lx[i] < 0: lx[i] = taillex - 1
        if lx[i] > taillex - 1: lx[i] = 0
        if ly[i] < 0: ly[i] = tailley - 1
        if ly[i] > tailley - 1: ly[i] = 0


############ Fonction du jeu
def collision(lx, ly, x, y, bonus):
    final = [False, False]
    for i in range(len(lx)):
        if lx[i] == x and ly[i] == y: final[0] = True
        if bonus is not None and bonus[0] == x and bonus[1] == y: final[1] = True
    return final


def jeu(taillex, tailley, params):
    """ taillex et tailley sont les dimensions du jeu souhaitées
    Règles du jeu : """

    ###### Initialisation du jeu #######
    # global delai, tour, vie, invincible, ennemies, score, bonus

    # Initialisation de x et y les coordonnées du carré perso
    x = ceil(taillex / 2)
    y = ceil(tailley / 2)

    current_tip = ""

    # création des objets mobiles en début de jeu (combien ?)
    params['ennemies'] = 3 / 100 * (taillex * tailley)

    lx, ly = cree_listes(x, y, taillex, tailley, ceil(params['ennemies']))

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
        col = collision(lx, ly, x, y, params['bonus'])
        if col[0] and params['invincible'] == 0:
            params['vie'] -= 1
            x = ceil(taillex / 2)
            y = ceil(tailley / 2)
            params['invincible'] = 3
            if params['score'] >= 3: params['score'] -= 3
            if params['vie'] == 0:
                perdu(taillex, tailley)
                continuer = False

        if col[1]:
            params['bonus'] = None
            params['vie'] += 1

        # À vous de jouer, que se passe-t-il s'il y a collision

        tips = ["Use arrow keys to move", "Avoid the red blocks !", "Bonus can spawn for revive"]

        t = t + 1 / fps  # temps passé
        if t > params['delai']:  # si on a passé le délai, on fait bouger les objets
            # et il peut se passer autre chose (au choix)
            t = 0

            if params['tour'] % 10 == 0 and params['tour'] != 0: # chaque 10 tours
                params['ennemies'] = params['ennemies'] + (1 / 100 * (taillex * tailley)) # ajout d'ennemis
                lx, ly = cree_listes(x, y, taillex, tailley, ceil(params['ennemies'])) # On crée de nouveaux ennemies
            if params['tour'] % 20 == 0 and params['tour'] != 0 and params['bonus'] is None: # permet de faire apparaitre un bonus
                params['bonus'] = [randint(0, taillex - 1), randint(0, tailley - 1)] # x, y du bonus à créer
                current_tip = "Take the gold block !" # tips[randint(0, len(tips) - 1)]
            if params['tour'] % 3 == 0: # on change de tip toutes les 3 secondes
                current_tip = tips[randint(0, len(tips) - 1)] # random tip from the list

            bouge(taillex, tailley, lx, ly, params['bonus'])  # on bouge les objets

            params['tour'] += 1  # on incrémente le tour
            params['score'] += 1  # à modifier si on veut faire des points

            if params['invincible'] != 0: params['invincible'] -= 1  # si le perso est invincible on le retire

        # Autres événements qui peuvent se passer à chaque nouvelle frame

        vt = False  # variable de test pour savoir si on a touché un ennemi
        if params['invincible'] != 0: vt = True  # si le perso est invincible, on l'affiche en rouge

        texte = {
            'values': [f"Score : {params['score']}", f"Round : {params['tour']}", f"Ennemies : {len(lx)}",
                       f"Life : {params['vie']}", f"Tips : {current_tip}"],
            'colors': [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [5, 181, 58]],
            'bg_colors': [[181, 146, 5], [0, 0, 0], [0, 0, 0], [156, 6, 6], [255, 255, 255]],
        }  # texte à afficher

        affiche_jeu(taillex, tailley, lx, ly, x, y, texte, vt, params['bonus'])  # affichage du jeu

        # permet de ne pas aller plus vite que fps frames par seconde
        clock.tick(fps)

        # Si on sort de la boucle, c'est qu'on a perdu (ou autre). Afficher alors
    # quelque chose ?


# Lancement du jeu
jeu(15,
    15,
    {
        'delai': 1,
        'tour': 0,
        'vie': 3,
        'invincible': 0,
        'ennemies': 0,
        'score': 0,
        'bonus': None

    })  # 15x15, 1 seconde de délai entre chaque mouvement, 3 vies, 0 ennemies, 0 points, pas de bonus
