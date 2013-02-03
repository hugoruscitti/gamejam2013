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

import actor_item


#===============================================================================
# ENCUENTRO
#===============================================================================

class Encuentro(pilas.escena.Base):

    def __init__(self, pareja, viejo, mapa):
        pilas.escena.Base.__init__(self)
        self.pareja = pareja
        self.viejo = viejo
        self.timer = pilas.actores.Temporizador(
            x=(pilas.mundo.motor.ancho_original/2)-50,
            y=(pilas.mundo.motor.alto_original/2)-10,
            fuente="visitor1.ttf",
        )
        self.mapa = mapa
        self.timer.ajustar(10, self.salir)

    def iniciar(self):
        pilas.escena_actual().camara.x = 0
        pilas.escena_actual().camara.y = 0

        self.sonidocorazon = pilas.sonidos.cargar("corazon.mp3")
        self.sonidocorazon.reproducir()

        pilas.fondos.Fondo("fondoencuentro.png")
        fotopareja = pilas.actores.Actor(self.pareja.imagen)
        fotopareja.escala = 0.8
        fotopareja.escala = [1]
        fotopareja.y = 100

        # TODO: el redibujar,  meterlo en una funcion
        pilas.actores.utils.insertar_como_nuevo_actor(self.viejo.barra)
        for item in self.viejo.barra.items:
            pilas.actores.utils.insertar_como_nuevo_actor(item)

        # TODO: el timer no se dibuja
        self.timer.iniciar()

        pilas.eventos.click_de_mouse.conectar(self.hace_click_de_mouse)

    def hace_click_de_mouse(self, evento):
        item = pilas.actores.utils.obtener_actor_en(evento.x, evento.y)

        if isinstance(item, actore_item.Item):
            if self.pareja.se_elimina_con_item(item):
                self.pareja.debe_eliminarse = True
            self.salir()

    def salir(self):
        self.sonidocorazon.detener()
        self.viejo.y = self.viejo.y -50
        while self.mapa.es_punto_solido(self.viejo.x, self.viejo.y):
            self.viejo.y = self.viejo.y -50
        pilas.recuperar_escena()




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
