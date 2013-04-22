#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""Los items que se van a agregar en la barra"""


#===============================================================================
# IMPORTS
#===============================================================================

import os

import pilas


#===============================================================================
# ITEM
#===============================================================================

class Item(pilas.actores.Actor):

    def __init__(self, imagen, *args, **kwargs):
        super(Item, self).__init__(imagen=imagen, *args, **kwargs)
        self.nombre_imagen = os.path.basename(self.imagen.ruta_original)
        self.radio_de_colision = max(self.ancho, self.alto) / 2


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
