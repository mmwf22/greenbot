import sqlite3
import os

# Pfad zur Datenbankdatei
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'db', 'plants.db')

def load_plants_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, pflanzabstand, reihenabstand, saattiefe FROM Pflanzen")
    plants = cursor.fetchall()
    conn.close()
    return plants
