import tkinter
from tkinter import messagebox, simpledialog #messagebox pour les messages d'info et d'erreur, simpledialog pour les petites interfaces d'entrée
import random

#fonctions de conversion

def convBase(nombre,baseA,baseB): #conversion d'une base A à une base B #nombre en str pour manipuler ses chiffres et bases en int
    digitlist = "0123456789ABCDEF" #liste des chiffres
    if baseA != 10: #Le nombre doit être converti en décimal
        indexd_length = -len(nombre)
        nombredecimal = 0
        for i in range(indexd_length, 0): #manipulation des chiffres en sens inverse
            nombredecimal += int(digitlist.index(nombre[i])) * baseA**(-i-1) #chiffre * base ** poids
        if baseB == 10:
            return str(nombredecimal) #On obtiendra le nombre converti en décimal en str
    if baseB != 10: #Conversion en bases autre que la base décimale
        if baseA == 10: #Le nombre est déjà un nombre décimal
            nombredecimal = int(nombre)
        nombreconverti = ""
        if nombredecimal == 0: #le cas où le nombre à convertir est déjà nul
            nombreconverti = "0"
        while nombredecimal != 0: #division euclidienne en boucle jusqu'à que le quotient soit égal à 0
            nombreconverti += digitlist[nombredecimal%baseB] #récupération du reste déterminant le chiffre via la liste des chiffres
            nombredecimal //= baseB #récupération du quotient
        nombreconverti = list(nombreconverti)
        nombreconverti.reverse() #Inversion des chiffres
        nombreconverti = "".join(nombreconverti) #Passage en str
        return nombreconverti #déjà en str


def convC2(nombre, baseA, bit): #si baseA est décimal, la conversion se fera en C2 et inversement #nombre et baseA en str et bit en int
    if baseA == 'decimal': #Conversion de décimal en C2
        if int(nombre) >= 0: #le nombre est positif ou nul
            nombrec2 = convBase(nombre, 10, 2) #entier naturel x #conversion en binaire
        else:
            nombrec2 = int(nombre) + 2**bit #entier naturel x + 2**n
            nombrec2 = convBase(str(nombrec2), 10, 2)
        liste_bits = ['0']*bit
        for i in range(1,len(nombrec2)+1):
            liste_bits[-i] = str(nombrec2[-i]) #pour remplir les bits avec des "0" à gauche
        nombrec2 = "".join(liste_bits)
        return nombrec2
    if baseA == 'C2': #Conversion de C2 à décimal
        if nombre[0] == '0': #Le bit de signe est de 0
            return convBase(nombre, 2, 10)
        else: #Le bit de signe est 1
            nombredecimal = int(convBase(nombre, 2, 10))
            return str(nombredecimal - 2**bit) #opération inverse

def convIEEE754(nombre, baseA, bit): #nombre en str, baseA en str ('decimal' ou 'IEEE754'), bit en int
    #définition des paramètres en fonction du nombre de bits (32 ou 64)
    if bit == 32:
        bitexp = 8
        bitmantisse = 23
    elif bit == 64:
        bitexp = 11
        bitmantisse = 52
    decalage = 2**(bitexp - 1) - 1  #décalage pour le codage de l'exposant
    if nombre == 0 and baseA == 'decimal':  #cas spécial lorsque le nombre égal 0
            return '0'*bit
    if baseA == 'decimal':  #conversion de décimal en IEEE754
        if float(nombre) > 0: #détermine le bit de signe
            signe = '0'
        elif float(nombre) < 0:
            signe = '1'
            nombre = str(-float(nombre))  #prend la valeur absolue du nombre
        nombre = float(nombre) #on travaillera avec le nombre en float
        exposantdec = 0 #Calcul de l'exposant
        nombretemporaire = nombre
        while nombretemporaire >= 2: #le cas où l'exposant sera positif
            nombretemporaire /= 2
            exposantdec += 1
        while nombretemporaire < 1: #le cas où l'exposant sera négatif
            nombretemporaire *= 2
            exposantdec -= 1
        exposantdec += decalage #exposant + décalage
        exposantbin = convBase(str(exposantdec), 10, 2)
        while len(exposantbin) < bitexp: #on remplit les bits manquant à gauche avec des '0'
            exposantbin = '0' + exposantbin
        #calcul de la mantisse
        mantissevaleur = nombre / (2 ** (exposantdec - decalage)) #mantisse sous forme a*2**n où 1 <= a < 2
        mantissevaleur -= 1  #normalisation
        mantisse = ""
        for _ in range(bitmantisse):
            mantissevaleur *= 2
            if mantissevaleur >= 1:
                mantisse += '1'
                mantissevaleur -= 1
            else:
                mantisse += '0'
        return signe + exposantbin + mantisse
    elif nombre == '0'*bit and baseA == 'IEEE754': #cas spécial avec 0
        return '0'
    elif baseA == 'IEEE754':  #conversion de IEEE754 en décimal
        if nombre[0] == '0': #récupération du bit de signe
            signe = 1
        elif nombre[0] == '1':
            signe = -1
        exposantbin = nombre[1:1 + bitexp]  #bits de l'exposant
        mantissebin = nombre[1 + bitexp:]  #bits de la mantisse
        exposantdec = int(convBase(exposantbin, 2, 10)) - decalage #exposant - décalage
        mantissevaleur = 1  #mantisse commence à 1 pour les nombres normaux
        #calcul de la mantisse en décimal
        puissance = -1
        for bit in mantissebin: #addition des poids à exposant négatif en partant de -1
            if bit == '1':
                mantissevaleur += 2 ** puissance
            puissance -= 1
        return str(signe*mantissevaleur*2**exposantdec)

