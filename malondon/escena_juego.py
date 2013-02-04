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


import conf
import actor_viejo
import actor_pareja
import actor_item
import escena_menu
import escena_encuentro



#===============================================================================
# JUEGO
#===============================================================================

class Juego(pilas.escena.Base):

    def _is_valid(self, x, y):
        try:
            return not self.mapa.es_punto_solido(x, y)
        except:
            return False

    def _cerca_de_xy(self, x, y, radio=0):
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

    def _random_xy_lejos_viejo(self):
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

    def _centrar_camara(self, evt):
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
        self.viejo = actor_viejo.Viejo(self.mapa)
        x, y = self._cerca_de_xy(0, 0, max([self.viejo.alto, self.viejo.ancho]))
        self.viejo.x, self.viejo.y = x, y

        # Crear parejas
        self.parejas = []
        self.items = []
        while len(self.parejas) < conf.CANTIDAD_PAREJAS:
            pareja = actor_pareja.Pareja(*self._random_xy_lejos_viejo())
            self.parejas.append(pareja)
            x, y = self._random_xy_lejos_viejo()
            item = actor_item.Item(imagen=pareja.me_elimina_el_item, x=x, y=y)
            self.items.append(item)

        # Agregamos todos los items que faltan mas la pistola
        while len(self.items) < conf.CANTIDAD_ITEMS:
            x, y = self._random_xy_lejos_viejo()
            nombre_imagen = random.choice(conf.PAREJAS_X_ITEMS.values())
            item = actor_item.Item(imagen=nombre_imagen, x=x, y=y)
            self.items.append(item)
        x, y = self._random_xy_lejos_viejo()
        self.items.append(actor_item.Item(imagen=conf.PISTOLA, x=x, y=y))

        # Creamos el timer del juego
        x=(pilas.mundo.motor.ancho_original/2)-50
        y=(pilas.mundo.motor.alto_original/2)-10
        self.timer = pilas.actores.Temporizador(x=x, y=y, fuente="visitor1.ttf")
        self.timer.ajustar(conf.TIEMPO_DE_JUEGO, self.youlose)
        self.timer.iniciar()

        #~ # Contador de parejas rotas
        #~ self.corazon_roto = pilas.actores.Actor("corazon_roto.png",
                                                #~ x=110, y=-210)
        #~ self.corazon_roto.escala = 2
        #~ self.corazon_roto.fijo = True
        #~ self.corazon_roto.z = -20000
        #~ self.contador = pilas.actores.Texto(str(len(self.parejas)),
                                            #~ fuente="visitor1.ttf",
                                            #~ x=147, y=-205)
        #~ self.contador.color = pilas.colores.rojo
        #~ self.contador.fijo = True
        #~ self.contador.z = -20000

        # Vinculamos las colisiones
        self.vincular_colisiones()

        # Eventos globales
        self.actualizar.conectar(self._centrar_camara)
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
            self.viejo.bloquear()
            pilas.mundo.agregar_tarea(2, self.youwin)
        self.musicajuego.continuar()

    def vincular_colisiones(self):
        #self.colisiones.agregar(self.viejo, self.parejas, self.ir_a_encuentro)
        self.colisiones.agregar(self.viejo, self.items, self.encontrar_items)

    def youwin(self):
        self.musicajuego.detener()
        self.camara.x, self.camara.y = 0, 0
        youwin = pilas.escena.Logos(escena_menu.Menu(), pasar_con_teclado=True,
                                    pasar_con_click_de_mouse=True,
                                    pilas_logo=False, mostrar_almenos=4)
        youwin.agregar_logo("youwin.png", timer=219.5, sonido="youwin.mp3")
        pilas.cambiar_escena(youwin)

    def youlose(self):
        self.musicajuego.detener()
        self.camara.x, self.camara.y = 0, 0
        youlose = pilas.escena.Logos(escena_menu.Menu(), pasar_con_teclado=True,
                                     pasar_con_click_de_mouse=True,
                                     pilas_logo=False, mostrar_almenos=6)
        youlose.agregar_logo("youlose.png", timer=6, sonido="perder.wav")
        pilas.cambiar_escena(youlose)

    def encontrar_items(self, viejo, item):
        viejo.agarrar_item(item)
        self.items.remove(item)

    def ir_a_encuentro(self, viejo, act):
        self.musicajuego.pausar()
        pareja = self.parejas[act]
        pilas.almacenar_escena(escena_encuentro.Encuentro(pareja, viejo, self.mapa))



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
