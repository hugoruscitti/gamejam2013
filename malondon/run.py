#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""Lanzador del juego Malondon"""


#===============================================================================
# IMPORTS
#===============================================================================

import pilas
import conf

import escena_menu
import escena_juego


#===============================================================================
# MAIN
#===============================================================================

def main():
    pilas.iniciar(titulo="Malondon",
                  pantalla_completa=conf.get("pantalla_completa", False))
    logos = pilas.escena.Logos(escena_menu.Menu(), pilas_logo=False)
    logos.agregar_logo("pilasengine.png", sonido="roar.wav")
    logos.agregar_logo("globalgamejam2013.png")
    logos.agregar_logo("cbagamejam2013.png", sonido="corazon_corto.mp3"),
    logos.agregar_logo("gpl3.png")
    pilas.cambiar_escena(logos)
    pilas.ejecutar()

if __name__ == "__main__":
    main()
