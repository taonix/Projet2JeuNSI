#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 12:13:34 2022

@author: elinfo
"""
from random import randint


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
        lx[i] = randint(0, taillex)
        ly[i] = randint(0, tailley)
    
    return (lx, ly)

print(cree_listes(10, 10, 5))

