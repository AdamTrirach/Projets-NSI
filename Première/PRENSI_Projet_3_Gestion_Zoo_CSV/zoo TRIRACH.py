# CONSIGNE : remplacer pass par les instructions attendues
# Les assertions vérifient certains résultats au fur et à mesure

import csv


# Une fonction qui peut servir
def affiche(table):
    """Fonction qui affiche les éléments d'une table, un élément par ligne,
    quelle que soit le type de cet élément"""
    for element in table:
        print(element)
    print()    # permet de séparer un peu les affichages


# I) a) Importation de la table et affichage
# écrire le code donné dans l'énoncé
with open('zoo.csv', 'r', newline='') as csvfile:
    tableReader = csv.reader(csvfile, delimiter=';')
    tableReader.__next__()
    for row in tableReader:
        print(' - '.join(row))

# I) b) Importation de la table et affectation d'une variable
def csv_tuple(nom_fichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    tuples en sautant la ligne d'entêtes"""
    with open(nom_fichier,'r',newline='') as csvfile:
        tableReader = csv.reader(csvfile, delimiter=';') #Lecture du fichier
        liste_tuples = [tuple(row) for row in tableReader] #utilisation d'une compréhension de liste 
        liste_tuples = liste_tuples[1:] #supprimer l'en-tête de la liste de tuples
    return liste_tuples

zoo = csv_tuple('zoo.csv')
assert zoo==[('mammifère', 'Lion'),
             ('mammifère', 'Kangourou'),
             ('mammifère', 'Panda'),
             ('poisson', 'Raie'),
             ('mammifère', 'Gorille'),
             ('mammifère', 'Girafe'),
             ('poisson', 'Requin'),
             ('oiseau', 'Perroquet'),
             ('mammifère', 'Girafe'),
             ('oiseau', 'Autruche'),
             ('mammifère', 'Panda'),
             ('reptile', 'Lézard'),
             ('amphibien', 'Crapaud')
             ]
affiche(zoo)


# II) a) Ajout d'un panda

zoo.append(('mammifère','Panda'))
assert zoo==[('mammifère', 'Lion'),
             ('mammifère', 'Kangourou'),
             ('mammifère', 'Panda'),
             ('poisson', 'Raie'),
             ('mammifère', 'Gorille'),
             ('mammifère', 'Girafe'),
             ('poisson', 'Requin'),
             ('oiseau', 'Perroquet'),
             ('mammifère', 'Girafe'),
             ('oiseau', 'Autruche'),
             ('mammifère', 'Panda'),
             ('reptile', 'Lézard'),
             ('amphibien', 'Crapaud'),
             ('mammifère','Panda')
             ]
affiche(zoo)


# II) b) Détection de doublons

def detecte_doublons(table):
    """Fonction qui renvoie True si au moins un doublon est détecté"""
    doublon_detecte = False
    for iligne in range(len(table)): 
        for jligne in range(iligne+1, len(table)): #pour chaque élément nous vérifions s'il n'est pas égal à un autre élément parmi tout le reste si ça n'a pas déjà été fait
            if table[iligne]==table[jligne]:
                doublon_detecte = True
    return doublon_detecte

assert detecte_doublons(zoo)
assert not detecte_doublons([('mammifère', 'Lion'),
                               ('poisson', 'Perche'),
                               ('mammifère', 'Panda')
                               ])


# II) c) Suppression de doublons

#Yanis tu peux utiliser la fonction set() stv

def supprime_doublons(table):
    """Fonction qui supprime les doublons d'une table"""
    table_unique = [] #on separe les doublon des élèments unique
    table_doublons = []
    for ligne in table:
        if ligne not in table_unique: 
            table_unique.append(ligne)
        else:
            table_doublons.append(ligne)
    for doublon in table_doublons:
        table.remove(doublon) #on enleve les doublon de la table qui est en parametre de la fonction cela va supprimer directement les doublons de la table
    

supprime_doublons(zoo)
assert not detecte_doublons(zoo)
affiche(zoo)


# III) a) Importation de la table (listes) et affectation d'une variable

def csv_liste(nomFichier):
    """Fonction qui importe un fichier csv sous la forme d'une liste de
    listes en sautant la ligne d'entêtes"""
    with open(nomFichier,'r',newline='') as csvfile:
        tableReader = csv.reader(csvfile, delimiter=';')
        liste_csv = [list(row) for row in tableReader] #utilisation d'une compréhension de liste
        liste_csv = liste_csv[1:] #supprimer l'en-tête      
    return liste_csv  

zoo = csv_liste('zoo.csv')
assert zoo==[['mammifère', 'Lion'],
             ['mammifère', 'Kangourou'],
             ['mammifère', 'Panda'],
             ['poisson', 'Raie'],
             ['mammifère', 'Gorille'],
             ['mammifère', 'Girafe'],
             ['poisson', 'Requin'],
             ['oiseau', 'Perroquet'],
             ['mammifère', 'Girafe'],
             ['oiseau', 'Autruche'],
             ['mammifère', 'Panda'],
             ['reptile', 'Lézard'],
             ['amphibien', 'Crapaud']
             ]
affiche(zoo)

# III) b) Nommage des animaux

def ajout_nom(table): 
    """Fonction qui demande et ajoute un nom à chaque élément de la table"""
    for iligne in range(len(table)):
        inom = str(input(f"Comment voulez-vous nommer votre animal n°{iligne+1} qui est un {table[iligne][1].lower()} ? ")) #Affichage optimisé, la fonction lower() met le str en minuscules
        table[iligne].append(inom)

ajout_nom(zoo)
affiche(zoo)


# IV) Tri de la table suivant un champ

def tri_table(table,i):
    """Fonction qui tri la table en fonction du champ d'indice i"""
    table.sort(key = lambda x : x[i]) 

affiche(zoo)