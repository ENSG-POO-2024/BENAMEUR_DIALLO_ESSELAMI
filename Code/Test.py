# -*- coding: utf-8 -*-
"""
Created on Thu May 16 18:29:11 2024

@author: benoi
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap

# Variable globale pour stocker le choix du joueur
choix_pokemon = None

def starter():
    """
    permet de choisir son starter

    Returns
    -------
    str
        nom du starter.

    """
    global choix_pokemon  # Utiliser la variable globale

    base_path = os.path.dirname(__file__)  # Répertoire contenant le script

    app = QApplication(sys.argv)
    dialog = QDialog()
    dialog.setWindowTitle("Choisissez votre Pokémon Starter")
    dialog.setFixedSize(600, 300)  # Ajustez la taille de la fenêtre selon vos besoins

    layout = QHBoxLayout()

    # Chemins relatifs des images
    image1_path = os.path.join(base_path, "asset", "Bulbizarre.png")
    image2_path = os.path.join(base_path, "asset", "Salameche.png")
    image3_path = os.path.join(base_path, "asset", "Carapuce.png")

    # Fonction pour gérer le choix du joueur
    def choisir_pokemon(pokemon):
        global choix_pokemon  # Utiliser la variable globale
        choix_pokemon = pokemon
        print(f"Vous avez choisi {pokemon}!")
        dialog.accept()

    # Ajout des images et des boutons
    for image_path, pokemon in zip([image1_path, image2_path, image3_path], ["Bulbizarre", "Salamèche", "Carapuce"]):
        vbox = QVBoxLayout()
        label = QLabel()
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        vbox.addWidget(label)

        bouton = QPushButton(f"Choisir {pokemon}")
        bouton.clicked.connect(lambda checked, p=pokemon: choisir_pokemon(p))
        vbox.addWidget(bouton)

        layout.addLayout(vbox)

    dialog.setLayout(layout)
    dialog.exec_()

    return choix_pokemon  # Retourner le choix du joueur
choix = starter()
liste_pokemon_joueur = [choix]




