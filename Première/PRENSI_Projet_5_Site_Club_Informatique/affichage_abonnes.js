fetch("data/liste_abonne.json") //charge le fichier json mis à jour 
    .then(response=> { //"then" permet de traiter la réponse en json, "reponse" s'agit donc de la réponse du serveur, "=>" facilite l'écriture de fonction 
        if (!response.ok) { //Si la réponse n'est pas correcte
            throw new Error("Erreur lors du chargement des abonnés."); //Traite une potentielle erreur de fichier, "throw" déclenche une erreur, 
        }
        return response.json(); 
    })
    .then(data=> { //là, on traite les données
        const tbody = document.querySelector("#table-abonnes tbody"); //"querySelector" sélectionne un élément HTML, ici la balise "tbody" avec l'id "table-abonnes" dans le fichier "consultation.html"
        data.forEach(abonne => { //"forEach" agit comme un "for element in table" en python, on boucle sur chaque élément du fichier json 
            const tr = document.createElement("tr"); //création d'une "tablerow" (ligen de table) dans la table de la page "consultation"
            const tdNom = document.createElement("td"); //création de cellules 
            const tdPrenom = document.createElement("td");
            const tdEmail = document.createElement("td");

            tdNom.textContent = abonne.nom; //Affiche le nom et prénom de l'abonné pour chaque ligne
            tdPrenom.textContent = abonne.prenom;
            tdEmail.textContent = abonne.email;

            tr.appendChild(tdNom); //"appendChild" permet d'ajouter un élément "enfant" dans un élément HTML
            tr.appendChild(tdPrenom);
            tr.appendChild(tdEmail);
            tbody.appendChild(tr);
        });
    })
    .catch(error => { //gère une erreur produite dans ".then" plus haut 
        console.error("Erreur :", error); //Affiche le type d'erreur dans la console (pour le développeur), l'affichage pour l'utilisateur ayant été déjà fait plus haut
    });