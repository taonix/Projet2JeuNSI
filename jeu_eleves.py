#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Rappelez votre nom ici au cas où :

from graphique_jeu import *
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT, QUIT

from random import randint
from math import *


### Vos fonctions ci-dessous

def cree_listes(x, y, taillex, tailley, nbre, lx, ly):
    """
    x, y : coordonnées du joueur
    taillex, tailley : dimensions de l'écran de jeu
    nbre : nombre de carrés voulus
    crée deux listes lx et ly de carrés mobiles en début de jeu,
    et les renvoie"""
    # votre code ici

    for i in range(nbre):  # crée les carrés

        randx = randint(0, taillex - 1)  # choisit un x aléatoire
        randy = randint(0, tailley - 1)  # choisit un y aléatoire

        while randx == x and randy == y:  # si ils sont sur le joueur
            randx = randint(0, taillex - 1)  # choisit un x aléatoire
            randy = randint(0, tailley - 1)  # choisit un y aléatoire

        ly.append(randy)  # ajoute le y
        lx.append(randx)  # ajoute le carré à la liste

    return (lx, ly)  # renvoie les listes


def gere_phantom(phantom, y, x):
    """Gère la le déplacement des phantoms.
    La fonction renvoie la liste les coordonnées du phantom"""
    if len(phantom) > 0:
        if phantom[1] == 0: phantom = []
        else:
            phantom[1] -= 1
            if phantom[1] > y + 2: phantom[0] = x
            pygame.mixer.Channel(3).play(pygame.mixer.Sound(r'.\assets\sounds\phantom.wav'))
    return phantom


def play_walk_sound(chan_walk):
    if chan_walk >= 7:
        chan_walk = 4
    else:
        chan_walk += 1
    pygame.mixer.Channel(chan_walk).play(pygame.mixer.Sound(r'.\assets\sounds\move.wav'))
    return chan_walk


def bouge(taillex, tailley, lx, ly, bonus):  # fonction de mouvement pour chaque carré rouge
    for i in range(len(lx)):

        x = randint(-1, 1)  # choisit un x aléatoire
        y = randint(-1, 1)  # choisit un y aléatoire

        while (i > 0 and lx[i - 1] == lx[i] + x and ly[i - 1] == ly[i] + y) or (lx[i]+x < 0 or lx[i]+x > taillex - 1 or ly[i]+y < 0 or ly[i]+y > tailley - 1):  # si ils sont sur le joueur
            x = randint(-1, 1)  # choisit un x aléatoire
            y = randint(-1, 1)  # choisit un y aléatoire

        lx[i] = lx[i] + x
        ly[i] = ly[i] + y

        if bonus is not None:
            while lx[i] == bonus[0] and ly[i] == bonus[1]:
                lx[i] = lx[i] + randint(-1, 1)
                ly[i] = ly[i] + randint(-1, 1)

#        if lx[i] < 0: lx[i] = 0
#        if lx[i] > taillex - 1: lx[i] = taillex - 1
#
#        if ly[i] < 0: ly[i] = 0
#        if ly[i] > tailley - 1: ly[i] = tailley - 1


############ Fonction du jeu
def collision(lx, ly, x, y, bonus, phantom):
    final = [False, False]
    for i in range(len(lx)):
        if lx[i] == x and ly[i] == y: final[0] = True
        if bonus is not None and bonus[0] == x and bonus[1] == y: final[1] = True
        if len(phantom) > 0 and phantom[0] == x and phantom[1] == y: final[0] = True
    return final


