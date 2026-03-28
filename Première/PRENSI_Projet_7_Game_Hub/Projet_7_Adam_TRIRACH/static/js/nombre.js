//variables principales
let nombreMystere = 0 ; 
let tempsRestant = 30 ;
let timer = null ; //null est l'équivalent de None en python
let jeuDemarre = false ;
let jeuTermine = false ;

//initialisation de la page (affiche tout sauf le jeu)
function preparerJeu() {
    document.getElementById("saisie").value = ""; //vide le champ de saisie
    document.getElementById("saisie").disabled = true; //bloque la saisie
    document.getElementById("envoyer").disabled = true; //desactive le bouton valider
    document.getElementById("indice").textContent = ""; //efface les messages d'indice (c'est plus ou c'est moins)
    document.getElementById("message-fin").textContent = ""; //efface le message de fin
    document.getElementById("chrono").textContent = "1:00"; //affiche le chrono à 1 minute
    jeuDemarre = false;
    jeuTermine = false;
    clearInterval(timer); //arrete le timer (sécurité recommandé par l'IA)
}

//commencer une nouvelle partie
function demarrerJeu() {
    nombreMystere = Math.floor(Math.random()*10000)+1 ; //nombre généré aléatoirement entre 1 et 10000
    //math floor arrondit à l'entier inférieur ; math random génère un nombre entre 0 et 1
    tempsRestant = 60 ; //timer = 1 minute
    jeuDemarre = true; //on demarre le jeu
    jeuTermine = false;
    //activation de l'interface
    document.getElementById("saisie").value = ""; //vide la saisie
    document.getElementById("saisie").disabled = false; //active la saisie
    document.getElementById("envoyer").disabled = false; //active le bouton vamider
    document.getElementById("saisie").focus(); //focus auto sur le champ
    document.getElementById("indice").textContent = "";
    document.getElementById("message-fin").textContent = "";
    //gestion du timer
    clearInterval(timer);
    lancerChrono(); //lance le chrono
}
//chronomètre
function lancerChrono() {
    timer= setInterval(() => {
        tempsRestant--; //décrémente le temps restant à 1
        const minutes= Math.floor(tempsRestant / 60); 
        const secondes = tempsRestant % 60;
        document.getElementById("chrono").textContent = `${minutes}:${secondes.toString().padStart(2, '0')}`; //affichage minutes secondes (voir drapeaux.js)
        if (tempsRestant <= 0) { //si temps écoulé arreter la partie
            terminerJeu(false);}
    }, 1000); //set interval a faire toutes les 1000 millisecondes (soit chaque seconde)
}

//vérifie la saisie
function verifierNombre() {
    if (!jeuDemarre || jeuTermine) return; // => ne rien faire si jeu inactif
    const champ = document.getElementById("saisie"); 
    const valeur = parseInt(champ.value); //transforme le contenu saisi dans le champ en int
    const indice = document.getElementById("indice");
    champ.value = ""; //vide automatiquement le champ après chaque tentative

    if (isNaN(valeur)) { //on vérifie si la saisie est valide (normalement l'input a le type number donc ce sera pas nécessaire)
        indice.textContent = "Ce n'est pas un nombre valide.";
        return;}

    if (valeur<nombreMystere){ //on compare la valeur entrée avec le nombre mystère (énoncé)
        indice.textContent= "🔼 C’est plus !";
    } else if (valeur>nombreMystere) {
        indice.textContent = "🔽 C’est moins !";
    } else { //si le nombre est deviné on termine la partie
        terminerJeu(true);
    }
}

//fin du jeu
function terminerJeu(gagne){
    jeuTermine = true;
    clearInterval(timer); //arrete le timer
    const champ = document.getElementById("saisie");
    const bouton = document.getElementById("envoyer");
    const message = document.getElementById("message-fin");
    champ.disabled = true;
    bouton.disabled = true;

    if (gagne) { //message de victoire/défaite
        message.textContent = `🎉 Bravo ! Tu as trouvé le nombre mystère : ${nombreMystere}`;
    } else {
        message.textContent = `Temps écoulé ! Le nombre était : ${nombreMystere}`;
    }
}

//au chargement de la page :
document.addEventListener("DOMContentLoaded",() => {
    preparerJeu();
    //gestion des évenements 
    document.getElementById("commencer").addEventListener("click", demarrerJeu);
    document.getElementById("envoyer").addEventListener("click", verifierNombre);
    document.getElementById("saisie").addEventListener("keypress", e => {
        if (e.key==="Enter") { //si la touche du clavier tapée est "entrée" c'est comme si on avait appuyé sur le bouton valider
            verifierNombre();
        }
    });
});
