#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""Personajes"""


#===============================================================================
# IMPORTS
#===============================================================================

import random

import pilas


#===============================================================================
# El Viejo
#===============================================================================

class Viejo(pilas.actores.Calvo):

    def __init__(self, *args, **kwargs):
        super(Viejo, self).__init__(*args, **kwargs)
        self.imagen = pilas.imagenes.cargar_grilla("viejo.png", 3, 4)


#===============================================================================
# PAREJA
#===============================================================================

class Pareja(object):

    MIEMBROS = ["miembro{}.png".format(idx) for idx in range(6)]

    def __init__(self):
        left = random.choice(Pareja.MIEMBROS)
        right = random.choice(Pareja.MIEMBROS)
        while right == left:
            right = random.choice(Pareja.MIEMBROS)
        self.corazon = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("corazon.png", 2), True
        )
        self.left = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla(left, 2), True
        )
        self.right = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla(right, 2), True
        )
        self.right.espejado = True

    def romper_pareja(self):
        self.corazon.imagen = pilas.imagenes.cargar_imagen("corazon_roto.png")
        self.left.imagen = (
            pilas.imagenes.cargar_grilla("humo.png", 4)
        )
        self.right.imagen = (
            pilas.imagenes.cargar_grilla("humo.png", 4)
        )

    def eliminar(self):
        self.corazon.eliminar()
        self.left.eliminar()
        self.right.eliminar()

    @property
    def x(self):
        self.corazon.x = x
        self.left.x = x - 12
        self.right.x = x + 12

    @property
    def y(self):
        self.corazon.y = y + 24
        self.left.y = y
        self.right.y = y




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