def jeu(taillex, tailley, params):
    """ taillex et tailley sont les dimensions du jeu souhaitées
    params est un dictionnaire contenant les paramètres de lancement du jeu
    Règles du jeu : Survivre le plus longtemps possible en évitant les carrés rouges"""

    ###### Initialisation du jeu #######
    # global delai, tour, vie, invincible, ennemies, score, bonus

    # Initialisation de x et y les coordonnées du carré perso
    x = ceil(taillex / 2)
    y = ceil(tailley / 2)

    chan_walk = 3  # channel pour que le son de la marche ne se coupe pas
    phantom = []  # initialisation de la variable qui contiendra les coordonnées du phantom

    # création des objets mobiles en début de jeu (combien ?)
    params['ennemies'] = 3 / 100 * (taillex * tailley)

    lx, ly = cree_listes(x, y, taillex, tailley, ceil(params['ennemies']), [], [])

    selectTip(None)

    # Autres initialisation (score, points de vie, ... ?)

    # Cette variable pourra passer à False quand on aura perdu (ou qu'on voudra
    # arrêter le jeu)
    continuer = True
    t = 0  # temps écoulé depuis le délai, ne pas modifier
    t_phantom = 0  # temps écoulé (pour le déplacement du phantom)

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
                    if x != 0:
                        x = x - 1
                        chan_walk = play_walk_sound(chan_walk)
                    pass

                elif event.key == K_RIGHT:
                    # appui sur la touche "droite"
                    if x != taillex - 1:
                        x = x + 1
                        chan_walk = play_walk_sound(chan_walk)
                    pass

                elif event.key == K_UP:
                    # appui sur la touche "haut"
                    if y != 0:
                        y = y - 1
                        chan_walk = play_walk_sound(chan_walk)
                    pass

                elif event.key == K_DOWN:
                    # appui sur la touche "bas"
                    if y != tailley - 1:
                        y = y + 1
                        chan_walk = play_walk_sound(chan_walk)
                    pass

        # Gestion des collisions
        # On récupère l'indice de collision dans i_coll
        col = collision(lx, ly, x, y, params['bonus'], phantom) # renvoie s'il y a eu collision avec un ennemi ou un bonus
        if col[0] and params['invincible'] == 0: # si on est touché et qu'on est pas invincible
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(r'.\assets\sounds\degat.wav'))
            params['vie'] -= 1
            x = ceil(taillex / 2)
            y = ceil(tailley / 2)
            params['invincible'] = 2
            if params['score'] >= 3: params['score'] -= 3
            if params['vie'] == 0:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(r'.\assets\sounds\lose.wav'))
                continuer = False

        if col[1]:
            params['bonus'] = None
            params['vie'] += 1
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(r'.\assets\sounds\bonus.wav'))

        t_phantom = t_phantom + 0.2
        if t_phantom > 1:
            t_phantom = 0
            phantom = gere_phantom(phantom, y, x)

        t = t + 1 / fps  # temps passé
        if t > params['delai']:  # si on a passé le délai, on fait bouger les objets
            # et il peut se passer autre chose (au choix)
            t = 0

            if params['tour'] % 10 == 0 and params['tour'] != 0:  # chaque 10 tours
                lx, ly = cree_listes(x, y, taillex, tailley, ceil(1 / 100 * (taillex * tailley)), lx,
                                     ly)  # On crée de nouveaux ennemies
            if params['tour'] % 20 == 0 and params['tour'] != 0 and params[
                'bonus'] is None:  # permet de faire apparaitre un bonus
                params['bonus'] = [randint(0, taillex - 1), randint(0, tailley - 1)]  # x, y du bonus à créer
                selectTip(r'bonus.png')
            if params['tour'] % 3 == 0:  # on change de tip toutes les 3 secondes
                selectTip(None)
            if params['tour'] % 15 == 0 and params['tour'] != 0: phantom = [x, tailley - 1]

            bouge(taillex, tailley, lx, ly, params['bonus'])  # on bouge les objets

            params['tour'] += 1  # on incrémente le tour
            params['score'] += 1  # à modifier si on veut faire des points

            if params['invincible'] != 0: params['invincible'] -= 1  # si le perso est invincible on le retire

        # Autres événements qui peuvent se passer à chaque nouvelle frame

        vt = False  # variable de test pour savoir si on a touché un ennemi
        if params['invincible'] != 0: vt = True  # si le perso est invincible, on l'affiche en rouge

        texte = {
            'values': [f"Score : {params['score']}", f"Round : {params['tour']}", f"Ennemies : {len(lx)}",
                       f"Life : {params['vie']}"],
            'colors': [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [5, 181, 58]],
            'bg_colors': [[181, 146, 5], [0, 0, 0], [0, 0, 0], [156, 6, 6], [255, 255, 255]],
        }  # texte à afficher

        affiche_jeu(taillex, tailley, lx, ly, phantom, x, y, texte, vt, params['bonus'])  # affichage du jeu

        # permet de ne pas aller plus vite que fps frames par seconde
        clock.tick(fps)

        # Si on sort de la boucle, c'est qu'on a perdu (ou autre). Afficher alors
    # quelque chose ?
    main_menu()


def main_menu():
    """Menu principal du jeu"""

    # Init de la musique
    pygame.mixer.music.stop()
    pygame.mixer.music.load(r'.\assets\sounds\title_music.wav')
    pygame.mixer.music.play(loops=-1)

    title_screen()
    continuer = True
    while continuer:
        # Gestion des évènements
        for event in pygame.event.get():  # Si on quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Si touche appuyée
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    # appui sur la touche "gauche"
                    # le carré perso se déplace à gauche
                    # Lancement du jeu
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound(r'.\assets\sounds\start.wav'))

                    # Init de la musique
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(r'.\assets\sounds\music.wav')
                    pygame.mixer.music.play(loops=-1)

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
                    continuer = False
                    pass

main_menu()