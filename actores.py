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
        self.x = self.x - 50
        self.radio_de_colision = 40
        self.imagen = pilas.imagenes.cargar_grilla("viejo.png", 3, 4)
        self._pensar = pilas.imagenes.cargar("pensar.png")
        pilas.mundo.agregar_tarea(random.randint(5, 10), self.malondiar)

    def malondiar(self):
        self.globo = pilas.actores.Actor(self._pensar)
        self.globo.aprender(pilas.habilidades.Imitar, self)
        pilas.mundo.agregar_tarea(2, self.dejar_de_malondiar)

    def dejar_de_malondiar(self):
        self.globo.eliminar()
        pilas.mundo.agregar_tarea(random.randint(5, 10), self.malondiar)

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
        self.z = self.y


#===============================================================================
# PAREJA
#===============================================================================

class Pareja(object):

    FOTOS = ["pareja_chetos.png",
             "pareja_punks.png",
             "pareja_religiosos.png"]

    def __init__(self, x, y):
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
        self.imagen = pilas.imagenes.cargar(random.choice(self.FOTOS))
        self.right.espejado = True
        self.right.centro = ("centro", "abajo")
        self.left.centro = ("centro", "abajo")
        self.corazon.centro = ("centro", "abajo")
        self.x, self.y, self.z = x, y, 10
        self.radio_de_colision = 70

    def romper_pareja(self):
        self.eliminar()
        self.corazon_roto = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("corazon_roto.png", 2), velocidad=0.9
        )
        self.corazon_roto.centro = ("centro", "abajo")
        self.corazon_roto.x, self.corazon_roto.y = self.x, self.corazon.y
        self.humo = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("humo.png", 4)
        )
        self.humo.x, self.humo.y = self.x, self.y
        self.humo.centro = ("centro", "abajo")

    def entregar_item(self, item):
        # TODO: verificar si el item destruye o no
        self.romper_pareja()
        
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
        self.corazon.y = v + 35
        self.left.y = v
        self.right.y = v
        self.left.z = v
        self.right.z = v



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
