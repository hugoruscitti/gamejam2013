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

import actores


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
        pilas.mundo.agregar_tarea(2, self.siguiente)
        self.pulsa_tecla.conectar(self.siguiente)
        self.click_de_mouse.conectar(self.siguiente)

    def siguiente(self, *args, **kwargs):
        if self._logos_futuros:
            pilas.cambiar_escena(Logos(*self._logos_futuros))
        else:
            pilas.cambiar_escena(Menu())


#===============================================================================
# MENU PRINCIPAL
#===============================================================================

class Menu(pilas.escena.Base):

    def juego(self):
        pilas.cambiar_escena(Juego())

    def about(self):
        pass

    def salir_del_juego(self):
        pilas.terminar()

    def iniciar(self):
        pilas.fondos.Fondo("menu.png")
        self.menu = pilas.actores.Menu([("Let's Break Some Hearts", self.juego),
                                        ("About", self.about),
                                        ('Exit', self.salir_del_juego)])



#===============================================================================
# JUEGO
#===============================================================================

class Juego(pilas.escena.Base):

    def centrar_camara(self):
        self.camara.x = [self.viejo.x]
        self.camara.y = [self.viejo.y]

    def iniciar(self):
        self.mapa = pilas.actores.MapaTiled("mapaprincipal.tmx")
        self.viejo = actores.Viejo(self.mapa)
        pilas.mundo.agregar_tarea_siempre(2, self.centrar_camara)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
