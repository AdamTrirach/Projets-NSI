<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Club Info | Admin</title>
    <link rel="stylesheet" href="style/style.css">
</head>

<body>
    <header>
        <h1>Espace Administrateur</h1>
        <nav>
            <ul>
                <li><a href="index.html">Accueil</a></li>
                <li><a href="inscription.html">Inscription</a></li>
                <li><a href="consultation.html">Liste des abonnés</a></li>
                <li><a href="admin.html">Espace Admin</a></li>
            </ul>
        </nav>
    </header>

    <div class="form-container">
        <?php
        session_start(); //démarrer la session

        //id admin requis (un seul existe)
        $admin_id = "admin231";
        $admin_mdp = "jpxrd456!";
        $identifiant = $_POST["identifiant"];
        $mot_de_passe = $_POST["mot_de_passe"];

        //vérif
        if ($identifiant === $admin_id && $mot_de_passe === $admin_mdp) {
            $_SESSION["admin"] = true; //stocker l'info dans la session 
            header("Location: admin_page.php"); //rediriger vers la page admin
            exit(); //arrête le script 
        } else {
            echo "<div class='error-message'>Identifiant ou mot de passe incorrect !</div>";
            echo "<a href='admin.html' class='button-link'>Retour</a>";
        }
        ?>
    </div>

    <footer>
        Site créé par Adam TRIRACH & Yanis EL OUARDI
    </footer>
</body>

</html>
