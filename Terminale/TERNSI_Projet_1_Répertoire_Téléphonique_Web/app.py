# app.py
# Répertoire téléphonique web avec inscription / connexion / profil personnel

# Ce fichier contient :
#la logique d'affichage et de recherche du répertoire,
#l'inscription / connexion d'un utilisateur (création d'une fiche contact lors de l'inscription),
#la gestion d'un compte administrateur simple (login admin),
#les opérations CRUD (édition / suppression) avec contrôle d'accès.

# Remarques :
#On utilise SQLite (via sqlite3) pour stocker les données dans 'repertoire.db'.
#On utilise werkzeug.security (generate_password_hash/check_password_hash)
#uniquement pour ne pas stocker de mots de passe en clair

#Toutes les actions importantes (création, modification, suppression) sont protégées
#côté serveur : même si un utilisateur modifie l'URL, il ne pourra pas faire d'action sans autorisation.

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
#generate_password_hash : crée un haché à partir d'un mot de passe (stocké en DB)
#check_password_hash : vérifie qu'un mot de passe correspond au haché

# --- Configuration de l'application ---
app = Flask(__name__)
app.config["SECRET_KEY"] = "cle_dev"  #clé nécessaire pour flash() et session
#SECRET_KEY est nécessaire pour utiliser les sessions et les messages flash dans Flask.

#Création d'un hash pour le mot de passe admin : on le garde en mémoire seulement
_ADMIN_USERNAME = "admin"
_ADMIN_PLAIN_PW = "123456"
_ADMIN_HASH = generate_password_hash(_ADMIN_PLAIN_PW)

def admin_required(): #vérifie si l'utilisateur courant est identifié comme admin dans la session
    return session.get("is_admin") is True

# --- Connexion à la base ---
def get_conn(): #ouvre une connection sqlite à la base "repertoire.db"
    conn = sqlite3.connect("repertoire.db")
    conn.row_factory = sqlite3.Row #permet de récupérer les colonnes par nom
    return conn

def next_id(conn, table, col): #calcul le prochain id
    val = conn.execute(f"SELECT COALESCE(MAX({col}), 0)+1 FROM {table}").fetchone()[0]
    #utilisation de COALESCE pour gérer le cas où la table est vide 
    #utilisation de AuTOINCREMENT possible mais COALESCE est préféré
    return val

# --- ROUTES PRINCIPALES ---

# --- Page d'accueil : liste publique ---
@app.route("/")
def index():
    """
    Page d'accueil avec recherche avancée.
    On accepte plusieurs champs de recherche (nom, prenom, date_naissance, adresse,
    profession, phone_fixe, phone_portable, email). 
    Pour la plupart des champs on utilise LIKE (recherche partielle). Pour date_naissance on utilise une égalité simple.
    """
    #récupération des champs de recherche (GET)
    nom = request.args.get("nom", "").strip()
    prenom = request.args.get("prenom", "").strip()
    date_naissance = request.args.get("date_naissance", "").strip()
    adresse = request.args.get("adresse", "").strip()
    profession = request.args.get("profession", "").strip()
    phone_fixe = request.args.get("phone_fixe", "").strip()
    phone_portable = request.args.get("phone_portable", "").strip()
    email = request.args.get("email", "").strip()

    #Ici on sélectionne toutes les colonnes utiles
    query = ("SELECT id_contact, nom, prenom, date_naissance, adresse, profession, "
             "phone_fixe, phone_portable, email FROM CONTACT WHERE 1=1")
    params = []

    #pour les textes on utilise LIKE (recherche partielle)
    if nom:
        query += " AND nom LIKE ?"
        params.append(f"%{nom}%")
    if prenom:
        query += " AND prenom LIKE ?"
        params.append(f"%{prenom}%")
    # date : recherche exacte (format YYYY-MM-DD attendu). Si tu veux partial, utilise LIKE.
    if date_naissance:
        query += " AND date_naissance = ?"
        params.append(date_naissance)
    if adresse:
        query += " AND adresse LIKE ?"
        params.append(f"%{adresse}%")
    if profession:
        query += " AND profession LIKE ?"
        params.append(f"%{profession}%")
    if phone_fixe:
        query += " AND phone_fixe LIKE ?"
        params.append(f"%{phone_fixe}%")
    if phone_portable:
        query += " AND phone_portable LIKE ?"
        params.append(f"%{phone_portable}%")
    if email:
        query += " AND email LIKE ?"
        params.append(f"%{email}%")

    query += " ORDER BY id_contact" #tri dans l'ordre de id_contact

    #exécution de la requête et recup des resultats
    conn = get_conn()
    try:
        contacts = conn.execute(query,params).fetchall()
    finally: #toujours fermer la connexion pour éviter les erreurs 
        conn.close()

    #renvoie aussi les valeurs de recherche pour préremplir le formulaire
    return render_template("index.html", contacts=contacts,search_values={"nom": nom, "prenom": prenom, "date_naissance": date_naissance,"adresse": adresse, "profession": profession,"phone_fixe": phone_fixe, "phone_portable": phone_portable,"email": email})

