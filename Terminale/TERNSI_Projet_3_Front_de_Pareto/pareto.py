#pareto.py

import matplotlib.pyplot as plt

#lecture des points depuis un fichier
def lirePoints(nomfichier):
    L = []
    with open(nomfichier, 'r') as file:
        n = int(file.readline().rstrip())
        for line in file.readlines():
            x, y = line.rstrip().split(',')
            L.append((int(x), int(y)))
    return L


#fonctions de base

def fusion(liste1,liste2):
    """
    fusionne deux listes de points déjà triées selon (x, y)
    """
    liste_fusionnee = []
    i = 0
    j = 0

    while i < len(liste1) and j < len(liste2):
        #comparaison sur x puis y
        if (liste1[i][0] < liste2[j][0]) or (liste1[i][0] == liste2[j][0] and liste1[i][1] <= liste2[j][1]):
            liste_fusionnee.append(liste1[i])
            i += 1
        else:
            liste_fusionnee.append(liste2[j])
            j += 1

    #ajout des éléments restants
    liste_fusionnee.extend(liste1[i:])
    liste_fusionnee.extend(liste2[j:])

    return liste_fusionnee


def tri_fusion(points):
    """
    trie une liste de points selon l'abscisse puis l'ordonnée (diviser pour régner)
    """
    if len(points) <= 1:
        return points
    m = len(points) // 2
    gauche = tri_fusion(points[:m])
    droite = tri_fusion(points[m:])
    return fusion(gauche, droite)

def trier_points(S):
    """
    trie les points selon x puis y à l'aide d'un tri fusion
    """
    return tri_fusion(S)

def domine(p1, p2):
    """
    return True si p1 domine p2
    p1 domine p2 <=> x1 > x2 et y1 > y2
    """
    return p1[0] > p2[0] and p1[1] > p2[1]


#algorithme Diviser pour Régner (squelette)

def epm(S):
    """
    calcule l'ensemble des points maximaux (front de Pareto)
    en diviser pour régner
    """
    n = len(S) #nb de points dans l'ensemble S

    #cas de base, ce point est forcément maximal si l'ensemble contient 0 ou 1 point
    if n <= 1:
        return S.copy()

    #découpage
    m = n // 2
    SL = S[:m] #sous ensemble gauche
    SR = S[m:] #sous ensemble droit

    #appels récursifs sur chaque sous ensembles
    epm_L = epm(SL)
    epm_R = epm(SR)

    #point t : point de epm_R avec le plus petit x
    t = min(epm_R, key=lambda p: p[0]) #point ayat la plus petite abscisse

    #filtrage de epm_L (on supprime ceux qui sont dominés par le point t)
    epm_L_filtre = []
    for p in epm_L:
        if not domine(t, p):
            epm_L_filtre.append(p)

    #fusion finale des deux ensembles de points maximaux
    return epm_L_filtre + epm_R

def afficher_front(points,front,nom_fichier):
    '''
    affiche les points et le front de Pareto pour un fichier donné
    '''
    x_points = [p[0] for p in points]
    y_points = [p[1] for p in points]

    x_front = [p[0] for p in front]
    y_front = [p[1] for p in front]

    plt.figure() #création d'une nouvelle figure pr l'affichage
    plt.scatter(x_points, y_points, label="Points") #affichage des points normaux
    plt.scatter(x_front, y_front, label="Front de Pareto") #affichage des points max (front de pareto)
    plt.xlabel("x") #etiquette des axes
    plt.ylabel("y")
    plt.title(f"Front de Pareto - {nom_fichier}") #insertion du titre du graphique
    plt.legend() #affichage de la légende
    plt.show() #affichage final de la figure 

#programme principal
if __name__ == "__main__":
    fichiers = ["data1.txt","data2.txt","data3.txt"] 
    for nom in fichiers:
        print("Traitement de", nom)
        points = lirePoints(nom)
        points = trier_points(points)
        front = epm(points) #calcul des points maximum (front de pareto)
        print("Nombre de points maximaux :", len(front))
        afficher_front(points,front,nom)
