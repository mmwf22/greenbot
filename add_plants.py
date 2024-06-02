import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('plants.db')

# Cursor-Objekt erstellen, um SQL-Befehle auszuführen
cursor = conn.cursor()

# Neue Pflanzen hinzufügen (Beispielwerte)
pflanzen = [
    ("Kopfsalat", 30.0, 30.0, 0.1),
    ("Randen", 10.0, 30.0, 2.0),
    ("Ruebli", 1.0, 30.0, 1.0)
]

# SQL-Befehl zum Einfügen von Pflanzen
insert_query = "INSERT INTO Pflanzen (name, pflanzabstand, reihenabstand, saattiefe) VALUES (?, ?, ?, ?)"

# Pflanzen in die Tabelle einfügen
cursor.executemany(insert_query, pflanzen)

# Aenderungen speichern und Verbindung schliessen
conn.commit()
conn.close()

print("Neue Pflanzen erfolgreich zur Datenbank hinzugefuegt.")

