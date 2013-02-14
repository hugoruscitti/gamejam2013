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
            mm_ancho = self.mapa.ancho / 2
            mm_alto = self.mapa.alto / 2
            return not self.mapa.es_punto_solido(x, y) and \
                    abs(x) <= mm_ancho and abs(y) <= mm_alto
        except:
            return False

    def _cerca_de_xy(self, x, y, radio_x, radio_y):
        new_x, new_y = x, y
        inc_x, inc_y = 0, 0
        toca_x = True
        while True:
            for sign_x in (0, 1, -1):
                new_x = new_x + inc_y * sign_x
                for sign_y in (0, 1, -1):
                    new_y = new_y + inc_y * sign_y
                    if self._is_valid(new_x, new_y):
                        return new_x, new_y
            if toca_x and inc_x == 0:
                inc_x = radio_x
                toca_x = False
            elif toca_x:
                inc_x += 1
                toca_x = False
            elif not toca_x and inc_y == 0:
                inc_y = radio_y
                toca_x = True
            elif not toca_x:
                inc_y += 1
                toca_x = True

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

    def _habilitar_items_tirados(self, evt):
        for item in tuple(self.items_tirados):
            if self.viejo.distancia_con(item) > max(item.alto, item.ancho):
                self.items_tirados.remove(item)
                self.items.append(item)

    def _cambiar_color_del_timer_si_falta_poco(self, evt):
        if int(self.timer.texto) <= conf.TIEMPO_DE_JUEGO * 0.10:
            self.timer.color = pilas.colores.rojo

    def _actualizar_parejas(self, evt):
        self.contador.texto = str(len(self.parejas))
        if not self.parejas:
            self.viejo.bloquear()
            pilas.mundo.agregar_tarea(2, self.youwin)
        elif len(self.items) + len(self.items_tirados) == 0:
            self.viejo.bloquear()
            pilas.mundo.agregar_tarea(2, self.youlose)

    def iniciar(self):

        # iniciamos la musica
        self.musicajuego = pilas.musica.cargar("musicajuego.mp3")
        self.musicajuego.reproducir(repetir=True)

        # cargamos el mapa
        self.mapa = pilas.actores.MapaTiled("mapaprincipal.tmx")
        self.mapa.z = self.mapa.alto + 10

        # creamos el protagonista
        self.viejo = actor_viejo.Viejo(self.mapa)
        x, y = self._cerca_de_xy(0, 0, self.viejo.ancho, self.viejo.alto)
        self.viejo.x, self.viejo.y = x, y

        # Crear parejas
        self.parejas = []
        self.items = []
        self.items_tirados = []
        while len(self.parejas) < conf.CANTIDAD_PAREJAS:
            pareja = actor_pareja.Pareja(*self._random_xy_lejos_viejo())
            self.parejas.append(pareja)
            x, y = self._random_xy_lejos_viejo()
            item = actor_item.Item(imagen=pareja.me_elimina_el_item, x=x, y=y)
            self.items.append(item)

        # Agregamos todos los items que faltan mas la pistola
        while len(self.items) < conf.CANTIDAD_ITEM_EXTRAS + conf.CANTIDAD_PAREJAS:
            x, y = self._random_xy_lejos_viejo()
            nombre_imagen = random.choice(conf.PAREJAS_X_ITEMS.values())
            item = actor_item.Item(imagen=nombre_imagen, x=x, y=y)
            self.items.append(item)
        x, y = self._random_xy_lejos_viejo()
        self.items.append(actor_item.Item(imagen=conf.PISTOLA, x=x, y=y))

        # Creamos el timer del juego
        x = (pilas.mundo.motor.ancho_original/2) - 50
        y = (pilas.mundo.motor.alto_original/2) - 10
        self.timer = pilas.actores.Temporizador(x=x, y=y, fuente="visitor1.ttf")
        self.timer.ajustar(conf.TIEMPO_DE_JUEGO, self.youlose)
        self.timer.iniciar()

        # Contador de parejas rotas
        x = -(pilas.mundo.motor.ancho_original/2) + 30
        y = (pilas.mundo.motor.alto_original/2) - 15
        self.corazon_roto = pilas.actores.Actor("corazon_roto.png", x=x, y=y)
        self.corazon_roto.fijo = True
        self.corazon_roto.z = -20000
        self.contador = pilas.actores.Texto(str(len(self.parejas)),
                                            fuente="visitor1.ttf",
                                            x=self.corazon_roto.x + 40,
                                            y=self.corazon_roto.y + 5)
        self.contador.color = pilas.colores.rojo
        self.contador.fijo = True
        self.contador.z = -20000

        # Vinculamos las colisiones
        self.vincular_colisiones()

        # Eventos globales
        self.actualizar.conectar(self._centrar_camara)
        self.actualizar.conectar(self._habilitar_items_tirados)
        self.actualizar.conectar(self._cambiar_color_del_timer_si_falta_poco)
        self.actualizar.conectar(self._actualizar_parejas)
        self.viejo.se_activo_item.conectar(self.se_usa_item)
        pilas.eventos.pulsa_tecla_escape.conectar(self.regresar_al_menu)

    def se_usa_item(self, evt):
        item = self.viejo.traer_item_en_indice(evt.item_idx)
        #item.escala = 0
        item.escala = [1.8, 1], 0.3
        item.x, item.y = self.viejo.x, self.viejo.y
        self.items_tirados.append(item)

    def regresar_al_menu(self, evento):
        self.musicajuego.detener()
        pilas.cambiar_escena(escena_menu.Menu())

    def reanudar(self):
        self.camara.x, self.camara.y = self.viejo.x, self.viejo.y
        for pareja in tuple(self.parejas):
            if pareja.para_eliminar:
                actor_pareja.romper_pareja(pareja)
                self.parejas.remove(pareja)
        self.vincular_colisiones()
        self.musicajuego.continuar()

    def vincular_colisiones(self):
        self.colisiones.agregar(self.viejo, self.parejas, self.ir_a_encuentro)
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
        if viejo.agarrar_item(item):
            self.items.remove(item)

    def ir_a_encuentro(self, viejo, pareja):
        self.musicajuego.pausar()
        encuentro = escena_encuentro.Encuentro(pareja, viejo, self.mapa)
        pilas.almacenar_escena(encuentro)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