#fonctions de conversion

def randomBase(): #retourne une liste de conversion où le premier élément est la baseA, la deuxième la baseB s'il y a un troisième le nombre de bits
    bases = [2, 8, 10, 16]
    complementa2 = ['decimal', 'C2']
    Ieee754 = ['decimal', 'IEEE754']
    conversions = [bases, complementa2, Ieee754]
    bitC2 = [8, 16]
    bitIeee754 = [32, 64]
    typeconversion = random.choices(conversions, weights=[0.5, 0.25, 0.25], k=1)
    listeconversion = random.sample(typeconversion[0], 2)
    if typeconversion[0] == bases: #traduction des type de conversions qui étaient des listes
        typeconversionstr = 'bases'
    elif typeconversion[0] == complementa2:
        typeconversionstr = 'C2'
        bit = random.choice(bitC2)
        listeconversion.append(bit)
    elif typeconversion[0] == Ieee754:
        typeconversionstr = 'IEEE754'
        bit = random.choice(bitIeee754)
        listeconversion.append(bit)
    return listeconversion, typeconversionstr

def randomEnonce(typeconversion, base, bit=None): #retourne un nombre au hasard dont on doit en faire la conversion
    #les deux premiers arguments en str, à part s'il s'agit dans un changement de base où la base sera en int (2, 8, 10 ou 16) #base = base de la bonne reponse
    #le troisième argument est nécessaire lorsque le type de conversion est 'C2' ou 'IEEE754', il sera en int
    if typeconversion == 'bases': #le choix aléatoire de l'énoncé se fait en décimal pour un changement de base, les conversions seront faites suivant la base initiale
        randomintervalle = random.randint(1,4)
        if randomintervalle == 1: #il y a relativement plus de chances que cela tombe sur un nombre entre 100 et 1000, le domaine le plus large est entre 1 et 10000
            nombrenonce = random.randint(100, 1000)
        elif randomintervalle == 2:
            nombrenonce = random.randint(10, 1000)
        elif randomintervalle == 3:
            nombrenonce = random.randint(1, 1000)
        elif randomintervalle == 4:
            nombrenonce = random.randint(1, 10000)
        if base != 10:
            nombrenonce = convBase(str(nombrenonce), 10, base)
        else:
            nombrenonce = str(nombrenonce)
    elif typeconversion == 'C2':
        if bit == 8: #pour éviter les dépassement suivant le nombre de bit
            nombrenonce = random.randint(-(2**(bit-1)), 2**(bit-1)-1) #un nombre possible à convertir en C2 suivant le nombre de bits
        elif bit == 16:
            randomintervalle = random.randint(1,5)
            if randomintervalle != 5:
                nombrenonce = random.randint(-1000, 1000) #la majorité des cas, on tombera sur un nombre entre -1000 et 1000 en 16 bits
            elif randomintervalle == 5: #il se peut qu'on ait des nombres plus grands ou plus petits (1 chance sur 5)
                nombrenonce = random.randint(-(2**(bit-1)), 2**(bit-1)-1)
        if base == 'C2':
            nombrenonce = convC2(str(nombrenonce), 'decimal', bit)
        else:
            nombrenonce = str(nombrenonce)
    elif typeconversion == 'IEEE754':
        randomintervalle = random.randint(1,4)
        if randomintervalle == 1: #randomisation de la partie entière
            nombrenonceint = random.randint(100, 1000)
        elif randomintervalle == 2:
            nombrenonceint = random.randint(10, 1000)
        elif randomintervalle == 3:
            nombrenonceint = random.randint(1, 1000)
        elif randomintervalle == 4:
            nombrenonceint = random.randint(1, 10000)
        nombrenoncefloat = 0 #randomisation de la partie flottante
        if bit == 32: #ajout de puissance négative de 2 dépend du nombre de bit
            finrange = 10
        elif bit == 64:
            finrange = 16
        bouclecasse = False
        for ipuissance in range(1, finrange):
            if not bouclecasse:
                unechancesurtrois = random.randint(1,3)
                if unechancesurtrois in [2,3]: #deux chances sur trois qu'on ajoute un bit du poids de ipuissance
                    nombrenoncefloat += 2**-ipuissance
                    if unechancesurtrois == 3: #on arrête l'ajout une chance sur 3 définitivement
                        bouclecasse = True
        nombrenonce = nombrenonceint + nombrenoncefloat
        if base == 'IEEE754':
            nombrenonce = convIEEE754(str(nombrenonce), 'decimal', bit)
        else:
            nombrenonce = str(nombrenonce)
    return nombrenonce

