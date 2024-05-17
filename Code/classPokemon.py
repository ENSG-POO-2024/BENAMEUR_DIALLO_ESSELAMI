# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:48:30 2024

@author: benoi
"""
import random as random
import csv


class Pokemon:
    def __init__(self, name, type_1, type_2, hp, attack, defense, attackSpecial, defenseSpecial, speed, moves, is_Legendary=False):
        self.name = name
        self.type_1 = type_1
        self.type_2 = type_2  # None si il n'en a pas
        self.hp = hp
        self.attack = attack
        self.attackSpecial = attackSpecial
        self.defense = defense
        self.defenseSpecial = defenseSpecial
        self.speed = speed  # Status du Pokémon (par exemple : Healthy, Paralyzed, poison, freezed, etc.)
        self.moves = moves  # Liste des attaques du Pokémon
        
  
class Move:
    def __init__(self, name, move_type, power, is_physical=True):
        self.name = name
        self.move_type = move_type
        self.power = power
        self.is_physical = is_physical
         
  
class Type:
    def __init__(self, nom, fort_contre=None, faible_contre=None, resistant_contre=None, pas_tres_efficace_contre=None, inefficace_contre=None, immunise_a=None):
        self.nom = nom
        self.fort_contre = fort_contre if fort_contre else []
        self.faible_contre = faible_contre if faible_contre else []
        self.resistant_contre = resistant_contre if resistant_contre else []
        self.inefficace_contre = inefficace_contre if inefficace_contre else []
        self.pas_tres_efficace_contre = pas_tres_efficace_contre if pas_tres_efficace_contre else []
        self.immunise_a = immunise_a if immunise_a else [] 
    


def calcul_damage(defenseur ,attaquant, move_choisi):
    """
    

    Parameters
    ----------
    defenseur : str
        nom du Pokémon qui subit l'attaque.
    attaquant : str
       nom du Pokémon qui réalise l'attaque.
    move_choisi : str
        nom de l'attaque.

    Returns 
    -------
    int
        renvoi le montant de dégâts infligés.

    """
    
    pv_loss = 0
    
    
    
    type_1_defenseur = pokedex[defenseur].type_1
    type_2_defenseur = pokedex[defenseur].type_2
    type_1_attaquant = pokedex[attaquant].type_1
    type_2_attaquant = pokedex[attaquant].type_2
    
    atk =  pokedex[attaquant].attack
    defense = pokedex[defenseur].defense
    spe_atk = pokedex[attaquant].attackSpecial
    spe_def = pokedex[defenseur].defenseSpecial
     
    puiss = moves[move_choisi].power
    
    CM=1
    
    move_type = moves[move_choisi].move_type
    
    if move_type == type_1_attaquant or move_type == type_2_attaquant: 
        CM = 1.5 #condition pour que l'effet du stab soit pris en compte
    if move_type in types[type_1_defenseur].faible_contre:
        CM = CM*2
    if move_type in types[type_1_defenseur].resistant_contre:
        CM = CM*0.5
    if move_type in types[type_1_defenseur].immunise_a:
        CM = 0
    if type_2_defenseur != None:    
        
        if move_type in types[type_2_defenseur].faible_contre:
            CM = CM*2
        if move_type in types[type_2_defenseur].resistant_contre:
            CM = CM*0.5
        if move_type in types[type_2_defenseur].immunise_a:
            CM = 0
    
    if CM == 0:
        pv_loss = 0
        print("C'est inefficace!")
        
    if moves[move_choisi].is_physical == True: 
        pv_loss = (((((50*0.4 +2)*atk*puiss)/defense)/50)+2)*CM #formule pour une attaque physique
    
    elif moves[move_choisi].is_physical == False:
       pv_loss = (((((50*0.4 +2)*spe_atk*puiss)/spe_def)/50)+2)*CM #formule pour une attaque spéciale
    
    if CM > 2:
        print("C'est super efficace!")
    elif CM < 1 and CM > 0:
        print("Ce n'est pas très efficace")
    
    return round(pv_loss)



#Définition des dicotionnaires
types = {
    "Normal": Type("Normal", faible_contre=["Combat"], pas_tres_efficace_contre=["Roche", "Acier"], inefficace_contre=["Spectre"], immunise_a=["Spectre"]),
    "Feu": Type("Feu", faible_contre=["Eau", "Roche", "Sol"], resistant_contre=["Feu", "Plante", "Glace", "Insecte", "Fée"], fort_contre=["Plante", "Glace", "Insecte", "Acier"], pas_tres_efficace_contre=["Feu", "Eau", "Roche", "Dragon"]),
    "Eau": Type("Eau", faible_contre=["Électrik", "Plante"], resistant_contre=["Feu", "Eau", "Glace"], fort_contre=["Feu", "Sol", "Roche"], pas_tres_efficace_contre=["Eau", "Dragon", "Plante"]),
    "Électrik": Type("Électrik", faible_contre=["Sol"], resistant_contre=["Électrik", "Vol", "Acier"], fort_contre=["Eau", "Vol"], pas_tres_efficace_contre=["Plante", "Dragon"], inefficace_contre=["Sol"]),
    "Plante": Type("Plante", faible_contre=["Feu", "Glace", "Poison", "Vol", "Insecte"], resistant_contre=["Plante", "Eau", "Électrik", "Sol"], fort_contre=["Eau", "Sol", "Roche"], pas_tres_efficace_contre=["Feu", "Plante", "Vol", "Poison", "Insecte", "Dragon", "Acier"]),
    "Glace": Type("Glace", faible_contre=["Feu", "Combat", "Roche", "Acier"], resistant_contre=["Glace"], fort_contre=["Plante", "Sol", "Vol", "Dragon"], pas_tres_efficace_contre=["Acier", "Glace", "Eau"]),
    "Combat": Type("Combat", faible_contre=["Vol", "Psy", "Fée"], resistant_contre=["Insecte", "Roche", "Ténèbres"], fort_contre=["Normal", "Glace", "Roche", "Ténèbres", "Acier"], pas_tres_efficace_contre=["Psy", "Fée", "Vol"], inefficace_contre=["Spectre"]),
    "Poison": Type("Poison", faible_contre=["Sol", "Psy"], resistant_contre=["Plante", "Combat", "Poison", "Insecte", "Fée"], fort_contre=["Plante", "Fée"], pas_tres_efficace_contre=["Spectre", "Poison", "Roche"], inefficace_contre=["Acier"]),
    "Sol": Type("Sol", faible_contre=["Eau", "Plante", "Glace"], resistant_contre=["Poison", "Roche"], fort_contre=["Feu", "Électrik", "Poison", "Roche", "Acier"], pas_tres_efficace_contre=["Plante", "Insecte"], inefficace_contre=["Vol"], immunise_a=["Électrik"]),
    "Vol": Type("Vol", faible_contre=["Électrik", "Glace", "Roche"], resistant_contre=["Plante", "Combat", "Insecte"], fort_contre=["Plante", "Combat", "Insecte"], pas_tres_efficace_contre=["Acier", "Électrik", "Roche"], immunise_a=["Sol"]),
    "Psy": Type("Psy", faible_contre=["Insecte", "Spectre", "Ténèbres"], resistant_contre=["Combat", "Psy"], fort_contre=["Combat", "Poison"], pas_tres_efficace_contre=["Psy", "Acier"], inefficace_contre=["Ténèbres"]),
    "Insecte": Type("Insecte", faible_contre=["Feu", "Vol", "Roche"], resistant_contre=["Plante", "Combat", "Sol"], fort_contre=["Plante", "Psy", "Ténèbres"], pas_tres_efficace_contre=["Acier", "Feu", "Poison", "Spectre", "Fée", "Combat", "Vol"]),
    "Roche": Type("Roche", faible_contre=["Eau", "Plante", "Combat", "Sol", "Acier"], resistant_contre=["Normal", "Poison", "Vol", "Feu"], fort_contre=["Feu", "Glace", "Vol", "Insecte"], pas_tres_efficace_contre=["Acier", "Combat", "Sol"]),
    "Spectre": Type("Spectre", faible_contre=["Spectre", "Ténèbres"], resistant_contre=["Poison", "Insecte"], fort_contre=["Psy", "Spectre"], pas_tres_efficace_contre=["Ténèbres"], inefficace_contre=["Normal"], immunise_a=["Normal", "Combat"]),
    "Dragon": Type("Dragon", faible_contre=["Glace", "Dragon", "Fée"], resistant_contre=["Plante", "Feu", "Eau", "Électrik"], fort_contre=["Dragon"], pas_tres_efficace_contre=["Acier"], inefficace_contre=["Fée"]),
    "Ténèbres": Type("Ténèbres", faible_contre=["Combat", "Insecte", "Fée"], resistant_contre=["Spectre", "Ténèbres"], fort_contre=["Psy", "Spectre"], pas_tres_efficace_contre=["Ténèbres", "Fée", "Combat"], immunise_a=["Psy"]),
    "Acier": Type("Acier", faible_contre=["Feu", "Combat", "Sol"], resistant_contre=["Normal", "Plante", "Glace", "Vol", "Psy", "Insecte", "Roche", "Dragon", "Acier", "Fée"], fort_contre=["Glace", "Roche", "Fée"], pas_tres_efficace_contre=["Feu", "Eau", "Acier", "Électrik"], immunise_a=["Poison"]),
    "Fée": Type("Fée", faible_contre=["Poison", "Acier"], resistant_contre=["Combat", "Insecte", "Ténèbres"], fort_contre=["Combat", "Dragon", "Ténèbres"], pas_tres_efficace_contre=["Feu", "Acier", "Poison"], immunise_a=["Dragon"])
}



moves = {
    "Charge": Move("Charge", "Normal", 50),
    "Lance-Flammes": Move("Lance-Flammes", "Feu", 90, is_physical=False),
    "Surf": Move("Surf", "Eau", 90, is_physical=False),
    "Tonnerre": Move("Tonnerre", "Électrik", 90, is_physical=False),
    "Éco-Sphère": Move("Éco-Sphère", "Plante", 90),
    "Laser Glace": Move("Laser Glace", "Glace", 90, is_physical=False),
    "Casse-Brique": Move("Casse-Brique", "Combat", 75),
    "Détritus": Move("Détritus", "Poison", 65, is_physical=False),
    "Séisme": Move("Séisme", "Sol", 100),
    "Tornade": Move("Tornade", "Vol", 40, is_physical=False),
    "Psyko": Move("Psyko", "Psy", 90, is_physical=False),
    "Piqûre": Move("Piqûre", "Insecte", 60),
    "Tomberoche": Move("Tomberoche", "Roche", 65),
    "Ball'Ombre": Move("Ball'Ombre", "Spectre", 80, is_physical=False),
    "Draco-Choc": Move("Draco-Choc", "Dragon", 85, is_physical=False),
    "Morsure": Move("Morsure", "Ténèbres", 60),
    "Luminocanon": Move("Luminocanon", "Acier", 80, is_physical = False),
    "Pouvoir Lunaire": Move("Pouvoir Lunaire", "Fée", 95, is_physical=False)
}





pokedex = {
    "Bulbizarre": Pokemon("Bulbizarre", "Plante", "Poison", 120, 69, 69, 85, 85, 65, [moves["Charge"], moves["Éco-Sphère"]]),
    "Herbizarre": Pokemon("Herbizarre", "Plante", "Poison", 135, 82, 83, 100, 100, 80, [moves["Charge"], moves["Éco-Sphère"]]),
    "Florizarre": Pokemon("Florizarre", "Plante", "Poison", 155, 102, 103, 120, 120, 100, [moves["Détritus"], moves["Éco-Sphère"]]),
    "Salamèche": Pokemon("Salamèche", "Feu", None, 114, 72, 63, 80, 90, 85, [moves["Charge"], moves["Lance-Flammes"]]),
    "Reptincel": Pokemon("Reptincel", "Feu", None, 133, 84, 78, 100, 85, 100, [moves["Charge"], moves["Lance-Flammes"]]),
    "Dracaufeu": Pokemon("Dracaufeu", "Feu", "Vol", 153, 104, 98, 129, 105, 120, [moves["Draco-Choc"], moves["Lance-Flammes"]]),
    "Carapuce": Pokemon("Carapuce", "Eau", None, 119, 68, 85, 70, 84, 63, [moves["Charge"], moves["Surf"]]),
    "Carabaffe": Pokemon("Carabaffe", "Eau", None, 134, 83, 100, 85, 100, 78, [moves["Charge"], moves["Surf"]]),
    "Tortank": Pokemon("Tortank", "Eau", None, 154, 103, 120, 105, 125, 98, [moves["Laser Glace"], moves["Surf"]]),
    "Chenipan": Pokemon("Chenipan", "Insecte", None, 120, 50, 55, 40, 40, 65, [moves["Charge"], moves["Piqûre"]]),
    "Chrysacier": Pokemon("Chrysacier", "Insecte", None, 125, 40, 75, 45, 45, 50, [moves["Charge"], moves["Piqûre"]]),
    "Papilusion": Pokemon("Papilusion", "Insecte", "Vol", 135, 65, 70, 110, 100, 90, [moves["Tornade"], moves["Piqûre"]]),
    "Aspicot": Pokemon("Aspicot", "Insecte", "Poison", 115, 55, 50, 40, 40, 70, [moves["Charge"], moves["Piqûre"]]),
    "Coconfort": Pokemon("Coconfort", "Insecte", "Poison", 120, 45, 70, 45, 45, 55, [moves["Charge"],moves["Piqûre"]]),
    "Dardargnan": Pokemon("Dardargnan", "Insecte", "Poison", 140, 110, 60, 65, 100, 95, [moves["Piqûre"], moves["Détritus"]]),
    "Roucool": Pokemon("Roucool", "Normal", "Vol", 115, 65, 60, 55, 55, 76, [moves["Tornade"], moves["Charge"]]),
    "Roucoups": Pokemon("Roucoups", "Normal", "Vol", 138, 80, 75, 70, 70, 91, [moves["Tornade"], moves["Charge"]]),
    "Roucarnage": Pokemon("Roucarnage", "Normal", "Vol", 158, 100, 95, 90, 90, 121, [moves["Tornade"], moves["Charge"]]),
    "Rattata": Pokemon("Rattata", "Normal", None, 105, 76, 55, 45, 55, 92, [moves["Charge"],moves["Morsure"]]),
    "Rattatac": Pokemon("Rattatac", "Normal", None, 130, 101, 80, 70, 90, 117, [moves["Charge"], moves["Morsure"]]),
    "Piafabec": Pokemon("Piafabec", "Normal", "Vol", 115, 80, 50, 51, 51, 90, [moves["Charge"], moves["Tornade"]]),
    "Rapasdepic": Pokemon("Rapasdepic", "Normal", "Vol", 140, 110, 85, 81, 81, 120, [moves["Charge"], moves["Tornade"]]),
    "Abo": Pokemon("Abo", "Poison", None, 110, 80, 64, 60, 74, 75, [moves["Détritus"], moves["Morsure"]]),
    "Arbok": Pokemon("Arbok", "Poison", None, 135, 115, 89, 85, 99, 100, [moves["Détritus"], moves["Morsure"]]),
    "Pikachu": Pokemon("Pikachu", "Électrik", None, 110, 75, 60, 70, 70, 110, [moves["Charge"], moves["Tonnerre"]]),
    "Raichu": Pokemon("Raichu", "Électrik", None, 135, 110, 75, 110, 100, 130, [moves["Casse-Brique"], moves["Tonnerre"]]),
    "Sabelette": Pokemon("Sabelette", "Sol", None, 125, 95, 105, 40, 50, 60, [moves["Charge"], moves["Tomberoche"]]),
    "Sablaireau": Pokemon("Sablaireau", "Sol", None, 150, 120, 130, 65, 75, 85, [moves["Tomberoche"], moves["Séisme"]]),
    "Nidoran♀": Pokemon("Nidoran♀", "Poison", None, 130, 67, 72, 60, 60, 61, [moves["Charge"], moves["Détritus"]]),
    "Nidorina": Pokemon("Nidorina", "Poison", None, 145, 82, 87, 75, 75, 76, [moves["Morsure"], moves["Détritus"]]),
    "Nidoqueen": Pokemon("Nidoqueen", "Poison", "Sol", 165, 112, 107, 95, 105, 96, [moves["Séisme"], moves["Détritus"]]),
    "Nidoran♂": Pokemon("Nidoran♂", "Poison", None, 121, 77, 60, 60, 60, 70, [moves["Charge"], moves["Détritus"]]),
    "Nidorino": Pokemon("Nidorino", "Poison", None, 136, 92, 77, 75, 75, 85, [moves["Morsure"], moves["Détritus"]]),
    "Nidoking": Pokemon("Nidoking", "Poison", "Sol", 156, 122, 97, 105, 95, 105, [moves["Séisme"], moves["Détritus"]]),
    "Mélofée": Pokemon("Mélofée", "Fée", None, 145, 65, 68, 80, 85, 55, [moves["Charge"], moves["Pouvoir Lunaire"]]),
    "Mélodelfe": Pokemon("Mélodelfe", "Fée", None, 170, 90, 93, 115, 110, 80, [moves["Pouvoir Lunaire"], moves["Tonnerre"]]),
    "Goupix": Pokemon("Goupix", "Feu", None, 113, 61, 60, 70, 85, 85, [moves["Charge"], moves["Lance-Flammes"]]),
    "Feunard": Pokemon("Feunard", "Feu", None, 148, 96, 95, 101, 120, 120, [moves["Ball'Ombre"], moves["Lance-Flammes"]]),
    "Rondoudou": Pokemon("Rondoudou", "Normal", "Fée", 190, 65, 40, 65, 45, 40, [moves["Charge"], moves["Pouvoir Lunaire"]]),
    "Grodoudou": Pokemon("Grodoudou", "Normal", "Fée", 215, 90, 65, 105, 70, 65, [moves["Charge"], moves["Pouvoir Lunaire"]]),
    "Nosferapti": Pokemon("Nosferapti", "Poison", "Vol", 115, 65, 55, 50, 60, 75, [moves["Tornade"], moves["Morsure"]]),
    "Nosferalto": Pokemon("Nosferalto", "Poison", "Vol", 150, 100, 90, 85, 95, 110, [moves["Tornade"], moves["Morsure"]]),
    "Mystherbe": Pokemon("Mystherbe", "Plante", "Poison", 120, 70, 75, 95, 85, 50, [moves["Éco-Sphère"], moves["Détritus"]]),
    "Ortide": Pokemon("Ortide", "Plante", "Poison", 135, 85, 90, 105, 95, 60, [moves["Éco-Sphère"], moves["Détritus"]]),
    "Rafflesia": Pokemon("Rafflesia", "Plante", "Poison", 150, 100, 105, 130, 110, 70, [moves["Éco-Sphère"], moves["Pouvoir Lunaire"]]),
    "Paras": Pokemon("Paras", "Insecte", "Plante", 110, 90, 75, 65, 75, 45, [moves["Piqûre"], moves["Charge"]]),
    "Parasect": Pokemon("Parasect", "Insecte", "Plante", 135, 115, 100, 80, 100, 50, [moves["Piqûre"], moves["Éco-Sphère"]]),
    "Mimitoss": Pokemon("Mimitoss", "Insecte", "Poison", 135, 75, 70, 60, 75, 65, [moves["Piqûre"], moves["Détritus"]]),
    "Aéromite": Pokemon("Aéromite", "Insecte", "Poison", 145, 85, 80, 110, 95, 110, [moves["Psyko"], moves["Détritus"]]),
    "Taupiqueur": Pokemon("Taupiqueur", "Sol", None, 85, 75, 45, 55, 65, 115, [moves["Charge"], moves["Séisme"]]),
    "Triopikeur": Pokemon("Triopikeur", "Sol", None, 110, 120, 70, 70, 90, 140, [moves["Tomberoche"], moves["Séisme"]]),
    "Miaouss": Pokemon("Miaouss", "Normal", None, 115, 65, 55, 60, 60, 110, [moves["Charge"], moves["Morsure"]]),
    "Persian": Pokemon("Persian", "Normal", None, 140, 90, 80, 85, 85, 135, [moves["Tonnerre"], moves["Morsure"]]),
    "Psykokwak": Pokemon("Psykokwak", "Eau", None, 125, 72, 68, 85, 70, 75, [moves["Surf"], moves["Charge"]]),
    "Akwakwak": Pokemon("Akwakwak", "Eau", None, 155, 102, 98, 115, 100, 105, [moves["Surf"], moves["Psyko"]]),
    "Férosinge": Pokemon("Férosinge", "Combat", None, 115, 100, 55, 55, 65, 90, [moves["Charge"], moves["Casse-Brique"]]),
    "Colossinge": Pokemon("Colossinge", "Combat", None, 140, 125, 80, 60, 70, 95, [moves["Séisme"], moves["Casse-Brique"]]),
    "Caninos": Pokemon("Caninos", "Feu", None, 130, 90, 65, 90, 70, 80, [moves["Morsure"], moves["Charge"]]),
    "Arcanin": Pokemon("Arcanin", "Feu", None, 165, 130, 100, 120, 100, 115, [moves["Morsure"], moves["Lance-Flammes"]]),
    "Ptitard": Pokemon("Ptitard", "Eau", None, 115, 70, 60, 60, 60, 110, [moves["Surf"], moves["Laser Glace"]]),
    "Têtarte": Pokemon("Têtarte", "Eau", None, 140, 85, 85, 70, 70, 110, [moves["Surf"], moves["Laser Glace"]]),
    "Tartard": Pokemon("Tartard", "Eau", "Combat", 165, 115, 115, 90, 110, 90, [moves["Surf"], moves["Casse-Brique"]]),
    "Abra": Pokemon("Abra", "Psy", None, 100, 40, 35, 125, 75, 110, [moves["Psyko"],moves["Casse-Brique"]]),
    "Kadabra": Pokemon("Kadabra", "Psy", None, 115, 55, 50, 140, 90, 125, [moves["Psyko"], moves["Casse-Brique"]]),
    "Alakazam": Pokemon("Alakazam", "Psy", None, 130, 70, 65, 155, 115, 140, [moves["Psyko"], moves["Casse-Brique"]]),
    "Machoc": Pokemon("Machoc", "Combat", None, 145, 100, 70, 55, 55, 55, [moves["Tomberoche"], moves["Casse-Brique"]]),
    "Machopeur": Pokemon("Machopeur", "Combat", None, 155, 120, 90, 70, 80, 65, [moves["Tomberoche"], moves["Casse-Brique"]]),
    "Mackogneur": Pokemon("Mackogneur", "Combat", None, 165, 150, 100, 85, 105, 75, [moves["Casse-Brique"], moves["Séisme"]]),
    "Chétiflor": Pokemon("Chétiflor", "Plante", "Poison", 125, 95, 55, 90, 50, 60, [moves["Éco-Sphère"],moves["Détritus"]]),
    "Boustiflor": Pokemon("Boustiflor", "Plante", "Poison", 140, 110, 70, 105, 65, 75, [moves["Éco-Sphère"], moves["Détritus"]]),
    "Empiflor": Pokemon("Empiflor", "Plante", "Poison", 155, 125, 85, 120, 90, 90, [moves["Éco-Sphère"], moves["Détritus"]]),
    "Tentacool": Pokemon("Tentacool", "Eau", "Poison", 115, 60, 55, 70, 120, 90, [moves["Surf"], moves["Détritus"]]),
    "Tentacruel": Pokemon("Tentacruel", "Eau", "Poison", 155, 90, 85, 100, 140, 120, [moves["Surf"], moves["Détritus"]]),
    "Racaillou": Pokemon("Racaillou", "Roche", "Sol", 115, 100, 120, 50, 50, 40, [moves["Charge"], moves["Tomberoche"]]),
    "Gravalanch": Pokemon("Gravalanch", "Roche", "Sol", 130, 115, 135, 65, 65, 55, [moves["Charge"], moves["Tomberoche"]]),
    "Grolem": Pokemon("Grolem", "Roche", "Sol", 155, 140, 150, 75, 85, 65, [moves["Séisme"], moves["Tomberoche"]]),
    "Ponyta": Pokemon("Ponyta", "Feu", None, 125, 105, 75, 85, 85, 110, [moves["Lance-Flammes"], moves["Charge"]]),
    "Galopa": Pokemon("Galopa", "Feu", None, 140, 120, 90, 100, 100, 125, [moves["Lance-Flammes"], moves["Charge"]]),
    "Ramoloss": Pokemon("Ramoloss", "Eau", "Psy", 165, 85, 85, 60, 60, 35, [moves["Charge"], moves["Surf"]]),
    "Flagadoss": Pokemon("Flagadoss", "Eau", "Psy", 170, 95, 130, 120, 100, 50, [moves["Surf"], moves["Psyko"]]),
    "Magnéti": Pokemon("Magnéti", "Électrik", "Acier", 100, 55, 90, 115, 75, 65, [moves["Luminocanon"], moves["Tonnerre"]]),
    "Magnéton": Pokemon("Magnéton", "Électrik", "Acier", 125, 80, 115, 140, 90, 90, [moves["Luminocanon"], moves["Tonnerre"]]),
    "Canarticho": Pokemon("Canarticho", "Normal", "Vol", 127, 110, 75, 78, 82, 80, [moves["Charge"], moves["Tornade"]]),
    "Doduo": Pokemon("Doduo", "Normal", "Vol", 110, 105, 65, 55, 55, 95, [moves["Charge"], moves["Tornade"]]),
    "Dodrio": Pokemon("Dodrio", "Normal", "Vol", 135, 130, 90, 80, 80, 130, [moves["Charge"], moves["Tornade"]]),
    "Otaria": Pokemon("Otaria", "Eau", None, 140, 65, 75, 65, 90, 65, [moves["Surf"], moves["Charge"]]),
    "Lamantine": Pokemon("Lamantine", "Eau", "Glace", 165, 90, 100, 90, 115, 90, [moves["Surf"],moves["Laser Glace"]]),
    "Tadmorv": Pokemon("Tadmorv", "Poison", None, 155, 100, 70, 60, 70, 45, [moves["Détritus"], moves["Charge"]]),
    "Grotadmorv": Pokemon("Grotadmorv", "Poison", None, 180, 125, 95, 85, 120, 70, [moves["Détritus"],moves["Séisme"]]),
    "Kokiyas": Pokemon("Kokiyas", "Eau", "Glace", 105, 85, 120, 65, 45, 60, [moves["Charge"], moves["Laser Glace"]]),
    "Crustabri": Pokemon("Crustabri", "Eau", "Glace", 125, 115, 200, 105, 65, 90, [moves["Surf"], moves["Laser Glace"]]),
    "Fantominus": Pokemon("Fantominus", "Spectre", "Poison", 105, 55, 50, 120, 55, 100, [moves["Ball'Ombre"], moves["Détritus"]]),
    "Spectrum": Pokemon("Spectrum", "Spectre", "Poison", 120, 70, 65, 135, 75, 115, [moves["Ball'Ombre"], moves["Détritus"]]),
    "Ectoplasma": Pokemon("Ectoplasma", "Spectre", "Poison", 135, 85, 80, 150, 95, 130, [moves["Ball'Ombre"], moves["Psyko"]]),
    "Onix": Pokemon("Onix", "Roche", "Sol", 110, 65, 180, 50, 65, 90, [moves["Charge"], moves["Tomberoche"]]),
    "Soporifik": Pokemon("Soporifik", "Psy", None, 135, 68, 65, 63, 110, 62, [moves["Psyko"], moves["Ball'Ombre"]]),
    "Hypnomade": Pokemon("Hypnomade", "Psy", None, 160, 93, 90, 93, 135, 87, [moves["Psyko"], moves["Ball'Ombre"]]),
    "Krabby": Pokemon("Krabby", "Eau", None, 105, 125, 110, 45, 45, 70, [moves["Charge"], moves["Surf"]]),
    "Krabboss": Pokemon("Krabboss", "Eau", None, 130, 150, 135, 70, 70, 95, [moves["Charge"], moves["Surf"]]),
    "Voltorbe": Pokemon("Voltorbe", "Électrik", None, 115, 50, 70, 75, 75, 120, [moves["Charge"], moves["Tonnerre"]]),
    "Électrode": Pokemon("Électrode", "Électrik", None, 135, 70, 90, 100, 100, 170, [moves["Charge"], moves["Tonnerre"]]),
    "Noeunoeuf": Pokemon("Noeunoeuf", "Plante", "Psy", 135, 60, 100, 80, 65, 60, [moves["Éco-Sphère"], moves["Psyko"]]),
    "Noadkoko": Pokemon("Noadkoko", "Plante", "Psy", 170, 115, 105, 145, 95, 75, [moves["Éco-Sphère"], moves["Psyko"]]),
    "Osselait": Pokemon("Osselait", "Sol", None, 125, 70, 115, 60, 70, 55, [moves["Charge"], moves["Tomberoche"]]),
    "Ossatueur": Pokemon("Ossatueur", "Sol", None, 135, 100, 130, 70, 100, 65, [moves["Tomberoche"], moves["Séisme"]]),
    "Kicklee": Pokemon("Kicklee", "Combat", None, 125, 140, 73, 55, 130, 107, [moves["Charge"], moves["Casse-Brique"]]),
    "Tygnon": Pokemon("Tygnon", "Combat", None, 125, 125, 99, 55, 130, 96, [moves["Charge"], moves["Casse-Brique"]]),
    "Excelangue": Pokemon("Excelangue", "Normal", None, 165, 75, 95, 80, 95, 50, [moves["Charge"], moves["Tonnerre"]]),
    "Smogo": Pokemon("Smogo", "Poison", None, 115, 85, 115, 80, 65, 55, [moves["Détritus"], moves["Charge"]]),
    "Smogogo": Pokemon("Smogogo", "Poison", None, 140, 110, 140, 105, 90, 80, [moves["Détritus"], moves["Lance-Flammes"]]),
    "Rhinocorne": Pokemon("Rhinocorne", "Sol", "Roche", 155, 105, 115, 50, 50, 45, [moves["Charge"], moves["Tomberoche"]]),
    "Rhinoféros": Pokemon("Rhinoféros", "Sol", "Roche", 180, 150, 140, 65, 65, 60, [moves["Tomberoche"], moves["Séisme"]]),
    "Leveinard": Pokemon("Leveinard", "Normal", None, 325, 25, 25, 55, 125, 70, [moves["Tonnerre"], moves["Laser Glace"]]),
    "Saquedeneu": Pokemon("Saquedeneu", "Plante", None, 140, 75, 135, 120, 60, 80, [moves["Charge"], moves["Éco-Sphère"]]),
    "Kangourex": Pokemon("Kangourex", "Normal", None, 180, 115, 100, 60, 100, 110, [moves["Casse-Brique"], moves["Morsure"]]),
    "Hypotrempe": Pokemon("Hypotrempe", "Eau", None, 105, 60, 90, 90, 45, 80, [moves["Charge"], moves["Surf"]]),
    "Hypocéan": Pokemon("Hypocéan", "Eau", None, 130, 85, 115, 115, 65, 105, [moves["Surf"],moves["Draco-Choc"]]),
    "Poissirène": Pokemon("Poissirène", "Eau", None, 120, 87, 80, 55, 70, 83, [moves["Charge"], moves["Surf"]]),
    "Poissoroy": Pokemon("Poissoroy", "Eau", None, 155, 112, 85, 85, 100, 88, [moves["Charge"], moves["Surf"]]),
    "Stari": Pokemon("Stari", "Eau", None, 105, 65, 75, 90, 75, 105, [moves["Charge"], moves["Surf"]]),
    "Staross": Pokemon("Staross", "Eau", "Psy", 135, 95, 105, 120, 105, 135, [moves["Psyko"], moves["Surf"]]),
    "M. Mime": Pokemon("M. Mime", "Psy", "Fée", 115, 65, 85, 120, 140, 110, [moves["Tonnerre"], moves["Psyko"]]),
    "Insécateur": Pokemon("Insécateur", "Insecte", "Vol", 145, 130, 100, 75, 100, 125, [moves["Charge"], moves["Piqûre"]]),
    "Lippoutou": Pokemon("Lippoutou", "Glace", "Psy", 140, 70, 55, 135, 115, 115, [moves["Psyko"], moves["Laser Glace"]]),
    "Élektek": Pokemon("Élektek", "Électrik", None, 140, 103, 60, 110, 95, 105, [moves["Tonnerre"], moves["Casse-Brique"]]),
    "Magmar": Pokemon("Magmar", "Feu", None, 140, 115, 77, 120, 105, 113, [moves["Lance-Flammes"], moves["Psyko"]]),
    "Scarabrute": Pokemon("Scarabrute", "Insecte", None, 140, 145, 120, 75, 90, 105, [moves["Piqûre"], moves["Casse-Brique"]]),
    "Tauros": Pokemon("Tauros", "Normal", None, 150, 120, 115, 60, 90, 130, [moves["Charge"], moves["Séisme"]]),
    "Magicarpe": Pokemon("Magicarpe", "Eau", None, 95, 30, 75, 35, 40, 100, [moves["Charge"], moves["Surf"]]),
    "Léviator": Pokemon("Léviator", "Eau", "Vol", 170, 145, 99, 80, 120, 101, [moves["Morsure"], moves["Séisme"]]),
    "Lokhlass": Pokemon("Lokhlass", "Eau", "Glace", 205, 105, 100, 105, 115, 80, [moves["Surf"], moves["Laser Glace"]]),
    "Métamorph": Pokemon("Métamorph", "Normal", None, 123, 68, 68, 68, 68, 68, [moves["Charge"], moves["Laser Glace"]]),
    "Evoli": Pokemon("Evoli", "Normal", None, 130, 75, 70, 65, 85, 75, [moves["Charge"], moves["Morsure"]]),
    "Aquali": Pokemon("Aquali", "Eau", None, 205, 85, 80, 130, 115, 85, [moves["Charge"], moves["Surf"]]),
    "Voltali": Pokemon("Voltali", "Électrik", None, 140, 85, 80, 130, 115, 150, [moves["Charge"], moves["Tonnerre"]]),
    "Pyroli": Pokemon("Pyroli", "Feu", None, 140, 150, 80, 115, 130, 85, [moves["Charge"], moves["Lance-Flammes"]]),
    "Porygon": Pokemon("Porygon", "Normal", None, 140, 80, 90, 105, 95, 60, [moves["Laser Glace"], moves["Tonnerre"]]),
    "Amonita": Pokemon("Amonita", "Roche", "Eau", 110, 60, 120, 110, 75, 55, [moves["Charge"], moves["Surf"]]),
    "Amonistar": Pokemon("Amonistar", "Roche", "Eau", 145, 80, 145, 135, 90, 75, [moves["Tomberoche"], moves["Surf"]]),
    "Kabuto": Pokemon("Kabuto", "Roche", "Eau", 105, 100, 110, 75, 65, 75, [moves["Charge"], moves["Surf"]]),
    "Kabutops": Pokemon("Kabutops", "Roche", "Eau", 135, 135, 125, 85, 90, 100, [moves["Surf"], moves["Tomberoche"]]),
    "Ptéra": Pokemon("Ptéra", "Roche", "Vol", 155, 125, 85, 80, 95, 150, [moves["Morsure"], moves["Tomberoche"]]),
    "Ronflex": Pokemon("Ronflex", "Normal", None, 235, 130, 85, 85, 130, 50, [moves["Séisme"], moves["Casse-Brique"]]),
    "Artikodin": Pokemon("Artikodin", "Glace", "Vol", 165, 105, 120, 115, 145, 105, [moves["Tornade"], moves["Laser Glace"]]),
    "Électhor": Pokemon("Électhor", "Électrik", "Vol", 165, 110, 105, 145, 110, 120, [moves["Tornade"], moves["Tonnerre"]]),
    "Sulfura": Pokemon("Sulfura", "Feu", "Vol", 165, 120, 110, 145, 105, 110, [moves["Tornade"], moves["Lance-Flammes"]]),
    "Minidraco": Pokemon("Minidraco", "Dragon", None, 116, 84, 65, 70, 70, 70, [moves["Charge"], moves["Draco-Choc"]]),
    "Draco": Pokemon("Draco", "Dragon", None, 136, 104, 85, 90, 90, 90, [moves["Surf"], moves["Draco-Choc"]]),
    "Dracolosse": Pokemon("Dracolosse", "Dragon", "Vol", 166, 154, 115, 120, 120, 100, [moves["Lance-Flammes"], moves["Draco-Choc"]]),
    "Mewtwo": Pokemon("Mewtwo", "Psy", None, 181, 130, 110, 174, 110, 150, [moves["Ball'Ombre"], moves["Psyko"]]),
    "Mew": Pokemon("Mew", "Psy", None, 175, 120, 120, 120, 120, 120, [moves["Laser Glace"], moves["Psyko"]]),
    "Feuforêve": Pokemon("Feuforêve", "Spectre", None, 135, 80, 80, 105, 105, 105, [moves["Ball'Ombre"], moves["Psyko"]]),
    }
