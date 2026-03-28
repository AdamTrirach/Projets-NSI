#create_admin.py
#crée un compte administrateur dans la table UTILISATEUR
#utilise le hashage du mot de passe avec werkzeug.security

import sqlite3
from werkzeug.security import generate_password_hash  #pour hacher le mot de passe
import os

DB = "repertoire.db"

def creer_admin():
    if not os.path.exists(DB): #si le fichier db est introuvable il faut exécuter le fichier initialisation_bd.py
        print("Erreur : la base de données 'repertoire.db' n'existe pas.")
        print("Lance d'abord 'initialisation_bd.py' pour la créer.")
        return
    #database connexion à la base SQLite
    database = sqlite3.connect(DB)

    #création du hash du mot de passe
    mot_de_passe = "123456"
    hash_mdp = generate_password_hash(mot_de_passe)

    #données de l'admin
    identifiant = "admin"
    id_user = 1  #on peut mettre 1 car c’est le premier utilisateur

    try:
        #on vérifie si un admin existe déjà
        cur = database.execute("SELECT * FROM UTILISATEUR WHERE username = ?", (identifiant,))
        if cur.fetchone():
            print("Un utilisateur 'admin' existe déjà.")
            return

        #insertion du compte admin dans la table UTILISATEUR
        database.execute(
            "INSERT INTO UTILISATEUR (id_user, username, password_hash) VALUES (?, ?, ?)",
            (id_user, identifiant, hash_mdp)
        )
        database.commit()
        print("Compte administrateur créé avec succès !")
    except Exception as e: 
        print("Erreur lors de la création :", e)
    finally:
        database.close()

# Programme principal
if __name__ == "__main__":
    creer_admin()