def randomReponses(bonnereponse, typeconversion, base, bit=None): #retourne une liste de quatres choix de réponses dont une réponse vraie, et l'index de la bonne réponse dans la liste, le tout sous forme de tuple
    #les trois premiers arguments en str, à part s'il s'agit dans un changement de base où la base sera en int (2, 8, 10 ou 16) #base = base de la bonne reponse
    #le quatrième argument est nécessaire lorsque le type de conversion est 'C2' ou 'IEEE754', il sera en int
    listereponses = [bonnereponse]
    if typeconversion == 'bases':
        if base != 10:
            nombredecimal = int(convBase(bonnereponse, base, 10)) #conversion en décimal pour appliquer l'algorithme à la fois pour toutes les bases
        elif base == 10:
            nombredecimal = int(bonnereponse)
        for i in range(3):
            mauvaisereponse = -1 #pour activer la boucle
            while mauvaisereponse < 0 or convBase(str(mauvaisereponse), 10, base) in listereponses or str(mauvaisereponse) in listereponses: #éviter les nombres négatifs en réponse pour des conversions de bases et les doublons de reponses
                randomindexalgo = random.randint(1,3) #algorithme aléatoire
                if randomindexalgo == 1: #algorithme pour générer une mauvaise réponse proche de la bonne
                    mauvaisereponse = nombredecimal + random.randint(-5, 5)
                elif randomindexalgo == 2: #moins proche
                    mauvaisereponse = nombredecimal + random.randint(-25, 25)
                elif randomindexalgo == 3: #mauvaise réponse plus évidente
                    mauvaisereponse = nombredecimal + random.randint(-100, 100)
            if base != 10:
                listereponses.append(convBase(str(mauvaisereponse), 10, base))
            elif base == 10:
                listereponses.append(str(mauvaisereponse))
    elif typeconversion == 'C2':
        if base == 'C2':
            nombredecimal = int(convC2(bonnereponse, base, bit))
        elif base == 'decimal':
            nombredecimal = int(bonnereponse)
        listetemporaire = [nombredecimal] #copie de la liste pour une liste temporaire
        for _ in range(3):
            mauvaisereponse = nombredecimal #pour activer la boucle
            while str(mauvaisereponse) in listereponses or mauvaisereponse in listetemporaire or mauvaisereponse < -(2**(bit-1)) or mauvaisereponse >= 2**(bit-1): #éviter les nombres négatifs en réponse pour des conversions de bases et les doublons de reponses
                randomindexalgo = random.randint(1,3) #algorithme aléatoire
                if randomindexalgo == 1: #algorithme pour générer une mauvaise réponse proche de la bonne
                    mauvaisereponse = nombredecimal + random.randint(-5, 5)
                elif randomindexalgo == 2: #moins proche
                    mauvaisereponse = nombredecimal + random.randint(-25, 25)
                elif randomindexalgo == 3: #mauvaise réponse plus évidente
                    mauvaisereponse = nombredecimal + random.randint(-100, 100)
            listetemporaire.append(mauvaisereponse) #éviter les doublons lorsque le nombre n'est pas en decimal, il n'est donc pas nécessaire de le convertir
            if base == 'C2':
                listereponses.append(convC2(str(mauvaisereponse), 'decimal', bit))
            elif base == 'decimal':
                listereponses.append(str(mauvaisereponse))
    elif typeconversion == 'IEEE754':
        if base == 'IEEE754':
            nombreIEEE754 = str(bonnereponse)
        elif base == 'decimal':
            nombreIEEE754 = convIEEE754(bonnereponse, 'decimal', bit)
        algo1utilise = False
        listetemporaire = [nombreIEEE754] #copie de la liste pour une liste temporaire
        for _ in range(3):
            mauvaisereponse = bonnereponse #pour activer la boucle
            while mauvaisereponse in listereponses or mauvaisereponse in listetemporaire:
                randomindexalgo = random.randint(1,4) #algorithme aléatoire
                mauvaisereponse = list(nombreIEEE754)
                if randomindexalgo == 1 and not algo1utilise: #faute de signe
                    if nombreIEEE754[0] == '0':
                        mauvaisereponse[0] = '1'
                    elif nombreIEEE754[0] == '1':
                        mauvaisereponse[0] = '0'
                    algo1utilise = True #éviter une répétition d'algorithme
                else:
                    if bit == 32: #modification des bits des mauvaises réponses différente suivant le nombre de bits pour ne pas avoir de réponses trop différentes
                        debutrange = 5
                        finrange = 16
                    if bit == 64:
                        debutrange = 8
                        finrange = 19
                    for ibit in range(debutrange,finrange):
                        randomindexalgobis = random.randint(1,4)
                        if randomindexalgobis == 1: #changement de certains bits de l'exposant et de certains bits de la mantisse parmi les premiers de la mantisse
                            if nombreIEEE754[ibit] == '0':
                                mauvaisereponse[ibit] = '1'
                            elif nombreIEEE754[ibit] == '1':
                                mauvaisereponse[ibit] = '0'
                mauvaisereponse = "".join(mauvaisereponse)
            listetemporaire.append(mauvaisereponse) #éviter les doublons lorsque le nombre n'est pas en IEEE754, il n'est donc pas nécessaire de le convertir
            if base == 'IEEE754':
                listereponses.append(mauvaisereponse)
            elif base == 'decimal':
                mauvaisereponse = convIEEE754(mauvaisereponse, 'IEEE754', bit)
                virguleatteinte = False
                chiffrevirgule = 0
                for ichiffre in bonnereponse: #il doit avoir autant de chiffres après la virgule dans la mauvaise réponse que dans la bonne
                    if virguleatteinte:
                        chiffrevirgule += 1
                    if ichiffre == '.':
                        virguleatteinte = True
                listereponses.append(str(round(float(mauvaisereponse), ndigits=chiffrevirgule)))
    random.shuffle(listereponses) #on mélange la liste des choix de réponses pour que la bonne réponse puisse se retrouver dans n'importe quelle position
    indexbonnereponse = listereponses.index(bonnereponse) #récupère le numéro de la bonne réponse parmi les choix de réponses
    return listereponses, indexbonnereponse

