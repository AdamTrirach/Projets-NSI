<?php
session_start(); //on commence la session (explication du concept de session en commentaires du fichier "connexion.php")
//vérifier si l'admin est connecté
if (!isset($_SESSION["admin"]) || $_SESSION["admin"] !== true) {
    die("<div class='error-message'>Accès refusé. <a href='admin.html' class='button-link'>Retour</a></div>");
}
//charger la liste des abonnés contenue dans "liste_abonne.json"
$fichier = "data/liste_abonne.json";
if (file_exists($fichier)){ //vérifie si le fichier existe
    $liste_abonne = json_decode(file_get_contents($fichier), true); //lecture du fichier
}
else {
    $liste_abonne = []; //en cas de problème avec le fichier, on renvoie un tableau vide pour éviter des erreurs récurrentes
} ?> 

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Club Info | Admin</title>
    <link rel="stylesheet" href="style/style.css">
</head>

<body>
    <header>
        <h1>Gestion des abonnés</h1>
        <nav>
            <ul>
                <li><a href="admin_logout.php">Déconnexion Admin</a></li>
            </ul>
        </nav>
    </header>

    <div>
        <table border="1">
            <thead>
                <tr>
                    <th>Nom</th>
                    <th>Prénom</th>
                    <th>Date de naissance</th>
                    <th>Adresse</th>
                    <th>Téléphone</th>
                    <th>Email</th>
                    <th>Suppression</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($liste_abonne as $index => $abonne) : ?>
                    <tr>
                        <td><?=$abonne["nom"] ?></td>
                        <td><?=$abonne["prenom"] ?></td>
                        <td><?=$abonne["date_naissance"] ?></td>
                        <td><?=isset($abonne["adresse"]) ? $abonne["adresse"] : "Aucun" ?></td> <!-- isset return false si la variable contient une valeur nulle/non définie ; format condition ? action si condition vraie : si condition fausse-->
                        <td><?=$abonne["telephone"] ?></td>
                        <td><?=$abonne["email"] ?></td>
                        <td>
                            <form action="supprimer_abonne.php" method="POST"> <!--La suppression se fait en php-->
                                <input type="hidden" name="index" value="<?php echo $index;?>"> <!-- cela permet de stocker des données (ici l'index, càd la position de l'abonné dans le fichier json) sans qu'ils soient affiché pour l'utilisateur dans un formulaire-->
                                <button type="submit" class="button-delete">Supprimer</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?> <!--termine la boucle forEach-->
            </tbody>
        </table><br><br>
    </div>

    <footer>
        Site créé par Adam TRIRACH & Yanis EL OUARDI
    </footer>
</body>

</html>