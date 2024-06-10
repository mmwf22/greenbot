import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('db/plants.db')

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
    ("Broccoli", 40.0, 40.0, 0.2),
    ("Rosenkohl", 50.0, 50.0, 0.2),
    ("Tomaten", 80.0, 80.0, 0.2),
    ("Cherry-Tomaten", 80.0, 80.0, 0.2),
    ("Schnittsalat", 10.0, 10.0, 0.2),
    ("Pak Choi", 30.0, 30.0, 0.2),
    ("Mangold", 25.0, 30.0, 2),
    ("Basilikum", 30.0, 30.0, 0.2),
    ("Petersilie", 2.0, 20.0, 0.2),
    ("Dill", 2.0, 15.0, 0.2)
]

# Funktion zum Reduzieren und Runden der Werte
def reduce_and_round(value):
    return round(value * 0.7, 1)

# SQL-Befehl zum Einfügen von Pflanzen
insert_query = "INSERT INTO Pflanzen (name, pflanzabstand, reihenabstand, saattiefe) VALUES (?, ?, ?, ?)"

# Pflanzen in die Tabelle einfügen
for pflanze in pflanzen:
    # Werte reduzieren und runden (außer saattiefe)
    name = pflanze[0]
    pflanzabstand = reduce_and_round(pflanze[1])
    reihenabstand = reduce_and_round(pflanze[2])
    saattiefe = pflanze[3]

    # Überprüfen, ob die Pflanze bereits vorhanden ist
    cursor.execute("SELECT COUNT(*) FROM Pflanzen WHERE name = ?", (name,))
    result = cursor.fetchone()
    
    if result[0] > 0:
        print(f"Pflanze '{name}' ist bereits in der Datenbank vorhanden.")
    else:
        cursor.execute(insert_query, (name, pflanzabstand, reihenabstand, saattiefe))
        print(f"Pflanze '{name}' erfolgreich zur Datenbank hinzugefügt.")

# Änderungen speichern und Verbindung schließen
conn.commit()
conn.close()

print("Überprüfung und Hinzufügen von Pflanzen abgeschlossen.")
