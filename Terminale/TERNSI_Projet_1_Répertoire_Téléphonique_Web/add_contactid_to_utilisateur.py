import sqlite3, os
DB = "repertoire.db"
if not os.path.exists(DB):
    print("repertoire.db introuvable. Lance initialisation_bd.py d'abord.")
    raise SystemExit(1)

conn = sqlite3.connect(DB)
try:
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(UTILISATEUR);")
    cols = [r[1] for r in cur.fetchall()]
    if "id_contact" in cols:
        print("La colonne id_contact existe déjà dans UTILISATEUR.")
    else:
        cur.execute("ALTER TABLE UTILISATEUR ADD COLUMN id_contact INT;")
        conn.commit()
        print("Colonne id_contact ajoutée à UTILISATEUR.")
finally:
    conn.close()
