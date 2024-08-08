import sqlite3
import os

# Pfad zur Datenbankdatei
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'plants.db')

# Verbindung zur SQLite-Datenbank herstellen (falls noch nicht vorhanden, wird sie erstellt)
conn = sqlite3.connect(db_path)

# Cursor-Objekt erstellen, um SQL-Befehle auszuführen
cursor = conn.cursor()

# SQL-Befehl zum Erstellen der Tabelle für Pflanzen
create_table_query = """
CREATE TABLE IF NOT EXISTS Pflanzen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pflanzabstand REAL NOT NULL,
    reihenabstand REAL NOT NULL,
    saattiefe REAL NOT NULL
);
"""

# Tabelle erstellen
cursor.execute(create_table_query)

# Änderungen speichern und Verbindung schliessen
conn.commit()
conn.close()

print("Datenbank 'plants.db' und Tabelle 'Pflanzen' erfolgreich erstellt.")
