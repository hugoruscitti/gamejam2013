#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""El menu principal del juego"""


#===============================================================================
# IMPORTS
#===============================================================================

import pilas
import actores


#===============================================================================
# MENU PRINCIPAL
#===============================================================================

class Menu(pilas.escena.Base):

    def juego(self):
        #self.musicamenu.detener()
        pass
        #~ pilas.cambiar_escena(Logos([(22,"viejo_historia.png",
                                    #~ "historia.mp3")], Juego))

    def about(self):
        self.musicamenu.detener()
        about = pilas.escena.Logos(self, pilas_logo=False)
        about.agregar_logo("about.png", timer=247, sonido="about.mp3")
        pilas.cambiar_escena(about)

    def full_screen(self):
        pilas.mundo.motor.canvas.alternar_pantalla_completa()

    def salir_del_juego(self):
        pilas.terminar()

    def mostrar_menu(self):
        opciones = {"Let's Break Some Hearts": self.juego,
                    "About": self.about,
                    "Full Screen?": self.full_screen,
                    "Exit": self.salir_del_juego}
        self.menu = pilas.actores.Menu(opciones.items(),
                                       fuente="visitor1.ttf", y=-40)
        self.fondo_menu = pilas.actores.Pizarra(0, -120, 640, 200)
        self.fondo_menu.pintar(pilas.colores.negro)
        self.fondo_menu.transparencia = 40
        self.fondo_menu.z = 300

    # Redefinidos
    #===========================
    def iniciar(self):
        self.musicamenu = pilas.sonidos.cargar("musicamenu.mp3")
        self.musicamenu.reproducir()
        pilas.fondos.Fondo("menu.png")
        pilas.mundo.agregar_tarea(1.5, self.mostrar_menu)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
