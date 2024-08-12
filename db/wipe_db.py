import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('db/plants.db', isolation_level=None)

# Cursor-Objekt erstellen, um SQL-Befehle auszuführen
cursor = conn.cursor()

# SQL-Befehl zum Löschen aller Einträge aus der Tabelle
delete_query = "DELETE FROM Pflanzen"

# Alle Einträge aus der Tabelle löschen
cursor.execute(delete_query)

# Resetting the auto-increment counter by rebuilding the table
cursor.execute("DROP TABLE IF EXISTS Pflanzen")
cursor.execute("CREATE TABLE Pflanzen (id INTEGER PRIMARY KEY, name TEXT, pflanzabstand REAL, reihenabstand REAL, saattiefe REAL)")

# Änderungen speichern und Verbindung schliessen
conn.commit()
conn.close()

print("Alle Einträge wurden erfolgreich aus der Datenbank gelöscht, und der Auto-Inkrement-Zähler wurde zurückgesetzt.")
