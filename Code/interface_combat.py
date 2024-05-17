# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:08:42 2024

@author: benoi
"""


import random
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QProgressBar, QVBoxLayout, QMessageBox, QGridLayout
from PyQt5.QtCore import QTimer
import classPokemon as cP
import time
from Test import liste_pokemon_joueur


class CombatWindow(QDialog):
    def __init__(self, nom_joueur, nom_adversaire, hp_joueur, hp_adversaire):
        super().__init__()
        self.setWindowTitle("Combat")
        self.setFixedSize(800, 800)  # Définition de la taille de la fenêtre
        self.nom_adversaire = nom_adversaire
        self.nom_joueur = nom_joueur

        # Définition des attributs pour les points de vie du joueur et de l'adversaire
        self.hp_joueur = hp_joueur
        self.hp_joueur_max = hp_joueur
        self.hp_adversaire = hp_adversaire
        self.hp_adversaire_max = hp_adversaire
        
        # Initialiser la liste des Pokémon vivants
        self.init_pokemon_vivant()

        # Zones de texte pour les noms des Pokémon
        self.label_nom_joueur = QLabel("Nom Joueur:")
        self.zone_texte_nom_joueur = QLineEdit(nom_joueur)
        self.zone_texte_nom_joueur.setReadOnly(True)  # Rendre la zone de texte non modifiable

        self.label_nom_adversaire = QLabel("Nom Adversaire:")
        self.zone_texte_nom_adversaire = QLineEdit(nom_adversaire)
        self.zone_texte_nom_adversaire.setReadOnly(True)  # Rendre la zone de texte non modifiable

        # Barres de vie
        self.barre_vie_joueur = QProgressBar()
        self.barre_vie_joueur.setRange(0, hp_joueur)
        self.barre_vie_joueur.setValue(hp_joueur)  # Valeur initiale = HP max
        self.barre_vie_joueur.setFormat(f"Vie Joueur: {hp_joueur}/{self.hp_joueur_max}")

        self.barre_vie_adversaire = QProgressBar()
        self.barre_vie_adversaire.setRange(0, hp_adversaire)
        self.barre_vie_adversaire.setValue(hp_adversaire)  # Valeur initiale = HP max
        self.barre_vie_adversaire.setFormat(f"Vie Adversaire: {hp_adversaire}/{self.hp_adversaire_max}")

        # Emplacements d'images
        self.image_joueur = QLabel("Image Joueur")
        self.image_adversaire = QLabel("Image Adversaire")

        # Boutons
        self.bouton_attaquer = QPushButton("Attaquer")
        self.bouton_fuir = QPushButton("Fuir")
        self.bouton_changer_pokemon = QPushButton("Changer de Pokemon")

        # Layout vertical pour organiser les éléments
        self.combat_layout = QVBoxLayout()  # Renommer la variable layout
        self.combat_layout.addWidget(self.label_nom_joueur)
        self.combat_layout.addWidget(self.zone_texte_nom_joueur)
        self.combat_layout.addWidget(self.label_nom_adversaire)
        self.combat_layout.addWidget(self.zone_texte_nom_adversaire)
        self.combat_layout.addWidget(self.barre_vie_joueur)
        self.combat_layout.addWidget(self.barre_vie_adversaire)
        self.combat_layout.addWidget(self.image_joueur)
        self.combat_layout.addWidget(self.image_adversaire)
        self.combat_layout.addWidget(self.bouton_attaquer)
        self.combat_layout.addWidget(self.bouton_fuir)
        self.combat_layout.addWidget(self.bouton_changer_pokemon)

        self.setLayout(self.combat_layout)

        # Connexion des boutons à leurs actions
        self.bouton_attaquer.clicked.connect(self.attaquer)
        self.bouton_fuir.clicked.connect(self.fuir)
        self.bouton_changer_pokemon.clicked.connect(self.changer_pokemon)

        # Création du timer pour gérer l'animation des pertes de points de vie du joueur
        self.timer = QTimer()
        
    def changer_pokemon(self):
        changer_pokemon_dialog = ChangerPokemonDialog(liste_pokemon_joueur)
        if changer_pokemon_dialog.exec_() == QDialog.Accepted:
            nouveau_pokemon = changer_pokemon_dialog.selection
            self.permuter_pokemon(nouveau_pokemon)

    def permuter_pokemon(self, nom_pokemon):
        index_nouveau_pokemon = next(i for i, p in enumerate(liste_pokemon_joueur) if p == nom_pokemon)
        liste_pokemon_joueur[0], liste_pokemon_joueur[index_nouveau_pokemon] = liste_pokemon_joueur[index_nouveau_pokemon], liste_pokemon_joueur[0]
        self.pokemon_actuel = liste_pokemon_joueur[0]
        self.nom_joueur = self.pokemon_actuel
        hp_joueur = cP.pokedex[self.nom_joueur].hp
        self.hp_joueur = hp_joueur
        self.hp_joueur_max = hp_joueur
        self.mettre_a_jour_interface()
        time.sleep(1)
        self.attaque_adversaire()
        self.fin_de_combat()

    def mettre_a_jour_interface(self):
        self.zone_texte_nom_joueur.setText(cP.pokedex[self.nom_joueur].name)
        self.barre_vie_joueur.setRange(0, cP.pokedex[self.nom_joueur].hp)
        self.barre_vie_joueur.setValue(cP.pokedex[self.nom_joueur].hp)
        self.barre_vie_joueur.setFormat(f"Vie Joueur: {cP.pokedex[self.nom_joueur].hp}/{cP.pokedex[self.nom_joueur].hp}")
        # self.mettre_a_jour_image(self.pokemon_actuel.image)

    # def mettre_a_jour_image(self, image_filename):
    #     base_path = os.path.dirname(__file__)
    #     image_path = os.path.join(base_path, "asset", image_filename)
    #     pixmap = QPixmap(image_path)
    #     self.image_joueur.setPixmap(pixmap)
    

    def attaquer(self):

        # Ajouter deux cases d'attaque
        self.case_attaque_1 = QPushButton(
            cP.pokedex[self.zone_texte_nom_joueur.text()].moves[0].name)
        self.case_attaque_2 = QPushButton(
            cP.pokedex[self.zone_texte_nom_joueur.text()].moves[1].name)

        # Ajouter les deux cases d'attaque au layout
        self.combat_layout.addWidget(self.case_attaque_1)
        self.combat_layout.addWidget(self.case_attaque_2)

        # Connecter les boutons d'attaque à leurs actions
        self.case_attaque_1.clicked.connect(self.attaquer_1)
        self.case_attaque_2.clicked.connect(self.attaquer_2)

    def attaquer_1(self):
        if cP.pokedex[self.zone_texte_nom_joueur.text()].speed > cP.pokedex[self.zone_texte_nom_adversaire.text()].speed:
            self.attaque_joueur(1)
            if not self.fin_de_combat():
                time.sleep(0.5)
                self.attaque_adversaire()
                self.fin_de_combat()
        elif cP.pokedex[self.zone_texte_nom_joueur.text()].speed < cP.pokedex[self.zone_texte_nom_adversaire.text()].speed:
            self.attaque_adversaire()
            if not self.fin_de_combat():
                time.sleep(0.5)
                self.attaque_joueur(1)
                self.fin_de_combat()
        else:
            result = random.randint(0, 1)
            if result == 0:
                self.attaque_adversaire()
                if not self.fin_de_combat():
                    time.sleep(0.5)
                    self.attaque_joueur(1)
                    self.fin_de_combat()  # L'adversaire attaque en premier
            else:
                self.attaque_joueur(1)
                if not self.fin_de_combat():
                    time.sleep(0.5)
                    self.attaque_adversaire()
                    self.fin_de_combat()  # Le joueur attaque en premier

    def attaquer_2(self):
        if cP.pokedex[self.zone_texte_nom_joueur.text()].speed > cP.pokedex[self.zone_texte_nom_adversaire.text()].speed:
            self.attaque_joueur(2)
            if not self.fin_de_combat():
                time.sleep(0.5)
                self.attaque_adversaire()
                self.fin_de_combat()
        elif cP.pokedex[self.zone_texte_nom_joueur.text()].speed < cP.pokedex[self.zone_texte_nom_adversaire.text()].speed:
            self.attaque_adversaire()
            if not self.fin_de_combat():
                time.sleep(0.5)
                self.attaque_joueur(2)
                self.fin_de_combat()
        else:
            result = random.randint(0, 1)
            if result == 0:
                self.attaque_adversaire()
                if not self.fin_de_combat():
                    time.sleep(0.5)
                    self.attaque_joueur(2)
                    self.fin_de_combat()  # L'adversaire attaque en premier
            else:
                self.attaque_joueur(2)
                if not self.fin_de_combat():
                    time.sleep(0.5)
                    self.attaque_adversaire()
                    self.fin_de_combat()  # Le joueur attaque en premier

    def attaque_joueur(self, nb_atk):
        # Réduire les points de vie de l'adversaire
        if nb_atk == 1:
            print(
                f"{self.nom_joueur} utilise {cP.pokedex[self.nom_joueur].moves[0].name}!")
            self.hp_adversaire -= cP.calcul_damage(
                self.nom_adversaire, self.nom_joueur, cP.pokedex[self.nom_joueur].moves[0].name)
            if self.hp_adversaire < 0:
                self.hp_adversaire = 0
            self.barre_vie_adversaire.setValue(self.hp_adversaire)
            self.barre_vie_adversaire.setFormat(
                f"Vie Adversaire: {self.hp_adversaire}/{self.hp_adversaire_max}")

        elif nb_atk == 2:
            print(
                f"{self.nom_joueur} utilise {cP.pokedex[self.nom_joueur].moves[1].name}!")
            self.hp_adversaire -= cP.calcul_damage(
                self.nom_adversaire, self.nom_joueur, cP.pokedex[self.nom_joueur].moves[1].name)
            if self.hp_adversaire < 0:
                self.hp_adversaire = 0
            self.barre_vie_adversaire.setValue(self.hp_adversaire)
            self.barre_vie_adversaire.setFormat(
                f"Vie Adversaire: {self.hp_adversaire}/{self.hp_adversaire_max}")


    def attaque_adversaire(self):
        nb_atk = random.randint(1, 2)
        if nb_atk == 1:
            print(
                f"{self.nom_adversaire} utilise {cP.pokedex[self.nom_adversaire].moves[0].name}!")
            self.hp_joueur -= cP.calcul_damage(
                self.nom_joueur, self.nom_adversaire, cP.pokedex[self.nom_adversaire].moves[0].name)
            if self.hp_joueur < 0:
                self.hp_joueur = 0
            self.barre_vie_joueur.setValue(self.hp_joueur)
            self.barre_vie_joueur.setFormat(
                f"Vie Joueur: {self.hp_joueur}/{self.hp_joueur_max}")

        elif nb_atk == 2:
            print(
                f"{self.nom_adversaire} utilise {cP.pokedex[self.nom_adversaire].moves[1].name}!")
            self.hp_joueur -= cP.calcul_damage(
                self.nom_joueur, self.nom_adversaire, cP.pokedex[self.nom_adversaire].moves[1].name)
            if self.hp_joueur < 0:
                self.hp_joueur = 0
            self.barre_vie_joueur.setValue(self.hp_joueur)
            self.barre_vie_joueur.setFormat(
                f"Vie Joueur: {self.hp_joueur}/{self.hp_joueur_max}")

    
    def capture_pokemon(self):
        result = random.randint(0, 10)
        if result != 0:
            print("plop")
            time.sleep(1)
            if result >= 1:
                time.sleep(0.5)
                print("plop")
                time.sleep(1)
            else:
                print("Vous n'avez pas réussi à capturer ce Pokémon...")
            if result >= 2:
                time.sleep(0.5)
                print("plop")
                time.sleep(1)
            else:
                print("Vous n'avez pas réussi à capturer ce Pokémon... Aaah presque!")
            if result >= 4:
                time.sleep(1)
                print(f"Vous avez capturé {self.nom_adversaire}!")
                if len(liste_pokemon_joueur) < 6:
                    liste_pokemon_joueur.append(self.nom_adversaire)
                    time.sleep(0.5)
                    print(f"{self.nom_adversaire} rejoint votre équipe!")
                    print(liste_pokemon_joueur)
                else:
                    print(liste_pokemon_joueur)
                    while True:
                        reponse = input(
                            f"Voulez-vous ajouter {self.nom_adversaire} à votre équipe ? (O/N): ")
                        if reponse.upper() == 'O':
                            if liste_pokemon_joueur:
                                while True:
                                    pokemon_a_retirer = input(
                                        "Quel Pokémon de votre équipe souhaitez-vous retirer ? (Entrez son nom) ")
                                    if pokemon_a_retirer in liste_pokemon_joueur:
                                        liste_pokemon_joueur.remove(
                                            pokemon_a_retirer)
                                        liste_pokemon_joueur.append(
                                            self.nom_adversaire)
                                        print(
                                            f"{self.nom_adversaire} rejoint votre équipe!")
                                        print(
                                            f"Voici votre équipe: {liste_pokemon_joueur}")
                                        self.reject()
                                        break
                                    else:
                                        print(
                                            "Ce Pokémon ne fait pas partie de votre équipe.")
                            else:
                                liste_pokemon_joueur.append(
                                    self.nom_adversaire)
                                print(
                                    f"{self.nom_adversaire} rejoint votre équipe!")
                                print(
                                    f"Voici votre équipe: {liste_pokemon_joueur}")
                                self.reject()
                            break
                        elif reponse.upper() == 'N':
                            print(
                                "Vous avez choisi de ne pas ajouter ce Pokémon à votre équipe.")
                            print(liste_pokemon_joueur)
                            self.reject()
                            break
                        else:
                            print(
                                "Réponse invalide. Veuillez répondre par 'O' pour oui ou 'N' pour non.")
        else:
            print("Vous n'avez pas réussi à capturer ce Pokémon.. Mince.")
        print("Fin de combat.")
        self.reject()


    def fin_de_combat(self):
        
        if self.hp_adversaire <= 0:
            print("Le Pokémon adverse est K.O! Vous venez de lancer une Poké Ball!")
            time.sleep(2)
            self.capture_pokemon()
            self.accept()
            return True
        elif self.hp_joueur <= 0:
            print(f"{self.nom_joueur} est K.O!")
            liste_pokemon_vivant.remove(self.nom_joueur)
            nbr_vivant = len(liste_pokemon_vivant)
            self.show_defeat_dialog(nbr_vivant)
            return True
        return False

    
    def init_pokemon_vivant(self):
        global liste_pokemon_vivant
        liste_pokemon_vivant = [pokemon for pokemon in liste_pokemon_joueur]

    def show_defeat_dialog(self, nbr_vivant):
        global liste_pokemon_vivant
        global liste_pokemon_joueur
        if nbr_vivant > 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Votre Pokémon est K.O! Voulez-vous changer de Pokémon ou fuir?")
            msg.setWindowTitle("Défaite")
            bouton_fuir = msg.addButton("Fuir", QMessageBox.RejectRole)
            bouton_changer = msg.addButton("Changer de Pokémon", QMessageBox.AcceptRole)
            msg.exec_()
            if msg.clickedButton() == bouton_fuir:
                self.fuir()
            elif msg.clickedButton() == bouton_changer:
                self.changer_pokemon()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Tous vos Pokémon sont K.O! Game Over.")
            msg.setWindowTitle("Game Over")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.close_combat()
            # Réinitialiser la liste des Pokémon vivants
            liste_pokemon_vivant = liste_pokemon_joueur[:]

    def close_combat(self):
        self.reject()

    def fuir(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Vous avez fuit!")
        msg.setWindowTitle("Fuite")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.close_combat)
        msg.exec_()



class ChangerPokemonDialog(QDialog):
    def __init__(self, pokemons):
        super().__init__()
        self.setWindowTitle("Changer de Pokémon")
        self.setFixedSize(600, 400)  # Ajustez la taille de la fenêtre selon vos besoins

        self.selection = None

        layout = QGridLayout()

        for i, pokemon in enumerate(pokemons):
            label = QLabel(cP.pokedex[liste_pokemon_joueur[i]].name)
            bouton = QPushButton(f"Choisir {cP.pokedex[liste_pokemon_joueur[i]].name}")
            bouton.clicked.connect(lambda checked, p=cP.pokedex[liste_pokemon_joueur[i]].name: self.choisir_pokemon(p))
            layout.addWidget(label, i, 0)
            layout.addWidget(bouton, i, 1)

        self.setLayout(layout)

    def choisir_pokemon(self, pokemon):
        self.selection = pokemon
        self.accept()




# Fonction pour lancer l'interface de combat
def lancer_interface_combat(nom_joueur, nom_adversaire):
    app = QApplication(sys.argv)
    combat_window = CombatWindow(
        nom_joueur, nom_adversaire, cP.pokedex[nom_joueur].hp, cP.pokedex[nom_adversaire].hp)
    combat_window.exec_()
    


# Test
if __name__ == "__main__":
    bulbizarre_hp = cP.pokedex["Bulbizarre"].hp
    print(bulbizarre_hp)
    bulbizarre_moves = cP.pokedex["Bulbizarre"].moves[0].name
    print(bulbizarre_moves)
