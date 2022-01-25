#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:17:46 2021

@author: profinfo
"""

import pygame
from pygame import Rect

pygame.init()


############## Constantes pygame ################
size = largeur, hauteur = 800, 600
tsprite = 20 # taille d'un sprite en pixels
couleur_fond = (10, 10, 10) # gris foncé
couleur_contour = (0, 0, 100) # bleu foncé
couleur_bloc_perso = (0,150,100) # bleu-vert
couleur_blocs_mobiles = (150,0,0) #  rouge un peu foncé
pos_jeu = 10,10 # position du jeu par rapport à (0,0)

# Le texte
couleur_texte=255, 255, 255 # noir
police = pygame.font.Font(None, 38) # police et taille du texte


fps = 30 # vitesse en frames/sec
pygame.key.set_repeat(500, 500)

############ Init du jeu ###################

# Initialisation de l'écran
screen = pygame.display.set_mode(size)

# Init de l'horloge
clock=pygame.time.Clock()

# pour rester appuyé sur une touche
pygame.key.set_repeat(200,100)

def convertit_coord_vers_rect(x,y, h, l):
    """ prend en argument des coordonnées dans la grille et 
    les dimensions du rectangle, et les
    convertit en coordonnées pygame"""
    xr = x*tsprite + pos_jeu[0]
    yr = y*tsprite + pos_jeu[1]
    return Rect(xr,yr,h,l)



def affiche_jeu(taillex, tailley, lx, ly, x, y, texte):
    """ taillex, tailley : dimensions du jeu
    lx, ly : listes des coord des blocs mobiles
    x, y : coords du bloc "perso"
    texte : texte à afficher à droite, sous forme de tableau (une ligne = 1 élt) """
    
    assert len(lx) == len(ly), "Les listes lx et ly doivent être de la même taille !"
    
    hjeu = tailley*tsprite
    ljeu = taillex*tsprite
    
    # position du texte, à droite
    xtexte = ljeu+tsprite + pos_jeu[0]
    ytexte = pos_jeu[1] + tsprite
    
    # Dessin du "fond"
    screen.fill(couleur_contour)
    pygame.draw.rect(screen, couleur_fond, convertit_coord_vers_rect(0,0,ljeu,hjeu))
    
    # Dessin des blocs "figés" de la grille
    
    # Dessin des blocs mobiles
    for i in range(len(lx)):
        pygame.draw.rect(screen, couleur_blocs_mobiles, convertit_coord_vers_rect(lx[i],ly[i], tsprite, tsprite))
    # Dessin du bloc perso
    pygame.draw.rect(screen, couleur_bloc_perso, convertit_coord_vers_rect(x,y, tsprite, tsprite))
    
#    for i,j in bloc:
#        pygame.draw.rect(screen, couleur_blocs_mobiles, convertit_coord_vers_rect(j,i, tsprite, tsprite))
#    
    # Dessin du texte
    for i in range(len(texte)):
        a_afficher = police.render(texte[i], 0, couleur_texte)    
        screen.blit(a_afficher, (xtexte,ytexte+i*tsprite))
    
    # mise à jour de l'affichage
    pygame.display.flip()
