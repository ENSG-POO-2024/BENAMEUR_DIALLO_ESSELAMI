# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:08:42 2024

@author: benoi
"""


import random
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QProgressBar, QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import classPokemon as cP
import time
from Test import liste_pokemon_joueur
import os
import dico_nombre as dc


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

        # Barres de vie
        self.barre_vie_joueur = QProgressBar()
        self.barre_vie_joueur.setRange(0, hp_joueur)
        self.barre_vie_joueur.setValue(hp_joueur)  # Valeur initiale = HP max
        self.barre_vie_joueur.setFormat(f"{hp_joueur}/{self.hp_joueur_max}")

        self.barre_vie_adversaire = QProgressBar()
        self.barre_vie_adversaire.setRange(0, hp_adversaire)
        self.barre_vie_adversaire.setValue(hp_adversaire)  # Valeur initiale = HP max
        self.barre_vie_adversaire.setFormat(f"{hp_adversaire}/{self.hp_adversaire_max}")
        
        # Détermination de la largeur des barres de vie
        self.barre_vie_joueur.setFixedWidth(600)  
        self.barre_vie_adversaire.setFixedWidth(600)  

        # Zones de texte pour les noms des Pokémon
        self.label_nom_joueur = QLabel("Nom Joueur:")
        self.zone_texte_nom_joueur = QLineEdit(nom_joueur)
        self.zone_texte_nom_joueur.setReadOnly(True)  # Rendre la zone de texte non modifiable
        self.zone_texte_nom_joueur.setFixedWidth(self.barre_vie_joueur.width())

        self.label_nom_adversaire = QLabel("Nom Adversaire:")
        self.zone_texte_nom_adversaire = QLineEdit(nom_adversaire)
        self.zone_texte_nom_adversaire.setReadOnly(True)  # Rendre la zone de texte non modifiable
        self.zone_texte_nom_adversaire.setFixedWidth(self.barre_vie_adversaire.width())

        # Emplacements d'images
        self.image_joueur = QLabel(self)
        self.image_adversaire = QLabel(self)
        
        # Layout horizontal pour décaler l'image de l'adversaire
        self.hbox_adversaire = QHBoxLayout()
        self.hbox_adversaire.addItem(QSpacerItem(550, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.hbox_adversaire.addWidget(self.image_adversaire)
        self.hbox_adversaire.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Boutons
        self.bouton_attaquer = QPushButton("Attaquer")
        self.bouton_fuir = QPushButton("Fuir")
        self.bouton_changer_pokemon = QPushButton("Changer de Pokemon")

        # Layout vertical pour organiser les éléments
        self.combat_layout = QVBoxLayout()  
        self.combat_layout.addWidget(self.label_nom_adversaire)
        self.combat_layout.addWidget(self.zone_texte_nom_adversaire)
        self.combat_layout.addWidget(self.barre_vie_adversaire)
        self.combat_layout.addLayout(self.hbox_adversaire)
        self.combat_layout.addWidget(self.image_adversaire)
        self.mettre_a_jour_image_adversaire()
        
        self.combat_layout.addWidget(self.image_joueur)
        self.mettre_a_jour_image_joueur()
        self.combat_layout.addWidget(self.label_nom_joueur)
        self.combat_layout.addWidget(self.zone_texte_nom_joueur)
        self.combat_layout.addWidget(self.barre_vie_joueur)
        
        # Ajouter un espace vide pour séparer la barre de vie et le bouton "Attaquer"
        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.combat_layout.addItem(spacer)
        
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
        
        self.set_background_image(os.path.join(os.path.dirname(__file__), "sprites", "Capture.png"))
        
    
    def set_background_image(self, image_path):
        """
        permet d'afficher l'image en arrière plan de la boite de dialogue combat

        Parameters
        ----------
        image_path : str
            chemin relatif à l'image de background.

        Returns
        -------
        None.

        """
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)
    
        
    def changer_pokemon(self):
        """
        ouvre la boite de dialogue pour sélectionner le Pokémon à changer en combat,
        selon la liste de pokemon encore en vie. Appelle la méthode permuter_pokemon et ChangerPokemonDialog 

        Returns
        -------
        None.

        """
        changer_pokemon_dialog = ChangerPokemonDialog(liste_pokemon_vivant)
        if changer_pokemon_dialog.exec_() == QDialog.Accepted:
            nouveau_pokemon = changer_pokemon_dialog.selection
            self.permuter_pokemon(nouveau_pokemon)
            
    def retirer_boutons_attaque(self):
        """
        méthode qui permet de retirer les boutons attaque 1 et attaque 2 générer par le bouton attaque

        Returns
        -------
        None.

        """
        
    # Retirer les boutons attaque 1 et attaque 2 du layout
        self.combat_layout.removeWidget(self.case_attaque_1)
        self.combat_layout.removeWidget(self.case_attaque_2)
        # Supprimer les boutons de l'interface
        self.case_attaque_1.deleteLater()
        self.case_attaque_2.deleteLater()   
        


    def get_image_path(self, pokemon_name):
        """
        
        
        Parameters
        ----------
        pokemon_name : str
            DESCRIPTION.

        Returns
        -------
        str
            le chemin d'accès correspondant à l'image du pokemon d'entrée.

        """
        return os.path.join(os.path.dirname(__file__), "sprites", f"spr_g_{dc.get_pokemon_number(pokemon_name)}.png")


    def mettre_a_jour_image_joueur(self):
        """
        permet d'actualiser les images du pokemon du joueur actuellement sur le terrain

        Returns
        -------
        None.

        """
        pixmap = QPixmap(self.get_image_path(self.nom_joueur))
        if pixmap.isNull():
            print("Image not found")
        self.image_joueur.setPixmap(pixmap)

    def mettre_a_jour_image_adversaire(self):
        """
        De même que la méthode d'avant mais pour l'adversaire

        Returns
        -------
        None.

        """
        pixmap = QPixmap(self.get_image_path(self.nom_adversaire))
        if pixmap.isNull():
            print("Image not found")
        self.image_adversaire.setPixmap(pixmap)
    

    def permuter_pokemon(self, nom_pokemon):
        """
        permet d'échanger l'emplacement dans la liste global pokemon joueur 
        celui du pokemon choisis avec celui de l'index 0'

        Parameters
        ----------
        nom_pokemon : str
            nom du pokemon à échanger.

        Returns
        -------
        None.

        """
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
        """
        Met à jour les éléments comme les barres de vie et les noms des zones de texte

        Returns
        -------
        None.

        """
        self.zone_texte_nom_joueur.setText(cP.pokedex[self.nom_joueur].name)
        self.barre_vie_joueur.setRange(0, cP.pokedex[self.nom_joueur].hp)
        self.barre_vie_joueur.setValue(cP.pokedex[self.nom_joueur].hp)
        self.barre_vie_joueur.setFormat(f"Vie Joueur: {cP.pokedex[self.nom_joueur].hp}/{cP.pokedex[self.nom_joueur].hp}")
        self.mettre_a_jour_image_joueur()

    

    def attaquer(self):
        """
        Permet de faire apparaitre 2 autres push button qui seront lier à attaque_1 et à attaque_2
        qui correspondront par la suite aux 2 attaques du pokemon du joueur 

        Returns
        -------
        None.

        """

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
        """
        Définit le tour de jeu ,
        Définit quelle pokemon va attaquer en premier, 
        appele la fonction qui va jouer l'attaque 1 du pokemon joueur 
        

        Returns
        -------
        None.

        """
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
                    self.fin_de_combat()  
            else:
                self.attaque_joueur(1)
                if not self.fin_de_combat():
                    time.sleep(0.5)
                    self.attaque_adversaire()
                    self.fin_de_combat() 

    def attaquer_2(self):
        """
        De même sauf que ce sera avec l'attaque 2 du Pokémon du joueur

        Returns
        -------
        None.

        """
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
                    self.fin_de_combat()  
            else:
                self.attaque_joueur(2)
                if not self.fin_de_combat():
                    time.sleep(0.5)
                    self.attaque_adversaire()
                    self.fin_de_combat()  


    def attaque_joueur(self, nb_atk):
        """
        effectue l'attaque du joueur et met à jour les points de vie de l'adversaire
        
        Parameters
        ----------
        nb_atk : int
            nombre indiquant quelle est l'attaque sélectionné par le joueur.

        Returns
        -------
        None.

        """
        # Réduire les points de vie de l'adversaire
        self.retirer_boutons_attaque()
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
        """
        l'adversaire effectue lance un dé pour connaitre l'attaque qu'il effectue,
        effectue les mêmes actions que la méthode précédente

        Returns
        -------
        None.

        """
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
        """
        méthode qui lance une pokéball et a une chance de capturer le pokémon (3 'plop'),
        ajoute le pokémon, si capturé, dans la liste de pokémon du joueur si il n'y a pas déjà 6 emplacements
        sinon demande à l'utilisateur de remplacer un de ses pokemons si il le souhaite. 

        Returns
        -------
        None.

        """
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
        """
        méthode qui vérifie l'état des joueurs et gère les résultats des combats  

        Returns
        -------
        bool
            si le combat n'est pas fini -> False .

        """
        
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
        """
        permet d'initialiser la liste de pokemon vivant (utiliser en début de combat)

        Returns
        -------
        None.

        """
        global liste_pokemon_vivant
        liste_pokemon_vivant = [pokemon for pokemon in liste_pokemon_joueur]

    def show_defeat_dialog(self, nbr_vivant):
        """
        affiche une boite de dialogue permettant de changer de pokemon si il en reste en vie,
        sinon ferme la page de combat

        Parameters
        ----------
        nbr_vivant : int
            DESCRIPTION.

        Returns
        -------
        None.

        """
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
        self.setFixedSize(600, 400)  

        self.selection = None

        layout = QGridLayout()

        for i, pokemon in enumerate(pokemons):
            label = QLabel(cP.pokedex[liste_pokemon_vivant[i]].name)
            bouton = QPushButton(f"Choisir {cP.pokedex[liste_pokemon_vivant[i]].name}")
            bouton.clicked.connect(lambda checked, p=cP.pokedex[liste_pokemon_vivant[i]].name: self.choisir_pokemon(p))
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
    


