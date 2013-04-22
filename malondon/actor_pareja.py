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

import conf

#===============================================================================
# ENCUENTRO
#===============================================================================

class _Encuentro(pilas.actores.Actor):

    def __init__(self, imagen_a_mostrar):
        super(_Encuentro, self).__init__(imagen="invisible.png")
        self.imagen_a_mostrar = imagen_a_mostrar
        self.fijo = True
        self.z = -5000
        self.escala = 0.8

    def mostrar_en(self, x, y):
        self.x = x; self.y = y
        self.imagen = self.imagen_a_mostrar

    def ocultar(self):
        self.imagen = pilas.imagenes.cargar("invisible.png")


#===============================================================================
# PAREJA
#===============================================================================

class Pareja(pilas.actores.Animacion):

    def __init__(self, x, y):
        super(Pareja, self).__init__(
            pilas.imagenes.cargar_grilla("pareja.png", 2), True, x=x, y=y,
            velocidad=float("0.{}".format(random.randint(7, 9)))
        )
        self.z = y
        self.espejado = bool(random.randint(0, 1))
        self.radio_de_colision = max(self.alto, self.ancho) / 3
        self.centro = ("centro", "abajo")

        self.nombre_imagen_grande = random.choice(conf.PAREJAS_X_ITEMS.keys())

        imagen_grande = pilas.imagenes.cargar(self.nombre_imagen_grande)
        self._encuentro = _Encuentro(imagen_grande)

    def encuentro(self, x, y):
        self._encuentro.mostrar_en(x, y)

    def ocultar_encuentro(self):
        self._encuentro.ocultar()

    def debe_eliminarse(self, item):
        """Informa si el item destruye a la pareja o no."""
        imagen_item = conf.PAREJAS_X_ITEMS[self.nombre_imagen_grande]
        print item.nombre_imagen, imagen_item
        return item.nombre_imagen in (imagen_item, conf.PISTOLA)

    @property
    def me_elimina_el_item(self):
        return conf.PAREJAS_X_ITEMS[self.nombre_imagen_grande]


#===============================================================================
# FUNCTIONS
#===============================================================================

def romper_pareja(pareja):
    pareja.eliminar()
    rota = pilas.actores.Animacion(
            pilas.imagenes.cargar_grilla("pareja_rota.png", 5),
            velocidad=5, x=pareja.x, y=pareja.y
        )
    rota.z = pareja.z
    rota.radio_de_colision = 0


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
