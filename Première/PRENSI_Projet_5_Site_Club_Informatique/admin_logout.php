<?php
session_start(); //lance la session
session_destroy(); //termine la session (après une séance de débugage, une IA m'a recommandé d'ajouter cela)
header("Location: admin.html"); //redirige vers admin.html
exit(); //arrête le script
?>
