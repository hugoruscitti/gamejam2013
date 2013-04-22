#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""La barra que contiene los items"""


#===============================================================================
# IMPORTS
#===============================================================================


import pilas

import actor_item


#===============================================================================
# Barra de items
#===============================================================================

class Barra(pilas.actores.Actor):

    def __init__(self, items=[], fijo=True, x=0, y=-210, capacidad=8):
        pilas.actores.Actor.__init__(self, imagen="barra.png", x=x, y=y)
        self.z = -10000
        self.fijo = True
        self.capacidad = capacidad
        self.se_activo_item = pilas.evento.Evento("se_activo_item")
        self._contenedor = []
        self._numeros = []
        pilas.escena_actual().pulsa_tecla.conectar(self._pulsa_tecla)

    def __len__(self):
        return len(self._contenedor)

    def __iter__(self):
        return iter(self._contenedor)

    def _pulsa_tecla(self, evt):
        es_repeticion = evt.es_repeticion
        texto = unicode(evt.texto)
        if not es_repeticion and texto.isdigit():
            idx = int(texto) - 1
            if 0 <= idx < self.capacidad and idx < len(self._contenedor):
                self.se_activo_item.emitir(item_idx=idx, item_nro=idx+1)

    def agregar_item(self, item):
        if len(self._contenedor) < self.capacidad:
            icono = item.imagen.ruta_original
            contenido = pilas.actores.Actor(imagen=icono, y=self.y)
            contenido.z = self.z - 1
            contenido.fijo = True
            self._contenedor.append(contenido)
            item.eliminar()
            item.destruir()
            self.actualizar()
            return True
        return False

    def quitar_item(self, idx):
        contenido = self._contenedor.pop(idx)
        item = actor_item.Item(contenido.imagen)
        contenido.eliminar()
        return item

    def actualizar(self):
        while self._numeros:
            numero = self._numeros.pop()
            numero.eliminar()
        for idx, contenido in enumerate(self._contenedor):
            if idx == 0:
                contenido.x = self.x - (self.ancho / 2) + 24
            else:
                contenido.x = self._contenedor[idx-1].x + 50
            numero = pilas.actores.Texto(str(idx+1),
                             fuente="visitor1.ttf", x=contenido.x,
                             y=contenido.y-5)
            numero.color = pilas.colores.negro
            numero.z = contenido.z - 1
            self._numeros.append(numero)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
