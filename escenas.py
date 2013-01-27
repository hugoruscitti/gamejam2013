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
CANTIDAD_ITEMS = CANTIDAD_PAREJAS + 10


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

    def __init__(self):
        pilas.escena.Base.__init__(self)
        self.musicamenu = pilas.sonidos.cargar("musicamenu.mp3")


    def juego(self):
        self.musicamenu.detener()
        pilas.cambiar_escena(Juego())

    def about(self):
        pilas.almacenar_escena(About())

    def full_screen(self):
        pilas.mundo.motor.canvas.alternar_pantalla_completa()

    def salir_del_juego(self):
        pilas.terminar()

    def mostrar_menu(self):
        self.menu = pilas.actores.Menu([("Let's Break Some Hearts", self.juego),
                                        ("About", self.about),
                                        ("Full Screen?", self.full_screen),
                                        ("Exit", self.salir_del_juego)],
                                        fuente="visitor1.ttf",
                                        y=-40)

        self.p = pilas.actores.Pizarra(0, -120, 640, 200)
        self.p.pintar(pilas.colores.negro)
        self.p.transparencia = 40
        self.p.z = 300

    def reanudar(self):
        self.musicamenu.continuar()

    def iniciar(self):
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
            try:
                if not self.mapa.es_punto_solido(x, y) \
                and self.viejo.distancia_al_punto(x, y) > 20:
                    valid = True
            except:
                pass
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
        self.musicajuego = pilas.sonidos.cargar("musicajuego.mp3")
        self.musicajuego.reproducir()
        self.mapa = pilas.actores.MapaTiled("mapaprincipal.tmx")
        self.mapa.z = self.mapa.alto + 10
        self.viejo = actores.Viejo(self.mapa)
        self.actualizar.conectar(self.centrar_camara)

        # CREAR PAREJAS
        self.parejas = {}
        self.lista_items = []
        for x in range(CANTIDAD_PAREJAS):
            x, y = self.random_xy()
            pareja = actores.Pareja(x, y)
            self.parejas[pareja.as_actor] = pareja
            x, y = self.random_xy()
            item = actores.Item(imagen=pareja.nombre_imagen_item, x=x, y=y)
            self.lista_items.append(item)

        # agregamos todos los items que faltan mas la pistola
        x, y = self.random_xy()
        self.lista_items.append(actores.Item(imagen=actores.PISTOLA, x=x, y=y))
        while len(self.lista_items) < CANTIDAD_ITEMS:
            x, y = self.random_xy()
            nombre_imagen = random.choice(actores.PAREJAS_X_ITEMS.values())
            item = actores.Item(imagen=nombre_imagen, x=x, y=y)
            self.lista_items.append(item)
        self.vincular_colisiones()

    def reanudar(self):
        self.vincular_colisiones()

    def vincular_colisiones(self):
        pilas.escena_actual().colisiones.agregar(self.viejo,
                                                 self.parejas.keys(),
                                                 self.ir_a_encuentro)
        pilas.escena_actual().colisiones.agregar(self.viejo,
                                                 self.lista_items,
                                                 self.encontrar_items)

    def encontrar_items(self, viejo, item):
        print item

    def ir_a_encuentro(self, viejo, act):
        self.musicajuego.pausar()
        pareja = self.parejas[act]
        pilas.almacenar_escena(Encuentro(pareja, viejo.items, viejo))


#===============================================================================
# ENCUENTRO
#===============================================================================

class Encuentro(pilas.escena.Base):

    def __init__(self, pareja, items, viejo):
        pilas.escena.Base.__init__(self)
        self.pareja = pareja
        self.items = items
        self.viejo = viejo

    def iniciar(self):
        pilas.escena_actual().camara.x = 0
        pilas.escena_actual().camara.y = 0

        # TODO: sonido corazon
        self.sonidocorazon = pilas.sonidos.cargar("musicamenu.mp3")
        self.sonidocorazon.reproducir()

        pilas.fondos.Fondo("fondoencuentro.png")
        fotopareja = pilas.actores.Actor(self.pareja.imagen)
        fotopareja.escala = 0.8
        fotopareja.escala = [1]
        fotopareja.y = 100
        self.barra = actores.Barra(self, self.items)
        for item in self.items:
            pilas.actores.utils.insertar_como_nuevo_actor(item)

    def salir(self):
        self.sonidocorazon.detener()
        self.viejo.y -= 80
        pilas.recuperar_escena()

    def entregar_item(self, item):
        self.pareja.entregar_item(item)
        self.salir()

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
