#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""Aca esta el actor principal del juego: EL VIEJO"""


#===============================================================================
# IMPORTS
#===============================================================================

import random

import pilas

import actor_barra


#===============================================================================
# EL VIEJO
#===============================================================================

class Viejo(pilas.actores.Calvo):

    def __init__(self, *args, **kwargs):
        super(Viejo, self).__init__(*args, **kwargs)
        self._pensar = pilas.imagenes.cargar("pensar.png")
        self._roar = pilas.sonidos.cargar("roar.wav")
        self.imagen = pilas.imagenes.cargar_grilla("viejo.png", 3, 4)
        self.centro = ("centro", "abajo")
        self.barra = actor_barra.Barra()
        pilas.mundo.agregar_tarea(random.randint(5, 10), self.malondiar)

    def bloquear(self):
        try:
            self.dejar_de_malondiar()
        except:
            pass
        self.hacer(pilas.comportamientos.Comportamiento())

    def malondiar(self):
        self.globo = pilas.actores.Actor(self._pensar, x=self.x, y=self.y)
        self.globo.centro = ("centro", self.alto + 25)
        self.globo.aprender(pilas.habilidades.Imitar, self)
        self._roar.reproducir()
        pilas.mundo.agregar_tarea(2.2, self.dejar_de_malondiar)

    def dejar_de_malondiar(self):
        self.globo.eliminar()
        self._roar.detener()
        pilas.mundo.agregar_tarea(random.randint(5, 10), self.malondiar)

    def agarrar_item(self, item):
        self.barra.agregar_item(item)

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
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
