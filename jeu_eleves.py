#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Rappelez votre nom ici au cas où :

from graphique_jeu import *
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT, QUIT

from random import randint
from math import *


### Vos fonctions ci-dessous

def cree_listes(taillex, tailley, nbre):
    """ 
    taillex, tailley : dimensions de l'écran de jeu
    nbre : nombre de carrés voulus
    crée deux listes lx et ly de carrés mobiles en début de jeu,
    et les renvoie"""
    # votre code ici
    lx = {}
    ly = {}

    for i in range(nbre):
        lx[i] = randint(0, taillex - 1)
        ly[i] = randint(0, tailley - 1)

    return (lx, ly)


def bouge(taillex, tailley, lx, ly):

    for i in range(len(lx)):

        lx[i] = lx[i] + randint(-1, 1)
        ly[i] = ly[i] + randint(-1, 1)

        if lx[i] < 0: lx[i] = taillex - 1
        if lx[i] > taillex - 1: lx[i] = 0
        if ly[i] < 0: ly[i] = tailley - 1
        if ly[i] > tailley - 1: ly[i] = 0

############ Fonction du jeu

delai = 1  # délai en secondes entre deux mouvements des objets mobiles
tour = 0  # nombre de tours effectués
def jeu(taillex, tailley):
    """ taillex et tailley sont les dimensions du jeu souhaitées
    Règles du jeu : """

    ###### Initialisation du jeu #######
    global delai, tour

    # création des objets mobiles en début de jeu (combien ?)
    lx, ly = cree_listes(taillex, tailley, ceil((taillex * tailley) / taillex))

    # Initialisation de x et y les coordonnées du carré perso
    x = ceil(taillex / 2)
    y = ceil(tailley / 2)

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
                    if x != taillex-1: x = x + 1
                    pass

                elif event.key == K_UP:
                    # appui sur la touche "haut"
                    if y != 0: y = y - 1
                    pass

                elif event.key == K_DOWN:
                    # appui sur la touche "bas"
                    if y != tailley-1: y = y + 1
                    pass

        # Gestion des collisions
        # On récupère l'indice de collision dans i_coll
        # i_coll = collision(lx, ly, x, y)
        # À vous de jouer, que se passe-t-il s'il y a collision

        t = t + 1 / fps  # temps passé
        if t > delai:  # si on a passé le délai, on fait bouger les objets
            # et il peut se passer autre chose (au choix)
            t = 0
            bouge(taillex, tailley, lx, ly)
            #delai = delai - 0.1
            tour = tour + 1

        # Autres événements qui peuvent se passer à chaque nouvelle frame
        affiche_jeu(taillex, tailley, lx, ly, x, y, [f"Ennemies : {len(lx)}", f"Score : {tour}"])

        # permet de ne pas aller plus vite que fps frames par seconde
        clock.tick(fps)

        # Si on sort de la boucle, c'est qu'on a perdu (ou autre). Afficher alors
    # quelque chose ?


# Lancement du jeu
jeu(15, 15)