<?php
session_start(); //lancer une session
//vérifier si l'admin est connecté (encore on sait jamais)
if (!isset($_SESSION["admin"]) || $_SESSION["admin"] !== true) { //isset retourne false si la valeur est nulle/non définie
    die("Accès refusé.");} //arrete le script 
//vérifier si l'index de l'abonné à supp est envoyé 
if (isset($_POST["index"])) {
    $fichier = "data/liste_abonne.json";
    if (file_exists($fichier)){ //vérifie si le fichier existe
        $liste_abonne = json_decode(file_get_contents($fichier), true); //lecture du fichier
    }
    else {
        $liste_abonne = []; //en cas de problème avec le fichier, on renvoie un tableau vide pour éviter des erreurs récurrentes
    }
    $index = intval($_POST["index"]); //pour info, intval = int() en python
    if (isset($liste_abonne[$index])) {
        array_splice($liste_abonne, $index, 1); //cette commande modifie une table en supprimant/remplaçant/ajoutant des éléments, ici supprime l'abonne via l'index donné
        file_put_contents($fichier,json_encode($liste_abonne, JSON_PRETTY_PRINT)); //pour rappel JSON_PRETTY_PRINT permet de soigner l'écriture dans unf cihier json
    }
}

//redirection vers la page admin
header("Location: admin_page.php");
exit(); //arrete le script
?>
