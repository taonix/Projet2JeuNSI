#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:17:46 2021

@author: profinfo
"""

import pygame
from pygame import Rect
import os, random

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("The Escaper")

############## Constantes pygame ################
size = largeur, hauteur = 710, 320
tsprite = 20  # taille d'un sprite en pixels
pos_jeu = 10, 10  # position du jeu par rapport à (0,0)
tip = None  # image de tip

# Le texte
police = pygame.font.Font(r'.\assets\font.ttf', 20)  # police et taille du texte

fps = 30  # vitesse en frames/sec
pygame.key.set_repeat(500, 500)

############ Init du jeu ###################

# Initialisation de l'écran
screen = pygame.display.set_mode(size)

# Init de l'horloge
clock = pygame.time.Clock()

# pour rester appuyé sur une touche
pygame.key.set_repeat(200, 100)

# Config de la musique
pygame.mixer.music.set_volume(0.3)


def selectTip(image_name):  # fonction pour afficher des tips aléatoires
    """ Prend en argument les dimensions de la grille et le nom de l'image à afficher pour les aides"""

    global tip # on utilise la variable globale pour pouvoir la modifier

    tips_folder = r'.\assets\tips' # chemin vers le dossier des tips
    if image_name is None: tip = pygame.image.load(os.path.join(f'{tips_folder}\simple', random.choice(os.listdir(f'{tips_folder}\simple')))) # on choisit un tip aléatoire
    else: tip = pygame.image.load(os.path.join(f'{tips_folder}\special', image_name)) # on choisit un tip précis


def convertit_coord_vers_rect(x, y, h, l):  # convertit les coordonnées en pixels en coordonnées de sprite
    """ prend en argument des coordonnées dans la grille et 
    les dimensions du rectangle, et les
    convertit en coordonnées pygame"""
    xr = x * tsprite + pos_jeu[0]
    yr = y * tsprite + pos_jeu[1]
    return Rect(xr, yr, h, l)


def title_screen():  # fonction pour afficher le texte de fin
    screen.blit(pygame.image.load(r'.\assets\titleScreen.png'), (0, 0))
    # mise à jour de l'affichage
    pygame.display.flip()


invincibile_cli = 0 # variable pour savoir si le joueur est invincibile


def affiche_jeu(taillex, tailley, lx, ly, phantom, x, y, texte, invincibile,
                bonus):  # affiche le jeu en fonction des paramètres reçus
    """ taillex, tailley : dimensions du jeu lx, ly : listes des coord des blocs mobiles x, y : coords du bloc
    "perso" texte : texte à afficher à droite, sous forme de tableau (un dictionnaire à trois catégories (texte,
    couleur, couleur_fond) contenant des tableaux est attendue ) """

    assert len(lx) == len(ly), "Les listes lx et ly doivent être de la même taille !"

    global invincibile_cli # on utilise la variable globale pour pouvoir la modifier

    hjeu = tailley * tsprite # hauteur du jeu
    ljeu = taillex * tsprite # largeur du jeu

    # position du texte, à droite
    xtexte = ljeu + tsprite + pos_jeu[0]
    ytexte = pos_jeu[1] + tsprite

    # Dessin du "fond"
    image = pygame.image.load(r'.\assets\background.png')
    screen.blit(image, (0, 0))

    # affichage de la grille
    screen.blit(pygame.image.load(r'.\assets\bg_game.png'), convertit_coord_vers_rect(0, 0, ljeu, hjeu))

    # Dessin des ennemies
    if invincibile and invincibile_cli == 0:
        couleur_bloc_perso = pygame.image.load(r'.\assets\skins\damaged_steve.png')
        invincibile_cli = 1
    else:
        couleur_bloc_perso = pygame.image.load(r'.\assets\skins\steve.png')
        if invincibile_cli == 1:
            invincibile_cli = 0

    # Dessin des blocs mobiles
    for i in range(len(lx)):
        path = r".\assets\skins\Enemies" # chemin vers les skins des ennemies
        skin = "zombie.png"              # nom du skin par défaut

        if i > 5: skin = "skeleton.png"
        if i > 10: skin = "creeper.png"

        screen.blit(pygame.image.load(path + "\\" + skin), convertit_coord_vers_rect(lx[i], ly[i], tsprite, tsprite)) # on affiche l'énemie

    # Dessin du phantom s'il y en a un
    if len(phantom) > 0: screen.blit(pygame.image.load(r'.\assets\skins\Enemies\phantom.png'), convertit_coord_vers_rect(phantom[0], phantom[1], tsprite, tsprite))

    # Dessin du bloc perso
    screen.blit(couleur_bloc_perso, convertit_coord_vers_rect(x, y, tsprite, tsprite))

    # Dessin du bloc bonus (S'il y en a un)
    if bonus is not None: screen.blit(pygame.image.load(r'.\assets\skins\objects\bonus.png'),
                                      convertit_coord_vers_rect(bonus[0], bonus[1], tsprite, tsprite))

    # Dessin du texte
    for i in range(len(texte['values'])):
        a_afficher = police.render(texte['values'][i], True, texte['colors'][i], texte['bg_colors'][i]) # on prépare le texte à afficher
        screen.blit(a_afficher, (xtexte, ytexte + (i*2) * tsprite)) # on affiche le texte
        if i == len(texte['values']) - 1 and tip is not None: screen.blit(tip, (xtexte, ytexte + (i*3) * tsprite)) # on affiche le tip si il y en a un

    # mise à jour de l'affichage
    pygame.display.flip()
