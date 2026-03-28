# Créé par adam.trirach et , le 14/10/2024 en Python 3.7
#Version avec manipulation de fichiers et mode de fichier

from random import randint

def fichier(): #Affiche le menu des fichiers
    boucle_fichier = True
    while boucle_fichier:
        boucle_fichier = False
        print() #Saute une ligne
        mode_fichier = str(input("Sélectionnez un mode de fichier :\n0 - Quitter\n1 - Nouveau fichier\n2 - Ouvrir un fichier\nVotre choix ? "))
        if mode_fichier == "0":
            return "0" #Renvoie l'information de fin de programme dans la fonction main
        if mode_fichier == "1":
            numero_fichier = str(randint(1, 1000000)) #Pour choisir un nom de fichier avec un numéro aléatoire pour ne pas qu'il y ait de nom de fichier potentiellement préexistant
            nom_fichier = f"nouveau_repertoire{numero_fichier}.txt"
            nouveau_fichier = open(nom_fichier,'w') #Création du nouveau fichier
            nouveau_fichier.write(f"Répertoire téléphonique {numero_fichier}\n") #Ecrire le titre du bloc note pour le nouveau fichier
            nouveau_fichier.close()
            print(f"Votre fichier s'appelle '{nom_fichier}'.\n")
            return nom_fichier #Nom du fichier retourné, enregistrement du nom du nouveau fichier pour le manipuler plus tard
        if mode_fichier == "2":
            probleme_fichier = True
            while probleme_fichier:
                extension_valide = False
                nom_fichier = str(input("Entrez le nom du fichier à importer avec l'extension : "))
                if nom_fichier[-4:] == ".txt": #Vérifie si le nom du fichier présete l'extension
                    extension_valide = True
                else:
                    print("L'extension est invalide ou ne figure pas dans le nom.")
                if extension_valide:
                    try:
                        fichier_ouvert = open(nom_fichier,'a')
                    except (IOError, OSError): #Le programme affichera le message ci-dessous s'il y a un problème lié au fichier.
                        print("Le fichier est introuvable, veuillez à ce qu'il se trouve dans le même emplacement que le programme.")
                    else:
                        probleme_fichier = False
                        print(f"Le fichier '{nom_fichier}' a bien été importé.\n")
            return nom_fichier #Nom du fichier retourné, enregistrement du nom du fichier préexistant pour le manipuler plus tard


def telephone_invalide(numéro): #Fonction permettant de vérifier si le numéro de téléphone est valide
    if numéro[0] == "0" and len(numéro) == 10: #Vérifie que le numéro de téléphone commence par 0 et comporte 10 caractères
        invalidation = False #On imagine que le téléphone est valide et sera reconnu invalide si nécessaire
        for chiffre in numéro:
            if chiffre not in "0123456789": #Vérifie que chaque caractère est un chiffre
                invalidation = True #Le téléphone n'est pas validé, le programme redemandera le nom du téléphone dans la fonction 'écriture'
                break
        return invalidation #Retourne True si téléphone invalide et False si téléphone valide
    else:
        return True #cf commentaire ligne 49

def ecriture(): #Permet l'ajout de contact avec les noms et les numéros de téléphone
    boucle_ecriture = True
    while boucle_ecriture:
        with open(repertoire_fichier, 'r') as fichier_extraction:
            contenu_fichier = fichier_extraction.read()
        print() #Sauter une ligne
        nom = str(input("Entrez un nom à ajouter dans le répertoire (0 pour terminer) : "))
        if nom == "0": #Quitter la fonction
            boucle_ecriture = False
        elif nom == "": #Détecte une entrée vide
            print("Vous n'avez entré aucun nom...")
        elif nom+" :" in contenu_fichier: #Regarde si le nom est déjà présent dans le répertoire
            print("Ce nom est déjà présent dans votre répertoire...")
        else:
            telephone_inadapte = True
            while telephone_inadapte: #Voir si le numéro de téléphone peut être ajouté dans la liste des contacts
                telephone = str(input("Téléphone : "))
                numéro_invalide = telephone_invalide(telephone) #Appelle la fonction vérifiant le numéro de téléphone
                if numéro_invalide: #Numéro de téléphone invalide
                    print("Le numéro de téléphone que vous avez entré est invalide. Veuillez réessayer en vérifiant qu'il y ait 10 chiffres et qu'il commence par 0.")
                else:
                    telephone_inadapte = False #On imagine que le numéro de téléphone est valide
                    if telephone in contenu_fichier:
                        telephone_inadapte = True
                        print("Le numéro de téléphone que vous avez entré existe déjà dans votre répertoire, veuillez réessayer.")
            with open(repertoire_fichier,'a') as fichier_ouvert: #Ajoute en écriture le contact en bloc-note
                fichier_ouvert.write(f"{nom} : {telephone}\n")
            print("Le contact a été ajouté dans votre répertoire avec succès.")


def lecture():
    erreur_nom = "Le nom que vous avez entré n'est pas présent dans votre répertoire." #Message d'erreur si le numéro de téléphone n'est pas localisé dans le répertoire
    boucle_lecture = True
    while boucle_lecture:
        print()
        nom = str(input("Entrez un nom à chercher dans le répertoire (0 pour terminer) :\n")) #demande le nom à cherche dans le répertoire
        if nom == "0": #Quitte le mode lecture
            boucle_lecture = False
        elif nom == "": #détecte une entrée vide
            print("Vous n'avez entré aucun nom...")
        else:
            with open(repertoire_fichier, 'r') as fichier_lecture: #Lecture du fichier
                nom_inconnu = True
                for ligne in fichier_lecture: #Vérifie chaque ligne
                    if nom+" :" in ligne: #Si le nom suivi d'un espace et de deux points est dans une des lignes du fichier
                        telephone = ligne[-11:-1] #Numéro de téléphone correspond aux 11 derniers caractères sans le retour à la ligne sur la ligne du nom retrouvé dans le fichier
                        print(f"Le numéro de téléphone de {nom} est : {telephone}.") #Affichage du numéro de téléphone
                        nom_inconnu = False #Le nom est retrouvé
                if nom_inconnu: #Si le nom n'a pas été localisé dans le fichier
                    print(erreur_nom) #Affichage du nombre d'erreur


def main():
    print("--- Début du programme ---")
    global repertoire_fichier #Globaliser le nom du fichier pour l'écriture
    repertoire_fichier = fichier()
    boucle_programme = True
    if repertoire_fichier == "0": #Quitter dans l'interface du mode de fichier
        print("\n--- Fin du programme ---")
        boucle_programme = False
    while boucle_programme: #Le menu s'affiche en boucle après une action tant que l'utilisateur ne quitte pas
        mode = str(input("0 - Quitter\n1 - Ecrire dans le répertoire\n2 - Rechercher dans le répertoire\nVotre choix ? ")) #Affiche les options du menu
        if mode == "0": #Quitter dans le menu du répertoire
            print("\n--- Fin du programme ---")
            boucle_programme = False
        if mode == "1": #Mode écriture
            ecriture()
        if mode == "2": #Mode lecture
            lecture()

main() #Lancement du programme

