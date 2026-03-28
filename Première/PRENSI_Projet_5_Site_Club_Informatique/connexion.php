<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Club Info | Connexion</title>
    <link rel="stylesheet" href="style/style.css">
</head>

<body>
    <header>
        <h1>Connexion au Club Informatique</h1>
    </header>
    <?php
    session_start(); // Démarre la session

    // Vérifie si l'utilisateur est déjà connecté
    if (isset($_SESSION["email"])) {
        header("Location: consultation.html");
        exit;
    }

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $email = htmlspecialchars($_POST["email"]);
        $password = htmlspecialchars($_POST["password"]);

        // Lire le fichier JSON contenant les abonnés
        $fichier = "data/liste_abonne.json";
        if (!file_exists($fichier)) {
            die("<div class='error-message'>Fichier des abonnés introuvable.</div>");
        }

        $liste_abonne = json_decode(file_get_contents($fichier), true);
        $connecte = false;

        // Vérification des identifiants
        foreach ($liste_abonne as $abonne) {
            if ($abonne["email"] === $email && password_verify($password, $abonne["password"])) { //vérifie le mot de passe en prenant en copte le hashage
                $_SESSION["email"] = $email; // Stocke l'email en session
                $connecte = true; 
                header("Location: consultation.html");
                exit; //arrete le script
            }
        }

        //si la connexion échoue
        if (!$connecte) {
            echo "<div class='error-message'>Email ou mot de passe incorrect.</div>";
            echo "<div>Vous serez automatiquement redirigé à la page de connexion dans quelques instants.</div>";
            header("Refresh: 3; URL=login.html");
        }
    }
    ?>
    <footer>
        Site créé par Adam TRIRACH & Yanis EL OUARDI
    </footer>
</body>

</html>
     