#Fonction affichage des questions

def afficherQCM(question, reponses, numero, numeroquestion): #affiche un question d'un QCM
    #question en str: La question à afficher.
    #reponses en list: Liste des 4 réponses possibles.
    #numero int: Index de la bonne réponse dans la liste des réponses.
    #numero question en int: numéro de la question

    #dimensions de la fenêtre
    largeur = 1000
    hauteur = 600
    #création de la fenêtre et du canvas
    fenetreQCM = tkinter.Tk()
    fenetreQCM.title(f"Question {numeroquestion} :")
    canevas = tkinter.Canvas(fenetreQCM, width=largeur, height=hauteur)
    canevas.pack()
    titre = f"Question {numeroquestion}"
    canevas.create_text(largeur/2, 30, text=titre, anchor='center', font=('Arial', 20, 'bold'), fill="blue")
    #affichage de la question et des réponses en bouton
    canevas.create_text(largeur/2, 100, text=question, anchor='center', font=('Arial', 16), width=650)
    x_reponse, y_reponse, espacement = largeur/2, 170, 60
    resultat = [None]
    reponsedonnee = [False]  #indication de l'état de la réponse (vraie ou fausse)
    boutons = []
    #commandes de chacun des boutons pour faciliter les commandes
    def bouton0():
        afficherResultat(0)
    def bouton1():
        afficherResultat(1)
    def bouton2():
        afficherResultat(2)
    def bouton3():
        afficherResultat(3)
    def afficherResultat(index): #afficher le résultat d'une réponse en fonction du numéro du bouton de la bonne réponse
        if not reponsedonnee[0]:  #pour voir si une réponse a déjà été donnée
            reponsedonnee[0] = True #le bouton a déjà été enclenché
            if index == numero: #Si le numéro de la réponse choisie est celle de la bonne réponse
                canevas.create_text(largeur/2, hauteur-100, text="Bonne réponse !", fill="green", font=('Arial', 16), anchor='center')
                resultat[0]  = True
                #"Bonne réponse !"
            else:
                canevas.create_text(largeur/2, hauteur-100, text="Mauvaise réponse.", fill="red", font=('Arial', 16), anchor='center')
                resultat[0] = False
                #"Mauvaise réponse."
            #désactiver les boutons après une sélection
            for ibouton in boutons:
                ibouton.config(state='disabled') #désactiver le bouton
            #affichage du bouton "suivant" pour passer à la question suivante ou aux résultats du QCM, en pratique elle va fermer la fenêtre
            boutonsuivant = tkinter.Button(fenetreQCM, text="Suivant", font=('Arial', 14), width=20, height=2, command=fenetreQCM.destroy)
            canevas.create_window(largeur / 2, hauteur - 50, window=boutonsuivant, anchor='center')
    gestionboutons = [bouton0, bouton1, bouton2, bouton3]
    for i in range(len(reponses)): #affichage des boutons
        bouton = tkinter.Button(fenetreQCM,text=reponses[i],font=('Arial', 14),width=80,height=2,command=gestionboutons[i])
        canevas.create_window(x_reponse,y_reponse + i*espacement,window=bouton,anchor='center')
        boutons.append(bouton) # ajoute ce bouton à la liste des boutons

    fenetreQCM.mainloop() #Lancement de la fenêtre
    return resultat[0] #retourne True si la bonne réponse a été donnée ou False si mauvaise réponse ou fermeture de la fenêtre

