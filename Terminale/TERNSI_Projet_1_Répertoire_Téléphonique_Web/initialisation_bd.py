#initialisation_bd.py

#initialise la base de données SQLite à partir de schema.sql
#crée ou recrée le fichier repertoire.db

import sqlite3
import os

def initialiser_base():
    #vérifie que le fichier schema.sql existe
    if not os.path.exists("schema.sql"):
        print("Erreur : fichier 'schema.sql' introuvable")
        return #arrete la fonction sans rien arreter (corrigée par l'IA, il y avait pass à la place)
    
    #supprime l'ancienne base si elle existe
    if os.path.exists("repertoire.db"): #vérifie si le fichier existe
        os.remove("repertoire.db") #supprime le fichier en question
        print("Info : ancienne BD supprimée")

    #connexion et exécution du SQL
    connexion = sqlite3.connect("repertoire.db") #crée / ouvre le fichier sql
    with open("schema.sql","r",encoding="utf8") as fichier_sql: #ouverture du fichier en mode lecture
        script=fichier_sql.read() #lit le contenu du fichier
        connexion.executescript(script) #execute les commandes sql du fichier
        print("Info : BD créée avec succès à partir de 'schema.sql'")

    #fermeture de la connexion
    connexion.close() 
    print("Fichier 'repertoire.db' prêt à être utilisée")

#programme principal
initialiser_base()
