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

import escena_menu


#===============================================================================
# MAIN
#===============================================================================

def main():
    pilas.iniciar(titulo="Malondon")
    logos = pilas.escena.Logos(escena_menu.Menu(), pilas_logo=False)
    logos.agregar_logo("pilasengine.png", sonido="roar.wav")
    logos.agregar_logo("globalgamejam2013.png", timer=2.0)
    logos.agregar_logo("cbagamejam2013.png", timer=2, sonido="corazon.mp3"),
    pilas.cambiar_escena(logos)
    pilas.ejecutar()

if __name__ == "__main__":
    main()
