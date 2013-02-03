#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: GPL 3
# Córdoba Game Jam 2013
# Abrutsky - Bravo - Cabral - Ruscitti - Taira


#===============================================================================
# DOC
#===============================================================================

"""El coso que guarda la configuracion de malondon"""


#===============================================================================
# IMPORTS
#===============================================================================

import json
import os


#===============================================================================
# CONSTANTS
#===============================================================================

MALONDON_CONF_PATH = os.path.join(os.path.expanduser("~"), ".malondon.json")


#===============================================================================
# LOAD OLD CONF
#===============================================================================

_conf = {}
if not os.path.exists(MALONDON_CONF_PATH):
    with open(MALONDON_CONF_PATH, "wb") as fp:
        json.dump({}, fp, ensure_ascii=False)
else:
    with open(MALONDON_CONF_PATH) as fp:
        _conf = json.load(fp)


#===============================================================================
# MAIN
#===============================================================================

def store(name, value):
    _conf[name] = value
    with open(MALONDON_CONF_PATH, "wb") as fp:
        json.dump(_conf, fp, ensure_ascii=False)


def get(name, default=None):
    return _conf.get(name, default)


#===============================================================================
# RELACIONES DE ITEMS CON PAREJAS
#===============================================================================

PAREJAS_X_ITEMS = {"pareja_chetos.png": "choripan.png",
                   "pareja_punks.png": "alianzas.png",
                   "pareja_religiosos.png": "consolador.png",
                   "pareja_viejos.png": "culo.png"}

PISTOLA = "pistola.png"

CANTIDAD_PAREJAS = 20

CANTIDAD_ITEMS = CANTIDAD_PAREJAS + 10

TIEMPO_DE_JUEGO = int((CANTIDAD_PAREJAS / 2.0) * 60)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
