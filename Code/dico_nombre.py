# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 09:41:54 2024

@author: Formation
"""


# Dictionnaire des 151 premiers Pokémon
pokemon_dict = {
    "Bulbizarre": "001",
    "Herbizarre": "002",
    "Florizarre": "003",
    "Salamèche": "004",
    "Reptincel": "005",
    "Dracaufeu": "006",
    "Carapuce": "007",
    "Carabaffe": "008",
    "Tortank": "009",
    "Chenipan": "010",
    "Chrysacier": "011",
    "Papilusion": "012",
    "Aspicot": "013",
    "Coconfort": "014",
    "Dardargnan": "015",
    "Roucool": "016",
    "Roucoups": "017",
    "Roucarnage": "018",
    "Rattata": "019",
    "Rattatac": "020",
    "Piafabec": "021",
    "Rapasdepic": "022",
    "Abo": "023",
    "Arbok": "024",
    "Pikachu": "025",
    "Raichu": "026",
    "Sabelette": "027",
    "Sablaireau": "028",
    "Nidoran♀": "029",
    "Nidorina": "030",
    "Nidoqueen": "031",
    "Nidoran♂": "032",
    "Nidorino": "033",
    "Nidoking": "034",
    "Mélofée": "035",
    "Mélodelfe": "036",
    "Goupix": "037",
    "Feunard": "038",
    "Rondoudou": "039",
    "Grodoudou": "040",
    "Nosferapti": "041",
    "Nosferalto": "042",
    "Mystherbe": "043",
    "Ortide": "044",
    "Rafflesia": "045",
    "Paras": "046",
    "Parasect": "047",
    "Mimitoss": "048",
    "Aéromite": "049",
    "Taupiqueur": "050",
    "Triopikeur": "051",
    "Miaouss": "052",
    "Persian": "053",
    "Psykokwak": "054",
    "Akwakwak": "055",
    "Férosinge": "056",
    "Colossinge": "057",
    "Caninos": "058",
    "Arcanin": "059",
    "Ptitard": "060",
    "Têtarte": "061",
    "Tartard": "062",
    "Abra": "063",
    "Kadabra": "064",
    "Alakazam": "065",
    "Machoc": "066",
    "Machopeur": "067",
    "Mackogneur": "068",
    "Chétiflor": "069",
    "Boustiflor": "070",
    "Empiflor": "071",
    "Tentacool": "072",
    "Tentacruel": "073",
    "Racaillou": "074",
    "Gravalanch": "075",
    "Grolem": "076",
    "Ponyta": "077",
    "Galopa": "078",
    "Ramoloss": "079",
    "Flagadoss": "080",
    "Magnéti": "081",
    "Magnéton": "082",
    "Canarticho": "083",
    "Doduo": "084",
    "Dodrio": "085",
    "Otaria": "086",
    "Lamantine": "087",
    "Tadmorv": "088",
    "Grotadmorv": "089",
    "Kokiyas": "090",
    "Crustabri": "091",
    "Fantominus": "092",
    "Spectrum": "093",
    "Ectoplasma": "094",
    "Onix": "095",
    "Soporifik": "096",
    "Hypnomade": "097",
    "Krabby": "098",
    "Krabboss": "099",
    "Voltorbe": "100",
    "Électrode": "101",
    "Noeunoeuf": "102",
    "Noadkoko": "103",
    "Osselait": "104",
    "Ossatueur": "105",
    "Kicklee": "106",
    "Tygnon": "107",
    "Excelangue": "108",
    "Smogo": "109",
    "Smogogo": "110",
    "Rhinocorne": "111",
    "Rhinoféros": "112",
    "Leveinard": "113",
    "Saquedeneu": "114",
    "Kangourex": "115",
    "Hypotrempe": "116",
    "Hypocéan": "117",
    "Poissirène": "118",
    "Poissoroy": "119",
    "Stari": "120",
    "Staross": "121",
    "M. Mime": "122",
    "Insécateur": "123",
    "Lippoutou": "124",
    "Élektek": "125",
    "Magmar": "126",
    "Scarabrute": "127",
    "Tauros": "128",
    "Magicarpe": "129",
    "Léviator": "130",
    "Lokhlass": "131",
    "Métamorph": "132",
    "Évoli": "133",
    "Aquali": "134",
    "Voltali": "135",
    "Pyroli": "136",
    "Porygon": "137",
    "Amonita": "138",
    "Amonistar": "139",
    "Kabuto": "140",
    "Kabutops": "141",
    "Ptéra": "142",
    "Ronflex": "143",
    "Artikodin": "144",
    "Électhor": "145",
    "Sulfura": "146",
    "Minidraco": "147",
    "Draco": "148",
    "Dracolosse": "149",
    "Mewtwo": "150",
    "Mew": "151",
    "Feuforêve" : "200",
}


# Fonction pour récupérer le numéro selon le nom du Pokémon
def get_pokemon_number(pokemon_name):
    return pokemon_dict.get(pokemon_name, "Pokémon non trouvé")

# Exemple d'utilisation
pokemon_name = "Pikachu"
pokemon_number = get_pokemon_number(pokemon_name)
print(f"Le numéro de {pokemon_name} est {pokemon_number}.")