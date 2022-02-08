#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:17:46 2021

@author: profinfo
"""

import pygame
from pygame import Rect
import os,random

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("The Escaper")


############## Constantes pygame ################
size = largeur, hauteur = 700, 320
tsprite = 20 # taille d'un sprite en pixels
couleur_fond = (255, 255, 255) # gris foncé
couleur_contour = (0, 0, 100) # bleu foncé
couleur_bloc_perso = (0,150,100) # bleu-vert
couleur_blocs_mobiles = (150,0,0) #  rouge un peu foncé
couleur_bloc_bonus = (181, 146, 5) # couleur bloc bonus
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

def gradientRect( window, left_colour, right_colour, target_rect ): # fonction pour faire un rectangle avec un gradient
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour,  (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)


def convertit_coord_vers_rect(x,y, h, l): # convertit les coordonnées en pixels en coordonnées de sprite
    """ prend en argument des coordonnées dans la grille et 
    les dimensions du rectangle, et les
    convertit en coordonnées pygame"""
    xr = x*tsprite + pos_jeu[0]
    yr = y*tsprite + pos_jeu[1]
    return Rect(xr,yr,h,l)

def perdu(taillex, tailley): # fonction pour afficher le texte de fin
   screen.fill(couleur_contour)
   gradientRect(screen, (0, 0, 0), (33, 33, 33), screen.get_rect())

   a_afficher = police.render("You lose ! (Space to restart)", True, [255, 255, 255], [0, 0, 0])
   screen.blit(a_afficher, (pos_jeu[0] + (taillex/2),pos_jeu[1] + (tailley/2)))
   
   # mise à jour de l'affichage
   pygame.display.flip()

def accueil(path): # fonction pour afficher le texte d'accueil
    # Dessin du "fond"
    image = pygame.image.load(path)
    screen.blit(image, (0, 0))
    pygame.display.flip()

invincibile_cli = 0
def affiche_jeu(taillex, tailley, lx, ly, x, y, texte, invincibile, bonus): # affiche le jeu en fonction des paramètres reçus
    """ taillex, tailley : dimensions du jeu
    lx, ly : listes des coord des blocs mobiles
    x, y : coords du bloc "perso"
    texte : texte à afficher à droite, sous forme de tableau (une ligne = 1 élt) """
    
    assert len(lx) == len(ly), "Les listes lx et ly doivent être de la même taille !"

    global invincibile_cli

    hjeu = tailley*tsprite
    ljeu = taillex*tsprite
    
    # position du texte, à droite
    xtexte = ljeu+tsprite + pos_jeu[0]
    ytexte = pos_jeu[1] + tsprite
    
    # Dessin du "fond"
    image = pygame.image.load(r'.\assets\background.png')
    screen.blit(image, (0, 0))

    #gradientRect(screen, (0, 0, 0), (33, 33, 33), convertit_coord_vers_rect(0,0,ljeu,hjeu))
    screen.blit(pygame.image.load(r'.\assets\bg_game.png'), convertit_coord_vers_rect(0, 0, ljeu,hjeu))
    
    # Dessin des blocs "figés" de la grille

    if invincibile and invincibile_cli == 0:
        couleur_bloc_perso = pygame.image.load(r'.\assets\skins\damaged_steve.png')
        invincibile_cli = 1
    else:
        couleur_bloc_perso = pygame.image.load(r'.\assets\skins\steve.png')
        if invincibile_cli == 1:
            invincibile_cli = 0

    # Dessin des blocs mobiles
    for i in range(len(lx)):
        path = r".\assets\skins\Enemies"
        skin = "zombie.png"
        if i>5: skin = "skeleton.png"
        if i>10: skin = "creeper.png"
        screen.blit(pygame.image.load(path + "\\" + skin), convertit_coord_vers_rect(lx[i],ly[i], tsprite, tsprite))
        #pygame.draw.rect(screen, couleur_blocs_mobiles, convertit_coord_vers_rect(lx[i],ly[i], tsprite, tsprite))
    # Dessin du bloc perso
    #pygame.draw.rect(screen, couleur_bloc_perso, convertit_coord_vers_rect(x,y, tsprite, tsprite))
    screen.blit(couleur_bloc_perso, convertit_coord_vers_rect(x, y, tsprite, tsprite))
    # Dessin du bloc bonus (S'il y en a un)
    if bonus is not None: screen.blit(pygame.image.load(r'.\assets\skins\objects\bonus.png'), convertit_coord_vers_rect(bonus[0], bonus[1], tsprite, tsprite))
    
#    for i,j in bloc:
#        pygame.draw.rect(screen, couleur_blocs_mobiles, convertit_coord_vers_rect(j,i, tsprite, tsprite))
#    
    # Dessin du texte
    j=0
    for i in range(len(texte['values'])):
        j = j + 1
        a_afficher = police.render(texte['values'][i], True, texte['colors'][i], texte['bg_colors'][i])
        screen.blit(a_afficher, (xtexte,ytexte+(i+j)*tsprite))



    # mise à jour de l'affichage
    pygame.display.flip()
    
