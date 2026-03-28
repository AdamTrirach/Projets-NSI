<?php
session_start();
header("Content-Type: application/json"); //la réponse renvoyée au serveur sera en format JSON 

//Vérifie si l'email est stocké en session (donc utilisateur connecté)
if (isset($_SESSION["email"])) { //Isset renvoie true si la valeur mise en argument est nulle (donc non définie), ici vérifie si la variable de session "email" est définie. 
    echo json_encode(["authenticated" => true]); //l'utilisateur est authentifié, on renvoie une réponse JSON avec la clé "authenticated" à true
} else {
    echo json_encode(["authenticated" => false]); //l'utilisateur n'est pas authentifié, on renvoie une réponse JSON avec la clé "authenticated" à false
}
?>