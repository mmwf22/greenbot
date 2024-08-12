import sqlite3
import os

# Pfad zur Datenbankdatei
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'db', 'plants.db')


def load_plants_from_db():
    """
    Lädt die Pflanzeninformationen aus der Datenbank.

    Diese Funktion stellt eine Verbindung zur SQLite-Datenbank her,
    führt eine Abfrage durch, um alle Pflanzen mit ihren jeweiligen
    Abständen und Saattiefe abzurufen, und schliesst anschliessend die
    Verbindung.

    Returns:
        list: Eine Liste von Tupeln, wobei jedes Tupel die Informationen
        einer Pflanze enthält (Name, Pflanzabstand, Reihenabstand, Saattiefe).
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, pflanzabstand, reihenabstand, saattiefe FROM Pflanzen"
    )
    plants = cursor.fetchall()
    conn.close()
    return plants
