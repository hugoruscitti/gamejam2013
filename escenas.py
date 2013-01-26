#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""Escenas para el juego"""


#===============================================================================
# IMPORTS
#===============================================================================

import pilas


#===============================================================================
# LOGOS INICIALES
#===============================================================================

class Logos(pilas.escena.Normal):

    def __init__(self, *logos):
        super(Logos, self).__init__()
        if logos:
            self._logos_futuros = list(logos)
        else:
            self._logos_futuros = ["pilasengine.png",
                                   "cbagamejam2013.png",
                                   "globalgamejam2013.png"]
        self._logo = pilas.imagenes.cargar_imagen(self._logos_futuros.pop(0))

    def iniciar(self):
        pilas.fondos.Fondo(imagen=self._logo)
        if self._logos_futuros:
            pilas.mundo.agregar_tarea(2, pilas.cambiar_escena,
                                      Logos(*self._logos_futuros))
        else:
            pilas.mundo.agregar_tarea(2, pilas.cambiar_escena, Menu())


#===============================================================================
# MENU PRINCIPAL
#===============================================================================

class Menu(pilas.escena.Base):

    def iniciar(self):
        pilas.fondos.Fondo("menu.png")

        def iniciar_juego():
            pilas.cambiar_escena(Juego())

        def salir_del_juego():
            pilas.terminar()

        self.menu = pilas.actores.Menu([("Let's Break Some Hearts", iniciar_juego),
                                        ('Exit', salir_del_juego)])



#===============================================================================
# JUEGO
#===============================================================================

class Juego(pilas.escena.Base):

    def iniciar(self):
        mapa = pilas.actores.Mapa()
        viejo = pilas.imagenes.cargar_grilla("viejo.png", 3, 4)
        c = pilas.actores.Calvo(mapa)
        c.imagen = viejo


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
