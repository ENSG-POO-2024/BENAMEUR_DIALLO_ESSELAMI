# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:00:49 2024

@author: benoi
"""
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import random
from interface_combat import lancer_interface_combat
import classPokemon as cP
import time
import Test
from Test import liste_pokemon_joueur
from route1_fond_carte import MapGame





if __name__ == '__main__':
    # print(f"Voici votre équipe:{liste_pokemon_joueur}")
    
    app = QApplication(sys.argv)
    game = MapGame()
    game.show()
    sys.exit(app.exec_())