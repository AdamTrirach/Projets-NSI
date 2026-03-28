class ArbreBinaire:
    def __init__(self, valeur): #constructeur
        self.valeur = valeur
        self.enfant_gauche = None
        self.enfant_droit = None

    def insert_gauche(self, valeur): 
        if self.enfant_gauche == None:
            self.enfant_gauche = ArbreBinaire(valeur)
        else:
            new_node = ArbreBinaire(valeur)
            new_node.enfant_gauche = self.enfant_gauche
            self.enfant_gauche = new_node

    def insert_droit(self, valeur):
        if self.enfant_droit == None:
            self.enfant_droit = ArbreBinaire(valeur)
        else:
            new_node = ArbreBinaire(valeur)
            new_node.enfant_droit = self.enfant_droit
            self.enfant_droit = new_node
    
    def get_valeur(self): #getter
        return self.valeur

    def get_gauche(self): #getter
        return self.enfant_gauche

    def get_droit(self): #getter
        return self.enfant_droit

    def estFeuille(self): 
        if not self.enfant_gauche and not self.enfant_droit:
            return True
        else:
            return False
    
# --- fin de la classe --- #

# =============================================================================
# Représentation graphique
# =============================================================================
from tkinter import *
from math import *

# ------------------- cercle-------------------#
def cercle(canv,x,y,r,col,colf):
    """dessine un cercle graphique sur le canvas de centre (x,y) de rayon r de
    couleur col et de couleur de fond colf"""
    canv.create_oval(x-r,y-r,x+r,y+r,outline=col, fill=colf)
# ------------------- dessinenoeud-------------------#
def dessinenoeud(canv,x,y,r,noeud):
    """ dessine un noeud graphique : un cercle rempli avec la valeur du noeud"""
    cercle(canv,x,y,r,"black","white")
    canv.create_text(x,y,text=noeud.valeur,fill="black")
# ------------------- centresuivant-------------------#
def centresuivant(x,y,r,m,dir,ouverture):
    # ouverture permet d'ajuster l'angle d'ouverture des noeuds
    """ calcule la position de noeud suivant :
        on calcule a et b les décalages par rapport à la position actuelle x,y
        dir permet de spécifier:
        si c'est un fils gauche on retranche le a
        si c'est un fils droit on ajoute le a à x
        pour y on ajoute toujours b dans les deux cas.
        m la distance entre les cercles : le nœud et ses descendants.
    """
    a=(2*r+m)*sin(pi/(ouverture)) # calcule le décalage sur l'axe des x : coordonnées polaire vers
    # cordonnées cartésiennes
    b=(2*r+m)*cos(pi/(ouverture)) # de même pour le décalage sur y. l'angle d'ouverture est 45 ° pour ouverture = 4
    if dir=="l": # dir pour left ou right c.à.d. fils gauche ou fils droit
        x1,y1=x-a,y+b # on décale vers la gauche donc on retranche a de x et
        # on ajoute b à y on descend vers le bas
    else:
        x1,y1=x+a,y+b # on décale vers la droite donc on ajoute a à x
    ouverture += 3 # en augmentant ouverture, on diminue l'angle pour la ligne suivante
    return x1,y1,ouverture
# ------------------- tracearbre-------------------#
def tracearbre(canv,x,y,r,m,noeud,ouverture):
    """ trace l'arbre graphique récursivement"""
    pas = 40 # pas ajustable permettant de réduire la distance entre les noeuds
    # pour éviter que des noeuds se superposent
    if noeud.estFeuille()==False: # si le noeud n'est pas une feuille
        if noeud.enfant_droit==None and noeud.enfant_gauche!=None : # s'il a un fils gauche mais pas de fils droit
            x1,y1,ouverture=centresuivant(x,y,r,m,"l",ouverture) # récupération de la position du noeud fils
            canv.create_line(x,y,x1,y1,fill="black") # tracé d'une droite entre x,y et x1,y1
            # cette fonction est dans la bibilothèque tkinter
            tracearbre(canv,x1,y1,r,m-pas,noeud.enfant_gauche,ouverture) # appel récursif pour traiter ce fils
        elif noeud.enfant_droit!=None and noeud.enfant_gauche==None : # s'il a un fils droit mais pas de fils gauche
            x1,y1,ouverture=centresuivant(x,y,r,m,"r",ouverture) # récupération de la position du noeud fils
            canv.create_line(x,y,x1,y1,fill="black") # tracé d'une droite entre x,y et x1,y1
            tracearbre(canv,x1,y1,r,m-pas,noeud.enfant_droit,ouverture) # appel récursif pour traiter ce fils
        else: # si il a un fils gauche et un fils droit
            x1,y1,ouverture=centresuivant(x,y,r,m,"l",ouverture) # récupération de la position du noeud fils gauche
            canv.create_line(x,y,x1,y1,fill="black") # tracé d'une droite entre x,y et x1,y1
            tracearbre(canv,x1,y1,r,m-pas,noeud.enfant_gauche,ouverture) # appel récursif pour traiter ce fils gauche
            x1,y1,ouverture=centresuivant(x,y,r,m,"r",ouverture-3) # récupération de la position du noeud fils droit
            # ouverture-3 pour compenser sur le noeud de droite
            # le +=3 dans centresuivant déjà appliqué
            canv.create_line(x,y,x1,y1,fill="black") # tracé d'une droite entre x,y et x1,y1
            tracearbre(canv,x1,y1,r,m-pas,noeud.enfant_droit,ouverture) # appel récursif pour traiter ce fils droit
    dessinenoeud(canv,x,y,r,noeud) # tracé du noeud courant
