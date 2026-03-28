<!--Cette page apparaît après avoir appuyé sur le bouton "s'inscrire". Peut afficher un message de succès ou d'erreur mais redirige directement vers une page suivant le cas-->
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Club Info | Inscription</title>
    <link rel="stylesheet" href="style/style.css">
</head>

<body>
    <header>
        <h1>Bienvenue sur le site du Club Informatique</h1>
    </header>

    <div class="form-container">
        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {

            //Variables des données du formulaire
            $nom = $_POST["nom"];
            $prenom = $_POST["prenom"];
            $date_naissance = $_POST["date_naissance"];
            $adresse = $_POST["adresse"];
            $telephone = $_POST["telephone"];
            $email = $_POST["email"]; //penser à si l'adresse mail existe déjà dans la liste d'abonnés
            $password = $_POST["password"];
            $confirm_password = $_POST["confirm_password"];

            //Vérification du mot de passe (cette partie a été ajoutée après que nous nous sommes rendus compte que nous n'avons pas inclus de mot de passe à entrer pour l'inscription)
            if ($password !== $confirm_password) {
                echo "<div class='error-message'>Les mots de passe ne correspondent pas.</div>";
                echo "<div>Vous serez automatiquement redirigé à la page d'inscription dans quelques instants.</div>";
                header("Refresh: 3; URL=inscription.html"); //retour à l'inscription automatique après 3 secondes
                die;
            }
            
            //code précédent trop complexe, une IA m'a proposé d'utiliser DateTime 
            $date_naissance2 = new DateTime($date_naissance); //convertit la date entrée dans le formulaire pour une manipulation facile
            $date_actuelle = new DateTime(); //prend la date actuelle 
            //calcul de la différence de date (l'age) en une seule ligne, au lieu de chercher les valeurs de l'année, du mois et du jour, et de calculer la différence et puis d'additionner le tout
            $age = $date_actuelle->diff($date_naissance2)->y; 
            //La méthode "diff" permet de calculer la différence entre deux dates et return une intervalle de date.
            //"->y" donne la différence en années, on l'utilise pour récupérer l'âge en années directement.

            if ($age < 18) {
                echo "<div class='error-message'>Il faut être majeur pour pouvoir s'inscrire.</div>";
                echo "<div>Vous serez automatiquement redirigé à la page d'inscription dans quelques instants.</div>";
                header("Refresh: 3; URL=inscription.html"); //retour à l'inscription automatique après 3 secondes
                die;
            }
            
            $hashed_password = password_hash($password, PASSWORD_DEFAULT); //hashage du mot de passe pour plus de sécurité

            //Ajout des données dans le fichier liste_abonne.json
            $abonne = [
                "nom" => $nom,
                "prenom" => $prenom,
                "date_naissance" => $date_naissance,
                "adresse" => $adresse,
                "telephone" => $telephone,
                "email" => $email,
                "password" => $hashed_password //mot de passe hashé donc apparaît crypté dans le fichier data
            ]; // On attribue les données entrées à l'abonné
            $fichier = "data/liste_abonne.json";
            if (file_exists($fichier)) {
                $liste_abonne = json_decode(file_get_contents($fichier), true); //lecture du fichier data
            } else {
                $liste_abonne = []; // Si le fichier n'existe pas, on initialise un tableau vide (on sait jamais)
            }
            foreach ($liste_abonne as $abonne_existant) { //équivalent en python à "for abonne_existant in liste_abonne"
                if ($abonne_existant["email"] === $email) {
                    echo "<div class='error-message'>Cet e-mail est déjà utilisé.</div>";
                    echo "<div>Vous serez automatiquement redirigé à la page d'inscription dans quelques instants.</div>";
                    header("Refresh: 3; URL=inscription.html"); //retour à l'inscription automatique après 3 secondes
                    die; //arrête le script
                }
            }
            $liste_abonne[] = $abonne; //Ajout des données, cette syntaxe simplifiée permet d'ajouter les données de l'abonné directement à la fin du tableau
            file_put_contents($fichier, json_encode($liste_abonne, JSON_PRETTY_PRINT)); //Ecriture des nouvelles données dans le fichier JSON, JSON_PRETTY_PRINT permet d'améliorer l'affichage en JSON (sauts de lignes, espace) 
            echo "<div class='success-message'>Inscription réussie !</div>";
            echo "<div>Vous serez automatiquement redirigé à la liste des abonnés dans quelques instants.</div>";
            header("Refresh: 3; URL=consultation.html"); //redirection vers consultation/liste des abonnes
        } else {
            echo "<div class='error-message'>Méthode de requête non valide.</div>";
            header("Refresh: 3; URL=inscription.html"); //retour à l'inscription automatique après 3 secondes
        }?>
    </div>
    
    <footer>
        Site créé par Adam TRIRACH & Yanis EL OUARDI
    </footer>
</body>

</html>