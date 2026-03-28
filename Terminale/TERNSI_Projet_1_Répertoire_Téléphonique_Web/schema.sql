/* schema.sql */

CREATE TABLE CONTACT (
  id_contact INTEGER PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  date_naissance DATE,
  adresse TEXT,
  profession VARCHAR(100),
  phone_fixe VARCHAR(20),
  phone_portable VARCHAR(20),
  email VARCHAR(255) UNIQUE
);

CREATE TABLE UTILISATEUR (
  id_user INTEGER PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash TEXT NOT NULL, /* le password est crypté */
  id_contact INTEGER,
  FOREIGN KEY (id_contact) REFERENCES CONTACT(id_contact)
);