#Fonctions principales

def fabriquer(): #fonction permettant de fabriquer ou d'essayer un QCM

    def afficher_page_creer():
        questions = []
        #fenêtre principale
        fenetre_creer = tkinter.Tk()
        fenetre_creer.title("Création de QCM")
        #label pour guider l'utilisateur, sert à placer du texte figé dans une fenetre
        label_instruction = tkinter.Label(fenetre_creer, text="Sélectionnez les informations pour chaque question.")
        label_instruction.pack()
        #variables pour stocker les entrées de l'utilisateur
        type_base_var = tkinter.StringVar(value="Changements de base") #Valeur par défaut (arbitraire) : changements de base
        base_init_var = tkinter.StringVar()
        base_finale_var = tkinter.StringVar()
        bits_var = tkinter.StringVar()

        #fonction pour créer une question #assez libre peu de vérification jugée inutile car c'est l'utilisateur qui doit veiller à la logique de la question
        def creer_question():
            #récupération explicite des données saisies
            type_base = type_base_var.get()
            base_init = base_init_var.get()
            base_finale = base_finale_var.get()
            bits = bits_var.get()
            #validation du numéro de la bonne réponse
            nombre = simpledialog.askstring("Nombre à convertir", f"Entrez le nombre à convertir :") #affiche une petite fenetre ou on peut rentrer un str ici un nombre à convertir
            #saisie des choix de réponse
            choix = []
            for i in range(4): #Choisir les quatres réponses possibles
                choix_reponse = simpledialog.askstring("Choix de réponse", f"Entrez le choix de réponse {i}:")
                if choix_reponse:
                    choix.append(choix_reponse)
                else:
                    messagebox.showerror("Erreur", "Tous les choix doivent être remplis.") #En cas d'entrée vide
                    return

            while True: #boucle permettant d'assurer la validité du numéro bonne réponse (compris entre 0 et 3)
                numero_bonne_reponse = simpledialog.askstring("Bonne réponse", "Entrez le numéro de la bonne réponse (entre 0 et 3):")
                if numero_bonne_reponse and numero_bonne_reponse.isdigit() and 0 <= int(numero_bonne_reponse) <= 3: #is digit -> vérifie que ce sont des chiffres
                    numero_bonne_reponse = int(numero_bonne_reponse)
                    break
                else:
                    messagebox.showerror("Erreur", "Le numéro de la bonne réponse doit être un chiffre entre 0 et 3.") #Message d'erreur si invalide, redemande l'entrée ensuite
            #création de l'énoncé
            if type_base == "Changements de base": #Détermine l'énoncé pour le changement de base d'une base initiale à une base finale
                enonce = f"Convertir {nombre} de {base_init} en {base_finale}."
            elif type_base in ["C2", "IEEE754"]: #Pour le C2/IEEE754, l'énoncé donnera le nombre de la base initiale, la base finale est implicite mais c'est juste l'autre, avec le nombre de bits
                enonce = f"Convertir {nombre} qui est en {base_init} en {bits} bits ({type_base})."
            #ajout des informations à la liste des questions
            questions.append([enonce, choix, numero_bonne_reponse])
            #passage à la question suivante ou fin
            if len(questions) < 10: #les 10 questions ne sont pas atteintes
                label_instruction.config(text=f"Question {len(questions) + 1}/10 : Remplissez les informations.") #demande les infos de question
            else: #les info des 10 questions ont été entrées
                boucle_erreur = True
                messagebox.showinfo("Terminé", "Vous avez créé les 10 questions !") #message qui informe l'utilisateur qu'il a entré les 10 questions
                while boucle_erreur: #boucle pour assurer la validité du fichier texte à créer
                    nom_fichier = simpledialog.askstring("Fichier", f"Entrez le titre du nouveau fichier :") #demande le nom du fichier, l'extension '.txt' est obligatoire
                    try: #gestion d'une potentielle erreur de fichier
                        with open(nom_fichier, 'w'): #Crée un fichier texte à l'emplacement du fichier source
                            pass
                    except (OSError, IOError): #s'il y a un problème de fichier, un message d'erreur s'affiche, il y apossibilité de rerentrer le fichier
                        messagebox.showerror("Erreur", "Le nom du fichier n'est pas valide.")
                    else: #fin de la boucle
                        boucle_erreur = False
                for iquestion in questions: #stockage des infos des questions
                    with open(nom_fichier, 'a') as fichier_QCM: #ouverture du fichier en mode ajout de données #une question = 6 lignes d'écriture
                        fichier_QCM.write(f"{iquestion[0]}\n") #enregistre en première ligne l'énoncé #ne pas oublier le saut de ligne
                        for ichoixreponse in iquestion[1]: #les quatres prochaines lignes comporteront les choix de réponse
                            fichier_QCM.write(f"{ichoixreponse}\n")
                        fichier_QCM.write(f"{iquestion[2]}\n") #la sixième comportera le numéro de la bonne réponse
                messagebox.showinfo("Fichier", "Informations du QCM enregistrés.") #message informant que les info ont été enregistrées
                fenetre_creer.quit()

        #widgets pour les informations sous forme de menu options (dans la même fenetre)
        #type de conversion
        tkinter.Label(fenetre_creer, text="Type de conversion :").pack()
        tkinter.OptionMenu(fenetre_creer, type_base_var, "Changements de base", "C2", "IEEE754").pack()
        #base initiale
        tkinter.Label(fenetre_creer, text="Base initiale :").pack()
        tkinter.OptionMenu(fenetre_creer, base_init_var, "Binaire", "Octal", "Décimal", "Hexadécimal", "C2", "IEEE754").pack()
        #base finale nécessaire que pour les changements de base
        tkinter.Label(fenetre_creer, text="Base finale (si nécessaire) :").pack()
        tkinter.OptionMenu(fenetre_creer, base_finale_var, "Binaire", "Octal", "Décimal", "Hexadécimal").pack()
        #nombre de bits nécessaire pour C2 et IEEE754
        tkinter.Label(fenetre_creer, text="Nombre de bits (si nécessaire) :").pack()
        tkinter.OptionMenu(fenetre_creer, bits_var, "8", "16", "32", "64").pack()
        #bouton pour valider la question
        tkinter.Button(fenetre_creer, text="Valider cette question", command=creer_question).pack()

        fenetre_creer.mainloop() #lancement de la fenetre créer


    def afficher_essayer(): #affiche une nouvelle fenêtre avec le titre 'Essayer'
        boucle_erreur = True
        while boucle_erreur: #assure que le nom de fichier est valide
            nom_fichier = simpledialog.askstring("Fichier", "Entrez le titre du fichier :") #interface pour entrer le nom du fichier AVEC l'extension
            try:
                with open(nom_fichier, 'r'): #test ouverture en mode lecture
                    pass
            except (OSError, IOError): #s'il y a une erreur, un message d'erreur apparaîtra, vous pourrez ensuite rerentrer le nom
                messagebox.showerror("Erreur", "Le nom du fichier n'est pas valide.")
            else:
                boucle_erreur = False #fin de la boucle, titre du fichier validé
                messagebox.showinfo("Fichier", "Le fichier a bien été importé.")
        liste_questions = []
        with open(nom_fichier, 'r') as fichier_QCM:
            for i in range(10): #lis et enregistre les lignes (6 par 6 pour chaque question 10 fois)
                question = fichier_QCM.readline() #1ere ligne du groupe info question d'une question
                liste_choix_reponses = []
                for _ in range(4): #lis et enregistre les quatres choix de réponse après
                    liste_choix_reponses.append(fichier_QCM.readline())
                numero_bonne_reponse = int(fichier_QCM.readline()) #lis et enregistre le numéro de la bonne réponse
                info_question = [question, liste_choix_reponses, numero_bonne_reponse] #prends toutes les info d'une question dans une liste
                liste_questions.append(info_question) #ajoute le groupe d'un infos d'une question dans la liste des questions

        score = 0
        for numeroquestion in range(1, 11): #affiche les 10 questions du QCM
            info_question = liste_questions[numeroquestion-1]
            question = info_question[0]
            liste_choix_reponses = info_question[1]
            numero_bonne_reponse = info_question[2]
            scorequestion = afficherQCM(question, liste_choix_reponses, numero_bonne_reponse, numeroquestion)
            if scorequestion: #si bonne réponse donnée, un point en +
                score += 1
        #affichage du score final
        fenetrescore = tkinter.Toplevel()
        fenetrescore.title("Score")
        largeur, hauteur = 300, 200
        canevas = tkinter.Canvas(fenetrescore, width=largeur, height=hauteur)
        canevas.pack()
        canevas.create_text(largeur / 2, 50, text="Score", font=("Arial", 24, "bold"), fill="blue", anchor="center")
        canevas.create_text(largeur / 2, 100, text=f"{score} / 10", font=("Arial", 18), fill="black", anchor="center")
        bouton_fermer = tkinter.Button(fenetrescore, text="Fermer", font=("Arial", 14), command=fenetrescore.destroy)
        canevas.create_window(largeur / 2, 150, window=bouton_fermer, anchor="center")
        fenetrescore.mainloop()

    #dimensions de la fenêtre
    largeur, hauteur = 800, 400
    #création de la fenêtre principale
    fenetre_fabriquer = tkinter.Tk()
    fenetre_fabriquer.title("Fabriquer un QCM")
    canevas = tkinter.Canvas(fenetre_fabriquer, width=largeur, height=hauteur)
    canevas.pack()
    canevas.create_text(largeur / 2, 50, text="Fabrication d'un QCM", font=("Arial", 24, "bold"), fill="blue", anchor="center") #titre de l'interface
    #bouton "Créer"
    bouton_creer = tkinter.Button(fenetre_fabriquer, text="Créer", font=("Arial", 14), width=20, height=2, command=afficher_page_creer)
    canevas.create_window(largeur / 2, 150, window=bouton_creer, anchor="center")
    #bouton "Essayer"
    bouton_essayer = tkinter.Button(fenetre_fabriquer, text="Essayer", font=("Arial", 14), width=20, height=2, command=afficher_essayer)
    canevas.create_window(largeur / 2, 220, window=bouton_essayer, anchor="center")

    fenetre_fabriquer.mainloop() #lancement de la fenetre principale