# ------------------- graphicarbre-------------------#
def graphicarbre(noeud):
    """ fonction de tracé graphique d'un arbre """
    cwidth=1000 # la largeur du canvas graphique
    cheight=700 # la hauteur du canvas
    couleurs=["red","green","bleu","white","black","cyan","magenta","yellow"]
    # fen est l'objet fenêtre héritée de la bibliothèque tkinter
    fen=Tk()
    # création d'un bouton avec la commande fermer(quit) attachée à la fenêtre
    btn=Button(fen, text="Quitter",command=fen.destroy)
    # placement du bouton en bas de la fenêtre
    btn.pack(side="bottom")
    # création d'un panneau dans lequel on affichera l'arbre
    pan=LabelFrame(fen)
    # placement de ce panneau en faut de la fenêtre
    pan.pack(side="top")
    # creation du canva graphique dans ce panneau
    canv=Canvas(pan,width=cwidth,height=cheight)
    # placement de ce canva en haut du panneau graphique
    canv.pack(side="top")
    # appel de la fonction de tracé graphique de l'arbre créé ci haut
    tracearbre(canv,cwidth//2,100,12,200,noeud,3)
    # actualisation de l'affichage graphique
    fen.mainloop()

# =============================================================================
# Fin Représentation graphique
# =============================================================================

# --- début de la construction de l'arbre binaire --- #

racine = ArbreBinaire('A') 
racine.insert_gauche('B')
racine.insert_droit('F')

b_node = racine.get_gauche()
b_node.insert_gauche('C')
b_node.insert_droit('D')

f_node = racine.get_droit()
f_node.insert_gauche('G')
f_node.insert_droit('H')

c_node = b_node.get_gauche()
c_node.insert_droit('E')

g_node = f_node.get_gauche()
g_node.insert_gauche('I')

h_node = f_node.get_droit()
h_node.insert_droit('J')

'''
           A
          / \ 
         B   F
        /\   /\ 
       C  D  G H
        \    /   \ 
         E  I     J
'''

# --- à faire 3 ---

graphicarbre(racine) #ce qu'elle renvoie est bien ce qui est demandé
#appuyer sur quitter pour avoir l'arbre suivant

# --- à faire 4 ---

#arbre 2

racine2 = ArbreBinaire('A')
racine2.insert_gauche('B')
racine2.insert_droit('C')

b_node2 = racine2.get_gauche()
b_node2.insert_gauche('D')
b_node2.insert_droit('E')

graphicarbre(racine2)
#appuyer sur quitter

# --- à faire 5 ---

'''
VARIABLE
T : arbre
x : noeud
DEBUT
HAUTEUR(T) :
    si T ≠ NIL :
        x ← T.racine
        renvoyer 1 + max(HAUTEUR(x.gauche), HAUTEUR(x.droit))
    sinon :
        renvoyer 0
    fin si
FIN
'''

def hauteur(T):
    '''
    T : instance de la classe ArbreBinaire
    Renvoie la hauteur de l'arbre binaire T
    '''
    if T != None:
        return 1 + max(hauteur(T.get_gauche()), hauteur(T.get_droit()))
    else:
        return 0

#test de la hauteur avec l'arbre 1
print(f"Hauteur Arbre 1 : {hauteur(racine)}") #doit renvoyer 4

#test facultatif avec l'arbre 2
print(f"Hauteur Arbre 2 : {hauteur(racine2)}") #doit renvoyer 3


# --- à faire 6 ---

'''
VARIABLE
T : arbre
x : noeud
DEBUT
TAILLE(T) :
    si T ≠ NIL :
        x ← T.racine
        renvoyer 1 + TAILLE(x.gauche) + TAILLE(x.droit)
    sinon :
        renvoyer 0
    fin si
FIN
'''

def taille(T):
    '''
    T : instance de la classe ArbreBinaire
    Renvoie la taille de l'arbre binaire T
    '''
    if T != None:
        return 1 + taille(T.get_gauche()) + taille(T.get_droit())
    else:
        return 0
    
#test de la taille avec l'arbre 1
print(f"Taille Arbre 1 : {taille(racine)}") #doit renvoyer 10

#test facultatif avec l'arbre 2
print(f"Taille Arbre 2 : {taille(racine2)}") #doit renvoyer 5


# --- à faire 7 ---

'''
VARIABLE
T : arbre
x : noeud
DEBUT
PARCOURS-INFIXE(T) :
    si T ≠ NIL :
        x ← T.racine
        PARCOURS-INFIXE(x.gauche)
        affiche x.clé
        PARCOURS-INFIXE(x.droit)
    fin si
FIN
'''

def parcours_infixe(T): #fonction adaptée pour un affichage sous forme de liste
    '''
    T : instance de la classe ArbreBinaire
    L : liste des valeurs parcourues selon le parcours infixe
    Renvoie L
    '''
    if T == None: #si arbre vide renvoyer une liste vide
        return []
    L = parcours_infixe(T.get_gauche())
    L += [T.get_valeur()]
    L += parcours_infixe(T.get_droit())
    return L 

#test du parcours infixe avec l'arbre 1
print(parcours_infixe(racine)) #doit renvoyer CEBDAIGFHJ sous forme de liste


# --- à faire 8 ---

'''
VARIABLE
T : arbre
x : noeud
DEBUT
PARCOURS-PREFIXE(T) :
    si T ≠ NIL :
        x ← T.racine
        affiche x.clé
        PARCOURS-PREFIXE(x.gauche)
        PARCOURS-PREFIXE(x.droit)
    fin si
FIN
'''

def parcours_prefixe(T):
    '''
    T : instance de la classe ArbreBinaire
    L : liste des valeurs parcourues selon le parcours préfixe
    Renvoie L
    '''
    if T == None: #si arbre vide renvoyer une liste vide
        return []
    L = [T.get_valeur()]
    L += parcours_prefixe(T.get_gauche())
    L += parcours_prefixe(T.get_droit())
    return L 

#test du parcours préfixe avec l'arbre 1
print(parcours_prefixe(racine)) #doit renvoyer ABCEDFGIHJ sous forme de liste


# --- à faire 9 ---

'''
VARIABLE
T : arbre
x : noeud
DEBUT
PARCOURS-SUFFIXE(T) :
    si T ≠ NIL :
        x ← T.racine
        PARCOURS-SUFFIXE(x.gauche)
        PARCOURS-SUFFIXE(x.droit)
        affiche x.clé
    fin si
FIN
'''

def parcours_suffixe(T):
    '''
    T : instance de la classe ArbreBinaire
    L : liste des valeurs parcourues selon le parcours suffixe
    Renvoie L
    '''
    if T == None: #si arbre vide renvoyer une liste vide
        return []
    L = parcours_suffixe(T.get_gauche())
    L += parcours_suffixe(T.get_droit())
    L += [T.get_valeur()]
    return L 

#test du parcours suffixe avec l'arbre 1
print(parcours_suffixe(racine)) #doit renvoyer ECDBIGJHFA sous forme de liste


# --- à faire 10 ---

'''
VARIABLE
T : arbre
Tg : arbre
Td : arbre
x : noeud
f : file (initialement vide)
DEBUT
PARCOURS-LARGEUR(T) :
    enfiler(T.racine, f)
    tant que f non vide :
        x ← defiler(f)
        affiche x.clé
        si x.gauche ≠ NIL :
            Tg ← x.gauche
            enfiler(Tg.racine, f)
        fin si
        si x.droit ≠ NIL :
            Td ← x.droite
            enfiler(Td.racine, f)
        fin si
    fin tant que
FIN
'''

def parcours_largeur(T):
    '''
    T : instance de la classe ArbreBinaire
    L : liste des valeurs parcourues selon le parcours en largeur
    file : liste représentant une file
    '''
    if T == None: #si arbre vide renvoyer une liste vide
        return []
    file = [T]
    L = []
    while file != []:
        node = file.pop(0) #defiler
        L.append(node.get_valeur())
        if node.get_gauche() != None:
            file.append(node.get_gauche())
        if node.get_droit() != None:
            file.append(node.get_droit())
    return L

#test du parcours en largeur avec l'arbre 1
print(parcours_largeur(racine)) #doit renvoyer ABFCDGHEIJ sous forme de liste


# --- à faire 11 ---

#arbre 3

node15 = ArbreBinaire(15)
node15.insert_gauche(6)
node15.insert_droit(18)

node6 = node15.get_gauche()
node6.insert_gauche(3)
node6.insert_droit(7)

node3 = node6.get_gauche()
node3.insert_gauche(2)
node3.insert_droit(4)

node7 = node6.get_droit()
node7.insert_droit(13)

node13 = node7.get_droit()
node13.insert_gauche(9)

node18 = node15.get_droit()
node18.insert_gauche(17)
node18.insert_droit(20)

graphicarbre(node15) #l'ABR correspond bien à celui représenté
#appuyer sur quitter


# --- à faire 12 ---

print(parcours_infixe(node15))
'''
Sortie : [2, 3, 4, 6, 7, 9, 13, 15, 17, 18, 20]
Un arbre binaire de recherche en est un si le parcours infixe de l'arbre fait apparaître des valeurs dans l'ordre croissant
Donc l'arbre 3 en est bien un
'''


#--- à faire 13 ---

'''
VARIABLE
T : arbre
x : noeud
k : entier
DEBUT
ARBRE-RECHERCHE(T,k) :
    si T == NIL :
        renvoyer faux
    fin si
    x ← T.racine
    si k == x.clé :
        renvoyer vrai
    fin si
    si k < x.clé :
        renvoyer ARBRE-RECHERCHE(x.gauche,k)
    sinon :
        renvoyer ARBRE-RECHERCHE(x.droit,k)
    fin si
FIN
'''

def arbre_recherche(T, k):
    '''
    T : instance de la classe ArbreBinaire
    k : entier recherché
    Renvoie True si k est présent dans l'arbre, sinon False
    '''
    if T == None: #si arbre vide renvoyer false
        return False
    if k == T.get_valeur():
        return True
    elif k < T.get_valeur():
        return arbre_recherche(T.get_gauche(), k)
    else:
        return arbre_recherche(T.get_droit(), k)

#test de la fonction arbre_recherche avec l'arbre 3 
#k = 13
print(arbre_recherche(node15, 13)) #doit renvoyer True
#k = 16
print(arbre_recherche(node15, 16)) #doit renvoyer False


#--- à faire 14 ---

'''
DEBUT
ARBRE-RECHERCHE-ITE(T,k) :
    x ← T.racine
    tant que x ≠ NIL faire
        si k == x.clé :
            renvoyer vrai
        fin si
        si k < x.clé :
            x ← x.gauche
        sinon :
            x ← x.droit
        fin si
    fin tant que
    renvoyer faux
FIN
'''

def arbre_recherche_ite(T, k):
    """
    T : instance de ArbreBinaire
    k : entier recherché
    Version itérative de la recherche dans un arbre binaire de recherche.
    """
    x = T
    while x is not None:
        valeur = x.get_valeur()
        if k == valeur:
            return True
        elif k < valeur:
            x = x.get_gauche()
        else:
            x = x.get_droit()
    return False

#test de la fonction arbre_recherche_ite avec l'arbre 3 
#k = 13
print(arbre_recherche_ite(node15, 13)) #doit renvoyer True
#k = 16
print(arbre_recherche_ite(node15, 16)) #doit renvoyer False


#--- à faire 15 --- 

'''
VARIABLE
T : arbre
x : noeud
y : noeud
DEBUT
ARBRE-INSERTION(T,y) :
    x ← T.racine
    tant que T ≠ NIL :
        x ← T.racine
        si y.clé < x.clé :
            T ← x.gauche
        sinon :
            T ← x.droit
        fin si
    fin tant que
    si y.clé < x.clé :
        insérer y à gauche de x
    sinon :
        insérer y à droite de x
    fin si
FIN
'''

def arbre_insertion(T, y):
    """
    T : instance de ArbreBinaire 
    y : entier à insérer dans l'arbre binaire de recherche
    """
    x = T
    noeud = None
    while x is not None:
        noeud = x
        if y < x.get_valeur():
            x = x.get_gauche()
        else:
            x = x.get_droit()
    if y < noeud.get_valeur():
        noeud.insert_gauche(y)
    else:
        noeud.insert_droit(y)
    return T


#test de la fonction arbre-insertion avec y=16
node15 = arbre_insertion(node15, 16)
graphicarbre(node15)
print(parcours_infixe(node15)) #devrait donner [2, 3, 4, 6, 7, 9, 13, 15, 16, 17, 18, 20]