# --- Inscription ---
@app.route("/register",methods=["GET","POST"])
def register():
    '''
    Formulmaire d'inscription
    crée un utilisateur dans la table UTILISATEUR (username + password_hash)
    créer simultanément une fiche dans CONTACT avec les info perso
    stocke la liaison UTILISATEUR.id_contact -> CONTACT.id_contact (pour retrouver la fiche plus tard)
    '''
    if request.method == "POST":
        #récupération des infos du formulaire
        username = request.form["username"].strip()
        password = request.form["password"]
        nom = request.form["nom"].strip()
        prenom = request.form["prenom"].strip()
        date_naissance = request.form.get("date_naissance") or None
        adresse = request.form.get("adresse") or None
        profession = request.form.get("profession") or None
        phone_fixe = request.form.get("phone_fixe") or None
        phone_portable = request.form.get("phone_portable")
        email = request.form.get("email") or None
        #les infos avec or None sont pas obligatoires

        #verification (si les infos requises ont bien été renseignés)
        if not username or not password or not nom or not prenom:
            flash("Les champs Nom, Prénom, Identifiant et Mot de passe sont obligatoires.", "error")
            return render_template("register.html")

        conn = get_conn()
        try:
            #vérifie si le nom d'utilisateur existe déjà
            exist = conn.execute("SELECT id_user FROM UTILISATEUR WHERE username = ?", (username,)).fetchone()
            if exist:
                flash("Nom d'utilisateur déjà pris.", "error")
                return render_template("register.html")

            #création du compte utilisateur (on insère d'abord avec id_contact NULL)
            id_user = next_id(conn, "UTILISATEUR", "id_user")
            hash_pw = generate_password_hash(password) #hashage du mot de passe
            # insert minimal (id_contact ajouté ensuite)
            conn.execute("INSERT INTO UTILISATEUR (id_user, username, password_hash, id_contact) VALUES (?, ?, ?, ?)",(id_user, username, hash_pw, None))

            #création de la fiche contact
            id_contact = next_id(conn, "CONTACT", "id_contact")
            conn.execute("""INSERT INTO CONTACT (id_contact, nom, prenom, date_naissance, adresse, profession, phone_fixe, phone_portable, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",(id_contact, nom, prenom, date_naissance, adresse, profession, phone_fixe, phone_portable, email))

            #lier le compte utilisateur à l'id_contact créé
            conn.execute("UPDATE UTILISATEUR SET id_contact = ? WHERE id_user = ?", (id_contact, id_user))
            conn.commit() #on sauvegarde les modifs

            flash("Compte et fiche créés avec succès. Connectez-vous.", "success")
            return redirect(url_for("login")) #redirection vers login après incription réussie
        finally:
            conn.close() #ferme la connexion

    return render_template("register.html")

# --- Connexion ---
@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Formulaire de connexion utilisateur normal
    On vérifie l'id et le mot de passe stocké en base, puis on place en session l'identifiant utilisateur et l'id_contact correspondant
    '''
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        conn = get_conn()
        try:
            #on recupere username, pasword_hash et id_contact
            user = conn.execute("SELECT id_user, username, password_hash, id_contact FROM UTILISATEUR WHERE username=?", (username,)).fetchone()
        finally:
            conn.close()

        #si l'identifiant et le mot de passe sont incorrectes
        if not user or not check_password_hash(user["password_hash"],password):
            flash("Identifiant ou mot de passe incorrect.","error")
            return render_template("login.html")

        #on enregistre la session avec id_contact (peut être NULL)
        session["user_id"] = user["id_user"]
        session["username"] = user["username"]
        session["contact_id"] = user["id_contact"] #None si pas lié
        flash("Connexion réussie.", "success")
        return redirect(url_for("profil"))

    return render_template("login.html")


# --- Déconnexion ---
@app.route("/logout")
def logout():
    '''
    Déconnecte l'utilisateur en vidant la session complète
    '''
    session.clear()
    flash("Déconnecté.","success")
    return redirect(url_for("index")) #retour à la page d'accueil

# --- Page profil (pour modifie sa propre fiche) ---
@app.route("/profil", methods=["GET", "POST"])
def profil():
    """
    Page permettant à l'utilisateur connecté de voir et modifier sa propre fiche
    Nous utilisons session['contact_id'] pour retrouver la fiche liée
    """
    if "username" not in session:
        flash("Connecte-toi d'abord.", "error")
        return redirect(url_for("login"))

    contact_id = session.get("contact_id")
    if not contact_id:
        flash("Aucune fiche liée à ce compte.", "error")
        return redirect(url_for("index"))

    conn = get_conn()
    try: #on récupere la fiche à partir de l'identifiant stocké en session
        person = conn.execute("SELECT * FROM CONTACT WHERE id_contact = ?", (contact_id,)).fetchone()
        if not person:
            flash("Fiche introuvable.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            #recup des champs du formulaire
            nom = request.form["nom"].strip()
            prenom = request.form["prenom"].strip()
            date_naissance = request.form.get("date_naissance") or None
            adresse = request.form.get("adresse") or None
            profession = request.form.get("profession") or None
            phone_fixe = request.form.get("phone_fixe") or None
            phone_portable = request.form.get("phone_portable") or None
            email = request.form.get("email") or None

            #mise a jour de la fiche dans la table CONTACT
            conn.execute("""UPDATE CONTACT SET nom=?, prenom=?, date_naissance=?, adresse=?, profession=?,
                            phone_fixe=?, phone_portable=?, email=? WHERE id_contact=?""",
                         (nom, prenom, date_naissance, adresse, profession, phone_fixe, phone_portable, email, contact_id))
            conn.commit()
            flash("Fiche mise à jour.", "success")

            #recharger la fiche pour affichage
            person = conn.execute("SELECT * FROM CONTACT WHERE id_contact = ?", (contact_id,)).fetchone()
    finally:
        conn.close()

    return render_template("profil.html", person=person)


# --- Edition d'une fiche (vue 'edit') ---
@app.route("/edit/<int:id_contact>",methods=["GET", "POST"])
def edit(id_contact):
    """
    Edition d'une fiche : accessible uniquement à l'admin ou au propriétaire (session['contact_id'])
    Cette vue est utilisée pour permettre à l'admin d'éditer n'importe quelle fiche et à un utilisateur de modifier sa propre fiche via l'ID stocké en session
    """
    #vérification d'autorisation :
    if not (session.get("is_admin") is True or session.get("contact_id") == id_contact):
        flash("Accès refusé : vous n'êtes pas autorisé à modifier cette fiche.", "error")
        return redirect(url_for("index"))

    conn = get_conn()
    try:
        #recuperation de la fiche à éditer
        person = conn.execute("SELECT * FROM CONTACT WHERE id_contact = ?", (id_contact,)).fetchone()
        if not person: #si personne introuvable
            flash("Personne introuvable.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            #lecture des champs envoyés ; si un champ est vide on garde l'ancienne info
            nom = request.form.get("nom", person["nom"]).strip()
            prenom = request.form.get("prenom", person["prenom"]).strip()
            date_naissance = request.form.get("date_naissance") or person["date_naissance"]
            adresse = request.form.get("adresse") or person["adresse"]
            profession = request.form.get("profession") or person["profession"]
            phone_fixe = request.form.get("phone_fixe") or person["phone_fixe"]
            phone_portable = request.form.get("phone_portable") or person["phone_portable"]
            email = request.form.get("email") or person["email"]

            #mise a jour en base
            conn.execute("""UPDATE CONTACT SET nom=?, prenom=?, date_naissance=?, adresse=?, profession=?, phone_fixe=?, phone_portable=?, email=? WHERE id_contact=?""", (nom, prenom, date_naissance, adresse, profession, phone_fixe, phone_portable, email, id_contact))
            conn.commit()
            flash("Personne mise à jour.","success")
            #si propriétaire, retourner vers profil ; si admin, vers admin dashboard
            if session.get("is_admin"): #si admin retourner au tableau admin sinon aller à profil
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("profil"))
    finally:
        conn.close()

    #affichage du formulaire d'édition (GET)
    return render_template("edit.html", person=person)



# --- Suppression d'une fiche (vue 'delete') ---
@app.route("/delete/<int:id_contact>", methods=["POST"])
def delete(id_contact):
    """
    Suppression : autorisée seulement à l'admin ou au propriétaire
    Si suppression réussie, redirige vers admin_dashboard (admin) ou index/profil (proprio)
    """
    #verif d'autorisation coté serveur (indsipensable pour la securité)
    if not (session.get("is_admin") is True or session.get("contact_id") == id_contact):
        flash("Accès refusé : vous n'êtes pas autorisé à supprimer cette fiche.", "error")
        return redirect(url_for("index"))

    conn = get_conn()
    try:
        person = conn.execute("SELECT nom, prenom FROM CONTACT WHERE id_contact = ?", (id_contact,)).fetchone()
        if not person:
            flash("Personne introuvable.", "error")
            return redirect(url_for("index"))

        #suppresion de la fiche
        conn.execute("DELETE FROM CONTACT WHERE id_contact = ?", (id_contact,))
        conn.commit()
        flash("Personne supprimée.", "success")
    finally:
        conn.close()

    #redirection adaptée
    if session.get("is_admin"): #si admin alors rediriger vers admin dashboard
        return redirect(url_for("admin_dashboard"))
    #si proprio supprimé sa propre fiche, on peut aussi vider sa session de contact
    session.pop("contact_id", None)
    return redirect(url_for("index"))

#--- Admin ---
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    '''
    Page de connexion spécifique à l'admin
    '''
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        #vérifier identifiant et mot de passe (hash)
        if username == _ADMIN_USERNAME and check_password_hash(_ADMIN_HASH, password):
            #ne pas clear() toute la session : on ne change que le flag admin et le username
            session["is_admin"] = True
            session["username"] = _ADMIN_USERNAME
            #retirer contact_id/user_id pour éviter confusion si admin veut travailler globalement
            session.pop("contact_id", None)
            session.pop("user_id", None)
            flash("Connexion admin réussie.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Identifiant admin ou mot de passe incorrect.", "error")
            return render_template("admin_login.html")
    return render_template("admin_login.html")

@app.route("/admin_logout")
def admin_logout():
    '''
    Déconnexion admin : ne supprime que le flag admin et username lié.
    On ne clear pas la session on garde la connexion de l'utilisateur (faute de temps)
    '''
    session.pop("is_admin", None)
    session.pop("username", None)
    flash("Admin déconnecté.", "success")
    return redirect(url_for("index"))

@app.route("/admin")
def admin_dashboard():
    '''
    Tableau de bord admin : liste complète des contacts avec actions
    '''
    if not admin_required():
        return redirect(url_for("admin_login"))
    conn = get_conn()
    try: #on selectionne les colonens utiles pour l'affichage admin
        contacts = conn.execute("SELECT id_contact, nom, prenom, profession, phone_portable, phone_fixe, email FROM CONTACT ORDER BY nom, prenom").fetchall()
    finally:
        conn.close()
    return render_template("admin_dashboard.html", contacts=contacts)

@app.route("/admin/confirm_delete/<int:id_contact>")
def admin_confirm_delete(id_contact):
    '''
    Affiche une page de confirmation avant suppression (admin only)
    '''
    if not admin_required():
        return redirect(url_for("admin_login"))
    conn = get_conn()
    try:
        person = conn.execute("SELECT id_contact, nom, prenom FROM CONTACT WHERE id_contact = ?", (id_contact,)).fetchone()
    finally:
        conn.close()
    if not person: #si personne introuvable
        flash("Personne introuvable.", "error")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_confirm_delete.html", person=person)

@app.route("/admin/delete/<int:id_contact>", methods=["POST"])
def admin_delete(id_contact):
    '''
    Supprime définitivement la fiche après confirmation pour l'admin
    '''
    if not admin_required(): #si pas admin
        return redirect(url_for("admin_login"))
    conn = get_conn()
    try:
        person = conn.execute("SELECT nom, prenom FROM CONTACT WHERE id_contact = ?", (id_contact,)).fetchone()
        if not person:
            flash("Personne introuvable.", "error")
            return redirect(url_for("admin_dashboard"))
        conn.execute("DELETE FROM CONTACT WHERE id_contact = ?", (id_contact,)) #suppression
        conn.commit()
        flash(f"Fiche de {person['nom']} {person['prenom']} supprimée.", "success")
    finally:
        conn.close()
    return redirect(url_for("admin_dashboard"))

# --- Alias pour compatibilité avec les templates ---
app.add_url_rule('/edit/<int:id_contact>', endpoint='edit_contact', view_func=edit, methods=['GET', 'POST'])
app.add_url_rule('/delete/<int:id_contact>', endpoint='delete_contact', view_func=delete, methods=['POST'])
#après erreur repérée par l'IA

# --- Lancer l'application ---
if __name__ == "__main__":
    app.run(debug=True)
