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

        self.eliminar = False
        self.nombre_imagen_grande = random.choice(conf.PAREJAS_X_ITEMS.keys())
        self.imagen_grande = pilas.imagenes.cargar(self.nombre_imagen_grande)

    def debe_eliminarse(self, item):
        """Informa si el item destruye a la pareja o no."""
        self.eliminar = item.nombre_imagen in (self.nombre_imagen_item,
                                               conf.PISTOLA)
        return self.eliminar

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
