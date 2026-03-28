#importation du module Flask et des fonctions utiles
from flask import Flask, render_template, request, redirect, url_for, session
import random

#création de l'application Flask
app = Flask(__name__) #ici on définit app comme le coeur du site

#clé secrète nécessaire pour utiliser les sessions (mémoriser des variables entre deux pages)
app.secret_key = "ma_clé_ultra_secrète"


#page d'accueil du site
@app.route("/") #associe l'URL "/" à la fonction ci-dessous
def index():
    return render_template("index.html")  #affiche le fichier templates/index.html


#pendu
@app.route("/pendu", methods=["GET", "POST"]) #route pour le jeu du pendu acceptant les méthodes GET et POST 
def pendu():
    #initialisation de la partie. Vérifie si c'est une nouvelle partie :
    if "mot" not in session:
        #on choisi au hasard dans le fichier texte du pendu 
        with open("data/mots_pendu.txt", "r", encoding="utf-8") as file:
            mots = file.read().splitlines() #lit le fichier ligne par ligne et le met dans un tableau 
            session["mot"] = random.choice(mots) #on choisit un mot dans la liste au hasard
            session["trouvees"] = []  #liste pour stocker les lettres correctement trouvées (dans la session)
            session["erreurs"] = 0  #compteur d'erreurs
            session["lettres_proposees"] = []  #liste de toutes les lettres déjà proposées

    #récupération des données de la partie depuis la session
    mot = session["mot"]
    trouvees = session["trouvees"]
    erreurs = session["erreurs"]
    lettres_proposees = session["lettres_proposees"]

    message = ""

    #traitement d'une proposition de lettre (méthode POST)
    if request.method == "POST":

        lettre = request.form["lettre"].lower() 
        #vérification : est-ce bien une seule lettre de a à z ?
        if not lettre.isalpha() or len(lettre) != 1: 
            message = "Entre une seule lettre de l'alphabet."
        elif lettre in lettres_proposees: #lettre déjà proposée ?
            message = "Tu as déjà proposé cette lettre."
        else: #nouvelle lettre proposée 
            lettres_proposees.append(lettre) #on enregistre cette lettre proposée
            if lettre in mot: #si la lettre est bonne
                trouvees.append(lettre) #on enregistre la lettre proposée parmi celles valides
                message = "Bonne lettre !"
            else:
                erreurs += 1 #sinon c'est compté comme une erreur !
                message = "Raté !"

        #on enregistre les données dans la session active
        session["trouvees"] = trouvees
        session["erreurs"] = erreurs
        session["lettres_proposees"] = lettres_proposees

    #construction de l'affichage du mot (avec les tirets du bas "_" pour les lettres cachées)
    affichage = ""
    for lettre in mot: #ce qui est fait ici en gros : on regarde chaque lettre du mot énoncé, si elle a été proposée par le joueur, on met la lettre telle quelle sinon on met un tiret du bas
        if lettre in trouvees: 
            affichage += lettre + " "
        else:
            affichage += "_ " #ne pas oublier l'espace

    #vérification de victoire ou défaite à chaque proposition 
    if set(mot).issubset(set(trouvees)): #vérifie si toutes les lettres présentes dans le mot énoncé se trouvent dans les lettres proposées
        #beaucoup plus propre qu'une boucle vérifiant chaque lettre manuellement et prend en compte les lettres qui se répètent (recommandé par une IA)
        message = "Bravo, tu as gagné ! Le mot était bien : " + mot
        session.clear()  #on réinitialise pour une nouvelle partie (en supprimant toutes les données enregistrées dans la session)

    elif erreurs >= 10: #le nombre d'erreurs tolérés est de 10 avant la fin de la partie
        message = "Tu as perdu ! Le mot était : " + mot
        session.clear()

    return render_template( #envoie le template HTML du pendu avec toutes les variables nécessaires pour les utiliser dans le développement de la page html associée 
        "pendu.html",                #nom du template HTML à afficher
        mot_affiche=affichage.strip(),  #mot à deviner avec les tirets du bas éventuellement
        erreurs=erreurs,             #nombre d'erreurs actuelles
        message=message,             #message d'information
        lettres=lettres_proposees    #liste des lettres déjà essayées (pour l'historique)
    )
#rejouer au pendu
@app.route("/rejouer",methods=["POST"])
def rejouer():
    session.clear()  #on supprime les données de la session (réinitialisiation)
    return redirect(url_for("pendu"))  #redirige à la page du pendu

#jeu des drapeaux type Jetpunk
@app.route("/drapeaux")
def drapeaux():
    return render_template("drapeaux.html")

#jeu memory informatique
@app.route("/memory")
def memory():
    return render_template("memory.html")

#devine le nombre mystère en un temps limité
@app.route("/nombre")
def nombre():
    return render_template("nombre.html")

#lancement du serveur si ce fichier est exécuté (DOIT ETRE A LA FIN DU FICHIER)
if __name__ == "__main__": #nécessaire pour éviter que le serveur se lance accidentellement
    app.run(debug=True)
    #debug=True permet au serveur de se recharger automatiquement quand le fichier se sauvegarde et de voir les erreurs en clair pendant le développement, à désactiver quand le site est entièrement développé
