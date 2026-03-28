# CONSIGNE : remplacer pass par les instructions attendues
# Les assertions vérifient certains résultats au fur et à mesure

zoo = [{'espèce': 'Lion', 'nom': 'Simba', 'classe': 'mammifère'},
       {'espèce': 'Kangourou', 'nom': 'Jumper', 'classe': 'mammifère'},
       {'espèce': 'Panda', 'nom': 'Pandi', 'classe': 'mammifère'},
       {'espèce': 'Raie', 'nom': 'Nicola', 'classe': 'poisson'},
       {'espèce': 'Gorille', 'nom': 'Kong', 'classe': 'mammifère'},
       {'espèce': 'Girafe', 'nom': 'Coucou', 'classe': 'mammifère'},
       {'espèce': 'Requin', 'nom': 'Marteau', 'classe': 'poisson'},
       {'espèce': 'Perroquet', 'nom': 'Blu', 'classe': 'oiseau'},
       {'espèce': 'Girafe', 'nom': 'Neck', 'classe': 'mammifère'},
       {'espèce': 'Autruche', 'nom': 'Speedy', 'classe': 'oiseau'},
       {'espèce': 'Panda', 'nom': 'Glass', 'classe': 'mammifère'},
       {'espèce': 'Lézard', 'nom': 'Curieux', 'classe': 'reptile'},
       {'espèce': 'Crapaud', 'nom': 'Prince', 'classe': 'amphibien'}
       ]

# Une fonction qui peut servir
def affiche(table):
    """Fonction qui affiche les éléments d'une table, un élément par ligne,
    quelle que soit le type de cet élément"""
    for element in table:
        print(element)
    print()    # permet de séparer un peu les affichages


# V) a) Importation de la table (dictionnaires) et affectation d'une variable
# Avec csv.reader(), on saute la ligne d'entête, et on définit manuellement les clés

import csv

def csv_dict(nomFichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    dictionnaires en sautant la ligne d'entêtes"""
    table = []
    with open(nomFichier, 'r', newline="", encoding="ISO-8859-1") as fichier: #l'encodage du fichier gestion.csv est ISO-8859-1
        fichier_lu = csv.reader(fichier, delimiter=";")
        compteur_en_tete = 0 
        for ligne in fichier_lu:
            compteur_en_tete += 1
            if compteur_en_tete == 1: #enregistrement des en-têtes qui seront utilisés comme clés des dictionnaires dans la liste
                liste_en_tete = ligne
            else:
                dictionnaire = {}
                index_en_tete = 0
                for colonne in ligne: #toutes les colonnes de la ligne
                    dictionnaire[liste_en_tete[index_en_tete]] = colonne #les colonnes sont affectés dans dictionnaire[clé de l'en-tête]
                    index_en_tete += 1
                table.append(dictionnaire) #on ajoute le dictionnaire à la liste
    return table

gestion = csv_dict('gestion.csv')
affiche(gestion)

# V) b) Importation de la table (dictionnaires) et affectation d'une variable
# Avec csv.DictReader(), on utilise la ligne d'entête comme clés

def csv_dict2(nomFichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    dictionnaires en utilisant la ligne d'entêtes comme clés"""
    table = []
    with open(nomFichier, 'r', newline="", encoding='ISO-8859-1') as fichier:
        fichier_lu = csv.DictReader(fichier, delimiter=";") #lecture 
        for element in fichier_lu:
            table.append(element) #dictionnaires ajoutés dans la liste
    return table

gestion2 = csv_dict2('gestion.csv')
assert gestion==gestion2
affiche(gestion2)


# VI) Fusion des deux tables

def fusion_tables(zoo,gestion):
    """Fonction qui combine les deux tables en ne gardant que les champs
    'nom', 'espèce', 'lieu' et 'comportement'"""
    table = []
    for iligne in range(len(zoo)): #on prend les éléments 'nom' et 'espèce' de la table zoo
        dict_ligne = {}
        dict_ligne['nom'] = zoo[iligne]['nom']
        dict_ligne['espèce'] = zoo[iligne]['espèce']
        table.append(dict_ligne)
    for iligne in range(len(gestion)):
        for element in gestion: #on prend les éléments 'lieu' et 'comportement' de la table gestion
            if table[iligne]['nom'] == element['nom']: #on associe les données au nom de l'animal pour fusionner les infos
                table[iligne]['lieu'] = element['lieu']
                table[iligne]['comportement'] = element['comportement']
    return table

fusion = fusion_tables(zoo,gestion2)
affiche(fusion)

# VII) Filtre d'une table suivant une valeur de champ

def filtre_table(table):
    """Fonction qui renvoir une table avec seulement les animaux n'ayant
    pas un comportement normal"""
    table_filtree = []
    for element in table:
        if element['comportement'] == 'normal':
            table_filtree.append(element)
    return table_filtree

problemes = filtre_table(fusion)
affiche(problemes)

#penser à enlever les chemins