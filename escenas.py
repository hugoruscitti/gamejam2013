#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        pilas.fondos.Fondo("fondo_menu")
        else:
            pilas.fondos.Selva()

        def iniciar_juego():
            pilas.cambiar_escena(Juego())

        def salir_del_juego():
            pilas.terminar()

        if self.mensaje:
            self.title = pilas.actores.Texto(self.mensaje)
            self.title.escala = 2
            self.title.y = 100

        self.menu = pilas.actores.Menu([('Jugar', iniciar_juego),
                                        ('Salir', salir_del_juego)])


pilas.iniciar()
l=Logos()
pilas.cambiar_escena(l)
pilas.ejecutar()