def aleatoire(): #fonction appelée lorsqu'on clique sur 'Aléatoire' #génère dix questions aléatoire
    fenetre.destroy()
    score = 0
    for numeroquestion in range(1, 11):
        #génération des questions aléatoires
        basealeatoire = randomBase() #base aléatoire
        conversionbaseA, conversionbaseB = basealeatoire[0][0], basealeatoire[0][1] #récupérations des changements de bases demandés
        typeconversion = basealeatoire[1] #typeconversion
        if typeconversion in 'C2IEEE754': #pour une question sur la C2 / l'IEEE754
            bit = basealeatoire[0][2]
            enonce = randomEnonce(typeconversion, conversionbaseA, bit) #génère un nombre à convertir au hasard
            if typeconversion == 'C2': #convertit le nombre énoncé en fonction de la question pour donner la bonne réponse dans l
                bonnereponse = convC2(enonce, conversionbaseA, bit) #conversion C2
            if typeconversion == 'IEEE754':
                bonnereponse = convIEEE754(enonce, conversionbaseA, bit) #conversion IEEE754
            inforeponses = randomReponses(bonnereponse, typeconversion, conversionbaseB, bit) #génère des choix de réponses aléatoires
        else:
            enonce = randomEnonce(typeconversion, conversionbaseA) #génère un nombre à convertir au hasard
            bonnereponse = convBase(enonce, conversionbaseA, conversionbaseB) #convertit le nombre énoncé en fonction de la question pour donner la bonne réponse
            inforeponses = randomReponses(bonnereponse, typeconversion, conversionbaseB) #génère des choix de réponses aléatoires
        listechoix = inforeponses[0]
        indexbonnereponse = inforeponses[1]
        if typeconversion in 'C2IEEE754':
            question = f"Quel est la conversion de {enonce} en {typeconversion} en {bit} ?" #mise en phrase de l'énoncé
        else:
            question = f"Quel est la conversion de {enonce} de la base {conversionbaseA} en base {conversionbaseB} ?" #mise en phrase de l'énoncé
        scorequestion = afficherQCM(question, listechoix, indexbonnereponse, numeroquestion) #affiche cette question du QCM
        if scorequestion: #même systeme de score que dans la fonction afficher_essayer
            score += 1
    # Affichage du score final
    fenetrescore = tkinter.Toplevel()
    fenetrescore.title("Score")
    largeur, hauteur = 300, 200

    canevas = tkinter.Canvas(fenetrescore, width=largeur, height=hauteur)
    canevas.pack()
    canevas.create_text(largeur / 2, 50, text="Score", font=("Arial", 24, "bold"), fill="blue", anchor="center")
    canevas.create_text(largeur / 2, 100, text=f"{score} / 10", font=("Arial", 18), fill="black", anchor="center")
    bouton_fermer = tkinter.Button(fenetrescore, text="Fermer", font=("Arial", 14), command=fenetrescore.destroy)
    canevas.create_window(largeur / 2, 150, window=bouton_fermer, anchor="center")
    fenetrescore.mainloop()


