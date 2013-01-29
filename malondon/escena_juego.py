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

import escena_menu
import escena_encuentro


#===============================================================================
# CANTIDAD PAREJAS
#===============================================================================

CANTIDAD_PAREJAS = 20
CANTIDAD_ITEMS = CANTIDAD_PAREJAS + 10
TIEMPO_DE_JUEGO = int((CANTIDAD_PAREJAS / 2.0) * 60)


#===============================================================================
# JUEGO
#===============================================================================

class Juego(pilas.escena.Base):

    def _is_valid(self, x, y):
        try:
            return not self.mapa.es_punto_solido(x, y)
        except:
            return False

    def cerca_de_xy(self, x, y, radio=0):
        inc_x, inc_y = 2, 2
        while not self._is_valid(x, y):
            x += random.randint(radio+1, radio+inc_x)
            y += random.randint(radio+1, radio+inc_y)
            if random.randint(0, 1):
                x = -x
            if random.randint(0, 1):
                y = -y
            if inc_x == inc_y:
                inc_x += 1
            else:
                inc_y += 1
        return x, y

    def random_xy(self):
        valid = False
        while not valid:
            x = (random.randint(0, self.mapa.ancho) / 2) + 10
            y = (random.randint(0, self.mapa.alto) / 2) + 10
            if random.randint(0, 1):
                x = -x
            if random.randint(0, 1):
                y = -y
            valid = self._is_valid(x, y) \
                    and self.viejo.distancia_al_punto(x, y) > 300
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
        # iniciamos la musica
        self.musicajuego = pilas.sonidos.cargar("musicajuego.mp3")
        self.musicajuego.reproducir()

        # cargamos el mapa
        self.mapa = pilas.actores.MapaTiled("mapaprincipal.tmx")
        self.mapa.z = self.mapa.alto + 10

        # creamos el protagonista
        self.viejo = actores.Viejo(self.mapa)
        xy = self.cerca_de_xy(0, 0, max([self.viejo.alto, self.viejo.ancho]))
        self.viejo.x, self.viejo.y = xy

        # Crear parejas
        self.parejas = {}
        self.lista_items = []
        for x in range(CANTIDAD_PAREJAS):
            pareja = actores.Pareja(*self.random_xy())
            self.parejas[pareja.as_actor] = pareja
            x, y = self.random_xy()
            item = actores.Item(imagen=pareja.nombre_imagen_item,
                                fijo=False, x=x, y=y)
            self.lista_items.append(item)

        # Agregamos todos los items que faltan mas la pistola
        x, y = self.random_xy()
        self.lista_items.append(actores.Item(imagen=actores.PISTOLA,
                                             fijo=False, x=x, y=y))
        while len(self.lista_items) < CANTIDAD_ITEMS:
            x, y = self.random_xy()
            nombre_imagen = random.choice(actores.PAREJAS_X_ITEMS.values())
            item = actores.Item(imagen=nombre_imagen, fijo=False, x=x, y=y)
            self.lista_items.append(item)

        # Creamos el timer del juego
        self.timer = pilas.actores.Temporizador(
            x=(pilas.mundo.motor.ancho_original/2)-50,
            y=(pilas.mundo.motor.alto_original/2)-10,
            fuente="visitor1.ttf",
        )
        self.timer.ajustar(TIEMPO_DE_JUEGO, self.youlose)
        self.timer.iniciar()

        # Contador de parejas rotas
        self.corazon_roto = pilas.actores.Actor(
            pilas.imagenes.cargar_grilla("corazon_roto.png", 2),
             x=110, y=-210
        )
        self.corazon_roto.escala = 2
        self.corazon_roto.fijo = True
        self.corazon_roto.z = -20000
        self.contador = pilas.actores.Texto(
            str(len(self.parejas)),
            fuente="visitor1.ttf", x=147, y=-205
        )
        self.contador.color = pilas.colores.rojo
        self.contador.fijo = True
        self.contador.z = -20000

        # Vinculamos las colisiones
        self.vincular_colisiones()

        # Eventos globales
        self.actualizar.conectar(self.centrar_camara)
        pilas.eventos.pulsa_tecla_escape.conectar(self.regresar_al_menu)

    def regresar_al_menu(self, evento):
        self.musicajuego.detener()
        self.camara.x, self.camara_y = 0, 0
        pilas.cambiar_escena(escena_menu.Menu())

    def reanudar(self):
        self.camara.x, self.camara.y = self.viejo.x, self.viejo.y
        for k in self.parejas.keys():
            pareja = self.parejas[k]
            if pareja.debe_eliminarse:
                pareja.romper_pareja()
                self.parejas.pop(k)
        self.vincular_colisiones()
        self.contador.texto = str(len(self.parejas))
        if self.parejas:
            self.musicajuego.detener()
            self.camara.x, self.camara.y = 0, 0
            youwin = pilas.escena.Logos(escena_menu.Menu(), pilas_logo=False)
            youwin.agregar_logo("youwin.png", timer=219.5, sonido="youwin.mp3")
            pilas.cambiar_escena(youwin)
        self.musicajuego.continuar()

    def vincular_colisiones(self):
        pilas.escena_actual().colisiones.agregar(self.viejo,
                                                 self.parejas.keys(),
                                                 self.ir_a_encuentro)
        pilas.escena_actual().colisiones.agregar(self.viejo,
                                                 self.lista_items,
                                                 self.encontrar_items)

    def youlose(self):
        self.musicajuego.detener()
        self.camara.x, self.camara.y = 0, 0
        pilas.cambiar_escena(
            Logos([(6, "youlose.png", "perder.wav")])
        )

    def encontrar_items(self, viejo, item):
        viejo.agarrar_item(item)

    def ir_a_encuentro(self, viejo, act):
        self.musicajuego.pausar()
        pareja = self.parejas[act]
        pilas.almacenar_escena(escena_encuentro.Encuentro(pareja, viejo, self.mapa))



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
