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
# EL VIEJO
#===============================================================================

class Viejo(pilas.actores.Calvo):

    def __init__(self, *args, **kwargs):
        super(Viejo, self).__init__(*args, **kwargs)
        self.imagen = pilas.imagenes.cargar_grilla("viejo.png", 3, 4)
        #self.aprender(habilidades.SeMantieneEnPantalla)

    def actualizar(self):
        topy = self.mapa.imagen.alto() / 2
        topx = self.mapa.imagen.ancho() / 2
        if self.x > topx:
            self.x = topx
        elif self.x < -topx:
            self.x = -topx
        if self.y > topy:
            self.y = topy
        elif self.x < -topx:
            self.y = -topy


#===============================================================================
# PAREJA
#===============================================================================

class Pareja(object):

    def __init__(self):
        self.velocidad = float("0.{}".format(random.randint(7, 9)))
        if random.randint(0, 1):
            self.left = pilas.actores.Animacion(
                pilas.imagenes.cargar_grilla("miembro0.png", 2),
                True, velocidad=self.velocidad
            )
            self.right = pilas.actores.Animacion(
                pilas.imagenes.cargar_grilla("miembro1.png", 2),
                True, velocidad=self.velocidad
            )
        else:
            self.left = pilas.actores.Animacion(
                pilas.imagenes.cargar_grilla("miembro1.png", 2),
                True, velocidad=self.velocidad
            )
            self.right = pilas.actores.Animacion(
                pilas.imagenes.cargar_grilla("miembro0.png", 2),
                True, velocidad=self.velocidad
            )
        self.corazon = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("corazon.png", 2),
            True, velocidad=0.9
        )

        self.right.espejado = True

    def romper_pareja(self):
        self.eliminar()
        self.corazon_roto = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("corazon_roto.png", 2),
            velocidad=0.9, x=self.x, y=self.corazon.y
        )
        self.humo = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("humo.png", 4), x=self.x, y=self.y
        )

    def eliminar(self):
        try:
            self.corazon.eliminar()
            self.left.eliminar()
            self.right.eliminar()
        except:
            pass
        try:
            self.humo.eliminar()
            self.corazon_roto.eliminar()
        except:
            pass

    @property
    def x(self):
        return self.corazon.x

    @x.setter
    def x(self, v):
        self.corazon.x = v
        self.left.x = v - 10
        self.right.x = v + 10

    @property
    def y(self):
        return self.left.y

    @y.setter
    def y(self, v):
        self.corazon.y = v + 24
        self.left.y = v
        self.right.y = v




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
