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

import webbrowser

import pilas
import actores

import conf
import escena_juego


#===============================================================================
# MENU PRINCIPAL
#===============================================================================

class Menu(pilas.escena.Base):

    def juego(self):
        self.musicamenu.detener()
        juego = pilas.escena.Logos(escena_juego.Juego(), pilas_logo=False)
        juego.agregar_logo("viejo_historia.png", timer=22,
                           sonido="historia.mp3")
        pilas.cambiar_escena(juego)

    def listen_game_over(self):
        webbrowser.open("http://www.jamendo.com/es/list/a97199/game-over")
        pilas.terminar()

    def about(self):
        self.musicamenu.detener()
        about = pilas.escena.Logos(Menu(), pilas_logo=False)
        about.agregar_logo("about.png", timer=247, sonido="about.mp3")
        pilas.cambiar_escena(about)

    def full_screen(self):
        pilas.mundo.motor.canvas.alternar_pantalla_completa()
        conf.store("pantalla_completa",
                   pilas.mundo.motor.canvas.esta_en_pantalla_completa())

    def salir_del_juego(self):
        pilas.terminar()

    def mostrar_menu(self):
        opciones = [("Let's Break Some Hearts", self.juego),
                    ("About", self.about),
                    ("Full Screen?", self.full_screen),
                    ("Listen: 'Game Over' Malondon OST", self.listen_game_over),
                    ("Exit", self.salir_del_juego)]
        self.menu = pilas.actores.Menu(opciones, fuente="visitor1.ttf")
        self.fondo_menu = pilas.actores.Pizarra(0, -105, 640, 230)
        self.fondo_menu.pintar(pilas.colores.negro)
        self.fondo_menu.transparencia = 25
        self.fondo_menu.z = 300

    # Redefinidos
    #===========================
    def iniciar(self):
        self.musicamenu = pilas.sonidos.cargar("musicamenu.mp3")
        self.musicamenu.reproducir()
        pilas.fondos.Fondo("menu.png")
        pilas.mundo.agregar_tarea(2, self.mostrar_menu)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
