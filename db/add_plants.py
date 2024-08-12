import os
import sqlite3

# Pfad zur Datenbankdatei
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'plants.db')

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(db_path)

# Cursor-Objekt erstellen, um SQL-Befehle auszuführen
cursor = conn.cursor()

# Neue Pflanzen hinzufügen (Beispielwerte)
pflanzen = [
    ("Kopfsalat", 30.0, 30.0, 0.2),
    ("Ruebli", 1.0, 30.0, 1.0),
    ("Randen", 10.0, 30.0, 2.0),
    ("Buschbohnen", 5.0, 40.0, 1.0),
    ("Peperoni lang", 40.0, 40.0, 0.2),
    ("Glockenpeperoni", 60.0, 60.0, 0.2),
    ("Chili", 40.0, 40.0, 0.2),
    ("Kohlrabi", 25.0, 25.0, 0.2),
    ("Rosenkohl", 50.0, 50.0, 0.2),
    ("Tomaten", 80.0, 80.0, 0.2),
    ("Cherry-Tomaten", 80.0, 80.0, 0.2),
    ("Schnittsalat", 10.0, 10.0, 0.2),
    ("Mangold", 25.0, 30.0, 2.0),
    ("Petersilie", 2.0, 20.0, 0.2),
    ("Dill", 2.0, 15.0, 0.2)
]

# SQL-Befehl zum Einfügen von Pflanzen
insert_query = """
INSERT INTO Pflanzen (name, pflanzabstand, reihenabstand, saattiefe)
VALUES (?, ?, ?, ?)
"""

# Pflanzen in die Tabelle einfügen
for pflanze in pflanzen:
    cursor.execute(insert_query, pflanze)

# Änderungen speichern und Verbindung schliessen
conn.commit()
conn.close()

print("Pflanzen erfolgreich zur Datenbank hinzugefügt.")
