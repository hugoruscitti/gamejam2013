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

import random

import pilas

import actores

#===============================================================================
# CANTIDAD PAREJAS
#===============================================================================

CANTIDAD_PAREJAS = 20


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
# ABOUT
#===============================================================================

class About(pilas.escena.Base):


    def iniciar(self):
        pilas.fondos.Fondo(imagen=pilas.imagenes.cargar_imagen("about.png"))
        self.pulsa_tecla.conectar(self.volver_al_menu)
        self.click_de_mouse.conectar(self.volver_al_menu)

    def volver_al_menu(self, evt):
        pilas.recuperar_escena()


#===============================================================================
# MENU PRINCIPAL
#===============================================================================

class Menu(pilas.escena.Base):

    def juego(self):
        self.musicamenu.detener()
        pilas.cambiar_escena(Juego())

    def about(self):
        pilas.almacenar_escena(About())

    def full_screen(self):
        pass

    def salir_del_juego(self):
        pilas.terminar()


    def mostrar_menu(self):
        self.menu = pilas.actores.Menu([("Let's Break Some Hearts", self.juego),
                                        ("About", self.about),
                                        ("Full Screen?", self.full_screen),
                                        ('Exit', self.salir_del_juego)])

    def iniciar(self):
        self.musicamenu = pilas.sonidos.cargar("musicamenu.mp3")
        self.musicamenu.reproducir()
        pilas.fondos.Fondo("menu.png")
        pilas.mundo.agregar_tarea(1.5, self.mostrar_menu)




#===============================================================================
# JUEGO
#===============================================================================

class Juego(pilas.escena.Base):

    def random_xy(self):
        valid = False
        while not valid:
            x = (random.randint(0, self.mapa.ancho) / 2) + 10
            y = (random.randint(0, self.mapa.alto) / 2) + 10
            if random.randint(0, 1):
                x = -x
            if random.randint(0, 1):
                y = -y
            valid = not self.mapa.es_punto_solido(x, y)
        return x, y

    def centrar_camara(self, evt):
        mm_ancho = self.mapa.ancho / 2
        mm_alto = self.mapa.alto / 2
        mp_ancho = pilas.mundo.motor.ancho_original / 2
        mp_alto = pilas.mundo.motor.alto_original / 2
        if abs(self.viejo.x) < mm_ancho - mp_ancho:
            self.camara.x = [self.viejo.x]
        if abs(self.viejo.y) < mm_alto - mp_alto:
            self.camara.y = [self.viejo.y]

    def iniciar(self):
        try:
            self.musicajuego = pilas.sonidos.cargar("musicajuego.mp3")
            self.musicajuego.reproducir()
        except:
            pass
        self.mapa = pilas.actores.MapaTiled("mapaprincipal.tmx")
        self.viejo = actores.Viejo(self.mapa)
        self.actualizar.conectar(self.centrar_camara)

        # CREAR PAREJAS
        for x in range(CANTIDAD_PAREJAS):
            x, y = self.random_xy()
            pareja = actores.Pareja(x, y)


#===============================================================================
# ENCUENTRO
#===============================================================================
class Barra():

    def __init__(self, items):
        for i,item in enumerate(items):
            actor = pilas.actores.Actor(item)
            actor.x = -205 + (i * 50)
            actor.y = -195

class Encuentro(pilas.escena.Base):

    def __init__(self, pareja="parejatest.jpg", items=["itemtest.png", "itemtest.png", "itemtest.png"]):
        pilas.escena.Base.__init__(self)
        self.pareja = pareja
        self.items = items

    def iniciar(self):
        try:
            # bajar volumen musicajuego: self.musicajuego.bajarVolumen(10%)
            # reproducir latido corazon

            pass
        except:
            pass

        pilas.fondos.Fondo("fondoencuentro.png")
        pareja = pilas.actores.Actor(self.pareja)
        pareja.escala = 0.8
        pareja.escala = [1]
        pareja.y = 100
        self.barra = Barra(self.items)

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