def main(): #affiche une interface de bienvenue avec deux boutons
    global fenetre
    #dimensions de la fenêtre
    largeur = 800
    hauteur = 400
    #création de la fenêtre et du canevas
    fenetre = tkinter.Tk()
    fenetre.title("Bienvenue au QCM")
    canevas = tkinter.Canvas(fenetre, width=largeur, height=hauteur)
    canevas.pack()
    canevas.create_text(largeur / 2, 50, text="Bienvenue dans l'application QCM", anchor='center', font=('Arial', 24, 'bold'), fill="blue") #Titre
    canevas.create_text(largeur / 2, 120, text="Choisissez une option pour commencer :", anchor='center', font=('Arial', 16))
    #boutons des options
    bouton_fabriquer = tkinter.Button(fenetre, text="Fabriquer", font=('Arial', 14), width=20, height=2, command=fabriquer)
    bouton_aleatoire = tkinter.Button(fenetre, text="Aléatoire", font=('Arial', 14), width=20, height=2, command=aleatoire)
    canevas.create_window(largeur / 2, 200, window=bouton_fabriquer, anchor='center')
    canevas.create_window(largeur / 2, 270, window=bouton_aleatoire, anchor='center')
    fenetre.mainloop() #lancement de la boucle principale

main() #lancement du programme