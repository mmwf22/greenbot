import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('db/plants.db')

# Cursor-Objekt erstellen, um SQL-Befehle auszuführen
cursor = conn.cursor()

# Neue Pflanzen hinzufügen (Beispielwerte)
pflanzen = [
    ("Buschbohnen", 5.0, 40.0, 1.0),
    ("Peperoni lang", 40.0, 40.0, 0.5),
    ("Glockenpeperoni", 60.0, 60.0, 0.5),
    ("Chili", 40.0, 40.0, 0.5),
    ("Kohlrabi", 25.0, 25.0, 0.5),
    ("Broccoli", 40.0, 40.0, 0.5),
    ("Rosenkohl", 50.0, 50.0, 0.5),
    ("Tomaten", 80.0, 80.0, 0.5),
    ("Cherry-Tomaten", 80.0, 80.0, 0.5),
    ("Basilikum", 30.0, 30.0, 0.5),
    ("Petersilie", 2.0, 20.0, 0.5),
    ("Dill", 2.0, 15.0, 0.5)


]

# SQL-Befehl zum Einfügen von Pflanzen
insert_query = "INSERT INTO Pflanzen (name, pflanzabstand, reihenabstand, saattiefe) VALUES (?, ?, ?, ?)"

# Pflanzen in die Tabelle einfügen
for pflanze in pflanzen:
    # Überprüfen, ob die Pflanze bereits vorhanden ist
    cursor.execute("SELECT COUNT(*) FROM Pflanzen WHERE name = ?", (pflanze[0],))
    result = cursor.fetchone()
    
    if result[0] > 0:
        print(f"Pflanze '{pflanze[0]}' ist bereits in der Datenbank vorhanden.")
    else:
        cursor.execute(insert_query, pflanze)
        print(f"Pflanze '{pflanze[0]}' erfolgreich zur Datenbank hinzugefügt.")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Überprüfung und Hinzufügen von Pflanzen abgeschlossen.")
