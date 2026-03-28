//chemins des 10 images en rapport avec l'informatique
const imagesCartes = ["cpu", "ram", "disque", "clavier", "souris", "ecran", "serveur", "reseau", "usb", "code"];

//plateau de jeu
let cartes = [];
let premiereCarte = null; //équivalent de None en python => valeur explicitement assignés pour indiquer "vide"
let verrouillage = false; 

function melanger(tableau) {
    //algorithme de Fisher-Yates (plus d'infos sur le script "static/js/drapeaux.js")
    for (let i = tableau.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random()*(i + 1));
        [tableau[i], tableau[j]] = [tableau[j], tableau[i]];
    }}

//création du jeu
function initialiserJeu() {
    const plateau = document.getElementById("plateau") ;
    const etat =document.getElementById("etat");
    plateau.innerHTML = ""; //vide le plateau
    etat.textContent = ""; //efface le message d'état
    premiereCarte = null;
    verrouillage = false; //deverouille les interactions

    //duplique les images pour faire des paires
    cartes = [...imagesCartes, ...imagesCartes];
    //cette syntaxe crée un nouveau tableau qui combine deux liste imagesCartes
    //il ne s'agit donc pas de listes dans une liste mais de deux listes mis l'un au bout de l'autre

    //mélange les cartes
    melanger(cartes);

    //affiche les cartes sur le plateau
    cartes.forEach((nom, index) => {
        const div = document.createElement("div"); //cree un element div pour la carte
        div.classList.add("carte"); //ajoute la classe CSS
        div.dataset.nom = nom; //stocke l'id de la carte

        //cree l'image de la carte
        const img=document.createElement("img");
        img.src = `/static/img/cartes/${nom}.png`; //les images doivent être là
        img.alt = nom;

        div.appendChild(img); //assemble les elements
        div.addEventListener("click", () => retournerCarte(div));
        //ajoute l'ecouteur devenement au clic (en gros quand on clique ça execute la fonction permettant de retourner la carte)

        //ajoute la carte au plateau
        plateau.appendChild(div);
    });
}

//fonction pour retourner une carte et verifier les paires
function retournerCarte(carte) {
    if (verrouillage || carte.classList.contains("visible")) return; //Si le jeu est verrouillé ou la carte déjà visible, on ne fait rien
    //"contains('visible')" permet de voir si la classe CSS visible est appliquée à la carte

    //retourne la carte
    carte.classList.add("visible"); //ajoute la classe css

    if (!premiereCarte) { //premiere carte selectionnée
        premiereCarte = carte;
    } else {
        //deuxième carte retournée
        const deuxiemeCarte = carte;

        if (premiereCarte.dataset.nom === deuxiemeCarte.dataset.nom) { //on vérifie si les deux cartes sont les memes
            //paires identiques => rien à faire, elles restent visibles
            premiereCarte = null;
            //vérifie si toutes les cartes sont visibles (en gros on verifie si la partie est terminée)
            if (document.querySelectorAll('.carte.visible').length===20) { //querySelectorAll selectionne tous les elements du DOM correspondant à un sélecteur CSS (ici la classe visible)
                document.getElementById("etat").textContent = "Bravo ! Tu as gagné !" ; //on affiche le message de victoire
            }
        } else {
            //pas la même => on les cache après un délai
            verrouillage = true;
            setTimeout(() => { 
                premiereCarte.classList.remove("visible"); //supprime une classe css
                deuxiemeCarte.classList.remove("visible");
                premiereCarte = null;
                verrouillage = false;
            },800) ; //délai de 800 millisecondes soit 0,8 sec avant de cacher (arbitraire)
        }
    }}

//lance le jeu au chargement de la page
document.addEventListener("DOMContentLoaded",initialiserJeu) ;
