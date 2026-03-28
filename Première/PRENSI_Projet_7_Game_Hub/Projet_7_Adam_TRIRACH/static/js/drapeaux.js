//js du jeu des drapeaux

//fonction de normalisation des noms de pays entrés
function normaliserText(str) { //ex : Etats-Unis => etatsunis 
    return str
        .normalize('NFD') //décompose les caractères accentués (ex : à => a`)
        .replace(/[\u0300-\u036f]/g, '') //retire diacritiques (`, cédille etc...) décomposés au préalable
        .replace(/[\s\-\']/g, '') //retire espaces,tirets,apostrophes...
        .toLowerCase();//passe en minuscules
}

document.addEventListener('DOMContentLoaded', () => { //ce code ne s'exécute QUE quand le DOM est prêt
    const container= document.getElementById('drapeaux') ; //rappel const permet de créer une constante nommée accessible uniquement en lecture
    const input =document.getElementById('reponse');
    const timerSpan = document.getElementById('timer');
    const messageFin = document.getElementById('message-fin') ;

    let paysSelect = []; //liste des pays selectionnés
    let normalizedNames = {}; //dictio des noms normalisés
    const guessed = new Set(); //set des pays devinés (évite les doublons comme en python)
    let timeLeft=120; // temps de la partie 120 secondes soit 2 muntes
    let timerId; //référence du timer

    //quand fin du jeu : désactive l'input et affiche un message
    function finGame(message="") {
        clearInterval(timerId); //tabete le timer 
        input.disabled = true; //desactive le champ de reponse
        if (message) {
            messageFin.textContent = message; //affiche message final
        }}

    //mise à jour du timer affiché (minutes:secondes)
    function updateTimer() {
        const minutes = Math.floor(timeLeft/60) ; //ne pas oublier points virgules //mathfloor tabondit
        const seconds = timeLeft%60; 
        timerSpan.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        // padStart(2, '0') assure qu'on a toujours 2 chiffres (ex :05 au lieu de 5)
        if (timeLeft <= 0) { //si temps écoulé
            finGame("Temps écoulé ! Partie terminée.") ;
        }}

    //démtabe le compte à rebours
    function startTimer() {
        updateTimer(); //affichage initial
        timerId = setInterval(() => { //setInterval exécute la fonction toute les 1000ms soit 1 seconde
            timeLeft-- ; //décrémente le temps restant (réduit de 1 seconde)
            updateTimer(); //mise à jour du Timer
        }, 1000) ;}

    //renvoie un échantillon aléatoire de n élements d'un tableau 
    function randomFlags(tableau,n) {
        const tab = tableau.slice(); //créer une copiee du tableau original pour ne pas le modifier
        for (let i = tab.length - 1; i > 0; i--) { //mélange aléatoirement le tableau
            //Algorithme de mélange : Fisher-Yates
            //On parcourt le tableau à l'envers (i part de la fin vers le début)
            //let i= arr.length - 1 commence au dernier élément i > 0 continue jusqu'au deuxième élément i-- décrémente à chaque itération
            const j =Math.floor(Math.random()*(i + 1));
            //math random génère un nombre aléatoire dans l'intervalle [0 ; 1], (i+1) donne un nombre entre 0 et i
            //math floor arrondit à l'entier inférieur
            [tab[i], tab[j]] = [tab[j], tab[i]]; //affectation par destructuration sans variable temporaire
        }
        return tab.slice(0, n); //retourne les n premiers elements du tableau mélangé
    }

    //charge la liste complète des pays et initialise le jeu
    fetch('/static/countries.json') //rappel : fetch permet d'effectuer des requetes réseaux pour récupérer le fichier json
        .then(resp => resp.json()) //transforme la réponse en json
        .then(data => { //traitement des données récupérés
            //choix aléatoire de 10 pays
            paysSelect=randomFlags(data,10);
            
            //préparation des noms normalisés
            paysSelect.forEach(country => { //pour chaque pays sélectionné
                const nameNorm = normaliserText(country.name); //normalise le nom du pays
                // map nom normalisé → code alpha2 (minuscules)
                normalizedNames[nameNorm] = country['alpha-2'].toLowerCase(); //stocke la correspondance entre le nom normalisé et le code alpha2
            }); //rappel apha2code : France => "fr" : Suisse => "ch"

            //création des balises image pour chaque drapeau
            paysSelect.forEach(country => { //pour chaque pays
                const code = country['alpha-2'].toLowerCase(); //récup le code pays
                const img = document.createElement('img'); //cree un nouvel element "img"
                img.src = `/static/svg/${code}.svg`; //récupère le fichier svg (le drapeau) associé au code
                img.alt = country.name; 
                img.dataset.code = code; //stocke le code pays dans un attribut data
                img.classList.add('drapeau'); //ajoute une classe CSS
                img.style.backgroundColor = "white"; //fond blanc par default
                container.appendChild(img); //ajoute l'image au conteneur dans le DOM
            });

            //lancemnt du timer
            startTimer() ;
        });

    //écouteur : à chaque saisie, vérifie la réponse
    input.addEventListener('input', () => {
        const v = normaliserText(input.value); //normalise la saisie 
        if (v in normalizedNames && !guessed.has(v)) { //vérifie si le texte normalisé correspond à un pays ET qu'il n'a pas été déjà trouvé
            guessed.add(v); //si c'est le cas ajoute la pays en question dans ceux devinés dans la partie
            const imgs = container.querySelectorAll(`img[data-code="${normalizedNames[v]}"]`);
            //récupère tous les drapaux correspondant au code du pays trouvé
            imgs.forEach(im => {
                im.style.backgroundColor = '#d4edda'; //fond vert clair (code couleur)
                im.style.border = '2px solid #28a745'; // bordure verte
            });
            input.value='' ; //efface ce qu'il y a dans le champ de saisie quand bonne réponse
        }

        //si tous les drapeaux sont devinés, termine la partie
        if (guessed.size === paysSelect.length) { //si len pays trouvés strictement égal à len pays sélectionnés pour la partie
            finGame("Bravo ! Tu as deviné tous les pays !") ; //affiche le message de succès ! 
        }
    });
});

//ne pas oublier les points virgules
//régler le problème du fichier json
