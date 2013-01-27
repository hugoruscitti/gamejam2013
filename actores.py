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

import escenas

#===============================================================================
# CONF
#===============================================================================


PAREJAS_X_ITEMS = {"pareja_chetos.png": "choripan.png",
                   "pareja_punks.png": "alianzas.png",
                   "pareja_religiosos.png": "consolador.png",
                   "pareja_viejos.png": "culo.png"}

PISTOLA = "pistola.png"


#===============================================================================
# EL VIEJO
#===============================================================================

class Viejo(pilas.actores.Calvo):

    def __init__(self, *args, **kwargs):
        super(Viejo, self).__init__(*args, **kwargs)
        self.x = self.x - 50
        self.imagen = pilas.imagenes.cargar_grilla("viejo.png", 3, 4)
        self._pensar = pilas.imagenes.cargar("pensar.png")
        self.barra = Barra()
        pilas.mundo.agregar_tarea(random.randint(5, 10), self.malondiar)
        self.centro = ("centro", "abajo")

    def malondiar(self):
        self.globo = pilas.actores.Actor(self._pensar, x=self.x, y=self.y)
        self.globo.centro = ("centro", self.alto + 25)
        self.globo.aprender(pilas.habilidades.Imitar, self)
        pilas.mundo.agregar_tarea(2, self.dejar_de_malondiar)

    def dejar_de_malondiar(self):
        self.globo.eliminar()
        pilas.mundo.agregar_tarea(random.randint(5, 10), self.malondiar)

    def agarrar_item(self, item):
        self.barra.insertar_item(item)

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
        self._actor = pilas.actores.Actor(imagen="invisible.png")
        self.debe_eliminarse = False

        self.nombre_imagen = random.choice(PAREJAS_X_ITEMS.keys())
        self.imagen = pilas.imagenes.cargar(self.nombre_imagen)
        self.right.espejado = True
        self.right.centro = ("centro", "abajo")
        self.left.centro = ("centro", "abajo")
        self.corazon.centro = ("centro", "abajo")
        self._actor.centro = ("centro", "abajo")
        self._actor.radio_de_colision = 25
        self.x, self.y = x, y

    def romper_pareja(self):
        self.radio_de_colision = 0
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
        if item.nombre_imagen in (self.nombre_imagen_item, PISTOLA):
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
        return self._actor.x

    @x.setter
    def x(self, v):
        self.corazon.x = v
        self._actor.x = v
        self.left.x = v - 10
        self.right.x = v + 10

    @property
    def y(self):
        return self._actor.y

    @y.setter
    def y(self, v):
        self.corazon.y = v + 35
        self._actor.y = v + 20
        self.left.y = v
        self.right.y = v
        self.left.z = v
        self.right.z = v
        self._actor.z = v

    @property
    def as_actor(self):
        return self._actor

    @property
    def z(self):
        return self._actor.z

    @property
    def nombre_imagen_item(self):
        return PAREJAS_X_ITEMS[self.nombre_imagen]


#===============================================================================
# ITEM
#===============================================================================

class Item(pilas.actores.Actor):

    def __init__(self, imagen, fijo, *args, **kwargs):
        super(Item, self).__init__(imagen=imagen, *args, **kwargs)
        self.nombre_imagen = imagen
        self.fijo = fijo


#===============================================================================
# Barra de items
#===============================================================================

class Barra(pilas.actores.Actor):

    def __init__(self, items=[]):
        # TODO: unhack la posicion de la barra
        pilas.actores.Actor.__init__(self, "barra.png", x=-110, y=-210)
        self.items = items
        for idx, item in enumerate(items):
            item.x = -280 + (idx * 50)
            item.y = -210
            pilas.actores.utils.insertar_como_nuevo_actor(item)
            item.z = -20000

        pilas.eventos.click_de_mouse.conectar(self.click_de_mouse)
        self.fijo = True
        self.z = -10000

    def click_de_mouse(self, evento):
        item = pilas.actores.utils.obtener_actor_en(evento.x, evento.y)
        if isinstance(item, Item) and isinstance(pilas.escena_actual(), Encuentro):
            #self.encuentro.entregar_item(item)
            # TODO: que la pareja recibe el item
            pass

    def insertar_item(self, item):
        if len(self.items) < 8:
            self.items.append(item)
            item.x = -280 -50 + len(self.items) * 50
            item.y = -210
            item.z = -20000
            #pilas.actores.utils.insertar_como_nuevo_actor(item)
            item.fijo = True
        else:
            print "ERROR: no se pueden tomar mas de 8 items."

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
